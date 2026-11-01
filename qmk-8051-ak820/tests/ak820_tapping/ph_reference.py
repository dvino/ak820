#!/usr/bin/env python3
"""Offline retained-QMK PH semantics, not candidate firmware qualification."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
QUANTUM = HERE.parents[1] / 'quantum'
CASES = json.loads((HERE / 'ph_reference_cases.json').read_text())


def build(work, quick_tap, mutation=None):
    # Remove includes only; keep every executable statement of the reference.
    source = (QUANTUM / 'action_tapping.c').read_text()
    if mutation:
        old, new = mutation
        if old not in source:
            raise AssertionError(f'Mutation target missing: {old}')
        source = source.replace(old, new)
    (work / 'retained_engine.inc').write_text(
        re.sub(r'^#include .*\n', '', source, flags=re.M))
    exe = work / f'ph-{quick_tap}'
    subprocess.run([
        os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g',
        '-Wall', '-Wextra', '-Werror', '-Wno-type-limits',
        '-fsanitize=undefined', '-fno-sanitize-recover=undefined',
        f'-DQUICK_TAP_TERM={quick_tap}', '-I', str(QUANTUM),
        '-I', str(work), str(HERE / 'ph_reference_harness.c'),
        '-o', str(exe)], check=True)
    return exe


def run(exe, trace):
    return subprocess.run([str(exe)], input=trace, text=True,
                          capture_output=True, check=True).stdout


class ReferenceSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The checkout is executable on hosts where /tmp is mounted noexec.
        cls.temp = tempfile.TemporaryDirectory(prefix='.ph-reference-', dir=HERE)
        cls.addClassCleanup(cls.temp.cleanup)
        work = Path(cls.temp.name)
        cls.executables = {term: build(work, term) for term in (0, 200)}

    def test_exact_event_and_dispatch_traces(self):
        for term, exe in self.executables.items():
            for case in CASES:
                with self.subTest(quick_tap=term, case=case['name']):
                    self.assertEqual(run(exe, case['input']),
                                     case['expected'][str(term)])

    def test_quick_tap_configurations_are_distinguished(self):
        case = next(c for c in CASES if c['name'] == 'mt_repeated_tap')
        outputs = [run(self.executables[t], case['input']) for t in (0, 200)]
        self.assertNotEqual(*outputs)
        # Zero permits a new hold; 200 continues the tap on the second press.
        self.assertIn('120 320 0 1 0 2204 02 0\n', outputs[0])
        self.assertIn('120 120 0 1 2 2204 00 0\n', outputs[1])

    def test_incoming_old_release_bypasses_waiting_head(self):
        for term, exe in self.executables.items():
            for prefix, release_dispatch in [('ordinary', '115'), ('modifier', '120')]:
                case = next(c for c in CASES if c['name'] == f'old_{prefix}_release')
                rows = [row.split() for row in run(exe, case['input']).splitlines()]
                released = next(r for r in rows if r[2:4] == ['0', '0'])
                self.assertEqual(released[:2], ['115', release_dispatch])

    def test_negative_controls(self):
        controls = [
            ('ph-disabled', '#        define TAP_GET_PERMISSIVE_HOLD true',
             '#        define TAP_GET_PERMISSIVE_HOLD false', 'mt_nested'),
            ('late-deadline', '< GET_TAPPING_TERM(', '<= GET_TAPPING_TERM(',
             'mt_deadline_200'),
            ('lost-queued-release-scan', 'waiting_buffer_scan_tap();',
             '(void)waiting_buffer_scan_tap;', 'queued_mt_release_scan'),
        ]
        for name, old, new, case_name in controls:
            with self.subTest(control=name):
                work = Path(self.temp.name) / name
                work.mkdir()
                exe = build(work, 0, (old, new))
                case = next(c for c in CASES if c['name'] == case_name)
                self.assertNotEqual(run(exe, case['input']), case['expected']['0'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
