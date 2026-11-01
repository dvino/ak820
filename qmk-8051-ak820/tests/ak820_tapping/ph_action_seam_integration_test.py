#!/usr/bin/env python3
"""Pinned synthetic integration: real frame pool and tapping, extracted seam.

Nested entry is deliberately injected through mocked hooks, not a reachability,
IRQ, resource, cancellation or full-firmware qualification claim.
"""
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
source = (ROOT / 'quantum/action.c').read_text()
start = source.index('void ak820_ph_action_continue(')
end = source.index('\n#endif\n\n#if defined(AK820_BOARD)', start)
prefix = source[:source.index('void action_exec(keyevent_t event) {')]
(out / 'continuation.c').write_text(prefix + source[start:end] + '\n')
frame = (BOARD / 'ak820_ph_frame.c').read_text()
needle = 'if (!action_active[i]) {'
assert frame.count(needle) == 1
(out / 'mutant_frame.c').write_text(frame.replace(needle, 'if (i == 0) {'))
tapping = (BOARD / 'ak820_tapping.c').read_text()
duplicate_guard = 'if (event->pressed == ((source_state_get(id) & SOURCE_ACTIVE) != 0)) return false;'
assert tapping.count(duplicate_guard) == 1
(out / 'mutant_tapping.c').write_text(tapping.replace(duplicate_guard, duplicate_guard.replace('return false;', 'return true;')))
# Diagnostic ABI control only; this is not a production fix or qualification.
fix = out / 'reentrant'
fix.mkdir()
header = (BOARD / 'ak820_tapping.h').read_text()
decl = 'bool ak820_tapping_before(const keyevent_t AK820_STATE_MEM *event);'
impl = decl[:-1] + ' {'
assert header.count(decl) == 1 and tapping.count(impl) == 1
(fix / 'ak820_tapping.h').write_text(header.replace(decl, decl[:-1] + ' __reentrant;'))
(fix / 'tapping.c').write_text(tapping.replace(impl, decl[:-1] + ' __reentrant {'))
continuation = (out / 'continuation.c').read_text()
assert continuation.count('#    include "ak820_tapping.h"') == 1
(fix / 'continuation.c').write_text(continuation.replace('#    include "ak820_tapping.h"', '#    include "' + str(fix / 'ak820_tapping.h') + '"'))
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    tok = raw[i]
    if tok == '-o': i += 2; continue
    if tok.startswith('-Wp,-MD,-MF,') or tok in ('quantum/action.c', '-c'): i += 1; continue
    flags.append(tok.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ)); i += 1
assert '--xstack' not in flags
defs = ['-DAK820_PH_ACTION_SEAM', '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-I' + str(BOARD)]
commands = []
def run(cmd, **kw):
    commands.append([str(x) for x in cmd])
    return subprocess.run([str(x) for x in cmd], check=True, text=True, **kw)

