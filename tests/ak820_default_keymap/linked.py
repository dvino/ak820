#!/usr/bin/env python3
import argparse,hashlib,importlib.util,itertools,json,re,traceback,sys
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--control',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--shard-index',type=int,default=0);ap.add_argument('--shard-count',type=int,default=1);a=ap.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);root=a.repo/'qmk-8051-ak820';iap=mod('iap',root/'tests/ak820_iap/run.py');e=iap.emitted;sys.path.insert(0,str(root/'util'));gen=mod('gen',root/'util/ak820_default_keymap.py');sim=a.repo/'toolchains/sdcc-4.6.0/bin/s51';fws=[e.Firmware(b,sim,out) for b in (a.build,a.control)];bootstrap=a.build/'default-keymap/bootstrap.asm';raw=gen.literal_block(bootstrap.read_text(),'_keymaps');assert len(raw)==512;arrays=gen.encode(raw,gen.literal_block(bootstrap.read_text(),'_ak820_default_metadata'));res={'pass':False,'cases':[],'raw_layer_count':{'value':2,'cpu_executable':False,'reason':'DCE eliminated keymap_layer_count_raw; bootstrap metadata and linked bounds prove two.'},'images':[]}
 paths=[Path(__file__),sim,bootstrap,root/'util/ak820_default_keymap.py',root/'quantum/keymap_introspection.c',root/'quantum/dynamic_keymap.c',root/'tests/ak820_iap/run.py',root/'tests/ak820_emitted/run.py']
 for fw in fws:paths +=[fw.image,fw.build/'ajazz_ak820_vial.map',fw.build/'build-report.json',fw.build/'dce/quantum/keymap_introspection.asm',fw.build/'dce/quantum/keymap_introspection.rst']
 paths +=[a.build/'default-keymap/generation.json',a.build/'default-keymap/ak820_default_keymap.inc'];before={str(p):sha(p) for p in paths};res['immutable_inputs']=before
 def code(fw,n,size):return [fw.code[fw.address(n)+j] for j in range(size)]
 for n,size in [('_encoder_map',8),('_ak820_led_points',164)]:assert code(fws[0],n,size)==code(fws[1],n,size);res[n]={'bytes':size,'sha256':hashlib.sha256(bytes(code(fws[0],n,size))).hexdigest(),'addresses':[f.address(n) for f in fws]}
 assert code(fws[1],'_keymaps',512)==raw
 for n,vals in zip(('classes','payload','offsets'),arrays):assert code(fws[0],'_ak820_default_'+n,len(vals))==vals
 res['tables']={n:{'address':fws[0].address('_ak820_default_'+n),'bytes':len(v),'sha256':hashlib.sha256(bytes(v)).hexdigest()} for n,v in zip(('classes','payload','offsets'),arrays)}
 cases=list(itertools.product(range(2),range(16),range(8)))+[(l,0,0) for l in (2,3,4,5,6,127,254,255)]+[(0,r,0) for r in (16,17,127,254,255)]+[(0,0,c) for c in (8,9,127,254,255)]+[(255,255,255)];res['total_cases_per_image']=len(cases);cases=cases[a.shard_index::a.shard_count]
 for fw in fws:
  assert not any(p in fw.code for p in range(0x2600,0x2700));asm=(fw.build/'dce/quantum/keymap_introspection.asm').read_text();name='_keycode_at_keymap_location_raw';assert re.search(re.escape(name)+r':\s*mov\s+(?:a|r\d),dpl',asm);assert 'keymap_layer_count_raw' not in fw.symbols and '_keymap_layer_count_raw' not in fw.symbols
  for j in (2,3):assert re.search(re.escape(name+'_PARM_'+str(j))+r':\s*\.ds\s+1\b',asm);assert fw.symbol_sizes[name+'_PARM_'+str(j)]==1
  class Safe(iap.Console):
   def command(self,commands):
    if isinstance(commands,str):commands=[commands]
    for line in commands:
     if re.match(r'(?:set memory|fill) rom ',line):
      w=line.split();addr=int(w[3],0);assert line.startswith('set memory rom ') and 0x2600<=addr and addr+len(w[4:])<=0x2700 and not any(addr+j in fw.code for j in range(len(w[4:])))
    f=out/'current.sim';f.write_text('\n'.join(commands)+'\n');return super().command('exec '+json.dumps(str(f)))
  c=Safe(sim,fw.image);ir={'image_sha256':sha(fw.image),'abi':{name+'_PARM_'+str(j):{'address':fw.address(name+'_PARM_'+str(j)),'space':fw.symbol_space(name+'_PARM_'+str(j)),'width':1} for j in (2,3)},'cases':[]};res['images'].append(ir)
  groups=[]
  for p in sorted(fw.code):
   if not groups or p!=groups[-1][-1]+1:groups.append([])
   groups[-1].append(p)
  def snapshot(label):
   h=hashlib.sha256();count=0
   for g in groups:
    for j in range(0,len(g),512):
     sl=g[j:j+512];tag=label+str(sl[0]);got=fw.extract(c.command([f'echo @@{tag}',f'dump /h rom {sl[0]:#x} {sl[-1]:#x} 16']),tag,sl[0],len(sl));assert got==[fw.code[p] for p in sl];h.update(bytes(got));count+=len(got)
   return {'bytes':count,'sha256_address_order':h.hexdigest()}
  try:
   ir['code_before']=snapshot('before');c.command([f'run {fw.address("__sdcc_gsinit_startup"):#x} {fw.address("_main"):#x}',e.memory('sfr',0xa8,[0]),e.memory('sfr',0xe8,[0]),e.memory('iram',0xfe,[0x79,0x96])]);sp=c.read('sfr',0x81,1)[0];assert sp==fw.initial_sp+2
   forbidden=['_ak820_flash_erase','_ak820_flash_program','_ak820_flash_program_page','_eeprom_read_byte','_eeprom_update_byte','_ak820_eeprom_write_block_xdata'];ir['stopguards']={n:fw.address(n) for n in forbidden};c.command([f'break {v:#x}' for v in ir['stopguards'].values()]+['break sfr w 0x86','break sfr r 0x86'])
   for l,r,col in cases:
    valid=l<2 and r<16 and col<8;want=raw[2*((l*16+r)*8+col)]|raw[2*((l*16+r)*8+col)+1]<<8 if valid else 1
    prestate=c.command('state');preinst=int(re.search(r'Inst=\s*(\d+)',prestate)[1]);log=c.command(fw.write(name+'_PARM_2',[r])+fw.write(name+'_PARM_3',[col])+fw.call(name,l));pcs=re.findall(r'F 0x([0-9a-fA-F]+)',log);assert pcs and int(pcs[-1],16)==0x2700,log[-2000:];dp=c.read('sfr',0x82,2);actual=dp[0]|dp[1]<<8;assert actual==want,(l,r,col,actual,want);actual_sp=c.read('sfr',0x81,1)[0];canary=c.read('iram',0xfe,2);assert actual_sp==sp and canary==[0x79,0x96];ticks=re.findall(r'Simulated (\d+) ticks',log);state=c.command('state');inst=re.findall(r'Inst=\s*(\d+)',state);ir['cases'].append({'args':[l,r,col],'valid':valid,'DPL':dp[0],'DPH':dp[1],'return':actual,'SP':sp,'canary':canary,'ticks':int(ticks[-1]) if ticks else None,'instructions':int(inst[-1])-preinst,'state':state,'pass':True})
   ir['pass']=True
  except Exception:ir['error']=traceback.format_exc();raise
  finally:
   try:ir['code_after']=snapshot('after');assert ir['code_after']==ir['code_before']
   finally:c.close();(out/('cpu-'+str(len(res['images']))+'.log')).write_text(c.log);(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
 res['immutable_inputs_unchanged']={str(p):sha(p) for p in paths}==before;assert res['immutable_inputs_unchanged'];res['pass']=True;(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'pass':True,'cases_per_image':len(cases)}))
if __name__=='__main__':main()
