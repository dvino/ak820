#!/usr/bin/env python3
"""Unwired synchronous Vial frame experiment; not production PH or cancellation."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
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
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=False)
out = a.out.resolve()
vial = (ROOT / 'quantum/vial.c').read_text()
keymap = (ROOT / 'quantum/keymap_common.c').read_text()
event = extract(vial, 'static void vial_keycode_event(uint16_t keycode, bool pressed) {')
# The producer body remains source-derived; only its ingress and event handoff change.
event = event.replace('static void vial_keycode_event(uint16_t keycode, bool pressed) {', '''void candidate_dispatch(uint8_t slot) __reentrant {
    uint16_t keycode = slot ? candidate_code1 : candidate_code0;
    bool pressed = slot ? candidate_pressed1 : candidate_pressed0;
    uint16_t previous = g_vial_magic_keycode_override;''', 1)
assert event.count('AK820_ACTION_EXEC(dummy_event);') == 1
event = event.replace('AK820_ACTION_EXEC(dummy_event);', '''candidate_events[slot] = dummy_event;
#ifndef NO_TAP_SNAPSHOT
        if (candidate_tap_depth && candidate_tap_pending[candidate_tap_depth - 1]) {
            candidate_tap_events[candidate_tap_depth - 1] = dummy_event;
            candidate_tap_pending[candidate_tap_depth - 1] = 0;
        }
#endif
        candidate_consume(&candidate_events[slot]);''')
# Original early return occurs before the global override is modified.
pos = event.rfind('}')
event = event[:pos] + '    g_vial_magic_keycode_override = previous;\n' + event[pos:]
producer = r'''#include "action.h"
#include "vial.h"
#ifndef AK820_PH_EXPERIMENTAL_TEST
#error test-only, not a production configuration
#endif
void register_code16(uint16_t code);
void unregister_code16(uint16_t code);
void candidate_consume(const keyevent_t __xdata *event) __reentrant;
uint16_t g_vial_magic_keycode_override;
__data uint8_t candidate_depth, candidate_overflow;
__data uint16_t candidate_code0, candidate_code1;
__data uint8_t candidate_pressed0, candidate_pressed1;
__xdata keyevent_t candidate_events[2], candidate_tap_events[2];
__data uint8_t candidate_tap_depth, candidate_tap_pending[2];
__xdata uint16_t candidate_tap_codes[2];
''' + event + r'''
void candidate_reserve(void) __naked {
    __asm
        mov a,_candidate_depth
        jz 00001$
        cjne a,#1,00003$
        mov _candidate_depth,#2
        mov _candidate_code1,dpl
        mov (_candidate_code1 + 1),dph
        mov _candidate_pressed1,b
        mov dpl,#1
        sjmp 00002$
    00001$:
        mov _candidate_depth,#1
        mov _candidate_code0,dpl
        mov (_candidate_code0 + 1),dph
        mov _candidate_pressed0,b
        mov dpl,#0
    00002$:
#ifndef UNSAFE_ABI
        push ar0
        push ar1
        push ar2
        push ar3
        push ar4
        push ar5
        push ar6
        push ar7
#endif
        lcall _candidate_dispatch
#ifndef UNSAFE_ABI
        pop ar7
        pop ar6
        pop ar5
        pop ar4
        pop ar3
        pop ar2
        pop ar1
        pop ar0
#endif
        dec _candidate_depth
        ret
    00003$:
        mov _candidate_overflow,#1
        ret
    __endasm;
}
void vial_keycode_down(uint16_t keycode) __naked {
    keycode;
    __asm
        mov b,#1
        ljmp _candidate_reserve
    __endasm;
}
void vial_keycode_up(uint16_t keycode) __naked {
    keycode;
    __asm
        mov b,#0
        ljmp _candidate_reserve
    __endasm;
}
'''
# The original tap body is retained; this experimental name uses a reentrant ABI.
tap = extract(vial, 'void vial_keycode_tap(uint16_t keycode) {')
tap = tap.replace('void vial_keycode_tap(uint16_t keycode)', 'void candidate_vial_tap_body(uint16_t keycode) __reentrant', 1)
producer += '\n#define QS_tap_code_delay 5\nvoid qs_wait_ms(uint16_t delay);\n' + tap + r'''
void candidate_vial_tap(uint16_t keycode) __reentrant {
    uint8_t slot = candidate_tap_depth;
    if (slot >= 2) { candidate_overflow = 1; return; }
    ++candidate_tap_depth;
    candidate_tap_codes[slot] = keycode;
    candidate_tap_pending[slot] = 1;
    candidate_vial_tap_body(candidate_tap_codes[slot]);
    --candidate_tap_depth;
}
'''
consumer = keymap[keymap.index('// translates key to keycode'):]
consumer = consumer[:consumer.index('\n}', consumer.index('uint16_t ak820_keycode_at')) + 2]
consumer = '#include "action.h"\n#include "keymap_common.h"\n#include "keymap_introspection.h"\n#include "vial.h"\n#include "encoder.h"\n' + consumer + '\n'
driver = r'''#include "action.h"
#include "keymap_common.h"
#include "vial.h"
extern __data uint8_t candidate_depth, candidate_overflow, candidate_tap_depth;
extern __xdata keyevent_t candidate_tap_events[2];
extern __xdata uint16_t candidate_tap_codes[2];
void vial_keycode_down(uint16_t keycode);
void vial_keycode_up(uint16_t keycode);
void candidate_vial_tap(uint16_t keycode) __reentrant;
__xdata __at (0x0f00) volatile uint8_t result[16];
bool vial_unlock_in_progress;
static uint16_t clock_value;
static uint8_t milestone_count, event_count, wait_depth;
uint16_t timer_read(void) { clock_value += 2; return clock_value; }
void register_code16(uint16_t code) { (void)code; }
void unregister_code16(uint16_t code) { (void)code; }
uint16_t keycode_at_keymap_location(uint8_t layer, uint8_t row, uint8_t col) { return 0; }
uint16_t keycode_at_encodermap_location(uint8_t layer, uint8_t idx, bool cw) { return 0; }
static void mark(uint8_t value) { if (milestone_count < 8) result[milestone_count++] = value; }
void qs_wait_ms(uint16_t delay) {
    if (delay != 5) { result[15] = 0xee; return; }
    mark(0x30 | wait_depth);
    ++wait_depth;
#ifndef NO_NEST
    if (wait_depth == 1) candidate_vial_tap(0x7701);
#endif
    --wait_depth;
    if (!wait_depth) {
        if (candidate_tap_codes[0] == 0x7700 && candidate_tap_events[0].type == KEY_EVENT &&
            candidate_tap_events[0].key.row == VIAL_MATRIX_MAGIC && candidate_tap_events[0].key.col == VIAL_MATRIX_MAGIC &&
            candidate_tap_events[0].pressed && candidate_tap_events[0].time == 3) result[15] = 3;
        else result[15] = 0xee;
    }
    mark(0x40 | wait_depth);
}
void candidate_consume(const keyevent_t __xdata *event) __reentrant {
    uint16_t resolved = ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
    if (resolved != 0x7700 && resolved != 0x7701) { result[15] = 0xef; return; }
    mark((event->pressed ? 0x10 : 0x20) | (uint8_t)(resolved & 1));
    if (event_count < 4) result[8 + event_count++] = (uint8_t)event->time;
#ifdef FORCE_OVERFLOW
    if (event->pressed && resolved == 0x7700) vial_keycode_down(0x7701);
    if (event->pressed && resolved == 0x7701) vial_keycode_down(0x7702);
#endif
}
void main(void) {
    for (uint8_t i = 0; i < 16; ++i) result[i] = 0;
#ifdef FORCE_OVERFLOW
    vial_keycode_down(0x7700);
#else
    candidate_vial_tap(0x7700);
#endif
    result[12] = candidate_depth | candidate_tap_depth;
    result[13] = candidate_overflow;
    result[14] = 0xa5;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
'''
# Native C reference runs the exact original tap body with instrumented callbacks.
ref_tap = extract(vial, 'void vial_keycode_tap(uint16_t keycode) {')
ref = r'''#include <stdint.h>
#include <stdio.h>
#define QS_tap_code_delay 5
static uint8_t events[8], count, depth;
void vial_keycode_down(uint16_t k) { events[count++] = 0x10 | (k & 1); }
void vial_keycode_up(uint16_t k) { events[count++] = 0x20 | (k & 1); }
void vial_keycode_tap(uint16_t k);
void qs_wait_ms(uint16_t delay) {
    if (delay != 5) return;
    events[count++] = 0x30 | depth;
    if (++depth == 1) vial_keycode_tap(0x7701);
    --depth;
    events[count++] = 0x40 | depth;
}
''' + ref_tap + r'''
int main(void) { vial_keycode_tap(0x7700); for (int i = 0; i < 8; ++i) printf("%u%c", events[i], i == 7 ? '\n' : ' '); return 0; }
'''
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
for name, text in [('producer', producer), ('consumer', consumer), ('driver', driver), ('reference', ref)]:
    (out / (name + '.c')).write_text(text)
commands = []
cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', str(out / 'reference.c'), '-o', str(out / 'reference')]
commands.append(cmd)
subprocess.run(cmd, check=True)
reference = subprocess.run([str(out / 'reference')], text=True, capture_output=True, check=True, timeout=5).stdout
(out / 'reference.log').write_text(reference)
expected_order = [int(x) for x in reference.split()]
assert expected_order == [0x10, 0x30, 0x11, 0x31, 0x41, 0x21, 0x40, 0x20]
assert '--xstack' not in flags
for variant in ('nested', 'control', 'unsafe', 'no_snapshot', 'overflow'):
    objects = []
    defines = {'control': ['-DNO_NEST'], 'unsafe': ['-DUNSAFE_ABI'], 'no_snapshot': ['-DNO_TAP_SNAPSHOT'], 'overflow': ['-DFORCE_OVERFLOW']}.get(variant, [])
    for name in ('producer', 'consumer', 'driver'):
        obj = out / f'{variant}_{name}.rel'
        cmd = [str(TOOL / 'sdcc'), *flags, '-DAK820_PH_EXPERIMENTAL_TEST', *defines, '-c', str(out / (name + '.c')), '-o', str(obj)]
        commands.append(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True, text=True)
        objects.append(obj)
    prod_asm = (out / f'{variant}_producer.asm').read_text()
    reserve = prod_asm.split('_candidate_reserve:', 1)[1].split('_vial_keycode_down:', 1)[0]
    assert reserve.index('mov _candidate_depth,#1') < reserve.index('mov _candidate_code0,dpl')
    assert reserve.index('mov _candidate_depth,#2') < reserve.index('mov _candidate_code1,dpl')
    assert 'lcall _candidate_dispatch' in reserve and 'mov _candidate_overflow,#1' in reserve
    assert ('push ar6' in reserve and 'pop ar6' in reserve and 'push ar7' in reserve and 'pop ar7' in reserve) == (variant != 'unsafe')
    assert 'ljmp _candidate_reserve' in prod_asm.split('_vial_keycode_down:', 1)[1].split('_vial_keycode_up:', 1)[0]
    assert 'ljmp _candidate_reserve' in prod_asm.split('_vial_keycode_up:', 1)[1].split('_candidate_vial_tap_body:', 1)[0]
    dispatch = prod_asm.split('_candidate_dispatch:', 1)[1].split('_candidate_reserve:', 1)[0]
    assert re.search(r'lcall\s+_candidate_consume', dispatch) and '_action_exec_PARM_1' not in dispatch
    tap_asm = prod_asm.split('_candidate_vial_tap_body:', 1)[1].split('_candidate_vial_tap:', 1)[0]
    calls = [re.search(r'\b(?:lcall|ljmp)\s+' + name + r'\b', tap_asm).start() for name in ('_vial_keycode_down', '_qs_wait_ms', '_vial_keycode_up')]
    assert calls == sorted(calls)
    actual = (out / f'{variant}_consumer.asm').read_text().split('_ak820_keycode_at:', 1)[1]
    assert '_g_vial_magic_keycode_override' in actual
    driver_asm = (out / f'{variant}_driver.asm').read_text()
    assert re.search(r'lcall\s+_ak820_keycode_at', driver_asm.split('_candidate_consume:', 1)[1].split('_main:', 1)[0])
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
    if variant == 'nested':
        assert values == expected_order + [3, 5, 7, 9, 0, 0, 0xa5, 3], values
    elif variant == 'control':
        assert values == [0x10, 0x30, 0x40, 0x20, 0, 0, 0, 0, 3, 5, 0, 0, 0, 0, 0xa5, 3], values
    elif variant == 'unsafe':
        assert values[:8] != expected_order and values[7] != 0x20, values
        assert values[12:15] == [0, 0, 0xa5], values
    elif variant == 'no_snapshot':
        assert values == expected_order + [3, 5, 7, 9, 0, 0, 0xa5, 0xee], values
    else:
        assert values == [0x10, 0x11, 0, 0, 0, 0, 0, 0, 3, 5, 0, 0, 0, 1, 0xa5, 0], values
    print(f'PASS: {variant}: {values}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
