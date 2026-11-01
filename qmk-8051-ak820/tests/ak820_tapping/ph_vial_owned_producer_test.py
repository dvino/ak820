#!/usr/bin/env python3
"""Unwired owned Vial producer: source reference and pinned SDCC controls."""
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

def extract(text, signature):
    start = text.index(signature)
    end = text.index('{', start) + 1
    depth = 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
vial = (ROOT / 'quantum/vial.c').read_text()
event = extract(vial, 'static void vial_keycode_event(uint16_t keycode, bool pressed) {')
wrappers = [extract(vial, sig) for sig in ('void vial_keycode_down(uint16_t keycode) {', 'void vial_keycode_up(uint16_t keycode) {', 'void vial_keycode_tap(uint16_t keycode) {')]
ref = r'''#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#define AK820_COMPACT_TAPPING
#define QK_MOD_TAP 0x2000
#define QK_LAYER_TAP_MAX 0x4fff
#define QK_MODS_MAX 0x1fff
#define KC_TRANSPARENT 1
#define VIAL_MATRIX_MAGIC 240
#define KEY_EVENT 1
#define QS_tap_code_delay 5
#define AK820_ACTION_EXEC(e) emit(e)
typedef struct { struct { uint8_t row, col; } key; uint8_t type; bool pressed; uint16_t time; } keyevent_t;
static uint16_t g_vial_magic_keycode_override, clock_value;
static uint8_t milestones[8], n, wait_depth;
static uint16_t timer_read(void) { clock_value += 2; return clock_value; }
static void register_code16(uint16_t k) { (void)k; }
static void unregister_code16(uint16_t k) { (void)k; }
static void emit(keyevent_t e) { milestones[n++] = (e.pressed ? 0x10 : 0x20) | (g_vial_magic_keycode_override & 1); }
static void qs_wait_ms(uint16_t delay);
''' + event + '\n' + '\n'.join(wrappers) + r'''
static void qs_wait_ms(uint16_t delay) {
    if (delay != 5) return;
    milestones[n++] = 0x30 | wait_depth;
    if (++wait_depth == 1) vial_keycode_tap(0x7701);
    --wait_depth;
    milestones[n++] = 0x40 | wait_depth;
}
int main(void) { vial_keycode_tap(0x7700); for (int i = 0; i < 8; ++i) printf("%u%c", milestones[i], i == 7 ? '\n' : ' '); return 0; }
'''
keymap = (ROOT / 'quantum/keymap_common.c').read_text()
consumer = keymap[keymap.index('// translates key to keycode'):]
consumer = consumer[:consumer.index('\n}', consumer.index('uint16_t ak820_keycode_at')) + 2]
consumer = '#include "action.h"\n#include "keymap_common.h"\n#include "keymap_introspection.h"\n#include "vial.h"\n#include "encoder.h"\n' + consumer + '\n'
driver = r'''#include "ak820_ph_vial.h"
#include "keymap_common.h"
#include "vial.h"
__xdata __at (0x0f00) volatile uint8_t result[16];
__xdata uint16_t g_vial_magic_keycode_override;
static __xdata ak820_ph_frame_handle_t hogs[3];
static uint8_t marks, events, wait_depth;
static uint16_t clock_value;
bool vial_unlock_in_progress;
uint16_t timer_read(void) { clock_value += 2; return clock_value; }
uint16_t keycode_at_keymap_location(uint8_t l, uint8_t r, uint8_t c) { return 0; }
uint16_t keycode_at_encodermap_location(uint8_t l, uint8_t i, bool cw) { return 0; }
static void mark(uint8_t v) { if (marks < 8) result[marks++] = v; }
bool ak820_ph_vial_basic(ak820_ph_frame_handle_t h) __reentrant {
    ak820_ph_frame_t __xdata *f = ak820_ph_frame_get(h);
    if (!f) return false;
    result[15] = (uint8_t)f->keycode;
    mark(f->event.pressed ? 0x50 : 0x60);
    return true;
}
bool ak820_ph_vial_dispatch(ak820_ph_frame_handle_t h) __reentrant {
    ak820_ph_frame_t __xdata *f = ak820_ph_frame_get(h);
    uint16_t previous = g_vial_magic_keycode_override;
    if (!f || f->event.type != KEY_EVENT || f->event.key.row != VIAL_MATRIX_MAGIC || f->event.key.col != VIAL_MATRIX_MAGIC) return false;
    g_vial_magic_keycode_override = f->keycode;
    uint16_t resolved = ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
    if (resolved != f->keycode || (resolved != 0x7700 && resolved != 0x7701)) return false;
    mark((f->event.pressed ? 0x10 : 0x20) | (resolved & 1));
    if (events < 4) result[8 + events++] = (uint8_t)f->event.time;
#ifdef NESTED_EVENT
    if (resolved == 0x7700 && f->event.pressed) {
        if (!ak820_ph_vial_down(0x7701) || !ak820_ph_vial_up(0x7701)) return false;
        f = ak820_ph_frame_get(h);
        result[15] = f && f->keycode == 0x7700 && f->event.type == KEY_EVENT &&
            f->event.key.row == VIAL_MATRIX_MAGIC && f->event.key.col == VIAL_MATRIX_MAGIC &&
            f->event.pressed && f->event.time == 3 &&
            ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC) == 0x7700;
    }
#endif
    g_vial_magic_keycode_override = previous;
#ifdef UP_HOOK_FAIL
    if (resolved == 0x7700 && !f->event.pressed) return false;
#endif
#ifdef HOOK_FAIL
    if (resolved == 0x7700 && f->event.pressed) return false;
#endif
    return true;
}
bool ak820_ph_vial_wait(void) __reentrant {
    mark(0x30 | wait_depth);
    ++wait_depth;
#if defined(OVERFLOW_UP)
    for (uint8_t i = 0; i < 3; ++i) hogs[i] = ak820_ph_frame_reserve();
#elif !defined(NO_NEST) && !defined(BASIC_TEST) && !defined(HOOK_FAIL)
    if (wait_depth == 1 && !ak820_ph_vial_tap(0x7701)) return false;
#endif
    --wait_depth;
    mark(0x40 | wait_depth);
    return true;
}
void main(void) {
    for (uint8_t i = 0; i < 16; ++i) result[i] = 0;
#ifdef BASIC_TEST
    result[12] = ak820_ph_vial_down(QK_MOD_TAP | 4) && ak820_ph_vial_up(QK_MOD_TAP | 4);
    result[14] = ak820_ph_vial_down(QK_MOD_TAP | KC_TRANSPARENT);
#else
    result[12] = ak820_ph_vial_tap(0x7700);
#endif
#ifdef OVERFLOW_UP
    for (uint8_t i = 0; i < 3; ++i) if (hogs[i]) ak820_ph_frame_release(hogs[i]);
#endif
    for (uint8_t i = 0; i < 3; ++i) hogs[i] = ak820_ph_frame_reserve();
    ak820_ph_frame_handle_t extra = ak820_ph_frame_reserve();
    result[13] = hogs[0] && hogs[1] && hogs[2] && extra;
    for (uint8_t i = 0; i < 3; ++i) if (hogs[i]) ak820_ph_frame_release(hogs[i]);
    if (extra) ak820_ph_frame_release(extra);
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
'''
for name, text in [('reference', ref), ('consumer', consumer), ('driver', driver)]:
    (out / (name + '.c')).write_text(text)
