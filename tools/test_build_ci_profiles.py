import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_ci_profiles as profiles
import ak820_profiles


class ProfileBuildOrchestrationTests(unittest.TestCase):
    def test_fresh_context_and_final_qualification_are_required_per_profile(self):
        self.exercise_profiles()

    def test_selected_profile_retains_all_qualification_steps(self):
        self.exercise_profiles(('game',))

    def test_multiple_selections_use_catalog_order(self):
        self.exercise_profiles(('game', 'main'))

    def test_incomplete_or_foreground_only_proof_is_rejected(self):
        for proof in ({'whole_program_qualified': True}, {'whole_program_stack_qualified': False}):
            with self.subTest(proof=proof), self.assertRaisesRegex(ValueError, 'incomplete'):
                self.exercise_profiles(('main',), runtime_result=proof)

    def exercise_profiles(self, selected=None, runtime_result=None):
        expected = tuple(name for name in ak820_profiles.RELEASE_PROFILES
                         if selected is None or name in selected)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            qmk = root / 'qmk-8051-ak820'; qmk.mkdir()
            toolchain = root / 'toolchain'; toolchain.mkdir()
            qmk_bin = root / '.venv/bin/qmk'; qmk_bin.parent.mkdir(parents=True); qmk_bin.write_text('qmk')
            python = root / '.venv/bin/python'; python.write_text('python')
            builds, bootstraps = qmk / '.build/ci-profiles', qmk / '.build/bootstrap'
            calls = []

            def run(command, **kwargs):
                calls.append(command)
                build_arg = command[command.index('--build-dir') + 1]
                build = Path(build_arg)
                if command[1].endswith('build_ak820.py'):
                    build.mkdir(parents=True)
                    (build / 'ajazz_ak820_vial.ihx').write_bytes(b'bootstrap image')
                    (build / 'ajazz_ak820_vial.map').write_bytes(b'bootstrap map')
                    return
                build.mkdir(parents=True)
                name = command[command.index('--profile') + 1]
                (build / 'configuration-report.json').write_text(json.dumps({
                    'configuration': ak820_profiles.configuration(name),
                    'offline_tests_passed': True,
                    'runtime_analysis': runtime_result if runtime_result is not None else {'whole_program_stack_qualified': True},
                    'identity': {'profile': name},
                }))
                (build / 'qualification.json').write_text('{}')
                (build / 'profile-tests').mkdir()
                (build / 'profile-tests/results.json').write_text('{}')

            def make_context(_root, _build, _stack, _toolchain, output):
                output.write_text('{}')

            with patch.object(profiles, 'QMK', qmk), patch.object(
                    profiles.configure_firmware, 'validate_tools', return_value=toolchain), \
                 patch.object(profiles.configure_firmware, 'run_runtime_analysis') as runtime, \
                 patch.object(profiles.ak820_parameter_spills, 'make_context_certificate',
                              side_effect=make_context) as context, \
                 patch.object(profiles.subprocess, 'run', side_effect=run):
                result = profiles.build_all(builds, bootstraps, toolchain, qmk_bin, python, selected)

            self.assertEqual(tuple(result['profiles']), expected)
            self.assertEqual(result['selected_profiles'], list(expected))
            self.assertEqual(len(calls), 2 * len(expected))
            self.assertEqual(runtime.call_count, len(expected))
            self.assertEqual(context.call_count, len(expected))
            for seed in (call for call in calls if call[1].endswith('build_ak820.py')):
                self.assertNotIn('--trim-parameter-spills', seed)
                self.assertEqual(seed[seed.index('--code-end') + 1], '0xe000')
                for option in ('--compress-default-keymap', '--short-calls',
                               '--nvm-update-block-asm', '--nvm-read-block-asm',
                               '--keymap-words-asm', '--trim-register-saves', '--tail-share'):
                    self.assertIn(option, seed)
                self.assertEqual(seed[seed.index('--outline-max-helpers') + 1], '400')
            for name in expected:
                final = [call for call in calls if call[1].endswith('configure_firmware.py')
                         and call[call.index('--profile') + 1] == name][0]
                self.assertIn('--parameter-spills-context', final)
                self.assertEqual(Path(final[final.index('--build-dir') + 1]), builds / name)

    def test_invalid_or_duplicate_selections_fail_before_building(self):
        for selected in ((), ('work',), ('main', 'main'), ('../main',)):
            with self.subTest(selected=selected), patch.object(
                    profiles.configure_firmware, 'validate_tools') as tools, \
                 patch.object(profiles.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'distinct canonical'):
                    profiles.build_all(Path('build'), Path('seed'), Path('toolchain'),
                                       Path('qmk'), Path('python'), selected)
                tools.assert_not_called()
                run.assert_not_called()

    def test_preexisting_output_root_fails_before_any_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            qmk = root / 'qmk'; qmk.mkdir()
            builds = qmk / 'builds'; builds.mkdir()
            bootstraps = qmk / 'bootstrap'
            toolchain = root / 'toolchain'; toolchain.mkdir()
            qmk_bin = root / 'qmk-bin'; qmk_bin.write_text('qmk')
            python = root / 'python'; python.write_text('python')
            with patch.object(profiles, 'QMK', qmk), \
                 patch.object(profiles.configure_firmware, 'validate_tools', return_value=toolchain), \
                 patch.object(profiles.subprocess, 'run') as run, \
                 self.assertRaisesRegex(ValueError, 'fresh directories'):
                profiles.build_all(builds, bootstraps, toolchain, qmk_bin, python)
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
