#!/usr/bin/env python3
import argparse,hashlib,importlib.util,itertools,json,re,traceback
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def require_boot_alias(text):
 aliases=re.findall(r'\bQK_BOOT\s*=\s*([^,\n]+)',text)
 assert aliases==['QK_BOOTLOADER'],('Missing, different or ambiguous QK_BOOT alias',aliases)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 root=a.repo/'qmk-8051-ak820';out=a.output;out.mkdir(parents=True,exist_ok=True)
 iap=mod('firewall_iap',root/'tests/ak820_iap/run.py');e=iap.emitted;mem=e.memory
 fw=e.Firmware(a.build,a.repo/'toolchains/sdcc-4.6.0/bin/s51',out)
 asm=(a.build/'dce/quantum/dynamic_keymap.asm').read_text()
 for name,width in [('_dynamic_keymap_set_buffer_PARM_2',2),('_dynamic_keymap_set_buffer_PARM_3',3)]:
  assert re.search(re.escape(name)+r':\s*\.ds\s+'+str(width)+r'\b',asm);assert fw.symbol_sizes[name]==width
 config=(root/'keyboards/ajazz/ak820/config.h').read_text()
 def define(n):return int(re.search(r'^#define '+n+r'\s+(0x[\da-fA-F]+|\d+)',config,re.M)[1],0)
 base=define('DYNAMIC_KEYMAP_EEPROM_ADDR');extent=define('MATRIX_ROWS')*define('MATRIX_COLS')*define('DYNAMIC_KEYMAP_LAYER_COUNT')*2
 keycode=(root/'quantum/keycodes.h').read_text();assert re.search(r'QK_BOOTLOADER\s*=\s*0x7C00',keycode,re.I)
 require_boot_alias(keycode)
 alias_line=re.search(r'\bQK_BOOT\s*=\s*QK_BOOTLOADER',keycode)[0]
 alias_negative_checks=[]
 for kind,changed in [('missing',keycode.replace(alias_line,'')),('different',keycode.replace(alias_line,'QK_BOOT = 0xFFFF')),('ambiguous',keycode+'\nQK_BOOT = QK_BOOTLOADER,\n')]:
  try:require_boot_alias(changed)
  except AssertionError:alias_negative_checks.append({'kind':kind,'rejected':True})
  else:raise AssertionError(('Alias drift accepted',kind))
 boot=[0x7c,0];assert base==64 and extent==1536
 assert not any(p in fw.code for p in range(0x2600,0x2701))
 manifest=a.build/'build-report.json';report=json.loads(manifest.read_text())
 relevant=['quantum/dynamic_keymap.c','keyboards/ajazz/ak820/ak820_nvm.c','keyboards/ajazz/ak820/config.h','quantum/keycodes.h']
 authenticated_sources=[]
 for rel in relevant:
  entries=[x for x in report['sources'] if x['path']==rel and x['origin']=='source']
  assert len(entries)==1 and entries[0]['sha256']==sha(root/rel),('Build source identity mismatch',rel)
  authenticated_sources.append({'path':rel,'sha256':entries[0]['sha256'],'unique_build_source_match':True})
 paths=[fw.image,a.build/'ajazz_ak820_vial.map',manifest,Path(__file__),root/'tests/ak820_iap/run.py',root/'tests/ak820_emitted/run.py',root/'keyboards/ajazz/ak820/config.h',root/'quantum/keycodes.h',a.repo/'tests/ak820_keymap_firewall/oracle.inc',a.repo/'tests/ak820_keymap_firewall/harness.c',a.build/'dce/quantum/dynamic_keymap.asm']+[root/x for x in relevant]
 before={str(p):sha(p) for p in paths};res={'pass':False,'authenticated_sources':authenticated_sources,'keycode_alias':{'QK_BOOT':'QK_BOOTLOADER','unique':True,'in_memory_negative_checks':alias_negative_checks},'immutable_inputs':before,'s51_sha256':sha(fw.simulator),'model':'uCsim generic C52; no devices','abi':{'offset':'DPTR','size_width':2,'data_generic_pointer_width':3,'parameter_addresses':{n:fw.address(n) for n in ('_dynamic_keymap_set_buffer_PARM_2','_dynamic_keymap_set_buffer_PARM_3')}},'cases':[],'limits':['Oversized diagnostic image, not flashable/device qualification.','CRT to main entry only; no main, board init, NVM init or ROM seeding.','Single primed cache page, batch_depth=1; no cross-page transitions, flash effects or durable storage.','IE and IE_EX disabled; no interrupt timing/peripheral/hardware proof.']}
 groups=[]
 for p in sorted(fw.code):
  if not groups or p!=groups[-1][-1]+1:groups.append([])
  groups[-1].append(p)
 class SafeConsole(iap.Console):
  def command(self,commands):
   rows=[commands] if isinstance(commands,str) else commands
   for row in rows:
    if row.startswith('exec '):
     content=Path(json.loads(row[5:])).read_text().splitlines()
    else:content=[row]
    for line in content:
     if re.match(r'(?:set memory|fill) rom ',line):
      assert line.startswith('set memory rom '),('Forbidden ROM fill',line)
      words=line.split();address=int(words[3],0);values=[int(x,0) for x in words[4:]]
      assert address>=0x2600 and address+len(values)<=0x2700 and not any(address+j in fw.code for j in range(len(values))),('Forbidden ROM mutation',line)
   return super().command(commands)
 c=SafeConsole(fw.simulator,fw.image)
 def snapshot(label):
  digest=hashlib.sha256();count=0
  for g in groups:
   for j in range(0,len(g),512):
    sl=g[j:j+512];labelpart=label+str(sl[0]);sf=out/'snapshot.sim';sf.write_text('\n'.join([f'echo @@{labelpart}',f'dump /h rom {sl[0]:#x} {sl[-1]:#x} 16'])+'\n');got=fw.extract(c.command('exec '+json.dumps(str(sf))),labelpart,sl[0],len(sl));assert got==[fw.code[p] for p in sl],('occupied CODE changed',label,sl[0]);digest.update(bytes(got));count+=len(sl)
  return {'bytes':count,'sha256_address_order':digest.hexdigest()}
 try:
  res['code_before']=snapshot('before')
  c.command([f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}",mem('sfr',0xa8,[0]),mem('sfr',0xe8,[0]),mem('iram',0xfe,[0x79,0x96])])
  sp=c.read('sfr',0x81,1);assert sp==[fw.initial_sp+2];res['crt_entry_sp']=sp[0]
  forbidden=['_ak820_flash_erase','_ak820_flash_program','_ak820_flash_program_page','_write_page'];res['flash_stopguards']={n:fw.address(n) for n in forbidden}
  c.command([f'break {fw.address(n):#x}' for n in forbidden])
  flags=['_page_valid','_page_dirty','_storage_failed','_cached_page','_batch_depth']
  valid=[(off,n,'boot') for off in (8,9) for n in range(1,29)]+[(8,28,'equal'),(9,27,'equal'),(8,1,'equal'),(9,2,'equal'),(0,2,'boot'),(extent-2,2,'boot'),(extent-1,1,'boot'),(extent-28,28,'boot')]
  invalid=[(0,0),(0xffff,0),(0,29),(0,255),(0,256),(0,0xffff),(extent,1),(extent-1,2),(0xffff,1),(0xfff0,28),(0x8000,1)]
  for unlocked,failed,dirty in itertools.product((0,1),repeat=3):
   for off,n,kind in valid+[(o,n,'reject') for o,n in invalid]:
    data=[(j*13+7)&255 for j in range(64)];packet=[(j*17+3)&255 for j in range(32)];start=off%64
    if kind=='boot':
     for j in range(n):packet[j]=boot[(off+j)%2]
     if off%2:data[start-1]=boot[0]
     if (off+n)%2:data[start+n]=boot[1]
    elif kind=='equal':packet[:n]=data[start:start+n]
    expected_packet=packet.copy();expected_cache=data.copy()
    if kind!='reject':
     if not unlocked:
      # Semantic oracle combines each input byte with its aligned key partner.
      for j in range(n):
       absolute=off+j;partner=j+1 if absolute%2==0 else j-1
       other=packet[partner] if 0<=partner<n else data[(off+partner)%64]
       if (packet[j],other)==((boot[0],boot[1]) if absolute%2==0 else (boot[1],boot[0])):expected_packet[j]=255
     if not failed:expected_cache[start:start+n]=expected_packet[:n]
    expected_dirty=int(bool(dirty or (kind!='reject' and not failed and expected_cache!=data)))
    cmds=[]
    for name,value in zip(flags,[1,dirty,failed,(base+off)//64 if kind!='reject' else 1,1]):cmds+=fw.write(name,[value])
    cmds+=fw.write('_page_data',data)+fw.write('_vial_unlocked',[unlocked])+[mem('xram',0x7fff,[0xb9]+packet+[0x6d])]
    cmds+=fw.write('_dynamic_keymap_set_buffer_PARM_2',list(n.to_bytes(2,'little')))+fw.write('_dynamic_keymap_set_buffer_PARM_3',[0,0x80,0])
    if kind=='reject':cmds += [f'break {fw.address(x):#x}' for x in ('_eeprom_read_byte','_ak820_eeprom_write_block_xdata')]
    cmds+=fw.call('_dynamic_keymap_set_buffer',off)
    observations=[('packet','xram',0x7fff,34),('cache','xram',fw.address('_page_data'),64),('guard','iram',0xfe,2)]+[(name,fw.symbol_space(name),fw.address(name),1) for name in flags]
    for label,space,address,count in observations:cmds+=fw.dump(label,space,address,count)
    cmds+=['echo @@SP','dump sfr 0x81 0x81']
    f=out/'current-case.sim';f.write_text('\n'.join(cmds)+'\n');log=c.command('exec '+json.dumps(str(f)));assert re.search(r'F 0x002700',log),log[-5000:]
    actual={label:fw.extract(log,label,address,count) for label,space,address,count in observations}
    assert actual['packet']==[0xb9]+expected_packet+[0x6d],('packet',unlocked,failed,dirty,off,n,actual['packet'],expected_packet)
    assert actual['cache']==expected_cache,('cache',unlocked,failed,dirty,off,n)
    assert actual['guard']==[0x79,0x96]
    for name,want in zip(flags,[1,expected_dirty,failed,(base+off)//64 if kind!='reject' else 1,1]):assert actual[name]==[want],(name,actual[name],want)
    assert int(re.search(r'0x81 SP:\s+0b[01]+\s+0x([0-9a-f]+)',log.rsplit('@@SP',1)[1])[1],16)==sp[0]
    if kind=='reject':c.command([f'clear {fw.address(x):#x}' for x in ('_eeprom_read_byte','_ak820_eeprom_write_block_xdata')])
    res['cases'].append({'unlocked':unlocked,'failed':failed,'dirty':dirty,'offset':off,'size':n,'kind':kind,'pass':True})
    if len(res['cases'])%64==0:(out/'progress.json').write_text(json.dumps({'completed':len(res['cases'])}))
  state=c.command('state');res['observed_peak_sp']=int(re.findall(r'Most value of stack pointer=\s+0x([0-9a-f]+)',state)[-1],16)
  res['pass']=True
 except Exception:
  res['error']=traceback.format_exc()
 finally:
  try:res['code_after']=snapshot('after');assert res['code_after']==res['code_before']
  except Exception:res['pass']=False;res['code_check_error']=traceback.format_exc()
  c.close();(out/'cpu.log').write_text(c.log)
  res['immutable_inputs_unchanged']={str(p):sha(p) for p in paths}==before
  res['pass']=res['pass'] and res['immutable_inputs_unchanged'];res['case_count']=len(res['cases']);(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
 assert res['pass'],res.get('error',res.get('code_check_error','input changed'))
 print(json.dumps({'pass':True,'cases':len(res['cases']),'occupied_code':res['code_after']['bytes']}))
if __name__=='__main__':main()
