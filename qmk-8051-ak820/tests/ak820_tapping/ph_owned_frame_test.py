#!/usr/bin/env python3
"""Unwired frame pool: host lifecycle checks and source-derived SDCC probe."""
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
p.add_argument('--out', required=True, type=Path)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
# Host shim supplies only event types; no firmware or host ABI equivalence is implied.
host_include = out / 'host_include'
host_include.mkdir()
(host_include / 'action.h').write_text('''#include <stdbool.h>\n#include <stdint.h>\n#define __xdata\ntypedef struct { uint8_t col, row; } keypos_t;\ntypedef enum { TICK_EVENT, KEY_EVENT } keyevent_type_t;\ntypedef struct { keypos_t key; uint16_t time; keyevent_type_t type; bool pressed; } keyevent_t;\n''')
commands = []
cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-I', str(host_include), '-I', str(BOARD), '-c', str(BOARD / 'ak820_ph_frame.c'), '-o', str(out / 'disabled.o')]
commands.append(cmd)
subprocess.run(cmd, check=True)
assert not subprocess.run(['nm', '--defined-only', str(out / 'disabled.o')], capture_output=True, text=True, check=True).stdout.strip()
print('PASS: disabled default exports no frame symbols')
cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', '-I', str(host_include), '-I', str(BOARD), str(BOARD / 'ak820_ph_frame.c'), str(HERE / 'ph_owned_frame_host.c'), '-o', str(out / 'host_test')]
commands.append(cmd)
subprocess.run(cmd, check=True)
host = subprocess.run([str(out / 'host_test')], capture_output=True, text=True, check=True, timeout=10)
(out / 'host.log').write_text(host.stdout + host.stderr)
print(host.stdout, end='')
vial = (ROOT / 'quantum/vial.c').read_text()
keymap = (ROOT / 'quantum/keymap_common.c').read_text()
event = extract(vial, 'static void vial_keycode_event(uint16_t keycode, bool pressed) {')
event = event.replace('static void vial_keycode_event(uint16_t keycode, bool pressed)', 'void probe_event(uint16_t keycode, bool pressed) __reentrant', 1)
assert event.count('    g_vial_magic_keycode_override = keycode;') == 1
event = event.replace('    g_vial_magic_keycode_override = keycode;', '''    ak820_ph_frame_handle_t handle = ak820_ph_frame_reserve();
    if (!handle) { result[2] = 1; return; }
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(handle);
    uint16_t previous = g_vial_magic_keycode_override;
    frame->keycode = keycode;
    g_vial_magic_keycode_override = keycode;''')
assert event.count('AK820_ACTION_EXEC(dummy_event);') == 1
event = event.replace('AK820_ACTION_EXEC(dummy_event);', 'frame->event = dummy_event;\n        probe_consume(handle);')
pos = event.rfind('}')
event = event[:pos] + '''    g_vial_magic_keycode_override = previous;
    if (!ak820_ph_frame_release(handle)) result[7] = 0xee;
''' + event[pos:]
producer = '''#include "ak820_ph_frame.h"
#include "vial.h"
extern __xdata volatile uint8_t result[16];
void register_code16(uint16_t code);
void unregister_code16(uint16_t code);
void probe_consume(ak820_ph_frame_handle_t h) __reentrant;
uint16_t g_vial_magic_keycode_override;
''' + event + '\n'
consumer = keymap[keymap.index('// translates key to keycode'):]
consumer = consumer[:consumer.index('\n}', consumer.index('uint16_t ak820_keycode_at')) + 2]
consumer = '#include "action.h"\n#include "keymap_common.h"\n#include "keymap_introspection.h"\n#include "vial.h"\n#include "encoder.h"\n' + consumer + '\n'
driver = r'''#include "ak820_ph_frame.h"
#include "keymap_common.h"
#include "vial.h"
void probe_event(uint16_t keycode, bool pressed) __reentrant;
__xdata __at (0x0f00) volatile uint8_t result[16];
__xdata ak820_ph_frame_handle_t outer_handle;
bool vial_unlock_in_progress;
static uint16_t clock_value;
uint16_t timer_read(void) { clock_value += 2; return clock_value; }
void register_code16(uint16_t keycode) { (void)keycode; }
void unregister_code16(uint16_t keycode) { (void)keycode; }
uint16_t keycode_at_keymap_location(uint8_t l, uint8_t r, uint8_t c) { return 0; }
uint16_t keycode_at_encodermap_location(uint8_t l, uint8_t i, bool cw) { return 0; }
void probe_consume(ak820_ph_frame_handle_t h) __reentrant {
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(h);
    uint16_t key = ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC);
    if (!frame || !ak820_ph_frame_pin(h)) return;
    if (key == 0x7700) {
        outer_handle = h;
        result[0] = frame->keycode == key && frame->event.time == 3;
#ifndef NO_NEST
        probe_event(0x7701, true);
#endif
        frame = ak820_ph_frame_get(h);
        result[5] = frame && frame->keycode == 0x7700 && frame->event.time == 3 &&
            ak820_keycode_at(0, (VIAL_MATRIX_MAGIC << 8) | VIAL_MATRIX_MAGIC) == 0x7700;
    } else if (key == 0x7701) {
        result[1] = frame->keycode == key && frame->event.time == 5;
        probe_event(0x7702, true);
        frame = ak820_ph_frame_get(outer_handle);
        result[3] = frame && frame->keycode == 0x7700 && frame->event.time == 3;
        frame = ak820_ph_frame_get(h);
        result[4] = frame && frame->keycode == 0x7701 && frame->event.time == 5;
    }
    if (!ak820_ph_frame_release(h)) result[6] = 0xee;
}
void main(void) {
    for (uint8_t i = 0; i < 16; ++i) result[i] = 0;
    probe_event(0x7700, true);
    result[8] = !ak820_ph_frame_get(outer_handle);
    result[9] = 0xa5;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
'''
for name, text in [('producer', producer), ('consumer', consumer), ('driver', driver)]:
    (out / (name + '.c')).write_text(text)
