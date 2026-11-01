#!/usr/bin/env python3
"""Source-derived seam trace and pinned-SDCC synthetic ABI check; mocks only."""
import argparse
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACTION = ROOT / 'quantum/action.c'
BOARD = ROOT / 'keyboards/ajazz/ak820'
TOOL = Path('/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-pointer-resume.phVRBT5t/tool-stage/sdcc-4.6.0/bin')
META = Path('/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-nine-link-qIQ1fYBH/build/final/main/obj_ajazz_ak820_vial/quantum/action.o.compile.json')
OBJ = '/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-nine-link-qIQ1fYBH/build/final/main/obj_ajazz_ak820_vial'

def function(text, signature):
    start = text.index(signature)
    i = text.index('{', start) + 1
    depth = 1
    while depth:
        depth += (text[i] == '{') - (text[i] == '}')
        i += 1
    return text[start:i]

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
source = ACTION.read_text()
legacy = function(source, 'void action_exec(keyevent_t event) {')
assert legacy == (HERE / 'ph_action_seam_legacy.fixture').read_text().strip()
seam = function(source, 'void ak820_ph_action_continue(')
common = r'''
#include <stdint.h>
#include <stdbool.h>
#ifndef __SDCC_mcs51
#define __xdata
#define __reentrant
#endif
#define AK820_BOARD
#define NO_DEBUG
#define NO_ACTION_TAPPING
#define NO_ACTION_ONESHOT
#define AK820_COMPACT_ONESHOT
#define AK820_COMPACT_DYNAMIC_MACRO
#define AK820_COMPACT_COMBO
#define AK820_COMPACT_TAPPING
#define AK820_COMPACT_AUTOSHIFT
#define AK820_COMBO_AUTOSHIFT
#define AK820_COMPACT_TAP_DANCE
#define AK820_COMPACT_LEADER
#define COMBO_ENABLE
#define AK820_RECORD_MEM __xdata
#define IS_NOEVENT(e) ((e).type == 0)
#define IS_EVENT(e) ((e).type != 0)
typedef struct { uint8_t col, row; } keypos_t;
typedef struct { keypos_t key; uint16_t time; uint8_t type; bool pressed; } keyevent_t;
typedef struct { uint8_t count; } tap_t;
typedef struct { keyevent_t event; tap_t tap; uint16_t keycode; } keyrecord_t;
typedef struct { keyevent_t event; keyrecord_t record; } ak820_ph_action_context_t;
static __xdata uint8_t trace[128], saved[128], n, sn, stop, nest, depth, error;
static __xdata ak820_ph_action_context_t inner;
static void mark(uint8_t x) __reentrant { trace[n++] = x; }
void ak820_ph_action_continue(ak820_ph_action_context_t __xdata *) __reentrant;
void ak820_oneshot_tick(uint16_t x) __reentrant { (void)x; mark(1); }
void ak820_dynamic_macro_task(uint16_t x) __reentrant { (void)x; mark(2); }
bool ak820_combo_tick(uint16_t x) __reentrant { (void)x; mark(3); return stop != 3; }
void ak820_tapping_discard(const keyevent_t __xdata *e) __reentrant { (void)e; mark(4); }
bool ak820_tapping_before(const keyevent_t __xdata *e) __reentrant { (void)e; mark(5); return stop != 5; }
void ak820_tap_dance_task(uint16_t x) __reentrant { (void)x; mark(6); }
bool ak820_tap_dance_before(const keyevent_t __xdata *e) __reentrant { (void)e; mark(7); return stop != 7; }
bool ak820_combo_before(const keyevent_t __xdata *e) __reentrant { (void)e; mark(8); return stop != 8; }
bool ak820_autoshift_before(const keyevent_t __xdata *e) __reentrant { (void)e; mark(9); return stop != 9; }
void clear_weak_mods(void) __reentrant { mark(10); }
bool pre_process_record_quantum(keyrecord_t __xdata *r) __reentrant { (void)r; mark(11); return stop != 11; }
bool ak820_tapping_process(keyrecord_t __xdata *r) __reentrant { (void)r; mark(12); return stop != 12; }
bool ak820_autoshift_process(keyrecord_t __xdata *r) __reentrant { (void)r; mark(13); return stop != 13; }
void process_record(keyrecord_t __xdata *r) __reentrant {
    mark(14); mark(r->event.key.row); mark(r->event.type); mark(r->event.pressed);
    if (r->tap.count || r->keycode) error = 1;
    if (nest && !depth) {
        r->keycode = 0x1234;
        depth = 1;
        inner.event.key.row = 7; inner.event.type = 1; inner.event.pressed = false;
#ifdef MUTANT_SAME_CONTEXT
        ak820_ph_action_continue((ak820_ph_action_context_t __xdata *)((char __xdata *)r - sizeof(keyevent_t)));
#else
        ak820_ph_action_continue(&inner);
#endif
        depth = 0;
        if (r->event.key.row != 4 || r->keycode != 0x1234) error = 2;
    }
}
void ak820_leader_task(uint16_t x) __reentrant { (void)x; mark(15); }
'''
driver = r'''
static __xdata ak820_ph_action_context_t ctx;
#ifdef __SDCC_mcs51
__xdata __at (0x0f00) volatile uint8_t result[2];
#endif
static bool check(void) {
    static const uint8_t stops[] = {0, 3, 5, 7, 8, 9, 11, 12, 13};
    for (uint8_t typ = 0; typ < 4; ++typ) for (uint8_t press = 0; press < 2; ++press) for (uint8_t k = 0; k < sizeof(stops); ++k) {
        ctx.event.key.row = typ + 1; ctx.event.key.col = 2; ctx.event.time = 101; ctx.event.type = typ; ctx.event.pressed = press;
        stop = stops[k]; n = 0; error = 0; action_exec(ctx.event); sn = n;
        for (uint8_t i = 0; i < n; ++i) saved[i] = trace[i];
        n = 0; ctx.record.tap.count = 0xff; ctx.record.keycode = 0xffff;
        ak820_ph_action_continue(&ctx);
        if (error || n != sn) return false;
        for (uint8_t i = 0; i < n; ++i) if (trace[i] != saved[i]) return false;
    }
    stop = 0; nest = 1; n = 0; error = 0; ctx.event.key.row = 4; ctx.event.type = 1; ctx.event.pressed = true;
    ak820_ph_action_continue(&ctx);
    return !error && ctx.event.key.row == 4 && ctx.record.event.key.row == 4 && ctx.record.keycode == 0x1234;
}
void main(void) {
    bool ok = check();
#ifdef __SDCC_mcs51
    result[0] = ok ? 0xa5 : 0x5a;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
#else
    if (!ok) __builtin_trap();
#endif
}
'''
probe = common + '\n' + legacy + '\n' + seam + '\n' + driver
(out / 'probe.c').write_text(probe)
commands = []
def run(cmd, **kw):
    commands.append([str(x) for x in cmd])
    return subprocess.run([str(x) for x in cmd], check=True, text=True, **kw)

