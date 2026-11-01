#!/usr/bin/env python3
"""Host adapter for source-derived VIA macro -> Vial -> retained tapping nesting.

This combines the board macro interpreter with the non-compact reference
arbitrator. A host process_record adapter invokes extracted process_record_via;
the XDATA, EEPROM, action entry, keymap, clock and output are host stubs. It is
not a linked board image, its preprocessing or HID pipeline, and does not
prove this hybrid configuration is deployed. A diagnostic limit stops before
the third macro callback can invoke VIA.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def function(text, signature):
    start = text.index(signature)
    end = text.index('{', start) + 1
    depth = 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]


vial = (ROOT / 'quantum/vial.c').read_text()
dynamic = (ROOT / 'quantum/dynamic_keymap.c').read_text()
via = (ROOT / 'quantum/via.c').read_text()
tapping = (ROOT / 'quantum/action_tapping.c').read_text()
harness = '#include <stdlib.h>\n' + (HERE / 'ph_reference_harness.c').read_text()
primitives = '''
#define AK820_BOARD
#define QK_MODS_MAX 0x1fff
#define QK_MACRO 0x7700
#define QK_MACRO_MAX 0x777f
#define VIAL_MATRIX_MAGIC 2
#define KEY_EVENT 1
#define DYNAMIC_KEYMAP_MACRO_COUNT 1
#define DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR 0
#define DYNAMIC_KEYMAP_MACRO_DELAY 0
#define SS_QMK_PREFIX 1
#define SS_TAP_CODE 1
#define SS_DOWN_CODE 2
#define SS_UP_CODE 3
#define SS_DELAY_CODE 4
#define VIAL_MACRO_EXT_TAP 5
#define VIAL_MACRO_EXT_DOWN 6
#define VIAL_MACRO_EXT_UP 7
#define QS_tap_code_delay 5
static const uint8_t macro_stream[] = {1, 5, 4, 0x22, 0};
static unsigned macro_callbacks;
static uint16_t g_vial_magic_keycode_override;
static bool ak820_macro_ready(void) { return true; }
static uint16_t ak820_macro_length(void) { return sizeof(macro_stream); }
static uint8_t eeprom_read_byte(const uint8_t *p) {
    uintptr_t offset = (uintptr_t)p;
    return offset < sizeof(macro_stream) ? macro_stream[offset] : 0;
}
static uint16_t timer_read(void) { return now; }
static void qs_wait_ms(uint16_t ms) { printf("wait %u %u\\n", now, ms); now += ms; }
static void wait_ms(uint16_t ms) { now += ms; }
static void register_code16(uint16_t code) { printf("direct-down %04x\\n", code); }
static void unregister_code16(uint16_t code) { printf("direct-up %04x\\n", code); }
static void tap_code(uint8_t code) { (void)code; }
static void register_code(uint8_t code) { (void)code; }
static void unregister_code(uint8_t code) { (void)code; }
static void send_char(char c) { (void)c; }
static void adapter_action_exec(keyevent_t event) {
    keyrecord_t r = {.event = event};
    map[2] = cached[2] = g_vial_magic_keycode_override;
    action_tapping_process(r);
}
#define AK820_ACTION_EXEC(event) adapter_action_exec(event)
'''
for sig in ('static void vial_keycode_event(', 'void vial_keycode_down(',
            'void vial_keycode_up(', 'void vial_keycode_tap('):
    primitives += '\n' + function(vial, sig) + '\n'
for sig in ('static uint16_t decode_keycode(', 'void dynamic_keymap_macro_send('):
    primitives += '\n' + function(dynamic, sig) + '\n'
primitives += '\n' + function(via, 'bool process_record_via(') + '\n#undef AK820_BOARD\n'
needle = 'static void process_record(keyrecord_t *r) {'
assert harness.count(needle) == 1
harness = harness.replace(needle, primitives + '\n' + needle)
needle = '    printf("%u %u %u %u %u %04x %02x %lx\\n", r->event.time,now,r->event.key.col,down,r->tap.count,k,mods,(unsigned long)layers);'
assert harness.count(needle) == 1
harness = harness.replace(needle, needle + '''
    if (k == QK_MACRO && down && ++macro_callbacks == 3) {
        puts("diagnostic-callback-limit");
        fflush(stdout);
        exit(0);
    }
    (void)process_record_via(k, r);
''')
with tempfile.TemporaryDirectory(prefix='.ph-vial-entry-', dir=HERE) as directory:
    path = Path(directory)
    (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', tapping, flags=re.M))
    (path / 'probe.c').write_text(harness)
    exe = path / 'probe'
    subprocess.run([os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DQUICK_TAP_TERM=0', '-I', str(ROOT / 'quantum'), '-I', str(path), str(path / 'probe.c'), '-o', str(exe)], check=True)
    trace = 'M 0 2204\nM 1 7700\nE 100 0 1\nE 110 1 1\nE 120 1 0\nE 130 0 0\n'
    output = subprocess.run([str(exe)], input=trace, text=True, capture_output=True, check=True, timeout=5).stdout
    print(output, end='')
    expected = [
        '100 120 0 1 0 2204 02 0',
        '110 120 1 1 0 7700 02 0',
        '121 120 2 1 0 2204 02 0',
        'wait 120 5',
        '125 125 2 0 0 2204 00 0',
        '110 125 1 1 0 7700 00 0',
        '120 125 1 0 0 7700 00 0',
        '110 125 1 1 0 7700 00 0',
        'diagnostic-callback-limit',
    ]
    assert output.splitlines() == expected, output
    print('PASS: extracted VIA/macro/Vial path repeats the queued macro callback in this host adapter')
