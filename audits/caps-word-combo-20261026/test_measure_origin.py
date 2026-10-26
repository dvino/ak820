"""Negative controls for original-root measurement admission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('measure_origin', Path(__file__).with_name('measure_origin.py'))
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)


class OriginAdmission(unittest.TestCase):
    def test_failed_canonical_measurement_cannot_supply_a_row(self):
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder)
            central, origin = parent / 'central', parent / 'origin'
            relative = Path('qmk-8051-ak820/.build/test/main')
            for root in (central, origin):
                (root / relative / 'profile-tests').mkdir(parents=True)
                (root / relative / 'profile-tests/results.json').write_text(json.dumps(
                    {'tests': [{'command': [sys.executable]}]}))
            native = parent / 'native.bin'
            native.write_bytes(b'offline fixture')
            with patch.object(measure, 'ROOT', central), \
                 patch.object(measure, 'source_files', return_value={}), \
                 patch.object(measure.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)) as run:
                with self.assertRaisesRegex(ValueError, 'Canonical original-root measurement failed'):
                    measure.measured_row(central / relative, origin,
                        central / 'toolchains/sdcc', native, parent / 'output')
                run.assert_called_once()

    def test_changed_source_or_build_blocks_before_subprocess(self):
        for changed_source in (True, False):
            with self.subTest(source=changed_source), tempfile.TemporaryDirectory() as folder:
                parent = Path(folder)
                central, origin = parent / 'central', parent / 'origin'
                relative = Path('qmk-8051-ak820/.build/test/main')
                for root in (central, origin):
                    (root / 'tools').mkdir(parents=True)
                    (root / 'tools/input.py').write_bytes(b'unchanged')
                    (root / relative).mkdir(parents=True)
                    (root / relative / 'image.ihx').write_bytes(b'unchanged')
                altered = origin / ('tools/input.py' if changed_source else relative / 'image.ihx')
                altered.write_bytes(b'changed')
                sources = {'tools/input.py': hashlib.sha256(b'unchanged').hexdigest()}
                with patch.object(measure, 'ROOT', central), \
                     patch.object(measure, 'source_files', return_value=sources), \
                     patch.object(measure.subprocess, 'run') as run:
                    with self.assertRaisesRegex(ValueError, 'source differs|build differs'):
                        measure.measured_row(central / relative, origin,
                            central / 'toolchains/sdcc', parent / 'unused-native.bin', parent / 'output')
                    run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
