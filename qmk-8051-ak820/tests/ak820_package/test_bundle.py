"""The release verifier must reject stale, additional and missing files."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
from check_ak820_bundle import digest_file, verify


class BundleTest(unittest.TestCase):
    def test_exact_content_and_negative_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / 'trial.bin'
            payload.write_bytes(b'trial')
            row = {'path': 'trial.bin', 'bytes': 5, 'sha256': digest_file(payload)}
            manifest = root / 'CONTENT-MANIFEST.json'
            manifest.write_text(json.dumps({'file_count': 1, 'files': [row]}))
            sums = root / 'SHA256SUMS'
            sums.write_text(row['sha256'] + '  trial.bin\n' + digest_file(manifest) + '  CONTENT-MANIFEST.json\n')
            self.assertEqual(verify(root)['result'], 'PASS')
            payload.write_bytes(b'TRIAL')
            with self.assertRaisesRegex(ValueError, 'SHA256'):
                verify(root)
            payload.write_bytes(b'trial')
            extra = root / 'ak820-vial-permanent.bin'
            extra.write_bytes(b'not-declared')
            with self.assertRaisesRegex(ValueError, 'File set'):
                verify(root)
            extra.unlink()
            payload.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing'):
                verify(root)
