#!/usr/bin/env python3
"""Compile exact production record declarations/assertions with real SDCC.

Standalone ABI check only; no production adapter code or firmware is built.
"""
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
header = (root / 'quantum/vial.h').read_text()
vial = (root / 'quantum/vial.c').read_text()
parts = ['#include <stdint.h>', '#ifndef __SDCC_mcs51', '#error Expected mcs51 compiler', '#endif']
for module in ('tap_dance', 'key_override'):
    typ = f'vial_{module}_entry_t'
    parts.append(re.search(r'typedef struct \{[^}]*\} ' + typ + ';', header).group())
    assertion = re.search(r'_Static_assert\(_Alignof\(' + typ + r'\)[^;]*;', vial).group()
    parts.append(assertion)
    parts.append(f'_Static_assert(sizeof({typ}) == 10, "Wire size");')
parts.append('void main(void) {}')
with tempfile.TemporaryDirectory(prefix='vial-alignment-') as temp:
    source = Path(temp) / 'alignment.c'
    source.write_text('\n'.join(parts))
    subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'sdcc', '-mmcs51', '--model-large',
                    '--std-sdcc11', '-c', str(source), '-o', str(Path(temp) / 'alignment.rel')], check=True)
print('PASS: real SDCC mcs51 large-model exact TD/KO type alignment 1 and size 10')
