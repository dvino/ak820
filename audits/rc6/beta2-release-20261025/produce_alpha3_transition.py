"""Offline alpha.3 transition evidence producer. Never opens a device.
Private output must be a new directory. Public evidence contains hashes/counts only.
"""
from pathlib import Path
import argparse, copy, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'tools/installer'),str(ROOT/'tools'),str(ROOT/'qmk-8051-ak820/util')]
import settings_backup as s
p=s.pack
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle',type=Path,required=True)
parser.add_argument('--archive',type=Path,required=True)
parser.add_argument('--stock',type=Path,required=True)
parser.add_argument('--build-paths',type=Path,required=True)
parser.add_argument('--private-output',type=Path,required=True)
args=parser.parse_args()
os.umask(0o077)
root=ROOT; out=args.private_output; out.mkdir(mode=0o700,exist_ok=False)
assert hashlib.sha256(args.archive.read_bytes()).hexdigest()=='3c8ac08db82141a00468bb0839b972d1bdb6ac16652ade89d5f65706448a4d97'
assert subprocess.check_output(['git','rev-parse','v0.6.0-alpha.3'],cwd=root,text=True).strip()=='b17d7c8b52ec7a234a742a64380e22354698030b'
contract_paths=['qmk-8051-ak820/keyboards/ajazz/ak820/ak820_combo.c','qmk-8051-ak820/quantum/dynamic_keymap.c','qmk-8051-ak820/quantum/rgb_matrix/rgb_matrix.h','qmk-8051-ak820/quantum/vialrgb_effects.inc','qmk-8051-ak820/util/pack_ak820.py']
contracts={name:hashlib.sha256(subprocess.check_output(['git','show','b17d7c8b52ec7a234a742a64380e22354698030b:'+name],cwd=root)).hexdigest() for name in contract_paths}
stock=args.stock.read_bytes()
paths=json.loads(args.build_paths.read_text())
catalog=json.loads((root/'tools/installer/settings-catalog.json').read_text())
# Reproduction accepts either original data or exactly this bounded correction.
if any(row['ihx_sha256']==s.FULL_IHX for row in catalog['historical_sources']):
 assert [row for row in catalog['historical_sources'] if row['ihx_sha256']==s.FULL_IHX]==[{'ihx_sha256':s.FULL_IHX,'code_sha256':'01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d'}]
 expected=[{'source':s.FULL_IHX,'target':row['settings_identity']['ihx_sha256']} for row in catalog['profiles']]
 assert [edge for edge in catalog['settings_transitions'] if edge['source']==s.FULL_IHX]==expected
 catalog['historical_sources']=[row for row in catalog['historical_sources'] if row['ihx_sha256']!=s.FULL_IHX]
 catalog['settings_transitions']=[edge for edge in catalog['settings_transitions'] if edge['source']!=s.FULL_IHX]
original_catalog=copy.deepcopy(catalog)
old_report=json.loads((root/'audits/rc6/beta2-release-20261025/transition-preflight.json').read_text())
assert len(old_report['cases']) in (120,130)
if len(old_report['cases'])==130:
 assert all(row['source_case']=='alpha3-packed' for row in old_report['cases'][120:])
 old_report['cases']=old_report['cases'][:120]
 old_report['backup_derivation']=old_report['backup_derivation'].split('; authenticated public alpha3')[0]
assert not any(row['ihx_sha256']==s.FULL_IHX for row in catalog['historical_sources'])
alpha=s.load_profile(args.bundle,stock)
assert alpha['ihx_sha256']==s.FULL_IHX
assert alpha['code_sha256']=='01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d'
catalog['historical_sources'].append({'ihx_sha256':s.FULL_IHX,'code_sha256':alpha['code_sha256']})
for row in catalog['profiles']:
 catalog['settings_transitions'].append({'source':s.FULL_IHX,'target':row['settings_identity']['ihx_sha256']})
s._catalog_images(catalog)
profiles={}
for name,buildpath in paths.items():
 build=Path(buildpath);bundle=out/'bundles'/name
 for folder in ('firmware','reports','reference'):(bundle/folder).mkdir(mode=0o700,parents=True,exist_ok=True)
 for suffix in ('ihx','map','mem'):shutil.copyfile(build/('ajazz_ak820_vial.'+suffix),bundle/('firmware/application.'+suffix))
 shutil.copyfile(build/'build-report.json',bundle/'reports/build-report.json')
 shutil.copyfile(root/'qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json',bundle/'reference/vial.json')
 profiles[name]=s.load_profile(bundle,stock,trusted_catalog=catalog)
