#!/usr/bin/env python3
"""Check the shared event-copy ABI in a complete linked C52 image, offline."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('emitted', ROOT / 'tests/ak820_emitted/run.py')
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xc700 or fw.symbol_sizes['_action_exec_PARM_1'] != 6:
        raise ValueError('Requires a production-bounded image with the pinned event ABI')
    # Only simulated XRAM is used. A nonzero high address byte and unrelated
    # first payload byte expose SDCC #4054's erroneous extra dereference.
    source = 0x1f37
    commands = fw.initialize() + fw.write('_vial_unlock_in_progress', [1])
    observations = []
    for row, col in [(0, 0), (1, 3), (15, 7), (0xfd, 0), (0xfc, 0), (0xf0, 0xf0), (0xff, 0xff)]:
        for time in (0, 1, 0x7e85, 0xffff):
            for kind in range(5):
                for pressed in (0, 1):
                    label = 'event-' + str(len(observations))
                    event = [col, row, time & 255, time >> 8, kind, pressed]
                    commands += [emitted.memory('xram', source, event)]
                    commands += fw.call('_ak820_action_exec', source)
                    commands += fw.dump_symbol(label + '-copy', '_action_exec_PARM_1', 6)
                    commands += fw.dump(label + '-input', 'xram', source, 6)
                    observations.append((label, event))
    log, stack = fw.execute('event-copy', commands)
    failures = []
    for label, event in observations:
        actual = fw.extract(log, label + '-copy', fw.address('_action_exec_PARM_1'), 6)
        original = fw.extract(log, label + '-input', source, 6)
        if actual != event or original != event:
            failures.append({'label': label, 'expected': event, 'actual': actual, 'input_after': original})
    paths = [Path(__file__), Path(emitted.__file__), ROOT / 'quantum/action.c', ROOT / 'quantum/action.h',
             ROOT / 'quantum/keyboard.c', ROOT / 'quantum/encoder.c', ROOT / 'quantum/vial.c']
    report = {
        'pass': not failures, 'cases': len(observations), 'failures': failures,
        'hardware_validated': False, 'physical_device_commands': 0,
        'limits': 'C52 event-copy ABI with unlock guard; production pipeline behavior is covered by the emitted feature suites. No device or IRQ timing proof.',
        'image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
        'map_sha256': hashlib.sha256((fw.build / 'ajazz_ak820_vial.map').read_bytes()).hexdigest(),
        'simulator_sha256': hashlib.sha256(args.s51.read_bytes()).hexdigest(),
        'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        **stack,
    }
    (fw.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return not report['pass']


if __name__ == '__main__':
    raise SystemExit(main())
