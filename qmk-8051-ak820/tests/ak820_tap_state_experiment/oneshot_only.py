#!/usr/bin/env python3
"""Characterize why enabling One Shot state alone is not usable One Shot.

Run against a bounded linked image with NO_ACTION_TAPPING still defined.
Expected observations deliberately describe the existing held-mod/no-layer
fallback, not successful One Shot behavior. No physical device is opened.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('ak820_tri_layer', ROOT / 'tests/ak820_tri_layer/run.py')
tri = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tri)
emitted, run_case, setup_keys = tri.emitted, tri.run_case, tri.setup_keys
rows, assign, report = tri.rows, tri.assign, tri.report


def cases(fw):
    osm, osl, letter = (0, 0), (0, 1), (1, 3)
    # Explicitly enable the runtime settings bit, so the absent One Shot
    # behavior is not an artifact of the fixture skipping keyboard_init().
    setup = setup_keys(fw, {osm: 0x52A2, osl: 0x5281, letter: 4})
    setup += fw.write('_keymap_config', [0, 4])
    setup += assign(*letter, 5, layer=1)
    yield run_case(fw, 'oneshot-only-osm-is-held-shift', setup, [
        ('osm_down', '_actual_keyboard_report', 8, report(0, 2), fw.transition(rows(osm), 100)),
        ('held_chord', '_actual_keyboard_report', 8, report(4, 2), fw.transition(rows(osm, letter), 120)),
        ('osm_up_removes_shift', '_actual_keyboard_report', 8, report(4), fw.transition(rows(letter), 140)),
        ('all_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 160)),
    ])
    yield run_case(fw, 'oneshot-only-osm-tap-does-not-arm-next-key', setup, [
        ('osm_tap_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(osm), 100) + fw.transition(rows(), 120)),
        ('next_a_is_plain', '_actual_keyboard_report', 8, report(4), fw.transition(rows(letter), 140)),
        ('all_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 160)),
    ])
    yield run_case(fw, 'oneshot-only-osl-does-not-enable-held-layer', setup, [
        ('osl_down_layer', '_layer_state', 1, [0], fw.transition(rows(osl), 100)),
        ('held_base_a', '_actual_keyboard_report', 8, report(4), fw.transition(rows(osl, letter), 120)),
        ('held_layer_still_zero', '_layer_state', 1, [0], []),
        ('all_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 160)),
    ])
    yield run_case(fw, 'oneshot-only-osl-tap-does-not-arm-next-layer', setup, [
        ('osl_tap_up_layer', '_layer_state', 1, [0], fw.transition(rows(osl), 100) + fw.transition(rows(), 120)),
        ('next_a_is_base', '_actual_keyboard_report', 8, report(4), fw.transition(rows(letter), 140)),
        ('all_up', '_actual_keyboard_report', 8, report(), fw.transition(rows(), 160)),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--s51', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xC700:
        raise ValueError('Characterization requires a bounded image below the NVM fixture')
    if '_process_tapping' in fw.symbols:
        raise ValueError('This characterization requires tapping to remain disabled')
    # Both-disabled firmware has the same observable fallback. Requiring a
    # retained One Shot state function proves this is the flag-only variant.
    fw.address('_clear_oneshot_mods')
    result = {
        'linked_image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
        'level': 'uCsim C52 linked code, simulated matrix/NVM/USB readiness; no hardware validation',
        'hardware_validated': False,
        'oneshot_available': False,
        'interpretation': 'PASS confirms held OSM and inactive OSL fallbacks; it does not claim working One Shot',
        'oneshot_state_code_retained': '_clear_oneshot_mods' in fw.symbols,
        'tests': list(cases(fw)),
        'test_source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__).resolve(), ROOT / 'tests/ak820_tri_layer/run.py',
                                         ROOT / 'tests/ak820_features/run.py', ROOT / 'tests/ak820_unlock/run.py',
                                         ROOT / 'tests/ak820_emitted/run.py')},
    }
    result['characterization_pass'] = all(item['pass'] for item in result['tests'])
    (fw.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['characterization_pass'] else 1)


if __name__ == '__main__':
    main()
