"""Independent orchestration regressions; no subprocess or device is opened."""
import contextlib
import importlib.util
import io
import json
import os
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
    def run_fixture(self, directory, change=None, profile='legacy-iap', *,
                    suite_output='mock suite PASS\n', required=False, launch_failure=False,
                    host=False, linked=True):
        build = directory / 'build'
        build.mkdir(exist_ok=True)
        for suffix in ('ihx', 'map'):
            (build / ('ajazz_ak820_vial.' + suffix)).write_bytes(b'original-' + suffix.encode())
        output = directory / 'report.json'
        toolchain = directory / 'toolchain'
        (toolchain / 'bin').mkdir(parents=True, exist_ok=True)
        for name in ('sdcc', 's51'):
            (toolchain / 'bin' / name).write_bytes(b'fixture-' + name.encode())
        cpu_outputs = []
        calls = 0

        def fake_process(command, **kwargs):
            nonlocal calls
            calls += 1
            self.assertEqual(kwargs['env']['AK820_SDCC_BIN'], str(toolchain / 'bin'))
            if '--s51' in command:
                self.assertEqual(command[command.index('--s51') + 1], str(toolchain / 'bin/s51'))
            if launch_failure and calls == 1:
                raise FileNotFoundError('synthetic missing command')
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
            return types.SimpleNamespace(returncode=0, stdout=suite_output)

        argv = ['test_keyboard.py', '--output', str(output),
                                          '--iap-fault-profile', profile, '--toolchain', str(toolchain),
                                          *(['--host'] if host else []),
                                          *(['--require-toolchain'] if required else [])]
        if linked:
            argv.extend(['--build-dir', str(build)])
        with mock.patch.object(sys, 'argv', argv), \
             mock.patch.object(runner.subprocess, 'run', side_effect=fake_process), \
             contextlib.redirect_stdout(io.StringIO()):
            code = runner.main()
        return code, json.loads(output.read_text()), cpu_outputs

    def test_selected_toolchain_reaches_all_suites_and_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, report, _ = self.run_fixture(Path(temporary), required=True, host=True)
        self.assertEqual(code, 0)
        self.assertTrue(report['require_toolchain'])
        self.assertEqual(set(report['tools']), {'sdcc', 's51'})
        self.assertTrue(all(len(item['sha256']) == 64 for item in report['tools'].values()))

    def test_required_toolchain_without_host_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit) as result:
                runner.main(['--require-toolchain'])
        self.assertEqual(result.exception.code, 2)
        self.assertIn('--require-toolchain requires --host', errors.getvalue())

    def test_default_uses_current_pinned_pair_without_mutating_process_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bindir = root / 'toolchains/sdcc-4.6.0/bin'
            bindir.mkdir(parents=True)
            for name in ('sdcc', 's51'):
                (bindir / name).write_bytes(name.encode())
            with mock.patch.object(runner, 'ROOT', root), mock.patch.dict(os.environ, {'PATH': '/fixture'}, clear=True):
                env, records = runner.tool_environment(required=True)
                self.assertEqual(env['AK820_SDCC_BIN'], str(bindir))
                self.assertNotIn('AK820_SDCC_BIN', os.environ)
                self.assertEqual(os.environ['PATH'], '/fixture')
                self.assertEqual(records['s51']['path'], str(bindir / 's51'))

    def test_explicit_incomplete_toolchain_is_an_error_not_a_skip(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, 'both bin/sdcc and bin/s51'):
                runner.tool_environment(Path(temporary))

    def test_optional_absent_toolchain_remains_available_offline_but_required_fails(self):
        with tempfile.TemporaryDirectory() as temporary, \
             mock.patch.object(runner, 'ROOT', Path(temporary)), \
             mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(runner.shutil, 'which', return_value=None):
            _, records = runner.tool_environment()
            self.assertEqual(records, {'sdcc': None, 's51': None})
            with self.assertRaisesRegex(ValueError, 'CPU checks are required'):
                runner.tool_environment(required=True)

    def test_skips_are_reported_and_fail_required_qualification(self):
        for required in (False, True):
            with self.subTest(required=required), tempfile.TemporaryDirectory() as temporary:
                code, report, _ = self.run_fixture(Path(temporary), required=required, host=True,
                    suite_output='Ran 4 tests in 0.01s\n\nOK (skipped=2)\n')
                self.assertEqual(code, int(required))
                self.assertEqual(report['unit_tests'], {'run': 4 * len(report['tests']),
                                                        'skipped': 2 * len(report['tests'])})
                self.assertTrue(all(test['exit_code'] == 0 for test in report['tests']))

    def test_launch_failure_is_saved_in_complete_failed_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, report, _ = self.run_fixture(Path(temporary), launch_failure=True)
            self.assertIn('synthetic missing command', Path(report['tests'][0]['log']).read_text())
        self.assertEqual(code, 1)
        self.assertFalse(report['passed'])
        self.assertEqual(report['tests'][0]['exit_code'], 127)

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
            self.assertEqual(len(first_outputs), 8)
            self.assertEqual(len(second_outputs), 8)
            self.assertFalse(set(first_outputs) & set(second_outputs))
            for report in (first, second):
                self.assertEqual(set(report['build_hashes']), {'ihx', 'map'})
                self.assertEqual(report['physical_device_commands'], 0)

    def test_inventory_is_default_but_bounded_host_and_linked_suites_follow_switches(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, report, outputs = self.run_fixture(Path(temporary), linked=False)
        self.assertEqual(code, 0)
        commands = [' '.join(record['command']) for record in report['tests']]
        self.assertTrue(any('ak820_inventory' in command for command in commands))
        self.assertFalse(any('ak820_bounded/run.py' in command for command in commands))
        self.assertFalse(any('ak820_bounded/emitted.py' in command for command in commands))
        self.assertEqual(outputs, [])

        with tempfile.TemporaryDirectory() as temporary:
            code, report, outputs = self.run_fixture(Path(temporary), linked=True)
        self.assertEqual(code, 0)
        commands = [' '.join(record['command']) for record in report['tests']]
        self.assertTrue(any('ak820_bounded/emitted.py' in command for command in commands))
        self.assertEqual(len(outputs), 8)
        self.assertTrue(any('ak820_combo/emitted.py' in command for command in commands))

        with tempfile.TemporaryDirectory() as temporary:
            code, report, _ = self.run_fixture(Path(temporary), host=True)
        self.assertEqual(code, 0)
        commands = [' '.join(record['command']) for record in report['tests']]
        self.assertTrue(any('ak820_inventory' in command for command in commands))
        self.assertTrue(any('ak820_bounded/run.py' in command for command in commands))
        self.assertTrue(any('ak820_macro_guard/parse.py' in command for command in commands))
        self.assertTrue(any('ak820_macro_guard/powercut.py' in command for command in commands))
        tap_dance = next(row['command'] for row in report['tests'] if 'tests/ak820_tap_dance/host.py' in row['command'])
        self.assertEqual(tap_dance[tap_dance.index('--sdcc') + 1], report['tools']['sdcc']['path'])
        self.assertTrue(any('ak820_via_decode/run.py' in command for command in commands))
        self.assertTrue(any('ak820_combo/run.py' in command for command in commands))
        self.assertTrue(any('ak820_repeat/table.py' in command for command in commands))
        cpu = next(row['command'] for row in report['tests'] if 'tests/ak820_repeat/cpu.py' in row['command'])
        self.assertEqual(cpu[cpu.index('--sdcc') + 1], report['tools']['sdcc']['path'])
        self.assertEqual(cpu[cpu.index('--simulator') + 1], report['tools']['s51']['path'])
        self.assertEqual(report['repeat_cpu_check'], 'passed')
        macro_cpu = next(row['command'] for row in report['tests'] if 'tests/ak820_macro_guard/cpu.py' in row['command'])
        self.assertEqual(macro_cpu[macro_cpu.index('--sdcc') + 1], report['tools']['sdcc']['path'])
        self.assertEqual(macro_cpu[macro_cpu.index('--simulator') + 1], report['tools']['s51']['path'])
        self.assertEqual(report['macro_cpu_check'], 'passed')
        td_cpu = next(row['command'] for row in report['tests'] if 'tests/ak820_tap_dance/cpu.py' in row['command'])
        self.assertEqual(td_cpu[td_cpu.index('--sdcc') + 1], report['tools']['sdcc']['path'])
        self.assertEqual(td_cpu[td_cpu.index('--simulator') + 1], report['tools']['s51']['path'])
        self.assertEqual(report['tap_dance_cpu_check'], 'passed')
        tapping = next(row['command'] for row in report['tests'] if 'tests/ak820_tapping/run.py' in row['command'])
        self.assertIn('--negative-controls', tapping)
        self.assertIn('--output', tapping)

    def test_missing_toolchain_reports_repeat_cpu_skip(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            env = {'AK820_SDCC_BIN': str(directory / 'toolchain/bin')}
            with mock.patch.object(runner, 'tool_environment', return_value=(env, {'sdcc': None, 's51': None})):
                code, report, _ = self.run_fixture(directory, host=True, linked=False)
        self.assertEqual(code, 0)
        self.assertEqual(report['repeat_cpu_check'], 'skipped: SDCC or s51 unavailable')
        self.assertEqual(report['macro_cpu_check'], 'skipped: SDCC or s51 unavailable')
        self.assertEqual(report['tap_dance_cpu_check'], 'skipped: SDCC or s51 unavailable')
        tap_dance = next(row['command'] for row in report['tests'] if 'tests/ak820_tap_dance/host.py' in row['command'])
        self.assertNotIn('--sdcc', tap_dance)
        self.assertFalse(any('tests/ak820_repeat/cpu.py' in row['command'] for row in report['tests']))
        self.assertFalse(any('tests/ak820_macro_guard/cpu.py' in row['command'] for row in report['tests']))
        self.assertFalse(any('tests/ak820_tap_dance/cpu.py' in row['command'] for row in report['tests']))

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
