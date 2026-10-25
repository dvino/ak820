#!/usr/bin/env python3
"""Offline parser adversaries and optional pinned real-assembler integration."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
import ak820_tailshare as tail

class TailTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def fixture(self, bodies, module='quantum/example.asm'):
        source=self.root/'input'; path=source/module; path.parent.mkdir(parents=True,exist_ok=True)
        lines=['\t.area CSEG\n']; listed=[]; address=0
        for index,body in enumerate(bodies):
            lines += [f'; function f{index}\n', f'_f{index}:\n']
            for text,size in body:
                lines.append('\t'+text+'\n')
                if size:
                    listed.append(f'{address:06X} '+('00 '*size)+f'[12] {len(lines)} {text}\n');address+=size
        path.write_text(''.join(lines)); path.with_suffix('.lst').write_text(''.join(listed))
        return source,path
    def run_plan(self, source):
        return tail.prepare(source,self.root/'output',self.root/'report.json')
    def test_exact_shared_operands_and_alias(self):
        body=[('mov _state,a',2),('mov dpl,#0x42',3),('ret',1)]
        source,path=self.fixture([body,body]); report=self.run_plan(source)
        self.assertEqual(report['estimated_object_saved_bytes'],3)
        result=(self.root/'output'/path.relative_to(source)).read_text()
        self.assertIn('_ak820_tailshare_00000 = .',result)
        self.assertEqual(result.count('mov _state,a'),1)
        self.assertEqual(result.count('ljmp\t_ak820_tailshare_00000'),1)
        self.assertEqual(report['linked_saved_bytes'],None)
    def test_boundaries_and_dangerous_operands(self):
        for index, bad in enumerate(['mov a,@a+pc','mov _SP,a','mov psw,a','mov 0x81,a',
                                      'mov a,00100$','lcall _foo','acall _foo','ajmp _foo','sjmp 00100$',
                                      'push _PSW','mov a,.','movc a,@a+pc']):
            with self.subTest(bad=bad):
                self.root=Path(self.tmp.name)/str(index); self.root.mkdir()
                body=[(bad,3),('ret',1)]
                source,_=self.fixture([body,body]); self.assertFalse(self.run_plan(source)['groups'])
    def test_label_splits_tail(self):
        body=[('mov dpl,#1',3),('00100$:',0),('ret',1)]
        source,_=self.fixture([body,body]); self.assertFalse(self.run_plan(source)['groups'])
    def test_excludes_hardware_modules(self):
        body=[('mov dpl,#1',3),('ret',1)]
        source,_=self.fixture([body,body],'ak820_nvm.asm'); self.assertFalse(self.run_plan(source)['groups'])
    def test_direct_control_alias_fails(self):
        body=[('mov secret,a',2),('mov dpl,#1',3),('ret',1)]
        source,path=self.fixture([body,body])
        # Append definitions so fixture instruction line numbers stay exact.
        path.write_text(path.read_text()+'secret = 0x81\n')
        self.assertFalse(any('secret' in str(group['body']) for group in self.run_plan(source)['groups']))
    def test_distinct_relocation_operands_do_not_match(self):
        source,_=self.fixture([[('mov _one,a',2),('ret',1)], [('mov _two,a',2),('ret',1)]])
        self.assertFalse(self.run_plan(source)['groups'])
    def test_directive_splits_tail(self):
        source,_=self.fixture([[('mov dpl,#1',3),('.even',0),('ret',1)]]*2)
        self.assertFalse(self.run_plan(source)['groups'])
    def test_listing_mismatch_fails(self):
        source,path=self.fixture([[('mov dpl,#1',3),('ret',1)]]*2)
        path.write_text(path.read_text().replace('#1','#2'))
        with self.assertRaisesRegex(ValueError,'mismatch'): self.run_plan(source)
    def test_collision_fails(self):
        source,path=self.fixture([[('mov dpl,#1',3),('ret',1)]]*2)
        path.write_text(path.read_text()+'; '+tail.PREFIX)
        with self.assertRaisesRegex(ValueError,'collision'): self.run_plan(source)
    def test_missing_listing_fails(self):
        source,path=self.fixture([[('ret',1)]])
        path.with_suffix('.lst').unlink()
        with self.assertRaisesRegex(ValueError,'listing'): self.run_plan(source)
    def test_duplicate_listing_fails(self):
        source,path=self.fixture([[('ret',1)]])
        listing=path.with_suffix('.lst'); listing.write_text(listing.read_text()*2)
        with self.assertRaisesRegex(ValueError,'Ambiguous'): self.run_plan(source)

class AssemblerTest(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('AK820_ASSEMBLER'),'set AK820_ASSEMBLER for pinned real assembler')
    def test_alias_keeps_numeric_label_scope_and_relocation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); source=root/'input'; source.mkdir(); (source/'quantum').mkdir()
            asm=source/'quantum/test.asm'
            asm.write_text('''\t.module test
\t.globl _state
\t.area CSEG
; function f
_f:
\tsjmp 00100$
00100$:
\tmov _state,a
\tmov dpl,#0x42
\tret
; function g
_g:
\tsjmp 00100$
00100$:
\tmov _state,a
\tmov dpl,#0x42
\tret
''')
            assembler=os.environ['AK820_ASSEMBLER']
            subprocess.run([assembler,'-plosgffw',str(asm.with_suffix('.rel')),str(asm)],check=True)
            report=tail.prepare(source,root/'output',root/'report.json')
            self.assertEqual(report['estimated_object_saved_bytes'],3)
            rewritten=root/'output/quantum/test.asm'
            subprocess.run([assembler,'-plosgffw',str(rewritten.with_suffix('.rel')),str(rewritten)],check=True)
            tail.verify_assembled(source,root/'output',root/'report.json',report)
            self.assertEqual(report['object_saved_bytes'],3)
            before=asm.with_suffix('.rel').read_text(); after=rewritten.with_suffix('.rel').read_text()
            self.assertIn('_ak820_tailshare_00000',after)
            self.assertIn('_state',after)
            def code_size(text):
                import re
                return int(re.search(r'A CSEG size ([0-9A-Fa-f]+)',text)[1],16)
            self.assertEqual(code_size(before)-code_size(after),3)

if __name__=='__main__': unittest.main()