source = (BOARD / 'ak820_ph_frame.c').read_text()
needle = 'if (!references[i] && generations[i] != UINT16_MAX)'
assert source.count(needle) == 1
(out / 'mutant_frame.c').write_text(source.replace(needle, 'if (generations[i] != UINT16_MAX)'))
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
cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-c', str(BOARD / 'ak820_ph_frame.c'), '-o', str(out / 'disabled_sdcc.rel')]
commands.append(cmd)
subprocess.run(cmd, cwd=ROOT, check=True, text=True)
assert '_ak820_ph_frame_reserve' not in (out / 'disabled_sdcc.asm').read_text()
print('PASS: disabled SDCC object exports no frame entry')
for variant in ('nested', 'control', 'mutant'):
    objects = []
    for name in ('frame', 'producer', 'consumer', 'driver'):
        obj = out / f'{variant}_{name}.rel'
        src = (out / 'mutant_frame.c' if variant == 'mutant' else BOARD / 'ak820_ph_frame.c') if name == 'frame' else out / (name + '.c')
        cmd = [str(TOOL / 'sdcc'), *flags, '-I' + str(BOARD), '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2', *(['-DNO_NEST'] if variant == 'control' else []), '-c', str(src), '-o', str(obj)]
        commands.append(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True, text=True)
        objects.append(obj)
    frame_asm = (out / f'{variant}_frame.asm').read_text()
    for function in ('reserve', 'pin', 'release', 'get'):
        assert '_ak820_ph_frame_' + function + ':' in frame_asm
        assert not re.search(r'_ak820_ph_frame_' + function + r'_PARM_', frame_asm)
    full_producer_asm = (out / f'{variant}_producer.asm').read_text()
    assert '_probe_event_PARM_' not in full_producer_asm
    producer_asm = full_producer_asm.split('_probe_event:', 1)[1]
    assert re.search(r'lcall\s+_ak820_ph_frame_reserve', producer_asm)
    assert producer_asm.index('_ak820_ph_frame_reserve') < producer_asm.index('_g_vial_magic_keycode_override')
    assert re.search(r'lcall\s+_probe_consume', producer_asm)
    full_driver_asm = (out / f'{variant}_driver.asm').read_text()
    assert '_probe_consume_PARM_' not in full_driver_asm
    driver_asm = full_driver_asm.split('_probe_consume:', 1)[1].split('_main:', 1)[0]
    for target in ('_ak820_ph_frame_get', '_ak820_ph_frame_pin', '_ak820_ph_frame_release', '_ak820_keycode_at'):
        assert re.search(r'lcall\s+' + target, driver_asm), target
    assert '_g_vial_magic_keycode_override' in (out / f'{variant}_consumer.asm').read_text().split('_ak820_keycode_at:', 1)[1]
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
        assert values == [1,1,1,1,1,1,0,0,1,165,0,0,0,0,0,0], values
    elif variant == 'control':
        assert values == [1,0,0,0,0,1,0,0,1,165,0,0,0,0,0,0], values
    else:
        assert values != [1,1,1,1,1,1,0,0,1,165,0,0,0,0,0,0] and values[3] == 0, values
    print(f'PASS: {variant}: {values}')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
