"""Reject accidental permanent images in a trial-only release, without USB."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
from check_ak820_release import image_variants


class ReleaseVariantsTest(unittest.TestCase):
    def test_trial_only_rejects_permanent_file_or_manifest_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'snapshot').mkdir()
            meta = {'trial_only': True, 'images': {'ak820-vial-trial.bin': {}, 'restore-native.bin': {}}}
            self.assertEqual(image_variants(root, meta), [('ak820-vial-trial.bin', True)])
            extra = root / 'snapshot/ak820-vial-permanent.bin'
            extra.write_bytes(b'')
            with self.assertRaises(ValueError):
                image_variants(root, meta)
            extra.unlink()
            meta['images']['ak820-vial-permanent.bin'] = {}
            with self.assertRaises(ValueError):
                image_variants(root, meta)

    def test_historical_dual_release_remains_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            meta = {'images': {'ak820-vial-trial.bin': {}, 'restore-native.bin': {},
                               'ak820-vial-permanent.bin': {}}}
            self.assertEqual(len(image_variants(root, meta)), 2)
            meta['trial_only'] = 'false'
            with self.assertRaises(ValueError):
                image_variants(root, meta)
