#!/usr/bin/env python3
"""Bounded host cancellation model; Combo milestone from retained source fixture."""
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
BOARD = HERE.parents[1] / 'keyboards/ajazz/ak820'
source = (HERE / 'ph_cancel_model.c').read_text()
variants = [('candidate', source)]
for name, old, new in [
    ('reacquire', '    m->cleaning = true;\n    for (unsigned i = 0; i < PHYSICAL;', '    m->cleaning = true; m->quarantine = false;\n    for (unsigned i = 0; i < PHYSICAL;'),
    ('no-held-quarantine', 'if (m->physical[i]) m->blocked[i] = true;', 'if (m->physical[i]) m->blocked[i] = false;'),
    ('early-combo-up', 'if (!m->combo_members) {', 'if (true) {'),
    ('physical-bits-as-lifecycle', 'if (!m->combo_members) {', 'if (!m->physical[4] && !m->physical[5]) {'),
    ('no-zero-depth-exit', 'if (!m->cleaning && !m->depth && !m->slots.count) m->quarantine = false;', 'if (!m->cleaning && !m->depth && !m->slots.count && 0) m->quarantine = false;'),
    ('double-up', '++m->ups[i]; if (m->on_up) m->on_up(m, i);', 'm->ups[i] += 2; if (m->on_up) m->on_up(m, i);'),
    ('no-drain-after-unpin', 'if (m->quarantine) { drain_waiting(m); maybe_exit(m); } }\nstatic unsigned reentrant_calls;', 'if (m->quarantine) maybe_exit(m); }\nstatic unsigned reentrant_calls;'),
    ('no-exit-after-finish', 'static void finish_claim(model *m, ak820_ph_slot *slot) { CHECK(ak820_ph_slot_finish(&m->slots, slot)); if (m->quarantine) { drain_waiting(m); maybe_exit(m); } }', 'static void finish_claim(model *m, ak820_ph_slot *slot) { CHECK(ak820_ph_slot_finish(&m->slots, slot)); }'),
]:
    assert source.count(old) == 1, name
    variants.append((name, source.replace(old, new)))
reference = subprocess.run(['python3', str(HERE / 'ph_combo_reference.py')], text=True, capture_output=True, check=True, timeout=20).stdout
prefix = reference.split('compiled direct-dispatch mutant:', 1)[0]
rows = [row for row in prefix.splitlines() if row.startswith('F ')]
assert rows == ['F 10 80 2 1 4129 a129 0 2', 'F 30 80 0 1 0006 0006 0 2', 'F 80 80 0 0 0006 0006 0 2', 'F 90 90 2 0 4129 a129 0 0']
assert 'both member-release orders' in reference
reference_release_time = int(rows[2].split()[1])
with tempfile.TemporaryDirectory(prefix='.ph-cancel-model-', dir=HERE) as directory:
    path = Path(directory)
    for name, body in variants:
        variant = path / (name + '.c')
        variant.write_text(body)
        exe = path / name
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-I', str(BOARD), str(variant), str(BOARD / 'ak820_ph_slots.c'), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], text=True, capture_output=True, timeout=5)
        if name == 'candidate':
            assert result.returncode == 0, result.stderr
            lines = result.stdout.splitlines()
            assert [row for row in lines if row.startswith('combo-last ')] == [f'combo-last {reference_release_time}'] * 2
            print(result.stdout, end='')
            print('PASS: both model last-member timestamps match retained Combo fixture')
        else:
            assert result.returncode == 1 and 'check failed:' in result.stderr, (name, result.returncode, result.stderr)
            print(f'PASS: {name} control rejected: {result.stderr.strip()}')
