#!/usr/bin/env python3
"""Exercise compact NKRO controls in the complete linked C52 image, offline."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('features',ROOT/'tests/ak820_features/run.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args();fw=f.emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
if max(fw.code)>=0xc700: raise ValueError('Requires production-bounded image')
key,control,second,mod=(1,3),(1,2),(6,4),(0,4)
setup=fw.initialize()+f.assign(*control,0x7011)
checks=[
 ('six_key','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),100)),
 ('on','_keymap_config',2,[0x80,0],fw.transition(f.rows(key,control),120)),
 ('old_owner_cancelled','_owned_mods',1,[0],[]),
 ('accepted_release','_keymap_config',2,[0x80,0],fw.transition(f.rows(),140)),
 ('nkro_key','_actual_keyboard_report',4,[6,0,0x20,0],fw.transition(f.rows(second),160)),
 ('nkro_clear','_keymap_config',2,[0,0],f.assign(*control,0x7012)+fw.transition(f.rows(second,control),180)),
 ('release_clean','_keymap_config',2,[0,0],fw.transition(f.rows(),200)),
 ('six_again','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),220)),
 ('toggle_on','_keymap_config',2,[0x80,0],f.assign(*control,0x7013)+fw.transition(f.rows(key,control),240)),
 ('toggle_release_no_change','_keymap_config',2,[0x80,0],fw.transition(f.rows(),260)),
 ('toggle_off','_keymap_config',2,[0,0],fw.transition(f.rows(control),280)),
]
results=[f.run_case(fw,'on-off-toggle-held-keys',setup,checks)]
# Clearing the old protocol also cancels deferred tap-hold and modifier owners.
setup=fw.initialize()+f.assign(*control,0x7011)+f.assign(*key,0x2204)
results.append(f.run_case(fw,'mode-switch-cancels-tap-and-physical-modifier',setup,[
 ('held_shift','_owned_mods',1,[2],fw.transition(f.rows(key,mod),100)+fw.transition(f.rows(key,mod),310)),
 ('cancelled','_owned_mods',1,[0],fw.transition(f.rows(key,mod,control),330)),
 ('release_no_resurrection','_owned_mods',1,[0],fw.transition(f.rows(),350)),
 ('new_tap','_actual_keyboard_report',4,[6,0,0,0],fw.transition(f.rows(key),370)+fw.transition(f.rows(),390)),
]))
features=set(json.loads((fw.build/'build-report.json').read_text())['configuration']['optional_features'])
if 'tap-dance' in features:
    setup=fw.initialize()+f.assign(*control,0x7011)+f.assign(*key,0x5700)+[f.emitted.memory('rom',0xcdc0,[4,0,0xe0,0,6,0,7,0,200,0])]
    results.append(f.run_case(fw,'mode-switch-cancels-tap-dance-hold',setup,[
        ('held_ctrl','_owned_mods',1,[1],fw.transition(f.rows(key),100)+fw.transition(f.rows(key),310)),
        ('cancelled','_owned_mods',1,[0],fw.transition(f.rows(key,control),330)),
        ('release_no_resurrection','_owned_mods',1,[0],fw.transition(f.rows(),350)),
    ]))
if 'one-shot' in features:
    for state in ('queued','held','consuming'):
        setup=fw.initialize()+f.assign(*control,0x7011)+f.assign(*mod,0x52a1)
        preparation=fw.transition(f.rows(mod),80)
        held=(mod,)
        if state!='held':
            preparation+=fw.transition(f.rows(),100)
            held=()
        if state=='consuming':
            preparation+=fw.transition(f.rows(key),120)
            held=(key,)
        results.append(f.run_case(fw,'mode-switch-cancels-osm-'+state,setup,[
            ('before','_owned_mods',1,[1],preparation),
            ('cancelled','_owned_mods',1,[0],fw.transition(f.rows(*held,control),140)),
            ('queue_empty','_ak820_oneshot_mods',1,[0],[]),
            ('consumer_empty','_ak820_oneshot_consumed',1,[0],[]),
            ('target_empty','_ak820_oneshot_target',1,[255],[]),
            ('releases','_owned_mods',1,[0],fw.transition(f.rows(),160)),
            ('new_plain','_actual_keyboard_report',4,[6,0,0x10,0],fw.transition(f.rows(key),180)),
        ]))
if 'space-cadet' in features:
    for held in (False,True):
        setup=fw.initialize()+f.assign(*control,0x7011)+f.assign(*mod,0x7c1a)
        preparation=fw.transition(f.rows(mod),100)
        if held: preparation+=fw.transition(f.rows(mod),310)
        when=330 if held else 120
        results.append(f.run_case(fw,'mode-switch-cancels-space-cadet-'+str(held),setup,[
            ('before','_owned_mods',1,[2 if held else 0],preparation),
            ('cancelled','_owned_mods',1,[0],fw.transition(f.rows(mod,control),when)),
            ('late_release','_owned_mods',1,[0],fw.transition(f.rows(),when+20)),
            ('new_plain','_actual_keyboard_report',4,[6,0,0x10,0],fw.transition(f.rows(key),when+40)),
        ]))
result={'level':'uCsim C52 complete linked image; no physical USB/IRQ/flash evidence','ihx_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),'tests':results,'hardware_validated':False,'pass':all(x['pass'] for x in results)}
(fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not result['pass'])
