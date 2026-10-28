#!/usr/bin/env python3
"""Run the production macro opcode-range check on an 8051 simulator."""
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
source = (root / 'keyboards/ajazz/ak820/ak820_macro.c').read_text()
start = source.index('static bool parse_byte(')
end = source.index('\n}\n', start) + 2
program = '''#include <stdint.h>
#include <stdbool.h>
#define AK820_XDATA __xdata
#define DYNAMIC_KEYMAP_MACRO_COUNT 16
typedef struct { uint8_t terminated, arguments; } macro_parse_t;
''' + source[start:end] + '''
__xdata macro_parse_t state;
__xdata volatile uint8_t status;
void finished(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t value;
    bool actual, expected;
    for (value = 0; value < 256; ++value) {
        state.terminated = 0; state.arguments = 3;
        actual = parse_byte(&state, (uint8_t)value);
        expected = value >= 1 && value <= 7;
        if (actual != expected || state.terminated != 0 ||
            state.arguments != (expected ? (value <= 3 ? 1 : 2) : 3)) {
            status = 0xee; finished(); for (;;) {}
        }
    }
    status = 0xa5; finished(); for (;;) {}
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-macro-cpu-') as folder:
    directory = Path(folder)
    fixture = directory / 'fixture.c'
    image = directory / 'fixture.ihx'
    fixture.write_text(program)
    subprocess.run([str(args.sdcc.resolve()), '--std-c11', '-mmcs51', '--model-large', '--opt-code-size',
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
        raise RuntimeError('8051 parser failed or did not finish: ' + result.stdout[-2000:] + result.stderr)
print('macro opcode range: 256 simulated 8051 cases passed')
