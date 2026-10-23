#!/usr/bin/env python3
"""CPU tests of linked reactive RGB; simulated memory only, no physical device."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('emitted_support', HERE.parent / 'ak820_emitted/run.py')
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    fw = support.Firmware(args.build_dir.resolve(), args.s51.resolve(),
                          (args.output_dir or args.build_dir / 'rgb-emitted').resolve())
    commands = fw.initialize() + fw.clock(0)
    # Existing EEPROM mode IDs: Solid=1, Direct=5; append Reactive=6.
    commands += fw.write('_rgb_matrix_config', [25, 0, 255, 160, 0, 255, 0, 0])
    observations = []

    def observe(label, index, expected):
        commands.extend(fw.dump(label, 'xram', fw.led_address(index), 4))
        observations.append((label, fw.led_address(index), expected))

    def event(slot, pressed=True):
        commands.extend(fw.write('_process_rgb_matrix_PARM_2', [slot & 7]))
        commands.extend(fw.write('_process_rgb_matrix_PARM_3', [int(pressed)]))
        commands.extend(fw.call('_process_rgb_matrix', slot >> 3))

    commands += fw.frame(16)
    observe('idle', 0, [0, 0, 0, 0])
    event(0)
    commands += fw.frame(32)
    # V=158 quantizes to152 -> CIE=71.
    observe('first_press', 0, [255, 71, 0, 0])
    observe('other_dark', 81, [0, 0, 0, 0])
    commands += fw.clock(512)
    event(125)
    event(0, False)
    commands += fw.frame(528)
    observe('chord_first', 0, [255, 41, 0, 0])
    observe('chord_last', 81, [255, 71, 0, 0])
    commands += fw.frame(2064)
    observe('first_expired', 0, [0, 0, 0, 0])
    commands += fw.frame(2560)
    observe('all_expired', 81, [0, 0, 0, 0])
    event(104)  # Encoder switch has no LED.
    commands += fw.frame(2576)
    observe('encoder_hole', 0, [0, 0, 0, 0])
    event(0)
    commands += fw.call('_rgb_matrix_set_suspend_state', 1)
    observe('suspend_immediate', 0, [0, 0, 0, 0])
    commands += fw.call('_rgb_matrix_set_suspend_state', 0) + fw.frame(2592)
    observe('resume_black', 0, [0, 0, 0, 0])
    commands += fw.clock(65520)
    event(0)
    commands += fw.frame(65552)
    observe('wrap_lit', 0, [255, 71, 0, 0])
    commands += fw.frame(67600)
    observe('wrap_expired', 0, [0, 0, 0, 0])
    log, stack = fw.execute('reactive-chords-expiry-suspend-wrap', commands)
    cases = []
    for label, address, expected in observations:
        actual = fw.extract(log, label, address, 4)
        cases.append({'name': label, 'pass': actual == expected, 'actual': actual, 'expected': expected})
    report = {'pass': all(c['pass'] for c in cases), 'cases': cases, **stack,
              'linked_image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              'limits': 'uCsim C52 CPU/linked-code fixtures; no VS11K28A peripheral, physical timing or device validation.'}
    (fw.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if not report['pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