observed = {}
for name, case, mutant in [('control', 0, None), ('nested_tapping', 1, None), ('nested_record', 2, None), ('reuse_mutant', 2, 'pool'), ('duplicate_mutant', 0, 'duplicate'), ('reentrant_control', 1, 'reentrant')]:
    objects = []
    frame_src = out / 'mutant_frame.c' if mutant == 'pool' else BOARD / 'ak820_ph_frame.c'
    tap_src = out / 'mutant_tapping.c' if mutant == 'duplicate' else fix / 'tapping.c' if mutant == 'reentrant' else BOARD / 'ak820_tapping.c'
    continuation_src = fix / 'continuation.c' if mutant == 'reentrant' else out / 'continuation.c'
    for unit, src in [('continuation', continuation_src), ('frame', frame_src), ('tapping', tap_src), ('driver', HERE / 'ph_action_seam_integration_sdcc.c')]:

        obj = out / (name + '_' + unit + '.rel')
        result = run([TOOL / 'sdcc', *flags, *defs, '-DTEST_CASE=' + str(case), '-c', src, '-o', obj], cwd=ROOT, capture_output=True)
        (out / (name + '_' + unit + '.compile.log')).write_text(result.stdout + result.stderr)
        objects.append(obj)
    asm = (out / (name + '_continuation.asm')).read_text()
    assert '_ak820_ph_action_continue:' in asm and '_ak820_ph_action_continue_PARM_' not in asm
    assert '_action_exec_PARM_1' not in asm
    tapasm = (out / (name + '_tapping.asm')).read_text()
    assert '_ak820_tapping_before:' in tapasm and '_ak820_tapping_process:' in tapasm
    before = tapasm.split('_ak820_tapping_before:', 1)[1].split('_ak820_tapping_process:', 1)[0]
    if mutant != 'reentrant':
        pointer = re.search(r'_ak820_tapping_before_event_\d+_\d+', before).group()
        assert before.index(pointer) < before.index('lcall\t_commit_pending') < before.rindex(pointer)
    else:
        assert not re.search(r'_ak820_tapping_before_event_\d+_\d+', before)
    image = out / (name + '.ihx')
    link = run([TOOL / 'sdcc', '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *objects, '-o', image], cwd=out, capture_output=True)
    (out / (name + '.link.log')).write_text(link.stdout + link.stderr)
    addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', (out / (name + '.map')).read_text()).group(1), 16)
    sim = run([TOOL / 's51', '-t', '51', '-c', '-', image], input=f'run 0 0x{addr:x}\ndump xram 0x0e00 0x0e3f\nquit\n', capture_output=True, timeout=15)
    (out / (name + '.sim.log')).write_text(sim.stdout + sim.stderr)
    values = []
    for offset in range(0, 64, 8):
        row = re.search(r'0x%04x\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})' % (0x0e00 + offset), sim.stdout)
        assert row, sim.stdout
        values.extend(int(x, 16) for x in row.group(1).split())
    assert values[0] == 0xa5 and values[2] <= 60 and values[3] == 0, (name, values)
    observed[name] = values
    print(name, values[:4], [hex(x) for x in values[4:4 + values[2]]])

def segment(name, first, last):
    values = observed[name]
    trace = values[4:4 + values[2]]
    return trace[trace.index(first) + 1:trace.index(last)]

control_trace = [0xa1, 0x11, 0x12, 0x13, 0x16, 0x21,
                 0xa2, 0x11, 0x12, 0x31, 0x13, 0x16, 0x22, 0x14, 0x42,
                 0xb2, 0x11, 0x12,
                 0xc2, 0x11, 0x12, 0x13, 0x22, 0x14, 0x62,
                 0xc1, 0x11, 0x12, 0x13, 0x21, 0x32]
assert observed['control'][4:4 + observed['control'][2]] == control_trace
for name in ('control', 'nested_tapping', 'nested_record', 'duplicate_mutant', 'reentrant_control'):
    assert observed[name][1] == 0, (name, observed[name])
assert observed['reuse_mutant'][1] == 2
assert 0x42 in segment('control', 0xa2, 0xb2)
assert 0x42 not in segment('control', 0xb2, 0xc2)
assert 0x42 not in segment('nested_tapping', 0xa2, 0xb2)
assert segment('nested_tapping', 0xa2, 0xb2) == [0x11, 0x12, 0x31, 0x11, 0x12, 0x13, 0x23, 0x14, 0x63]
assert 0x42 in segment('nested_tapping', 0xb2, 0xc2)
assert segment('reentrant_control', 0xa2, 0xb2) == [0x11, 0x12, 0x31, 0x11, 0x12, 0x13, 0x23, 0x14, 0x63, 0x13, 0x16, 0x22, 0x14, 0x42]
assert 0x42 not in segment('reentrant_control', 0xb2, 0xc2)
assert 0x42 in segment('nested_record', 0xa2, 0xb2)
assert 0x43 in segment('nested_record', 0xa2, 0xb2)
assert 0x42 not in segment('nested_record', 0xb2, 0xc2)
assert 0x42 in segment('duplicate_mutant', 0xb2, 0xc2)
for name in ('control', 'nested_tapping', 'nested_record'):
    assert 0x62 in segment(name, 0xc2, 0xc1)
    assert 0x32 in observed[name][4:4 + observed[name][2]]
print('PASS: normal ordering, scoped lifetime, duplicate and slot-reuse mutants')
print('COUNTEREXAMPLE: constructed nested tapping release suppresses original B press and admits its duplicate; reentrant-only diagnostic restores these outcomes')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
