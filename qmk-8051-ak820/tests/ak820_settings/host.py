#!/usr/bin/env python3
"""Run production settings against the offline checked-storage fixture."""
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='ak820-settings-') as tmp:
    for autoshift, oneshot, leader in ((a, o, l) for a in (False, True) for o in (False, True) for l in (False, True)):
        binary = Path(tmp) / f'host-as{autoshift}-os{oneshot}-leader{leader}'
        command = ['cc', '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror',
                   '-fsanitize=undefined', '-fno-sanitize-recover=undefined']
        if autoshift:
            command += ['-DAK820_COMPACT_AUTOSHIFT']
        if oneshot:
            command += ['-DAK820_COMPACT_ONESHOT']
        command += ['-DCAPS_WORD_ENABLE']
        if leader:
            command += ['-DAK820_COMPACT_LEADER', '-DAK820_LEADER_TIMEOUT=517']
        command += ['-I', str(ROOT / 'keyboards/ajazz/ak820'),
                    str(ROOT / 'util/test_ak820_settings.c'),
                    str(ROOT / 'keyboards/ajazz/ak820/ak820_settings.c'), str(ROOT / 'keyboards/ajazz/ak820/ak820_crc.c'), '-o', str(binary)]
        print(f'autoshift={int(autoshift)} oneshot={int(oneshot)} leader={int(leader)}', flush=True)
        subprocess.run(command, check=True)
        subprocess.run([str(binary)], check=True)
