#!/usr/bin/env python3
"""Pinned SDCC actual Vial producer/entry adapter, with mocked action core.

This diagnostic does not build firmware or implement a PH entry. It extracts
production Vial event/down functions and the current naked adapter, then links
an instrumented action_exec stub. It demonstrates why pointer ingress alone
cannot retain the outer generated identity or shared by-value event.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
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

def producer_calls(assembly, target):
    body = assembly.split('_vial_keycode_event:', 1)[1].split('_vial_keycode_down:', 1)[0]
    return bool(re.search(r'^\s*(?:lcall|acall|ljmp|ajmp|sjmp)\s+' + re.escape(target) + r'\s*(?:;[^\n]*)?$', body, re.M | re.I))

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True, help='new directory for retained assembly, map and simulator evidence')
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=False)
out = a.out.resolve()
vial = (ROOT / 'quantum/vial.c').read_text()
action = (ROOT / 'quantum/action.c').read_text()
magic = re.search(r'^#define VIAL_MATRIX_MAGIC\s+\d+\s*$', (ROOT / 'quantum/vial.h').read_text(), re.M)
assert magic
producer = '#include "action.h"\n' + magic.group(0) + '\nvoid register_code16(uint16_t code);\nvoid unregister_code16(uint16_t code);\nuint16_t g_vial_magic_keycode_override;\n'
producer += extract(vial, 'static void vial_keycode_event(uint16_t keycode, bool pressed) {') + '\n'
producer += extract(vial, 'void vial_keycode_down(uint16_t keycode) {') + '\n'
fallback_macro = re.search(r'^#\s*define AK820_ACTION_EXEC\(event\) action_exec\(event\)\s*$', (ROOT / 'quantum/action.h').read_text(), re.M)
assert fallback_macro, 'missing action.h fallback macro'
fallback_producer = producer.replace('#include "action.h"\n', '#include "action.h"\n#undef AK820_ACTION_EXEC\n' + fallback_macro.group(0) + '\n', 1)
adapter = '#include "action.h"\n_Static_assert(sizeof(keyevent_t) == 6, "event snapshot ABI");\n'
adapter += extract(action, 'void ak820_action_exec(const keyevent_t __xdata *event) __naked {') + '\n'
driver = r'''
#include "action.h"
extern uint16_t g_vial_magic_keycode_override;
void vial_keycode_down(uint16_t keycode);
__xdata __at (0x0f00) volatile uint8_t result[8];
static uint16_t clock_value;
uint16_t timer_read(void) { clock_value += 2; return clock_value; }
void register_code16(uint16_t code) { (void)code; }
void unregister_code16(uint16_t code) { (void)code; }
void action_exec(keyevent_t event) {
    if (g_vial_magic_keycode_override == 0x7700) {
        result[0] = (uint8_t)g_vial_magic_keycode_override;
        result[1] = (uint8_t)event.time;
#ifndef NO_NEST
        vial_keycode_down(0x7701);
#endif
        result[2] = (uint8_t)g_vial_magic_keycode_override;
        result[3] = (uint8_t)event.time;
        result[7] = (uint8_t)(g_vial_magic_keycode_override >> 8);
    } else {
        result[4] = (uint8_t)g_vial_magic_keycode_override;
        result[5] = (uint8_t)event.time;
    }
}
void main(void) {
    for (uint8_t i = 0; i < 8; ++i) result[i] = 0;
    vial_keycode_down(0x7700);
    result[6] = 0xa5;
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
(out / 'producer.c').write_text(producer)
(out / 'fallback_producer.c').write_text(fallback_producer)
(out / 'adapter.c').write_text(adapter)
(out / 'driver.c').write_text(driver)
commands = []
fallback_cmd = [str(TOOL / 'sdcc'), *flags, '-c', str(out / 'fallback_producer.c'), '-o', str(out / 'fallback_producer.rel')]
commands.append(fallback_cmd)
subprocess.run(fallback_cmd, cwd=ROOT, check=True, text=True)
fallback_assembly = (out / 'fallback_producer.asm').read_text()
assert producer_calls(fallback_assembly, '_action_exec'), 'fallback did not use by-value action_exec'
assert not producer_calls(fallback_assembly, '_ak820_action_exec'), 'fallback unexpectedly passed the adapter check'
print('PASS: compiled action.h by-value fallback rejected by producer adapter check')
for variant in ('nested', 'control'):
    objects = []
    for unit in ('producer', 'adapter', 'driver'):
        obj = out / f'{variant}_{unit}.rel'
        cmd = [str(TOOL / 'sdcc'), *flags, *(['-DNO_NEST'] if variant == 'control' else []), '-c', str(out / (unit + '.c')), '-o', str(obj)]
        commands.append(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True, text=True)
        objects.append(obj)
    compiled_adapter = (out / f'{variant}_adapter.asm').read_text()
    adapter_body = compiled_adapter.split('_ak820_action_exec:', 1)[1]
    assert adapter_body.index('#_action_exec_PARM_1') < adapter_body.index('ljmp _action_exec')
    assert len(re.findall(r'\bmovx\s+@dptr,a', adapter_body.split('ljmp _action_exec', 1)[0])) == 6
    compiled_driver = (out / f'{variant}_driver.asm').read_text()
    driver_body = compiled_driver.split('_action_exec:', 1)[1].split('_main:', 1)[0]
    assert '_action_exec_PARM_1' in driver_body and '_g_vial_magic_keycode_override' in driver_body
    assert ('lcall\t_vial_keycode_down' in driver_body) == (variant == 'nested')
    compiled_producer = (out / f'{variant}_producer.asm').read_text()
    assert '_vial_keycode_event_PARM_2' in compiled_producer and '_vial_keycode_event_dummy_event_' in compiled_producer
    assert producer_calls(compiled_producer, '_ak820_action_exec'), 'Vial producer did not call or jump to the adapter'
    image = out / f'{variant}.ihx'
    cmd = [str(TOOL / 'sdcc'), '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *map(str, objects), '-o', str(image)]
    commands.append(cmd)
    subprocess.run(cmd, cwd=out, check=True, text=True)
    map_text = (out / f'{variant}.map').read_text()
    match = re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', map_text)
    assert match, 'missing probe breakpoint in link map'
    address = int(match.group(1), 16)
    script = f'run 0 0x{address:x}\ndump xram 0x0f00 0x0f07\nquit\n'
    sim = subprocess.run([str(TOOL / 's51'), '-t', '51', '-c', '-', str(image)], input=script, text=True, capture_output=True, timeout=10, check=True)
    (out / f'{variant}.sim.log').write_text(sim.stdout + sim.stderr)
    row = re.search(r'0x0f00\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})', sim.stdout)
    assert row, sim.stdout
    values = [int(x, 16) for x in row.group(1).split()]
    expected = [0, 3, 1, 5, 1, 5, 0xa5, 0x77] if variant == 'nested' else [0, 3, 0, 3, 0, 0, 0xa5, 0x77]
    assert values == expected, (variant, values, expected)
    print(f'PASS: {variant} observed {values}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print('PASS: source-derived Vial/adapter counterexample; instrumented action core, no PH seam')
