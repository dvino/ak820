#!/usr/bin/env python3
"""Verify linked FD01 instructions and no-IAP routing in offline uCsim only.

The ordinary C52 simulator does not implement the CH555 USB controller or Flash.
RAM/MMIO fixtures are explicit; this tests the actual compiled handler and ABI.
It is not a physical timing or persistence test.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--build", required=True, type=Path)
parser.add_argument("--simulator", required=True, type=Path)
parser.add_argument("--output", required=True, type=Path)
args = parser.parse_args()
fw = emitted.Firmware(args.build.resolve(), args.simulator.resolve(), args.output.resolve())
cases = []
for failed in (0, 1):
    commands = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"]
    nv = [failed, 1, 1, 7, 0x12, 0, 12 if failed else 0]
    for name, values in (
        ("_storage_failed", [nv[0]]), ("_page_valid", [nv[1]]), ("_page_dirty", [nv[2]]),
        ("_batch_depth", [nv[3]]), ("_cached_page", nv[4:6]), ("_first_failure_stage", [nv[6]]),
        ("_ak820_flash_diagnostic", [1, 0x9a, 0x40, 0x42, 0x80, 0xc7]),
        ("_vial_unlocked", [0]), ("_vial_unlock_in_progress", [1]),
        ("_USB_EnumStatus", [1]), ("_D0UsbConfig", [1]), ("_USB_SleepStatus", [0]),
        ("_raw_state", [2]), ("_raw_buffer", [0xfd, 1] + [0xa5] * 30),
    ):
        commands += fw.write(name, values)
    commands += [emitted.memory("xram", 0x2203, [0x12]), emitted.memory("sfr", 0xa8, [0])]
    forbidden = ["_ak820_nvm_begin", "_ak820_nvm_flush", "_ak820_nvm_end", "_ak820_flash_erase", "_ak820_flash_program", "_ak820_flash_program_page"]
    commands += [f"break {fw.address(name):#x}" for name in forbidden]
    commands += fw.call("_ak820_usb_raw_task")
    commands += fw.dump("reply", "xram", 0x10c0, 32)
    commands += fw.dump_symbol("state", "_raw_state", 1)
    commands += fw.dump_symbol("fault", "_first_failure_stage", 1)
    commands += fw.dump_symbol("dirty", "_page_dirty", 1)
    commands += fw.dump_symbol("batch", "_batch_depth", 1)
    commands += fw.dump("endpoint", "xram", 0x2203, 1)
    log, stack = fw.execute(f"fd01-failed-{failed}", commands)
    response = fw.extract(log, "reply", 0x10c0, 32)
    expected = [0xfd, 1, 1, 0xa8] + nv + [1, 0x9a, 0x40, 0x42, 0x80, 0xc7, 0, 1, 1, 0, 3] + [0] * 10
    assert response == expected, (response, expected)
    assert fw.extract(log, "state", fw.address("_raw_state"), 1) == [5]
    assert fw.extract(log, "fault", fw.address("_first_failure_stage"), 1) == [nv[6]]
    assert fw.extract(log, "dirty", fw.address("_page_dirty"), 1) == [1]
    assert fw.extract(log, "batch", fw.address("_batch_depth"), 1) == [7]
    assert fw.extract(log, "endpoint", 0x2203, 1)[0] & 3 == 0
    cases.append({"failed": failed, "reply": bytes(response).hex(), "pass": True, **stack})

report = {"result": "PASS", "level": "actual linked CPU instructions with explicit RAM/MMIO fixtures", "physical_usb_opened": False,
          "ihx_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(), "cases": cases}
(args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
