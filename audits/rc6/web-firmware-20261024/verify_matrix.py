#!/usr/bin/env python3
"""Verify retained four-image offline evidence against frozen Git blobs."""
import json,hashlib,tarfile,sys,itertools,re,subprocess
from pathlib import Path
if not __debug__: raise SystemExit('Run without Python optimization; assertions are required')
import argparse
parser=argparse.ArgumentParser(description='Validate retained exact-image runtime matrix and raw build archives')
parser.add_argument('--root',type=Path,default=next((p for p in Path(__file__).resolve().parents if (p/'tools/configure_firmware.py').is_file()),Path.cwd()))
parser.add_argument('--final-dir',type=Path,help='Evidence directory (defaults to audits/rc6/web-firmware-20261024/final)')

args=parser.parse_args()
ROOT=args.root.resolve(); FINAL=(args.final_dir or ROOT/'audits/rc6/web-firmware-20261024/final').resolve(); INDEX=json.loads((FINAL/'matrix.json').read_text()); COMMIT=INDEX['source_commit']
assert re.fullmatch(r'[0-9a-f]{40}', COMMIT)
EXPECTED={'full','full-mac-pc','full-os-indicators','full-mac-pc-os-indicators'}
sys.path.insert(0,str(ROOT/'tools'));import configure_firmware as cf
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
blob_hashes={}
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',COMMIT],cwd=ROOT).decode().splitlines())
def frozen_hash(name):
 if name not in blob_hashes:blob_hashes[name]=sha(subprocess.check_output(['git','show',COMMIT+':'+name],cwd=ROOT))
 return blob_hashes[name]
def offline_flags(value):
 if isinstance(value,dict):
  for key,item in value.items():
   if key in ('hardware_validated','release_approved','settings_writes_authorized','flashing_authorized'):assert item is False,(key,'unexpected permission or validation claim')
   if key=='physical_device_commands':assert type(item) is int and item==0
   offline_flags(item)
 elif isinstance(value,list):
  for item in value:offline_flags(item)
