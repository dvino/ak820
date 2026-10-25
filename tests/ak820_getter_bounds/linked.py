#!/usr/bin/env python3
import argparse,hashlib,importlib.util,itertools,json,re,traceback
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--shard-index',type=int,default=0);ap.add_argument('--shard-count',type=int,default=1);a=ap.parse_args();assert 0<=a.shard_index<a.shard_count;out=a.output;out.mkdir(parents=True,exist_ok=True);root=a.repo/'qmk-8051-ak820'
 iap=mod('iap',root/'tests/ak820_iap/run.py');e=iap.emitted;mem=e.memory;fw=e.Firmware(a.build,a.repo/'toolchains/sdcc-4.6.0/bin/s51',out)
 assert not any(p in fw.code for p in range(0x2600,0x2701))
 asm=a.build/'dce/quantum/dynamic_keymap.asm';text=asm.read_text();abi={}
 for target in ('keymap','encodermap'):
  name='_keycode_at_'+target+'_location';body=text.split(name+':',1)[1].split(';------------------------------------------------------------',1)[0]
  assert re.search(r'mov\s+r7,dpl',body) and re.search(r'mov\s+dpl,\s*r7',body)
  for j in (2,3):
   p=name+'_PARM_'+str(j);assert re.search(re.escape(p)+r':\s*\.ds\s+1\b',text);assert fw.symbol_sizes[p]==1;abi[p]={'address':fw.address(p),'width':1,'space':fw.symbol_space(p)}
  assert re.search(r'ljmp\s+_dynamic_keymap_get_'+('keycode' if target=='keymap' else 'encoder'),body)
 report=json.loads((a.build/'build-report.json').read_text());auth=[]
 for rel in ['quantum/dynamic_keymap.c','keyboards/ajazz/ak820/ak820_keymap_words.c','keyboards/ajazz/ak820/ak820_nvm.c','keyboards/ajazz/ak820/config.h']:
  entries=[x for x in report['sources'] if x['path']==rel and x['origin']=='source'];assert len(entries)==1 and entries[0]['sha256']==sha(root/rel),(rel,entries);auth.append(entries[0])
 paths=[fw.image,a.build/'ajazz_ak820_vial.map',a.build/'build-report.json',asm,a.build/'dce/ak820_keymap_words.asm',a.build/'dce/ak820_nvm.asm',Path(__file__),root/'tests/ak820_iap/run.py',root/'tests/ak820_emitted/run.py',fw.simulator]+[root/x['path'] for x in auth];before={str(p):sha(p) for p in paths}
 res={'pass':False,'immutable_inputs':before,'authenticated_sources':auth,'abi':abi,'cases':[],'limits':['Generic C52 CPU model; no peripherals or hardware.','CRT to main entry only; IE/IE_EX disabled. No main or NVM init, ROM seed, IRQ, new read-fault, cross-page or durable-storage proof.','Single actual 64-byte cache page primed per call; source bytes and CODE preserved.']}
 class SafeConsole(iap.Console):
  def command(self,commands):
   for row in ([commands] if isinstance(commands,str) else commands):
    lines=Path(json.loads(row[5:])).read_text().splitlines() if row.startswith('exec ') else [row]
    for line in lines:
     if re.match(r'(?:set memory|fill) rom ',line):
      assert line.startswith('set memory rom ');w=line.split();addr=int(w[3],0);v=w[4:];assert 0x2600<=addr and addr+len(v)<=0x2700 and not any(addr+j in fw.code for j in range(len(v)))
   if isinstance(commands,list):
    f=out/'current.sim';f.write_text('\n'.join(commands)+'\n');commands='exec '+json.dumps(str(f))
   return super().command(commands)
 c=SafeConsole(fw.simulator,fw.image);groups=[]
 for p in sorted(fw.code):
  if not groups or p!=groups[-1][-1]+1:groups.append([])
  groups[-1].append(p)
 def snapshot(label):
  h=hashlib.sha256();count=0
  for g in groups:
   for j in range(0,len(g),512):
    sl=g[j:j+512];tag=label+str(sl[0]);got=fw.extract(c.command([f'echo @@{tag}',f'dump /h rom {sl[0]:#x} {sl[-1]:#x} 16']),tag,sl[0],len(sl));assert got==[fw.code[p] for p in sl];h.update(bytes(got));count+=len(sl)
  return {'bytes':count,'sha256_address_order':h.hexdigest()}
 try:
  res['code_before']=snapshot('before');c.command([f'run {fw.address("__sdcc_gsinit_startup"):#x} {fw.address("_main"):#x}',mem('sfr',0xa8,[0]),mem('sfr',0xe8,[0]),mem('iram',0xfe,[0x79,0x96])]);sp=c.read('sfr',0x81,1);assert sp==[fw.initial_sp+2];res['crt_sp']=sp[0]
  forbidden=['_ak820_flash_erase','_ak820_flash_program','_ak820_flash_program_page','_write_page','_eeprom_update_byte','_ak820_eeprom_write_block_xdata'];res['stopguards']={n:fw.address(n) for n in forbidden};c.command([f'break {v:#x}' for v in res['stopguards'].values()]+['break sfr w 0x86',f'break {fw.address("_eeprom_read_byte"):#x}'])
  cases=[('keymap',l,r,col) for l,r,col in itertools.product(range(6),range(16),range(8))]
  cases += [('keymap',*v) for axis,valid in enumerate((6,16,8)) for bad in (valid,valid+1,127,254,255) for v in [tuple(bad if k==axis else 0 for k in range(3))]]
  cases += [('encodermap',l,0,b) for l in range(6) for b in range(256)]
  cases += [('encodermap',l,idx,b) for l,idx,b in itertools.product((0,5,6,7,127,255),(0,1,2,127,255),(0,1,2,255)) if l>=6 or idx!=0]
  res['total_case_count']=len(cases);res['shard_index']=a.shard_index;res['shard_count']=a.shard_count;cases=cases[a.shard_index::a.shard_count]
  flags=['_page_valid','_page_dirty','_storage_failed','_cached_page','_batch_depth']
  for target,l,x,y in cases:
   valid=l<6 and (x<16 and y<8 if target=='keymap' else x==0);addr=(64+2*((l*16+x)*8+y) if target=='keymap' else 1600+4*l+(0 if y else 2)) if valid else 64
   data=[(j*29+17+(addr//64)*7)&255 for j in range(64)];flagvals=[1,0,0,addr//64,1];name='_keycode_at_'+target+'_location';cmds=[]
   for n,v in zip(flags,flagvals):cmds+=fw.write(n,[v])
   cmds+=fw.write('_page_data',data)+fw.write(name+'_PARM_2',[x])+fw.write(name+'_PARM_3',[y])+fw.call(name,l);log=c.command(cmds);reads=[]
   while True:
    pcs=re.findall(r'F 0x([0-9a-fA-F]+)',log);assert pcs,log[-3000:];pc=int(pcs[-1],16)
    if pc==0x2700:break
    assert pc==fw.address('_eeprom_read_byte'),('unexpected stop',pc,log[-3000:]);assert valid and len(reads)<2,('unexpected EEPROM read',target,l,x,y,reads)
    dp=c.read('sfr',0x82,2);reads.append(dp[0]+256*dp[1]);log=c.command('run')
   assert reads==([addr,addr+1] if valid else []),(target,l,x,y,reads,addr)
   dp=c.read('sfr',0x82,2);actual=dp[0]+256*dp[1];want=(data[addr%64]*256+data[addr%64+1]) if valid else 0;assert actual==want,(target,l,x,y,actual,want)
   observations=[('cache','xram',fw.address('_page_data'),64),('canary','iram',0xfe,2)]+[(n,fw.symbol_space(n),fw.address(n),1) for n in flags]
   obs=[]
   for tag,space,address,n in observations:obs+=fw.dump(tag,space,address,n)
   obs+=['echo @@SP','dump sfr 0x81 0x81'];observed=c.command(obs)
   values={tag:fw.extract(observed,tag,address,n) for tag,space,address,n in observations}
   assert values['cache']==data;assert values['canary']==[0x79,0x96]
   assert int(re.search(r'0x81 SP:\s+0b[01]+\s+0x([0-9a-f]+)',observed.rsplit('@@SP',1)[1])[1],16)==sp[0]
   for n,v in zip(flags,flagvals):assert values[n]==[v]
   res['cases'].append({'target':target,'args':[l,x,y],'valid':valid,'return':actual,'reads':reads,'pass':True})
   if len(res['cases'])%128==0:(out/'progress.json').write_text(json.dumps({'completed':len(res['cases'])}))
  res['pass']=True;res['state']=c.command('state')
 except Exception:res['error']=traceback.format_exc()
 finally:
  try:res['code_after']=snapshot('after');assert res['code_after']==res['code_before']
  except Exception:res['pass']=False;res['code_error']=traceback.format_exc()
  c.close();(out/'cpu.log').write_text(c.log);res['immutable_inputs_unchanged']={str(p):sha(p) for p in paths}==before;res['pass'] &= res['immutable_inputs_unchanged'];res['case_count']=len(res['cases']);(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
 assert res['pass'],res.get('error',res.get('code_error','input changed'))
 print(json.dumps({'pass':True,'cases':res['case_count']}))
if __name__=='__main__':main()
