#!/usr/bin/env python3
"""Exercise the production alternate-repeat CODE lookup on an 8051 simulator."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sdcc', type=Path, required=True)
parser.add_argument('--simulator', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
source = (root / 'quantum/repeat_key.c').read_text()
start = source.index('#if defined(AK820_BOARD) && defined(__SDCC_mcs51)\n/* All callers use static const tables')
end = source.index('\nuint16_t get_alt_repeat_key_keycode', start)
helper = source[start:end]
program = '''#include <stdint.h>
#define AK820_BOARD
#define KC_NO 0
''' + helper + '''
static const __code uint8_t pairs[][2] = {
    {0, 255}, {4, 5}, {6, 7}, {4, 8}, {128, 1}, {255, 0}
};
__xdata volatile uint8_t status;
void finished(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t target;
    uint8_t size, i, expected;
    for (size = 0; size <= sizeof(pairs); size += 2) {
        for (target = 0; target < 256; ++target) {
            expected = 0;
            for (i = 0; i < size; ++i) {
                if (((const __code uint8_t *)pairs)[i] == target) {
                    expected = ((const __code uint8_t *)pairs)[i ^ 1];
                    break;
                }
            }
            if (find_alt_keycode(pairs, size, target) != expected) {
                status = 0xee; finished(); for (;;) {}
            }
        }
    }
    status = 0xa5; finished(); for (;;) {}
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-repeat-cpu-') as folder:
    directory = Path(folder)
    fixture = directory / 'fixture.c'
    image = directory / 'fixture.ihx'
    fixture.write_text(program)
    subprocess.run([str(args.sdcc.resolve()), '-mmcs51', '--model-large', '--opt-code-size',
                    str(fixture), '-o', str(image)], check=True)
    mapping = image.with_suffix('.map').read_text()
    def address(name):
        match = re.search(r'^\s*(?:C:|D:)?\s*([0-9A-Fa-f]+)\s+_' + name + r'\s', mapping, re.M)
        if not match:
            raise RuntimeError('missing simulator symbol: ' + name)
        return int(match.group(1), 16)
    commands = f'break 0x{address("finished"):x}\nrun\ndump xram 0x{address("status"):x} 0x{address("status"):x}\nquit\n'
    result = subprocess.run([str(args.simulator.resolve()), '-t', '8051', '-c', '-', str(image)],
                            input=commands, text=True, capture_output=True, timeout=120, check=True)
    rows = re.findall(r'^0x[0-9a-fA-F]+\s+((?:[0-9a-fA-F]{2}\s+)+)', result.stdout, re.M)
    data = bytes.fromhex(' '.join(rows))
    if data != b'\xa5':
        raise RuntimeError('8051 lookup failed or did not finish: ' + result.stdout[-2000:] + result.stderr)
print('alternate-repeat CODE lookup: 1792 simulated 8051 cases passed')