def check(folder):
 rec=read(folder/'record.json'); c=read(folder/'configuration-report.json'); q=read(folder/'qualification.json'); p=read(folder/'profile-results.json'); r=rec['runtime']; ident=rec['identity']
 for value in (rec,c,q,p):offline_flags(value)
 assert cf.validate_tests(folder/'qualification.json',ident)==c['qualification']
 assert p['format']=='ak820-profile-tests-1' and p['profile']==rec['profile']
 assert rec['source']==c['source']=={'commit':COMMIT,'dirty':False}
 assert rec['resources']==c['resources']
 assert rec['base_suites']==len(q['tests'])==28
 assert rec['optional_features']==cf.profiles.configuration(rec['profile'])['optional_features']
 assert c['configuration']==cf.profiles.configuration(rec['profile'])
 for obj in [rec,c,r]:
  assert obj['hardware_validated'] is False and obj['release_approved'] is False and obj['physical_device_commands']==0
 assert rec['offline_tests_passed'] is c['offline_tests_passed'] is True
 assert r==read(folder/'runtime-safety/summary.json')==c['runtime_analysis'] and r['identity']==p['identity']==c['identity']==ident
 assert r['passed'] and r['whole_program_stack_qualified'] and r['unresolved_roots']==[]
 assert r['root_bounds']=={'_main':r['foreground_bound'],'_USB_DeviceInterrupt':6,'_ak820_led_irq':2,'_ak820_timer_irq':2}
 assert r['irq_bound']==61 and r['main_entry_frame_bound']==2 and r['pre_main_bound']==2
 assert r['stack_bound']==max(r['pre_main_bound'],r['foreground_bound']+2+61)
 assert r['stack_margin']==r['stack_capacity']-r['stack_bound']>=0
 assert rec['resources']['internal_ram']['stack_margin']==r['stack_margin']
 assert sha((folder/'raw-build.tar.xz').read_bytes())==rec['raw_build']['sha256']
 assert (folder/'raw-build.tar.xz').stat().st_size==rec['raw_build']['bytes']
 with tarfile.open(folder/'raw-build.tar.xz') as tf:
  members=tf.getmembers(); assert all(m.isfile() or m.isdir() for m in members), 'Nonregular archive member'; assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts for m in members), 'Unsafe archive path'; assert len(members)==len({x.name for x in members}), 'Duplicate archive member names'; ms={x.name:x for x in members}; prefixes={x.split('/ajazz_ak820_vial.ihx')[0] for x in ms if x.endswith('/ajazz_ak820_vial.ihx')};assert len(prefixes)==1
  prefix=prefixes.pop()
  payload={m.name:tf.extractfile(m).read() for m in members if m.isfile()}
  def raw(name):return payload[prefix+'/'+name]
  def hs(name,h):assert sha(raw(name))==h,(folder.name,name)
  for f in folder.rglob('*'):
   if f.is_file() and f.name not in ['record.json','raw-build.tar.xz','qualification-command.log']:
    name=f.relative_to(folder).as_posix(); name={'profile-results.json':'profile-tests/results.json'}.get(name,name)
    if name.endswith('-linked.json'):name='profile-tests/'+name.removesuffix('-linked.json')+'/results.json'
    assert raw(name)==f.read_bytes(),(folder.name,name,'loose/raw differs')
  for suffix in ['ihx','map','mem']:hs('ajazz_ak820_vial.'+suffix,ident[suffix+'_sha256'])
  br=json.loads(raw('build-report.json'))
  assert sha(cf.canonical(br['sources']))==ident['source_manifest_sha256']
  assert sha(cf.canonical(c['configuration']))==ident['configuration_sha256']
  for item in br['sources']:
   if item['origin']=='source':
    name=item['path']
    if name.startswith(prefix+'/'):assert sha(payload[name])==item['sha256'],name
    else:
     fullname='qmk-8051-ak820/'+name
     if fullname in tracked:assert frozen_hash(fullname)==item['sha256'],name
     else:
      assert name.startswith('lib/lufa/'),('Unexpected untracked input',name)
      lock=json.loads(subprocess.check_output(['git','show',COMMIT+':qmk-8051-ak820/dependencies/lufa.json'],cwd=ROOT))
      assert lock['required_files'][name.removeprefix('lib/lufa/')]==item['sha256'],name
  for item in br['artifacts']:
   assert sha(payload[item['path']])==item['sha256'] and len(payload[item['path']])==item['size'],item['path']
  hs('build-report.json',ident['build_report_sha256']);hs('qualification.json',c['qualification']['sha256']);hs('profile-tests/results.json',c['profile_tests']['sha256'])
  for report in r['reports'].values():hs(report['path'],report['sha256'])
  for name,h in r['logs'].items():hs('runtime-safety/'+name+'.log',h)
  fg=json.loads(raw('runtime-stack.json'));irq=json.loads(raw('runtime-safety/irq/results.json'));start=json.loads(raw('runtime-safety/startup.json'))
  for value in (br,fg,irq,start):offline_flags(value)
  recombined=cf.combine_runtime_safety(fg,start,irq,ident,c['resources']['internal_ram'],r['source_files'])
  assert all(r[key]==value for key,value in recombined.items()), 'Runtime component contract differs'
  assert r['source_files']==cf.runtime_source_snapshot(), 'Incomplete runtime source snapshot'
  test_names={name for name in tracked if name.startswith(('tools/','qmk-8051-ak820/tests/','qmk-8051-ak820/keyboards/ajazz/ak820/tests/')) and Path(name).suffix in ('.py','.c','.h','.inc')}
  assert set(p['source_files'])==test_names, 'Incomplete frozen test source snapshot'
  assert fg['whole_program_qualified'] is False and set(fg['roots'])==set(r['root_bounds'])
  for name,bound in r['root_bounds'].items():assert fg['roots'][name]['bound']==bound and fg['roots'][name]['unresolved']==[]
  for name,h in fg['identity']['listing_sha256'].items():hs(name,h)
  assert irq['pass'] and irq['linked_image_sha256']==ident['ihx_sha256'] and irq['linked_map_sha256']==ident['map_sha256']
  orders={x for n in range(1,4) for x in itertools.permutations(('timer','usb','led'),n)}
  assert {tuple(x['irq_order']) for x in irq['ordered_nests']}==orders and len(irq['ordered_nests'])==15
  assert {tuple(x['irq_order']) for x in irq['cpu_cases']}==orders and len(irq['cpu_cases'])==15
  assert all(x['canary_and_registers_preserved'] for x in irq['cpu_cases']) and irq['selector_cases']['input_values_checked']==256
  assert irq['all_distinct_source_irq_bound']==61 and irq['wrapper_bytes_on_stack']==17
  assert start['interrupt_enables_unchanged_until_main'] and start['pre_main_control_stack_bound']==2 and start['main_entry_frame_bound']==2
  assert q['passed'] and q['build_unchanged'] and len(q['tests'])==28 and q['unit_tests']==rec['base_unit_tests'] and q['unit_tests']=={'run':273,'skipped':0}
  assert q['hardware_validated'] is False and q['physical_device_commands']==0
  assert q['test_environment']=={},(folder.name,'unexpected test environment override')
  command_log=(folder/'qualification-command.log').read_text()
  startup_at=command_log.find('RUN RUNTIME startup');irq_at=command_log.find('RUN RUNTIME irq')
  base_at=command_log.find('RUN '+' '.join(q['tests'][0]['command']))
  profile_at=command_log.find('RUN PROFILE gates')
  assert 0<=startup_at<irq_at<base_at<profile_at,(folder.name,'runtime gate must precede regression suites')
  assert sum(x['unit_tests']['run'] for x in q['tests'])==q['unit_tests']['run']
  cf.validate_qualification_contract(q)
  unit_specs=[('tools/installer','test_*.py'),('tools','test_build_release_bundle.py'),('tools','test_build_windows_installer.py'),('tools','test_keyboard_runner.py'),('tools','test_ak820_device_tests.py'),('tools','test_ak820_device_protocol.py'),('qmk-8051-ak820/tests/ak820_package','test_*.py'),('qmk-8051-ak820/tests/ak820_inventory','test_*.py')]
  expected_base=[['-B','-m','unittest','discover','-s',a,'-p',b] for a,b in unit_specs]+[['tools/check_docs.py']]
  expected_base += [[f'tests/{name}/run.py'] for name in ('ak820_usb','ak820_keymap','ak820_caps_word','ak820_macro_guard','ak820_diagnostic','ak820_optimization','ak820_rgb','ak820_via_decode','ak820_combo','ak820_bounded')]
  expected_base += [['tests/ak820_tapping/run.py','--negative-controls','--output','<output>']]
  expected_base += [[f'tests/{name}/run.py','--build-dir','<build-dir>','--s51','<s51>','--output-dir','<output-dir>']+(['--iap-fault-profile','guarded-erase'] if name=='ak820_iap' else []) for name in ('ak820_features','ak820_unlock','ak820_tri_layer','ak820_iap')]
  expected_base += [[f'tests/{name}/emitted.py','--build-dir','<build-dir>','--s51','<s51>','--output-dir','<output-dir>'] for name in ('ak820_rgb','ak820_bounded','ak820_tapping','ak820_combo')]
  def normalize(cmd):
   cmd=cmd[1:].copy()
   for flag in ('--build-dir','--s51','--output-dir','--output'):
    if flag in cmd:cmd[cmd.index(flag)+1]='<'+flag[2:]+'>'
   return cmd
  assert [normalize(x['command']) for x in q['tests']]==expected_base,(folder.name,'base suite plan')
  previous=base_at
  for row in q['tests']:
   position=command_log.find('RUN '+' '.join(row['command']),previous)
   assert position>=previous and position<profile_at, 'Missing/out-of-order base command'
   previous=position+1
   assert row['exit_code']==0 and row['unit_tests']['skipped']==0
   bn='/'.join(row['log'].split('/')[-2:]);hs(bn,row['log_sha256'])
   assert cf.unittest_counts(raw(bn).decode())==row['unit_tests']
   assert row['build_before']==row['build_after']=={s:ident[s+'_sha256'] for s in ['ihx','map']}
  build=Path(p['tests'][0]['command'][0]) # determine original paths from linked row
  linked=next(x for x in p['tests'] if x['id']=='core-compact-linked');args=linked['command'];build=Path(args[args.index('--build-dir')+1]);toolchain=Path(args[args.index('--s51')+1]).parent.parent
  clone=Path(p['tests'][0]['cwd']); oldroot,oldqmk,oldpy=cf.ROOT,cf.QMK,sys.executable
  cf.ROOT=clone;cf.QMK=clone/'qmk-8051-ak820';sys.executable=p['tests'][0]['command'][0]
  plan=cf.profile_test_plan(rec['profile'],build,toolchain)
  cf.ROOT,cf.QMK,sys.executable=oldroot,oldqmk,oldpy
  assert p['passed'] is True and p['hardware_validated'] is False and p['physical_device_commands']==0
  assert rec['profile_suites']==[x[0] for x in plan]==[x['id'] for x in p['tests']]
  previous=profile_at
  for row,(name,cwd,cmd) in zip(p['tests'],plan):
   position=command_log.find('RUN PROFILE '+name,previous)
   assert position>=previous, 'Missing/out-of-order profile command'
   previous=position+1
   assert row['command']==cmd and row['cwd']==str(cwd) and row['exit_code']==0
   assert row['build_before']==row['build_after']==ident
   hs('profile-tests/'+name+'.log',row['log_sha256'])
   if '-m' in cmd and 'unittest' in cmd:
    counts=cf.unittest_counts(raw('profile-tests/'+name+'.log').decode())
    assert counts['run']>0 and counts['skipped']==0, (name,'empty or skipped unittest suite')
  for feature,count,key in [('mac-pc',10,'ihx_sha256'),('os-indicators',19 if 'mac-pc' in rec['optional_features'] else 13,'linked_image_sha256')]:
   if feature not in rec['optional_features']:continue
   result=json.loads(raw('profile-tests/'+feature+'/results.json'))
   assert result['pass'] is True and result['hardware_validated'] is False
   assert result[key]==ident['ihx_sha256'] and len(result['tests'])==count
   assert len({case['name'] for case in result['tests']})==count and all(case['pass'] for case in result['tests'])
  for sources in [r['source_files'],p['source_files']]:
   for name,h in sources.items():assert sha((ROOT/name).read_bytes())==h,(name,'source changed'); assert frozen_hash(name)==h,(name,'not frozen blob')
  assert bool(c['short_calls'])==rec['short_calls'] is False
  import build_capability_catalog as catalog_tools
  cat=read(FINAL/'capability-catalog.json')
  entry=next(e for e in cat['images'] if e['profile']==rec['profile'])
  assert rec['catalog']=={'sha256':sha((FINAL/'capability-catalog.json').read_bytes()),'entry_sha256':sha(cf.canonical(entry))}
  assert entry['build_identity']==ident and entry['resources']==rec['resources']
  assert entry['features']==sorted(c['configuration']['base_features']+rec['optional_features'])
  assert entry['model']=='ajazz/ak820' and entry['settings_schema']==c['configuration']['nvm_schema']
  assert entry['fixed_limits']==catalog_tools.fixed_limits(folder)
  for key in ('timing_ms','runtime_qmk_settings'):assert entry[key]==c['configuration'][key]
  # Read the retained IHX; the fingerprint includes zero-filled complete windows.
  from pack_ak820 import read_ihex
  assert entry['code_identity']==catalog_tools.code_identity(read_ihex(folder/'ajazz_ak820_vial.ihx'))
  assert entry['evidence_sha256']=={'configuration':sha((folder/'configuration-report.json').read_bytes()),'base_suites':sha((folder/'qualification.json').read_bytes()),'supplemental_suites':sha((folder/'profile-results.json').read_bytes()),'runtime':sha((folder/'runtime-safety/summary.json').read_bytes())}
  assert entry['project_verified'] is True and entry['status']=='development' and entry['compatible_transitions']==[]
  for obj in (entry,cat):
   for key in ('release_approved','hardware_validated','settings_writes_authorized','flashing_authorized'):assert obj[key] is False
  assert sha((folder/'qualification-command.log').read_bytes())==rec['command_log_sha256']
 return {'variant':folder.name,'profile':rec['profile'],'short_calls':rec['short_calls'],'code':rec['resources']['code_bytes'],'bound':r['stack_bound'],'capacity':r['stack_capacity'],'margin':r['stack_margin'],'record_sha256':sha((folder/'record.json').read_bytes()),'raw_sha256':rec['raw_build']['sha256']}
