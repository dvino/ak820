#!/usr/bin/env python3
"""Execute linked startup bytes offline; never opens HID or programs a device.

The small instruction model deliberately offers two short-MOVX interpretations
to expose the generic CRT's unverified P2 assumption. Neither interpretation is
asserted to be the VS11 silicon. Optional uCsim executes the complete emitted
CRT on a generic C52 CPU, without pretending to model AK820 peripherals.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'util'))
import pack_ak820 as packer


class CopyCPU:
    """Only instructions reached in the linked XINIT and marker-check slices."""
    def __init__(self, rom, pc, short_mode='forbidden'):
        self.rom = rom
        self.pc = pc
        self.reg = [0] * 8
        self.sfr = {0x82: 0, 0x83: 0, 0xa0: 0xa7}
        self.a = 0
        self.xram = bytearray([0xa5]) * 65536
        self.writes = []
        self.short_mode = short_mode
        self.short_writes = 0
        self.steps = 0

    @property
    def dptr(self):
        return self.sfr[0x82] | self.sfr[0x83] << 8

    @dptr.setter
    def dptr(self, value):
        self.sfr[0x82], self.sfr[0x83] = value & 255, (value >> 8) & 255

    def byte(self):
        value = self.rom[self.pc]
        self.pc = (self.pc + 1) & 0xffff
        return value

    def branch(self, condition):
        offset = self.byte()
        if condition:
            self.pc = (self.pc + (offset if offset < 128 else offset - 256)) & 0xffff

    def write(self, address):
        self.xram[address] = self.a
        self.writes.append((address, self.a))

    def run(self, stops):
        while self.pc not in stops:
            if self.steps > 100000:
                raise AssertionError('Startup slice instruction bound exceeded')
            self.steps += 1
            at, op = self.pc, self.byte()
            if 0x78 <= op <= 0x7f:
                self.reg[op - 0x78] = self.byte()
            elif 0xe8 <= op <= 0xef:
                self.a = self.reg[op - 0xe8]
            elif 0xf8 <= op <= 0xff:
                self.reg[op - 0xf8] = self.a
            elif 0x88 <= op <= 0x8f:
                self.sfr[self.byte()] = self.reg[op - 0x88]
            elif 0xa8 <= op <= 0xaf:
                self.reg[op - 0xa8] = self.sfr[self.byte()]
            elif 0x08 <= op <= 0x0f:
                self.reg[op - 8] = (self.reg[op - 8] + 1) & 255
            elif 0xd8 <= op <= 0xdf:
                index = op - 0xd8
                self.reg[index] = (self.reg[index] - 1) & 255
                self.branch(self.reg[index] != 0)
            elif 0xb8 <= op <= 0xbf:
                value = self.byte()
                self.branch(self.reg[op - 0xb8] != value)
            elif op == 0x75:
                address, value = self.byte(), self.byte()
                self.sfr[address] = value
            elif op == 0x05:
                index = self.byte()
                self.sfr[index] = (self.sfr[index] + 1) & 255
            elif op == 0x53:
                address, value = self.byte(), self.byte()
                self.sfr[address] = self.sfr.get(address, 0) & value
            elif op == 0xf5:
                self.sfr[self.byte()] = self.a
            elif op == 0x90:
                self.dptr = self.byte() << 8 | self.byte()
            elif op == 0xe4:
                self.a = 0
            elif op == 0x44:
                self.a |= self.byte()
            elif op == 0x93:
                self.a = self.rom[(self.dptr + self.a) & 0xffff]
            elif op == 0xa3:
                self.dptr = self.dptr + 1
            elif op == 0xf0:
                self.write(self.dptr)
            elif op == 0xf2:
                if self.short_mode == 'forbidden':
                    raise ValueError('Executed unverified short MOVX in startup')
                self.short_writes += 1
                address = self.reg[0]
                if self.short_mode == 'classic_p2':
                    address |= self.sfr[0xa0] << 8
                self.write(address)
            elif op in (0x60, 0x70, 0x80):
                self.branch(op == 0x80 or (self.a == 0 if op == 0x60 else self.a != 0))
            elif op == 0x02:
                self.pc = self.byte() << 8 | self.byte()
            else:
                raise AssertionError(f'Unsupported slice instruction {op:02x} at {at:04x}')
        return self


def image_prefix(build):
    return build / ('application' if (build / 'application.ihx').exists() else 'ajazz_ak820_vial')


def load(build):
    prefix = image_prefix(build)
    data = packer.read_ihex(prefix.with_suffix('.ihx'))
    symbols = packer.read_symbols(prefix.with_suffix('.map'))
    rom = bytearray(65536)
    for address, value in data.items():
        rom[address] = value
    return data, symbols, rom


def copy_slice(rom, symbols, mode):
    return CopyCPU(rom, symbols['s_GSINIT3'], mode).run({symbols['s_GSINIT3'] + symbols['l_GSINIT3']})


def assert_copy(cpu, rom, symbols):
    source, destination, count = (symbols[key] for key in ('s_XINIT', 's_XISEG', 'l_XINIT'))
    expected = bytearray([0xa5]) * 65536
    expected[destination:destination + count] = rom[source:source + count]
    assert cpu.xram == expected, 'XINIT copied wrong bytes/address or damaged unrelated XRAM'
    assert cpu.writes == list(enumerate(rom[source:source + count], destination)), 'XINIT write order/extent differs'


def check_erase_leaf(stock):
    """Decode the immutable copied routine, checking relocated branch closure."""
    blob = stock[0xe650:0xe6a7]
    lengths = {0xa2: 2, 0x92: 2, 0xc2: 2, 0xef: 1, 0x54: 2, 0xff: 1,
               0xc3: 1, 0xee: 1, 0x94: 2, 0x40: 2, 0x50: 2, 0x7c: 2, 0x80: 2,
               0x75: 3, 0xec: 1, 0x42: 2, 0x8e: 2, 0x8f: 2, 0xe4: 1,
               0xf5: 2, 0xe5: 2, 0x30: 3, 0x7d: 2, 0xfd: 1, 0xf4: 1,
               0x52: 2, 0xcf: 1, 0xed: 1, 0x22: 1}
    starts, targets, pc = set(), [], 0
    while pc < len(blob):
        starts.add(pc)
        opcode = blob[pc]
        assert opcode in lengths, f'Unexpected erase helper opcode {opcode:02x}'
        size = lengths[opcode]
        if opcode in (0x40, 0x50, 0x80, 0x30):
            offset = blob[pc + size - 1]
            targets.append(pc + size + (offset if offset < 128 else offset - 256))
        pc += size
    assert pc == len(blob) and blob[-1] == 0x22
    assert all(target in starts for target in targets), 'Erase branch leaves copied leaf/instruction boundaries'
    return len(starts)


def generic_crt(build, simulator, output, symbols, data, stock):
    spec = importlib.util.spec_from_file_location('ak820_emitted', ROOT / 'tests/ak820_emitted/run.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fw = module.Firmware(build, simulator, output)
    xseg, xlen = symbols['s_XSEG'], symbols['l_XSEG']
    xiseg, ilen = symbols['s_XISEG'], symbols['l_XISEG']
    commands = ['fill xram 0 0xffff 0xa5',
                f"run {symbols['__sdcc_gsinit_startup']:#x} {symbols['s_GSINIT']:#x}"]
    observations = [('cleared', xseg, bytes(xlen)),
                    ('initialized', xiseg, bytes(data[symbols['s_XINIT'] + i] for i in range(ilen))),
                    ('before_app', 0x3e0, bytes([0xa5]) * 32),
                    ('after_app', xiseg + ilen, bytes([0xa5]) * 32),
                    ('usb_fifo', 0x1000, bytes([0xa5]) * 32)]
    for label, address, expected in observations:
        commands += fw.dump(label, 'xram', address, len(expected))
    # GSINIT then performs ordinary C initializers (some intentionally write
    # non-zero bytes in XSEG). Verify it reaches main with XINIT preserved.
    commands += [f"run {symbols['s_GSINIT']:#x} {symbols['_main']:#x}"]
    commands += fw.dump('at_main_initialized', 'xram', xiseg, ilen)
    log, result = fw.execute('full-crt', commands)
    for label, address, expected in observations:
        assert fw.extract(log, label, address, len(expected)) == list(expected), label
    assert fw.extract(log, 'at_main_initialized', xiseg, ilen) == list(observations[1][2])
    # Stop BEFORE the actual native erase operation. Only emulator RAM/SFRs
    # are changed; this verifies the caller's ABI with hostile inherited state.
    payload = packer.pack(data, symbols, stock, bytes(packer.empty_nvm()), True)
    commands = [module.memory('rom', packer.APP_START, payload[:packer.LOW_START - packer.APP_START]),
                module.memory('sfr', 0xa8, [0xff]), module.memory('sfr', 0xe8, [0xff]),
                module.memory('sfr', 0xd0, [0x18]), module.memory('sfr', 0x81, [0xf0]),
                module.memory('sfr', 0xa2, [0x0d]),
                f'run {packer.APP_START:#x} {packer.ERASE_START:#x}']
    for label, address in [('ie', 0xa8), ('ie_ex', 0xe8), ('psw', 0xd0), ('sp', 0x81), ('xbus', 0xa2)]:
        commands += fw.dump(label, 'sfr', address, 1)
    commands += fw.dump('erase_args', 'iram', 6, 2)
    entry_log, _ = fw.execute('entry-before-erase', commands)
    for label, address, expected in [('ie', 0xa8, 0), ('ie_ex', 0xe8, 0), ('psw', 0xd0, 0),
                                     ('sp', 0x81, 0x22), ('xbus', 0xa2, 8)]:
        section = entry_log.split('\n@@' + label + '\n', 1)[1]
        found = re.search(r'^0x' + f'{address:02x}' + r'\s+(?:\w+:\s+0b[01]+\s+0x([0-9a-f]{2})|([0-9a-f]{2}))', section, re.M)
        assert found and int(found[1] or found[2], 16) == expected, label
    assert fw.extract(entry_log, 'erase_args', 6, 2) == [0x27, 0xc0]
    result['scope'] = 'Generic C52 CRT and pre-erase ABI only; no VS11 peripherals or flash operation'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', required=True, type=Path)
    parser.add_argument('--legacy-build', required=True, type=Path)
    parser.add_argument('--stock-rom', required=True, type=Path)
    parser.add_argument('--simulator', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data, symbols, rom = load(args.build)
    stock = args.stock_rom.read_bytes()
    assert packer.digest(stock) == packer.STOCK_SHA
    packer.validate_startup(data, symbols)
    cpu = copy_slice(rom, symbols, 'forbidden')
    assert_copy(cpu, rom, symbols)
    assert cpu.sfr[0xa0] == 0xa7 and cpu.short_writes == 0
    # Exercise the emitted loop's boundary cases by changing only relocation
    # operands in simulated ROM. The independent oracle is a flat byte copy.
    synthetic = []
    for count in (0, 1, 255, 256, 257, 512, 538, 2048):
        fake, table = bytearray(rom), dict(symbols)
        source, destination, entry = 0xc000, 0x04f3, symbols['s_GSINIT3']
        for offset, value in ((1, count & 255), (4, count >> 8), (8, (count + 255) >> 8),
                              (10, source & 255), (12, source >> 8),
                              (14, destination & 255), (16, destination >> 8)):
            fake[entry + offset] = value
        fake[source:source + count] = bytes((i * 37 + 19) & 255 for i in range(count))
        table.update({'s_XINIT': source, 's_XISEG': destination, 'l_XINIT': count})
        model = copy_slice(fake, table, 'forbidden')
        assert_copy(model, fake, table)
        synthetic.append({'length': count, 'writes': len(model.writes), 'steps': model.steps})
    old_data, old_symbols, old_rom = load(args.legacy_build)
    old = copy_slice(old_rom, old_symbols, 'classic_p2')
    assert_copy(old, old_rom, old_symbols)
    low = copy_slice(old_rom, old_symbols, 'low256')
    assert low.xram != old.xram and low.short_writes == old_symbols['l_XINIT']
    for bad_data, bad_symbols in [(old_data, old_symbols), (dict(data), dict(symbols))]:
        if bad_symbols is not old_symbols:
            bad_data[symbols['s_GSINIT3'] + 6] ^= 1
        try:
            packer.validate_startup(bad_data, bad_symbols)
        except ValueError:
            pass
        else:
            raise AssertionError('Packer accepted legacy or mutated startup')
    payload = packer.pack(data, symbols, stock, bytes(packer.empty_nvm()), True)
    packed_rom = bytearray(stock)
    packed_rom[packer.APP_START:packer.APP_END] = payload
    # A permanent package skips the trial erase leaf on every entry. Exercise
    # two independent reset entries, preserving the OEM marker bytes, and
    # stop before CRT/main. This does not model OEM loader dispatch itself.
    permanent = packer.pack(data, symbols, stock, bytes(packer.empty_nvm()), False)
    permanent_rom = bytearray(stock)
    permanent_rom[packer.APP_START:packer.APP_END] = permanent
    marker_before = bytes(permanent_rom[0x27c0:0x2800])
    permanent_boots = []
    for boot in range(2):
        entry = CopyCPU(permanent_rom, packer.APP_START)
        entry.sfr.update({0xa8: 0xff, 0xe8: 0xff, 0xd0: 0x18, 0x81: 0xf0, 0xa2: 0x0d})
        entry.run({packer.CODE_START})
        assert not entry.writes and bytes(entry.rom[0x27c0:0x2800]) == marker_before
        assert entry.sfr[0xa8] == entry.sfr[0xe8] == entry.sfr[0xd0] == 0
        assert entry.sfr[0x81] == 0x20 and entry.sfr[0xa2] == 8
        permanent_boots.append({'boot': boot + 1, 'reached_code_start': True,
                                'trial_erase_not_called': True, 'marker_preserved': True})
    passed, failed = packer.CODE_START, packer.MARKER_CHECK_START + 15
    for bad in range(-1, 64):
        image = bytearray(packed_rom)
        image[0x27c0:0x2800] = bytes(64)
        if bad >= 0:
            image[0x27c0 + bad] = 1
        check = CopyCPU(image, packer.MARKER_CHECK_START).run({passed, failed})
        assert check.pc == (passed if bad < 0 else failed) and not check.writes
    prefix, legacy_prefix = image_prefix(args.build), image_prefix(args.legacy_build)
    inputs = {'ihx': prefix.with_suffix('.ihx'), 'map': prefix.with_suffix('.map'),
              'legacy_ihx': legacy_prefix.with_suffix('.ihx'),
              'legacy_map': legacy_prefix.with_suffix('.map'), 'stock_rom': args.stock_rom,
              'packer': Path(packer.__file__), 'runner': Path(__file__)}
    report = {'status': 'PASS', 'hardware_validated': False, 'usb_opened': False,
              'ihx_sha256': packer.digest(inputs['ihx'].read_bytes()),
              'inputs': {name: {'name': path.name, 'sha256': packer.digest(path.read_bytes())}
                         for name, path in inputs.items()},
              'actual_xinit_bytes': len(cpu.writes), 'xinit_start': symbols['s_XISEG'],
              'synthetic_lengths': synthetic, 'marker_cases': 65,
              'permanent_two_entry_control': permanent_boots,
              'native_erase_leaf_instructions': check_erase_leaf(stock),
              'legacy_classic_p2_model': 'PASS', 'legacy_low256_model': 'CORRUPTS_XRAM',
              'legacy_or_mutated_startup_pack_rejected': True,
              'limits': ['Alternative short-MOVX interpretations are model assumptions, not measurements of VS11.',
                         'This removes an unverified startup dependency; it does not prove the unique cause of rc3 hardware failure.',
                         'No flash erase/program, interrupt timing, USB hardware or physical matrix is simulated.']}
    if args.simulator:
        report['ucsim'] = generic_crt(args.build, args.simulator, args.output, symbols, data, stock)
    (args.output / 'startup-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
