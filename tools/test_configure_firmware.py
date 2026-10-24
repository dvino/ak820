"""Negative controls for profile selection, protected memory and approval."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import configure_firmware as config


class ProfileTests(unittest.TestCase):
    def test_short_call_proof_cannot_be_removed_or_unbound(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build = root/'build'; build.mkdir()
            image = build/'ajazz_ak820_vial.ihx'; image.write_text('fixture')
            with patch.object(config, 'QMK', root):
                self.assertIsNone(config.check_short_calls({},build,image))
                (build/'shortcalls-input').mkdir()
                with self.assertRaisesRegex(ValueError,'Missing opt-in'):
                    config.check_short_calls({},build,image)
                (root/'util').mkdir(); (root/'util/ak820_shortcalls.py').write_text('fixture')
                report = {'short_calls':{}, 'shortcalls_sha256':config.sha(root/'util/ak820_shortcalls.py'),
                          'artifacts':[]}
                with self.assertRaisesRegex(ValueError,'Missing or ambiguous'):
                    config.check_short_calls(report,build,image)

    def test_new_runtime_features_require_their_exact_suites(self):
        for name in config.profiles.PROFILES:
            features = config.profiles.configuration(name)['optional_features']
            plan = config.profile_test_plan(name, Path('/build'), Path('/toolchain'))
            identifiers = [identifier for identifier, _, _ in plan]
            self.assertEqual(len(identifiers), len(set(identifiers)))
            for feature, prefix in (('dynamic-macros', 'dynamic-macro'), ('gui-lock', 'gui-lock')):
                for suffix in ('host', 'linked'):
                    self.assertEqual(prefix + '-' + suffix in identifiers, feature in features)

    def test_exact_named_combinations_and_no_inherited_switches(self):
        for name, features in config.profiles.PROFILES.items():
            self.assertEqual(config.profiles.select(list(features)), name)
            value = config.profiles.configuration(name)
            self.assertEqual(set(value['make_options']), set(config.profiles.SWITCHES.values()))
            self.assertFalse(value['release_approved'])

    def test_unknown_duplicate_and_unimplemented_choices_fail(self):
        for features in (['one-shot', 'one-shot'], ['mouse-keys'], ['QMK_SETTINGS=yes'], ['no-combos']):
            with self.assertRaises(ValueError):
                config.profiles.select(features)
        self.assertEqual(config.profiles.select(['nkro-control', 'one-shot']), 'nkro-one-shot')
        self.assertEqual(config.profiles.select(['space-cadet', 'one-shot', 'nkro-control']), 'full')
        for value in (None, {}, {'profile': 'unknown'}, {'profile': 'standard', 'release_approved': True}):
            with self.assertRaises(ValueError):
                config.profiles.validate_configuration(value)

    def test_same_schema_does_not_approve_a_different_feature_set(self):
        legacy = {'build_id': config.profiles.SCHEMA,
                  'builder_sha256': next(iter(config.profiles.LEGACY_BUILDERS))}
        config.profiles.require_release_qualification(legacy)
        for name in config.profiles.PROFILES:
            report = {**legacy, 'configuration': config.profiles.configuration(name)}
            with self.assertRaisesRegex(ValueError, 'not approved'):
                config.profiles.require_release_qualification(report)

    def test_deleting_configuration_does_not_make_a_current_build_legacy(self):
        import build_release_bundle
        import build_ci_release
        for report in ({'builder_sha256': config.sha(config.QMK / 'util/build_ak820.py')},
                       {'builder_sha256': next(iter(config.profiles.LEGACY_BUILDERS)),
                        'sources': [{'origin': 'source', 'path': 'util/ak820_profiles.py'}]}, {}):
            for guard in (build_release_bundle.require_release_qualification,
                          build_ci_release.require_release_qualification):
                with self.assertRaisesRegex(ValueError, 'not legacy provenance'):
                    guard(report)

    def test_caller_supplied_stack_numbers_cannot_approve_packaging(self):
        forged = {'release_approved': True, 'stack_bound': 1, 'stack_margin': 159}
        with self.assertRaisesRegex(ValueError, 'No profile is approved'):
            config.require_release_approval(forged)

    def test_rejection_survives_python_optimization(self):
        code = ('import sys; sys.path.insert(0, sys.argv[1]); '
                'import configure_firmware as c; c.require_release_approval({"release_approved": True})')
        result = subprocess.run([sys.executable, '-O', '-c', code, str(HERE)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No profile is approved', result.stderr)

    def test_profile_suite_contract_rejects_omitted_duplicate_and_wrong_image(self):
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            (build / 'profile-tests').mkdir()
            toolchain = build / 'toolchain'
            identity = {'ihx_sha256': 'image', 'profile': 'one-shot'}
            rows = []
            for name, cwd, command in config.profile_test_plan('one-shot', build, toolchain):
                log = build / 'profile-tests' / (name + '.log')
                log.write_text('Ran 10 tests in 0.1s\n\nOK\n')
                rows.append({'id': name, 'cwd': str(cwd), 'command': command, 'exit_code': 0,
                             'build_before': identity, 'build_after': identity, 'log_sha256': config.sha(log)})
            report = {'format': 'ak820-profile-tests-1', 'profile': 'one-shot', 'identity': identity,
                      'passed': True, 'hardware_validated': False, 'physical_device_commands': 0,
                      'source_files': {'fixture': 'source'}, 'tests': rows}
            with patch.object(config, 'test_source_snapshot', return_value={'fixture': 'source'}):
                config.validate_profile_tests(report, 'one-shot', identity, build, toolchain)
                bad = copy.deepcopy(report); bad['tests'].pop()
                with self.assertRaisesRegex(ValueError, 'omitted or duplicated'):
                    config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                bad = copy.deepcopy(report); bad['tests'][-1] = bad['tests'][0]
                with self.assertRaisesRegex(ValueError, 'identity, arguments'):
                    config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                bad = copy.deepcopy(report); bad['tests'][-1]['build_after'] = {'ihx_sha256': 'different'}
                with self.assertRaisesRegex(ValueError, 'identity, arguments'):
                    config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                bad = copy.deepcopy(report)
                next(row for row in bad['tests'] if row['id'] == 'one-shot-host')['command'].remove('--oneshot')
                with self.assertRaisesRegex(ValueError, 'identity, arguments'):
                    config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                short_log = build / 'profile-tests/short-call-gates.log'
                original = short_log.read_text()
                for text in ('Ran 0 tests in 0.1s\n\nOK\n',
                             'Ran 15 tests in 0.1s\n\nOK (skipped=1)\n'):
                    short_log.write_text(text)
                    bad = copy.deepcopy(report)
                    next(row for row in bad['tests'] if row['id'] == 'short-call-gates')['log_sha256'] = config.sha(short_log)
                    with self.assertRaisesRegex(ValueError, 'empty or skipped'):
                        config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                short_log.write_text(original)

    def test_inline_feature_is_bound_to_exact_compiler_flags(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build = root / 'candidate'
            flags = build / 'obj_ajazz_ak820_vial/cflags.txt'
            flags.parent.mkdir(parents=True)
            selected = config.profiles.configuration('full')
            text = ' '.join('-D' + config.profiles.SWITCHES[feature]
                            for feature in selected['optional_features'])
            def report(value):
                flags.write_text(value)
                return {'artifacts': [{'path': flags.relative_to(root).as_posix(),
                                       'sha256': config.sha(flags), 'size': flags.stat().st_size}]}
            with patch.object(config, 'QMK', root):
                valid = report(text)
                config.check_feature_defines(valid, build, selected)
                for value in (text.replace('-DAK820_COMPACT_SPACE_CADET', ''),
                              text + ' -UAK820_COMPACT_SPACE_CADET',
                              text + ' -DAK820_COMPACT_SPACE_CADET',
                              text + ' -DAK820_COMPACT_MOUSEKEY',
                              text.replace('-DAK820_COMPACT_SPACE_CADET', '-DAK820_COMPACT_SPACE_CADET=0')):
                    with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'feature flag'):
                        config.check_feature_defines(report(value), build, selected)
                valid = report(text)
                flags.write_text(text + ' -UAK820_COMPACT_SPACE_CADET')
                with self.assertRaisesRegex(ValueError, 'Unbound'):
                    config.check_feature_defines(valid, build, selected)

    def test_combined_options_run_interaction_and_inline_checks(self):
        plan = config.profile_test_plan('full', Path('/tmp/full'), Path('/tmp/sdcc'))
        commands = {name: command for name, _, command in plan}
        self.assertIn('--oneshot', commands['one-shot-host'])
        self.assertIn('--space-cadet', commands['one-shot-host'])
        for required in ('outline-gates', 'stack-gates', 'outline-integrity', 'vialrgb-linked',
                         'startup-gates', 'startup-stack', 'irq-gates', 'release-safety-gates',
                         'nkro-control-linked', 'one-shot-linked'):
            self.assertIn(required, commands)

    def test_mouse_profile_runs_exact_pipeline_and_host_suites(self):
        plan = config.profile_test_plan('full-mouse', Path('/tmp/mouse'), Path('/tmp/sdcc'))
        commands = {name: command for name, _, command in plan}
        for name in ('mouse-keys-host', 'mouse-keys-linked', 'nkro-control-linked', 'one-shot-linked'):
            self.assertIn(name, commands)
        self.assertNotIn('--diagnostic-overflow', commands['mouse-keys-linked'])
        self.assertEqual(config.profiles.select(['nkro-control', 'one-shot', 'space-cadet', 'mouse-keys']),
                         'full-mouse')

    def test_auto_shift_profile_keeps_full_features_and_owns_timing(self):
        profile = config.profiles.configuration('full-auto-shift')
        self.assertEqual(profile['optional_features'], ['nkro-control', 'one-shot', 'space-cadet', 'auto-shift'])
        self.assertEqual(profile['timing_ms']['auto_shift'], 175)
        commands = {name: command for name, _, command in
                    config.profile_test_plan('full-auto-shift', Path('/tmp/as'), Path('/tmp/sdcc'))}
        for name in ('auto-shift-host', 'auto-shift-linked', 'nkro-control-linked', 'one-shot-linked', 'core-compact-host'):
            self.assertIn(name, commands)

    def test_combined_mouse_auto_shift_requires_both_feature_suites(self):
        name = 'full-mouse-auto-shift'
        profile = config.profiles.configuration(name)
        self.assertEqual(set(profile['optional_features']),
                         {'nkro-control', 'one-shot', 'space-cadet', 'mouse-keys', 'auto-shift'})
        self.assertEqual(config.profiles.select(profile['optional_features']), name)
        commands = {test: command for test, _, command in
                    config.profile_test_plan(name, Path('/tmp/combined'), Path('/tmp/sdcc'))}
        for required in ('mouse-keys-host', 'mouse-keys-linked', 'auto-shift-host',
                         'auto-shift-linked', 'nkro-control-linked', 'one-shot-linked'):
            self.assertIn(required, commands)
        self.assertNotIn('--diagnostic-overflow', commands['mouse-keys-linked'])

    def test_short_call_controls_are_required_in_every_profile(self):
        for name in config.profiles.PROFILES:
            commands = {test: command for test, _, command in
                        config.profile_test_plan(name, Path('/tmp/profile'), Path('/tmp/sdcc'))}
            self.assertEqual(commands['short-call-gates'][1:],
                             ['-B', '-m', 'unittest', 'discover', '-s',
                              'tests/ak820_shortcalls', '-p', 'test_*.py'])

    def test_profile_suites_receive_validated_custom_tool_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            build=Path(directory)/'build';build.mkdir()
            toolchain=Path(directory)/'external-sdcc'
            identity={'ihx_sha256':'fixture'}
            observed=[]
            def run(command, **kwargs):
                observed.append(kwargs['env'])
                kwargs['stdout'].write('Ran 1 test in 0.001s\n\nOK\n')
                return subprocess.CompletedProcess(command,0)
            with patch.dict(os.environ,{'AK820_SDCC_BIN':'stale-inherited-path'}), \
                 patch.object(config,'profile_test_plan',return_value=[('short-call-gates',build,['fixture'])]), \
                 patch.object(config,'test_source_snapshot',return_value={}), \
                 patch.object(config,'inspect',return_value={'identity':identity}), \
                 patch.object(config,'validate_profile_tests'), \
                 patch.object(config.subprocess,'run',side_effect=run):
                config.run_profile_tests('standard',build,toolchain,identity)
                self.assertEqual(os.environ['AK820_SDCC_BIN'],'stale-inherited-path')
            self.assertEqual(len(observed),1)
            self.assertEqual(observed[0]['AK820_SDCC_BIN'],str((toolchain/'bin').resolve()))

    def runtime_fixture(self, build):
        return {'identity': {'ihx_sha256': 'image', 'map_sha256': 'map'},
                'analyzer_sha256': config.sha(config.QMK / 'tests/ak820_stack/analyze.py'),
                'decoder_source_sha256': config.sha(config.QMK / 'util/ak820_linked_inventory.py'),
                'whole_program_qualified': False,
                'roots': {'_main': {'bound': None}, '_ak820_led_irq': {'bound': None},
                          '_ak820_timer_irq': {'bound': 2}, '_USB_DeviceInterrupt': {'bound': 6}}}

    def invoke_runtime_fixture(self, build, report, status=2):
        def run(*args, **kwargs):
            (build / 'runtime-stack.json').write_text(json.dumps(report))
            return subprocess.CompletedProcess(args[0], status)
        with patch.object(config.subprocess, 'run', side_effect=run):
            return config.run_runtime_analysis(build, {'ihx_sha256': 'image', 'map_sha256': 'map'})

    def test_runtime_analysis_preserves_unknown_bounds_without_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            result = self.invoke_runtime_fixture(build, self.runtime_fixture(build))
            self.assertFalse(result['whole_program_qualified'])
            self.assertEqual(set(result['unresolved_roots']), {'_main', '_ak820_led_irq'})
            self.assertIsNone(result['root_bounds']['_main'])
            self.assertEqual(result['report_sha256'], config.sha(build / 'runtime-stack.json'))

    def test_runtime_analysis_rejects_wrong_image_sources_and_forged_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            mutations = [('identity', 'ihx_sha256', 'wrong image'),
                         ('identity', 'map_sha256', 'wrong map'),
                         (None, 'analyzer_sha256', 'wrong analyzer'),
                         (None, 'decoder_source_sha256', 'wrong decoder'),
                         (None, 'whole_program_qualified', True)]
            for section, key, value in mutations:
                report = self.runtime_fixture(build)
                (report[section] if section else report)[key] = value
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'differs from this image'):
                    self.invoke_runtime_fixture(build, report)

    def test_runtime_analysis_rejects_missing_root_and_inconsistent_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            report = self.runtime_fixture(build)
            del report['roots']['_ak820_led_irq']
            with self.assertRaisesRegex(ValueError, 'omitted a required root'):
                self.invoke_runtime_fixture(build, report)
            with self.assertRaisesRegex(ValueError, 'exit status disagrees'):
                self.invoke_runtime_fixture(build, self.runtime_fixture(build), 0)
            report = self.runtime_fixture(build)
            for value in report['roots'].values():
                value['bound'] = 2
            with self.assertRaisesRegex(ValueError, 'exit status disagrees'):
                self.invoke_runtime_fixture(build, report, 2)
            with self.assertRaisesRegex(ValueError, 'analysis failed'):
                self.invoke_runtime_fixture(build, self.runtime_fixture(build), 1)

    def test_duplicate_json_and_fake_success_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            for content in ('{"passed":false,"passed":true}', '{"bound":NaN}'):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    config.load_json(path)

    def test_deleted_extra_or_duplicate_relocated_listing_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'
            (build / 'dce').mkdir(parents=True)
            listing = build / 'dce/fixture.rst'
            listing.write_text('  003027 22 [24] 1 ret\n')
            record = {'path': 'build/dce/fixture.rst', 'sha256': config.sha(listing),
                      'size': listing.stat().st_size}
            report = {'artifacts': [record]}
            with patch.object(config, 'QMK', root):
                self.assertEqual(config.retained_static_symbols(report, build, {0x3027: 0x22}), {})
                with self.assertRaisesRegex(ValueError, 'listing'):
                    config.retained_static_symbols({'artifacts': [record, record]}, build, {0x3027: 0x22})
                extra = build / 'dce/extra.rst'
                extra.write_text('')
                with self.assertRaisesRegex(ValueError, 'listing'):
                    config.retained_static_symbols(report, build, {0x3027: 0x22})
                extra.unlink()
                listing.unlink()
                with self.assertRaisesRegex(ValueError, 'listing'):
                    config.retained_static_symbols(report, build, {0x3027: 0x22})


class MemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = config.ROOT / 'audits/rc6/compact-runtime-20261024/final/full'
        cls.memory = (fixture / 'ajazz_ak820_vial.mem').read_text()
        cls.symbols = config.linked_symbols(fixture / 'ajazz_ak820_vial.map')
        # Only occupied addresses matter for memory membership, not contents.
        cls.code = {0x28a0: 0, 0x2fff: 0, 0x3027: 0, 0xc6ff: 0}

    def test_both_windows_are_independent_and_capacity_is_not_a_bound(self):
        result = config.memory_report(self.code, self.symbols, self.memory)
        self.assertEqual([row['trailing_free_bytes'] for row in result['code_windows']], [0, 0])
        self.assertIsNone(result['internal_ram']['runtime_stack_bound'])
        self.assertIsNone(result['internal_ram']['stack_margin'])
        self.assertFalse(result['internal_ram']['stack_qualified'])

    def test_protected_byte_cannot_be_hidden_by_total_size(self):
        for address in (0x289f, 0x3000, 0x3026, 0xc700, 0xef00, 0xf000):
            with self.subTest(address=address), self.assertRaisesRegex(ValueError, 'protected'):
                config.memory_report({**self.code, address: 0}, self.symbols, self.memory)

    def test_stack_map_mismatch_static_overlap_and_paged_data_fail(self):
        for change in ({'s_SSEG': 0x50}, {'l_SSEG': 1}, {'l_PSEG': 1}, {'l_ISEG': 1},
                       {'s_OSEG': 250, 'l_OSEG': 8}, {'_ak820_led_dma': 0x400}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                config.memory_report(self.code, {**self.symbols, **change}, self.memory)

    def test_grid_corruption_fails(self):
        for memory in (self.memory.replace('0xf0:', '0xe0:'),
                       self.memory.replace('|S|S|S|S|', '|x|S|S|S|', 1)):
            with self.assertRaises(ValueError):
                config.memory_report(self.code, self.symbols, memory)


if __name__ == '__main__':
    unittest.main()