for mutant in (False, True):
    name = 'mutant' if mutant else 'owned'
    asm = out / (name + '.asm')
    run([TOOL / 'sdcc', '-mmcs51', '--model-large', '--std-sdcc11', *(['-DMUTANT_SAME_CONTEXT'] if mutant else []), '-c', out / 'probe.c', '-o', out / (name + '.rel')])
    text = asm.read_text()
    body = text.split('_ak820_ph_action_continue:', 1)[1].split('_check:', 1)[0]
    assert '_action_exec_PARM_1' not in body and '_ak820_ph_action_continue_PARM_' not in text
    image = out / (name + '.ihx')
    run([TOOL / 'sdcc', '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', out / (name + '.rel'), '-o', image], cwd=out)
    addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', (out / (name + '.map')).read_text()).group(1), 16)
    sim = run([TOOL / 's51', '-t', '51', '-c', '-', image], input=f'run 0 0x{addr:x}\ndump xram 0x0f00 0x0f01\nquit\n', capture_output=True, timeout=15)
    (out / (name + '.sim.log')).write_text(sim.stdout + sim.stderr)
    row = re.search(r'0x0f00\s+([0-9a-fA-F]{2})', sim.stdout)
    assert row and int(row.group(1), 16) == (0x5a if mutant else 0xa5), sim.stdout
print('PASS: 72 source-derived differential traces and nested-context negative control (mock hooks)')

