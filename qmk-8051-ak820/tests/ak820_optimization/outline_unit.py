#!/usr/bin/env python3
"""Focused safety gates for the exact 8051 outliner; no compiler or USB needed."""
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'util'))
import ak820_outline_audit as outline


BODY=[('mov','dptr,#_private','900000'),('mov','r0,#0x11','7811'),
      ('mov','r1,#0x22','7922'),('mov','b,#0x33','75f033')]


def listing(path, entries):
    """Construct small SDAS-style listing fixtures with exact instruction size."""
    path.parent.mkdir(parents=True,exist_ok=True)
    assembly=[];rows=[];address=0
    for number,entry in enumerate(entries,1):
        if isinstance(entry,str):assembly.append(entry);continue
        opcode,operands,data=entry
        source='\t'+opcode+'\t'+operands
        assembly.append(source)
        # The unresolved symbol uses the actual SDAS relocation marker format.
        encoded='90r00r00' if operands=='dptr,#_private' else ' '.join(data[i:i+2].upper() for i in range(0,len(data),2))
        rows.append(f'      {address:06X} {encoded:<20} [24] {number:4d} {source}')
        address+=len(data)//2
    path.write_text('\n'.join(assembly)+'\n')
    path.with_suffix('.lst').write_text('\n'.join(rows)+'\n')


class OutliningGates(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='ak820-outline-unit-')
        self.directory=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def parse(self):return outline.parse_dce(self.directory,'.lst')[0]
    def source(self,name,body,extra=()):
        listing(self.directory/'quantum'/name,
                ['\t.area CSEG (CODE)','ar0 = 0x00','ar1 = 0x01',*extra,'_function:']+body)

    def test_forbidden_instruction_operands(self):
        for opcode,operands in [('lcall','_f'),('ret',''),('reti',''),('ljmp','_f'),
                                ('jnz','00001$'),('push','acc'),('pop','acc'),
                                ('movc','a,@a+dptr'),('mov','a,@r0'),('mov','@r1,a'),
                                ('mov','a,sp'),('mov','psw,a'),('mov','a,_direct'),
                                ('mov','dptr,#(00101$-.)'),('mov','a,#(.+1)')]:
            with self.subTest(opcode=opcode,operands=operands):self.assertFalse(outline.allowed(opcode,operands))
        for opcode,operands in [('movx','a,@dptr'),('movx','@dptr,a'),('mov','b,a'),
                                ('anl','ar0,#0x1f'),('clr','c'),('mov','dptr,#(_var+0x1)')]:
            self.assertTrue(outline.allowed(opcode,operands))

    def test_label_boundaries(self):
        body=BODY[:2]+['00101$:']+BODY[2:]+['00102$:']+BODY[:2]+['00103$:']+BODY[2:]
        self.source('labels.asm',body)
        self.assertEqual(outline.occurrences(self.parse()),[])

    def test_private_symbol_identity(self):
        self.source('one.asm',BODY)
        self.source('two.asm',BODY)
        self.assertEqual(outline.occurrences(self.parse()),[])
        self.source('one.asm',BODY+['_again:']+BODY)
        groups=outline.occurrences(self.parse())
        self.assertTrue(groups)
        self.assertTrue(all(len({s[0].module for s in group[3]})==1 for group in groups))

    def test_global_symbols_and_relocation_markers(self):
        self.source('one.asm',BODY,extra=['\t.globl _private'])
        self.source('two.asm',BODY,extra=['\t.globl _private'])
        groups=outline.occurrences(self.parse())
        self.assertEqual(len(groups),1)
        saving,size,key,matches=groups[0]
        self.assertEqual((saving,size,len(matches)),(3,10,2))
        self.assertEqual(matches[0][0].data,bytes.fromhex('900000'))

    def test_hardware_sections_and_bank_aliases_excluded(self):
        listing(self.directory/'driver.asm',['\t.area CSEG (CODE)']+BODY+BODY)
        self.source('other_area.asm',BODY+BODY,extra=['\t.area AK820LOW (CODE)'])
        self.source('bank_one.asm',BODY+BODY,extra=['ar0 = 0x08'])
        self.assertEqual(self.parse(),[])

    def test_overlaps_are_removed(self):
        self.source('overlap.asm',BODY*4)
        selected=outline.select(self.parse(),max_helpers=8,min_saving=1)
        seen=set()
        for candidate in selected:
            for sequence in candidate[3]:
                for insn in sequence:
                    cell=(insn.module,insn.line)
                    self.assertNotIn(cell,seen);seen.add(cell)

    def test_repeated_apply_rejected_readonly_parse_allowed(self):
        self.source('repeat.asm',BODY+['_again:']+BODY)
        selected=outline.select(self.parse(),min_saving=1)
        target=self.directory.parent/(self.directory.name+'-outlined')
        try:
            outline.outline_dce(self.directory,target,selected)
            with self.assertRaisesRegex(ValueError,'already outlined'):
                outline.outline_dce(target,self.directory/'second',[])
            with self.assertRaisesRegex(ValueError,'already outlined'):
                outline.outline_assembled(target,self.directory/'third')
            # Even an empty post-link listing is legal for a read-only scan.
            for asm in target.rglob('*.asm'):asm.with_suffix('.lst').write_text('')
            self.assertEqual(outline.parse_dce(target,'.lst')[0],[])
        finally:
            import shutil
            if target.exists():shutil.rmtree(target)


if __name__=='__main__':unittest.main()
