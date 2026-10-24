#!/usr/bin/env python3
"""Run production Ctrl/GUI controls in the linked image on a C52 CPU fixture."""
import argparse, hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('unlock',ROOT/'tests/ak820_unlock/run.py')
u=importlib.util.module_from_spec(spec); spec.loader.exec_module(u)
spec=importlib.util.spec_from_file_location('emitted',ROOT/'tests/ak820_emitted/run.py')
e=importlib.util.module_from_spec(spec); spec.loader.exec_module(e)

def rows(*keys):
    result=[0]*16
    for r,c in keys: result[r] |= 1<<c
    return result
def assign(r,c,k): return [e.memory('rom',0xC740+2*(8*r+c),k.to_bytes(2,'big'))]
def report(key=0,mods=0): return [mods,0,key,0,0,0,0,0]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-dir',type=Path,required=True)
    p.add_argument('--s51',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    fw=e.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    cg,ctrl,gui,letter,osm,mt,nkro,repeat=(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,2)
    base=fw.initialize()+assign(*cg,0x701b)+assign(*ctrl,0xe0)+assign(*gui,0xe3)+assign(*letter,4)
    cases=[]
    cases.append(u.run_case(fw,'held-physical-modifiers-follow-output-swap',base,[
        ('before','_actual_keyboard_report',8,report(0,9),fw.transition(rows(ctrl,gui),100)),
        ('swapped-held-both-sides','_actual_keyboard_report',8,report(0,9),fw.transition(rows(ctrl,gui,cg),120)),
        ('gui-owner-release-leaves-swapped-ctrl','_actual_keyboard_report',8,report(0,8),fw.transition(rows(ctrl,cg),140)),
        ('letter-with-swapped-ctrl','_actual_keyboard_report',8,report(4,8),fw.transition(rows(ctrl,cg,letter),160)),
        ('ctrl-owner-release','_actual_keyboard_report',8,report(4,0),fw.transition(rows(cg,letter),180)),
        ('gui-alone-swaps-to-ctrl','_actual_keyboard_report',8,report(4,1),fw.transition(rows(gui,cg,letter),200)),
        ('all-released','_actual_keyboard_report',8,report(),fw.transition(rows(),220)),
    ]))
    # All three supported commands act on key-down only, resend immediately,
    # and do not disturb a physical Ctrl owner while the mapping changes.
    mode_setup=fw.initialize()+assign(*cg,0x701b)+assign(*ctrl,0xe0)
    cases.append(u.run_case(fw,'swap-toggle-normal-held-owner',mode_setup,[
        ('ctrl','_actual_keyboard_report',8,report(0,1),fw.transition(rows(ctrl),100)),
        ('swap','_actual_keyboard_report',8,report(0,8),fw.transition(rows(ctrl,cg),120)),
        ('swap-up','_actual_keyboard_report',8,report(0,8),fw.transition(rows(ctrl),140)),
        ('toggle-off','_actual_keyboard_report',8,report(0,1),assign(*cg,0x701d)+fw.transition(rows(ctrl,cg),160)),
        ('toggle-up','_actual_keyboard_report',8,report(0,1),fw.transition(rows(ctrl),180)),
        ('toggle-on','_actual_keyboard_report',8,report(0,8),fw.transition(rows(ctrl,cg),200)),
        ('toggle-up-again','_actual_keyboard_report',8,report(0,8),fw.transition(rows(ctrl),220)),
        ('normal','_actual_keyboard_report',8,report(0,1),assign(*cg,0x701c)+fw.transition(rows(ctrl,cg),240)),
        ('normal-up','_actual_keyboard_report',8,report(0,1),fw.transition(rows(ctrl),260)),
        ('owner-up','_actual_keyboard_report',8,report(),fw.transition(rows(),280)),
    ]))
    # A fully tapped swap control must not consume queued One Shot Ctrl. The
    # queued owner is then consumed by A and released normally.
    setup=fw.initialize()+assign(*cg,0x701b)+assign(*osm,0x52a1)+assign(*letter,4)
    cases.append(u.run_case(fw,'oneshot-ctrl-is-swapped-only-at-output',setup,[
        ('queue','_ak820_oneshot_mods',1,[1],fw.transition(rows(osm),100)+fw.transition(rows(),120)),
        ('queued-output','_actual_keyboard_report',8,report(0,1),[]),
        ('control-down','_ak820_oneshot_mods',1,[1],fw.transition(rows(cg),140)),
        ('control-up','_ak820_oneshot_mods',1,[1],fw.transition(rows(),160)),
        ('mapped-queued-output','_actual_keyboard_report',8,report(0,8),[]),
        ('consumer','_actual_keyboard_report',8,report(4,8),fw.transition(rows(letter),180)),
        ('consumed','_ak820_oneshot_mods',1,[0],[]),
        ('all-up','_actual_keyboard_report',8,report(),fw.transition(rows(),200)),
    ]))
    # Pressed OSM remains a physical modifier while the swap is tapped. It is
    # still allowed to queue on its own up edge, then serves the next key.
    setup=fw.initialize()+assign(*cg,0x701b)+assign(*osm,0x52a1)+assign(*letter,4)
    cases.append(u.run_case(fw,'oneshot-held-osm-survives-swap-tap',setup,[
        ('osm-down','_actual_keyboard_report',8,report(0,1),fw.transition(rows(osm),100)),
        ('control-down','_actual_keyboard_report',8,report(0,8),fw.transition(rows(osm,cg),120)),
        ('control-up','_actual_keyboard_report',8,report(0,8),fw.transition(rows(osm),140)),
        ('osm-up-queues','_ak820_oneshot_mods',1,[1],fw.transition(rows(),160)),
        ('queued-owner-remapped','_actual_keyboard_report',8,report(0,8),[]),
        ('consumer','_actual_keyboard_report',8,report(4,8),fw.transition(rows(letter),180)),
        ('consumed','_ak820_oneshot_mods',1,[0],[]),
        ('all-up','_actual_keyboard_report',8,report(),fw.transition(rows(),200)),
    ]))
    # Toggle to NKRO while the two physical modifier owners are held and check
    # the swapped modifier bitmap, then release the owners independently.
    setup=(fw.initialize()+assign(*cg,0x701b)+assign(*ctrl,0xe0)+assign(*letter,4)+
           assign(*nkro,0x7011))
    cases.append(u.run_case(fw,'nkro-modifier-bitmap-follows-swap',setup,[
        ('physical','_actual_keyboard_report',8,report(4,1),fw.transition(rows(ctrl,letter),100)),
        ('swapped-6kro','_actual_keyboard_report',8,report(4,8),fw.transition(rows(ctrl,cg,letter),120)),
        ('nkro-on','_keymap_config',2,[0x80,0],fw.transition(rows(ctrl,cg,nkro,letter),140)+fw.transition(rows(cg),160)),
        ('swapped-nkro','_actual_keyboard_report',4,[6,8,0x10,0],fw.transition(rows(ctrl,cg,letter),180)),
        ('control-up','_actual_keyboard_report',4,[6,0,0x10,0],fw.transition(rows(cg,letter),200)),
        ('letter-up','_actual_keyboard_report',4,[6,0,0,0],fw.transition(rows(),220)),
    ]))
    # Hold an encoded MT(LGUI, A) action beyond its tapping term. The output
    # changes from GUI to Ctrl when the session swap is pressed, and the MT
    # release removes the owner without leaving a transformed modifier behind.
    mt_setup=fw.initialize()+assign(*cg,0x701b)+assign(*mt,0x2804)
    wait=fw.clock(350)+fw.call('_protocol_task')+['fill xram 0x2201 0x2203 0x12']
    cases.append(u.run_case(fw,'mod-tap-held-gui-owner-swaps-and-releases',mt_setup,[
        ('pending','_actual_keyboard_report',8,report(),fw.transition(rows(mt),100)),
        ('held-gui','_actual_keyboard_report',8,report(0,8),wait),
        ('held-swapped-ctrl','_actual_keyboard_report',8,report(0,1),fw.transition(rows(mt,cg),370)),
        ('released','_actual_keyboard_report',8,report(),fw.transition(rows(cg),390)),
        ('all-up','_actual_keyboard_report',8,report(),fw.transition(rows(),410)),
    ]))
    # The swap key is a control action, not a Repeat source. A later Repeat
    # still replays the last printable key after the control's key-up edge.
    rep_setup=fw.initialize()+assign(*cg,0x701b)+assign(*letter,4)+assign(*repeat,0x7c79)
    cases.append(u.run_case(fw,'ctrl-gui-control-is-not-repeat-history',rep_setup,[
        ('letter','_actual_keyboard_report',8,report(4),fw.transition(rows(letter),100)),
        ('letter-up','_actual_keyboard_report',8,report(),fw.transition(rows(),120)),
        ('control-down','_actual_keyboard_report',8,report(),fw.transition(rows(cg),140)),
        ('control-up','_actual_keyboard_report',8,report(),fw.transition(rows(),160)),
        ('repeat-letter','_actual_keyboard_report',8,report(4),fw.transition(rows(repeat),180)),
        ('repeat-up','_actual_keyboard_report',8,report(),fw.transition(rows(),200)),
    ]))
    # The built-in AK820 macro interpreter produces an encoded modifier owner.
    # A macro-generated GUI down/up must be transformed in the output report
    # while the macro stream and owner cleanup remain unchanged.
    tspec=importlib.util.spec_from_file_location('tap_emitted',ROOT/'tests/ak820_tapping/emitted.py')
    te=importlib.util.module_from_spec(tspec); tspec.loader.exec_module(te)
    trace=te.Trace(fw,'macro-gui-owner-follows-output-swap')
    macro_key=(0,1)
    trace.map(cg,0x701b); trace.map(macro_key,0x7700)
    trace.event(cg,1,100)
    trace.macro([1,2,0xe3,1,3,0xe3])
    trace.event(cg,0,120); trace.check('clean-report',report())
    macro_result=trace.run()
    macro_result['pass']=macro_result['pass_'] and macro_result['hid_send_trace']==[report(0,1),report()]
    macro_result['expected_hid_send_trace']=[report(0,1),report()]
    del macro_result['pass_']
    cases.append(macro_result)
    result={'level':'linked SDCC image in generic C52 CPU simulator; hardware/USB/IRQ behavior unverified',
            'ihx_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),
            'tests':cases,'hardware_validated':False,'pass':all(x['pass'] for x in cases)}
    (fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2)); raise SystemExit(not result['pass'])
if __name__=='__main__': main()
