#!/usr/bin/env python3
"""Reject incompatible opt-in ABI and attempts to spoof its assertions."""
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'qmk-8051-ak820/util'))
from build_ak820 import update_block_abi_flag
class Policy(unittest.TestCase):
 def checkflag(self,flags='',names=('eeprom_read_byte',),enabled=True,version='4.6.0',keyboard='ajazz/ak820'):
  return update_block_abi_flag(enabled,keyboard,version,names,flags)
 def test_default_off(self):self.assertEqual(self.checkflag(enabled=False),'')
 def test_supported(self):self.assertEqual(self.checkflag(),' -DAK820_READ_HOOK_PRESERVES_RN=1')
 def test_bad_flags(self):
  for flag in ['--stack-auto','--xstack','--parms-in-bank1','--all-callee-saves','--model-small','--model-medium','--model-huge','--model-flat24','--sdcccall 0','--sdcccall=1','--callee-saves ak820_eeprom_update_block_xdata','--callee-saves=_ak820_eeprom_update_block_xdata','-DAK820_NVM_UPDATE_BLOCK_ASM','-DAK820_READ_HOOK_PRESERVES_RN=1']:
   with self.subTest(flag=flag),self.assertRaises(ValueError):self.checkflag(flags=flag)
 def test_bad_contract(self):
  for kw in [dict(names=()),dict(version='4.4.0'),dict(keyboard='other')]:
   with self.subTest(kw=kw),self.assertRaises(ValueError):self.checkflag(**kw)
if __name__=='__main__':unittest.main()
