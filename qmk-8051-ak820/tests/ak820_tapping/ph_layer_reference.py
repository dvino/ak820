#!/usr/bin/env python3
"""Offline retained non-board QMK lookup boundary; not full action/HID pipeline."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def function(path, name):
    text = (ROOT / path).read_text()
    matches = list(re.finditer(r'^[A-Za-z_][^\n;{}]*\b' + name + r'\([^\n]*\) \{', text, re.M))
    match = matches[-1] if name == 'store_or_get_action' else (matches[0] if matches else None)
    assert match, name
    if name == 'layer_switch_get_layer':
        return text[match.start():text.index('\n#ifdef AK820_BOARD\nuint8_t layer_switch_get_layer', match.start())]
    start = text.index('{', match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[match.start():end]


def source(mutation=None):
    parts = []
    for path, names in [
        ('quantum/keymap_common.c', ['action_for_key', 'action_for_keycode']),
        ('quantum/action_layer.c', ['store_or_get_action', 'layer_switch_get_layer', 'layer_switch_get_action']),
        ('quantum/quantum.c', ['get_record_keycode', 'get_event_keycode', 'pre_process_record_quantum']),
        ('quantum/action.c', ['is_tap_action', 'is_tap_record', 'process_record_tap_hint']),
    ]:
        for name in names:
            body = function(path, name)
            # These functions have board/non-board alternative signatures outside
            # their shared body. Select the retained non-board definition only.
            if name == 'layer_switch_get_layer':
                body = 'uint8_t layer_switch_get_layer(keypos_t key) {\n' + body.split('#endif', 1)[1]
            parts.append(body)
    parts.append(re.sub(r'^#include .*\n', '', (ROOT / 'quantum/action_tapping.c').read_text(), flags=re.M))
    result = '\n'.join(parts)
    if mutation:
        old, new = mutation
        assert result.count(old) == 1, old
        result = result.replace(old, new)
    return result


def build(work, mutation=None):
    (work / 'retained.inc').write_text(source(mutation))
    exe = work / 'reference'
    subprocess.run([os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g',
                    '-Wall', '-Wextra', '-Werror', '-Wno-type-limits',
                    '-fsanitize=undefined', '-fno-sanitize-recover=undefined',
                    '-I' + str(ROOT / 'quantum'), '-I' + str(ROOT / 'quantum/keymap_extras'),
                    '-I' + str(ROOT / 'quantum/sequencer'),
                    '-I' + str(ROOT / 'platforms'),
                    '-I' + str(work), str(HERE / 'ph_layer_reference_harness.c'),
                    '-o', str(exe)], check=True)
    return exe


def run(exe, trace):
    return subprocess.run([str(exe)], input=trace, text=True, capture_output=True, check=True).stdout


class LayerReference(unittest.TestCase):
    def test_retained_lookup(self):
        with tempfile.TemporaryDirectory(prefix='.ph-layer-reference-', dir=HERE) as temp:
            work = Path(temp)
            exe = build(work)
            trace = 'M 0 0 4129\nM 0 1 4\nM 1 0 1\nM 1 1 2205\nE 10 0 1\nS 0\nE 20 1 1\nE 30 1 0\nE 40 0 0\nE 50 1 1\nE 60 1 0\n'
            output = run(exe, trace)
            print(output, end='')
            self.assertEqual(output.splitlines()[:2], ['P 10 10 0 1 4129', 'PENDING LT count=0 interrupted=0 layer=0'])
            self.assertNotIn('OVERFLOW', output)
            self.assertEqual([r for r in output.splitlines() if r.startswith('F ')], [
                'F 10 30 0 1 4129 a129 0 2',
                'F 20 30 1 1 2205 2205 1 2',
                'F 30 30 1 0 2205 2205 1 2',
                'F 40 40 0 0 4129 a129 0 0',
                'F 50 60 1 1 0004 0004 1 0',
                'F 60 60 1 0 0004 0004 1 0'])
            self.assertIn('P 20 20 1 1 0004', output)
            self.assertIn('F 20 30 1 1 2205', output)
            self.assertIn('F 30 30 1 0 2205', output)
            self.assertIn('F 40 40 0 0 4129', output)
            self.assertIn('F 50 60 1 1 0004', output)
            self.assertIn('F 60 60 1 0 0004', output)
            for name, mutation in [
                ('no-ph', ('#        define TAP_GET_PERMISSIVE_HOLD true', '#        define TAP_GET_PERMISSIVE_HOLD false')),
                ('no-refresh', ('get_record_keycode(record, true)', 'get_record_keycode(record, false)')),
            ]:
                with self.subTest(control=name):
                    directory = work / name
                    directory.mkdir()
                    self.assertNotEqual(run(build(directory, mutation), trace), output)

    def check_layer_trace(self, trace, expected, mutation, mutant_row):
        with tempfile.TemporaryDirectory(prefix='.ph-layer-reference-', dir=HERE) as temp:
            work = Path(temp)
            output = run(build(work), trace)
            rows = [line for line in output.splitlines() if line.startswith('F ')]
            self.assertEqual(rows, expected)
            directory = work / 'mutant'
            directory.mkdir()
            # build(check=True) must succeed before the semantic control runs.
            changed = run(build(directory, mutation), trace)
            changed_rows = [line for line in changed.splitlines() if line.startswith('F ')]
            self.assertIn(mutant_row, changed_rows)
            with self.assertRaises(AssertionError):
                self.assertEqual(changed_rows, expected)
            print('baseline:\n' + output + 'compiled semantic mutant:\n' + changed, end='')

    def test_release_cache_after_layer_off(self):
        self.check_layer_trace(
            'M 0 0 4129\nM 1 0 1\nM 0 1 4\nM 1 1 5\nE 10 0 1\nE 220 1 1\nE 230 0 0\nE 240 1 0\n',
            ['F 10 220 0 1 4129 a129 0 2',
             'F 220 220 1 1 0005 0005 0 2',
             'F 230 230 0 0 4129 a129 0 0',
             'F 240 240 1 0 0005 0005 0 0'],
            ('layer = read_source_layers_cache(key);',
             'layer = layer_switch_get_layer(key);'),
            'F 240 240 1 0 0005 0004 0 0')

    def test_transparent_fallback_while_layer_on(self):
        self.check_layer_trace(
            'M 0 0 4129\nM 1 0 1\nM 0 1 4\nM 1 1 1\nE 10 0 1\nE 220 1 1\nE 230 1 0\nE 240 0 0\n',
            ['F 10 220 0 1 4129 a129 0 2',
             'F 220 220 1 1 0004 0004 0 2',
             'F 230 230 1 0 0004 0004 0 2',
             'F 240 240 0 0 4129 a129 0 0'],
            ('if (action.code != ACTION_TRANSPARENT)',
             'if (action.code != ACTION_TRANSPARENT || i == 1)'),
            'F 220 220 1 1 0001 0001 0 2')


if __name__ == '__main__':
    unittest.main(verbosity=2)
