#!/usr/bin/env python3
"""Exercise compact Auto Shift through the exact linked C52 Quantum pipeline."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('features',ROOT/'tests/ak820_features/run.py')
features=importlib.util.module_from_spec(spec);spec.loader.exec_module(features)
emitted,run_case=features.emitted,features.run_case
rows,assign,report=features.rows,features.assign,features.report

def tick(fw,time):
    return fw.clock(time)+fw.call('_protocol_task')+['fill xram 0x2201 0x2203 0x12']

def cases(fw):
    a,b,shift,ctrl,control=(1,3),(6,4),(0,4),(0,5),(1,2)
    setup=fw.initialize()
    yield run_case(fw,'as-threshold-and-release',setup,[
        ('pending','_actual_keyboard_report',8,report(),fw.transition(rows(a),100)),
        ('early','_actual_keyboard_report',8,report(),tick(fw,280)),
        ('shifted','_actual_keyboard_report',8,report(4,2),tick(fw,281)),
        ('held','_actual_keyboard_report',8,report(4,2),tick(fw,500)),
        ('released','_actual_keyboard_report',8,report(),fw.transition(rows(),520)),
    ])
    yield run_case(fw,'as-short-and-interrupted',setup,[
        ('short','_actual_keyboard_report',8,report(),fw.transition(rows(a),100)+fw.transition(rows(),120)),
        ('pending','_as_state',1,[1],fw.transition(rows(a),200)),
        ('interrupted','_actual_keyboard_report',8,[0,0,4,5,0,0,0,0],fw.transition(rows(a,b),220)),
        ('first_up','_actual_keyboard_report',8,[0,0,0,5,0,0,0,0],fw.transition(rows(b),240)),
        ('both_up','_actual_keyboard_report',8,report(),fw.transition(rows(),260)),
    ])
    yield run_case(fw,'as-remap-freezes-keycode',setup,[
        ('pending','_as_state',1,[1],fw.transition(rows(a),100)),
        ('original_down','_actual_keyboard_report',8,report(4,2),assign(*a,5)+tick(fw,281)),
        ('original_up','_actual_keyboard_report',8,report(),fw.transition(rows(),300)),
        ('remapped_down','_actual_keyboard_report',8,report(5,2),fw.transition(rows(a),400)+tick(fw,581)),
        ('remapped_up','_actual_keyboard_report',8,report(),fw.transition(rows(),600)),
    ])
    for owner_first in (False,True):
        yield run_case(fw,'as-real-shift-'+str(int(owner_first)),setup,[
            ('auto_shift','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),100)+tick(fw,281)),
            ('both','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a,shift),300)),
            ('first_up','_actual_keyboard_report',8,report(0 if owner_first else 4,2),fw.transition(rows(shift) if owner_first else rows(a),320)),
            ('all_up','_actual_keyboard_report',8,report(),fw.transition(rows(),340)),
        ])
    yield run_case(fw,'as-ctrl-bypasses-delay',setup,[
        ('hotkey','_actual_keyboard_report',8,report(4,1),fw.transition(rows(ctrl),100)+fw.transition(rows(ctrl,a),120)),
        ('no_owner','_as_state',1,[0],[]),
        ('all_up','_actual_keyboard_report',8,report(),fw.transition(rows(),140)),
    ])
    yield run_case(fw,'as-encoded-control-owner-bypass',setup+assign(*control,0x0106),[
        ('encoded_ctrl','_actual_keyboard_report',8,report(6,1),fw.transition(rows(control),100)),
        ('basic_immediate','_actual_keyboard_report',8,[1,0,6,4,0,0,0,0],fw.transition(rows(control,a),120)),
        ('no_owner','_as_state',1,[0],[]),
        ('owner_preserved','_actual_keyboard_report',8,report(6,1),fw.transition(rows(control),140)),
        ('all_up','_actual_keyboard_report',8,report(),fw.transition(rows(),160)),
    ])
    yield run_case(fw,'as-held-owner-new-key',setup,[
        ('shifted_origin','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),100)+tick(fw,281)),
        ('new_key_immediate','_actual_keyboard_report',8,[2,0,4,5,0,0,0,0],fw.transition(rows(a,b),300)),
        ('shift_owner_up','_actual_keyboard_report',8,[0,0,0,5,0,0,0,0],fw.transition(rows(b),320)),
        ('both_up','_actual_keyboard_report',8,report(),fw.transition(rows(),340)),
    ])
    for code,name in ((0x7c79,'repeat'),(0x7c7a,'alt-repeat')):
        src,out=(4,4) if code==0x7c79 else (0x2f,0x30)
        yield run_case(fw,'as-'+name+'-remembers-shift',setup+assign(*a,src)+assign(*control,code),[
            ('origin','_actual_keyboard_report',8,report(src,2),fw.transition(rows(a),100)+tick(fw,281)),
            ('origin_up','_actual_keyboard_report',8,report(),fw.transition(rows(),300)),
            ('replayed','_actual_keyboard_report',8,report(out,2),fw.transition(rows(control),320)),
            ('replay_up','_actual_keyboard_report',8,report(),fw.transition(rows(),340)),
        ])
    yield run_case(fw,'as-oneshot-bypasses-delay',setup+assign(*control,0x52a2),[
        ('one_shot','_actual_keyboard_report',8,report(0,2),fw.transition(rows(control),100)+fw.transition(rows(),120)),
        ('immediate','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),140)),
        ('no_owner','_as_state',1,[0],[]),
        ('consumed','_actual_keyboard_report',8,report(),fw.transition(rows(),160)),
    ])
    yield run_case(fw,'as-caps-word',setup+fw.call('_caps_word_on'),[
        ('capital','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),100)+tick(fw,281)),
        ('up','_actual_keyboard_report',8,report(0,2),fw.transition(rows(),300)),
        ('caps_off','_actual_keyboard_report',8,report(),fw.call('_caps_word_off')),
    ])
    for shifted in (False,True):
        prepared=fw.transition(rows(a),100)+(tick(fw,281) if shifted else [])
        yield run_case(fw,'as-clear-'+str(int(shifted)),setup,[
            ('clear','_actual_keyboard_report',8,report(),prepared+fw.call('_clear_keyboard')),
            ('no_tick_revival','_actual_keyboard_report',8,report(),tick(fw,500)),
            ('no_release_revival','_actual_keyboard_report',8,report(),fw.transition(rows(),520)),
            ('next_owner','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),600)+tick(fw,781)),
            ('next_up','_actual_keyboard_report',8,report(),fw.transition(rows(),800)),
        ])
        yield run_case(fw,'as-unlock-'+str(int(shifted)),setup,[
            ('clear','_actual_keyboard_report',8,report(),prepared+features.unlock.vial(fw,6)),
            ('blocked_release','_actual_keyboard_report',8,report(),fw.transition(rows(),400)),
            ('cancel_unlock','_actual_keyboard_report',8,report(),features.unlock.vial(fw,8)+tick(fw,500)),
            ('next_owner','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),600)+tick(fw,781)),
            ('next_up','_actual_keyboard_report',8,report(),fw.transition(rows(),800)),
        ])
    yield run_case(fw,'as-timer-wrap',setup,[
        ('pending','_actual_keyboard_report',8,report(),fw.transition(rows(a),65500)),
        ('early','_actual_keyboard_report',8,report(),tick(fw,144)),
        ('wrapped','_actual_keyboard_report',8,report(4,2),tick(fw,145)),
        ('up','_actual_keyboard_report',8,report(),fw.transition(rows(),160)),
    ])
    yield run_case(fw,'as-controls-and-held-release',setup+assign(*control,0x7c14),[
        ('disabled','_actual_keyboard_report',8,report(4),fw.transition(rows(a),100)+fw.transition(rows(a,control),120)),
        ('release','_actual_keyboard_report',8,report(),fw.transition(rows(),140)),
        ('immediate','_actual_keyboard_report',8,report(5),fw.transition(rows(b),160)),
        ('up','_actual_keyboard_report',8,report(),fw.transition(rows(),180)),
        ('on','_as_flags',1,[1],assign(*control,0x7c13)+fw.transition(rows(control),200)+fw.transition(rows(),220)),
        ('deferred_again','_actual_keyboard_report',8,report(),fw.transition(rows(a),240)),
        ('shifted_again','_actual_keyboard_report',8,report(4,2),tick(fw,421)),
        ('up_again','_actual_keyboard_report',8,report(),fw.transition(rows(),440)),
    ])

def direct_cases(fw):
    spec=importlib.util.spec_from_file_location('tap_linked',ROOT/'tests/ak820_tapping/emitted.py')
    tap=importlib.util.module_from_spec(spec);spec.loader.exec_module(tap)
    for duration in (174,175):
        t=tap.Trace(fw,'as-exact-release-'+str(duration));t.map((0,0),4)
        t.event((0,0),1,100);t.check('pending',report());t.event((0,0),0,100+duration);t.check('released',report())
        result=t.run();expected=[report(4),report()] if duration==174 else [report(4,2),report(0,2),report()]
        result['expected_hid_send_trace']=expected;result['pass']=result.pop('pass_') and result['hid_send_trace']==expected;yield result
    t=tap.Trace(fw,'as-combo-fallback-output-bypass');t.map((0,0),4);t.map((0,1),5)
    combo=[4,0,5,0,0x20,8,1,0,6,0]
    t.commands+=[emitted.memory('rom',0xc700+0x658,combo)]+fw.call('_ak820_combo_reload')
    t.event((0,0),1,100);t.tick(140);t.check('fallback',report(4));t.event((0,0),0,150)
    t.event((0,0),1,200);t.event((0,1),1,220);t.check('combo',report(6));t.tick(500);t.check('still_plain',report(6));t.event((0,0),0,510);t.event((0,1),0,520);t.check('up',report())
    r=t.run();r['pass']=r.pop('pass_');yield r
    t=tap.Trace(fw,'as-encoder-macro-dual-role-bypass');t.commands+=[emitted.memory('rom',0xcd40,[0,4])]
    t.event((253,0),1,100);t.check('encoder_immediate',report(4));t.event((253,0),0,110);t.check('encoder_up',report())
    t.map((0,0),0x2104);t.event((0,0),1,200);t.event((0,0),0,220);t.check('mt_up',report());t.macro([1,2,4]);t.check('macro_down',report(4));t.macro([1,3,4]);t.check('macro_up',report())
    r=t.run();r['pass']=r.pop('pass_');yield r
    has_nkro=fw.compiled_feature('nkro')
    t=tap.Trace(fw,'as-nkro-held-and-release' if has_nkro else 'as-nkro-disabled-stale-setting-held-and-release')
    if has_nkro:
        t.width=32
        t.commands=[c.replace(f'{fw.address("_actual_keyboard_report")+7:#x} 16;',f'{fw.address("_actual_keyboard_report")+31:#x} 16;') for c in t.commands]
    t.commands+=fw.write('_keymap_config',[128,0])+fw.write('_keyboard_protocol',[1]);t.map((0,0),4)
    t.event((0,0),1,100);t.tick(275);t.check('shifted_report',[6,2,16]+[0]*29 if has_nkro else report(4,2))
    t.event((0,0),0,300);t.check('released_report',[6]+[0]*31 if has_nkro else report())
    t.check_memory('setting-retained','_keymap_config',0,[128,0])
    r=t.run();r['pass']=r.pop('pass_');yield r
    for shifted in (False,True):
        t=tap.Trace(fw,('as-nkro-switch-cancels-' if has_nkro else 'as-nkro-disabled-control-keeps-owner-')+str(int(shifted)));t.map((0,0),4);t.map((0,1),0x7013)
        t.event((0,0),1,100)
        if shifted:t.tick(275)
        # At 300 the timeout has elapsed in both traces. A compiled NK_TOGG
        # clears that owner; an omitted control cannot change mode or clear it.
        t.event((0,1),1,300);t.check('control_result',report() if has_nkro else report(4,2))
        t.check_memory('mode','_keymap_config',0,[128,0] if has_nkro else [0,0])
        t.tick(500);t.event((0,0),0,510);t.event((0,1),0,520);t.check('no_revival',report())
        r=t.run();r['pass']=r.pop('pass_');yield r

def mouse_cases(fw):
    if '_mousekey_task' not in fw.symbols:
        return
    # Exercise both features enabled, including their shared USB endpoint.
    # A, Q and B are populated physical positions; row 1/column 4 is masked.
    a,button,right=(1,3),(1,2),(6,4)
    fw.symbols['_as_mouse_report']=fw.address('_input_snapshot')+40
    fw.symbols['_as_mouse_buttons']=fw.address('_input_snapshot')+41
    setup=fw.initialize()+assign(*button,0xd1)+assign(*right,0xd0)
    ready=['fill xram 0x2201 0x2203 0x12']
    yield run_case(fw,'as-pending-mouse-button-interruption',setup,[
        ('pending','_as_state',1,[1],fw.transition(rows(a),100)),
        ('mouse_interrupts_plain','_actual_keyboard_report',8,report(4),fw.transition(rows(a,button),120)),
        ('button_down','_as_mouse_buttons',1,[1],ready+tick(fw,140)),
        ('key_up','_actual_keyboard_report',8,report(),fw.transition(rows(button),160)),
        ('button_still_held','_as_mouse_buttons',1,[1],[]),
        ('button_up','_as_mouse_buttons',1,[0],fw.transition(rows(),180)+ready+tick(fw,200)),
    ])
    yield run_case(fw,'as-held-mouse-movement-and-drag',setup,[
        ('shifted','_actual_keyboard_report',8,report(4,2),fw.transition(rows(a),100)+tick(fw,281)),
        ('move','_as_mouse_report',6,[2,0,8,0,0,0],ready+fw.transition(rows(a,right),300)),
        ('shift_preserved','_actual_keyboard_report',8,report(4,2),[]),
        ('drag','_as_mouse_buttons',1,[1],ready+fw.transition(rows(a,right,button),320)+ready+tick(fw,340)),
        ('owner_up','_actual_keyboard_report',8,report(),fw.transition(rows(right,button),360)),
        ('drag_survives','_as_mouse_buttons',1,[1],[]),
        ('all_up','_as_mouse_buttons',1,[0],fw.transition(rows(),380)+ready+tick(fw,400)),
        ('no_key_revival','_actual_keyboard_report',8,report(),tick(fw,600)),
    ])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir',required=True,type=Path);parser.add_argument('--s51',required=True,type=Path);parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args();fw=emitted.Firmware(args.build_dir.resolve(),args.s51.resolve(),args.output_dir.resolve(),auto_shift=True)
    if max(fw.code)>=0xc700:raise ValueError('Requires a bounded image below fake NVM')
    result={'linked_image_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),'level':'uCsim generic C52, exact linked pipeline; no hardware/USB/IRQ timing proof','hardware_validated':False,'tests':list(cases(fw))+list(direct_cases(fw))+list(mouse_cases(fw))}
    result['pass']=all(t['pass'] and t['fixture_auto_shift']=='enabled-default' for t in result['tests']);(fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not result['pass'])
if __name__=='__main__':main()
