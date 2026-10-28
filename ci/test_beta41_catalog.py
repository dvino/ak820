#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from beta41_catalog import ARCHIVE, PROFILES, SOURCE_TAG, TARGET_TAG, canonical, file_records, promote, sha


class Beta41CatalogTests(unittest.TestCase):
    def fixture(self, directory: Path, source_tag: str = SOURCE_TAG) -> None:
        payload = {}
        rows = []
        images = []
        for profile in PROFILES:
            ihx = ('image:' + profile).encode()
            code = ('code:' + profile).encode()
            payload[f'profiles/{profile}/firmware/application.ihx'] = ihx
            rows.append({'profile': profile, 'settings_identity': {
                'ihx_sha256': sha(ihx), 'code_sha256': sha(code)}})
            images.append({'profile': profile, 'flashing_authorized': False,
                           'release_approved': False, 'hardware_validated': False,
                           'settings_writes_authorized': False})
        payload['firmware-matrix.json'] = canonical({'profiles': rows})
        payload['capability-catalog.json'] = canonical({
            'format': 'ak820-development-capability-catalog-1',
            'release_approved': False, 'flashing_authorized': False,
            'hardware_validated': False, 'settings_writes_authorized': False,
            # Catalog producers may order images independently of the firmware matrix.
            'images': list(reversed(images))})
        payload['INSTALL-en.md'] = b'install instructions\n'
        payload['INSTALL-ru.md'] = 'инструкция\n'.encode()
        descriptor = {'format': 'ak820-beta-release-catalog-1', 'tag': source_tag,
                      'status': 'beta', 'default_profile': 'main',
                      'installable_profiles': list(PROFILES),
                      'catalog_profiles': list(PROFILES),
                      'hardware_validated': False, 'flashing_authorized': False,
                      'settings_writes_authorized': False,
                      'assets': file_records(payload)}
        payload['release-catalog.json'] = canonical(descriptor)
        payload['release-manifest.json'] = canonical({
            'format': 'ak820-beta-release-manifest-1', 'tag': source_tag,
            'files': file_records(payload)})
        (directory / 'release-catalog.json').write_bytes(payload['release-catalog.json'])
        (directory / 'capability-catalog.json').write_bytes(payload['capability-catalog.json'])
        (directory / 'release-manifest.json').write_bytes(payload['release-manifest.json'])
        with zipfile.ZipFile(directory / ARCHIVE, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(payload.items()):
                archive.writestr(name, data)

    def test_beta41_is_exactly_bound_and_write_gates_remain_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture(directory)
            digest = promote(directory)
            self.assertEqual(digest, sha((directory / ARCHIVE).read_bytes()))
            with zipfile.ZipFile(directory / ARCHIVE) as archive:
                payload = {name: archive.read(name) for name in archive.namelist()}
            descriptor = json.loads(payload['release-catalog.json'])
            capabilities = json.loads(payload['capability-catalog.json'])
            manifest = json.loads(payload['release-manifest.json'])
            self.assertEqual(descriptor['tag'], TARGET_TAG)
            self.assertTrue(descriptor['release_approved'])
            self.assertTrue(descriptor['flashing_authorized'])
            self.assertFalse(descriptor['hardware_validated'])
            self.assertFalse(descriptor['settings_writes_authorized'])
            self.assertEqual([row['profile'] for row in descriptor['flashing_authorized_images']],
                             list(PROFILES))
            self.assertTrue(capabilities['flashing_authorized'])
            self.assertFalse(capabilities['hardware_validated'])
            self.assertFalse(capabilities['settings_writes_authorized'])
            self.assertEqual([image['profile'] for image in capabilities['images']],
                             list(PROFILES))
            for image in capabilities['images']:
                self.assertTrue(image['flashing_authorized'])
                self.assertFalse(image['hardware_validated'])
                self.assertFalse(image['settings_writes_authorized'])
            for row, authorized in zip(json.loads(payload['firmware-matrix.json'])['profiles'],
                                       descriptor['flashing_authorized_images']):
                self.assertEqual(row['profile'], authorized['profile'])
                self.assertEqual(row['settings_identity']['ihx_sha256'], authorized['ihx_sha256'])
                self.assertEqual(row['settings_identity']['code_sha256'], authorized['code_sha256'])
                self.assertEqual(sha(payload[f"profiles/{row['profile']}/firmware/application.ihx"]),
                                 authorized['ihx_sha256'])
            self.assertEqual(descriptor['assets'], file_records({name: data for name, data in payload.items()
                                                                  if name not in ('release-catalog.json',
                                                                                  'release-manifest.json')}))
            self.assertEqual(manifest['tag'], TARGET_TAG)
            self.assertEqual(manifest['files'], file_records({name: data for name, data in payload.items()
                                                               if name != 'release-manifest.json'}))
            for name in ('release-catalog.json', 'capability-catalog.json', 'release-manifest.json'):
                self.assertEqual((directory / name).read_bytes(), payload[name])

    def test_beta5_requires_beta5_source_and_preserves_write_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture(directory, 'v0.6.0-beta.5')
            promote(directory, 'v0.6.0-beta.5')
            descriptor = json.loads((directory / 'release-catalog.json').read_text())
            self.assertEqual(descriptor['tag'], 'v0.6.0-beta.5')
            self.assertTrue(descriptor['flashing_authorized'])
            self.assertFalse(descriptor['settings_writes_authorized'])
            self.assertFalse(descriptor['hardware_validated'])
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture(directory)
            with self.assertRaisesRegex(ValueError, 'Source catalog'):
                promote(directory, 'v0.6.0-beta.5')

    def test_wrong_tag_and_writable_source_catalog_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture(directory)
            with self.assertRaisesRegex(ValueError, 'Only the exact beta.4.1'):
                promote(directory, 'v0.6.0-beta.6')

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture(directory)
            archive_path = directory / ARCHIVE
            with zipfile.ZipFile(archive_path) as archive:
                payload = {name: archive.read(name) for name in archive.namelist()}
            capabilities = json.loads(payload['capability-catalog.json'])
            capabilities['flashing_authorized'] = True
            payload['capability-catalog.json'] = canonical(capabilities)
            descriptor = json.loads(payload['release-catalog.json'])
            descriptor['assets']['capability-catalog.json'] = {
                'sha256': sha(payload['capability-catalog.json']),
                'size': len(payload['capability-catalog.json'])}
            payload['release-catalog.json'] = canonical(descriptor)
            manifest = json.loads(payload['release-manifest.json'])
            manifest['files']['capability-catalog.json'] = {
                'sha256': sha(payload['capability-catalog.json']),
                'size': len(payload['capability-catalog.json'])}
            manifest['files']['release-catalog.json'] = {
                'sha256': sha(payload['release-catalog.json']),
                'size': len(payload['release-catalog.json'])}
            payload['release-manifest.json'] = canonical(manifest)
            for name in ('release-catalog.json', 'capability-catalog.json', 'release-manifest.json'):
                (directory / name).write_bytes(payload[name])
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, data in sorted(payload.items()):
                    archive.writestr(name, data)
            with self.assertRaisesRegex(ValueError, 'expected read-only release'):
                promote(directory)


if __name__ == '__main__':
    unittest.main()
