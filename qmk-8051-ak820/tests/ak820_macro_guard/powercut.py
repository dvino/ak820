#!/usr/bin/env python3
"""Run the production macro upload/NVM power-cut fixture without a device."""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
board = root / 'keyboards/ajazz/ak820'
with tempfile.TemporaryDirectory(prefix='ak820-macro-powercut-') as folder:
    binary = Path(folder) / 'test'
    cc = os.environ.get('CC', 'cc')
    sanitizer_flags = ['-fsanitize=address,undefined', '-fno-sanitize-recover=undefined', '-fno-omit-frame-pointer']
    negative = Path(folder) / 'negative.c'
    negative.write_text('#include <limits.h>\nint main(void) { volatile int x = INT_MAX; return (x + 1) == 0; }\n')
    subprocess.run([cc, '-std=c11', '-O1', *sanitizer_flags, str(negative), '-o', str(Path(folder) / 'negative')], check=True)
    env = os.environ.copy()
    env['ASAN_OPTIONS'] = 'detect_leaks=0'
    control = subprocess.run([str(Path(folder) / 'negative')], env=env, text=True, capture_output=True)
    if control.returncode == 0 or 'runtime error:' not in control.stderr:
        raise RuntimeError('UBSan negative control did not fail with a runtime-error diagnostic')
    command = [cc, '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror',
               '-Wno-clobbered', '-Wno-int-to-pointer-cast', *sanitizer_flags,
               '-DAK820_BOARD=', '-I' + str(board / 'tests/include'),
               '-I' + str(board), str(board / 'tests/macro_powercut.c'), str(board / 'ak820_macro.c'),
               str(board / 'ak820_nvm.c'), str(board / 'ak820_crc.c'), '-o', str(binary)]
    subprocess.run(command, check=True)
    subprocess.run([str(binary)], check=True, env=env)
