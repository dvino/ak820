#!/usr/bin/env python3
"""Compare a narrow ownership slice to the retained reference, not firmware."""
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
reference = (ROOT / 'quantum/action_tapping.c').read_text()
harness = (HERE / 'ph_reference_harness.c').read_text()
marker = 'static void process_record(keyrecord_t *r) {'
assert harness.count(marker) == 1
harness = harness.replace(marker, 'static bool injected;\n' + marker)
marker = '    printf("%u %u %u %u %u %04x %02x %lx\\n", r->event.time,now,r->event.key.col,down,r->tap.count,k,mods,(unsigned long)layers);'
assert harness.count(marker) == 1
harness = harness.replace(marker, marker + '''
    if (r->event.key.col == 1 && down && r->tap.count == 1 && !injected) {
        injected = true;
        keyrecord_t nested = {.event={.key={0,0},.time=now,.pressed=false,.type=1}};
        action_tapping_process(nested);
    }
''')
flags = [os.environ.get('CC', 'cc'), '-std=c11', '-O1', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-fsanitize=undefined', '-fno-sanitize-recover=undefined']
with tempfile.TemporaryDirectory(prefix='.ph-first-tap-', dir=HERE) as directory:
    path = Path(directory)
    (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', reference, flags=re.M))
    (path / 'reference.c').write_text(harness)
    refexe = path / 'reference'
    subprocess.run(flags + ['-DQUICK_TAP_TERM=0', '-I', str(ROOT / 'quantum'), '-I', str(path), str(path / 'reference.c'), '-o', str(refexe)], check=True)
    input_trace = 'M 0 6\nM 1 2204\nE 90 0 1\nE 100 1 1\nE 110 1 0\n'
    ref = subprocess.run([str(refexe)], input=input_trace, text=True, capture_output=True, check=True, timeout=5).stdout
    expected = ('90 90 0 1 0 0006 00 0\n'
                '100 110 1 1 1 2204 00 0\n'
                '110 110 0 0 0 0006 00 0\n'
                '110 110 1 0 1 2204 00 0\n')
    assert ref == expected, ref
    slots = (BOARD / 'ak820_ph_slots.c').read_text()
    body = (HERE / 'ph_first_tap_slice.c').read_text()
    barrier_old = 'if (slot->state == AK820_PH_WAITING) {'
    decision_old = 's->tap_count = 1;'
    assert slots.count(barrier_old) == 1 and body.count(decision_old) == 1
    for name, slot_source, slice_source in (
        ('candidate', slots, body),
        ('claimed-head-barrier', slots.replace(barrier_old, 'if (slot->state == AK820_PH_CLAIMED) return 0;\n        ' + barrier_old), body),
        ('replay-claimed-slot', slots.replace(barrier_old, 'if (slot->state == AK820_PH_WAITING || slot->state == AK820_PH_CLAIMED) {'), body),
        ('wrong-tap-decision', slots, body.replace(decision_old, 's->tap_count = 0;')),
    ):
        (path / 'slots.c').write_text(slot_source)
        (path / 'slice.c').write_text(slice_source)
        exe = path / name
        subprocess.run(flags + ['-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-I', str(BOARD), str(path / 'slots.c'), str(path / 'slice.c'), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], text=True, capture_output=True, timeout=5)
        if name == 'candidate':
            assert result.returncode == 0 and result.stdout == expected, (result.returncode, result.stdout, result.stderr)
        else:
            assert result.returncode != 0 or result.stdout != expected, name
        print(f'PASS: {name}' + (' matches retained first-tap trace' if name == 'candidate' else ' fails the first-tap oracle'))
