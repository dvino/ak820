import json
from contextlib import ExitStack
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_ci_release as ci
import build_release_bundle as local
import ak820_profiles as profiles
import test_pointer_policy_binding as binding_tests


class ReleaseGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.build = Path(self.tmp.name)
        self.path = self.build / 'build-report.json'
        self.report = {'compiler_input_contract': ci.CANONICAL_POLICY, 'configuration': {'profile': 'test'}}
        self.path.write_text(json.dumps(self.report))
        self.identity = {'identity': {'build_report_sha256': ci.sha(self.path)},
                         'configuration': self.report['configuration']}

    def qualify(self):
        ci.qualify_build_report(self.report, self.path, self.build, self.build)

    def test_canonical_inspection_and_safety(self):
        with patch.object(ci.configure_firmware, 'inspect', return_value=self.identity) as inspect, \
             patch.object(ci, 'validate_configuration') as configuration, \
             patch.object(ci.release_safety, 'validate') as safety:
            self.qualify()
            inspect.assert_called_once_with(self.build, self.build)
            configuration.assert_called_once_with(self.report['configuration'])
            safety.assert_called_once_with(self.report)

    def test_forged_marker_fails_inspection(self):
        with patch.object(ci.configure_firmware, 'inspect', side_effect=ValueError('forged')), \
             patch.object(ci.release_safety, 'validate') as safety:
            with self.assertRaisesRegex(ValueError, 'forged'):
                self.qualify()
            safety.assert_not_called()

    def test_changed_report_and_configuration_rejected(self):
        for field in ('hash', 'configuration', 'file'):
            with self.subTest(field=field):
                result = {'identity': dict(self.identity['identity']), 'configuration': dict(self.identity['configuration'])}
                def inspect(*args):
                    if field == 'hash':
                        result['identity']['build_report_sha256'] = 'wrong'
                    if field == 'configuration':
                        result['configuration'] = {'profile': 'other'}
                    if field == 'file':
                        self.path.write_text('{}')
                    return result
                with patch.object(ci.configure_firmware, 'inspect', side_effect=inspect), \
                     patch.object(ci.release_safety, 'validate') as safety:
                    with self.assertRaises(ValueError):
                        self.qualify()
                    safety.assert_not_called()
                self.path.write_text(json.dumps(self.report))

    def test_invalid_safety_stops(self):
        with patch.object(ci.configure_firmware, 'inspect', return_value=self.identity), \
             patch.object(ci, 'validate_configuration'), \
             patch.object(ci.release_safety, 'validate', side_effect=ValueError('safety')):
            with self.assertRaisesRegex(ValueError, 'safety'):
                self.qualify()

    def test_markerless_uses_historical_guard(self):
        names = ('util/build_ak820.py', 'keyboards/ajazz/ak820/ak820_mousekey.c')
        hashes = profiles.HISTORICAL_COMPILER_INPUT_PAIR
        report = {'configuration': profiles.configuration('full'), 'builder_sha256': hashes[0],
                  'sources': [{'origin': 'source', 'path': name, 'sha256': value}
                              for name, value in zip(names, hashes)]}
        with patch.object(ci.release_safety, 'validate') as safety, \
             patch.object(ci.configure_firmware, 'inspect') as inspect:
            ci.qualify_build_report(report, self.path, self.build, self.build)
            safety.assert_called_once_with(report)
            inspect.assert_not_called()
            report['sources'][0]['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'Compiler-input contract is not closed'):
                ci.qualify_build_report(report, self.path, self.build, self.build)

    def test_forged_canonical_marker_real_inspect(self):
        config = ci.configure_firmware
        build, toolchain, report = binding_tests.PointerBindingTest().canonical_fixture(self.build)
        report['artifacts'] = [row for row in report['artifacts'] if not row['path'].endswith('.o.compile.json')]
        (build / 'build-report.json').write_text(json.dumps(report))
        with patch.object(config, 'QMK', self.build), patch.object(config, 'validate_tools', return_value=toolchain), \
             patch.object(config, 'check_pass30', wraps=config.check_pass30) as pass30:
            with self.assertRaises(ValueError):
                config.inspect(build, toolchain)
            pass30.assert_not_called()

    def test_invalid_safety_single_and_all_profile_leave_no_output(self):
        root = self.build
        build = root / 'builds' / 'main'
        build.mkdir(parents=True)
        report_path = build / 'build-report.json'
        report_path.write_text(json.dumps(self.report))
        identity = {'identity': {'build_report_sha256': ci.sha(report_path), 'ihx_sha256': 'unused'},
                    'configuration': self.report['configuration']}
        policy = root / 'policies' / 'main'
        policy.mkdir(parents=True)
        for name in ('release-policy.json', 'program-review.md', 'packing-validation.json'):
            (policy / name).write_text('{}')
        qualification = build / 'qualification.json'
        qualification.write_text('{}')
        catalog = root / 'catalog.json'
        catalog.write_text('{}')
        matrix = {'profiles': [{'identity': {'ihx_sha256': 'unused'}}]}
        with ExitStack() as stack:
            for name, value in (('ROOT', root), ('SOURCE', root), ('_validate_source_commit', lambda *x: None),
                                ('_git_blob', lambda *x: None), ('_require_committed_input', lambda *x: None),
                                ('release_profile_names', lambda: ('main',)),
                                ('settings_matrix_from_builds', lambda *x: (matrix, {'main': build}))):
                stack.enter_context(patch.object(ci, name, value))
            stack.enter_context(patch.object(ci.capability_catalog, 'catalog', return_value={}))
            stack.enter_context(patch.object(ci.configure_firmware, 'inspect', return_value=identity))
            stack.enter_context(patch.object(ci, 'validate_configuration'))
            stack.enter_context(patch.object(ci.release_safety, 'validate', side_effect=ValueError('safety')))
            output = root / 'single'
            with self.assertRaisesRegex(ValueError, 'safety'):
                ci.assemble(build, qualification, policy / 'release-policy.json', policy / 'program-review.md',
                            policy / 'packing-validation.json', output, root, 'commit')
            self.assertFalse(output.exists())
            self.assertFalse(output.with_suffix('.zip').exists())
            output = root / 'all'
            with self.assertRaisesRegex(ValueError, 'safety'):
                ci.assemble_profiles(root / 'builds', root / 'policies', output, root, 'commit', catalog)
            self.assertFalse(output.exists())
            self.assertEqual(list(root.glob('.all.stage-*')), [])

    def test_post_inspection_mutations_clean_single_output(self):
        root = self.build
        build = root / 'build'
        build.mkdir()
        configuration = {'profile': 'test', 'nvm_schema': 1}
        report = {'compiler_input_contract': ci.CANONICAL_POLICY, 'configuration': configuration,
                  'keyboard': 'ajazz/ak820', 'keymap': 'vial', 'build_id': 1, 'hardware_validated': False}
        report_path = build / 'build-report.json'
        report_path.write_text(json.dumps(report))
        paths = {'build_report': report_path}
        for suffix in ('ihx', 'map', 'mem'):
            path = build / ('ajazz_ak820_vial.' + suffix)
            path.write_text(suffix)
            paths[suffix] = path
        identity = {name + '_sha256': ci.sha(path) for name, path in paths.items()}
        policy = {'program': {'schema': 1, 'ihx_sha256': identity['ihx_sha256'], 'symbols_sha256': 'symbols'},
                  'source_files': []}
        policy_path, review, receipt, qualification = (root / name for name in ('policy', 'review', 'receipt', 'qualification'))
        policy_path.write_text(json.dumps(policy))
        for path in (review, receipt, qualification):
            path.write_text('{}')
        for name in ('keyboards/ajazz/ak820/info.json', 'keyboards/ajazz/ak820/keymaps/vial/vial.json',
                     'util/build_ak820.py'):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{}')
        for stage, changed in [('copy', name) for name in paths] + [('archive', name) for name in paths]:
            with self.subTest(stage=stage, changed=changed), ExitStack() as stack:
                original = paths[changed].read_bytes()
                for name, value in (('ROOT', root), ('SOURCE', root), ('_validate_source_commit', lambda *x: None),
                                    ('_git_blob', lambda *x: None), ('_require_committed_input', lambda *x: None),
                                    ('_qualification', lambda *x: None), ('_validate_policy_sources', lambda *x: None),
                                    ('_review_record', lambda *x: {'policy_sha256': ci.sha(policy_path)}),
                                    ('host_manifest', lambda *x: {})):
                    stack.enter_context(patch.object(ci, name, value))
                stack.enter_context(patch.object(ci.configure_firmware, 'inspect', return_value={
                    'identity': identity, 'configuration': configuration}))
                stack.enter_context(patch.object(ci, 'validate_configuration', return_value=configuration))
                stack.enter_context(patch.object(ci.release_safety, 'validate'))
                stack.enter_context(patch.object(ci.diagnostic, 'diagnostic_build'))
                stack.enter_context(patch.object(ci.release, 'validate_build_artifact'))
                stack.enter_context(patch.object(ci.release, 'validate_tools'))
                stack.enter_context(patch.object(ci.authorization, 'validate_qualification_contract'))
                stack.enter_context(patch.object(ci.authorization, 'validate_policy'))
                stack.enter_context(patch.object(ci.authorization, 'symbols_sha256', return_value='symbols'))
                stack.enter_context(patch.object(ci.authorization, 'validate_bundle_authorization'))
                def mutate():
                    if stage == 'copy':
                        paths[changed].write_bytes(original + b'changed')
                    return 'commit'
                stack.enter_context(patch.object(ci, '_git_head', side_effect=mutate))
                zip_write = ci.zipfile.ZipFile.write
                archive_name = ('reports/build-report.json' if changed == 'build_report'
                                else 'firmware/application.' + changed)
                def write_corrupt(zf, filename, arcname=None, *args, **kwargs):
                    if stage == 'archive' and arcname == archive_name:
                        zf.writestr(arcname, Path(filename).read_bytes() + b'changed')
                    else:
                        zip_write(zf, filename, arcname, *args, **kwargs)
                stack.enter_context(patch.object(ci.zipfile.ZipFile, 'write', write_corrupt))
                output = root / ('out-' + stage + '-' + changed)
                try:
                    with self.assertRaisesRegex(ValueError, 'Copied release input differs' if stage == 'copy'
                                                else 'Packaged release input differs'):
                        ci.assemble(build, qualification, policy_path, review, receipt, output, root, 'commit')
                    self.assertFalse(output.exists())
                    self.assertFalse(output.with_suffix('.zip').exists())
                    self.assertFalse(output.with_suffix('.zip.sha256').exists())
                finally:
                    paths[changed].write_bytes(original)

    def test_later_profile_failure_cleans_previous_staging(self):
        root = self.build
        builds = {name: root / 'builds' / name for name in ('main', 'game')}
        for name, build in builds.items():
            build.mkdir(parents=True)
            (build / 'build-report.json').write_text(json.dumps(self.report))
            (build / 'qualification.json').write_text('{}')
            policy = root / 'policies' / name
            policy.mkdir(parents=True)
            for filename in ('release-policy.json', 'program-review.md', 'packing-validation.json'):
                (policy / filename).write_text('{}')
        catalog = root / 'catalog.json'
        catalog.write_text('{}')
        matrix = {'profiles': [{'identity': {'ihx_sha256': name}} for name in builds]}
        calls = []
        real_assemble = ci.assemble
        def assemble(build, qualification, policy, review, receipt, output, toolchain, commit, **kwargs):
            calls.append(build.name)
            if build.name == 'game':
                return real_assemble(build, qualification, policy, review, receipt, output, toolchain, commit, **kwargs)
            output.mkdir(parents=True)
            (output / 'partial').write_text('staged')
            archive = output.with_suffix('.zip')
            archive.write_bytes(b'archive')
            Path(str(archive) + '.sha256').write_text('checksum')
            return {'archive': str(archive)}
        with ExitStack() as stack:
            for name, value in (('ROOT', root), ('SOURCE', root), ('_validate_source_commit', lambda *x: None),
                                ('_git_blob', lambda *x: None), ('_require_committed_input', lambda *x: None),
                                ('release_profile_names', lambda: tuple(builds)),
                                ('settings_matrix_from_builds', lambda *x: (matrix, builds)),
                                ('assemble', assemble)):
                stack.enter_context(patch.object(ci, name, value))
            stack.enter_context(patch.object(ci.capability_catalog, 'catalog', return_value={}))
            identity = {'identity': {'build_report_sha256': ci.sha(builds['game'] / 'build-report.json')},
                        'configuration': self.report['configuration']}
            stack.enter_context(patch.object(ci.configure_firmware, 'inspect', return_value=identity))
            stack.enter_context(patch.object(ci, 'validate_configuration'))
            safety = stack.enter_context(patch.object(ci.release_safety, 'validate', side_effect=ValueError('invalid safety')))
            with self.assertRaisesRegex(ValueError, 'invalid safety'):
                ci.assemble_profiles(root / 'builds', root / 'policies', root / 'all', root, 'commit', catalog)
            safety.assert_called_once_with(self.report)
        self.assertEqual(calls, ['main', 'game'])
        self.assertFalse((root / 'all').exists())
        self.assertEqual(list(root.glob('.all.stage-*')), [])

    def test_direct_local_guard_rejects_canonical_and_other_markers(self):
        for marker in (ci.CANONICAL_POLICY, 'unverified', 'unknown', 'ak820-pointer-inputs-1'):
            with self.subTest(marker=marker):
                with self.assertRaises(ValueError):
                    local.require_release_qualification({'compiler_input_contract': marker})


if __name__ == '__main__':
    unittest.main()
