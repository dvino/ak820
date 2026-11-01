#!/usr/bin/env python3
"""Hybrid retained QMK first-tap -> VIA macro -> extended Vial counterexample.

The source-derived producer and tapping functions use the existing host
adapter. The callback-only suppression variant is a negative control: it
suppresses repeated macro callbacks but does not own or repair queue slots.
This is not a production path, scheduler, ABI, or hardware test.
"""
import contextlib
import io
import os
from pathlib import Path
import re
import runpy
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    adapter = runpy.run_path(str(HERE / 'ph_vial_macro_entry_reference.py'))
with tempfile.TemporaryDirectory(prefix='.ph-vial-first-tap-', dir=HERE) as directory:
    path = Path(directory)
    (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', adapter['tapping'], flags=re.M))
    original = adapter['harness']
    stream = 'static const uint8_t macro_stream[] = {1, 5, 4, 0x22, 0};'
    assert original.count(stream) == 1
    original = original.replace(stream, 'static const uint8_t macro_stream[] = {1, 5, 5, 0x21, 0};')
    declaration = 'static void process_record(keyrecord_t *r) {'
    first = '    uint16_t k=cached[r->event.key.col]; bool down=r->event.pressed;'
    assert original.count(declaration) == 1 and original.count(first) == 1
    suppressed = original.replace(declaration, 'static bool macro_seen;\n' + declaration)
    suppressed = suppressed.replace(first, first + '\n    if (k == QK_MACRO && down) { if (macro_seen) return; macro_seen = true; }')
    trace = 'M 0 2204\nM 1 7700\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n'
    variants = [
        ('literal-reference', original),
        ('callback-only-suppression', suppressed),
        ('same-keycode', original.replace('{1, 5, 5, 0x21, 0}', '{1, 5, 4, 0x22, 0}')),
        ('zero-wait', original.replace('#define QS_tap_code_delay 5', '#define QS_tap_code_delay 0')),
    ]
    outputs = {}
    for name, body in variants:
        (path / 'probe.c').write_text(body)
        exe = path / name
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DQUICK_TAP_TERM=0', '-I', str(ROOT / 'quantum'), '-I', str(path), str(path / 'probe.c'), '-o', str(exe)], check=True)
        output = subprocess.run([str(exe)], input=trace, text=True, capture_output=True, check=True, timeout=5).stdout
        outputs[name] = output.splitlines()
        print(name + ':\n' + output, end='')
    literal = [
        '100 120 0 1 1 2204 00 0',
        '110 120 1 1 0 7700 00 0',
        '121 120 2 1 0 2105 01 0',
        'wait 120 5',
        '125 125 2 0 0 2105 00 0',
        '110 125 1 1 0 7700 00 0',
        '120 125 0 0 1 2204 00 0',
        '110 125 1 1 0 7700 00 0',
        'diagnostic-callback-limit',
    ]
    suppressed_expected = [
        '100 120 0 1 1 2204 00 0',
        '110 120 1 1 0 7700 00 0',
        '121 120 2 1 0 2105 01 0',
        'wait 120 5',
        '125 125 2 0 0 2105 00 0',
        '120 125 0 0 1 2204 00 0',
        '120 125 0 0 1 2204 00 0',
        '130 130 1 0 0 7700 00 0',
    ]
    assert outputs['literal-reference'] == literal, outputs['literal-reference']
    assert outputs['callback-only-suppression'] == suppressed_expected, outputs['callback-only-suppression']
    assert '121 120 2 1 0 2204 02 0' in outputs['same-keycode']
    assert 'wait 120 0' in outputs['zero-wait']
    assert outputs['same-keycode'] != literal and outputs['zero-wait'] != literal
    print('PASS: bounded literal trace; callback-only suppression duplicates release; same-keycode and wait controls differ')
