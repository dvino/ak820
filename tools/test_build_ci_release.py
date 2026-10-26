"""Focused offline tests for fresh-build CI bundle assembly."""
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

import build_ci_release as ci


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class QualificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ihx, self.mapfile = self.root / 'app.ihx', self.root / 'app.map'
        self.ihx.write_bytes(b'fresh ihx')
        self.mapfile.write_bytes(b'fresh map')
        self.toolchain = self.root / 'toolchain'
        (self.toolchain / 'bin').mkdir(parents=True)
        for name in ('sdcc', 's51'):
            (self.toolchain / 'bin' / name).write_bytes(b'pinned')
        self.report = {
            'format': 'ak820-offline-tests-1', 'passed': True, 'require_toolchain': True,
            'hardware_validated': False, 'physical_device_commands': 0,
            'iap_fault_profile': 'guarded-erase', 'build_unchanged': True,
            'build_hashes': {'ihx': sha(b'fresh ihx'), 'map': sha(b'fresh map')},
            'unit_tests': {'run': 3, 'skipped': 0},
            'tools': {'sdcc': {'sha256': ci.release.SDCC46_PINS['sdcc']},
                      's51': {'sha256': ci.SDCC46_S51_SHA256}},
            'tests': [{'exit_code': 0, 'unit_tests': {'skipped': 0},
                       'build_before': {'ihx': sha(b'fresh ihx'), 'map': sha(b'fresh map')},
                       'build_after': {'ihx': sha(b'fresh ihx'), 'map': sha(b'fresh map')}}],
        }
        # These tests check schema gates without executing the pinned binaries.
        self.toolchain.joinpath('bin/sdcc').write_bytes(b'sdcc')
        self.toolchain.joinpath('bin/s51').write_bytes(b's51')

    def validate(self, report=None):
        return ci._qualification(report or self.report, self.root / 'qualification.json',
                                 self.ihx, self.mapfile, self.toolchain)

    def test_valid_qualification_passes(self):
        with patch.object(ci, 'sha', side_effect=lambda path: (
                ci.release.SDCC46_PINS['sdcc'] if path.name == 'sdcc' else
                ci.SDCC46_S51_SHA256 if path.name == 's51' else sha(path.read_bytes()))):
            self.validate()

    def test_bad_exit_skip_and_mutated_build_are_rejected(self):
        for mutate in (
            lambda x: x['tests'][0].update(exit_code=1),
            lambda x: x['tests'][0]['unit_tests'].update(skipped=1),
            lambda x: x.update(build_unchanged=False),
            lambda x: x['build_hashes'].update(ihx='0' * 64),
            lambda x: x.update(physical_device_commands=1),
        ):
            report = json.loads(json.dumps(self.report))
            mutate(report)
            with self.subTest(report=report), self.assertRaises(ValueError):
                self.validate(report)