# Compile the real action translation unit, with and without the guard. The
# actual legacy body must remain byte-identical to the retained pre-change body.
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    tok = raw[i]
    if tok == '-o': i += 2; continue
    if tok.startswith('-Wp,-MD,-MF,') or tok in ('quantum/action.c', '-c'): i += 1; continue
    flags.append(tok.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ)); i += 1
assert '--xstack' not in flags
block = '#ifdef AK820_PH_ACTION_SEAM\n' + seam + '\n\n#endif\n'
assert source.count(block) == 1
(out / 'baseline.c').write_text(source.replace(block, ''))
for name, enabled in [('baseline', False), ('off', False), ('on', True)]:
    src = out / 'baseline.c' if name == 'baseline' else 'quantum/action.c'
    run([TOOL / 'sdcc', *flags, *(['-DAK820_PH_ACTION_SEAM'] if enabled else []), '-S', src, '-o', out / (name + '.asm')], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    asm = (out / (name + '.asm')).read_text()
    assert ('_ak820_ph_action_continue:' in asm) == enabled
    assert '_action_exec:' in asm and '_action_exec_PARM_1' in asm
# Compare the actual off-path instructions against the pre-seam translation
# unit. Normalize only SDCC's internal local-object ordinal.
def instructions(text):
    body = text.split('_action_exec:', 1)[1].split('_ak820_action_exec:', 1)[0]
    body = body.split('_ak820_ph_action_continue:', 1)[0]
    return [re.sub(r'(_action_exec_record_\d+_)\d+', r'\1N', s) for line in body.splitlines() if (s := line.strip()) and not s.startswith((';', '.', '_')) and not re.match(r'\d+\$:', s)]
assert instructions((out / 'off.asm').read_text()) == instructions((out / 'baseline.asm').read_text())

# Compile the actual scoped pool separately against a synthetic consumer.
frame = (BOARD / 'ak820_ph_frame.c').read_text()
assert frame.count('action_contexts[i].event.key.row = row;') == 1
(out / 'mutant_frame.c').write_text(frame.replace('action_contexts[i].event.key.row = row;', 'action_contexts[i].event.key.row = 0;'))
defs = ['-DAK820_PH_ACTION_SEAM', '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-I' + str(BOARD)]
run([TOOL / 'sdcc', *flags, *defs[1:], '-S', BOARD / 'ak820_ph_frame.c', '-o', out / 'frame_off.asm'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
frame_off = (out / 'frame_off.asm').read_text()
assert '_ak820_ph_action_run' not in frame_off and '_action_contexts' not in frame_off
for name in ('pool', 'pool_mutant'):
    frame_src = BOARD / 'ak820_ph_frame.c' if name == 'pool' else out / 'mutant_frame.c'
    objects = []
    for unit, src in [('frame', frame_src), ('driver', HERE / 'ph_action_seam_pool_sdcc.c')]:
        obj = out / (name + '_' + unit + '.rel')
        run([TOOL / 'sdcc', *flags, *defs, '-c', src, '-o', obj], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        objects.append(obj)
    pool_asm = (out / (name + '_frame.asm')).read_text()
    body = pool_asm.split('_ak820_ph_action_run:', 1)[1]
    assert '_ak820_ph_action_run_PARM_' not in pool_asm
    assert body.index('_timer_read') < body.index('_ak820_ph_action_continue')
    image = out / (name + '.ihx')
    run([TOOL / 'sdcc', '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *objects, '-o', image], cwd=out, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', (out / (name + '.map')).read_text()).group(1), 16)
    sim = run([TOOL / 's51', '-t', '51', '-c', '-', image], input=f'run 0 0x{addr:x}\ndump xram 0x0f00 0x0f01\nquit\n', capture_output=True, timeout=15)
    (out / (name + '.sim.log')).write_text(sim.stdout + sim.stderr)
    match = re.search(r'0x0f00\s+([0-9a-fA-F]{2})\s+([0-9a-fA-F]{2})', sim.stdout)
    assert match and int(match.group(1), 16) == (0xa5 if name == 'pool' else 0x5a) and int(match.group(2), 16) == 20, sim.stdout
print('PASS: actual scoped context pool nested, exhausted and reused; wrong-row mutant rejected')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print('PASS: original action_exec body unchanged; actual guarded translation-unit assembly inspected')
