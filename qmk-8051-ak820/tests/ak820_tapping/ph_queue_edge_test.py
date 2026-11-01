#!/usr/bin/env python3
"""Unwired queue API: host negative control and pinned-SDCC synthetic ABI."""
import argparse
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
TOOL = Path('/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-pointer-resume.phVRBT5t/tool-stage/sdcc-4.6.0/bin')
META = Path('/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-nine-link-qIQ1fYBH/build/final/main/obj_ajazz_ak820_vial/quantum/action.o.compile.json')
OBJ = '/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-nine-link-qIQ1fYBH/build/final/main/obj_ajazz_ak820_vial'
p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
include = out / 'host_include'
include.mkdir()
(include / 'action.h').write_text('''#include <stdbool.h>\n#include <stdint.h>\n#define __xdata\ntypedef struct { uint8_t col, row; } keypos_t;\ntypedef enum { TICK_EVENT, KEY_EVENT } keyevent_type_t;\ntypedef struct { keypos_t key; uint16_t time; keyevent_type_t type; bool pressed; } keyevent_t;\n''')
source = (BOARD / 'ak820_ph_queue.c').read_text()
needle = '    q->records[q->slots.tail] = *frame;'
assert source.count(needle) == 1
(out / 'mutant_queue.c').write_text(source.replace(needle, '    /* negative control: omit queue-owned event/keycode copy */'))
defines = ['-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=2', '-DAK820_PH_QUEUE_ENABLE']
commands = []
for name, queue in [('host', BOARD / 'ak820_ph_queue.c'), ('no_copy', out / 'mutant_queue.c')]:
    cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', *defines, '-I', str(include), '-I', str(BOARD), str(HERE / 'ph_queue_edge_harness.c'), str(BOARD / 'ak820_ph_frame.c'), str(BOARD / 'ak820_ph_slots.c'), str(queue), '-o', str(out / name)]
    commands.append(cmd)
    subprocess.run(cmd, check=True)
    run = subprocess.run([str(out / name)], capture_output=True, text=True, timeout=5)
    (out / (name + '.log')).write_text(f'exit={run.returncode}\n' + run.stdout + run.stderr)
    if name == 'host':
        assert run.returncode == 0, run.stderr
    else:
        assert run.returncode != 0 and 'failed line' in run.stderr, run.stderr
    print(f'PASS: {name} exit {run.returncode}')
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    token = raw[i]
    if token in ('--include', '-o'):
        i += 2
        continue
    if token.startswith('-Wp,-MD,-MF,') or token == 'quantum/action.c' or token == '-c':
        i += 1
        continue
    flags.append(token.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ))
    i += 1
assert '--xstack' not in flags
cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-c', str(BOARD / 'ak820_ph_queue.c'), '-o', str(out / 'disabled.rel')]
commands.append(cmd)
subprocess.run(cmd, cwd=ROOT, check=True, text=True)
assert '_ak820_ph_queue_enqueue' not in (out / 'disabled.asm').read_text()
objects = []
for name, src in [('frame', BOARD / 'ak820_ph_frame.c'), ('slots', BOARD / 'ak820_ph_slots.c'), ('queue', BOARD / 'ak820_ph_queue.c'), ('harness', HERE / 'ph_queue_edge_harness.c')]:
    obj = out / (name + '.rel')
    cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), *defines, '-c', str(src), '-o', str(obj)]
    commands.append(cmd)
    subprocess.run(cmd, cwd=ROOT, check=True, text=True)
    objects.append(obj)
assembly = (out / 'queue.asm').read_text()
for fn in ('enqueue', 'claim', 'record', 'finish', 'unclaim'):
    assert '_ak820_ph_queue_' + fn + ':' in assembly
    assert not re.search('_ak820_ph_queue_' + fn + r'_PARM_', assembly)
assert re.search(r'lcall\s+_ak820_ph_frame_get', assembly)
assert re.search(r'lcall\s+_ak820_ph_slots_enqueue', assembly)
assert re.search(r'lcall\s+_ak820_ph_slots_claim', assembly)
cmd = [str(TOOL / 'sdcc'), '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *map(str, objects), '-o', str(out / 'probe.ihx')]
commands.append(cmd)
subprocess.run(cmd, cwd=out, check=True, text=True)
text = (out / 'probe.map').read_text()
addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', text).group(1), 16)
sim = subprocess.run([str(TOOL / 's51'), '-t', '51', '-c', '-', str(out / 'probe.ihx')], input=f'run 0 0x{addr:x}\ndump xram 0x0f00 0x0f07\nquit\n', text=True, capture_output=True, timeout=10, check=True)
(out / 'probe.sim.log').write_text(sim.stdout + sim.stderr)
row = re.search(r'0x0f00\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})', sim.stdout)
assert row, sim.stdout
values = [int(x, 16) for x in row.group(1).split()]
assert values[:2] == [0, 0xa5], values
print(f'PASS: SDCC/s51 queue edge: {values[:2]}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