class PolicySourceTests(unittest.TestCase):
    def test_source_mutation_and_missing_compiled_input_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'source.c'
            path.write_bytes(b'original')
            required_names = {'.github/workflows/windows-installer.yml', 'tools/ci_checks.py',
                              'tools/test_keyboard.py', 'tools/build_ci_release.py',
                              'tools/build_ci_profiles.py'}
            required_names |= set(ci.HOST_FILES) if hasattr(ci, 'HOST_FILES') else set()
            for name in required_names:
                item = root / name
                item.parent.mkdir(parents=True, exist_ok=True)
                item.write_bytes(b'x')
            lock = root / 'qmk-8051-ak820/dependencies/lufa.json'
            lock.parent.mkdir(parents=True)
            lock.write_text(json.dumps({'format': 'ak820-external-dependency-1', 'name': 'lufa',
                                        'destination': 'lib/lufa',
                                        'revision': '549b97320d515bfca2f95c145a67bd13be968faa',
                                        'required_files': {}}))
            required_records = {
                'source.c': {'size': 8, 'sha256': sha(b'original')},
                'qmk-8051-ak820/dependencies/lufa.json': {
                    'size': lock.stat().st_size, 'sha256': sha(lock.read_bytes())}}
            policy = {'source_files': required_records}
            with patch.object(ci, 'ROOT', root):
                with patch.object(ci, 'host_manifest', return_value={}), \
                     patch.object(ci, 'HOST_FILES', set(), create=True), \
                     patch.object(ci, '_git_blob', side_effect=lambda file: file.read_bytes()):
                    with self.assertRaisesRegex(ValueError, 'omits required'):
                        ci._validate_policy_sources(policy, {'sources': []})
                path.write_bytes(b'mutated')
                with patch.object(ci, 'host_manifest', return_value={}), \
                     patch.object(ci, 'HOST_FILES', set(), create=True), \
                     patch.object(ci, '_git_blob', side_effect=lambda file: file.read_bytes()):
                    with self.assertRaisesRegex(ValueError, 'differs from reviewed policy'):
                        ci._validate_policy_sources(policy, {'sources': []})
                policy['source_files']['source.c'] = {'size': 7, 'sha256': sha(b'mutated')}
                with patch.object(ci, 'host_manifest', return_value={}), \
                     patch.object(ci, 'HOST_FILES', set(), create=True), \
                     patch.object(ci, '_git_blob', return_value=b'original'):
                    with self.assertRaisesRegex(ValueError, 'differs from committed HEAD'):
                        ci._validate_policy_sources(policy, {'sources': []})
                policy['source_files'].update({name: {'size': 1, 'sha256': sha(b'x')}
                                               for name in required_names})
                report = {'sources': [{'origin': 'source', 'path': 'source.c',
                                       'sha256': sha(b'other')}]}
                with patch.object(ci, 'host_manifest', return_value={}), \
                     patch.object(ci, 'HOST_FILES', set(), create=True), \
                     patch.object(ci, '_git_blob', side_effect=lambda file: file.read_bytes()):
                    with self.assertRaisesRegex(ValueError, 'absent from the reviewed policy'):
                        ci._validate_policy_sources(policy, report)

    def test_only_committed_lock_files_may_be_untracked_lufa_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            required_names = {'.github/workflows/windows-installer.yml', 'tools/ci_checks.py',
                              'tools/test_keyboard.py', 'tools/build_ci_release.py',
                              'tools/build_ci_profiles.py'}
            for name in required_names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'x')
            lock_path = root / 'qmk-8051-ak820/dependencies/lufa.json'
            lock_path.parent.mkdir(parents=True)
            lufa_path = root / 'qmk-8051-ak820/lib/lufa/LUFA/Header.h'
            lufa_path.parent.mkdir(parents=True)
            lufa_bytes = b'pinned LUFA header'
            lufa_path.write_bytes(lufa_bytes)
            lock = {'format': 'ak820-external-dependency-1', 'name': 'lufa',
                    'destination': 'lib/lufa',
                    'revision': '549b97320d515bfca2f95c145a67bd13be968faa',
                    'required_files': {'LUFA/Header.h': sha(lufa_bytes)}}
            lock_path.write_text(json.dumps(lock))
            records = {name: {'size': 1, 'sha256': sha(b'x')} for name in required_names}
            records['qmk-8051-ak820/dependencies/lufa.json'] = {
                'size': lock_path.stat().st_size, 'sha256': sha(lock_path.read_bytes())}
            lufa_name = 'qmk-8051-ak820/lib/lufa/LUFA/Header.h'
            records[lufa_name] = {'size': len(lufa_bytes), 'sha256': sha(lufa_bytes)}
            policy = {'source_files': records}
            report = {'sources': [{'origin': 'source', 'path': 'lib/lufa/LUFA/Header.h',
                                   'sha256': sha(lufa_bytes)}]}

            def blob(path):
                if path == lufa_path:
                    raise ValueError('LUFA is not a Git blob')
                if path.name == 'generated.h':
                    raise ValueError('not present as a Git blob')
                return path.read_bytes()

            with patch.object(ci, 'ROOT', root), patch.object(ci, 'host_manifest', return_value={}), \
                 patch.object(ci, '_git_blob', side_effect=blob):
                ci._validate_policy_sources(policy, report)

                lufa_path.write_bytes(b'altered LUFA header')
                records[lufa_name] = {'size': lufa_path.stat().st_size,
                                      'sha256': sha(lufa_path.read_bytes())}
                report['sources'][0]['sha256'] = sha(lufa_path.read_bytes())
                with self.assertRaisesRegex(ValueError, 'LUFA lock'):
                    ci._validate_policy_sources(policy, report)

                lufa_path.write_bytes(lufa_bytes)
                records[lufa_name] = {'size': len(lufa_bytes), 'sha256': sha(lufa_bytes)}
                report['sources'][0]['sha256'] = sha(lufa_bytes)
                arbitrary = 'qmk-8051-ak820/other/generated.h'
                arbitrary_path = root / arbitrary
                arbitrary_path.parent.mkdir(parents=True, exist_ok=True)
                arbitrary_path.write_bytes(b'untracked')
                records[arbitrary] = {'size': 9, 'sha256': sha(b'untracked')}
                with self.assertRaisesRegex(ValueError, 'Git blob'):
                    ci._validate_policy_sources(policy, report)


