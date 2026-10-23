#!/usr/bin/env python3
"""Bound the linked IRQ callbacks and exercise real OEM wrappers in uCsim.

The C52 CPU does not implement VS11K28A interrupt routing or peripherals.
Calls below supply the two-byte hardware return frame with LCALL, then run
the unchanged OEM prologue/epilogue and linked application callback. USB
ACK side effects and a nested higher-priority IRQ are supplied explicitly.
This proves neither electrical IRQ timing nor whole-program stack bounds.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'util'))
import pack_ak820 as packer

spec = importlib.util.spec_from_file_location('irq_iap_support', HERE.parent / 'ak820_iap/run.py')
iap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iap)
emitted = iap.emitted

IRQ = {'timer': (1, '_ak820_timer_irq'), 'usb': (7, '_USB_DeviceInterrupt'),
       'led': (10, '_ak820_led_irq')}
ROW = re.compile(r'^\s*([0-9A-F]{6})\s+((?:[0-9A-F]{2}\s+)+)\[\s*\d+\]\s+\d+\s+(.+)$')


def linked_instructions(fw):
    """Read relocated instructions, comparing every listed byte to the IHX."""
    result = {}
    for filename in ('ak820_timer.rst', 'ak820_board.rst', 'protocol/ch555/usb_ak820.rst'):
        for row in (fw.build / 'dce' / filename).read_text().splitlines():
            found = ROW.match(row)
            if not found:
                continue
            address, raw, assembly = int(found[1], 16), bytes.fromhex(found[2]), found[3]
            assert raw == bytes(fw.code.get(address + i, -1) for i in range(len(raw))), (filename, address)
            assembly = assembly.split(';', 1)[0].strip().lower()
            result[address] = (raw, assembly)
    return result


def callback_bound(instructions, entry):
    """Explore every direct branch, balanced PUSH/POP and call in an IRQ.

    Two known indirect tables are checked structurally: SDCC's consecutive
    SJMP dispatch and the LED selector's sixteen CLR bit / RET entries. The
    bound assumes execution enters a valid table entry, as the source index
    checks require. Unsupported SP writes, dispatch or recursion fail closed.
    """
    memo, active = {}, set()

    def bound(start):
        if start in memo:
            return memo[start]
        assert start not in active, f'Recursive IRQ call at {start:#x}'
        active.add(start)
        work, seen, heights, maximum, returns = [(start, 0)], set(), {}, 0, 0
        while work:
            pc, height = work.pop()
            if (pc, height) in seen:
                continue
            assert height >= 0, f'Stack underflow at {pc:#x}'
            assert pc not in heights or heights[pc] == height, f'Unbalanced stack loop at {pc:#x}'
            heights[pc] = height
            seen.add((pc, height))
            assert pc in instructions, f'IRQ escaped checked instructions at {pc:#x}'
            raw, assembly = instructions[pc]
            opcode, following = raw[0], pc + len(raw)
            mnemonic = assembly.split()[0]
            operands = assembly[len(mnemonic):].strip()
            first = operands.split(',', 1)[0].strip()
            assert not (first in ('sp', '_sp', '0x81') and mnemonic in
                        ('mov', 'inc', 'dec', 'add', 'anl', 'orl', 'xrl', 'pop')), assembly
            maximum = max(maximum, height)
            if opcode in (0x22, 0x32):
                assert opcode == 0x22 and height == 0, f'Unbalanced/non-RET callback at {pc:#x}'
                returns += 1
                continue
            if opcode == 0xC0:  # PUSH direct
                height += 1
                maximum = max(maximum, height)
            elif opcode == 0xD0:  # POP direct
                height -= 1
            elif opcode == 0x12 or opcode & 0x1F == 0x11:  # LCALL / ACALL
                target = int.from_bytes(raw[1:3], 'big') if opcode == 0x12 else \
                    (following & 0xF800) | ((opcode & 0xE0) << 3) | raw[1]
                maximum = max(maximum, height + 2 + bound(target))
            elif opcode == 0x02 or opcode & 0x1F == 0x01:  # LJMP / AJMP
                target = int.from_bytes(raw[1:3], 'big') if opcode == 0x02 else \
                    (following & 0xF800) | ((opcode & 0xE0) << 3) | raw[1]
                work.append((target, height))
                continue
            elif opcode == 0x73:  # JMP @A+DPTR: checked adjacent dispatch table.
                targets, at = [], following
                while at in instructions and instructions[at][0][0] == 0x80:
                    targets.append(at)
                    at += 2
                if not targets:
                    for i in range(16):
                        at = following + i * 3
                        assert instructions.get(at, (b'',))[0][:1] == b'\xc2', f'Unknown indirect IRQ dispatch {pc:#x}'
                        assert instructions.get(at + 2, (b'',))[0] == b'\x22'
                        targets.append(at)
                work.extend((target, height) for target in targets)
                continue
            elif opcode in (0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0xD5) or \
                    0xB4 <= opcode <= 0xBF or 0xD8 <= opcode <= 0xDF:
                delta = raw[-1] if raw[-1] < 128 else raw[-1] - 256
                work.append((following + delta, height))
                if opcode == 0x80:
                    continue
            work.append((following, height))
        assert returns, f'IRQ callback has no balanced return at {start:#x}'
        active.remove(start)
        memo[start] = maximum
        return maximum

    return bound(entry)


def wrapper_bytes(stock, ordinal):
    address = 0x1858 + ordinal * 76
    raw = stock[address:address + 76]
    prefix = bytes.fromhex('c0e0c0f0c083c082c0d075d000') + b''.join(bytes((0xC0, r)) for r in range(8))
    suffix = b''.join(bytes((0xD0, r)) for r in reversed(range(8))) + bytes.fromhex('d0d0d082d083d0f0d0e032')
    assert raw[:29] == prefix and raw[49:] == suffix
    assert raw[29:35] == bytes.fromhex('7b007a30') + bytes((0x79, ordinal * 3))
    assert raw[46:49] == bytes.fromhex('120dc4')
    assert stock[0x0DC4:0x0DCA] == bytes.fromhex('8a838982e473')
    return address, raw


def cpu_case(fw, stock, name, reserve, nested=None):
    console = iap.Console(fw.simulator, fw.image)
    try:
        console.command(fw.initialize())
        console.command(emitted.memory('rom', 0x0DC4, stock[0x0DC4:0x0DCA]))
        for ordinal, symbol in IRQ.values():
            address, raw = wrapper_bytes(stock, ordinal)
            console.command([emitted.memory('rom', address, raw),
                             emitted.memory('rom', 0x3000 + ordinal * 3, packer.ljmp(fw.address(symbol)))])
        # CRT and support initialization are complete. Reserve a representative
        # main stack frame without claiming that it is the global worst case.
        stack_start = fw.initial_sp + reserve
        assert stack_start < 0xE0
        registers = bytes((0x30 + i) & 255 for i in range(32))
        console.command([emitted.memory('iram', 0, registers),
                         f'fill iram {fw.initial_sp + 1:#x} {stack_start:#x} 0xa7',
                         emitted.memory('sfr', 0x81, [stack_start, 0x34, 0x12]),
                         emitted.memory('sfr', 0xA8, [0]),
                         emitted.memory('sfr', 0xD0, [0xD0]),
                         emitted.memory('sfr', 0xE0, [0xA5]),
                         emitted.memory('sfr', 0xF0, [0x5A]),
                         emitted.memory('sfr', 0xA6, [0x1E])])
        if name == 'usb':
            # SET_CONFIGURATION reaches the largest static USB call depth.
            console.command([emitted.memory('xram', 0x1000, [0, 9, 1, 0, 0, 0, 0, 0]),
                             emitted.memory('xram', 0x220F, [0x38]),
                             emitted.memory('xram', 0x223D, [0x20]),
                             'break xram w 0x220f'])
        ordinal, _ = IRQ[name]
        wrapper, _ = wrapper_bytes(stock, ordinal)
        console.command(emitted.memory('rom', 0x2600, [0x12, wrapper >> 8, wrapper & 255, 0x02, 0x27, 0]))
        console.command('break 0x2700')
        if nested:
            # A synthetic higher-priority interrupt is injected exactly when
            # the USB callback enters endpoints_reset with its maximum frame.
            stop = fw.address('_endpoints_reset')
            console.command(f'run 0x2600 {stop:#x}')
            before_sp = console.read('sfr', 0x81, 1)[0]
            before_registers = console.read('iram', 0, 32)
            before_sfr = {address: console.read('sfr', address, 1) for address in (0x82, 0x83, 0xD0, 0xE0, 0xF0)}
            inner, _ = wrapper_bytes(stock, IRQ[nested][0])
            console.command(emitted.memory('rom', 0x2610, [0x12, inner >> 8, inner & 255,
                                                          0x02, stop >> 8, stop & 255]))
            console.command(f'run 0x2610 {stop:#x}')
            assert console.read('sfr', 0x81, 1) == [before_sp]
            assert console.read('iram', 0, 32) == before_registers
            assert all(console.read('sfr', address, 1) == value for address, value in before_sfr.items())
            result = console.command('run')
        else:
            result = console.command('run 0x2600 0x2700')
        if name == 'usb':
            assert "Event `write' at xram[0x220f]" in result, result
            # Explicitly model the documented ACK_TRANSFER side effect.
            console.command(emitted.memory('xram', 0x223D, [0]))
            result = console.command('run')
        assert '0x2700' in result, result
        assert console.read('sfr', 0x81, 1) == [stack_start]
        assert console.read('iram', 0, 32) == list(registers)
        assert console.read('iram', fw.initial_sp + 1, reserve) == [0xA7] * reserve
        assert console.read('sfr', 0x82, 2) == [0x34, 0x12]
        assert console.read('sfr', 0xD0, 1) == [0xD0]
        assert console.read('sfr', 0xE0, 1) == [0xA5]
        assert console.read('sfr', 0xF0, 1) == [0x5A]
        state = console.command('state')
        peak = int(re.findall(r'Most value of stack pointer=\s+0x([0-9a-f]+)', state)[-1], 16)
        return {'irq': name, 'nested_irq': nested, 'reserved_main_bytes': reserve,
                'peak_sp': peak, 'irq_stack_bytes': peak - stack_start,
                'canary_and_registers_preserved': True}
    finally:
        (fw.output / f'{name}-{nested or "single"}.log').write_text(console.log)
        console.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--stock-rom', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--main-sample-bytes', type=int, default=56,
                        help='Representative main stack reservation, not a whole-program bound')
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    stock = args.stock_rom.read_bytes()
    assert len(stock) == 65536 and packer.digest(stock) == packer.STOCK_SHA
    instructions = linked_instructions(fw)
    bounds = {name: 17 + callback_bound(instructions, fw.address(symbol))
              for name, (_, symbol) in IRQ.items()}
    pair = sum(sorted(bounds.values())[-2:])
    if not 0 < args.main_sample_bytes or args.main_sample_bytes + pair > fw.stack_capacity:
        raise ValueError('Representative main frame plus nested IRQ exceeds the linked stack capacity')
    for ordinal, _ in IRQ.values():
        wrapper_bytes(stock, ordinal)
    cases = [cpu_case(fw, stock, name, args.main_sample_bytes) for name in IRQ]
    cases += [cpu_case(fw, stock, 'usb', args.main_sample_bytes, nested=name) for name in ('timer', 'led')]
    for case in cases:
        expected = bounds[case['irq']] + (bounds[case['nested_irq']] if case['nested_irq'] else 0)
        assert case['irq_stack_bytes'] <= expected, (case, bounds)
    result = {'pass': True, 'scope': 'linked CPU instructions and explicit peripheral/interrupt model',
              'linked_image_sha256': packer.digest(fw.image.read_bytes()),
              'linked_map_sha256': packer.digest((fw.build / 'ajazz_ak820_vial.map').read_bytes()),
              'stock_rom_sha256': packer.digest(stock),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'initial_sp': fw.initial_sp, 'stack_capacity': fw.stack_capacity,
              'wrapper_bytes_on_stack': 17, 'irq_bounds': bounds,
              'two_priority_level_irq_bound': pair,
              'sample_main_plus_nested_irq_bytes': args.main_sample_bytes + pair,
              'sample_remaining_bytes': fw.stack_capacity - args.main_sample_bytes - pair,
              'cpu_cases': cases,
              'limits': ['Main stack reservation is an observed-scenario example, not a whole-program bound.',
                         'Indirect dispatch bounds assume valid DPTR/index values selecting a checked table entry.',
                         'Two nested priority levels follow the CH555 header contract; VS11 silicon IRQ routing is not modeled.',
                         'Boot entry does not normalize IP/IP_EX; both priority orderings remain possible.',
                         'USB ACK side effect and nested hardware return frames are supplied by the fixture.',
                         'No physical USB, flash, LED DMA, interrupt timing or whole-program reentrancy proof.']}
    (fw.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
