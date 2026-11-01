#!/usr/bin/env python3
"""Retained PH callback nesting probe; not a production scheduler or ABI test.

The adapter injects all three records directly into tapping; basic Vial codes
actually bypass tapping, and compact Vial reduces generated MT/LT to tap codes.
The deliberately deferred lane is a negative control, not an implementation.
The middle marker has zero elapsed time; it does not simulate a wait.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
source = (ROOT / 'quantum/action_tapping.c').read_text()
harness = (HERE / 'ph_reference_harness.c').read_text()
needle = 'static void process_record(keyrecord_t *r) {'
assert harness.count(needle) == 1
helper = '''
static bool deferred, injected;
static void generated_tap(void) {
    keyrecord_t down = {.event={.key={0,2},.time=now,.pressed=true,.type=1}};
    keyrecord_t up = {.event={.key={0,2},.time=now,.pressed=false,.type=1}};
    cached[2] = map[2];
    puts("generated-down-begin");
    action_tapping_process(down);
    puts("generated-between-edges");
    action_tapping_process(up);
    puts("generated-up-end");
}
'''
harness = harness.replace(needle, helper + needle)
needle = '    printf("%u %u %u %u %u %04x %02x %lx\\n", r->event.time,now,r->event.key.col,down,r->tap.count,k,mods,(unsigned long)layers);'
assert harness.count(needle) == 1
harness = harness.replace(needle, needle + '''
    if (r->event.key.col == 1 && down && !injected) {
        injected = true;
        puts("callback-before");
#ifdef DEFER_LANE
        deferred = true;
#else
        generated_tap();
#endif
        puts("callback-after");
    }
''')
needle = '            action_tapping_process(r);'
assert harness.count(needle) == 1
harness = harness.replace(needle, needle + '''
            if (deferred) { deferred = false; generated_tap(); }
''')

with tempfile.TemporaryDirectory(prefix='.ph-generated-lane-', dir=HERE) as directory:
    path = Path(directory)
    (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', source, flags=re.M))
    (path / 'probe.c').write_text(harness)
    binaries = []
    for flags in ([], ['-DDEFER_LANE']):
        exe = path / ('deferred' if flags else 'synchronous')
        subprocess.run([os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DQUICK_TAP_TERM=0', *flags, '-I', str(ROOT / 'quantum'), '-I', str(path), str(path / 'probe.c'), '-o', str(exe)], check=True)
        binaries.append(exe)
    for code in ('0006', '2206', '4106'):
        trace = f'M 0 2204\nM 1 0005\nM 2 {code}\nE 100 0 1\nE 110 1 1\nE 120 1 0\nE 130 0 0\n'
        outputs = [subprocess.run([str(exe)], input=trace, text=True, capture_output=True, check=True).stdout for exe in binaries]
        print(f'generated {code}:\nsynchronous:\n{outputs[0]}deferred:\n{outputs[1]}')
        for output in outputs:
            assert 'OVERFLOW' not in output
        assert outputs[0].index('callback-before') < outputs[0].index('generated-down-begin') < outputs[0].index('generated-between-edges') < outputs[0].index('generated-up-end') < outputs[0].index('callback-after')
        assert outputs[1].index('callback-before') < outputs[1].index('callback-after') < outputs[1].index('generated-down-begin')
        rows = [[line.split() for line in output.splitlines() if re.match(r'^\d+ ', line)] for output in outputs]
        assert rows[0] != rows[1]
        generated = [[row for row in trace_rows if row[2] == '2'] for trace_rows in rows]
        for index, records in enumerate(generated):
            assert len(records) == 2
            count = '0' if code == '0006' or index == 0 else '1'
            assert [row[:6] for row in records] == [
                ['120', '120', '2', '1', count, code],
                ['120', '120', '2', '0', count, code],
            ]
        # Reentry encounters the still-live queue tail; do not treat these
        # duplicate reference callbacks as desirable production behavior.
        press = '110 120 1 1 0 0005'
        release = '120 120 1 0 0 0005'
        assert sum(line.startswith(press) for line in outputs[0].splitlines()) == 3
        assert sum(line.startswith(release) for line in outputs[0].splitlines()) == 2
        assert sum(line.startswith(press) for line in outputs[1].splitlines()) == 1
        assert sum(line.startswith(release) for line in outputs[1].splitlines()) == 1
        if code != '0006':
            assert f'120 120 2 1 0 {code}' in outputs[0]
            assert f'120 120 2 1 1 {code}' in outputs[1]
print('PASS: retained synchronous callback differs from deliberately deferred lane for basic, MT and LT')
