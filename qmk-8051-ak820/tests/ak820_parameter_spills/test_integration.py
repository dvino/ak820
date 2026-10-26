import copy,json,re,unittest,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
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
 def test_ast_identity_stays_strict(self):
  candidate=self.candidate('normal')
  self.assertFalse(proof.source_proof(candidate,self.raw,self.ast.replace('FUNCTION (_normal=', 'FUNCTION (_other=',1),self.pre)[0])
  self.assertFalse(proof.source_proof(candidate,self.raw,self.ast+'\nFUNCTION (_normal=duplicate)\n',self.pre)[0])
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
 def capture_fixture(self,base,returncode=0):
  root=base/'root';obj=base/'obj';destination=base/'metadata';toolchain=base/'toolchain'
  root.mkdir();obj.mkdir();toolchain.mkdir();(root/'unit.c').write_text('int unit;\n')
  original=obj/'unit.asm';original.write_text('mov a,#1\n')
  (obj/'cflags.txt').write_text('-mmcs51 --model-large')
  (obj/'unit.d').write_text(str(original)+': unit.c\n')
  sdcc=toolchain/'bin'/'sdcc';sdcc.parent.mkdir();sdcc.write_text('compiler')
  ast=(OUT/'adversaries-noasm.ast.txt').read_bytes();warnings=b'warning: synthetic compiler diagnostic\n'
  def run(command,**kwargs):
   if '-E' in command:
    deparg=next(arg for arg in command if arg.startswith('-Wp,-MD,-MF,'))
    Path(deparg.rsplit(',',1)[1]).write_text('unit.pre.o: unit.c\n')
    return SimpleNamespace(stdout=b'int unit;\n',stderr=b'',returncode=0)
   (Path(kwargs['cwd'])/'unit.asm').write_text(original.read_text())
   (Path(kwargs['cwd'])/'unit.dumpraw0').write_text('raw')
   return SimpleNamespace(stdout=ast,stderr=warnings,returncode=returncode)
  return root,obj,destination,sdcc,{(root/'unit.c').resolve():proof.sha(root/'unit.c')},run,ast,warnings
 def test_capture_keeps_ast_and_hashes_separate_diagnostics(self):
  with tempfile.TemporaryDirectory() as d:
   fixture=self.capture_fixture(Path(d));root,obj,destination,sdcc,inputs,run,ast,warnings=fixture
   with patch.object(proof.subprocess,'run',side_effect=run):
    record=proof.capture(root,obj,'unit.asm',destination,sdcc,inputs)
   ast_path=destination/'unit.ast.log';diagnostics=destination/'unit.diagnostics.log'
   self.assertEqual(ast_path.read_bytes(),ast);self.assertEqual(diagnostics.read_bytes(),warnings)
   hashes=record['files_sha256'];self.assertEqual(hashes['unit.ast.log'],proof.sha(ast_path));self.assertEqual(hashes['unit.diagnostics.log'],proof.sha(diagnostics))
 def test_capture_nonzero_still_fails(self):
  with tempfile.TemporaryDirectory() as d:
   root,obj,destination,sdcc,inputs,run,*_=self.capture_fixture(Path(d),returncode=1)
   with patch.object(proof.subprocess,'run',side_effect=run):
    with self.assertRaisesRegex(ValueError,'Typed SDCC capture failed'):
     proof.capture(root,obj,'unit.asm',destination,sdcc,inputs)
if __name__=='__main__':unittest.main()
