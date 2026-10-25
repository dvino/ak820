#!/usr/bin/env python3
"""Run production settings against the offline checked-storage fixture."""
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='ak820-settings-') as tmp:
    for autoshift in (False, True):
        binary = Path(tmp) / ('host-as' if autoshift else 'host')
        command = ['cc', '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror',
                   '-fsanitize=undefined', '-fno-sanitize-recover=undefined']
        if autoshift:
            command += ['-DAK820_COMPACT_AUTOSHIFT']
        command += ['-I', str(ROOT / 'keyboards/ajazz/ak820'),
                    str(ROOT / 'util/test_ak820_settings.c'),
                    str(ROOT / 'keyboards/ajazz/ak820/ak820_settings.c'), str(ROOT / 'keyboards/ajazz/ak820/ak820_crc.c'), '-o', str(binary)]
        subprocess.run(command, check=True)
        subprocess.run([str(binary)], check=True)
