"""Offline byte/path validation equivalence for release authorization."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))

import test_ci_authorization as fixture
import ak820_release_manifest as host

auth, markdown, raw = fixture.auth, fixture.markdown, fixture.raw

# Captured from the original host identity contract, independent of HOST_FILES.
EXPECTED_HOST_FILES = frozenset((
    'AK820.sh', 'AK820.cmd', 'tools/build_ci_release.py',
    'qmk-8051-ak820/util/ak820_ci_authorization.py', 'tools/build_release_bundle.py',
    'qmk-8051-ak820/util/ak820_profiles.py', 'qmk-8051-ak820/util/ak820_extension_settings.py',
    'tools/installer/ak820.py', 'tools/installer/i18n.py', 'tools/ak820_device_protocol.py',
    'tools/ak820_leader_marker.py',
    'tools/installer/settings_backup.py', 'tools/installer/settings_workflow.py',
    'tools/installer/profile-catalog.json', 'tools/installer/settings-catalog.json',
    'tools/installer/requirements.txt', 'tools/installer/70-ak820.rules',
    'qmk-8051-ak820/util/ak820_tool.py', 'qmk-8051-ak820/util/ak820_diagnose.py',
    'qmk-8051-ak820/util/pack_ak820.py', 'qmk-8051-ak820/util/prepare_ak820_trial.py',
    'qmk-8051-ak820/util/native_macro_import.py', 'qmk-8051-ak820/util/ak820_release_manifest.py',
))


class AuthorizationBytesTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture.AuthorizationTests('test_pass')
        self.fixture.setUp()

    @staticmethod
    def snapshot(bundle):
        return {str(p.relative_to(bundle)): p.read_bytes() for p in bundle.rglob('*') if p.is_file()}

    def compare(self, bundle, files, manifest, record, error=None):
        for name, data in files.items():
            (bundle / name).write_bytes(data)
        if error is None:
            self.assertEqual(auth.validate_bundle_authorization(bundle, manifest, record),
                             auth.validate_bundle_authorization_bytes(files, manifest, record))
        else:
            with self.assertRaisesRegex(ValueError, error) as path_error:
                auth.validate_bundle_authorization(bundle, manifest, record)
            with self.assertRaises(type(path_error.exception)) as byte_error:
                auth.validate_bundle_authorization_bytes(files, manifest, record)
            self.assertEqual(str(path_error.exception), str(byte_error.exception))

    def test_host_identities_and_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(host.HOST_FILES, EXPECTED_HOST_FILES)
            files = {name: name.encode() for name in EXPECTED_HOST_FILES}
            for name, data in files.items():
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            manifest = {'host_files': host.host_manifest(root)}
            self.assertEqual(manifest['host_files']['AK820.sh'], {
                'size': 8, 'sha256': '75073f16623afc510df93c9c33c519d492bc1b86141e075f63e47f27738077a4'})
            self.assertIsNone(host.validate_host_manifest(manifest, root))
            self.assertIsNone(host.validate_host_manifest_bytes(manifest, files))
            for name in sorted(files):
                with self.subTest(host_file=name):
                    altered = dict(files); altered[name] = bytes((files[name][0] ^ 1,)) + files[name][1:]
                    (root / name).write_bytes(altered[name])
                    with self.assertRaisesRegex(ValueError, 'Host code differs') as path_error:
                        host.validate_host_manifest(manifest, root)
                    with self.assertRaises(ValueError) as byte_error:
                        host.validate_host_manifest_bytes(manifest, altered)
                    self.assertEqual(str(path_error.exception), str(byte_error.exception))
                    (root / name).write_bytes(files[name])
            name = sorted(files)[0]
            for altered_manifest in ({}, {'host_files': {}},
                                     {'host_files': {**manifest['host_files'], 'extra': {}}}):
                with self.assertRaisesRegex(ValueError, 'Incomplete or unexpected host-code manifest'):
                    host.validate_host_manifest_bytes(altered_manifest, files)
                with self.assertRaisesRegex(ValueError, 'Incomplete or unexpected host-code manifest'):
                    host.validate_host_manifest(altered_manifest, root)
            with self.assertRaises(FileNotFoundError) as byte_missing:
                host.validate_host_manifest_bytes(manifest, {k:v for k,v in files.items() if k != name})
            self.assertEqual(byte_missing.exception.errno, 2)
            self.assertEqual(byte_missing.exception.filename, name)
            (root / 'extra').write_bytes(b'x')
            self.assertIsNone(host.validate_host_manifest(manifest, root))
            self.assertIsNone(host.validate_host_manifest_bytes(manifest, {**files, 'extra': b'x'}))
            (root / name).write_bytes(files[name])
            (root / name).unlink()
            with self.assertRaises(FileNotFoundError):
                host.validate_host_manifest(manifest, root)

    def test_ci_baseline_tampering_and_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, manifest, record = self.fixture.bundle_fixture(folder)
            original = self.snapshot(bundle)
            self.compare(bundle, original, manifest, record)
            for name in sorted(original):
                with self.subTest(name=name):
                    changed = dict(original); changed[name] += b'!'
                    self.compare(bundle, changed, manifest, record, '.')
            for name, data in original.items():
                (bundle / name).write_bytes(data)
            for name in sorted(original):
                with self.subTest(missing=name):
                    missing = dict(original); del missing[name]
                    (bundle / name).unlink(missing_ok=True)
                    with self.assertRaises(FileNotFoundError) as path_missing:
                        auth.validate_bundle_authorization(bundle, manifest, record)
                    with self.assertRaises(FileNotFoundError) as byte_missing:
                        auth.validate_bundle_authorization_bytes(missing, manifest, record)
                    self.assertEqual(path_missing.exception.errno, byte_missing.exception.errno)
                    self.assertEqual(byte_missing.exception.filename, name)
                    (bundle / name).write_bytes(original[name])
            for fmt, files in (('ak820-offline-review-2', manifest['files']),
                               ('ak820-reproduced-review-1', {})):
                with self.assertRaisesRegex(ValueError, 'Mixed exact-build'):
                    auth.validate_bundle_authorization_bytes(original, {'files': files}, {'format': fmt})
            self.assertIsNone(auth.validate_bundle_authorization_bytes({}, {'files': {}},
                               {'format': 'ak820-offline-review-2'}))

    def test_rehashed_duplicate_review_and_qualification(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, manifest, record = self.fixture.bundle_fixture(folder)
            original = self.snapshot(bundle)
            duplicated = dict(original)
            duplicated['reviews/program-review.md'] *= 2
            self.compare(bundle, duplicated, manifest, record, 'Expected one')
            changed = dict(original)
            q = json.loads(changed['reports/qualification.json'])
            q['tests'].append(copy.deepcopy(q['tests'][0]))
            changed['reports/qualification.json'] = raw(q)
            a = json.loads(changed['reports/build-attestation.json'])
            a['qualification_sha256'] = auth.digest(changed['reports/qualification.json'])
            changed['reports/build-attestation.json'] = raw(a)
            updated_record = dict(record, attestation_sha256=auth.digest(changed['reports/build-attestation.json']))
            self.compare(bundle, changed, manifest, updated_record, 'duplicate|Duplicate')

    def test_rehashed_semantically_invalid_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, manifest, record = self.fixture.bundle_fixture(folder)
            changed = self.snapshot(bundle)
            receipt = json.loads(changed['reports/packing-validation.json'])
            receipt['packing']['physical_usb_opened'] = True
            changed['reports/packing-validation.json'] = raw(receipt)
            policy = json.loads(changed['reviews/program-policy.json'])
            policy['packing_receipt_sha256'] = auth.digest(changed['reports/packing-validation.json'])
            changed['reviews/program-policy.json'] = raw(policy)
            review = dict(self.fixture.review, policy_sha256=auth.digest(changed['reviews/program-policy.json']))
            changed['reviews/program-review.md'] = markdown(review)
            attestation = json.loads(changed['reports/build-attestation.json'])
            attestation['policy_sha256'] = auth.digest(changed['reviews/program-policy.json'])
            attestation['program_review_sha256'] = auth.digest(changed['reviews/program-review.md'])
            changed['reports/build-attestation.json'] = raw(attestation)
            changed_record = dict(record, policy_sha256=attestation['policy_sha256'],
                                  program_review_sha256=attestation['program_review_sha256'],
                                  attestation_sha256=auth.digest(changed['reports/build-attestation.json']))
            self.compare(bundle, changed, manifest, changed_record, 'Packing receipt lacks')

    def test_symbol_hash_equivalence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'app.map'
            golden = b'C: 00008010 foo\r\nC: 00008020 bar\nC: 00008011 foo\n'
            path.write_bytes(golden)
            self.assertEqual(auth.pack.parse_symbols_bytes(golden), {'foo': 0x8011, 'bar': 0x8020})
            self.assertEqual(auth.symbols_sha256_bytes(golden),
                             '438c8d371a50b4a2eb76beacb921cdbf2fbdf5aa728f96b2d1da155e07d1c97f')
            for data in (b'C: 00008010 foo\r\nC: 00008020 bar\n', b''):
                path.write_bytes(data)
                if data:
                    self.assertEqual(auth.symbols_sha256(path), auth.symbols_sha256_bytes(data))
                else:
                    with self.assertRaisesRegex(ValueError, 'MAP has no packing symbols'):
                        auth.symbols_sha256_bytes(data)
                    with self.assertRaisesRegex(ValueError, 'MAP has no packing symbols'):
                        auth.symbols_sha256(path)


if __name__ == '__main__':
    unittest.main()
