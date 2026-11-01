#!/usr/bin/env python3
"""Differential host scan experiment; retained helpers, not linked firmware."""
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
source = (ROOT / 'quantum/action_tapping.c').read_text()
def extract(signature):
    start = source.index(signature)
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]
reference = extract('bool waiting_buffer_typed(keyevent_t event) {') + '\n' + extract('void waiting_buffer_scan_tap(void) {') + '\n'
implementation = (HERE / 'ph_scan_slots.c').read_text()
write = '            candidate->tap.count = 1;'
visible = '        if (slot->state == AK820_PH_RETIRED) continue;'
pin_callback = '            callback(context);\n            if (!ak820_ph_slot_unpin(&queue->slots, slot)) return PH_SCAN_ERROR;'
bound = ' < term) {'
assert implementation.count(write) == 1 and implementation.count(visible) == 2
assert implementation.count(pin_callback) == 1 and implementation.count(bound) == 1
variants = [
    ('candidate', implementation),
    ('lost-writeback', implementation.replace(write, '            /* mutation lost */')),
    ('hide-claimed', implementation.replace(visible, '        if (slot->state == AK820_PH_RETIRED || slot->state == AK820_PH_CLAIMED) continue;')),
    ('early-unpin', implementation.replace(pin_callback, '            if (!ak820_ph_slot_unpin(&queue->slots, slot)) return PH_SCAN_ERROR;\n            callback(context);')),
    ('inclusive-term', implementation.replace(bound, ' <= term) {')),
]
with tempfile.TemporaryDirectory(prefix='.ph-scan-slots-', dir=HERE) as directory:
    path = Path(directory)
    (path / 'retained_scan.inc').write_text(reference)
    for name, body in variants:
        variant = path / (name + '.c')
        variant.write_text(body)
        exe = path / name
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-I', str(HERE), '-I', str(BOARD), '-I', str(path), str(variant), str(HERE / 'ph_scan_slots_harness.c'), str(BOARD / 'ak820_ph_slots.c'), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], text=True, capture_output=True, timeout=5)
        if name == 'candidate':
            assert result.returncode == 0, result.stderr
            print(result.stdout, end='')
        else:
            assert result.returncode == 1 and 'check failed:' in result.stderr, (name, result.returncode, result.stderr)
            print(f'PASS: {name} control rejected: {result.stderr.strip()}')
