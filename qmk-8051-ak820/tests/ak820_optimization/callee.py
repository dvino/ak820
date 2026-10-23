#!/usr/bin/env python3
"""Check the selected callee-save ABI in an actual linked AK820 image.

All operations execute inside generic uCsim C52. Fake NVM/port state is supplied
in simulator memory; neither a device nor physical flash is accessed. R0..R7
are checked independently of functional return values and stack restoration.
Run the same test on an ordinary caller-save build as a negative control.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("ak820_emitted_support", ROOT / "tests/ak820_emitted/run.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
Firmware, memory = _module.Firmware, _module.memory

# This is intentionally a short audited list of source-defined C functions.
# No naked helper or prebuilt SDCC runtime-library function is selected.
FUNCTIONS = {
    "timer_read": "ak820_timer.asm",
    "timer_read32": "ak820_timer.asm",
    "ak820_nvm_ok": "ak820_nvm.asm",
    "get_mods": "quantum/action_util.asm",
    "get_weak_mods": "quantum/action_util.asm",
    "matrix_get_row": "matrix.asm",
    "readPin": "lib/ch555/gpio.asm",
    "eeprom_read_byte": "ak820_nvm.asm",
    "eeprom_update_byte": "eeprom_driver.asm",
    "ak820_flash_read": "ak820_flash.asm",
    "mDelaymS": "lib/ch555/hal.asm",
}


def snapshot(log: str, label: str, address: int, count: int) -> list[int]:
    marker = "@@" + label
    if marker not in log:
        raise ValueError("Missing observation: " + label)
    tail = log.rsplit(marker, 1)[1].split("\necho @@", 1)[0]
    result = bytearray()
    # Single-SFR dumps use a named bit-decoded row, unlike ordinary memory.
    for match in re.finditer(r"^0x([0-9a-f]+)\s+(?:(?:\w+):\s+0b[01]+\s+0x([0-9a-f]{2})|((?:[0-9a-f]{2}\s+)+))", tail, re.M):
        row = int(match[1], 16)
        if row != address + len(result):
            if result:
                raise ValueError("Discontinuous observation: " + label)
            continue
        values = bytes.fromhex(match[2] or match[3])[:16]
        result.extend(values[:count - len(result)])
        if len(result) == count:
            return list(result)
    raise ValueError("Incomplete observation: " + label)


def function_cases(fw: Firmware, function: str):
    # Each case: name, setup, first argument, expected return bytes or None,
    # additional observations (space, address, bytes). All callers use bank 0,
    # as does the compiled firmware; this test does not promise cross-bank ABI.
    if function in ("timer_read", "timer_read32"):
        for value in (0, 1, 255, 256, 65535, 65536, 0x12345678, 0xFFFFFFFF):
            for ie in (0, 0x80):
                yield (f"{value:08x}-{ie:02x}", fw.clock(value) + [memory("sfr", 0xA8, [ie])], None,
                       list(value.to_bytes(4, "little")[:2 if function == "timer_read" else 4]),
                       [("sfr", 0xA8, [ie])])
    elif function == "ak820_nvm_ok":
        for failed in (0, 1):
            yield str(failed), fw.write("_storage_failed", [failed]), None, [1 - failed], []
    elif function in ("get_mods", "get_weak_mods"):
        symbol = "_real_mods" if function == "get_mods" else "_weak_mods"
        for value in range(256):
            yield str(value), fw.write(symbol, [value]), None, [value], []
    elif function == "matrix_get_row":
        values = [(row * 31 + 17) & 255 for row in range(16)]
        for row in range(256):
            yield str(row), fw.write("_matrix", values), row, [values[row] if row < 16 else 0], []
    elif function == "readPin":
        ports = {0: 0x80, 1: 0x90, 2: 0xA0, 3: 0xB0, 4: 0xC0, 7: 0xF1}
        for value in (0, 0x55, 0xAA, 255):
            setup = [memory("sfr", address, [value]) for address in ports.values()]
            for pin in range(256):
                port, mask = pin >> 3, 1 << (pin & 7)
                expected = 255 if port not in ports else int(bool(value & (mask << 4 if port == 7 else mask)))
                yield f"{value}-{pin}", setup, pin, [expected], []
    elif function == "ak820_flash_read":
        for offset in range(256):
            value = (offset * 29 + 7) & 255
            yield str(offset), [memory("rom", 0xC700 + offset, [value])], 0xC700 + offset, [value], []
    elif function == "eeprom_read_byte":
        for offset in list(range(256)) + [0x27FF, 0x2800, 0x8000, 0xFFFF]:
            value = (offset * 29 + 7) & 255
            setup = fw.write("_page_valid", [0])
            if offset < 0x2800:
                setup += [memory("rom", 0xC700 + offset, [value])]
            yield str(offset), setup, offset, [value if offset < 0x2800 else 0], []
        for offset in range(64):
            value = (offset * 19 + 3) & 255
            setup = (fw.write("_page_valid", [1]) + fw.write("_cached_page", [4, 0]) +
                     [memory("xram", fw.address("_page_data") + offset, [value])])
            yield f"cached-{offset}", setup, 256 + offset, [value], []
    elif function == "eeprom_update_byte":
        for value in range(256):
            offset, old = value & 63, value ^ (0 if value & 1 else 0xA5)
            setup = (fw.write("_storage_failed", [0]) + fw.write("_page_valid", [1]) + fw.write("_page_dirty", [0]) +
                     fw.write("_cached_page", [0, 0]) + fw.write("_batch_depth", [1]) +
                     fw.write("_eeprom_update_byte_PARM_2", [value]) +
                     [memory("xram", fw.address("_page_data") + offset, [old])])
            expected = [("xram", fw.address("_page_data") + offset, [value]),
                        ("xram", fw.address("_page_dirty"), [int(old != value)])]
            yield f"cached-{value}", setup, offset, None, expected
        for offset in (0, 63, 64, 0x27FF):
            setup = (fw.write("_storage_failed", [0]) + fw.write("_page_valid", [0]) + fw.write("_page_dirty", [0]) +
                     fw.write("_batch_depth", [1]) + fw.write("_eeprom_update_byte_PARM_2", [0xA5]) +
                     [memory("rom", 0xC700 + offset, [0])])
            yield f"load-{offset}", setup, offset, None, [("xram", fw.address("_page_data") + offset % 64, [0xA5])]
        # Rejected range, previous fault, and flush failure paths. The fake
        # ROM_CTRL lacks ready bit 6, so the last case returns before IAP.
        for name, offset, failed, batch in (("range", 0xFFFF, 0, 1), ("fault", 0, 1, 1), ("flush", 0, 0, 0)):
            setup = (fw.write("_storage_failed", [failed]) + fw.write("_page_valid", [0]) + fw.write("_page_dirty", [0]) +
                     fw.write("_batch_depth", [batch]) + fw.write("_eeprom_update_byte_PARM_2", [0xA5]) +
                     [memory("rom", 0xC700, [0]), memory("sfr", 0x86, [0])])
            yield name, setup, offset, None, [("xram", fw.address("_storage_failed"), [1])]
    elif function == "mDelaymS":
        for delay in (0, 1, 2, 3, 16):
            yield str(delay), [], delay, None, []
    else:
        raise ValueError(function)


def run_function(fw: Firmware, function: str) -> dict:
    # initialize() stops at main with the CRT return address still on stack.
    # Compare each call with that actual entry state, not the linker SP seed.
    commands = fw.initialize() + fw.dump("entry-sp", "sfr", 0x81, 1)
    cases = list(function_cases(fw, function))
    for index, (_, setup, argument, returned, extra) in enumerate(cases):
        sentinel = [(index * 43 + r * 29 + 17) & 255 for r in range(8)]
        commands += setup + [memory("sfr", 0xD0, [0]), memory("iram", 0, sentinel)]
        commands += fw.call("_" + function, argument)
        label = f"case-{index:04d}-end"
        commands += fw.dump(label + "-regs", "iram", 0, 8)
        commands += fw.dump(label + "-sp", "sfr", 0x81, 1)
        if returned is not None:
            commands += fw.dump(label + "-dptr", "sfr", 0x82, min(len(returned), 2))
            if len(returned) == 4:
                commands += fw.dump(label + "-b", "sfr", 0xF0, 1) + fw.dump(label + "-a", "sfr", 0xE0, 1)
        for number, (space, address, expected) in enumerate(extra):
            commands += fw.dump(label + f"-extra-{number}", space, address, len(expected))
    log, stack = fw.execute("callee-" + function, commands)
    failures = []
    for index, (name, _, _, returned, extra) in enumerate(cases):
        label = f"case-{index:04d}-end"
        sentinel = [(index * 43 + r * 29 + 17) & 255 for r in range(8)]
        observed = {"regs": snapshot(log, label + "-regs", 0, 8), "sp": snapshot(log, label + "-sp", 0x81, 1)}
        expected = {"regs": sentinel, "sp": snapshot(log, "entry-sp", 0x81, 1)}
        if returned is not None:
            observed["return"] = snapshot(log, label + "-dptr", 0x82, min(len(returned), 2))
            if len(returned) == 4:
                observed["return"] += snapshot(log, label + "-b", 0xF0, 1) + snapshot(log, label + "-a", 0xE0, 1)
            expected["return"] = returned
        for number, (_, address, values) in enumerate(extra):
            observed[f"extra-{number}"] = snapshot(log, label + f"-extra-{number}", address, len(values))
            expected[f"extra-{number}"] = values
        if observed != expected:
            failures.append({"case": name, "observed": observed, "expected": expected})
    return {"function": function, "pass": not failures, "cases": len(cases), "failed_cases": len(failures),
            "first_failures": failures[:3], **stack}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    fw = Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xC700:
        raise ValueError("The simulator NVM fixture requires a bounded image below 0xC700")
    listings = {}
    for name, path in FUNCTIONS.items():
        data = (fw.build / "dce" / path).read_bytes()
        if not re.search(rb"^_" + name.encode() + rb":", data, re.M):
            raise ValueError("Selected C function is missing from its expected object: " + name)
        listings[path] = hashlib.sha256(data).hexdigest()
    results = [run_function(fw, name) for name in FUNCTIONS]
    report = {"pass": all(item["pass"] for item in results), "tests": results,
              "linked_image_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "selected_callee_saves": list(FUNCTIONS), "checked_registers": [f"R{i}" for i in range(8)],
              "register_bank": 0, "linked_listings_sha256": listings,
              "test_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in (Path(__file__).resolve(), ROOT / "tests/ak820_emitted/run.py")},
              "limits": "CPU ABI, returns, bounds and simulated memory branches only. Not an exhaustive firmware stack bound or physical IRQ/timing/IAP/USB proof."}
    (fw.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
