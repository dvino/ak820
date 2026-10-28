#!/usr/bin/env python3
"""Exercise extracted production source decoder and VIA packet assembly on SDCC 8051.

This is an isolated ABI fixture, not a linked keyboard or IRQ/hardware test.
"""
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
tapping = (root / 'keyboards/ajazz/ak820/ak820_tapping.c').read_text()
start = tapping.index('uint8_t ak820_tapping_source_ptr(')
end = tapping.index('#    endif\n#    define source_of', start)
decoder = tapping[start:end].replace('#    ifdef AK820_COMPACT_ONESHOT', '#ifdef AK820_COMPACT_ONESHOT') + '\n#endif\n'
via = (root / 'quantum/via.c').read_text()
start = via.index('                    union { uint32_t value; uint8_t bytes[4]; } value;')
end = via.index('\n#else', start)
assembly = via[start:end]
program = r'''
#include <stdint.h>
#define MATRIX_ROWS 16
#define MATRIX_COLS 8
#define NUM_ENCODERS 1
#define KEYLOC_ENCODER_CW 253
#define KEYLOC_ENCODER_CCW 252
#define NONE 255
#define AK820_STATE_MEM __xdata
#define AK820_COMPACT_ONESHOT
/* keypos_t field order matches keyboard.h */
typedef struct { uint8_t col; uint8_t row; } keypos_t;
''' + decoder + r'''
__xdata volatile uint8_t status;
__xdata uint8_t command_data[5];
__xdata uint32_t observed;
static void via_set_layout_options(uint32_t value) { observed = value; }
static void decode_packet(void) {
''' + assembly + r'''
}
void finished(void) __naked { __asm ret __endasm; }
void main(void) {
    __xdata keypos_t key;
    uint8_t i;
    static const __code uint8_t rows[] = {0, 15, 16, 252, 253, 254, 255};
    static const __code uint8_t cols[] = {0, 1, 7, 8, 255};
    uint8_t j;
    for (i = 0; i < sizeof(rows); ++i) {
        for (j = 0; j < sizeof(cols); ++j) {
            uint8_t expected = 255;
            key.row = rows[i]; key.col = cols[j];
            if (key.row < 16 && key.col < 8) expected = key.row * 8 + key.col;
            else if (key.col == 0 && key.row == 253) expected = 128;
            else if (key.col == 0 && key.row == 252) expected = 129;
            if (ak820_tapping_source_ptr(&key) != expected || ak820_tapping_source(key) != expected) {
                status = 1; finished(); for (;;) {}
            }
        }
    }
    command_data[1]=0x12; command_data[2]=0x34; command_data[3]=0x56; command_data[4]=0x78;
    decode_packet();
    if (observed != 0x12345678UL) { status=2; finished(); for (;;) {} }
    command_data[1]=0xa5; command_data[2]=0x5a; command_data[3]=0xff; command_data[4]=0x78;
    decode_packet();
    if (observed != 0xa55aff78UL) { status=3; finished(); for (;;) {} }
    for (i=0; i<32; ++i) {
        uint32_t value = (uint32_t)1 << i;
        command_data[1]=value >> 24; command_data[2]=value >> 16;
        command_data[3]=value >> 8; command_data[4]=value;
        decode_packet();
        if (observed != value) { status=4; finished(); for (;;) {} }
    }
    status=0xa5; finished(); for (;;) {}
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-compact-cpu-') as folder:
    directory = Path(folder)
    source = directory / 'fixture.c'
    image = directory / 'fixture.ihx'
    source.write_text(program)
    subprocess.run([str(args.sdcc.resolve()), '--std-c11', '-mmcs51', '--model-large',
                    '--opt-code-size', str(source), '-o', str(image)], check=True)
    mapping = image.with_suffix('.map').read_text()
    def address(name):
        match = re.search(r'^\s*(?:C:|D:)?\s*([0-9A-Fa-f]+)\s+_' + name + r'\s', mapping, re.M)
        if not match:
            raise ValueError('missing simulator symbol: ' + name)
        return int(match.group(1), 16)
    commands = f'break 0x{address("finished"):x}\nrun\ndump xram 0x{address("status"):x} 0x{address("status"):x}\nquit\n'
    result = subprocess.run([str(args.simulator.resolve()), '-t', '8051', '-c', '-', str(image)],
                            input=commands, text=True, capture_output=True, timeout=120, check=True)
    rows = re.findall(r'^0x[0-9a-fA-F]+\s+((?:[0-9a-fA-F]{2}\s+)+)', result.stdout, re.M)
    if bytes.fromhex(' '.join(rows)) != b'\xa5':
        raise RuntimeError('8051 compact ABI fixture failed: ' + result.stdout[-2000:] + result.stderr)
print('Compact source pointer/by-value and 32-bit VIA assembly: 8051 fixture passed')