commands = []
cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', str(out / 'reference.c'), '-o', str(out / 'reference')]
commands.append(cmd)
subprocess.run(cmd, check=True)
reference = subprocess.run([str(out / 'reference')], text=True, capture_output=True, check=True, timeout=5).stdout
(out / 'reference.log').write_text(reference)
expected = [int(x) for x in reference.split()]
assert expected == [16, 48, 17, 49, 65, 33, 64, 32]
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    t = raw[i]
    if t in ('--include', '-o'):
        i += 2
        continue
    if t.startswith('-Wp,-MD,-MF,') or t == 'quantum/action.c' or t == '-c':
        i += 1
        continue
    flags.append(t.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ))
    i += 1
assert '--xstack' not in flags
cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-c', str(BOARD / 'ak820_ph_vial.c'), '-o', str(out / 'disabled.rel')]
commands.append(cmd)
subprocess.run(cmd, cwd=ROOT, check=True, text=True)
assert '_ak820_ph_vial_down' not in (out / 'disabled.asm').read_text()
print('PASS: disabled producer exports no entry')
for name, capacity, enabled in [('disabled_cap1', 1, False), ('enabled_cap1', 1, True), ('enabled_cap2', 2, True)]:
    cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=' + str(capacity), *(['-DAK820_PH_VIAL_ENABLE'] if enabled else []), '-c', str(BOARD / 'ak820_ph_vial.c'), '-o', str(out / (name + '.rel'))]
    commands.append(cmd)
    check = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    (out / (name + '.log')).write_text(check.stdout + check.stderr)
    if enabled and capacity == 1:
        assert check.returncode != 0 and 'AK820_PH_VIAL_ENABLE requires at least two frames' in check.stderr, check.stderr
    else:
        assert check.returncode == 0, check.stderr
        asm = (out / (name + '.asm')).read_text()
        assert ('_ak820_ph_vial_down:' in asm) == enabled
