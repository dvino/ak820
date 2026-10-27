"""Regression for exact-image Direct metadata in offline fixtures."""
import importlib.util
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'prepare_release', Path(__file__).with_name('prepare_release.py'))
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)
sys.path.insert(0, str(prepare.ROOT / 'tools/installer'))


class DirectFixtureMetadata(unittest.TestCase):
    def test_direct_capability_is_forwarded_from_exact_image_identity(self):
        import settings_backup as settings
        calls = []

        def capture(*args, **kwargs):
            calls.append(kwargs['direct_capable'])
            return {'limitations': ['Direct' if kwargs['direct_capable'] else 'legacy']}

        # Exercise forwarding for Direct and legacy image identities. Parsers
        # and validators are mocked to keep this unit test independent of
        # private release inputs.
        for direct in (True, False):
            with self.subTest(direct=direct), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp) / 'fixture'
                image = {'ihx_sha256': '1' * 64, 'code_sha256': '2' * 64,
                         'build_id': settings.pack.BUILD_ID}
                if direct:
                    image['direct_protocol'] = 1
                profile = {'definition_sha256': '3' * 64}
                with patch.object(settings, 'validate_rom'), \
                     patch.object(settings, '_rom_identity', return_value=image), \
                     patch.object(settings, 'rgb_wire', return_value=b'valid-rgb'), \
                     patch.object(settings, '_combo_capable', return_value=False), \
                     patch.object(settings, 'validate_backup', return_value={'ok': True}), \
                     patch.object(settings, 'settings_from_nvm', side_effect=capture):
                    result = prepare.make_backup(folder, bytes(settings.pack.NVM_END), profile)
                self.assertEqual(result, {'ok': True})
                self.assertEqual(calls[-1], direct)


if __name__ == '__main__':
    unittest.main()
