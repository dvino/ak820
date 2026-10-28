#!/usr/bin/env python3
"""Exercise SDCC Tap Dance fallback and nested dispatch on an 8051 simulator.

The offline fixture links production source with stub hooks; it is not a
keyboard firmware image and does not establish IRQ or hardware behavior.
"""
import argparse
import ast
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sdcc', required=True, type=Path)
parser.add_argument('--simulator', required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
host_tree = ast.parse((root / 'tests/ak820_tap_dance/host.py').read_text())
fixture = next(ast.literal_eval(node.value) for node in host_tree.body
               if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'fixture' for t in node.targets))
fixture = fixture.replace('#define AK820_STATE_MEM\n', '#define AK820_STATE_MEM __xdata\n')
fixture = fixture.replace('vial_tap_dance_entry_t *e', 'vial_tap_dance_entry_t __xdata *e')
source = (root / 'keyboards/ajazz/ak820/ak820_tap_dance.c').read_text()
source = re.sub(r'^#include[^\n]*\n', '', source, flags=re.M)
cases = r'''
__xdata volatile uint8_t status;
int putchar(int value) { return value; } /* SDCC assert's unused output hook. */
void finished(void) __naked { __asm ret __endasm; }
static void reenter(void) {
    td_slots[1].source = 1; td_slots[1].state = TD_DOWN + 1;
    td_entry = fixture[1]; td_wait = &td_slots[1]; td_map_set(1, 1);
    td_finish(false);
}
static void setup(uint8_t state) {
    ak820_tap_dance_cancel();
    memset(refs, 0, sizeof refs); memset(downs, 0, sizeof downs);
    memset(fixture, 0, sizeof fixture);
    fixture[0].on_tap = 4; fixture[0].on_hold = 5;
    fixture[1].on_tap = 8; fixture[1].on_hold = 9;
    td_entry = fixture[0]; td_slots[0].source = 0; td_slots[0].state = state;
    td_wait = &td_slots[0];
}
void main(void) {
    /* Missing double action: emit two tap pulses, requiring extra=true. */
    setup(2); td_finish(false);
    if (downs[4] != 2 || refs[4] != 0) { status = 1; finished(); for (;;) {} }
    /* Present double action: one separate pulse, requiring extra=false. */
    setup(2); td_entry.on_double_tap = 6; td_finish(false);
    if (downs[4] != 0 || downs[6] != 1 || refs[6] != 0) { status = 2; finished(); for (;;) {} }
    /* Nested finish resets its bit before returning through the guard. Outer
       work is already committed; nested pending work must survive. */
    setup(TD_DOWN + 1); reenter_on_down = true; td_finish(false);
    if (refs[5] != 1 || downs[9] != 0 || td_wait != &td_slots[1]) { status = 3; finished(); for (;;) {} }
    td_finish(false);
    if (refs[9] != 1) { status = 4; finished(); for (;;) {} }
    status = 0xa5; finished(); for (;;) {}
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-td-cpu-') as folder:
    directory = Path(folder)
    program = directory / 'fixture.c'
    image = directory / 'fixture.ihx'
    program.write_text(fixture + source + cases)
    subprocess.run([str(args.sdcc.resolve()), '--std-c11', '-mmcs51', '--model-large', '--opt-code-size',
                    str(program), '-o', str(image)], check=True)
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
    data = bytes.fromhex(' '.join(rows))
    if data != b'\xa5':
        raise RuntimeError('8051 Tap Dance fixture failed or did not finish: ' + result.stdout[-2000:] + result.stderr)
print('Tap Dance SDCC bit-local fallback and nested dispatch: 3 simulated 8051 cases passed')
