#!/usr/bin/env python3
"""Check the exact pre-main control stack and the CRT's live main call frame."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ANALYZER = Path(__file__).parents[1] / 'ak820_stack/analyze.py'
spec = importlib.util.spec_from_file_location('startup_stack_analyzer', ANALYZER)
stack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stack)


def check(instructions, symbols, code, initial_sp):
    crt, main, program = (symbols[name] for name in
                          ('__sdcc_gsinit_startup', '_main', '__sdcc_program_startup'))
    if bytes(code.get(crt + i, 0xFF) for i in range(3)) != bytes((0x75, 0x81, initial_sp)):
        raise ValueError('CRT must set the linked stack pointer before any call')
    expected = bytes((0x12, main >> 8, main & 255, 0x80, 0xFE))
    if bytes(code.get(program + i, 0xFF) for i in range(5)) != expected:
        raise ValueError('Expected one persistent CRT LCALL frame at main entry')
    # Main is a proof cutpoint, not an assumed leaf of the whole program. Its
    # original body is analyzed separately. Replacing only its entry with RET
    # computes startup's frame usage up to that boundary, including the LCALL.
    boundary = dict(instructions)
    boundary[main] = b'\x22'
    cut_code = dict(code)
    cut_code[main] = 0x22
    analyzer = stack.Analyzer(boundary, cut_code)
    result = analyzer.bound(crt + 3)
    if result['bound'] is None:
        raise ValueError('Unresolved pre-main stack paths: ' + str(result['unresolved']))
    for pc in result['reachable']:
        if pc == main:
            continue
        raw = analyzer.instruction(pc)
        op = raw[0]
        following = pc + len(raw)
        direct_target = None
        if op in (0x02, 0x12):
            direct_target = int.from_bytes(raw[1:], 'big')
        elif (op & 0x1F) in (0x01, 0x11):
            direct_target = (following & 0xF800) | ((op & 0xE0) << 3) | raw[1]
        elif op in (0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0xD5) or 0xB4 <= op <= 0xBF or 0xD8 <= op <= 0xDF:
            direct_target = following + (raw[-1] if raw[-1] < 128 else raw[-1] - 256)
        if op == 0x73 or analyzer.pointer_transfers:
            raise ValueError('Indirect startup transfer needs a separate main-entry proof')
        if direct_target == main and pc != program:
            raise ValueError('Alternate main entry bypasses the checked CRT frame')
        if following == main and op not in (0x02, 0x22, 0x32, 0x80) and (op & 0x1F) != 0x01:
            raise ValueError('Fallthrough main entry bypasses the checked CRT frame')
        destination = raw[2] if op == 0x85 else raw[1] if len(raw) > 1 and (
            op in (0x05, 0x15, 0x42, 0x43, 0x52, 0x53, 0x62, 0x63,
                   0x75, 0x86, 0x87, 0xC5, 0xD0, 0xD5, 0xF5)
            or 0x88 <= op <= 0x8F) else None
        bit_destination = raw[1] if op in (0x10, 0x92, 0xB2, 0xC2, 0xD2) else None
        if destination in (0xA8, 0xE8) or (
                bit_destination is not None and (bit_destination & 0xF8) in (0xA8, 0xE8)):
            raise ValueError('CRT modifies interrupt enables before main')
    if main not in result['reachable'] or program not in result['reachable']:
        raise ValueError('CRT does not reach the checked main call boundary')
    # This may conservatively include an earlier transient helper frame. It is
    # nevertheless an upper bound on every live frame at the main cutpoint,
    # including a helper that tail-transfers to the program-startup call.
    return {'pre_main_control_stack_bound': result['bound'], 'main_entry_frame_bound': result['bound'],
            'crt_initial_sp': initial_sp, 'interrupt_enables_unchanged_until_main': True,
            'reachable': result['reachable'],
            'scope': 'Pre-main control stack and main-entry frame upper bound only; main body and interrupts are separate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    instructions, symbols, code, identity = stack.load(args.build_dir)
    memory = (args.build_dir / 'ajazz_ak820_vial.mem').read_text()
    match = re.search(r'sp set to 0x([0-9a-f]+)', memory)
    if not match:
        raise ValueError('Missing linked stack placement')
    result = check(instructions, symbols, code, int(match[1], 16))
    result.update(identity=identity, checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  analyzer_sha256=hashlib.sha256(ANALYZER.read_bytes()).hexdigest(),
                  hardware_validated=False, physical_device_commands=0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('reachable', 'identity')}, indent=2))


if __name__ == '__main__':
    main()
