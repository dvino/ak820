#!/usr/bin/env python3
"""Bounded OSM CPU regressions through the complete linked input pipeline."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('features',ROOT/'tests/ak820_features/run.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
fw=f.emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
if max(fw.code)>=0xc700: raise ValueError('Requires production-bounded image')
osm,key,other,mod,rep=(1,2),(1,3),(6,4),(0,4),(1,5)
results=[]
for mask in (1,2,15,17,18,31):
 mods=(mask&15) << (4 if mask&16 else 0)
 setup=fw.initialize()+f.assign(*osm,0x52a0|mask)
 results.append(f.run_case(fw,'osm-mask-'+str(mask),setup,[
  ('armed','_owned_mods',1,[mods],fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)),
  ('target_down','_actual_keyboard_report',8,f.report(4,mods),fw.transition(f.rows(key),140)),
  ('rolled','_actual_keyboard_report',8,[mods,0,4,5,0,0,0,0],fw.transition(f.rows(key,other),160)),
  ('target_release','_actual_keyboard_report',8,[0,0,0,5,0,0,0,0],fw.transition(f.rows(other),180)),
  ('clean','_owned_mods',1,[0],fw.transition(f.rows(),200)),
 ]))
setup=fw.initialize()+f.assign(*osm,0x52a2)
results.append(f.run_case(fw,'held-chord-does-not-arm',setup,[
 ('held','_actual_keyboard_report',8,f.report(4,2),fw.transition(f.rows(osm),100)+fw.transition(f.rows(osm,key),120)),
 ('clean','_owned_mods',1,[0],fw.transition(f.rows(osm),140)+fw.transition(f.rows(),160)),
 ('next_plain','_actual_keyboard_report',8,f.report(5),fw.transition(f.rows(other),180)),
]))
results.append(f.run_case(fw,'physical-owner-survives-consumption',setup,[
 ('target','_actual_keyboard_report',8,f.report(4,2),fw.transition(f.rows(mod),80)+fw.transition(f.rows(mod,osm),100)+fw.transition(f.rows(mod),120)+fw.transition(f.rows(mod,key),140)),
 ('physical_remains','_owned_mods',1,[2],fw.transition(f.rows(mod),160)),
 ('all_clean','_owned_mods',1,[0],fw.transition(f.rows(),180)),
]))
setup2=setup+f.assign(*other,0x52a1)
results.append(f.run_case(fw,'busy-osm-holds-without-rearming',setup2,[
 ('consumer','_owned_mods',1,[2],fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)+fw.transition(f.rows(key),140)),
 ('busy_hold','_owned_mods',1,[3],fw.transition(f.rows(key,other),160)),
 ('busy_release','_owned_mods',1,[2],fw.transition(f.rows(key),180)),
 ('consumer_up','_owned_mods',1,[0],fw.transition(f.rows(),200)),
 ('plain_next','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),220)),
]))
results.append(f.run_case(fw,'unlock-cancels-queued-and-held-state',setup,[
 ('armed','_owned_mods',1,[2],fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)),
 ('unlock_clear','_owned_mods',1,[0],f.unlock.vial(fw,6)),
 ('plain_after_unlock','_actual_keyboard_report',8,f.report(4),f.unlock.vial(fw,8)+fw.transition(f.rows(key),160)),
]))
results.append(f.run_case(fw,'repeat-retains-consumed-modifier',setup+f.assign(*rep,0x7c79),[
 ('target','_actual_keyboard_report',8,f.report(4,2),fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)+fw.transition(f.rows(key),140)),
 ('repeat','_actual_keyboard_report',8,f.report(4,2),fw.transition(f.rows(),160)+fw.transition(f.rows(rep),180)),
 ('repeat_release','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),200)),
]))
results.append(f.run_case(fw,'caps-word-and-osm-owners',setup+fw.call('_caps_word_on'),[
 ('shifted','_actual_keyboard_report',8,f.report(4,2),fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)+fw.transition(f.rows(key),140)),
 ('osm_consumed','_owned_mods',1,[0],fw.transition(f.rows(),160)),
 ('caps_still_on','_caps_word_active',1,[1],[]),
]))
combo=[4,0,5,0,0x20,8,1,0,6,0]
combo_setup=setup+[f.emitted.memory('rom',0xc700+0x658,combo)]+fw.call('_ak820_combo_reload')
results.append(f.run_case(fw,'combo-output-consumes-osm',combo_setup,[
 ('armed','_owned_mods',1,[2],fw.transition(f.rows(osm),100)+fw.transition(f.rows(),120)),
 ('combo_shifted','_actual_keyboard_report',8,f.report(6,2),fw.transition(f.rows(key),140)+fw.transition(f.rows(key,other),160)),
 ('combo_release_clean','_owned_mods',1,[0],fw.transition(f.rows(other),180)+fw.transition(f.rows(),200)),
]))
for active in (False, True):
 prep=fw.transition(f.rows(osm),100)
 if active: prep+=fw.transition(f.rows(),120)+fw.transition(f.rows(key),140)
 results.append(f.run_case(fw,'unlock-'+('consumer' if active else 'held-osm'),setup,[
  ('owned','_owned_mods',1,[2],prep),
  ('unlock_clears','_owned_mods',1,[0],f.unlock.vial(fw,6)),
  ('suppressed_release','_owned_mods',1,[0],fw.transition(f.rows(),160)),
  ('plain_after','_actual_keyboard_report',8,f.report(4),f.unlock.vial(fw,8)+fw.transition(f.rows(key),180)),
 ]))
result={'level':'uCsim C52 complete linked code; no physical USB/IRQ validation','ihx_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),'tests':results,'hardware_validated':False,'pass':all(x['pass'] for x in results)}
(fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not result['pass'])
