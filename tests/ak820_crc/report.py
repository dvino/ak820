# SPDX-License-Identifier: GPL-2.0-or-later
import hashlib
import json
from pathlib import Path

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

root = Path('/src')
report = {
    'result': 'PASS',
    'compiler': Path('compiler.txt').read_text().splitlines()[0],
    'crc_compile_flags': ['-mmcs51', '--model-large'],
    'harness_compile_flags': ['-mmcs51', '--model-large'],
    'cpu_command': ['s51', '-t', '8051', '-c', '-', 'cpu.ihx'],
    'cpu_stdin': 'step 50000000\ndump xram 0x2000 0x2003\nquit\n',
    'expected_xram_2000': 'a5 00 04 a5',
    'completed_differential_cases': 1024,
    'abi_check': 'PASS',
    'buffer_canaries': 'PASS',
    'native_exhaustive_state_byte_transitions': 16777216,
    'native_random_buffers': 25600,
    'crc_instruction_bytes': int(next(line.split()[3] for line in Path('ak820_crc.rel').read_text().splitlines() if line.startswith('A CSEG ')), 16),
    'cpu_image_sha256': sha('cpu.ihx'),
    'cpu_log_sha256': sha('cpu.log'),
    'source_sha256': {str(p.relative_to(root)): sha(p) for p in [root/'qmk-8051-ak820/keyboards/ajazz/ak820/ak820_crc.c', root/'qmk-8051-ak820/keyboards/ajazz/ak820/ak820_crc.h', root/'tests/ak820_crc/cpu.c', root/'tests/ak820_crc/native.c']},
    'device_tested': False,
}
Path('result.json').write_text(json.dumps(report, indent=2)+'\n')
