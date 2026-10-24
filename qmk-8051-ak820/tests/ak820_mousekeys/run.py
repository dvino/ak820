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


def cases(fw, diagnostic=False):
    # A diagnostic overflow image cannot use fake NVM at c740: that address
    # can contain linked instructions. Only direct production ABI is tested.
    setup = (fw.call("_host_set_driver", fw.address("_ch555_usb_stack_driver")) +
             fw.write("_USB_EnumStatus", [1]) + fw.write("_D0UsbConfig", [1]) + ready(fw))
    setup = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"] + setup if diagnostic else fw.initialize()
    snapshot = "_mouse_snapshot"
    for code, expected in [(0xcd,mouse(y=-8)),(0xce,mouse(y=8)),(0xcf,mouse(x=-8)),(0xd0,mouse(x=8)),
                           (0xd9,mouse(v=1)),(0xda,mouse(v=-1)),(0xdb,mouse(h=-1)),(0xdc,mouse(h=1))]:
        yield run_case(fw, f"direction-{code:02x}", setup, [
            ("immediate",snapshot,6,expected,fw.clock(100)+key(fw,code)),
            ("release_no_motion",snapshot,6,expected,key(fw,code,False)+tick(fw,120)),
        ])
    yield run_case(fw,"cursor-cadence-gap-wrap",setup,[
        ("first",snapshot,6,mouse(x=8),fw.clock(65530)+key(fw,0xd0)),
        ("before_threshold","_cursor_time",2,[250,255],tick(fw,13)),
        ("threshold","_cursor_time",2,[14,0],tick(fw,14)),
        ("long_gap","_cursor_time",2,[232,3],tick(fw,1000)),
        ("same_tick_no_catchup","_cursor_time",2,[232,3],tick(fw,1000)),
    ])
    yield run_case(fw,"wheel-threshold",setup,[
        ("first",snapshot,6,mouse(v=1),fw.clock(100)+key(fw,0xd9)),
        ("before","_wheel_time",2,[100,0],tick(fw,179)),
        ("at","_wheel_time",2,[180,0],tick(fw,180)),
    ])
    yield run_case(fw,"diagonal-opposing-drag",setup,[
        ("right",snapshot,6,mouse(x=8),fw.clock(100)+key(fw,0xd0)),
        ("up_only",snapshot,6,mouse(y=-8),key(fw,0xcd)),
        ("diagonal",snapshot,6,mouse(x=8,y=-8),tick(fw,120)),
        ("opposed_no_immediate",snapshot,6,mouse(x=8,y=-8),key(fw,0xcf)),
        ("opposed_repeat",snapshot,6,mouse(y=-8),tick(fw,140)),
        ("button_no_motion",snapshot,6,mouse(buttons=1),key(fw,0xd1)),
        ("drag",snapshot,6,mouse(buttons=1,y=-8),tick(fw,160)),
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
        ("first",snapshot,6,mouse(x=8),fw.clock(100)+key(fw,0xd0)),
        ("busy_consumes_tick","_cursor_time",2,[120,0],fw.clock(120)+fw.call("_mousekey_task")),
        ("busy_consumes_gap","_cursor_time",2,[200,0],fw.clock(200)+fw.call("_mousekey_task")),
        ("ready_no_catchup","_cursor_time",2,[200,0],tick(fw,201)),
        ("next_step",snapshot,6,mouse(x=8),tick(fw,220)),
    ])
    unsupported = [0xd6,0xd7,0xd8,0xdd,0xde,0xdf]
    commands=[]
    for code in unsupported: commands += key(fw,code)+key(fw,code,False)
    yield run_case(fw,"unsupported-do-not-reset-cadence",setup,[
        ("held",snapshot,6,mouse(x=8),fw.clock(100)+key(fw,0xd0)),
        ("clock_unchanged","_cursor_time",2,[100,0],fw.clock(119)+commands),
        ("threshold","_cursor_time",2,[120,0],tick(fw,120)),
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
    # NKRO's compact user control clears all report owners on mode change.
    nkro=(1,2)
    yield run_case(fw,"matrix-nkro-change-release",physical+features.assign(*nkro,0x7011),[
        ("held",snapshot,6,mouse(buttons=1),fw.transition(features.rows(a),100)),
        ("mode_change_release",snapshot,6,mouse(),fw.transition(features.rows(a,nkro),120)+tick(fw,130)),
    ])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir",required=True,type=Path)
    parser.add_argument("--s51",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    parser.add_argument("--diagnostic-overflow",action="store_true",help="Direct ABI only; image is not installable")
    args=parser.parse_args()
    fw=emitted.Firmware(args.build_dir.resolve(),args.s51.resolve(),args.output_dir.resolve())
    if max(fw.code)>=0xc700 and not args.diagnostic_overflow: raise ValueError("Bounded image required for matrix/NVM fixture")
    fw.symbols["_mouse_snapshot"]=fw.address("_input_snapshot")+40
    result={"linked_image_sha256":hashlib.sha256(fw.image.read_bytes()).hexdigest(),
            "level":"uCsim C52 linked production code; simulated peripherals only", "diagnostic_overflow":args.diagnostic_overflow,
            "tests":list(cases(fw,args.diagnostic_overflow)),"hardware_validated":False}
    result["pass"]=all(item["pass"] for item in result["tests"])
    (fw.output/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["pass"] else 1)
if __name__=="__main__": main()
