#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
import ak820_register_saves as trim

ASM='''\t.module test
\t.area CSEG
; function leaf
_leaf:
\tmov a,#42
\tmov dpl,#42
\tret
; function caller
_caller:
 ar0 = 0x00
 ar1 = 0x01
\tpush ar0
\tpush ar1
\tlcall _leaf
\tpop ar1
\tpop ar0
\tret
'''
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.source=self.root/'input'; (self.source/'quantum').mkdir(parents=True)
        self.asm=self.source/'quantum/test.asm'
    def fixture(self,text=ASM):
        self.asm.write_text(text)
        enc={'mov a,#42':'742a','mov dpl,#42':'75822a','ret':'22','push ar0':'c000','push ar1':'c001','pop ar0':'d000','pop ar1':'d001','lcall _leaf':'120000'}
        out=[];address=0
        for n,l in enumerate(text.splitlines(),1):
            text=l.strip()
            if text.startswith('lcall _'): enc[text]='120000'
            if text=='mov r0,#42': enc[text]='782a'
            if text in enc:
                b=enc[text];out.append(f'{address:06X} '+ ' '.join(b[i:i+2].upper() for i in range(0,len(b),2))+f' [12] {n} {l.strip()}\n');address+=len(b)//2
        self.asm.with_suffix('.lst').write_text(''.join(out))
    def plan(self): return trim.prepare(self.source,self.root/'output',self.root/'report.json')
    def test_match(self):
        self.fixture();r=self.plan();self.assertEqual(r['estimated_object_saved_bytes'],8)
        self.assertNotIn('push', (self.root/'output/quantum/test.asm').read_text())
        self.assertEqual(self.asm.read_text(),ASM)
    def test_unknown_fails_closed(self):
        for bad in ['mov psw,#0','mov 0x00,#1','mov @r0,a','movx @dptr,a','mov a,sp','reti','sjmp _leaf','.db 0','push ar0','_alternate:', 'mov secret,a']:
            with self.subTest(bad=bad):
                self.fixture(ASM.replace('mov a,#42','mov a,#42\n\t'+bad));self.assertFalse(self.plan()['groups'])
                import shutil;shutil.rmtree(self.root/'output')
    def test_alias_bank_reject(self):
        self.fixture(ASM.replace('ar0 = 0x00','ar0 = 0x08'));self.assertFalse(self.plan()['groups'])
    def test_duplicate_symbol(self):
        self.fixture(ASM+'\n; function leaf\n_leaf:\n\tret\n');self.assertFalse(self.plan()['groups'])
    def test_wrong_pop_order(self):
        self.fixture(ASM.replace('pop ar1\n\tpop ar0','pop ar0\n\tpop ar1'));self.assertFalse(self.plan()['groups'])
    def test_unresolved_call(self):
        self.fixture(ASM.replace('_leaf:', '_missing:'));self.assertFalse(self.plan()['groups'])
    def test_transitive_clobber(self):
        text=ASM.replace('mov a,#42','mov r0,#42').replace('lcall _leaf','lcall _middle')
        text+='\n; function middle\n_middle:\n\tlcall _leaf\n\tret\n'
        self.fixture(text);r=self.plan()
        self.assertEqual(len(r['groups']),1)
        self.assertEqual(r['groups'][0]['preserved'],['ar1'])
    def test_recursive_closure(self):
        self.fixture(ASM.replace('mov a,#42','lcall _leaf'));self.assertFalse(self.plan()['groups'])
    def test_two_calls_and_duplicate_push(self):
        for text in [ASM.replace('lcall _leaf','lcall _leaf\n\tlcall _leaf'), ASM.replace('push ar1','push ar0')]:
            self.fixture(text);self.assertFalse(self.plan()['groups'])
            import shutil;shutil.rmtree(self.root/'output')
    def test_opcode_tamper(self):
        self.fixture();p=self.asm.with_suffix('.lst');p.write_text(p.read_text().replace('C0 00','C0 D0'));self.assertFalse(self.plan()['groups'])
    def test_listing_mismatch(self):
        self.fixture();self.asm.write_text(ASM.replace('#42','#43'))
        with self.assertRaises(ValueError):self.plan()
    def test_decoder(self):
        self.assertEqual(trim.decode('mov','r7,#255',bytes.fromhex('7fff')),{7})
        for op,args,b in [('mov','r7,#255','78ff'),('lcall','00100$','120000'),('mov','psw,#0','75d000')]:
            self.assertIsNone(trim.decode(op,args,bytes.fromhex(b)))
    @unittest.skipUnless(os.environ.get('AK820_ASSEMBLER'),'real assembler not configured')
    def test_real_cfg_and_alias_adversaries(self):
        cases=[
            ('harvard-read',ASM.replace('mov a,#42','mov dptr,#0x2100\n\tmovx a,@dptr\n\tmovc a,@a+dptr\n\tmov a,#42'),8),
            ('private-frame',ASM.replace('mov a,#42','push ar0\n\tmov a,#42\n\tpop ar0'),4),
            ('cfg-union',ASM.replace('mov a,#42','mov a,#42\n\tjz 00100$\n\tmov r0,#42\n00100$:'),4),
            ('cfg-bad-join',ASM.replace('mov a,#42','mov a,#42\n\tjz 00100$\n\tpush ar0\n00100$:'),0),
            ('callee-bank-write',ASM.replace('mov a,#42','mov psw,#8'),0),
            ('callee-stack-alias',ASM.replace('mov a,#42','mov a,sp'),0),
            ('callee-iram-indirect',ASM.replace('mov a,#42','mov a,@r0'),0),
            ('callee-xdata-write',ASM.replace('mov a,#42','movx @dptr,a'),0),
            ('callee-computed-jump',ASM.replace('mov a,#42','jmp @a+dptr'),0),
            ('caller-write-outside',ASM.replace('push ar0','movx @dptr,a\n\tpush ar0'),8),
            ('caller-interior-entry',ASM.replace('push ar0','jz 00101$\n\tpush ar0').replace('pop ar1','00101$:\n\tpop ar1'),0),
        ]
        import shutil
        for label,text,saving in cases:
            with self.subTest(label=label):
                self.asm.write_text(text)
                subprocess.run([os.environ['AK820_ASSEMBLER'],'-plosgffw',str(self.asm.with_suffix('.rel')),str(self.asm)],check=True)
                self.assertEqual(self.plan()['estimated_object_saved_bytes'],saving)
                shutil.rmtree(self.root/'output')
    @unittest.skipUnless(os.environ.get('AK820_ASSEMBLER'),'real assembler not configured')
    def test_real_assembly(self):
        self.asm.write_text(ASM)
        assembler=os.environ['AK820_ASSEMBLER']
        subprocess.run([assembler,'-plosgffw',str(self.asm.with_suffix('.rel')),str(self.asm)],check=True)
        report=self.plan();out=self.root/'output/quantum/test.asm'
        subprocess.run([assembler,'-plosgffw',str(out.with_suffix('.rel')),str(out)],check=True)
        trim.verify_assembled(self.source,self.root/'output',self.root/'report.json',report)
        self.assertEqual(report['object_saved_bytes'],8)
if __name__=='__main__':unittest.main()
