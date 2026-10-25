"""Negative controls for profile selection, protected memory and approval."""
from __future__ import annotations

import copy
import json
import os
import re
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
    def test_included_fixtures_and_tool_dependencies_are_part_of_source_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('qmk-8051-ak820/tests/fixture/host_tests.inc',
                         'tests/test_compact_key_overrides.py',
                         'qmk-8051-ak820/util/test_ak820_settings.c',
                         'qmk-8051-ak820/util/ak820_extension_settings.py'):
                with self.subTest(name=name):
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('original fixture')
                    with patch.object(config, 'ROOT', root), patch.object(config.subprocess, 'check_output',
                            return_value=name.encode() + b'\0'):
                        before = config.test_source_snapshot()
                        self.assertEqual(before, {name: config.sha(path)})
                        path.write_text('changed fixture')
                        self.assertNotEqual(config.test_source_snapshot(), before)

    def test_runtime_proof_cannot_survive_later_checker_edits_or_grant_release_approval(self):
        result = {'identity': {'ihx_sha256': 'image'}, 'resources': {'internal_ram': {}},
                  'release_approved': True}
        proof = {'identity': result['identity'], 'passed': True, 'source_files': {'checker': 'before'},
                 'stack_bound': 160, 'stack_margin': 6, 'release_approved': False}
        with patch.object(config, 'runtime_source_snapshot', return_value={'checker': 'before'}):
            config.apply_runtime_safety(result, proof)
            self.assertFalse(result['release_approved'])
            self.assertTrue(result['resources']['internal_ram']['stack_qualified'])
        with patch.object(config, 'runtime_source_snapshot', return_value={'checker': 'after'}), \
             self.assertRaisesRegex(ValueError, 'sources changed after checks'):
            config.apply_runtime_safety(result, proof)

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
            for feature, prefix in (('tap-dance', 'tap-dance'), ('key-overrides', 'key-overrides'), ('qmk-settings', 'qmk-settings'), ('dynamic-macros', 'dynamic-macro'), ('gui-lock', 'gui-lock'), ('leader', 'leader'), ('os-indicators', 'os-indicators'), ('mac-pc', 'mac-pc')):
                for suffix in ('host', 'linked'):
                    self.assertEqual(prefix + '-' + suffix in identifiers, feature in features)
            for suffix in ('host', 'flags', 'linked'):
                self.assertEqual('ctrl-gui-' + suffix in identifiers, 'ctrl-gui-swap' in features)

    def test_shared_gui_handler_does_not_prove_ctrl_gui_swap(self):
        selected = config.profiles.configuration('full-gui-lock')
        symbols = {symbol: 0x3027 for feature, symbol in config.SYMBOLS.items()
                   if feature in selected['optional_features']}
        symbols['_gui_disabled'] = 0x20
        code = {0x3027: 0x22}
        config.check_feature_symbols(symbols, selected, code)
        swapped = config.profiles.configuration('full-ctrl-gui')
        with self.assertRaisesRegex(ValueError, 'feature state'):
            config.check_feature_symbols(symbols, swapped, code)
        symbols['_ctrl_gui_swapped'] = 0x21
        config.check_feature_symbols(symbols, swapped, code)
        with self.assertRaisesRegex(ValueError, 'feature state'):
            config.check_feature_symbols(symbols, selected, code)

    def test_exact_named_combinations_and_no_inherited_switches(self):
        for name, features in config.profiles.PROFILES.items():
            self.assertEqual(set(config.profiles.configuration(config.profiles.select(list(features)))['optional_features']), set(features))
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

    def test_release_catalog_is_bounded_and_covers_every_existing_module(self):
        names = config.profiles.RELEASE_PROFILES
        self.assertLessEqual(len(names), 12)
        self.assertEqual(len(names), len(set(names)))
        self.assertIn(config.profiles.DEFAULT_PROFILE, names)
        features = {feature for name in names for feature in config.profiles.configuration(name)['optional_features']}
        self.assertEqual(features, set(config.profiles.SWITCHES))
        for name in names:
            self.assertFalse(config.profiles.configuration(name)['release_approved'])

    def test_work_default_preserves_required_and_excluded_modules(self):
        self.assertEqual(config.profiles.DEFAULT_PROFILE, 'work')
        features = config.profiles.configuration('work')['optional_features']
        self.assertIn('os-indicators', features)
        self.assertNotIn('mac-pc', features)
        self.assertNotIn('mouse-keys', features)

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
                for row in rows:
                    command = row['command']
                    if not any(command[index:index + 2] == ['-m', 'unittest']
                               for index in range(len(command) - 1)):
                        continue
                    log = build / 'profile-tests' / (row['id'] + '.log')
                    original = log.read_text()
                    for text in ('Ran 0 tests in 0.1s\n\nOK\n',
                                 'Ran 15 tests in 0.1s\n\nOK (skipped=1)\n'):
                        log.write_text(text)
                        bad = copy.deepcopy(report)
                        next(item for item in bad['tests'] if item['id'] == row['id'])['log_sha256'] = config.sha(log)
                        with self.subTest(suite=row['id'], log=text), self.assertRaisesRegex(ValueError, 'empty or skipped'):
                            config.validate_profile_tests(bad, 'one-shot', identity, build, toolchain)
                    log.write_text(original)

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
        for required in ('outline-gates', 'stack-gates', 'runtime-safety-gates', 'delay-abi', 'outline-integrity', 'vialrgb-linked',
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

    def test_profile_requalification_replaces_stale_results_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            toolchain = build / 'toolchain'
            identity = {'ihx_sha256': 'fixture'}
            command = ['python', '-m', 'unittest']
            statuses = iter((0, 0, 1))
            def run(command, **kwargs):
                status = next(statuses)
                kwargs['stdout'].write('Ran 1 test in 0.001s\n\n' + ('OK\n' if status == 0 else 'FAILED\n'))
                return subprocess.CompletedProcess(command, status)
            with patch.object(config, 'profile_test_plan', return_value=[('gates', build, command)]), \
                 patch.object(config, 'test_source_snapshot', return_value={}), \
                 patch.object(config, 'inspect', return_value={'identity': identity}), \
                 patch.object(config.subprocess, 'run', side_effect=run):
                config.run_profile_tests('standard', build, toolchain, identity)
                stale = build / 'profile-tests/obsolete.log'
                stale.write_text('previous result')
                config.run_profile_tests('standard', build, toolchain, identity)
                self.assertFalse(stale.exists())
                self.assertTrue(json.loads((build / 'profile-tests/results.json').read_text())['passed'])
                with self.assertRaisesRegex(ValueError, 'Profile suite failed'):
                    config.run_profile_tests('standard', build, toolchain, identity)
                self.assertFalse(json.loads((build / 'profile-tests/results.json').read_text())['passed'])

    def test_profile_requalification_rejects_output_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'; build.mkdir()
            elsewhere = root / 'elsewhere'; elsewhere.mkdir()
            protected = elsewhere / 'keep.log'; protected.write_text('keep')
            (build / 'profile-tests').symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'must not be a symlink'):
                config.run_profile_tests('standard', build, root / 'toolchain', {'ihx_sha256': 'fixture'})
            self.assertEqual(protected.read_text(), 'keep')

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

    def test_ctrl_gui_state_requires_one_unique_internal_bit_allocation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'
            (build / 'dce').mkdir(parents=True)
            listing = build / 'dce/fixture.rst'
            valid = ('  567 .area BSEG (BIT)\n'
                     '  000021 570 _ctrl_gui_swapped:\n'
                     '  000021 571 .ds 1\n'
                     '  572 .area CSEG (CODE)\n'
                     '  003027 22 [24] 573 ret\n')
            def inspect(text):
                listing.write_text(text)
                report = {'artifacts': [{'path': 'build/dce/fixture.rst',
                                        'sha256': config.sha(listing), 'size': listing.stat().st_size}]}
                return config.retained_static_symbols(report, build, {0x3027: 0x22})
            with patch.object(config, 'QMK', root):
                self.assertEqual(inspect(valid), {'_ctrl_gui_swapped': 0x21})
                for changed in (valid.replace('BSEG (BIT)', 'XSEG (XDATA)'),
                                valid.replace('BSEG (BIT)', 'BSEG (DATA)'),
                                valid.replace('.ds 1', '.ds 2'),
                                valid.replace('000021 571', '000022 571'),
                                valid.replace('000021', '000080'),
                                valid.replace('  000021 571 .ds 1\n', ''), valid + valid):
                    with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, 'feature'):
                        inspect(changed)


class MemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = config.ROOT / 'audits/rc6/compact-runtime-20261024/final/full'
        cls.memory = (fixture / 'ajazz_ak820_vial.mem').read_text()
        cls.symbols = config.linked_symbols(fixture / 'ajazz_ak820_vial.map')
        # Only occupied addresses matter for memory membership, not contents.
        cls.code = {0x28a0: 0, 0x2fff: 0, 0x3027: 0, 0xc6ff: 0}

    def test_both_windows_are_independent_and_capacity_is_not_a_bound(self):
        result = config.memory_report(self.code, self.symbols, self.memory, historical=True)
        self.assertEqual([row['trailing_free_bytes'] for row in result['code_windows']], [0, 0])
        self.assertIsNone(result['internal_ram']['runtime_stack_bound'])
        self.assertIsNone(result['internal_ram']['stack_margin'])
        self.assertFalse(result['internal_ram']['stack_qualified'])

    def test_protected_byte_cannot_be_hidden_by_total_size(self):
        for address in (0x289f, 0x3000, 0x3026, 0xc700, 0xef00, 0xf000):
            with self.subTest(address=address), self.assertRaisesRegex(ValueError, 'protected'):
                config.memory_report({**self.code, address: 0}, self.symbols, self.memory, historical=True)

    def test_stack_map_mismatch_static_overlap_and_paged_data_fail(self):
        for change in ({'s_SSEG': 0x50}, {'l_SSEG': 1}, {'l_PSEG': 1}, {'l_ISEG': 1},
                       {'s_OSEG': 250, 'l_OSEG': 8}, {'_ak820_led_dma': 0x400}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                config.memory_report(self.code, {**self.symbols, **change}, self.memory, historical=True)

    def test_current_ordinary_window_and_total_budget(self):
        match = re.search(r'EXTERNAL RAM\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\d+)\s+(\d+)', self.memory, re.I)
        memory = self.memory[:match.start()] + 'EXTERNAL RAM 0x0440 0x0fff 3008 3008' + self.memory[match.end():]
        symbols = {**self.symbols, 's_XSEG': 0x440, 'l_XSEG': 3008, 's_XISEG': 0x1000, 'l_XISEG': 0,
                   '_ak820_flash_stage': 0x400}
        result = config.memory_report(self.code, symbols, memory)['xram']
        self.assertEqual((result['bytes'], result['reserved_bytes'], result['total_bytes'],
                          result['physical_capacity']), (3008, 64, 3072, 3072))
        for changed in (memory.replace('0x0440', '0x0400'),
                        memory.replace('0x0fff 3008', '0x1000 3009'),
                        memory.replace('3008 3008', '3008 3072'),
                        memory.replace('0x0fff 3008', '0x043f 0')):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                config.memory_report(self.code, symbols, changed)
        for value in (0x3c0, 0x440, 0x1000, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                config.memory_report(self.code, {**symbols, '_ak820_flash_stage': value}, memory)
        for change in ({'l_XSEG': 3009}, {'l_XSEG': -1}, {'l_XISEG': -1},
                       {'s_XISEG': 0xfff}, {'s_XISEG': 0x1001}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                config.memory_report(self.code, {**symbols, **change}, memory)
        with self.assertRaises(ValueError):
            config.memory_report(self.code, self.symbols, self.memory)

    def test_stage_requires_bound_compiler_allocation_extent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'
            build.mkdir()
            board = build / 'ak820_board.asm'
            stage = build / 'ak820_flash.asm'
            (build / 'allocation').mkdir()
            metadata_asm = build / 'allocation/ak820_flash.asm'
            metadata = metadata_asm.with_suffix('.adb')
            board.write_text('.area XSEG (XDATA)\n_ak820_led_dma = 0x200\n')
            valid = '.area XSEG (XDATA)\nG$ak820_flash_stage$0_0$0 == 0x0400\n_ak820_flash_stage = 0x400\n'
            allocation = 'S:G$ak820_flash_stage$0_0$0({64}DA64d,SC:U),F,0,0\n'
            def inspect(asm=valid, adb=allocation):
                stage.write_text(asm)
                metadata.write_text(adb)
                metadata_asm.write_text(asm.replace("= 0x400", "= 0x0400"))
                report = {'expected_objects': ['build/ak820_board.rel', 'build/ak820_flash.rel'],
                          'artifacts': [{'path': path.relative_to(root).as_posix(),
                                         'sha256': config.sha(path), 'size': path.stat().st_size}
                                        for path in (board, stage, metadata_asm, metadata)]}
                return config.check_absolute_xdata(report, build)
            with patch.object(config, 'QMK', root):
                self.assertEqual(inspect()[-1]['reserved_end_exclusive'], 0x440)
                for asm, adb in ((valid.replace('= 0x400', '= 0x440'), allocation),
                                 (valid + '_overlap = 0x420\n', allocation),
                                 (valid, allocation.replace('{64}DA64d', '{65}DA65d')),
                                 (valid, allocation.replace('{64}DA64d', '{63}DA63d')),
                                 (valid, allocation + allocation), (valid, '')):
                    with self.subTest(asm=asm, adb=adb), self.assertRaises(ValueError):
                        inspect(asm, adb)

    def test_grid_corruption_fails(self):
        for memory in (self.memory.replace('0xf0:', '0xe0:'),
                       self.memory.replace('|S|S|S|S|', '|x|S|S|S|', 1)):
            with self.assertRaises(ValueError):
                config.memory_report(self.code, self.symbols, memory, historical=True)


if __name__ == '__main__':
    unittest.main()
