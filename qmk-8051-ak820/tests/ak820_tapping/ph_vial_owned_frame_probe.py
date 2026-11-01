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
event = event.replace('AK820_ACTION_EXEC(dummy_event);', 'candidate_events[slot] = dummy_event;\n        candidate_consume(&candidate_events[slot]);')
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
__xdata keyevent_t candidate_events[2];
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
        lcall _candidate_dispatch
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
# Extract the original complete board/non-board consumer preprocessor block.
consumer = keymap[keymap.index('// translates key to keycode'):]
consumer = consumer[:consumer.index('\n}', consumer.index('uint16_t ak820_keycode_at')) + 2]
consumer = '#include "action.h"\n#include "keymap_common.h"\n#include "keymap_introspection.h"\n#include "vial.h"\n#include "encoder.h"\n' + consumer + '\n'
driver = r'''#include "action.h"
#include "keymap_common.h"
#include "vial.h"
extern __data uint8_t candidate_depth, candidate_overflow;
void vial_keycode_down(uint16_t keycode);
void vial_keycode_up(uint16_t keycode);
__xdata __at (0x0f00) volatile uint8_t result[16];
bool vial_unlock_in_progress;
static uint16_t clock_value;
uint16_t timer_read(void) { clock_value += 2; return clock_value; }
void register_code16(uint16_t code) { (void)code; }
void unregister_code16(uint16_t code) { (void)code; }
uint16_t keycode_at_keymap_location(uint8_t layer, uint8_t row, uint8_t col) { return 0; }
uint16_t keycode_at_encodermap_location(uint8_t layer, uint8_t idx, bool cw) { return 0; }
void candidate_consume(const keyevent_t __xdata *event) __reentrant {
    uint16_t resolved = ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
    if (resolved == 0x7700 && event->pressed) {
        result[0] = (uint8_t)resolved;
        result[1] = (uint8_t)(resolved >> 8);
        result[2] = (uint8_t)event->time;
#ifndef NO_NEST
        vial_keycode_down(0x7701);
        vial_keycode_up(0x7701);
#endif
        resolved = ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
        result[3] = (uint8_t)resolved;
        result[4] = (uint8_t)(resolved >> 8);
        result[5] = (uint8_t)event->time;
    } else if (resolved == 0x7701) {
        if (event->pressed) {
            result[6] = (uint8_t)resolved;
            result[7] = (uint8_t)event->time;
#ifdef FORCE_OVERFLOW
            vial_keycode_down(0x7702);
            result[15] = (uint8_t)ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
#endif
        } else {
            result[8] = (uint8_t)resolved;
            result[9] = (uint8_t)event->time;
        }
    } else if (resolved == 0x7700 && !event->pressed) {
        result[10] = (uint8_t)resolved;
        result[11] = (uint8_t)(resolved >> 8);
    }
}
void main(void) {
    for (uint8_t i = 0; i < 16; ++i) result[i] = 0;
    vial_keycode_down(0x7700);
    vial_keycode_up(0x7700);
    result[12] = candidate_depth;
    result[13] = candidate_overflow;
    result[14] = 0xa5;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
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
for name, text in [('producer', producer), ('consumer', consumer), ('driver', driver)]:
    (out / (name + '.c')).write_text(text)
commands = []
assert '--xstack' not in flags
for variant in ('nested', 'control', 'overflow'):
    objects = []
    for name in ('producer', 'consumer', 'driver'):
        obj = out / f'{variant}_{name}.rel'
        defines = ['-DNO_NEST'] if variant == 'control' else (['-DFORCE_OVERFLOW'] if variant == 'overflow' else [])
        cmd = [str(TOOL / 'sdcc'), *flags, '-DAK820_PH_EXPERIMENTAL_TEST', *defines, '-c', str(out / (name + '.c')), '-o', str(obj)]
        commands.append(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True, text=True)
        objects.append(obj)
    prod_asm = (out / f'{variant}_producer.asm').read_text()
    reserve = prod_asm.split('_candidate_reserve:', 1)[1].split('_vial_keycode_down:', 1)[0]
    assert reserve.index('mov _candidate_depth,#1') < reserve.index('mov _candidate_code0,dpl')
    assert reserve.index('mov _candidate_depth,#2') < reserve.index('mov _candidate_code1,dpl')
    assert 'lcall _candidate_dispatch' in reserve
    down = prod_asm.split('_vial_keycode_down:', 1)[1].split('_vial_keycode_up:', 1)[0]
    up = prod_asm.split('_vial_keycode_up:', 1)[1]
    assert 'ljmp _candidate_reserve' in down and 'ljmp _candidate_reserve' in up
    dispatch = prod_asm.split('_candidate_dispatch:', 1)[1].split('_candidate_reserve:', 1)[0]
    assert re.search(r'lcall\s+_candidate_consume', dispatch)
    assert '_action_exec_PARM_1' not in dispatch
    consumer_asm = (out / f'{variant}_consumer.asm').read_text().split('_ak820_keycode_at:', 1)[1]
    assert '_g_vial_magic_keycode_override' in consumer_asm
    driver_asm = (out / f'{variant}_driver.asm').read_text().split('_candidate_consume:', 1)[1].split('_main:', 1)[0]
    assert len(re.findall(r'lcall\s+_ak820_keycode_at', driver_asm)) >= 2
    assert (bool(re.search(r'lcall\s+_vial_keycode_down', driver_asm))) == (variant != 'control')
    assert (bool(re.search(r'lcall\s+_vial_keycode_up', driver_asm))) == (variant != 'control')
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
    expected = [0,119,3,0,119,3,0,0,0,0,0,119,0,0,165,0] if variant == 'control' else [0,119,3,0,119,3,1,5,1,7,0,119,0,int(variant == 'overflow'),165,int(variant == 'overflow')]
    assert values == expected, (variant, values, expected)
    print(f'PASS: {variant}: {values}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
