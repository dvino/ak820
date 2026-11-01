#!/usr/bin/env python3
"""Focused host-only frame-to-real-slot copy edge and ordering controls."""
import argparse
import ast
import json
from pathlib import Path
import resource
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
include = out / 'include'
include.mkdir()
(include / 'action.h').write_text('''#include <stdbool.h>\n#include <stdint.h>\n#define __xdata\ntypedef struct { uint8_t col, row; } keypos_t;\ntypedef enum { TICK_EVENT, KEY_EVENT } keyevent_type_t;\ntypedef struct { keypos_t key; uint16_t time; keyevent_type_t type; bool pressed; } keyevent_t;\n''')
# Extract the reviewed slot slice's expected rows rather than replaying its harness.
fixture = ast.parse((HERE / 'ph_vial_slot_slice_test.py').read_text())
candidates = [node.value for node in ast.walk(fixture) if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'expected' for t in node.targets)]
assert len(candidates) == 1
reference = ast.literal_eval(candidates[0])
assert len(reference) == 7
expected = []
for line in reference[1:6]:
    row = line.split()
    if row[0] == 'wait':
        expected.append('wait ' + row[-1])
    else:
        expected.append(f'{row[0]} {row[5]} {row[3]}')
assert expected == ['110 7700 1', '121 2105 1', 'wait 5', '125 2105 0', '120 2204 0']
(out / 'reference.log').write_text('\n'.join(expected) + '\n')
source = (BOARD / 'ak820_ph_slots.c').read_text()
needle = '        if (slot->state == AK820_PH_WAITING) {'
assert source.count(needle) == 1
variants = {
    'candidate': (source, []),
    'no_copy': (source, ['-DPH_MUTANT_ALIAS']),
    'no_pin': (source, ['-DPH_MUTANT_NO_PIN']),
    'retry_committed': (source, ['-DPH_MUTANT_RETRY_COMMITTED']),
    'barrier': (source.replace(needle, '        if (slot->state == AK820_PH_CLAIMED) return 0;\n' + needle), []),
    'replay': (source.replace(needle, '        if (slot->state == AK820_PH_WAITING || slot->state == AK820_PH_CLAIMED) {'), []),
}
commands = []
def no_core():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
for name, (slots, defines) in variants.items():
    slotfile = out / (name + '_slots.c')
    slotfile.write_text(slots)
    exe = out / name
    cmd = ['cc', '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=4', *defines, '-I', str(include), '-I', str(BOARD), str(HERE / 'ph_frame_queue_slice.c'), str(BOARD / 'ak820_ph_frame.c'), str(slotfile), '-o', str(exe)]
    commands.append(cmd)
    subprocess.run(cmd, check=True)
    run = subprocess.run([str(exe)], capture_output=True, text=True, timeout=5, preexec_fn=no_core)
    (out / (name + '.log')).write_text(f'exit={run.returncode}\n' + run.stdout + run.stderr)
    if name == 'candidate':
        assert run.returncode == 0, run.stderr
        assert run.stdout.splitlines() == expected, (run.stdout, expected)
        assert 'nested-failure child-committed=0 macro-effects=1 child-effects=0; no replay, drained' in run.stderr
        assert 'nested-failure child-committed=1 macro-effects=1 child-effects=1; no replay, drained' in run.stderr
        assert 'nested-failure saturated-child macro-effects=1; no replay, drained after unpin' in run.stderr
        print('PASS: reference-order no-replay edge and committed-failure cleanup')
    else:
        assert run.returncode != 0 or run.stdout.splitlines() != expected, (name, run.stdout)
        if name == 'retry_committed':
            assert run.returncode != 0 and 'check_nested_failure' in run.stderr, run.stderr
        print(f'PASS: negative control {name} rejected (exit {run.returncode})')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
