#!/usr/bin/env python3
"""Isolated production callback host diagnostic; no PH or SDCC safety proof."""
import ast
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def production():
    # Reuse the existing fixture's extraction recipe without executing its CLI.
    tree = ast.parse((HERE / 'run.py').read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('function', 'stripped')]
    start = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'parts' for t in n.targets))
    end = next(i for i in range(start, len(tree.body)) if isinstance(tree.body[i], ast.With))
    scope = dict(ROOT=ROOT, re=re)
    exec(compile(ast.Module(body=nodes + tree.body[start:end], type_ignores=[]), str(HERE / 'run.py'), 'exec'), scope)
    parts = scope['parts']
    for name in ('ak820_autoshift', 'ak820_tap_dance'):
        parts.append(scope['stripped']('keyboards/ajazz/ak820/' + name + '.c'))
    parts.append(scope['function']('quantum/via.c', 'process_record_via'))
    source = '\n'.join(parts)
    for signature, replacement in [
        ('void action_exec(keyevent_t event) {', 'void body_action_exec(keyevent_t event) {'),
        ('void process_record(keyrecord_t AK820_RECORD_MEM *record_argument) {', 'void body_process_record(keyrecord_t AK820_RECORD_MEM *record_argument) {'),
    ]:
        assert source.count(signature) == 1, signature
        source = source.replace(signature, replacement)
    return source


def main():
    harness = (HERE / 'harness.c').read_text().split('int main(int argc,char **argv) {')[0]
    extra = (HERE / 'continuations_harness.c').read_text()
    # Declarations precede extracted production; instrumentation follows it.
    declarations, tests = extra.split('/* CALLBACK TESTS */')
    harness = harness.replace('/* PRODUCTION */', declarations + '\n' + production()) + tests
    with tempfile.TemporaryDirectory(prefix='.continuations-', dir=HERE) as directory:
        work = Path(directory)
        (work / 'protocol').mkdir()
        (work / 'protocol/usb_descriptor.h').write_text('#define SHARED_EPSIZE 32\n')
        (work / '_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
        src = work / 'test.c'
        src.write_text(harness)
        exe = work / 'test'
        cmd = [os.environ.get('CC', 'cc'), '-std=gnu11', '-O1', '-g', '-ffunction-sections', '-fdata-sections', '-Wl,--gc-sections', '-Wno-implicit-function-declaration', '-Wno-unused-function', '-Wno-unknown-pragmas', '-Wno-int-to-pointer-cast', '-fsanitize=undefined', '-fno-sanitize-recover=undefined']
        cmd += ['-D' + d for d in ('MAX_LAYER=6', 'CAPS_WORD_ENABLE', 'GRAVE_ESC_ENABLE', 'VIAL_ENABLE', 'EEPROM_CUSTOM', 'PROTOCOL_CH555', 'NKRO_ENABLE', 'REPEAT_KEY_ENABLE', 'TRI_LAYER_ENABLE', 'ENCODER_MAP_ENABLE', 'EXTRAKEY_ENABLE', 'NO_RESET', 'AK820_COMPACT_AUTOSHIFT', 'AK820_COMPACT_TAP_DANCE', 'VIA_ENABLE')]
        cmd += ['-include', str(ROOT / 'keyboards/ajazz/ak820/config.h')]
        cmd += ['-I' + str(p) for p in (work, ROOT / 'keyboards/ajazz/ak820', ROOT / 'quantum', ROOT / 'quantum/keymap_extras', ROOT / 'quantum/sequencer', ROOT / 'quantum/send_string', ROOT / 'quantum/process_keycode', ROOT / 'platforms', ROOT / 'tmk_core/protocol', ROOT)]
        cmd += [str(src), '-o', str(exe)]
        subprocess.run(cmd, check=True)
        subprocess.run([str(exe)], check=True)
        # A compiled semantic mutant, not a compiler failure, must be detected.
        old = 'registered_record = last_record;'
        assert harness.count(old) == 1
        src.write_text(harness.replace(old, 'registered_record = last_record; registered_record.keycode = KC_NO;'))
        subprocess.run(cmd, check=True, capture_output=True)
        result = subprocess.run([str(exe)], capture_output=True)
        assert result.returncode != 0 and b'Assertion' in result.stderr, result
        print('PASS: compiled Repeat-identity mutant rejected by assertion')


if __name__ == '__main__':
    main()
