#!/usr/bin/env python3
"""Offline Mouse Keys regressions using the real linked SDCC/Quantum image.

The C52 fixture supplies simulated matrix, NVM and endpoint readiness. It does
not prove physical USB, interrupt timing or pointer behavior on an operating system.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("features", ROOT / "tests/ak820_features/run.py")
features = importlib.util.module_from_spec(spec)
spec.loader.exec_module(features)
emitted, run_case = features.emitted, features.run_case


def mouse(buttons=0, x=0, y=0, v=0, h=0):
    return [2, buttons, x & 255, y & 255, v & 255, h & 255]


def ready(fw):
    return ["fill xram 0x2201 0x2203 0x12"]


def tick(fw, ms):
    return ready(fw) + fw.clock(ms) + fw.call("_mousekey_task")


def key(fw, code, down=True):
    return ready(fw) + fw.call("_register_code" if down else "_unregister_code", code)


def cadence_case(fw, setup, name, code, period, expected, start):
    """Count actual send attempts and inspect the accepted endpoint snapshot."""
    sentinel = [0xa5] * 6
    threshold = (start + period) & 65535
    gap = (threshold + 1000) & 65535
    steps = [
        ('first', fw.clock(start) + key(fw, code), 1, expected),
        ('before', fw.write('_mouse_snapshot', sentinel) + tick(fw, (threshold - 1) & 65535), 0, sentinel),
        ('repeat', tick(fw, threshold), 1, expected),
        ('long_gap', fw.write('_mouse_snapshot', sentinel) + tick(fw, gap), 1, expected),
        ('no_catchup', fw.write('_mouse_snapshot', sentinel) + tick(fw, gap), 0, sentinel),
    ]
    commands = list(setup) + [f'break {fw.address("_ak820_usb_try_send"):#x}',
        'commands 1 "echo @@MOUSE_SEND; run"']
    for label, transition, _, _ in steps:
        commands += ['echo @@BEGIN_' + label] + transition + fw.dump_symbol(label + '@', '_mouse_snapshot', 6)
        commands += ['echo @@END_' + label]
    log, stack = fw.execute(name, commands)
    observations = {}
    for label, _, count, report in steps:
        begin, end = '@@BEGIN_' + label + '\n', '@@END_' + label + '\n'
        lines = log.splitlines(keepends=True)
        if sum(1 for line in lines if line == begin) != 1 or sum(1 for line in lines if line == end) != 1:
            raise ValueError('Missing or ambiguous cadence markers: ' + label)
        segment = ''.join(lines[lines.index(begin) + 1:lines.index(end)])
        observations[label] = {'attempts': segment.count('@@MOUSE_SEND\n'),
                               'report': fw.extract(segment, label + '@', fw.address('_mouse_snapshot'), 6)}
    expected_steps = {label: {'attempts': count, 'report': report} for label, _, count, report in steps}
    return {'name': name, 'pass': observations == expected_steps,
            'observations': observations, 'expected': expected_steps, **stack}


def cases(fw, diagnostic=False, cursor_step=8, cursor_period=20, wheel_step=1, wheel_period=80):
    c, w, cs, ws = cursor_period, wheel_period, cursor_step, wheel_step
    def u16(value):
        value &= 65535
        return [value & 255, value >> 8]
    # A diagnostic overflow image cannot use fake NVM at c740: that address
    # can contain linked instructions. Only direct production ABI is tested.
    setup = (fw.call("_host_set_driver", fw.address("_ch555_usb_stack_driver")) +
             fw.write("_USB_EnumStatus", [1]) + fw.write("_D0UsbConfig", [1]) + ready(fw))
    setup = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"] + setup if diagnostic else fw.initialize()
    snapshot = "_mouse_snapshot"
    yield cadence_case(fw, setup, 'cursor-cadence-send-count', 0xd0, c, mouse(x=cs), 65530)
    yield cadence_case(fw, setup, 'wheel-cadence-send-count', 0xd9, w, mouse(v=ws), 100)
    for code, expected in [(0xcd,mouse(y=-cs)),(0xce,mouse(y=cs)),(0xcf,mouse(x=-cs)),(0xd0,mouse(x=cs)),
                           (0xd9,mouse(v=ws)),(0xda,mouse(v=-ws)),(0xdb,mouse(h=-ws)),(0xdc,mouse(h=ws))]:
        yield run_case(fw, f"direction-{code:02x}", setup, [
            ("immediate",snapshot,6,expected,fw.clock(100)+key(fw,code)),
            ("release_no_motion",snapshot,6,expected,key(fw,code,False)+tick(fw,120)),
        ])
    sentinel = [0xa5] * 6
    gap = (65530 + c + 1000) & 65535
    yield run_case(fw,"cursor-cadence-gap-wrap",setup,[
        ("first",snapshot,6,mouse(x=cs),fw.clock(65530)+key(fw,0xd0)),
        ("before_output",snapshot,6,sentinel,fw.write(snapshot,sentinel)+tick(fw,(65530+c-1)&65535)),
        ("before_threshold","_cursor_time",2,u16(65530),[]),
        ("repeat_output",snapshot,6,mouse(x=cs),tick(fw,(65530+c)&65535)),
        ("threshold","_cursor_time",2,u16(65530+c),[]),
        ("gap_output",snapshot,6,mouse(x=cs),fw.write(snapshot,sentinel)+tick(fw,gap)),
        ("long_gap","_cursor_time",2,u16(gap),[]),
        ("same_tick_output",snapshot,6,sentinel,fw.write(snapshot,sentinel)+tick(fw,gap)),
        ("same_tick_no_catchup","_cursor_time",2,u16(gap),[]),
    ])
    yield run_case(fw,"wheel-threshold",setup,[
        ("first",snapshot,6,mouse(v=ws),fw.clock(100)+key(fw,0xd9)),
        ("before_output",snapshot,6,sentinel,fw.write(snapshot,sentinel)+tick(fw,100+w-1)),
        ("before","_wheel_time",2,u16(100),[]),
        ("repeat_output",snapshot,6,mouse(v=ws),tick(fw,100+w)),
        ("at","_wheel_time",2,u16(100+w),[]),
        ("same_tick_output",snapshot,6,sentinel,fw.write(snapshot,sentinel)+tick(fw,100+w)),
    ])
    yield run_case(fw,"diagonal-opposing-drag",setup,[
        ("right",snapshot,6,mouse(x=cs),fw.clock(100)+key(fw,0xd0)),
        ("up_only",snapshot,6,mouse(y=-cs),key(fw,0xcd)),
        ("diagonal",snapshot,6,mouse(x=cs,y=-cs),tick(fw,100+c)),
        ("opposed_no_immediate",snapshot,6,mouse(x=cs,y=-cs),key(fw,0xcf)),
        ("opposed_repeat",snapshot,6,mouse(y=-cs),tick(fw,100+2*c)),
        ("button_no_motion",snapshot,6,mouse(buttons=1),key(fw,0xd1)),
        ("drag",snapshot,6,mouse(buttons=1,y=-cs),tick(fw,100+3*c)),
        ("button_up_no_motion",snapshot,6,mouse(),key(fw,0xd1,False)),
    ])
    for code in range(0xd1,0xd6):
        yield run_case(fw,f"button-{code-0xd0}",setup,[
            ("down",snapshot,6,mouse(buttons=1<<(code-0xd1)),key(fw,code)),
            ("up",snapshot,6,mouse(),key(fw,code,False)),
        ])
    yield run_case(fw,"busy-final-release-clear",setup,[
        ("held",snapshot,6,mouse(buttons=1),key(fw,0xd1)),
        ("busy_release_retains",snapshot,6,mouse(buttons=1),fw.call("_unregister_code",0xd1)),
        ("retry",snapshot,6,mouse(),tick(fw,101)),
        ("held_again",snapshot,6,mouse(buttons=2),key(fw,0xd2)),
        ("clear_busy_retains",snapshot,6,mouse(buttons=2),fw.call("_clear_keyboard")),
        ("clear_retry",snapshot,6,mouse(),tick(fw,102)),
    ])
    yield run_case(fw,"busy-movement-drops-backlog",setup,[
        ("first",snapshot,6,mouse(x=cs),fw.clock(100)+key(fw,0xd0)),
        ("busy_consumes_tick","_cursor_time",2,u16(100+c),fw.clock(100+c)+fw.call("_mousekey_task")),
        ("busy_consumes_gap","_cursor_time",2,u16(100+3*c),fw.clock(100+3*c)+fw.call("_mousekey_task")),
        ("ready_no_catchup_output",snapshot,6,sentinel,fw.write(snapshot,sentinel)+tick(fw,100+3*c)),
        ("ready_no_catchup","_cursor_time",2,u16(100+3*c),[]),
        ("next_step",snapshot,6,mouse(x=cs),tick(fw,100+4*c)),
    ])
    unsupported = [0xd6,0xd7,0xd8,0xdd,0xde,0xdf]
    commands=[]
    for code in unsupported: commands += key(fw,code)+key(fw,code,False)
    yield run_case(fw,"unsupported-do-not-reset-cadence",setup,[
        ("held",snapshot,6,mouse(x=cs),fw.clock(100)+key(fw,0xd0)),
        ("clock_unchanged","_cursor_time",2,u16(100),fw.clock(100+c-1)+commands),
        ("threshold","_cursor_time",2,u16(100+c),tick(fw,100+c)),
    ])
    if diagnostic:
        return
    a=(1,3)
    physical=setup+features.assign(*a,0xd1)
    yield run_case(fw,"matrix-unlock-release",physical,[
        ("held",snapshot,6,mouse(buttons=1),fw.transition(features.rows(a),100)),
        ("unlock_release",snapshot,6,mouse(),ready(fw)+features.unlock.vial(fw,6)+tick(fw,110)),
        ("suppressed_up",snapshot,6,mouse(),fw.transition(features.rows(),120)),
        ("cancel_clean",snapshot,6,mouse(),features.unlock.vial(fw,8)),
    ])
    # Only a compiled NKRO control changes mode and clears report owners.
    has_nkro=fw.compiled_feature("nkro")
    nkro=(1,2)
    yield run_case(fw,"matrix-nkro-change-release" if has_nkro else "matrix-nkro-disabled-keeps-mouse-owner",physical+features.assign(*nkro,0x7011),[
        ("held",snapshot,6,mouse(buttons=1),fw.transition(features.rows(a),100)),
        ("control_result",snapshot,6,mouse() if has_nkro else mouse(buttons=1),fw.transition(features.rows(a,nkro),120)+tick(fw,130)),
        ("mode","_keymap_config",2,[128,0] if has_nkro else [0,0],[]),
        ("physical_release",snapshot,6,mouse(),fw.transition(features.rows(),140)+tick(fw,150)),
    ])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir",required=True,type=Path)
    parser.add_argument("--s51",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    parser.add_argument("--diagnostic-overflow",action="store_true",help="Direct ABI only; image is not installable")
    for key, default in (("cursor-step", 8), ("cursor-period", 20), ("wheel-step", 1), ("wheel-period", 80)):
        parser.add_argument("--mouse-" + key, type=int, default=default)
    args=parser.parse_args()
    fw=emitted.Firmware(args.build_dir.resolve(),args.s51.resolve(),args.output_dir.resolve())
    if max(fw.code)>=0xc700 and not args.diagnostic_overflow: raise ValueError("Bounded image required for matrix/NVM fixture")
    fw.symbols["_mouse_snapshot"]=fw.address("_input_snapshot")+40
    result={"linked_image_sha256":hashlib.sha256(fw.image.read_bytes()).hexdigest(),
            "level":"uCsim C52 linked production code; simulated peripherals only", "diagnostic_overflow":args.diagnostic_overflow,
            "tests":list(cases(fw,args.diagnostic_overflow,args.mouse_cursor_step,args.mouse_cursor_period,
                               args.mouse_wheel_step,args.mouse_wheel_period)),"hardware_validated":False}
    result["pass"]=all(item["pass"] for item in result["tests"])
    (fw.output/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["pass"] else 1)
if __name__=="__main__": main()
