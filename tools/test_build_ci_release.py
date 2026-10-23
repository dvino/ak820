"""Focused offline tests for fresh-build CI bundle assembly."""
import hashlib
import json
from pathlib import Path
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
                              'tools/test_keyboard.py', 'tools/build_ci_release.py'}
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
                              'tools/test_keyboard.py', 'tools/build_ci_release.py'}
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
            report = {'keyboard': 'ajazz/ak820', 'keymap': 'vial', 'build_id': 532482,
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
            policy = {'source_files': {}, 'program': {'ihx_sha256': sha(b'fresh ihx'), 'symbols_sha256': '1' * 64}}
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
                          'program': {'ihx_sha256': '0' * 64, 'symbols_sha256': '1' * 64}}
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
