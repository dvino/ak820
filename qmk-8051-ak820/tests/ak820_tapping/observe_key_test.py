#!/usr/bin/env python3
"""Exercise the extracted lookup with stubbed layer and keycode readers.

The layer and keycode readers are stubs; this does not test the real cache,
transparent layers, keymap or encoder boundaries, SDCC ABI, or integration.
Source review of action_layer.c supports nonmutation: the helper calls the
layer and keycode readers rather than the source-cache writers.
"""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
source = (root / 'quantum/action_layer.c').read_text()
start = source.index('uint16_t ak820_observe_key(uint16_t position) {')
end = source.index('\n}\n', start) + 3
function = source[start:end]
harness = '''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#ifdef VIAL_ENABLE
#define VIAL_MATRIX_MAGIC 0xff
#define KC_NO 0
static bool vial_unlock_in_progress;
static uint16_t g_vial_magic_keycode_override;
#endif
static uint8_t layer = 1;
static unsigned lookups;
uint8_t ak820_layer_for_key(uint16_t position) { (void)position; return layer; }
uint16_t ak820_keycode_at(uint8_t selected, uint16_t position) {
    ++lookups;
    return (uint16_t)(selected * 100 + position);
}
''' + function + '''
int main(void) {
    assert(ak820_observe_key(3) == 103);
    assert(lookups == 1);
    layer = 2;
    assert(ak820_observe_key(3) == 203);
    assert(lookups == 2);
#ifdef VIAL_ENABLE
    g_vial_magic_keycode_override = 4321;
    assert(ak820_observe_key(0xffff) == 4321);
    assert(lookups == 2);
    vial_unlock_in_progress = true;
    assert(ak820_observe_key(0xffff) == KC_NO);
    assert(ak820_observe_key(3) == KC_NO);
    assert(lookups == 2);
#endif
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-ph-observe-') as directory:
    path = Path(directory)
    (path / 'test.c').write_text(harness)
    for flags in ([], ['-DVIAL_ENABLE']):
        subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', *flags, str(path / 'test.c'), '-o', str(path / 'test')], check=True)
        subprocess.run([str(path / 'test')], check=True)
print('PASS: stubbed layer/keycode lookup and Vial override/unlock branches')
