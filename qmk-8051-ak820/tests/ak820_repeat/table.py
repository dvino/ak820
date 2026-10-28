#!/usr/bin/env python3
"""Offline checks for the production alternate-repeat table lookup."""
import argparse
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sdcc', type=Path, help='also compile the isolated mcs51 CODE-pointer helper')
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
source = (root / 'quantum/repeat_key.c').read_text()
start = source.index('#if defined(AK820_BOARD) && defined(__SDCC_mcs51)\n/* All callers use static const tables')
end = source.index('\nuint16_t get_alt_repeat_key_keycode', start)
helper = source[start:end]
header = '''#include <stdint.h>
#define KC_NO 0
#define pgm_read_byte(p) (*((uint8_t *)(p)))
'''
test = r'''
#include <assert.h>
int main(void) {
    uint8_t pairs[254];
    for (unsigned seed = 0; seed < 8; ++seed) {
        for (unsigned i = 0; i < sizeof(pairs); ++i)
            pairs[i] = (i * 17 + (i / 3) * seed) & 255;
        for (unsigned size = 0; size <= sizeof(pairs); size += 2) {
            for (unsigned target = 0; target <= 255; ++target) {
                uint8_t expected = 0;
                for (unsigned i = 0; i < size; ++i)
                    if (pairs[i] == target) { expected = pairs[i ^ 1]; break; }
                assert(find_alt_keycode((const uint8_t (*)[2])pairs, size, target) == expected);
            }
        }
    }
    return 0;
}
'''
# The actual helper is compiled with native pointer semantics in both branches;
# the SDCC compile below separately checks the target's address-space types.
with tempfile.TemporaryDirectory(prefix='ak820-repeat-table-') as folder:
    directory = Path(folder)
    fixture = directory / 'table.c'
    fixture.write_text(header + helper + test)
    for name, flags in [('generic', []), ('target-branch', ['-DAK820_BOARD', '-D__SDCC_mcs51', '-D__code='])]:
        exe = directory / name
        subprocess.run(['cc', '-std=c11', '-O1', '-Wall', '-Wextra', '-Werror',
                        '-fsanitize=undefined', '-fno-sanitize-recover=undefined',
                        *flags, str(fixture), '-o', str(exe)], check=True)
        subprocess.run([str(exe)], check=True)
    if args.sdcc:
        fixture.write_text(header + helper + '''
static const uint8_t pairs[][2] = {{4,5},{6,7},{8,9}};
uint8_t screen(uint8_t target) { return find_alt_keycode(pairs, sizeof(pairs), target); }
''')
        subprocess.run([str(args.sdcc), '--std-c11', '--model-large', '-mmcs51',
                        '-DAK820_BOARD', '-c', str(fixture), '-o', str(directory / 'table.rel')], check=True)
print('alternate-repeat table: native exhaustive lookup passed; isolated SDCC compile ' +
      ('passed' if args.sdcc else 'skipped (no compiler supplied)'))
