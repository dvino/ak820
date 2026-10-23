#!/usr/bin/env python3
"""Exercise standard Tri Layer interactions in a linked AK820 SDCC image.

The C52 fixture supplies matrix/NVM/USB readiness only; no device is opened.
Both the action cache and layer/Repeat/Vial handlers are real linked code.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('ak820_features', ROOT / 'tests/ak820_features/run.py')
features = importlib.util.module_from_spec(spec)
spec.loader.exec_module(features)
unlock, emitted = features.unlock, features.emitted
rows, assign, report, run_case = features.rows, features.assign, features.report, features.run_case
LOWER, UPPER = 0x7C77, 0x7C78


def setup_keys(fw, mapping):
    commands = fw.initialize()
    for key, code in mapping.items():
        if not fw.code[fw.address('_ak820_matrix_mask') + key[0]] & (1 << key[1]):
            raise ValueError(f'Test position is not a physical AK820 key: {key}')
        commands += assign(*key, code)
        for layer in range(1, 6):
            commands += assign(*key, 1, layer=layer)
    return commands


def cases(fw):
    lower, upper, second_lower, letter, repeat, toggle = (0, 0), (0, 1), (1, 5), (1, 3), (1, 2), (2, 4)
    setup = setup_keys(fw, {lower: LOWER, upper: UPPER})
    for first, second, first_layer, second_layer, name in (
        (lower, upper, 2, 4, 'lower-first'), (upper, lower, 4, 2, 'upper-first')
    ):
        yield run_case(fw, 'tri-layer-order-' + name, setup, [
            ('first', '_layer_state', 1, [first_layer], fw.transition(rows(first), 100)),
            ('both', '_layer_state', 1, [14], fw.transition(rows(first, second), 120)),
            ('first_up', '_layer_state', 1, [second_layer], fw.transition(rows(second), 140)),
            ('both_up', '_layer_state', 1, [0], fw.transition(rows(), 160)),
            ('no_hid', '_actual_keyboard_report', 8, report(), []),
        ])
    yield run_case(fw, 'tri-layer-simultaneous', setup, [
        ('both', '_layer_state', 1, [14], fw.transition(rows(lower, upper), 100)),
        ('both_up', '_layer_state', 1, [0], fw.transition(rows(), 120)),
    ])
    hidden = setup + assign(*lower, 5, layer=3) + assign(*upper, 6, layer=3)
    yield run_case(fw, 'tri-layer-release-hidden-by-adjust-map', hidden, [
        ('adjust', '_layer_state', 1, [14], fw.transition(rows(lower), 100) + fw.transition(rows(lower, upper), 120)),
        ('lower_up', '_layer_state', 1, [4], fw.transition(rows(upper), 140)),
        ('upper_up', '_layer_state', 1, [0], fw.transition(rows(), 160)),
        ('no_spurious_hid', '_actual_keyboard_report', 8, report(), []),
    ])
    yield run_case(fw, 'tri-layer-live-remap-release', setup, [
        ('adjust', '_layer_state', 1, [14], fw.transition(rows(lower, upper), 100)),
        ('original_lower_up', '_layer_state', 1, [4], assign(*lower, 5) + fw.transition(rows(upper), 120)),
        ('original_upper_up', '_layer_state', 1, [0], fw.transition(rows(), 140)),
        ('new_lower_assignment', '_actual_keyboard_report', 8, report(5), fw.transition(rows(lower), 160)),
        ('new_assignment_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 180)),
    ])
    yield run_case(fw, 'tri-layer-unlock-preserves-unrelated-toggle', setup + fw.write('_layer_state', [0x20]), [
        ('held_with_toggle', '_layer_state', 1, [0x2E], fw.transition(rows(lower, upper), 100)),
        ('unlock_clear_held', '_layer_state', 1, [0x20], unlock.vial(fw, 6)),
        ('second_unlock_idempotent', '_layer_state', 1, [0x20], unlock.vial(fw, 6)),
        ('suppressed_up_then_cancel', '_layer_state', 1, [0x20], fw.transition(rows(), 120) + unlock.vial(fw, 8)),
        ('reusable_after_cancel', '_layer_state', 1, [0x2E], fw.transition(rows(lower, upper), 140)),
        ('reused_up', '_layer_state', 1, [0x20], fw.transition(rows(), 160)),
    ])
    yield run_case(fw, 'tri-layer-unlock-preserves-other-member-toggle', setup + fw.write('_layer_state', [4]), [
        ('lower_with_upper_toggle', '_layer_state', 1, [14], fw.transition(rows(lower), 100)),
        ('unlock_preserves_upper', '_layer_state', 1, [4], unlock.vial(fw, 6)),
        ('cancel_preserves_upper', '_layer_state', 1, [4], fw.transition(rows(), 120) + unlock.vial(fw, 8)),
    ])
    yield run_case(fw, 'tri-layer-unlock-suppresses-new-press', setup, [
        ('new_press_suppressed', '_layer_state', 1, [0], unlock.vial(fw, 6) + fw.transition(rows(lower, upper), 100)),
        ('new_up_suppressed', '_layer_state', 1, [0], fw.transition(rows(), 120)),
        ('cancel_clean', '_layer_state', 1, [0], unlock.vial(fw, 8)),
    ])
    # These are ordinary QMK shared layer bits, not per-key reference counts:
    # either duplicate Lower release clears Lower and recalculates Adjust.
    duplicate = setup_keys(fw, {lower: LOWER, upper: UPPER, second_lower: LOWER})
    yield run_case(fw, 'tri-layer-duplicate-lower-shared-bit', duplicate, [
        ('both_lower', '_layer_state', 1, [2], fw.transition(rows(lower), 100) + fw.transition(rows(lower, second_lower), 120)),
        ('duplicate_adjust', '_layer_state', 1, [14], fw.transition(rows(lower, second_lower, upper), 140)),
        ('first_lower_up', '_layer_state', 1, [4], fw.transition(rows(second_lower, upper), 160)),
        ('upper_up', '_layer_state', 1, [0], fw.transition(rows(second_lower), 180)),
        ('last_lower_up', '_layer_state', 1, [0], fw.transition(rows(), 200)),
    ])
    mo = setup_keys(fw, {lower: 0x5221, upper: 0x5222})
    yield run_case(fw, 'tri-layer-ordinary-mo-remains-ordinary', mo, [
        ('mo_pair_no_adjust', '_layer_state', 1, [6], fw.transition(rows(lower, upper), 100)),
        ('mo_lower_only', '_layer_state', 1, [2], fw.transition(rows(lower), 120)),
        ('mo_all_up', '_layer_state', 1, [0], fw.transition(rows(), 140)),
    ])
    toggled = setup_keys(fw, {lower: LOWER, upper: UPPER, toggle: 0x5261})
    yield run_case(fw, 'tri-layer-toggle-plus-upper', toggled, [
        ('lower_toggled', '_layer_state', 1, [2], fw.transition(rows(toggle), 100) + fw.transition(rows(), 120)),
        ('upper_with_toggle', '_layer_state', 1, [14], fw.transition(rows(upper), 140)),
        ('upper_up_keeps_toggle', '_layer_state', 1, [2], fw.transition(rows(), 160)),
        ('toggle_off', '_layer_state', 1, [0], fw.transition(rows(toggle), 180) + fw.transition(rows(), 200)),
    ])
    remembered = setup_keys(fw, {lower: LOWER, upper: UPPER, letter: 4, repeat: 0x7C79})
    yield run_case(fw, 'tri-layer-repeat-keeps-letter-history', remembered, [
        ('letter', '_actual_keyboard_report', 8, report(4), fw.transition(rows(letter), 100)),
        ('layer_cycle', '_layer_state', 1, [0], fw.transition(rows(), 120) + fw.transition(rows(lower, upper), 140) + fw.transition(rows(), 160)),
        ('repeat_letter', '_actual_keyboard_report', 8, report(4), fw.transition(rows(repeat), 180)),
        ('repeat_no_layer', '_layer_state', 1, [0], []),
        ('repeat_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 200)),
    ])
    yield run_case(fw, 'tri-layer-synthetic-paired-vial-events', fw.initialize(), [
        ('virtual_lower', '_layer_state', 1, [2], fw.call('_vial_keycode_down', LOWER)),
        ('virtual_both', '_layer_state', 1, [14], fw.call('_vial_keycode_down', UPPER)),
        ('virtual_lower_up', '_layer_state', 1, [4], fw.call('_vial_keycode_up', LOWER)),
        ('virtual_both_up', '_layer_state', 1, [0], fw.call('_vial_keycode_up', UPPER)),
    ])
    # MO and TL both need cleanup when they together made Adjust active;
    # exercise both physical scan orders of the two different handler kinds.
    for tl_first in (False, True):
        mapping = {lower: LOWER if tl_first else 0x5221, upper: 0x5222 if tl_first else UPPER}
        first, second = (upper, lower) if tl_first else (lower, upper)
        mixed = setup_keys(fw, mapping)
        yield run_case(fw, 'tri-layer-unlock-mixed-mo-' + ('tl-first' if tl_first else 'mo-first'), mixed, [
            ('mixed_adjust', '_layer_state', 1, [14], fw.transition(rows(first), 100) + fw.transition(rows(first, second), 120)),
            ('mixed_unlock', '_layer_state', 1, [0], unlock.vial(fw, 6)),
            ('mixed_cancel', '_layer_state', 1, [0], fw.transition(rows(), 140) + unlock.vial(fw, 8)),
        ])
    layered_key = setup_keys(fw, {lower: LOWER, upper: UPPER, letter: 4}) + assign(*letter, 5, layer=3)
    yield run_case(fw, 'tri-layer-held-adjust-key-release', layered_key, [
        ('adjust_letter', '_actual_keyboard_report', 8, report(5), fw.transition(rows(lower, upper), 100) + fw.transition(rows(lower, upper, letter), 120)),
        ('layers_up', '_layer_state', 1, [0], fw.transition(rows(letter), 140)),
        ('letter_still_held', '_actual_keyboard_report', 8, report(5), []),
        ('original_adjust_letter_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 160)),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--s51', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xC700:
        raise ValueError('Tri Layer runtime tests require a bounded image below the NVM fixture')
    fw.address('_process_tri_layer')
    result = {'linked_image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              'level': 'uCsim C52 linked code; no physical USB/peripheral/IRQ validation',
              'hardware_validated': False, 'tests': list(cases(fw)),
              'test_source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(), ROOT / 'tests/ak820_features/run.py', ROOT / 'tests/ak820_unlock/run.py', ROOT / 'tests/ak820_emitted/run.py')}}
    result['pass'] = all(item['pass'] for item in result['tests'])
    (fw.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)


if __name__ == '__main__':
    main()
