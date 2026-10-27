#!/usr/bin/env python3
"""Exercise every single-byte mutation of a journal header in a linked image."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--s51', required=True, type=Path)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    build = args.build_dir.resolve()
    spec = importlib.util.spec_from_file_location('ak820_emitted', ROOT / 'tests/ak820_emitted/run.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    fw = module.Firmware(build, args.s51.resolve(), (args.output_dir or build / 'bounded-tests').resolve())
    # Ordinary RAM ends before the native/peripheral windows. Keep the fixture
    # above both uninitialized and initialized linked XDATA, and below 0x1000.
    # Below 0x0440 are fixed native, LED DMA and IAP-stage reservations.
    ram_start, ram_end, fixture_size = 0x0440, 0x1000, 9
    mem = (build / 'ajazz_ak820_vial.mem').read_text()
    bounds = re.search(r'EXTERNAL RAM\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)', mem, re.I)
    areas = {(name, int(start, 16), int(size, 16))
             for name, start, size in re.findall(
                 r'^(\w+)\s+([0-9A-F]+)\s+([0-9A-F]+)\s+=.*\([^\n]*XDATA\)',
                 (build / 'ajazz_ak820_vial.map').read_text(), re.M)}
    if not bounds or not areas or any(
            start < ram_start or start + size > ram_end
            for _, start, size in areas if size):
        raise ValueError('Missing or unsupported linked ordinary XRAM layout')
    fixture = max(start + size for _, start, size in areas)
    if (int(bounds[1], 16) != ram_start or
            int(bounds[2], 16) + 1 != fixture or
            fixture + fixture_size > ram_end):
        raise ValueError('Journal fixture overlaps linked data or exceeds ordinary XRAM')
    valid = bytes([0xa5, 0, 0, 0x34, 0x1c, 255, 255, 0xcb, 0xe3])
    commands, expected = fw.initialize(), []
    for index in range(9):
        for value in range(256):
            header = bytearray(valid); header[index] = value
            label = f'header_{index:02}_{value:03}_END'
            commands += [module.memory('xram', fixture, header)]
            # B=0 supplies the generic XDATA tag in the control image; it is
            # harmless for the candidate's private two-byte pointer ABI.
            commands += fw.call('_journal_header_valid', fixture)
            # This SDCC bool returns in DPL, as checked in the linked listing.
            commands += fw.dump(label, 'sfr', 0x82, 1)
            expected.append((label, value == valid[index]))
    log, stack = fw.execute('journal-header-byte-domain', commands)
    # Exact padded labels avoid matching one observation's numeric prefix.
    sections = {part.split('\n', 1)[0]: part for part in log.split('@@')[1:]}
    for label, wanted in expected:
        actual = fw.extract('@@' + sections[label], label, 0x82, 1)[0]
        if actual != int(wanted):
            raise AssertionError((label, actual, wanted))
    report = {'pass': True, 'cases': len(expected),
              'linked_image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              'linked_map_sha256': hashlib.sha256((build / 'ajazz_ak820_vial.map').read_bytes()).hexdigest(),
              'fixture_address': fixture, 'fixture_size_bytes': fixture_size,
              'ordinary_xram_start': ram_start, 'ordinary_xram_end_exclusive': ram_end,
              'linked_xdata_areas': [{'name': name, 'start': start, 'size': size}
                                     for name, start, size in sorted(areas)],
              'initial_sp': fw.initial_sp, 'stack_capacity_bytes': fw.stack_capacity, **stack,
              'limits': 'Direct linked helper CPU execution with a simulated XDATA fixture. Stack peak covers this helper without IRQ overlap; no physical flash or durability proof.'}
    (fw.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
