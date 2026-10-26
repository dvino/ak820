import importlib.util, io, tarfile, tempfile, hashlib, json, stat
from pathlib import Path
p=Path('/home/danil/ChatGPT/ak820-beta2-20261025/audits/rc6/beta2-release-20261025/verify-public-assets.py')
s=importlib.util.spec_from_file_location('reviewed',p); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
def f(name, kind='file', target='', mode=0o751): return (name,kind,target,mode)
results=[]
with tempfile.TemporaryDirectory(prefix='ak820-independent-tar-') as tmp:
 root=Path(tmp)
 def run(label, entries, accept=False, expected=None):
  path=root/(label+'.tar.gz')
  with tarfile.open(path,'w:gz') as t:
   for name,kind,target,mode in entries:
    m=tarfile.TarInfo(name); m.mode=mode
    if kind=='file': m.size=3; t.addfile(m,io.BytesIO(b'abc'))
    else:
     m.type={'sym':tarfile.SYMTYPE,'hard':tarfile.LNKTYPE,'dir':tarfile.DIRTYPE,'fifo':tarfile.FIFOTYPE,'char':tarfile.CHRTYPE}[kind]; m.linkname=target; t.addfile(m)
  try:
   files,modes=v.tar_contents(path)
   if not accept: raise AssertionError('unexpected acceptance '+label)
   if expected is not None: assert set(files)==set(expected),(label,files)
   dest=root/(label+'-out'); v.check_safe_extract(files,dest,modes)
   for n,b in files.items():
    out=dest/n; assert out.read_bytes()==b==b'abc'; assert not out.is_symlink(); assert stat.S_IMODE(out.stat().st_mode)==modes[n]&0o777
   results.append({'case':label,'result':'PASS accepted; regular bytes/modes checked'})
  except ValueError as e:
   if accept: raise
   results.append({'case':label,'result':'PASS rejected','reason':str(e)})
 run('relative-sibling',[f('p/data'),f('p/link','sym','data',0o000)],True,['p/data','p/link'])
 run('parent-relative',[f('p/data'),f('p/sub/link','sym','../data')],True,['p/data','p/sub/link'])
 run('hard-root-relative',[f('p/data'),f('else/link','hard','p/data')],True,['p/data','else/link'])
 run('real-directory-dotdot',[f('p/sub','dir'),f('p/data'),f('p/link','sym','sub/../data')],True,['p/data','p/link'])
 run('forward-chain',[f('p/a','sym','b'),f('p/b','hard','p/c'),f('p/c')],True,['p/a','p/b','p/c'])
 for label,entries in [
 ('absolute-member',[f('/escape')]),('parent-member',[f('../escape')]),('dot-member',[f('p/./x')]),('double-slash-member',[f('p//x')]),
 ('duplicate-file',[f('p/x'),f('p/x')]),('duplicate-directory',[f('p/','dir'),f('p','dir')]),('directory-file-collision',[f('p','dir'),f('p')]),
 ('absolute-sym',[f('p/a','sym','/etc/passwd')]),('absolute-hard',[f('p/a','hard','/etc/passwd')]),
 ('escape-sym',[f('p/a','sym','../../escape')]),('escape-hard',[f('p/a','hard','../escape')]),('backslash-target',[f('p/a','sym','..\\escape')]),
 ('missing-sym',[f('p/a','sym','absent')]),('missing-hard',[f('p/a','hard','p/absent')]),
 ('self-cycle',[f('p/a','sym','a')]),('mixed-cycle',[f('p/a','sym','b'),f('p/b','hard','p/a')]),
 ('directory-target',[f('p','dir'),f('alias','sym','p')]),('directory-alias-child',[f('p','dir'),f('alias','sym','p'),f('alias/file')]),
 ('file-ancestor',[f('p'),f('p/file')]),('link-ancestor',[f('p','sym','real'),f('real'),f('p/file')]),
 ('fifo',[f('p/fifo','fifo')]),('char-device',[f('p/dev','char')]),('empty-target',[f('p/a','sym','')]),('missing-component-dotdot',[f('p/data'),f('p/link','sym','missing/../data')]),('file-component-dotdot',[f('p/data'),f('p/file'),f('p/link','sym','file/../data')]),('hard-missing-component',[f('p/data'),f('p/link','hard','p/missing/../data')])]: run(label,entries)
print(json.dumps({'verifier_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cases':results},indent=2))
