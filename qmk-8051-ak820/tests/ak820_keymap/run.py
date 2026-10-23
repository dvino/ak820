#!/usr/bin/env python3
"""Offline VIA keymap regression against the current dispatcher and NVM code."""
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def definition(path, name):
    source = (ROOT / path).read_text()
    match = re.search(r'^(?:static )?[\w *]+\b' + name + r'\([^\n]*\) \{', source, re.M)
    if not match:
        raise ValueError('Missing production function: ' + name)
    return source[match.start():source.index('\n}', match.end()) + 2]


def main():
    via = (ROOT / 'quantum/via.h').read_text()
    enums = [re.search(r'enum ' + name + r' \{.*?\n\};', via, re.S).group(0)
             for name in ('via_command_id', 'via_keyboard_value_id')]
    functions = [definition('quantum/dynamic_keymap.c', name) for name in (
        'dynamic_keymap_key_to_eeprom_address', 'dynamic_keymap_get_keycode',
        'dynamic_keymap_set_keycode', 'dynamic_keymap_reset', 'ak820_dynamic_read_buffer',
        'dynamic_keymap_get_buffer', 'dynamic_keymap_set_buffer',
        'dynamic_keymap_macro_get_buffer')]
    functions += [definition('quantum/via.c', name) for name in ('via_eeprom_is_valid', 'via_init', 'raw_hid_receive')]
    source = (HERE / 'harness.c').read_text().replace('/* AK820_ACTUAL_SOURCE */', '\n'.join(enums + functions))
    board = ROOT / 'keyboards/ajazz/ak820'
    with tempfile.TemporaryDirectory(prefix='ak820-keymap-') as temp:
        work = Path(temp)
        (work / 'host.c').write_text(source)
        command = [os.environ.get('CC', 'cc'), '-std=c11', '-O1', '-g', '-Wall', '-Wextra',
                   '-Werror', '-Wno-int-to-pointer-cast', '-Wno-unused-parameter',
                   '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                   '-DEEPROM_CUSTOM', '-include', str(board / 'config.h'),
                   '-I' + str(board), '-I' + str(ROOT / 'platforms'),
                   '-I' + str(ROOT / 'drivers/eeprom'), str(work / 'host.c'),
                   str(board / 'ak820_nvm.c'), str(board / 'ak820_macro.c'),
                   str(ROOT / 'drivers/eeprom/eeprom_driver.c'), '-o', str(work / 'host')]
        subprocess.run(command, check=True)
        env = os.environ.copy()
        env['ASAN_OPTIONS'] = 'detect_leaks=0'
        subprocess.run([str(work / 'host')], check=True, env=env)


if __name__ == '__main__':
    main()