def make_backup(name,rom,profile,kind):
 folder=out/'backups'/name;folder.mkdir(mode=0o700,parents=True)
 s.validate_rom(rom,profile);nvm=rom[p.NVM_START:p.NVM_END];image=s._rom_identity(rom,profile);ihx=image['ihx_sha256'];settings=s.settings_from_nvm(nvm,s.rgb_wire(nvm[24:32],image=image),combos=s._combo_capable(profile,ihx))
 files={'settings.json':s.canonical(settings),'before-full-rom.bin':rom,'saved-nvm.bin':nvm,'read-log.jsonl':s.canonical({'offline_derived':True,'source_kind':kind,'physical_device_commands':0}),'.gitignore':b'*\n'}
 manifest={'format':s.FORMAT_V2 if image['build_id']==s.extensions.SCHEMA else s.FORMAT,'created_utc':datetime.now(timezone.utc).isoformat(),'device':s.DEVICE,'definition_sha256':profile['definition_sha256'],'nvm_schema':image['build_id'],'source_build_id':image['build_id'],'source_ihx_sha256':ihx,'code_sha256':image['code_sha256'],'counts':{'layers':6,'physical_keys':83,'assignments':498,'encoder_assignments':12,'macros':16,'macro_capacity':8192},'scope':'Offline derived from saved ROM or exact packed image; no new device capture/getters','files':{name:s._record(data) for name,data in files.items()}}
 for name,data in {**files,'manifest.json':s.canonical(manifest)}.items():path=folder/name;path.write_bytes(data);path.chmod(0o600)
 return s.validate_backup(folder,profile)