class AssemblyPreflightTests(unittest.TestCase):
    def test_profile_set_is_exact_and_settings_matrix_rebinds_actual_images(self):
        import ak820_profiles
        import firmware_matrix
        sys.path.insert(0, str(ci.ROOT / 'tools/installer'))
        import settings_backup
        names = ('main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); builds_root = root/'builds'; builds_root.mkdir()
            source_map = ci.ROOT / 'releases/rc6/firmware/application.map'
            rows = []
            measured = {}
            for index, name in enumerate(names):
                (builds_root/name).mkdir()
                mapfile = builds_root/name/'ajazz_ak820_vial.map'
                mapfile.write_bytes(source_map.read_bytes() + f'\npath: /local/{name}\n'.encode())
                ihx = f'{index:064x}'
                configuration = ak820_profiles.configuration(name)
                artifact_identity = {'profile': name, 'configuration_sha256': f'{index+60:064x}',
                    'ihx_sha256': ihx, 'map_sha256': ci.sha(mapfile),
                    'mem_sha256': f'{index+80:064x}', 'build_report_sha256': f'{index+100:064x}',
                    'source_manifest_sha256': f'{index+120:064x}',
                    'compiler_sha256': f'{index+140:064x}', 'nvm_schema': configuration['nvm_schema']}
                contract = settings_backup.catalog_settings_identity(
                    configuration, ihx, f'{index+20:064x}', f'{index+40:064x}')
                rows.append({'profile': name, 'configuration': configuration,
                             'identity': {'ihx_sha256': ihx, 'nvm_schema': configuration['nvm_schema']},
                             'reproducible_identity': ci.reproducible_identity(builds_root/name, artifact_identity),
                             'settings_identity': contract,
                             'release_approved': False, 'installable': False})
                measured[name] = {'profile': name, 'configuration': configuration,
                    'identity': artifact_identity,
                    'measurement_status': 'linked-memory-pass', 'runtime_status': 'exact-image-pass',
                    'offline_tests_status': 'exact-image-pass', 'release_approved': False,
                    'installable': False}
            settings_catalog = root/'settings-catalog.json'
            settings_catalog.write_text(json.dumps({'format': firmware_matrix.FORMAT,
                'profiles': rows, 'settings_transitions': []}))
            with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                matrix, builds = ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)
            self.assertEqual(tuple(row['profile'] for row in matrix['profiles']), names)
            self.assertEqual(matrix['profiles'][0]['settings_identity'], rows[0]['settings_identity'])
            self.assertFalse(any(row['release_approved'] or row['installable'] for row in matrix['profiles']))
            self.assertEqual(tuple(builds), names)
            # CI map/report paths change raw hashes, while linked symbols stay stable.
            changed_map = builds_root/'main'/'ajazz_ak820_vial.map'
            changed_map.write_bytes(source_map.read_bytes() + b'\npath: /ci/profiles/main\n')
            measured['main']['identity']['map_sha256'] = ci.sha(changed_map)
            measured['main']['identity']['build_report_sha256'] = 'e' * 64
            measured['main']['identity']['source_manifest_sha256'] = 'd' * 64
            with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)
            for field in ('configuration_sha256', 'compiler_sha256'):
                original = measured['main']['identity'][field]
                measured['main']['identity'][field] = 'f' * 64
                with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                    with self.assertRaisesRegex(ValueError, 'does not bind the measured profile'):
                        ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)
                measured['main']['identity'][field] = original
            symbol_map = changed_map.read_text()
            altered_map, replacements = re.subn(r'(?m)^C:\s+[0-9A-Fa-f]{8}',
                'C: 00FFFFFF', symbol_map, count=1)
            self.assertEqual(replacements, 1)
            changed_map.write_text(altered_map)
            measured['main']['identity']['map_sha256'] = ci.sha(changed_map)
            with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                with self.assertRaisesRegex(ValueError, 'does not bind the measured profile'):
                    ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)
            changed_map.write_text(symbol_map)
            measured['main']['identity']['map_sha256'] = ci.sha(changed_map)
            catalog = json.loads(settings_catalog.read_text())
            source = settings_backup.WORK_IHX
            catalog['historical_sources'] = [{'ihx_sha256':source,
                'code_sha256':settings_backup._legacy_images()[source]['code_sha256']}]
            catalog['settings_transitions'] = [{'source':source,'target':rows[0]['identity']['ihx_sha256']}]
            settings_catalog.write_text(json.dumps(catalog))
            with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                matrix, _ = ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)
            self.assertEqual(matrix['historical_sources'],catalog['historical_sources'])
            self.assertEqual(matrix['settings_transitions'],catalog['settings_transitions'])
            measured['shortcuts']['identity']['ihx_sha256'] = 'f' * 64
            with patch.object(firmware_matrix, 'measured_row', side_effect=lambda build, toolchain: measured[build.name]):
                with self.assertRaisesRegex(ValueError, 'does not bind the measured profile'):
                    ci.settings_matrix_from_builds(builds_root, root/'toolchain', settings_catalog)

    def test_profile_release_requires_each_committed_policy_review_and_receipt_before_assembly(self):
        names = ci.release_profile_names()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root/'qmk-8051-ak820'; source.mkdir()
            builds = source/'.build/ci-profiles'; builds.mkdir(parents=True)
            policies = root/'ci/profiles'; policies.mkdir(parents=True)
            settings = root/'tools/installer/settings-catalog.json'; settings.parent.mkdir(parents=True)
            settings.write_text('{}')
            for name in names:
                (policies/name).mkdir()
            out = root/'dist/ci-firmware'
            with patch.object(ci, 'ROOT', root), patch.object(ci, 'SOURCE', source), \
                 patch.object(ci, '_validate_source_commit'), patch.object(ci, '_require_committed_input'), \
                 patch.object(ci, 'settings_matrix_from_builds', return_value=({}, {name: builds/name for name in names})):
                with self.assertRaisesRegex(ValueError, 'Missing or unsafe .* policy'):
                    ci.assemble_profiles(builds, policies, out, root/'toolchain', 'a' * 40, settings)
            self.assertFalse(out.exists())

    def test_profile_release_writes_capabilities_from_exact_measured_builds(self):
        names = ci.release_profile_names()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root/'qmk-8051-ak820'; source.mkdir()
            builds_root = source/'.build/ci-profiles'; builds_root.mkdir(parents=True)
            builds = {name: builds_root/name for name in names}
            policies = root/'ci/profiles'
            for name in names:
                (policies/name).mkdir(parents=True)
                for filename in ('release-policy.json', 'program-review.md', 'packing-validation.json'):
                    (policies/name/filename).write_text('{}')
            settings = root/'settings.json'; settings.write_text('{}')
            matrix = {'profiles': [{'identity': {'ihx_sha256': name}} for name in names]}
            capabilities = {'images': [{'build_identity': {'map_sha256': 'measured-raw-map'}}]}
            def assemble_stub(build, qualification, policy, review, receipt, destination, *args, **kwargs):
                destination.mkdir(parents=True)
                (destination/'identity.json').write_text(build.name)
                archive = destination.with_suffix('.zip'); archive.write_bytes(b'profile')
                return {'archive': str(archive)}
            out = root/'dist/release'; toolchain = root/'toolchain'
            with patch.object(ci, 'ROOT', root), patch.object(ci, 'SOURCE', source), \
                 patch.object(ci, '_validate_source_commit'), patch.object(ci, '_require_committed_input'), \
                 patch.object(ci, '_git_head', return_value='a' * 40), \
                 patch.object(ci, 'settings_matrix_from_builds', return_value=(matrix, builds)), \
                 patch.object(ci.capability_catalog, 'catalog', return_value=capabilities) as measured, \
                 patch.object(ci, 'assemble', side_effect=assemble_stub):
                ci.assemble_profiles(builds_root, policies, out, toolchain, 'a' * 40, settings)
            measured.assert_called_once_with([builds[name] for name in names], toolchain)
            self.assertEqual(json.loads((out/'reports/capability-catalog.json').read_text()), capabilities)
            self.assertEqual(json.loads((out/'reports/firmware-matrix.json').read_text()), matrix)

    def test_commit_identity_and_committed_input_are_enforced(self):
        with patch.object(ci, '_git_head', return_value='a' * 40):
            ci._validate_source_commit('a' * 40)
            with self.assertRaisesRegex(ValueError, 'does not match'):
                ci._validate_source_commit('b' * 40)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'policy.json'
            path.write_bytes(b'working tree')
            with patch.object(ci, 'ROOT', Path(directory)), \
                 patch.object(ci, '_git_blob', return_value=b'committed version'):
                with self.assertRaisesRegex(ValueError, 'differs from committed HEAD'):
                    ci._require_committed_input(path, 'Policy')

    def test_bad_commit_and_existing_output_fail_before_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'qmk-8051-ak820'
            build = source / '.build/ci'
            build.mkdir(parents=True)
            output = root / 'dist/bundle'
            inputs = [root / name for name in ('qualification.json', 'policy.json', 'review.md', 'receipt.json')]
            for path in inputs:
                path.write_text('{}')
            with patch.object(ci, 'ROOT', root), patch.object(ci, 'SOURCE', source):
                with self.assertRaisesRegex(ValueError, '40-character'):
                    ci.assemble(build, *inputs, output, root / 'toolchain', 'bad')
                output.mkdir(parents=True)
                with patch.object(ci, '_git_head', return_value='a' * 40), \
                     patch.object(ci, '_git_blob', side_effect=lambda file: file.read_bytes()):
                    with self.assertRaisesRegex(ValueError, 'already exists'):
                        ci.assemble(build, *inputs, output, root / 'toolchain', 'a' * 40)

    def test_assembly_copies_fresh_outputs_and_mismatch_creates_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'qmk-8051-ak820'
            build = source / '.build/ci'
            build.mkdir(parents=True)
            output = root / 'dist/bundle'
            for name, payload in (('ajazz_ak820_vial.ihx', b'fresh ihx'),
                                  ('ajazz_ak820_vial.map', b'fresh map'),
                                  ('ajazz_ak820_vial.mem', b'fresh mem')):
                (build / name).write_bytes(payload)
            import ak820_profiles
            configuration = ak820_profiles.configuration('main')
            report = {'keyboard': 'ajazz/ak820', 'keymap': 'vial',
                      'build_id': configuration['nvm_schema'],
                      'configuration': configuration,
                      'builder_sha256': '166dff0bb41a7a029b8f3c1c8cd57976368e63714458ee26b8fabcf1eb6564a6',
                      'hardware_validated': False, 'artifacts': [
                          {'path': f'.build/ci/ajazz_ak820_vial.{ext}', 'sha256': sha(payload),
                           'size': len(payload)} for ext, payload in
                          (('ihx', b'fresh ihx'), ('map', b'fresh map'), ('mem', b'fresh mem'))]}
            (build / 'build-report.json').write_text(json.dumps(report))
            (source / 'keyboards/ajazz/ak820/keymaps/vial').mkdir(parents=True)
            (source / 'keyboards/ajazz/ak820/info.json').write_bytes(b'info')
            (source / 'keyboards/ajazz/ak820/keymaps/vial/vial.json').write_bytes(b'vial')
            (source / 'util').mkdir(parents=True)
            (source / 'util/build_ak820.py').write_bytes(b'builder')
            q, p, r, receipt = [root / name for name in ('q.json', 'p.json', 'r.md', 'receipt.json')]
            q.write_text('{}')
            policy = {'source_files': {}, 'program': {'ihx_sha256': sha(b'fresh ihx'),
                      'symbols_sha256': '1' * 64, 'schema': configuration['nvm_schema']}}
            p.write_text(json.dumps(policy))
            review = {'format': 'ak820-ci-program-review-1', 'policy_sha256': sha(p.read_bytes())}
            r.write_text('```json\n' + json.dumps(review) + '\n```\n')
            receipt.write_text('{}')
            host = {}
            patches = [
                patch.object(ci, 'ROOT', root), patch.object(ci, 'SOURCE', source),
                patch.object(ci, '_git_head', return_value='a' * 40),
                patch.object(ci, '_git_blob', side_effect=lambda file: file.read_bytes()),
                patch.object(ci, 'host_manifest', return_value=host),
                patch.object(ci.diagnostic, 'diagnostic_build'),
                patch.object(ci.release, 'validate_build_artifact'),
                patch.object(ci.release, 'validate_tools'),
                patch.object(ci.authorization, 'validate_policy'),
                patch.object(ci.authorization, 'symbols_sha256', return_value='1' * 64),
                patch.object(ci.authorization, 'validate_bundle_authorization'),
                patch.object(ci.authorization, 'validate_qualification_contract'),
                patch.object(ci, 'require_release_qualification'),
                patch.object(ci, '_validate_policy_sources'),
                patch.object(ci, '_qualification'),
            ]
            for item in patches:
                item.start()
                self.addCleanup(item.stop)
            result = ci.assemble(build, q, p, r, receipt, output, root / 'toolchain', 'a' * 40)
            self.assertEqual((output / 'firmware/application.ihx').read_bytes(), b'fresh ihx')
            self.assertTrue(Path(result['archive']).is_file())
            self.assertFalse((output / 'firmware/application.bin').exists())

            bad_output = root / 'dist/bad'
            bad_policy = {'source_files': {},
                          'program': {'ihx_sha256': '0' * 64, 'symbols_sha256': '1' * 64,
                                      'schema': configuration['nvm_schema']}}
            bad_policy_path = root / 'bad-policy.json'
            bad_policy_path.write_text(json.dumps(bad_policy))
            bad_review = root / 'bad-review.md'
            bad_review.write_text('```json\n' + json.dumps({
                'format': 'ak820-ci-program-review-1',
                'policy_sha256': sha(bad_policy_path.read_bytes())}) + '\n```\n')
            with self.assertRaisesRegex(ValueError, 'reviewed program'):
                ci.assemble(build, q, bad_policy_path, bad_review, receipt, bad_output,
                            root / 'toolchain', 'a' * 40)
            self.assertFalse(bad_output.exists())


if __name__ == '__main__':
    unittest.main()