print('PASS: disabled capacity 1 accepted; enabled capacity 1 rejected and capacity 2 accepted')
for variant in ('nested', 'nested_event', 'control', 'basic', 'overflow_up', 'hook_fail', 'up_hook_fail'):
    defines = {'nested_event': ['-DNESTED_EVENT', '-DNO_NEST'], 'control': ['-DNO_NEST'], 'basic': ['-DBASIC_TEST'], 'overflow_up': ['-DOVERFLOW_UP'], 'hook_fail': ['-DHOOK_FAIL'], 'up_hook_fail': ['-DUP_HOOK_FAIL', '-DNO_NEST']}.get(variant, [])
    objects = []
    for name, src in [('frame', BOARD / 'ak820_ph_frame.c'), ('vial', BOARD / 'ak820_ph_vial.c'), ('consumer', out / 'consumer.c'), ('driver', out / 'driver.c')]:
        obj = out / f'{variant}_{name}.rel'
        cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=4', '-DAK820_PH_VIAL_ENABLE', *defines, '-c', str(src), '-o', str(obj)]
        commands.append(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True, text=True)
        objects.append(obj)
    assembly = (out / f'{variant}_vial.asm').read_text()
    for name in ('ak820_ph_vial_down', 'ak820_ph_vial_up', 'ak820_ph_vial_tap'):
        assert '_' + name + ':' in assembly and not re.search('_' + name + r'_PARM_', assembly)
    assert '_event_PARM_' not in assembly
    body = assembly.split('_event:', 1)[1].split('_ak820_ph_vial_down:', 1)[0]
    assert re.search(r'lcall\s+_ak820_ph_frame_reserve', body)
    assert re.search(r'lcall\s+_ak820_ph_vial_dispatch', body)
    assert re.search(r'lcall\s+_ak820_ph_vial_basic', body)
    tap_body = assembly.split('_ak820_ph_vial_tap:', 1)[1]
    calls = [re.search(r'\b(?:lcall|ljmp)\s+_' + name, tap_body).start() for name in ('ak820_ph_vial_down', 'ak820_ph_vial_wait', 'ak820_ph_vial_up')]
    assert calls == sorted(calls)
    driver_asm = (out / f'{variant}_driver.asm').read_text()
    assert re.search(r'lcall\s+_ak820_keycode_at', driver_asm.split('_ak820_ph_vial_dispatch:', 1)[1].split('_ak820_ph_vial_wait:', 1)[0])
    cmd = [str(TOOL / 'sdcc'), '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *map(str, objects), '-o', str(out / (variant + '.ihx'))]
    commands.append(cmd)
    subprocess.run(cmd, cwd=out, check=True, text=True)
    text = (out / (variant + '.map')).read_text()
    addr = int(re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', text).group(1), 16)
    sim = subprocess.run([str(TOOL / 's51'), '-t', '51', '-c', '-', str(out / (variant + '.ihx'))], input=f'run 0 0x{addr:x}\ndump xram 0x0f00 0x0f0f\nquit\n', text=True, capture_output=True, timeout=10, check=True)
    (out / (variant + '.sim.log')).write_text(sim.stdout + sim.stderr)
    rows = [re.search(r'0x0f0' + suffix + r'\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})', sim.stdout) for suffix in ('0', '8')]
    assert all(rows), sim.stdout
    values = [int(x, 16) for row in rows for x in row.group(1).split()]
    cases = {
        'nested': expected + [3,5,7,9,1,1,0,0],
        'nested_event': [16,17,33,48,64,32,0,0,3,5,7,9,1,1,0,1],
        'control': [16,48,64,32,0,0,0,0,3,5,0,0,1,1,0,0],
        'basic': [80,96,0,0,0,0,0,0,0,0,0,0,1,1,1,4],
        'overflow_up': [16,48,64,0,0,0,0,0,3,0,0,0,0,1,0,0],
        'hook_fail': [16,0,0,0,0,0,0,0,3,0,0,0,0,1,0,0],
        'up_hook_fail': [16,48,64,32,0,0,0,0,3,5,0,0,0,1,0,0],
    }
    assert values == cases[variant], (variant, values, cases[variant])
    print(f'PASS: {variant}: {values}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
