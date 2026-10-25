"""Bounded admission and architectural-state model; not a simulator test."""
import copy,random,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
import ak820_parameter_spills as proof

class RestoreTests(unittest.TestCase):
 def fixture(self,tail='mov dptr,#0x1234',encoded='901234',gap='',address=13):
  directory=tempfile.TemporaryDirectory();self.addCleanup(directory.cleanup);root=Path(directory.name)
  (root/'f.asm').write_text('mov a,dpl\n'+gap+tail+'\n')
  end={'line':1,'address':11,'op':'mov','args':'a,dpl','bytes':'e582'}
  body=[end]
  if tail:body.append({'line':2+gap.count('\n'),'address':address,'op':tail.split(' ')[0],'args':tail.split(' ',1)[-1],'bytes':encoded})
  c={'module':'f.asm','function':'_f','entry':[end],'boundary_state_replacement_only':['mov r7,dpl','mov a,r7','mov dptr,#(_formal+0x0000)'],'replacement_bytes':6,'net_bytes':7}
  inv=proof.Inventory(root,[{'module':'f.asm','name':'_f','body':body}],{}, {},set(),{})
  return c,inv
 def test_admitted_and_report_boundary(self):
  c,inv=self.fixture(gap=';comment\n\n');proof.choose_emitted_replacement(c,inv)
  self.assertEqual(c['emitted_replacement'],c['boundary_state_replacement_only'][:-1])
  self.assertFalse(c['dptr_restore_elision']['prefix_endpoint_equivalent'])
  self.assertEqual((c['net_bytes'],c['replacement_bytes']),(10,3))
 def test_barriers_and_bad_bytes(self):
  cases=[dict(tail='mov dpl,#0x34',encoded='758234'),dict(tail='lcall _f',encoded='120000'),dict(tail='sjmp 1$',encoded='8000'),dict(tail='movx a,@dptr',encoded='e0'),dict(gap='00001$:\n'),dict(gap='.area CSEG\n'),dict(gap='.db 0\n'),dict(encoded='001234'),dict(encoded='9012'),dict(address=14),dict(tail='')]
  for kwargs in cases:
   with self.subTest(**kwargs):
    c,inv=self.fixture(**kwargs);proof.choose_emitted_replacement(c,inv)
    self.assertEqual(c['emitted_replacement'],c['boundary_state_replacement_only'])
    self.assertEqual(c['net_bytes'],7)
 def test_fixed_immediates_only(self):
  for operand in ('_formal_12','0','65535','0x1234','0XFFFF'):
   with self.subTest(operand=operand):
    c,inv=self.fixture(tail='mov dptr,#'+operand);proof.choose_emitted_replacement(c,inv)
    self.assertTrue(c['dptr_restore_elision']['admitted'])
  for operand in ('.','(.+1)','(.-1)','_formal+1','(_formal+1)','1$','65536','0x10000','-1',"'A"):
   with self.subTest(operand=operand):
    c,inv=self.fixture(tail='mov dptr,#'+operand);proof.choose_emitted_replacement(c,inv)
    self.assertFalse(c['dptr_restore_elision']['admitted'])
 def test_full_architectural_state_model_all_psw_banks(self):
  # The CPU's MOV direct/register and MOVX semantics affect only ACC parity,
  # active-bank registers, DPTR, and the private formal bytes. Other bytes are
  # canaries. PC is compared at the shared continuation, not by code address.
  rng=random.Random(0x8051)
  for psw in range(256):
   for width in range(1,5):
    state={'iram':bytearray(rng.randbytes(256)),'sfr':bytearray(rng.randbytes(128))}
    state['sfr'][0x50]=psw
    for rewritten in (False,True):
     s=copy.deepcopy(state);r=s['iram'];f=s['sfr'];bank=((psw>>3)&3)*8
     tokens=[f[2],f[3],f[0x70],f[0x60]]
     # Representative full reload into r4..r7; assignment order captures A
     # before replacing it, just as the generator does.
     r[bank+4:bank+4+width]=bytes(tokens[:width])
     f[0x60]=tokens[width-1];f[0x50]=(psw&254)|(f[0x60].bit_count()&1)
     if not rewritten:f[2:4]=bytes([0xff,0x22]) # restored formal endpoint
     # The immediate instruction has no reads and no flags.
     f[2:4]=bytes([0x34,0x12])
     if rewritten:self.assertEqual(s,original)
     else:original=s

if __name__=='__main__':unittest.main()