rom=bytearray(stock);rom[p.APP_START:p.APP_END]=alpha['payload']
backup=make_backup('alpha3-packed',bytes(rom),profiles['main'],'authenticated public alpha3 exact packed image; offline OEM-derived defaults; no getter capture')
assert backup['source_identity']==(s.FULL_IHX,alpha['code_sha256'])
assert backup['manifest']['nvm_schema']==p.BUILD_ID
results=[];regressions=[]
def check_plan(backup,profile):
 plan=s.plan_restore(backup,profile)
 target_nvm=profile['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START]
 assert plan['key_count']==498 and plan['encoder_count']==12
 assert len(backup['settings']['macros']['commands'])==16 and len(plan['combo_entries'])==8
 assert profile['schema']==s.extensions.SCHEMA
 assert plan['extension_data']==s.extensions.from_nvm(target_nvm)
 assert plan['combo_entries']==backup['settings']['combos']['entries_hex']
 src=s._profile_images(profile)[s.FULL_IHX];dst=s._profile_images(profile)[profile['ihx_sha256']]
 assert s.rgb_wire(plan['rgb_saved_config'],selected=True,image=dst)==s.rgb_wire(backup['nvm'][24:32],selected=True,image=src)
 return plan
for name,profile in profiles.items():
 plan=check_plan(backup,profile)
 row={'source':s.FULL_IHX,'target':profile['ihx_sha256'],'source_case':'alpha3-packed','target_profile':name,'offline_only':True,'physical_device_commands':0,'passed':True,'key_count':498,'encoder_count':12,'macro_count':16,'combo_count':8,'combo_action':'restore','backup_manifest_sha256':backup['identity'],'source_schema':alpha['schema'],'target_schema':profile['schema'],'target_default_extensions_preserved':True,'rgb_translation_verified':True}
 results.append(row);print('alpha3-packed ->',name,'PASS')
# Deliberate offline modifications to authenticated source NVM, never a capture.
variant=bytearray(rom)
at=p.NVM_START+s.DeviceAPI.key_offset(0,s.PHYSICAL[0]);variant[at:at+2]=(4).to_bytes(2,'big')
at=p.NVM_START+s.DeviceAPI.encoder_offset(0,0);variant[at:at+2]=(5).to_bytes(2,'big')
at=p.NVM_START+s.DeviceAPI.COMBO_OFFSET
variant[at:at+10]=s.DeviceAPI.stored_combo(bytes.fromhex('04000500000000000600'))
variant[p.NVM_START+24:p.NVM_START+29]=bytes((6*4+1,73,181,120,41))
modified=make_backup('alpha3-nondefault-fixture',bytes(variant),profiles['main'],'OFFLINE FIXTURE: source NVM basic matrix/encoder key, nonempty Combo, RGB effect31 HSV/brightness/speed changed')
for name,profile in profiles.items():
 plan=check_plan(modified,profile)
 assert modified['settings']['keys'][0]['keycode']==4
 assert modified['settings']['encoders'][0]['keycode']==5
 assert plan['combo_entries'][0]=='04000500000000000600'
 regressions.append({'case':'nondefault-combo-basic-keycode-rgb','target_profile':name,'passed':True,'rgb_saved_config_hex':plan['rgb_saved_config'].hex()})
def rejected(label,back,profile,substring):
 try:s.plan_restore(back,profile)
 except ValueError as error:
  assert substring in str(error),str(error)
  regressions.append({'case':label,'passed':True,'error':str(error)})
 else:raise AssertionError(label+' unexpectedly accepted')
without=copy.deepcopy(profiles['main']);without['settings_transitions']=original_catalog['settings_transitions']
rejected('missing-explicit-edge-before-any-unlock-or-write',backup,without,'not explicitly reviewed')
unsupported=bytearray(rom);at=p.NVM_START+s.DeviceAPI.key_offset(0,s.PHYSICAL[0]);unsupported[at:at+2]=(0x7011).to_bytes(2,'big')
unsupported_backup=make_backup('alpha3-unsupported-keycode-fixture',bytes(unsupported),profiles['main'],'OFFLINE FIXTURE: alpha3 NKRO keycode 0x7011 unsupported by main')
rejected('unsupported-target-keycode',unsupported_backup,profiles['main'],'Unsupported keycode')
direct=bytearray(rom);direct[p.NVM_START+24]=5*4+1
b=make_backup('alpha3-direct-fixture',bytes(direct),profiles['main'],'OFFLINE FIXTURE: selected Direct RGB mode without palette getter')
rejected('rgb-direct-target-without-effect',b,profiles['typing'],'Saved RGB effect is unsupported')
rejected('rgb-direct-palette-no-getter',b,profiles['game'],'Direct Control palette has no getter')
report={**old_report,'backup_derivation':old_report['backup_derivation']+'; authenticated public alpha3 packed image with offline OEM-derived defaults (no live capture)','cases':old_report['cases']+results}
assert report['cases'][:120]==old_report['cases'] and len(report['cases'])==130
for filename in ('tools/installer/settings-catalog.json','web/firmware-matrix.json'):
 value=json.loads((root/filename).read_text())
 assert (value['historical_sources']==original_catalog['historical_sources'] and value['settings_transitions']==original_catalog['settings_transitions']) or (value['historical_sources']==catalog['historical_sources'] and value['settings_transitions']==catalog['settings_transitions'])
 value['historical_sources']=catalog['historical_sources'];value['settings_transitions']=catalog['settings_transitions']
 (root/filename).write_bytes(s.canonical(value))
audit=root/'audits/rc6/beta2-release-20261025'
(audit/'transition-preflight.json').write_bytes(s.canonical(report))
evidence={'format':'ak820-alpha3-transition-fix-1','offline_only':True,'physical_device_commands':0,'hardware_validated':False,'source_kind':'authenticated public alpha3 packed bytes, OEM-derived offline NVM; not live settings/getters','alpha3_ihx_sha256':alpha['ihx_sha256'],'alpha3_code_sha256':alpha['code_sha256'],'alpha3_schema':alpha['schema'],'source_tag_commit':'b17d7c8b52ec7a234a742a64380e22354698030b','public_zip_sha256':'3c8ac08db82141a00468bb0839b972d1bdb6ac16652ade89d5f65706448a4d97','canonical_cases_preserved':120,'canonical_cases_added':10,'canonical_total':130,'explicit_edges_added':10,'actual_alpha3_cases':results,'separate_offline_fixture_regressions':regressions,'limitations':['No USB/device operation or physical update validation.','Packed OEM-default derivation is not a live capture or durable restore proof.','Nondefault settings are explicitly modified offline fixtures.']}
evidence.update(historical_source_contracts=contracts,public_zip_hash_rechecked=True,producer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(audit/'alpha3-transition-fix.json').write_bytes(s.canonical(evidence))
print('PASS: 10 actual alpha3 plans, 10 nondefault fixture plans, 4 fail-closed negatives; old120 preserved')
