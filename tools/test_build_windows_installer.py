"""Offline standalone packaging allowlist/recipe regressions; no PyInstaller run."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_windows_installer as builder


class WindowsInstallerBuildTests(unittest.TestCase):
    def test_only_reviewed_allowlisted_inputs_and_no_personal_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / 'releases/rc6'
            files = ['firmware/application.ihx', 'reference/info.json', 'reference/vial.json']
            required = ['AK820.cmd', 'tools/installer/approved-release.json',
                        'releases/rc6/installer-release.json'] + ['releases/rc6/' + name for name in files]
            for name in required + ['evidence/oem-backup/before-full-rom.bin', 'host/runs/private.bin']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'fixture')
            with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'BUNDLE', bundle), \
                 patch.object(builder, 'HOST_FILES', {'AK820.cmd'}), \
                 patch.object(builder.ak820, 'load_release', return_value={
                     'install_modes': ['permanent', 'trial'], 'files': {name: {'sha256': builder.ak820.packer.NATIVE_PUBLIC_SHA} for name in files}}):
                self.assertEqual(builder.package_files(), sorted(required))

    def test_old_trial_only_release_is_not_packaged_as_permanent(self):
        with patch.object(builder.ak820, 'load_release', return_value={'trial_only': True}):
            with self.assertRaisesRegex(ValueError, 'newly reviewed'):
                builder.package_files()

    def test_gui_windowed_cli_console_and_explicit_data_only(self):
        commands = builder.build_commands(Path('output'), Path('work'), ['AK820.cmd'])
        self.assertEqual(len(commands), 2)
        self.assertIn('--windowed', commands[0])
        self.assertIn('--console', commands[1])
        self.assertNotIn('--console', commands[0])
        self.assertNotIn('--windowed', commands[1])
        self.assertTrue(commands[0][-1].endswith('gui.py'))
        self.assertTrue(commands[1][-1].endswith('ak820.py'))
        self.assertEqual(commands[0].count('--add-data'), 1)


if __name__ == '__main__':
    unittest.main()
