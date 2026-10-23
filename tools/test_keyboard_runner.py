"""Independent orchestration regressions; no subprocess or device is opened."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location('keyboard_runner_under_test', Path(__file__).with_name('test_keyboard.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class OfflineRunnerTests(unittest.TestCase):
    def run_fixture(self, directory, change=None, profile='legacy-iap'):
        build = directory / 'build'
        build.mkdir(exist_ok=True)
        for suffix in ('ihx', 'map'):
            (build / ('ajazz_ak820_vial.' + suffix)).write_bytes(b'original-' + suffix.encode())
        output = directory / 'report.json'
        cpu_outputs = []
        calls = 0

        def fake_process(command, **kwargs):
            nonlocal calls
            calls += 1
            if '--output-dir' in command:
                target = Path(command[command.index('--output-dir') + 1])
                # Model the strict IAP runner: an existing directory is an
                # error, even when a fresh top-level report was requested.
                self.assertFalse(target.exists(), target)
                target.mkdir()
                cpu_outputs.append(str(target))
            if change and calls == 1:
                (build / ('ajazz_ak820_vial.' + change)).write_bytes(b'changed-during-suite')
            if change and calls == 2:
                # Restore the final file to prove per-suite snapshots detect
                # an intervening mutation that a final-only hash misses.
                (build / ('ajazz_ak820_vial.' + change)).write_bytes(b'original-' + change.encode())
            return types.SimpleNamespace(returncode=0, stdout='mock suite PASS\n')

        with mock.patch.object(sys, 'argv', ['test_keyboard.py', '--build-dir', str(build), '--output', str(output),
                                          '--iap-fault-profile', profile]), \
             mock.patch.object(runner.subprocess, 'run', side_effect=fake_process), \
             contextlib.redirect_stdout(io.StringIO()):
            code = runner.main()
        return code, json.loads(output.read_text()), cpu_outputs

    def test_guarded_erase_profile_reaches_only_iap_and_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, report, _ = self.run_fixture(Path(temporary), profile='guarded-erase')
        self.assertEqual(code, 0)
        self.assertEqual(report['iap_fault_profile'], 'guarded-erase')
        matching = [item['command'] for item in report['tests']
                    if '--iap-fault-profile' in item['command']]
        self.assertEqual(len(matching), 1)
        self.assertIn('tests/ak820_iap/run.py', matching[0])
        self.assertEqual(matching[0][-2:], ['--iap-fault-profile', 'guarded-erase'])

    def test_same_build_and_report_can_run_twice_with_fresh_cpu_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            first_code, first, first_outputs = self.run_fixture(directory)
            second_code, second, second_outputs = self.run_fixture(directory)
            self.assertEqual((first_code, second_code), (0, 0))
            self.assertTrue(first['passed'] and second['passed'])
            self.assertTrue(first['build_unchanged'] and second['build_unchanged'])
            self.assertEqual(len(first_outputs), 5)
            self.assertEqual(len(second_outputs), 5)
            self.assertFalse(set(first_outputs) & set(second_outputs))
            for report in (first, second):
                self.assertEqual(set(report['build_hashes']), {'ihx', 'map'})
                self.assertEqual(report['physical_device_commands'], 0)

    def test_transient_ihx_or_map_mutation_fails_even_after_restoration(self):
        for suffix in ('ihx', 'map'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temporary:
                code, report, _ = self.run_fixture(Path(temporary), change=suffix)
                self.assertEqual(code, 1)
                self.assertFalse(report['passed'])
                self.assertFalse(report['build_unchanged'])
                self.assertTrue(all(test['exit_code'] == 0 for test in report['tests']))
                self.assertNotEqual(report['tests'][0]['build_after'], report['build_hashes'])


if __name__ == '__main__':
    unittest.main()
