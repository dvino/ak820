#!/usr/bin/env python3
"""Check the emitted delay callee-save ABI in a C52 CPU model, offline."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('iap', ROOT / 'tests/ak820_iap/run.py')
iap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iap)
emitted = iap.emitted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    console = iap.Console(fw.simulator, fw.image)
    cases = []
    try:
        console.command(fw.initialize())
        for name, counts in (('_mDelayuS', (0, 1, 40, 1000)), ('_mDelaymS', (0, 1, 10))):
            for count in counts:
                registers = [(0x41 + i * 17) & 255 for i in range(8)]
                console.command([emitted.memory('iram', 0, registers),
                                 emitted.memory('sfr', 0xD0, [0]),
                                 emitted.memory('sfr', 0xA8, [0])])
                stack = console.read('sfr', 0x81, 1)
                console.command(fw.call(name, count))
                assert console.read('iram', 0, 8) == registers, (name, count, 'R0-R7 preservation')
                assert console.read('sfr', 0x81, 1) == stack, (name, count, 'balanced stack')
                local = [symbol for symbol in fw.symbols if symbol.startswith(name + '_n_')]
                assert len(local) == 1, (name, local)
                assert console.read('xram', fw.address(local[0]), 2) == [0, 0], (name, count, 'loop completion')
                cases.append({'function': name, 'count': count, 'registers_preserved': True,
                              'stack_balanced': True, 'loop_completed': True})
    finally:
        console.close()
        (fw.output / 'cpu.log').write_text(console.log)
    result = {'ihx_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              'hardware_validated': False, 'cases': cases,
              'limitation': 'C52 CPU model; no wall-clock timing or physical USB wake validation'}
    (fw.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: emitted microsecond/millisecond delays preserve R0-R7, balance stack and finish loops')


if __name__ == '__main__':
    main()
