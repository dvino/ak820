import copy,json,re,unittest,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"util"))
import ak820_parameter_spills as proof
OUT=Path(__file__).resolve().parent/'fixtures'
class ProofTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(OUT/'adversaries-noasm.dumpraw0').read_text();cls.ast=(OUT/'adversaries-noasm.ast.txt').read_text();cls.pre=(OUT/'adversaries-noasm.i').read_text()
 def candidate(self,name):
  bind=next(l for l in self.raw.splitlines() if '= recv _'+name+' ' in l)
  symbol=re.search(r'\t(_\w+)\s+\[',bind)[1]
  return {'object':symbol,'function':'_'+name}
 def test_source_type_and_escape_real_compiler(self):
  for name,expected in [('normal',True),('volatile_parameter',False),('plain_pointer',True),('volatile_pointer',False),('volatile_pointee',True),('escaped_parameter',False),('macro_hidden_volatile',False)]:
   with self.subTest(name=name):self.assertEqual(proof.source_proof(self.candidate(name),self.raw,self.ast,self.pre)[0],expected)
 def test_ambiguous_recv(self):
  self.assertFalse(proof.source_proof(self.candidate('normal'),self.raw+self.raw,self.ast,self.pre)[0])
 def test_missing_preprocessed(self):
  self.assertFalse(proof.source_proof(self.candidate('normal'),self.raw,self.ast,'')[0])
 def test_inline_asm_source(self):
  self.assertFalse(proof.source_proof(self.candidate('normal'),self.raw,self.ast,self.pre+'\n__asm nop __endasm;')[0])
 def test_string_and_line_are_not_asm(self):
  self.assertTrue(proof.source_proof(self.candidate('normal'),self.raw,self.ast,self.pre+'\n#line 1 "asm/file.h"\nconst char *x="__asm";')[0])
 def test_no_debug_type_shortcut(self):
  adb=(OUT/'debug.adb').read_text()
  normal=re.search(r'S:Ladversaries.normal\$value.*?(\(\{2\}SI:U\))',adb)[1]
  volatile=re.search(r'S:Ladversaries.volatile_parameter\$value.*?(\(\{2\}SI:U\))',adb)[1]
  self.assertEqual(normal,volatile) # Actual debug metadata loses the qualifier.
 def test_escaped_literal_does_not_hide_assembly(self):
  self.assertFalse(proof.source_proof(self.candidate('normal'),self.raw,self.ast,self.pre+'\nconst char*x="a\\\\\\\""; __asm nop __endasm;')[0])
 def test_lexer_unterminated(self):
  with self.assertRaises(ValueError):proof.strip_c_literals('/*')
 def test_canonical_comments_and_literals(self):
  self.assertEqual(proof.canonical('mov a, r0 ; hi'),proof.canonical(' mov a,r0'))
  self.assertNotEqual(proof.canonical('.ascii "a;b"'),proof.canonical('.ascii "a"'))
 def test_mixed_abi_flags(self):
  with tempfile.TemporaryDirectory() as d:
   obj=Path(d)
   for flags in ['-mmcs51 --model-large --stack-auto','-mmcs51 --model-large --sdcccall 1','-mmcs51 --model-small']:
    (obj/'cflags.txt').write_text(flags)
    with self.assertRaises(ValueError):proof.compiler_flags(obj)
 def test_postlink_rejects_wrong_image(self):
  with tempfile.TemporaryDirectory() as d:
   b=Path(d);cert=b/'context.json';cert.write_text('{}')
   (b/'ajazz_ak820_vial.ihx').write_text('image');(b/'ajazz_ak820_vial.map').write_text('map')
   stack=b/'stack.json';stack.write_text(json.dumps({'identity':{'ihx_sha256':'wrong','map_sha256':'wrong'}}))
   with self.assertRaises(ValueError):proof.postlink_audit(b,b,cert,b/'result.json',{'context_sha256':proof.sha(cert)},stack)
if __name__=='__main__':unittest.main()
