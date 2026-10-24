#!/usr/bin/env python3
"""Exercise volatile GUI controls in the complete linked C52 image, offline."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('features',ROOT/'tests/ak820_features/run.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build-dir',type=Path,required=True)
p.add_argument('--s51',type=Path,required=True)
p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args()
fw=f.emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
if max(fw.code)>=0xc700: raise ValueError('Requires production-bounded image')
control,gui,key,mod=(1,2),(1,3),(6,4),(0,4)
results=[]
for usage,mask in ((0xe3,8),(0xe7,128)):
    setup=fw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,usage)+f.assign(*key,4)
    results.append(f.run_case(fw,'held-gui-'+str(usage),setup,[
        ('default','_actual_keyboard_report',8,f.report(0,mask),fw.transition(f.rows(gui),100)),
        ('off','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(gui,control),120)),
        ('owner-kept','_owned_mods',1,[mask],[]),
        ('control-up','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(gui),140)),
        ('typing','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(gui,key),160)),
        ('on-held','_actual_keyboard_report',8,f.report(4,mask),f.assign(*control,0x7009)+fw.transition(f.rows(gui,key,control),180)),
        ('on-release','_actual_keyboard_report',8,f.report(4,mask),fw.transition(f.rows(gui,key),200)),
        ('gui-up','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),220)),
        ('all-up','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),240)),
    ]))
setup=fw.initialize()+f.assign(*control,0x700b)+f.assign(*gui,0x0904)
results.append(f.run_case(fw,'encoded-control-gui-and-toggle',setup,[
    ('encoded','_actual_keyboard_report',8,f.report(4,9),fw.transition(f.rows(gui),100)),
    ('off-only-gui','_actual_keyboard_report',8,f.report(4,1),fw.transition(f.rows(gui,control),120)),
    ('owner-kept','_owned_weak_mods',1,[9],[]),
    ('up-no-toggle','_actual_keyboard_report',8,f.report(4,1),fw.transition(f.rows(gui),140)),
    ('on','_actual_keyboard_report',8,f.report(4,9),fw.transition(f.rows(gui,control),160)),
    ('all-up','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),180)),
]))
setup=fw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,0xe3)
results.append(f.run_case(fw,'clear-keeps-session-mask-with-clean-owners',setup,[
    ('off','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(control),100)+fw.transition(f.rows(),120)),
    ('masked','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(gui),140)),
    ('clear','_owned_mods',1,[0],fw.call('_clear_keyboard')),
    ('late-release','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),160)),
    ('new-still-masked','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(gui),180)),
    ('on-new-owner','_actual_keyboard_report',8,f.report(0,8),f.assign(*control,0x7009)+fw.transition(f.rows(gui,control),200)),
    ('clean','_owned_mods',1,[0],fw.transition(f.rows(),220)),
]))
features=set(json.loads((fw.build/'build-report.json').read_text())['configuration']['optional_features'])
if 'one-shot' in features:
    setup=fw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,0x52a8)+f.assign(*key,4)
    results.append(f.run_case(fw,'one-shot-gui-masked-and-consumed',setup,[
        ('off','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(control),100)+fw.transition(f.rows(),120)),
        ('queue-masked','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(gui),140)+fw.transition(f.rows(),160)),
        ('queued','_owned_mods',1,[8],[]),
        ('consume','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),180)),
        ('consumed','_owned_mods',1,[0],fw.transition(f.rows(),200)),
        ('on-no-resurrection','_actual_keyboard_report',8,f.report(),f.assign(*control,0x7009)+fw.transition(f.rows(control),220)+fw.transition(f.rows(),240)),
    ]))
    for osm_state in ('queued','held'):
        setup=fw.initialize()+f.assign(*control,0x700b)+f.assign(*gui,0x52a1)+f.assign(*key,4)
        preparation=fw.transition(f.rows(gui),100)
        held=(gui,)
        if osm_state=='queued':
            preparation+=fw.transition(f.rows(),120)
            held=()
        results.append(f.run_case(fw,'controls-preserve-'+osm_state+'-one-shot',setup,[
            ('before','_owned_mods',1,[1],preparation),
            ('toggle','_owned_mods',1,[1],fw.transition(f.rows(*held,control),140)),
            ('control-up','_owned_mods',1,[1],fw.transition(f.rows(*held),160)),
            ('on','_owned_mods',1,[1],f.assign(*control,0x7009)+fw.transition(f.rows(*held,control),180)),
            ('on-up','_owned_mods',1,[1],fw.transition(f.rows(*held),200)),
            ('off','_owned_mods',1,[1],f.assign(*control,0x700a)+fw.transition(f.rows(*held,control),220)),
            ('off-up','_owned_mods',1,[1],fw.transition(f.rows(*held),240)),
            ('queued-after-release','_ak820_oneshot_mods',1,[1],fw.transition(f.rows(),260)),
            ('consumer','_actual_keyboard_report',8,f.report(4,1),fw.transition(f.rows(key),280)),
            ('consumed','_owned_mods',1,[0],fw.transition(f.rows(),300)),
        ]))
setup=fw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,0x0804)+f.assign(*key,0x7c79)
results.append(f.run_case(fw,'gui-controls-preserve-repeat-history',setup,[
    ('original','_actual_keyboard_report',8,f.report(4,8),fw.transition(f.rows(gui),100)),
    ('up','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),120)),
    ('off','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(control),140)+fw.transition(f.rows(),160)),
    ('repeat-masked','_actual_keyboard_report',8,f.report(4),fw.transition(f.rows(key),180)),
    ('repeat-up','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),200)),
    ('on','_actual_keyboard_report',8,f.report(),f.assign(*control,0x7009)+fw.transition(f.rows(control),220)+fw.transition(f.rows(),240)),
    ('repeat-restored','_actual_keyboard_report',8,f.report(4,8),fw.transition(f.rows(key),260)),
    ('clean','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(),280)),
]))
if 'nkro-control' in features:
    setup=fw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,0xe7)+f.assign(*key,4)+f.assign(*mod,0x7011)
    results.append(f.run_case(fw,'mask-survives-nkro-switch',setup,[
        ('off','_actual_keyboard_report',8,f.report(),fw.transition(f.rows(control),100)+fw.transition(f.rows(),120)),
        ('nkro','_keymap_config',2,[0x80,0],fw.transition(f.rows(mod),140)+fw.transition(f.rows(),160)),
        ('nkro-masked','_actual_keyboard_report',4,[6,0,0x10,0],fw.transition(f.rows(gui,key),180)),
        ('nkro-on','_actual_keyboard_report',4,[6,0x80,0x10,0],f.assign(*control,0x7009)+fw.transition(f.rows(gui,key,control),200)),
        ('clean','_actual_keyboard_report',4,[6,0,0,0],fw.transition(f.rows(),220)),
    ]))
# Combined features retain their raw modifiers; GUI masks only publication.
if 'dynamic-macros' in features:
    dm=(0,5)
    setup=(fw.initialize()+f.assign(*dm,0x7c53)+f.assign(*control,0x700a)+
           f.assign(*gui,0xe3)+f.assign(*key,4)+f.assign(*mod,0xe0))
    results.append(f.run_case(fw,'gui-dynamic-macro-raw-capture-and-replay',setup,[
        ('record','_dm_record',1,[1],fw.transition(f.rows(dm),100)+fw.transition(f.rows(),120)),
        ('masked-owner','_actual_keyboard_report',8,f.report(0,1),fw.transition(f.rows(gui,mod),140)+fw.transition(f.rows(gui,mod,control),160)+fw.transition(f.rows(gui,mod),180)),
        ('recorded-key','_actual_keyboard_report',8,f.report(4,1),fw.transition(f.rows(gui,mod,key),200)),
        ('raw-capture','_dm_taps',2,[4,9],fw.transition(f.rows(gui,mod),220)),
        ('toggle','_actual_keyboard_report',8,f.report(0,9),f.assign(*control,0x700b)+fw.transition(f.rows(gui,mod,control),240)+fw.transition(f.rows(gui,mod),260)),
        ('on','_actual_keyboard_report',8,f.report(0,9),f.assign(*control,0x7009)+fw.transition(f.rows(gui,mod,control),280)+fw.transition(f.rows(gui,mod),300)),
        ('off','_actual_keyboard_report',8,f.report(0,1),f.assign(*control,0x700a)+fw.transition(f.rows(gui,mod,control),320)+fw.transition(f.rows(gui,mod),340)),
        ('controls-not-recorded','_dm_lengths',2,[1,0],fw.transition(f.rows(mod),360)+f.assign(*dm,0x7c55)+fw.transition(f.rows(mod,dm),380)+fw.transition(f.rows(mod),400)),
        # Each transition has two task calls six ms apart. Keep GU_ON inside
        # the ten-ms playback phase so it reveals the same active macro tap.
        ('replay-masked','_actual_keyboard_report',8,f.report(4,1),f.assign(*dm,0x7c56)+fw.transition(f.rows(mod,dm),420)+fw.transition(f.rows(mod),427)+fw.clock(436)+fw.call('_protocol_task')+['fill xram 0x2201 0x2203 0x12']),
        ('replay-owner','_owned_mods',1,[9],[]),
        ('on-during-replay','_actual_keyboard_report',8,f.report(4,9),f.assign(*control,0x7009)+fw.transition(f.rows(mod,control),437)),
        ('release-keeps-ctrl','_actual_keyboard_report',8,f.report(0,1),fw.transition(f.rows(mod),450)),
        ('only-physical-owner','_owned_mods',1,[1],[]),
        ('replay-finished','_dm_play',1,[0],fw.transition(f.rows(mod),480)),
        ('clean','_owned_mods',1,[0],fw.transition(f.rows(),500)),
        ('clean-report','_actual_keyboard_report',8,f.report(),[]),
    ]))
if 'auto-shift' in features:
    # Ordinary GUI cases explicitly use AS_OFF; this interaction keeps the
    # production Auto Shift default enabled and reports that fixture mode.
    afw=f.emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve(),auto_shift=True)
    def as_tick(now):
        return afw.clock(now)+afw.call('_protocol_task')+['fill xram 0x2201 0x2203 0x12']
    setup=afw.initialize()+f.assign(*control,0x700a)+f.assign(*gui,0xe3)+f.assign(*key,4)
    results.append(f.run_case(afw,'gui-auto-shift-raw-bypass-and-owned-shift',setup,[
        ('off','_actual_keyboard_report',8,f.report(),afw.transition(f.rows(control),100)+afw.transition(f.rows(),120)),
        ('masked-gui-owner','_owned_mods',1,[8],afw.transition(f.rows(gui),140)),
        ('raw-gui-bypasses','_actual_keyboard_report',8,f.report(4),afw.transition(f.rows(gui,key),160)),
        ('not-deferred','_as_state',1,[0],[]),
        ('raw-gui-release','_actual_keyboard_report',8,f.report(),afw.transition(f.rows(),180)),
        ('no-gui-pending','_as_state',1,[1],afw.transition(f.rows(key),200)),
        ('before-175ms','_actual_keyboard_report',8,f.report(),as_tick(380)),
        ('at-175ms','_actual_keyboard_report',8,f.report(4,2),as_tick(381)),
        ('toggle-preserves-shift','_actual_keyboard_report',8,f.report(4,2),f.assign(*control,0x700b)+afw.transition(f.rows(key,control),400)+afw.transition(f.rows(key),420)),
        ('gui-and-shift','_actual_keyboard_report',8,f.report(4,10),afw.transition(f.rows(key,gui),440)),
        ('mask-only-gui','_actual_keyboard_report',8,f.report(4,2),afw.transition(f.rows(key,gui,control),460)),
        ('both-owners-kept','_owned_mods',1,[10],[]),
        ('shift-survives-gui-release','_actual_keyboard_report',8,f.report(4,2),afw.transition(f.rows(key),480)),
        ('all-up','_actual_keyboard_report',8,f.report(),afw.transition(f.rows(),500)),
        ('no-owner-leak','_owned_mods',1,[0],[]),
    ]))
# Observe endpoint FIFO as well as application state when a GUI release waits.
spec=importlib.util.spec_from_file_location('transport',ROOT/'tests/ak820_transport_retry/run.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
setup=fw.initialize()+fw.call('_register_code',0xe3)
control_call=lambda code: fw.write('_ak820_gui_process_PARM_2',[1])+fw.call('_ak820_gui_process',code)
results.append(t.case(fw,'gui-off-retries-busy-endpoint',setup,[
    ('down-accepted',0x1040,f.report(0,8),[]),
    ('off-pending',0x1040,f.report(0,8),control_call(0x700a)+t.post(fw)),
    ('release-accepted',0x1040,f.report(),t.ready(1)+t.post(fw)),
    ('on-pending',0x1040,f.report(),control_call(0x7009)+t.post(fw)),
    ('held-gui-restored',0x1040,f.report(0,8),t.ready(1)+t.post(fw)),
    ('physical-release',0x1040,f.report(),fw.call('_unregister_code',0xe3)+t.ready(1)+t.post(fw)),
]))
setup=fw.initialize()+control_call(0x700a)+fw.call('_register_code',0xe3)
results.append(t.case(fw,'gui-mask-survives-resume-cleanup',setup,[
    ('sleep',fw.address('_actual_keyboard_report'),f.report(),fw.write('_USB_SleepStatus',[2])+t.post(fw)),
    ('resume-clears',fw.address('_actual_keyboard_report'),f.report(),fw.write('_USB_SleepStatus',[0])+fw.write('_keyboard_reset',[1])+fw.call('_protocol_pre_task')+t.post(fw)),
    ('new-gui-masked',fw.address('_actual_keyboard_report'),f.report(),fw.call('_register_code',0xe3)),
    ('on-exposes-new-owner',fw.address('_actual_keyboard_report'),f.report(0,8),control_call(0x7009)),
    ('release',fw.address('_actual_keyboard_report'),f.report(),fw.call('_unregister_code',0xe3)),
]))
result={'level':'uCsim C52 complete linked image; no physical USB/IRQ/flash evidence',
        'ihx_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),
        'tests':results,'hardware_validated':False,'pass':all(x['pass'] for x in results)}
(fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));raise SystemExit(not result['pass'])
