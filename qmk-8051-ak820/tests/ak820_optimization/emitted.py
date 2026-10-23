#!/usr/bin/env python3
"""Exhaust the linked native MUL helper and verify its register-preserving ABI.

Only generic uCsim C52 CPU state is exercised. Test scratch ROM/XRAM exists in the
simulator alone. No physical device is opened and no flash operation is issued.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("ak820_emitted_support", HERE.parent / "ak820_emitted/run.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
Firmware, memory = _module.Firmware, _module.memory


def trampoline(x: int, function: int, parameter: int) -> list[int]:
    # Counter 0x2f00 and table 0x3000 are simulator scratch, outside firmware RAM.
    # Every call gets sentinel R0..R7. Failure writes 255, which cannot equal the
    # high byte of any unsigned 8x8 product (maximum 254).
    code = [0x90,0x2f,0x00,0xe4,0xf0]  # MOV DPTR,#counter; CLR A; MOVX @DPTR,A
    loop = len(code)
    code += [0x90,0x2f,0x00,0xe0,0x90,parameter >> 8,parameter & 255,0xf0,0x75,0x82,x]
    for register in range(8):
        code += [0x78 + register, 0x11 * (register + 1)]  # MOV Rn,#sentinel
    code += [0x12,function >> 8,function & 255]
    branches = []
    for register in range(8):
        code += [0xb8 + register,0x11 * (register + 1),0]  # CJNE Rn,#sentinel,fail
        branches.append(len(code) - 1)
    code += [0xe5,0x82,0x80,2]  # MOV A,DPL; SJMP store
    fail = len(code)
    code += [0x74,255]  # MOV A,#invalid-product
    for branch in branches:
        code[branch] = fail - (branch + 1)
    code += [0xf5,0xf0,0x90,0x2f,0x00,0xe0,0xf5,0x82,0x75,0x83,0x30,0xe5,0xf0,0xf0]
    # MOV B,A; read counter; DPTR=0x3000+counter; MOV A,B; MOVX @DPTR,A
    code += [0x90,0x2f,0x00,0xe0,0x04,0xf0,0x70,0]  # INC counter; JNZ loop
    relative = loop - len(code)
    assert -128 <= relative < 128
    code[-1] = relative & 255
    code += [0x02,0x27,0x00]
    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    build = args.build_dir.resolve()
    output = (args.output_dir or build / "optimization-emitted").resolve()
    firmware = Firmware(build, args.s51.resolve(), output)
    helper, parameter = firmware.address("_mulhi8"), firmware.address("_mulhi8_PARM_2")
    # Check the linked image itself, rather than trusting assembly text only.
    expected_code = bytes([0x85,0x82,0xf0,0x90,parameter >> 8,parameter & 255,0xe0,0xa4,0x85,0xf0,0x82,0x22])
    actual_code = bytes(firmware.code[helper + index] for index in range(len(expected_code)))
    if actual_code != expected_code:
        raise AssertionError(f"Native helper instructions changed: {actual_code.hex()} != {expected_code.hex()}")
    commands = [f"run {firmware.address('__sdcc_gsinit_startup'):#x} {firmware.address('_main'):#x}"]
    for x in range(256):
        commands += [memory("rom", 0x2000, trampoline(x, helper, parameter)), "run 0x2000 0x2700"]
        commands += firmware.dump(f"mul_{x:03d}_end", "xram", 0x3000, 256)
    log, stack = firmware.execute("mul-all-operands-registers", commands)
    for x in range(256):
        actual = firmware.extract(log, f"mul_{x:03d}_end", 0x3000, 256)
        expected = [x * y >> 8 for y in range(256)]
        if actual != expected:
            bad = next(y for y in range(256) if actual[y] != expected[y])
            raise AssertionError(f"MUL or R0..R7 preservation failed at {x} * {bad}: {actual[bad]} != {expected[bad]}")
    report = {"pass": True, "cpu": "uCsim C52", "linked_image_sha256": hashlib.sha256(firmware.image.read_bytes()).hexdigest(),
              "tests": [{"name": "native_mul_all_operands_and_register_preservation", "pass": True, "cases": 65536,
                         "preserved_registers": [f"R{i}" for i in range(8)], "helper_address": helper, "linked_helper_bytes": actual_code.hex(), **stack}],
              "limits": "CPU/ABI proof only; the complete RGB path is checked separately by ak820_emitted. No physical timing, DMA, USB or IAP validation."}
    (output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
