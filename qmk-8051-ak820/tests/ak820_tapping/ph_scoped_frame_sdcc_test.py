#!/usr/bin/env python3
"""Pinned synthetic SDCC ABI and s51 check of scoped staging consumers."""
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
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    token = raw[i]
    if token in ('--include', '-o'):
        i += 2
        continue
    if token.startswith('-Wp,-MD,-MF,') or token in ('quantum/action.c', '-c'):
        i += 1
        continue
    flags.append(token.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ))
    i += 1
assert '--xstack' not in flags
defines = ['-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-DAK820_PH_SCOPED_ENABLE', '-DAK820_PH_VIAL_ENABLE', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=2', '-DAK820_PH_QUEUE_ENABLE']
commands = []
for name in ('frame', 'vial', 'queue'):
    obj = out / ('legacy_' + name + '.rel')
    cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), *[d for d in defines if d != '-DAK820_PH_SCOPED_ENABLE'], '-c', str(BOARD / ('ak820_ph_' + name + '.c')), '-o', str(obj)]
    commands.append(cmd)
    subprocess.run(cmd, cwd=ROOT, check=True)
    assert '_ak820_ph_scoped_' not in (out / ('legacy_' + name + '.asm')).read_text()
    assert '_ak820_ph_queue_enqueue_scoped' not in (out / ('legacy_' + name + '.asm')).read_text()
objects = []
for name in ('frame', 'slots', 'queue', 'vial', 'driver'):
    src = HERE / 'ph_scoped_frame_sdcc.c' if name == 'driver' else BOARD / ('ak820_ph_' + name + '.c')
    obj = out / (name + '.rel')
    cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), *defines, '-c', str(src), '-o', str(obj)]
    commands.append(cmd)
    subprocess.run(cmd, cwd=ROOT, check=True)
    objects.append(obj)
for name, symbols in {'frame': ('ak820_ph_scoped_run',), 'vial': ('ak820_ph_scoped_consume', 'ak820_ph_scoped_vial_down', 'ak820_ph_scoped_vial_up', 'ak820_ph_scoped_vial_tap'), 'queue': ('ak820_ph_queue_enqueue_scoped',)}.items():
    asm = (out / (name + '.asm')).read_text()
    for symbol in symbols:
        assert '_' + symbol + ':' in asm
        assert not re.search('_' + symbol + r'_PARM_', asm), symbol
cmd = [str(TOOL / 'sdcc'), '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *map(str, objects), '-o', str(out / 'probe.ihx')]
commands.append(cmd)
subprocess.run(cmd, cwd=out, check=True)
addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', (out / 'probe.map').read_text()).group(1), 16)
sim = subprocess.run([str(TOOL / 's51'), '-t', '51', '-c', '-', str(out / 'probe.ihx')], input=f'run 0 0x{addr:x}\ndump xram 0x0f00 0x0f07\nquit\n', text=True, capture_output=True, timeout=15, check=True)
(out / 'probe.sim.log').write_text(sim.stdout + sim.stderr)
row = re.search(r'0x0f00\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})', sim.stdout)
assert row, sim.stdout
values = [int(x, 16) for x in row.group(1).split()]
assert values[:4] == [0xa5, 0x10, 0x11, 0x20], values
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print('PASS: pinned SDCC/s51 scoped nested Vial and copied queue', values[:4])