if __name__=='__main__':
 rows=[]
 records=list(FINAL.glob('*/record.json'))
 assert len(records)==4 and {read(f)['profile'] for f in records}==EXPECTED
 assert all(read(f)['short_calls'] is False for f in records)
 # Imported validators must themselves be the source frozen in the matrix.
 for name in ('tools/configure_firmware.py','tools/build_capability_catalog.py','qmk-8051-ak820/util/ak820_profiles.py','qmk-8051-ak820/util/ak820_ci_authorization.py'):
  assert sha((ROOT/name).read_bytes())==frozen_hash(name), (name,'validator differs from frozen source')
 for f in sorted(records):
  try:rows.append(check(f.parent));print(json.dumps(rows[-1]),flush=True)
  except Exception as e:print('FAILED',f,repr(e));raise
 index=INDEX
 assert index['source_commit']==COMMIT and index['qualified_profiles']==4 and index['available_named_profiles']==len(cf.profiles.PROFILES)==21 and index['build_variants']==4
 assert index['release_approved'] is False and index['hardware_validated'] is False and index['physical_device_commands']==0
 assert index['base_suites_per_variant']==28 and index['base_unit_skips']==0
 assert index['base_unit_tests_per_variant']==273==read(records[0])['base_unit_tests']['run']
 assert all(read(f)['base_unit_tests']['run']==index['base_unit_tests_per_variant'] for f in records)
 indexed={item['variant']:item for item in index['variants']}
 assert len(index['variants'])==len(indexed)==4 and set(indexed)=={row['variant'] for row in rows}
 assert index['minimum_stack_margin']==min(row['margin'] for row in rows)
 assert index['supplemental_suites_total']==sum(len(read(FINAL/row['variant']/'record.json')['profile_suites']) for row in rows)
 catalog=read(FINAL/'capability-catalog.json')
 offline_flags(catalog)
 assert catalog['format']=='ak820-development-capability-catalog-1' and catalog['status']=='development-only'
 assert len(catalog['images'])==4 and {e['profile'] for e in catalog['images']}==EXPECTED
 assert len({e['code_identity']['sha256'] for e in catalog['images']})==4
 assert index['catalog_sha256']==sha((FINAL/'capability-catalog.json').read_bytes())
 for row in rows:
  item=indexed[row['variant']];record=read(FINAL/row['variant']/'record.json')
  for name in ['profile','short_calls','record_sha256']:assert item[name]==row[name]
  for name,key in [('code_bytes','code'),('stack_bound','bound'),('stack_capacity','capacity'),('stack_margin','margin'),('raw_build_sha256','raw_sha256')]:assert item[name]==row[key]
  assert item['xram_bytes']==record['resources']['xram']['bytes'] and item['ihx_sha256']==record['identity']['ihx_sha256']
 print('VALIDATED',len(rows))
