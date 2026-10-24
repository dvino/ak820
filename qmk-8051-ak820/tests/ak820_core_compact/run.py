#!/usr/bin/env python3
"""Exhaustive host differentials for scalar positions and compact key dispatch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def function(path, name):
    source = path.read_text()
    match = re.search(r'^.*\b' + name + r'\([^\n]*\) \{', source, re.M)
    if match is None:
        raise ValueError('Missing production function: ' + name)
    return source[match.start():source.index('\n}', match.end()) + 2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    keymap = ROOT / 'quantum/keymap_common.c'
    rgb = ROOT / 'quantum/process_keycode/process_rgb.c'
    repeat = ROOT / 'quantum/process_keycode/process_repeat_key.c'
    paths = [keymap, rgb, repeat, ROOT / 'quantum/keymap_common.h', ROOT / 'quantum/keycodes.h',
             ROOT / 'quantum/quantum_keycodes.h', ROOT / 'quantum/keymap_extras/keymap_us.h',
             ROOT / 'quantum/sequencer/sequencer.h',
             HERE / 'fixtures/keymap_38ad013.c', HERE / 'fixtures/rgb_38ad013.c',
             HERE / 'fixtures/repeat_38ad013.c', Path(__file__)]
    common = '''#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include "keycodes.h"
#define AK820_BOARD
typedef struct { uint8_t col, row; } keypos_t;
typedef struct { struct { bool pressed; } event; } keyrecord_t;
static uint32_t calls, trace;
'''
    position = function(keymap, 'ak820_keycode_at')
    # The source shares the body with the non-AK820 public aggregate form.
    position, replaced = re.subn(r'#else\n__attribute__\(\(weak\)\) uint16_t keymap_key_to_keycode[^\n]*\n'
                                 r'    uint8_t row = key.row, col = key.col;\n#endif\n', '', position)
    if replaced != 1:
        raise ValueError('Scalar/public shared function boundary changed')
    keymap_body = common + '''#define MATRIX_ROWS 16
#define MATRIX_COLS 8
#define NUM_ENCODERS 1
#define ENCODER_MAP_ENABLE
#define VIAL_ENABLE
#define VIAL_MATRIX_MAGIC 240
#define KEYLOC_ENCODER_CW 253
#define KEYLOC_ENCODER_CCW 252
bool vial_unlock_in_progress;
uint16_t g_vial_magic_keycode_override = 0x8ace;
static uint16_t keycode_at_keymap_location(uint8_t layer, uint8_t row, uint8_t col) {
    ++calls; trace = ((uint32_t)layer << 16) | ((uint16_t)row << 8) | col;
    return 0x1000u ^ trace;
}
static uint16_t keycode_at_encodermap_location(uint8_t layer, uint8_t index, bool clockwise) {
    ++calls; trace = 0x80000000u | ((uint32_t)layer << 16) | ((uint16_t)index << 8) | clockwise;
    return clockwise ? 0x7321 : 0x4567;
}
''' + position + '\n' + (HERE / 'fixtures/keymap_38ad013.c').read_text() + '''
int main(void) {
    uint32_t cases = 0;
    for (unsigned unlock = 0; unlock < 2; ++unlock) {
        vial_unlock_in_progress = unlock;
        for (unsigned layer = 0; layer < 256; ++layer) {
            for (uint32_t position = 0; position < 65536; ++position) {
                keypos_t key = {.row=position >> 8, .col=position};
                calls=trace=0;
                uint16_t expected=reference_keymap_key_to_keycode(layer,key);
                uint32_t expected_calls=calls,expected_trace=trace;
                calls=trace=0;
                assert(ak820_keycode_at(layer,position)==expected);
                assert(calls==expected_calls && trace==expected_trace);
                ++cases;
            }
        }
    }
    printf("PASS: %u position/layer/unlock cases, exact lookup calls and values\\n",cases);
}
'''
    action_names = ['step', 'step_reverse', 'increase_hue', 'decrease_hue', 'increase_sat',
                    'decrease_sat', 'increase_val', 'decrease_val', 'increase_speed', 'decrease_speed']
    actions = ','.join('rgb_matrix_' + name for name in action_names)
    rgb_body = common + '''#define RGB_MATRIX_ENABLE
#define ENABLE_RGB_MATRIX_BREATHING
#define ENABLE_RGB_MATRIX_CYCLE_LEFT_RIGHT
#define AK820_RGB_CODE
#define MOD_MASK_SHIFT 0x22
#define RGB_MATRIX_SOLID_COLOR 1
#define RGB_MATRIX_BREATHING 2
#define RGB_MATRIX_CYCLE_LEFT_RIGHT 4
static uint8_t mods;
static uint8_t get_mods(void) { return mods; }
static void rgb_matrix_toggle(void) { ++calls; trace=100; }
static void rgb_matrix_mode(uint8_t mode) { ++calls; trace=200+mode; }
''' + '\n'.join(f'static void rgb_matrix_{name}(void) {{ ++calls; trace={i+1}; }}'
                  for i, name in enumerate(action_names)) + '\n' + \
        'static void (* const ak820_rgb_actions[])(void)={' + actions + '};\n' + \
        'static void (* const reference_rgb_actions[])(void)={' + actions + '};\n' + \
        function(rgb, 'process_rgb') + '\n' + (HERE / 'fixtures/rgb_38ad013.c').read_text() + '''
int main(void) {
    uint32_t cases = 0;
    for (unsigned modifier = 0; modifier < 256; ++modifier) {
        mods=modifier;
        for (unsigned pressed = 0; pressed < 2; ++pressed) {
            keyrecord_t record={.event={.pressed=pressed}};
            for (uint32_t keycode = 0; keycode < 65536; ++keycode) {
                calls=trace=0;
                bool expected=reference_process_rgb(keycode,&record);
                uint32_t expected_calls=calls,expected_trace=trace;
                calls=trace=0;
                assert(process_rgb(keycode,&record)==expected);
                assert(calls==expected_calls && trace==expected_trace);
                assert(record.event.pressed==pressed);
                ++cases;
            }
        }
    }
    printf("PASS: %u RGB code/modifier/edge cases, exact action and consume behavior\\n",cases);
}
'''
    repeat_body = common + '''#include "quantum_keycodes.h"
#define NO_ACTION_TAPPING
#define NO_ACTION_ONESHOT
#define TRI_LAYER_ENABLE
static bool user_result;
static bool remember_last_key_user(uint16_t keycode, keyrecord_t *record, uint8_t *mods) {
    ++calls; trace = ((uint32_t)keycode << 16) | ((uint16_t)*mods << 8) | record->event.pressed;
    *mods ^= 0xa5;
    return user_result;
}
''' + function(repeat, 'remember_last_key') + '\n' + (HERE / 'fixtures/repeat_38ad013.c').read_text() + '''
int main(void) {
    uint32_t cases = 0;
    for (unsigned modifier = 0; modifier < 256; ++modifier) {
        for (unsigned pressed = 0; pressed < 2; ++pressed) {
            keyrecord_t record={.event={.pressed=pressed}};
            for (unsigned callback_result = 0; callback_result < 2; ++callback_result) {
                user_result=callback_result;
                for (uint32_t keycode = 0; keycode < 65536; ++keycode) {
                    uint8_t expected_mods=modifier, actual_mods=modifier;
                    calls=trace=0;
                    bool expected=reference_remember_last_key(keycode,&record,&expected_mods);
                    uint32_t expected_calls=calls,expected_trace=trace;
                    calls=trace=0;
                    assert(remember_last_key(keycode,&record,&actual_mods)==expected);
                    assert(calls==expected_calls && trace==expected_trace);
                    assert(actual_mods==expected_mods && record.event.pressed==pressed);
                    ++cases;
                }
            }
        }
    }
    printf("PASS: %u Repeat code/modifier/edge/callback cases, exact callback and result\\n",cases);
}
'''
    rows = []
    with tempfile.TemporaryDirectory(prefix='ak820-core-compact-') as directory:
        work = Path(directory)
        for name, body, defines in [('positions', keymap_body, []), ('rgb-release', rgb_body, []),
                                   ('rgb-press', rgb_body, ['RGB_TRIGGER_ON_KEYDOWN']),
                                   ('repeat-standard', repeat_body, []),
                                   ('repeat-one-shot', repeat_body, ['AK820_COMPACT_ONESHOT'])]:
            source, binary = work / (name + '.c'), work / name
            source.write_text(body)
            subprocess.run([os.environ.get('CC', 'cc'), '-std=gnu11', '-O2', '-g', '-Wall', '-Wextra',
                            '-Werror', '-Wno-unused-parameter', '-fsanitize=undefined',
                            '-fno-sanitize-recover=undefined', '-I' + str(ROOT / 'quantum'),
                            '-I' + str(ROOT / 'quantum/keymap_extras'),
                            '-I' + str(ROOT / 'quantum/sequencer'),
                            *['-D' + define for define in defines], str(source), '-o', str(binary)], check=True)
            result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
            print(name + ': ' + result.stdout.strip())
            rows.append({'name': name, 'pass': True, 'summary': result.stdout.strip(),
                         'fixture_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    report = {'pass': True, 'hardware_validated': False, 'tests': rows,
              'limits': 'Host production-function differential against 38ad013; no target ABI or device timing proof.',
              'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in paths}}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
