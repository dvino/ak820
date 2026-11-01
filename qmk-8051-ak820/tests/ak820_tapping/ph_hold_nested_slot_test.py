#!/usr/bin/env python3
"""Host-only PH hold-settlement callback with a nested preheld release.

The synchronous nested call is injected by the host callback; this is not a
claim that this exact callback is reachable in a linked AK820 image. The
candidate retains the source process_tapping body and uses the earlier
trace-specific owned-slot pump, including its explicit scan-write rejection.
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
BOARD = ROOT / 'keyboards/ajazz/ak820'
with contextlib.redirect_stdout(io.StringIO()):
    previous = runpy.run_path(str(HERE / 'ph_vial_slot_slice_test.py'))
adapter = previous['adapter']
original = adapter['tapping']
candidate = previous['body']
claim_index = '        unsigned index = (unsigned)(owned - candidate_slots.slots);'
unclaim = '            if (!ak820_ph_slot_unclaim(owned)) _Exit(92);'
assert candidate.count(claim_index) == 1 and candidate.count(unclaim) == 1
candidate = candidate.replace(claim_index, claim_index + '\n        if (in_nested && candidate_records[index].event.key.col == 1 && candidate_records[index].event.pressed) ++nested_claims;')
candidate = candidate.replace(unclaim, '            if (in_nested && candidate_records[index].event.key.col == 1 && candidate_records[index].event.pressed) ++nested_unclaims;\n' + unclaim)
# The prior slice's release guard was trace-specific and is not used here.
harness = adapter['harness']
start = 'static void process_record(keyrecord_t *r) {'
assert harness.count(start) == 1
harness = harness.replace(start, 'static void nested_hold_callback(void);\nstatic bool did_nest, in_nested;\nstatic unsigned nested_claims, nested_unclaims;\n' + start)
log = '    printf("%u %u %u %u %u %04x %02x %lx\\n", r->event.time,now,r->event.key.col,down,r->tap.count,k,mods,(unsigned long)layers);'
assert harness.count(log) == 1
harness = harness.replace(log, log + '\n    if (k == 0x2204 && down && !r->tap.count && !did_nest) { did_nest = true; nested_hold_callback(); }')
include = '#include "retained_engine.inc"'
assert harness.count(include) == 1
harness = harness.replace(include, include + r'''
static void nested_hold_callback(void) {
    printf("hold-enter %u %u %u %u %02x\n", now, tapping_key.event.pressed, tapping_key.tap.count, tapping_key.tap.interrupted, mods);
    printf("queued-enter %u %u %u\n", waiting_buffer_head != waiting_buffer_tail, waiting_buffer[waiting_buffer_tail].event.key.col, waiting_buffer[waiting_buffer_tail].event.pressed);
    now = 121;
    keyrecord_t release = {.event={.key={0,2},.time=now,.pressed=false,.type=1}};
    in_nested = true;
    action_tapping_process(release);
    in_nested = false;
    printf("slot-observation %u %u\n", nested_claims, nested_unclaims);
    printf("hold-exit %u %u %u %u %02x\n", now, tapping_key.event.pressed, tapping_key.tap.count, tapping_key.tap.interrupted, mods);
}
''')
settlement = '''                    ac_dprintf("Tapping: End. No tap. Interfered by typing key\\n");
                    process_record(&tapping_key);
                    //tapping_key = (keyrecord_t){0};
                    memset(&tapping_key,0,sizeof(keyrecord_t));'''
early = '''                    ac_dprintf("Tapping: End. No tap. Interfered by typing key\\n");
                    keyrecord_t copy = tapping_key;
                    memset(&tapping_key,0,sizeof(keyrecord_t));
                    process_record(&copy);'''
assert candidate.count(settlement) == 1
mutant = candidate.replace(settlement, early)
trace = 'M 0 2204\nM 1 0005\nM 2 0006\nE 90 2 1\nE 100 0 1\nE 110 1 1\nE 120 1 0\nE 140 0 0\n'
flags = [os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-Wno-unused-function', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DQUICK_TAP_TERM=0', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3']
with tempfile.TemporaryDirectory(prefix='.ph-hold-nested-', dir=HERE) as directory:
    path = Path(directory)
    results = {}
    for name, body in [('reference', original), ('candidate', candidate), ('early-clear', mutant)]:
        (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', body, flags=re.M))
        (path / 'probe.c').write_text('#include "ak820_ph_slots.h"\n' + harness)
        exe = path / name
        subprocess.run(flags + ['-I', str(ROOT / 'quantum'), '-I', str(BOARD), '-I', str(path), str(path / 'probe.c'), str(BOARD / 'ak820_ph_slots.c'), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], input=trace, text=True, capture_output=True, timeout=5)
        results[name] = result
        print(name, 'exit', result.returncode)
        print(result.stdout, end='')
    expected = [
        '90 90 2 1 0 0006 00 0',
        '100 120 0 1 0 2204 02 0',
        'hold-enter 120 1 0 1 02',
        'queued-enter 1 1 1',
        '121 121 2 0 0 0006 02 0',
        'hold-exit 121 1 0 1 02',
        '110 121 1 1 0 0005 02 0',
        '120 121 1 0 0 0005 02 0',
        '140 140 0 0 0 2204 00 0',
    ]
    for name in ('reference', 'candidate'):
        result = results[name]
        assert result.returncode == 0, (name, result.stderr)
        rows = result.stdout.splitlines()
        observation = [row for row in rows if row.startswith('slot-observation ')]
        assert observation == ['slot-observation 1 1' if name == 'candidate' else 'slot-observation 0 0'], (name, observation)
        assert [row for row in rows if not row.startswith('slot-observation ')] == expected, (name, rows)
    mutant_result = results['early-clear']
    assert mutant_result.returncode == 0
    rows = mutant_result.stdout.splitlines()
    assert 'hold-enter 120 0 0 0 02' in rows
    assert rows.index('110 121 1 1 0 0005 02 0') < rows.index('hold-exit 121 0 0 0 02')
    assert rows != results['candidate'].stdout.splitlines()
    print('PASS: all reference callback/state rows match; nested claim unclaimed; early-clear changes state and ordering')
