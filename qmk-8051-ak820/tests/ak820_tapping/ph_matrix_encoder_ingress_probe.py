#!/usr/bin/env python3
"""Source-derived matrix/encoder callers and SDCC ingress ABI experiment.

The owned branch is a test-only transformation, not production wiring. Matrix,
timer, wait and action callbacks are instrumented mocks; no IRQs are modeled.
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


def extract(text, signature):
    start = text.index(signature)
    end = text.index('{', start) + 1
    depth = 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def body(asm, start, end=None):
    part = asm.split('_' + start + ':', 1)[1]
    return part.split('_' + end + ':', 1)[0] if end else part

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
keyboard = (ROOT / 'quantum/keyboard.c').read_text()
encoder = (ROOT / 'quantum/encoder.c').read_text()
action = (ROOT / 'quantum/action.c').read_text()
tick = extract(keyboard, 'static inline void generate_tick_event(void) {')
matrix = extract(keyboard, 'static bool matrix_task(void) {')
enc = extract(encoder, 'static void encoder_exec_mapping(uint8_t index, bool clockwise) {')
tick = once(tick, '        MAKE_TICK_EVENT;\n        AK820_ACTION_EXEC(dummy_event);', '''#ifdef TEST_OWNED
        test_emit(0, 0, false, TICK_EVENT);
#else
        MAKE_TICK_EVENT;
        AK820_ACTION_EXEC(dummy_event);
#endif''')
matrix = once(matrix, '                    MAKE_KEYEVENT(row, col, key_pressed);\n                    AK820_ACTION_EXEC(dummy_event);', '''#ifdef TEST_OWNED
                    test_emit(row, col, key_pressed, KEY_EVENT);
#else
                    MAKE_KEYEVENT(row, col, key_pressed);
                    AK820_ACTION_EXEC(dummy_event);
#endif''')
enc = once(enc, 'static void encoder_exec_mapping(uint8_t index, bool clockwise) {', '''#ifdef TEST_OWNED
static void encoder_exec_mapping(uint8_t index, bool clockwise) __reentrant {
#else
static void encoder_exec_mapping(uint8_t index, bool clockwise) {
#endif''')
needle = '''    // The action wrapper snapshots the event before processing it.
    MAKE_EVENT(clockwise ? KEYLOC_ENCODER_CW : KEYLOC_ENCODER_CCW, index, true,
               clockwise ? ENCODER_CW_EVENT : ENCODER_CCW_EVENT);'''
enc = once(enc, needle, '''#ifdef TEST_OWNED
    ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
    if (!h) { test_failure(); return; }
    ak820_ph_frame_t __xdata *f = ak820_ph_frame_get(h);
    f->event.key.row = clockwise ? KEYLOC_ENCODER_CW : KEYLOC_ENCODER_CCW;
    f->event.key.col = index;
    f->event.time = timer_read();
    f->event.type = clockwise ? ENCODER_CW_EVENT : ENCODER_CCW_EVENT;
    f->event.pressed = true;
    if (test_dispatch(h)) {
#    if ENCODER_MAP_KEY_DELAY > 0
        wait_ms(ENCODER_MAP_KEY_DELAY);
#    endif
        f->event.time = timer_read();
        f->event.pressed = false;
        if (test_dispatch(h)) {
#    if ENCODER_MAP_KEY_DELAY > 0
            wait_ms(ENCODER_MAP_KEY_DELAY);
#    endif
        }
    }
    ak820_ph_frame_release(h);
#else
''' + needle)
needle = '''    dummy_event.pressed = false;
    AK820_ACTION_EXEC(dummy_event);
#        if ENCODER_MAP_KEY_DELAY > 0
    wait_ms(ENCODER_MAP_KEY_DELAY);
#        endif
#    else'''
enc = once(enc, needle, '''    dummy_event.pressed = false;
    AK820_ACTION_EXEC(dummy_event);
#        if ENCODER_MAP_KEY_DELAY > 0
    wait_ms(ENCODER_MAP_KEY_DELAY);
#        endif
#endif /* TEST_OWNED */
#    else''')
header = r'''
#include "action.h"
#include "matrix.h"
#include "debug.h"
#include "ak820_ph_frame.h"
void matrix_scan_perf_task(void);
bool should_process_keypress(void);
void switch_events(uint8_t row, uint8_t col, bool pressed);
void vial_unlock_task(void);
void wait_ms(uint16_t ms);
#ifdef TEST_OWNED
void test_emit(uint8_t row, uint8_t col, bool pressed, keyevent_type_t type) __reentrant;
bool test_dispatch(ak820_ph_frame_handle_t h) __reentrant;
void test_failure(void);
#endif
'''
ghost = extract(keyboard[keyboard.index('#else\n\nstatic inline bool has_ghost_in_row'):], 'static inline bool has_ghost_in_row(uint8_t row, matrix_row_t rowdata) {')
producer = header + '\n' + ghost + '\n' + tick + '\n' + matrix + '\n' + enc + r'''
void probe_matrix(void) { matrix_task(); }
#ifdef TEST_OWNED
void probe_encoder(uint8_t index, bool clockwise) __reentrant { encoder_exec_mapping(index, clockwise); }
#else
void probe_encoder(uint8_t index, bool clockwise) { encoder_exec_mapping(index, clockwise); }
#endif
'''
adapter = '#include "action.h"\n_Static_assert(sizeof(keyevent_t) == 6, "event ABI");\n' + extract(action, 'void ak820_action_exec(const keyevent_t __xdata *event) __naked {') + '\n'
(out / 'producer.c').write_text(producer)
(out / 'adapter.c').write_text(adapter)
(out / 'driver.c').write_text((HERE / 'ph_matrix_encoder_ingress_probe_driver.c').read_text())
raw = json.loads(META.read_text())['argv'][1:]
flags = []
i = 0
while i < len(raw):
    t = raw[i]
    if t == '-o':
        i += 2
        continue
    if t.startswith('-Wp,-MD,-MF,') or t in ('quantum/action.c', '-c'):
        i += 1
        continue
    flags.append(t.replace('.build/final/main/obj_ajazz_ak820_vial', OBJ))
    i += 1
assert '--xstack' not in flags
# Override the default zero delay to exercise the actual optional wait branches.
flags += ['-DENCODER_MAP_KEY_DELAY=1', '-DAK820_PH_FRAME_ENABLE', '-I' + str(BOARD)]
commands = []
def run(cmd, cwd=ROOT):
    commands.append([str(x) for x in cmd])
    subprocess.run([str(x) for x in cmd], cwd=cwd, check=True, text=True)

cases = [
    ('off_tick', 0, False, False, 2),
    ('off_physical_nested', 1, False, False, 2),
    ('off_physical_control', 6, False, False, 2),
    ('off_physical_release', 10, False, False, 2),
    ('off_encoder_cw_control', 7, False, False, 2),
    ('off_encoder_ccw_control', 8, False, False, 2),
    ('owned_tick', 0, True, False, 2),
    ('owned_physical_nested', 1, True, False, 2),
    ('owned_encoder_physical', 2, True, False, 2),
    ('owned_encoder_nested', 3, True, False, 2),
    ('owned_full', 4, True, False, 2),
    ('owned_nested_full', 5, True, False, 1),
    ('owned_tick_full', 9, True, False, 2),
    ('owned_release_full_next_scan', 11, True, False, 2),
    ('owned_physical_control', 6, True, False, 2),
    ('owned_physical_release', 10, True, False, 2),
    ('owned_encoder_cw_control', 7, True, False, 2),
    ('owned_encoder_ccw_control', 8, True, False, 2),
    ('unsafe_owned_nested', 1, True, True, 2),
]
results = {}
for name, case, owned, unsafe, capacity in cases:
    defs = ['-DPROBE_CASE=' + str(case), '-DAK820_PH_FRAME_CAPACITY=' + str(capacity)]
    if owned:
        defs.append('-DTEST_OWNED')
    if unsafe:
        defs.append('-DTEST_UNSAFE_ADAPTER')
    objects = []
    for unit, src in [('producer', out / 'producer.c'), ('adapter', out / 'adapter.c'), ('driver', out / 'driver.c'), ('frame', BOARD / 'ak820_ph_frame.c')]:
        obj = out / (name + '_' + unit + '.rel')
        run([TOOL / 'sdcc', *flags, *defs, '-c', src, '-o', obj])
        objects.append(obj)
    prod = (out / (name + '_producer.asm')).read_text()
    adapt = body((out / (name + '_adapter.asm')).read_text(), 'ak820_action_exec')
    assert len(re.findall(r'\bmovx\s+@dptr,a', adapt.split('ljmp _action_exec', 1)[0])) == 6
    assert '#_action_exec_PARM_1' in adapt
    tick_body = body(prod, 'generate_tick_event', 'matrix_task')
    matrix_body = body(prod, 'matrix_task', 'encoder_exec_mapping')
    eb = body(prod, 'encoder_exec_mapping', 'probe_matrix')
    if owned:
        assert '_ak820_action_exec' not in prod and '_action_exec_PARM_1' not in prod and 'dummy_event' not in prod
        assert '_test_emit' in tick_body and '_test_emit' in matrix_body
        assert eb.index('_ak820_ph_frame_reserve') < eb.index('_ak820_ph_frame_get') < eb.index('_timer_read') < eb.index('_test_dispatch')
        assert eb.index('_ak820_ph_frame_get') < re.search(r'\bmovx\s+@dptr,a', eb).start()
        assert '_encoder_exec_mapping_PARM_2' not in prod
        driver = (out / (name + '_driver.asm')).read_text()
        emit = body(driver, 'test_emit', 'main')
        assert emit.index('_ak820_ph_frame_reserve') < emit.index('_ak820_ph_frame_get') < emit.index('_timer_read') < emit.index('_test_dispatch')
        assert emit.index('_ak820_ph_frame_get') < re.search(r'\bmovx\s+@dptr,a', emit).start()
        assert '_test_emit_PARM_' not in driver
        db = body(driver, 'test_dispatch', 'test_emit')
        assert ('_ak820_action_exec' in db) == unsafe
    else:
        assert all('_ak820_action_exec' in part for part in (tick_body, matrix_body, eb))
        assert 'dummy_event' in prod
    image = out / (name + '.ihx')
    run([TOOL / 'sdcc', '-mmcs51', '--model-large', '--iram-size', '0x0100', '--xram-size', '0x0c00', '--xram-loc', '0x0400', '--code-size', '0xc700', *objects, '-o', image], out)
    m = re.search(r'\b([0-9A-Fa-f]{8})\s+_probe_done\b', (out / (name + '.map')).read_text())
    assert m
    script = f'run 0 0x{int(m.group(1), 16):x}\ndump xram 0x0e00 0x0e3f\nquit\n'
    sim = subprocess.run([str(TOOL / 's51'), '-t', '51', '-c', '-', str(image)], input=script, text=True, capture_output=True, timeout=10, check=True)
    (out / (name + '.sim.log')).write_text(sim.stdout + sim.stderr)
    result = []
    for offset in range(0, 64, 8):
        match = re.search(r'0x%04x\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})' % (0x0e00 + offset), sim.stdout)
        assert match, sim.stdout
        result.extend(int(x, 16) for x in match.group(1).split())
    assert result[62:64] == [0, 0xa5], (name, result)
    results[name] = result
    before, after = result[16:22], result[48:54]
    if case == 0:
        assert result[0] == 1 and result[1] == 0 and before[0:2] == [0, 0] and before[4] == 0 and before[5] == 0, (name, result)
    elif case in (4, 9):
        assert result[0] == 0 and result[1] == 1 and result[2] == 0, (name, result)
    elif case in (6, 7, 8, 10):
        if case in (6, 10):
            assert result[0:3] == [1, 0, 0] and result[16:22] == [1, 0, 101, 0, 1, int(case == 6)], (name, result)
        else:
            row, kind = (253, 2) if case == 7 else (252, 3)
            assert result[0:3] == [2, 0, 2] and result[4:8] == [0x11, 0x80, 0x10, 0x80], (name, result)
            assert result[16:28] == [1, row, 101, 0, kind, 1, 1, row, 102, 0, kind, 0], (name, result)
    elif case == 5:
        assert result[0] == 1 and result[1] == 1 and result[2] == 0 and before == after, (name, result)
        assert before == [1, 253, 101, 0, 2, 1], (name, result)
    elif case == 11:
        assert result[3] == 1 and result[56:62] == [1, 0, 101, 0, 1, 1], (name, result)
        assert result[54:56] == [0, 1], (name, result)
        assert result[0:3] == [1, 1, 0] and result[4] == 0x10, (name, result)
        assert before == [0, 0, 102, 0, 0, 0], (name, result)
        print('PASS: failed release advances matrix state; next scan is tick, not release retry; cleanup required')
    else:
        assert result[1] == 0, (name, result)
        if not owned or unsafe:
            assert before != after, (name, result)
        else:
            assert before == after, (name, result)
            if case == 1:
                assert result[0:3] == [3, 0, 2] and result[4:9] == [0x11, 0x11, 0x80, 0x10, 0x80], (name, result)
                assert result[16:34] == [1, 0, 101, 0, 1, 1, 2, 252, 102, 0, 3, 1, 2, 252, 103, 0, 3, 0], (name, result)
            elif case == 2:
                assert result[0:3] == [3, 0, 2] and result[4:9] == [0x11, 0x11, 0x80, 0x10, 0x80], (name, result)
                assert result[16:34] == [1, 253, 101, 0, 2, 1, 1, 0, 102, 0, 1, 1, 1, 253, 103, 0, 2, 0], (name, result)
            else:
                assert result[0:3] == [4, 0, 4] and result[4:12] == [0x11, 0x11, 0x80, 0x10, 0x80, 0x80, 0x10, 0x80], (name, result)
                assert result[16:40] == [1, 253, 101, 0, 2, 1, 2, 252, 102, 0, 3, 1, 2, 252, 103, 0, 3, 0, 1, 253, 104, 0, 2, 0], (name, result)
    print('PASS:', name, 'counts', result[:3], 'outer', before, after)
for name in ('tick', 'physical_control', 'physical_release', 'encoder_cw_control', 'encoder_ccw_control'):
    assert results['off_' + name] == results['owned_' + name], name
    print('PASS: off/owned no-nesting trace matches:', name)
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print('PASS: source-derived matrix/encoder producers with instrumented action core; no production or IRQ qualification')
