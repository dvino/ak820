#!/usr/bin/env python3
"""Offline fixtures for complete, exact-image candidate exports."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import build_profile_catalog as catalog


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / 'result'
        self.names = catalog.firmware_matrix.candidate_names()
        self.assertEqual(len(self.names), 9)
        (self.root / 'web').mkdir()
        (self.root / 'web/module-descriptions.json').write_text('{}')
        reference = self.root / 'keyboards/ajazz/ak820/keymaps/vial'
        reference.mkdir(parents=True)
        (reference / 'vial.json').write_text('{}')
        self.builds, self.rows = {}, {}
        for name in self.names:
            build = self.root / 'builds' / name
            build.mkdir(parents=True)
            identity = {}
            for suffix in ('ihx', 'map', 'mem'):
                path = build / ('ajazz_ak820_vial.' + suffix)
                path.write_text(name + '.' + suffix)
                identity[suffix + '_sha256'] = catalog.configured.sha(path)
            for filename in ('configuration-report.json', 'qualification.json'):
                (build / filename).write_text('{}')
            (build / 'runtime-safety').mkdir()
            (build / 'runtime-safety/summary.json').write_text('{}')
            self.builds[name] = build
            self.rows[name] = dict(identity=identity, configuration={'profile': name},
                                   measurement_status='linked-memory-pass',
                                   runtime_status='exact-image-pass',
                                   offline_tests_status='exact-image-pass')
        for target, value in (('ROOT', self.root), ('QMK', self.root)):
            replacement = patch.object(catalog, target, value)
            replacement.start()
            self.addCleanup(replacement.stop)
        replacement = patch.object(catalog.firmware_matrix, 'matrix',
                                   side_effect=lambda rows: {'profiles': list(rows)})
        replacement.start()
        self.addCleanup(replacement.stop)

    def export(self):
        return catalog.export_catalog(self.builds, self.rows, self.output)

    def assert_clean(self):
        for path in catalog.final_paths(self.output):
            self.assertFalse(path.exists())
            self.assertFalse(path.is_symlink())
        self.assertEqual(list(self.root.glob('.result-stage-*')), [])

    def test_success_exact_nine_and_deterministic_archive(self):
        result, archive = self.export()
        self.assertEqual(result['profiles'], list(self.names))
        manifest = json.loads((self.output / 'candidate-manifest.json').read_text())
        self.assertEqual(manifest['profiles'], list(self.names))
        for field in ('release_approved', 'installable', 'hardware_validated'):
            self.assertIs(manifest[field], False)
        for name in self.names:
            for suffix in ('ihx', 'map', 'mem'):
                copied = self.output / 'profiles' / name / 'firmware' / ('application.' + suffix)
                self.assertEqual(catalog.configured.sha(copied), self.rows[name]['identity'][suffix + '_sha256'])
        with zipfile.ZipFile(archive) as package:
            for entry in package.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(entry.external_attr >> 16, 0o100644)
        self.assertEqual(archive.with_suffix('.zip.sha256').read_text(),
                         catalog.configured.sha(archive) + '  result.zip\n')
        archive_bytes = archive.read_bytes()
        self.output = self.root / 'second' / 'result'
        self.export()
        self.assertEqual(archive_bytes, self.output.with_suffix('.zip').read_bytes())

    def test_stale_artifact_rejected_for_each_exact_identity(self):
        for suffix in ('ihx', 'map', 'mem'):
            with self.subTest(suffix=suffix):
                path = self.builds[self.names[0]] / ('ajazz_ak820_vial.' + suffix)
                original = path.read_bytes()
                path.write_bytes(b'stale')
                with self.assertRaisesRegex(ValueError, 'measured identity'):
                    self.export()
                self.assert_clean()
                path.write_bytes(original)
        self.export()

    def test_interrupted_copy_or_zip_is_retryable(self):
        for target in ('shutil.copyfile', 'zipfile.ZipFile.writestr'):
            with self.subTest(target=target):
                with patch('build_profile_catalog.' + target, side_effect=KeyboardInterrupt):
                    with self.assertRaises(KeyboardInterrupt):
                        self.export()
                self.assert_clean()
        self.export()

    def test_publication_failure_rolls_back_own_outputs(self):
        real_link = catalog.os.link
        calls = 0

        def fail_checksum(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('interrupted checksum publication')
            return real_link(source, destination)

        with patch.object(catalog.os, 'link', side_effect=fail_checksum):
            with self.assertRaises(OSError):
                self.export()
        self.assert_clean()
        self.export()

    def test_existing_outputs_and_dangling_symlinks_refused(self):
        for path in catalog.final_paths(self.output):
            for symlink in (False, True):
                with self.subTest(path=path.name, symlink=symlink):
                    if symlink:
                        path.symlink_to(self.root / 'missing')
                    else:
                        path.write_text('preserve')
                    with self.assertRaisesRegex(ValueError, 'fresh output'):
                        self.export()
                    if symlink:
                        self.assertTrue(path.is_symlink())
                    else:
                        self.assertEqual(path.read_text(), 'preserve')
                    path.unlink()
                    self.assert_clean()

    def test_incomplete_qualification_is_rejected(self):
        self.rows[self.names[0]]['runtime_status'] = 'not-proven'
        with self.assertRaisesRegex(ValueError, 'Incomplete offline qualification'):
            self.export()
        self.assert_clean()


if __name__ == '__main__':
    unittest.main()
