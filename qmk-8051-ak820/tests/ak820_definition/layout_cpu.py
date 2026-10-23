#!/usr/bin/env python3
"""Check actual uint32 VIA layout ABI with CODE reads and a batched page cache."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def capture_get(fw):
    target = fw.address("_via_get_layout_options")
    # Store SDCC uint32 return DPL/DPH/B/A without changing it first.
    trampoline = [0x12, target >> 8, target & 255, 0xAC, 0x82, 0xAD, 0x83, 0xAE, 0xF0, 0xFF,
                  0x90, 0x02, 0x00, 0xEC, 0xF0, 0xA3, 0xED, 0xF0, 0xA3, 0xEE, 0xF0, 0xA3, 0xEF, 0xF0,
                  0x02, 0x27, 0]
    return [emitted.memory("rom", 0x2600, trampoline), "run 0x2600 0x2700"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--s51", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    commands = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"]
    observations = []
    for value in range(256):
        label = f"code_read_{value}@"
        commands += [emitted.memory("rom", 0xC728, [value])] + capture_get(fw)
        commands += fw.dump(label, "xram", 0x200, 4)
        observations.append((label, 0x200, [value, 0, 0, 0]))
    # A valid page under an explicit batch exercises the actual EEPROM adapters
    # and backend without pretending the CPU model implements flash programming.
    commands += fw.write("_page_valid", [1]) + fw.write("_cached_page", [0, 0]) + fw.write("_batch_depth", [1])
    values = {low | (high << 16) for low in range(256) for high in (0, 0xA55A, 0xFFFF)}
    values.update((1 << bit) | low for bit in range(16, 32) for low in (0, 0x80, 0xFF))
    for value in sorted(values):
        label = f"write_{value:08x}@"
        page = [0x5A] * 64
        expected = page.copy()
        expected[0x28] = value & 255
        commands += fw.write("_page_data", page) + fw.write("_page_dirty", [0])
        commands += [emitted.memory("sfr", 0xE0, [value >> 24])]
        commands += fw.call("_via_set_layout_options", value & 0xFFFFFF)
        commands += fw.dump_symbol(label + "page@", "_page_data", 64)
        commands += capture_get(fw) + fw.dump(label + "read@", "xram", 0x200, 4)
        observations += [(label + "page@", fw.address("_page_data"), expected),
                         (label + "read@", 0x200, [value & 255, 0, 0, 0])]
    commands += fw.dump_symbol("storage_fault@", "_storage_failed", 1)
    observations.append(("storage_fault@", fw.address("_storage_failed"), [0]))
    log, stack = fw.execute("layout-options", commands)
    tests = []
    for label, address, expected in observations:
        actual = fw.extract(log, label, address, len(expected))
        item = {"label": label, "pass": actual == expected}
        if not item["pass"]:
            item.update(actual=actual, expected=expected)
        tests.append(item)
    report = {"result": "PASS" if all(item["pass"] for item in tests) else "FAIL", "hardware_validated": False,
              "level": "linked C52, actual uint32 ABI and EEPROM adapters; simulated CODE + batched cache, no flash operations",
              "ihx_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "code_read_values": 256, "setter_values": len(values), "initial_sp": fw.initial_sp, **stack, "tests": tests}
    (fw.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("result", "code_read_values", "setter_values", "tested_stack_bytes")}))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
