import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import build_beta_release_assets as assets


class BundleValidationTests(unittest.TestCase):
    def test_accepts_ci_reproduced_bundle_and_current_pins(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundle = root / 'bundle'
            for part in ('firmware', 'reports', 'reviews'):
                (bundle / part).mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(assets.CANDIDATE_ZIP) as catalog:
                ihx = catalog.read('profiles/work/firmware/application.ihx')
            content = {'firmware/application.ihx': ihx, 'firmware/application.map': b'm',
                       'reports/build-report.json': b'r'}
            for name, data in content.items(): (bundle / name).write_bytes(data)
            (root / 'example.py').write_bytes(b'x')
            policy = {'source_files': {'example.py': {'sha256': assets.sha(b'x'), 'size': 1}}}
            (root / 'ci').mkdir()
            (root / 'ci/release-policy.json').write_text(json.dumps(policy))
            (root / 'ci/release-safety.json').write_text(json.dumps({'program': {'ihx_sha256': assets.WORK_IHX}, 'source_files': {}, 'witnesses': {}}))
            (bundle / 'reviews/program-policy.json').write_bytes((root / 'ci/release-policy.json').read_bytes())
            content['reviews/program-policy.json'] = (bundle / 'reviews/program-policy.json').read_bytes()
            files = {name: {'sha256': assets.sha(data), 'size': len(data)} for name, data in content.items()}
            (bundle / 'reviews/independent-review.md').write_text('review')
            files['reviews/independent-review.md'] = {'sha256': assets.sha(b'review'), 'size': 6}
            manifest = {'files': files, 'host_files': {}}
            (bundle / 'installer-release.json').write_text(json.dumps(manifest))
            record = {'format': 'ak820-reproduced-review-1', 'host_files': {}, 'build': {
                'ihx_sha256': files['firmware/application.ihx']['sha256'],
                'map_sha256': files['firmware/application.map']['sha256'],
                'build_report_sha256': files['reports/build-report.json']['sha256']}}
            identity = root / 'identity.json'
            identity.write_text(json.dumps({'ihx_sha256': assets.WORK_IHX, 'code_sha256': assets.WORK_CODE}))
            with patch.object(assets, 'ROOT', root), patch.object(assets, 'WORK_IDENTITY', identity), \
                 patch.object(assets, 'read_review_record', return_value=record), \
                 patch.object(assets, 'validate_host_manifest'), \
                 patch.object(assets.authorization, 'validate_bundle_authorization') as auth:
                result = assets.validate_bundle(bundle)
                self.assertEqual(result['files']['firmware/application.ihx']['size'], len(ihx))
                auth.assert_called_once()

    def test_rejects_modified_manifest_file(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = Path(temp); (bundle / 'firmware').mkdir()
            (bundle / 'firmware/application.ihx').write_bytes(b'changed')
            (bundle / 'installer-release.json').write_text(json.dumps({'files': {
                'firmware/application.ihx': {'sha256': '0' * 64, 'size': 1}}}))
            with patch.object(assets, 'ROOT', bundle), self.assertRaisesRegex(ValueError, 'hash/size mismatch'):
                assets.validate_bundle(bundle)

    def test_rejects_unsafe_paths(self):
        for value in ('../escape', '/absolute', 'a\\..\\b', 'a//b', 'a/./b'):
            with self.subTest(value=value), self.assertRaises(ValueError): assets._safe_name(value)

    def test_rejects_symlink_ancestor_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundle = root / 'bundle'; outside = root / 'outside'
            (bundle / 'firmware').mkdir(parents=True); outside.mkdir()
            (bundle / 'firmware/application.ihx').write_bytes(b'i')
            (outside / 'build-report.json').write_bytes(b'private')
            (bundle / 'reports').symlink_to(outside, target_is_directory=True)
            files = {
                'firmware/application.ihx': {'sha256': assets.sha(b'i'), 'size': 1},
                'reports/build-report.json': {'sha256': assets.sha(b'private'), 'size': 7},
            }
            (bundle / 'installer-release.json').write_text(json.dumps({'files': files}))
            with patch.object(assets, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Missing or unsafe'):
                assets.validate_bundle(bundle)

    def test_rejects_symlinked_bundle_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); outside = root / 'outside'; outside.mkdir()
            (root / 'linked-bundle').symlink_to(outside, target_is_directory=True)
            with patch.object(assets, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Symlink in bundle path'):
                assets.validate_bundle(root / 'linked-bundle')


class PromotionTests(unittest.TestCase):
    def test_build_archives_hash_closed_work_only_release(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle, output = Path(temp) / 'bundle', Path(temp) / 'assets'
            bundle.mkdir()
            with patch.object(assets, 'validate_bundle', return_value={}):
                assets.build(bundle, output, 'v0.6.0-beta.1')
            archive = output / 'AK820-Beta1-Catalog.zip'
            self.assertTrue((output / 'INSTALL-en.md').is_file())
            self.assertTrue((output / 'INSTALL-ru.md').is_file())
            self.assertIn('AK820-Beta1-Catalog.zip', (output / 'INSTALL-en.md').read_text())
            self.assertIn('AK820-Beta1-Catalog.zip', (output / 'INSTALL-ru.md').read_text())
            self.assertEqual((output / 'AK820-Beta1-Catalog.zip.sha256').read_text().split()[0], assets.sha(archive.read_bytes()))
            with zipfile.ZipFile(archive) as zf:
                members = {name: zf.read(name) for name in zf.namelist()}
            manifest = json.loads(members['release-manifest.json'])
            for name, item in manifest['files'].items():
                self.assertEqual({'sha256': assets.sha(members[name]), 'size': len(members[name])}, item)
            descriptor = json.loads(members['release-catalog.json'])
            self.assertEqual(descriptor['installable_profiles'], ['work'])
            matrix = json.loads(members['firmware-matrix.json'])
            approved = [row['profile'] for row in matrix['profiles'] if row['release_approved'] or row['installable']]
            self.assertEqual(approved, ['work'])
            self.assertEqual(next(row for row in matrix['profiles'] if row['profile'] == 'work')['settings_status'],
                             'reviewed-exact-packed-code')
            caps = json.loads(members['capability-catalog.json'])
            self.assertTrue(next(row for row in caps['images'] if row['profile'] == 'work')['release_approved'])
            self.assertEqual([row['profile'] for row in caps['images'] if row['release_approved']], ['work'])
            self.assertFalse(caps['flashing_authorized'])
            self.assertFalse(caps['settings_writes_authorized'])
            self.assertFalse(caps['hardware_validated'])

    def test_tampered_work_settings_pin_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp) / 'identity.json'
            record.write_text(json.dumps({'ihx_sha256': assets.WORK_IHX, 'code_sha256': '0' * 64}))
            with patch.object(assets, 'WORK_IDENTITY', record), self.assertRaisesRegex(ValueError, 'CODE identity'):
                assets.validate_work_identity()

    def test_cross_profile_firmware_link_is_rejected(self):
        payload = assets._catalog_payload()
        matrix = json.loads(payload['firmware-matrix.json'])
        row = next(item for item in matrix['profiles'] if item['profile'] != 'work')
        payload['profiles/' + row['profile'] + '/firmware/application.ihx'] = payload['profiles/work/firmware/application.ihx']
        with self.assertRaisesRegex(ValueError, 'does not match matrix'):
            assets.validate_profile_links(payload)


if __name__ == '__main__': unittest.main()
