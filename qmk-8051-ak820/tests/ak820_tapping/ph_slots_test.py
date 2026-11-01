#!/usr/bin/env python3
"""Host checks for the unwired slot ownership primitive, not PH equivalence."""
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
BOARD = HERE.parents[1] / 'keyboards/ajazz/ak820'
source = (BOARD / 'ak820_ph_slots.c').read_text()
old = 'if (slot->state == AK820_PH_WAITING) {'
pins = 'slot->state == AK820_PH_RETIRED && !slot->pins'
assert source.count(old) == 1 and source.count(pins) == 1
with tempfile.TemporaryDirectory(prefix='.ph-slots-', dir=HERE) as directory:
    path = Path(directory)
    disabled = path / 'disabled.o'
    subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-Wall', '-Wextra', '-Werror', '-I', str(BOARD), '-c', str(BOARD / 'ak820_ph_slots.c'), '-o', str(disabled)], check=True)
    symbols = subprocess.run(['nm', '-g', str(disabled)], text=True, capture_output=True, check=True).stdout
    assert 'ak820_ph_' not in symbols, symbols
    print('PASS: disabled source exports no PH slot symbols')
    for name, body in [
        ('candidate', source),
        ('replay-claim', source.replace(old, 'if (slot->state == AK820_PH_WAITING || slot->state == AK820_PH_CLAIMED) {')),
        ('block-at-claim', source.replace(old, 'if (slot->state == AK820_PH_CLAIMED) return 0;\n        ' + old)),
        ('reuse-pinned', source.replace(pins, 'slot->state == AK820_PH_RETIRED')),
    ]:
        candidate = path / (name + '.c')
        exe = path / name
        candidate.write_text(body)
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-I', str(BOARD), str(candidate), str(HERE / 'ph_slots_harness.c'), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], text=True, capture_output=True)
        if name == 'candidate':
            assert result.returncode == 0, result.stderr
            print(result.stdout, end='')
        else:
            assert result.returncode != 0 and 'check failed:' in result.stderr, result.stderr
            print(f'PASS: compiled {name} mutant rejected')
    for capacity in (1, 255):
        bounds_exe = path / f'bounds-{capacity}'
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', f'-DAK820_PH_SLOT_CAPACITY={capacity}', '-I', str(BOARD), str(BOARD / 'ak820_ph_slots.c'), str(HERE / 'ph_slots_bounds.c'), '-o', str(bounds_exe)], check=True)
        subprocess.run([str(bounds_exe)], check=True)
    print('PASS: host capacities 1 and 255 do not wrap')
    trace_exe = path / 'trace'
    subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-I', str(BOARD), str(BOARD / 'ak820_ph_slots.c'), str(HERE / 'ph_slots_trace.c'), '-o', str(trace_exe)], check=True)
    actual = subprocess.run([str(trace_exe)], text=True, capture_output=True, check=True).stdout.splitlines()
    ref = subprocess.run(['python3', str(HERE / 'ph_generated_lane_reference.py')], text=True, capture_output=True, check=True, timeout=20).stdout
    sync = ref.split('generated 0006:\nsynchronous:\n', 1)[1].split('deferred:\n', 1)[0]
    expected, released = [], False
    markers = {'callback-before', 'generated-down-begin', 'generated-between-edges', 'generated-up-end', 'callback-after'}
    for line in sync.splitlines():
        if line in markers:
            expected.append(line)
        elif line.startswith('120 120 1 0 0 0005') and not released:
            expected.append('queued-release')
            released = True
    assert released and actual == expected, (actual, expected)
    print('PASS: ownership-only nested release milestones match first-delivery hybrid trace')
