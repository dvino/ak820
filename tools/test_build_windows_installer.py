"""Offline standalone packaging allowlist/recipe regressions; no PyInstaller run."""
from pathlib import Path
import tempfile
import sys
import json
import zipfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import build_windows_installer as builder


class WindowsInstallerBuildTests(unittest.TestCase):
    def test_only_reviewed_allowlisted_inputs_and_no_personal_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = ['firmware/application.ihx', 'reference/info.json', 'reference/vial.json']
            required = ['AK820.cmd', 'tools/installer/profile-catalog.json', 'tools/installer/settings-catalog.json']
            required.extend(builder.PUBLIC_GUIDES)
            required.extend(builder.PUBLIC_ASSETS)
            contexts = []
            for profile in ('main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios'):
                bundle = root / 'releases/beta2' / profile
                required.extend(f'releases/beta2/{profile}/{name}' for name in files + ['installer-release.json','approved-release.json'])
                contexts.append(SimpleNamespace(profile=profile, bundle=bundle, approval=bundle/'approved-release.json',
                    manifest={'install_modes': ['permanent','trial'], 'files': {name: {} for name in files}}))
            for name in required + ['evidence/oem-backup/before-full-rom.bin', 'host/runs/private.bin']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'fixture')
            with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'release_contexts', return_value=tuple(contexts)), \
                 patch.object(builder, 'HOST_FILES', {'AK820.cmd', 'tools/installer/profile-catalog.json', 'tools/installer/settings-catalog.json'}):
                self.assertEqual(builder.package_files(), sorted(set(required)))

    def test_old_trial_only_release_is_not_packaged_as_permanent(self):
        context = SimpleNamespace(profile='main', bundle=builder.ROOT/'releases/beta2/main',
            approval=builder.ROOT/'releases/beta2/main/approved-release.json', manifest={'trial_only': True})
        with patch.object(builder.ak820, 'release_contexts', return_value=(context,)):
            with self.assertRaisesRegex(ValueError, 'permanent'):
                builder.package_files()

    def test_missing_or_symlinked_public_guide_blocks_inventory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            guide = root / builder.PUBLIC_GUIDES[0]
            guide.parent.mkdir(parents=True, exist_ok=True)
            guide.write_text('guide', encoding='utf-8')
            with patch.object(builder, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'Missing or unsafe public guide'):
                    builder.guide_files()
                for name in builder.PUBLIC_GUIDES[1:]:
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('guide', encoding='utf-8')
                for name in builder.PUBLIC_ASSETS:
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b'image fixture')
                self.assertEqual(builder.guide_files(), [*builder.PUBLIC_GUIDES, *builder.PUBLIC_ASSETS])
                guide.unlink()
                outside = root / 'outside.md'
                outside.write_text('private', encoding='utf-8')
                guide.symlink_to(outside)
                with self.assertRaisesRegex(ValueError, 'Missing or unsafe public guide'):
                    builder.guide_files()

    def test_public_readme_images_are_explicit_binary_hash_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in builder.PUBLIC_GUIDES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('guide', encoding='utf-8')
            for name in builder.PUBLIC_ASSETS:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'\x00\xffwebp fixture')
            with patch.object(builder, 'ROOT', root):
                names = builder.guide_files()
                hashes = builder.snapshot_inputs(names)
                self.assertEqual(set(names), set((*builder.PUBLIC_GUIDES, *builder.PUBLIC_ASSETS)))
                self.assertEqual(set(hashes), set(names))
                self.assertTrue(all(len(hashes[name]) == 64 for name in builder.PUBLIC_ASSETS))

    def test_tampered_guide_is_detected_by_build_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            name = builder.PUBLIC_GUIDES[0]
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('approved source', encoding='utf-8')
            with patch.object(builder, 'ROOT', root):
                snapshot = builder.snapshot_inputs([name])
                path.write_text('changed while packaging', encoding='utf-8')
                with self.assertRaisesRegex(RuntimeError, 'Approved input changed during build'):
                    builder.verify_sources_unchanged(snapshot)

    def test_missing_or_tampered_alternate_profile_blocks_package_inventory(self):
        # release_contexts validates the complete catalog before returning any
        # contexts, so an invalid non-default profile cannot be silently omitted.
        with patch.object(builder.ak820, 'release_contexts',
                          side_effect=ValueError('tampered profile bundle: shortcuts')):
            with self.assertRaisesRegex(ValueError, 'shortcuts'):
                builder.package_files()

    def test_gui_windowed_cli_console_and_explicit_data_only(self):
        commands = builder.build_commands(Path('output'), Path('work'), ['AK820.cmd'])
        self.assertEqual(len(commands), 2)
        self.assertIn('--windowed', commands[0])
        self.assertEqual(commands[0][commands[0].index('--contents-directory') + 1], '_internal')
        self.assertEqual(commands[1][commands[1].index('--contents-directory') + 1], '_internal')
        self.assertIn('--console', commands[1])
        self.assertNotIn('--console', commands[0])
        self.assertNotIn('--windowed', commands[1])
        self.assertTrue(commands[0][-1].endswith('gui.py'))
        self.assertTrue(commands[1][-1].endswith('ak820.py'))
        self.assertEqual(commands[0].count('--add-data'), 1)

    def test_settings_runtime_is_bound_and_collected_for_both_apps(self):
        required = {'tools/ak820_device_protocol.py', 'tools/installer/settings_backup.py',
                    'tools/installer/settings_workflow.py'}
        self.assertTrue(required <= builder.HOST_FILES)
        for command in builder.build_commands(Path('output'), Path('work'), sorted(required)):
            self.assertIn(str(builder.ROOT / 'tools'), command)
            self.assertEqual(command.count('--add-data'), len(required))

    def test_every_allowlisted_file_is_hash_verified_in_each_app_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names = ['tools/installer/approved-release.json', 'releases/rc6/installer-release.json']
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(('exact:' + name).encode())
            app = root / 'AK820' / '_internal'
            for name in names:
                path = app / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((root / name).read_bytes())
            with patch.object(builder, 'ROOT', root):
                self.assertEqual(set(builder.verify_collected(root / 'AK820', names)), set(names))
                (app / names[0]).write_bytes(b'wrong')
                with self.assertRaisesRegex(RuntimeError, 'hash mismatch'):
                    builder.verify_collected(root / 'AK820', names)

    def test_missing_collected_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(builder, 'ROOT', root):
                with self.assertRaisesRegex(RuntimeError, 'missing packaged approved input'):
                    builder.verify_collected(root / 'AK820', ['release/file.bin'])

    def _synthetic_package(self, root):
        names = ['AK820.cmd', 'releases/beta2/main/installer-release.json', 'releases/beta2/main/approved-release.json']
        for name in names + ['AK820.cmd']:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('source:' + name).encode())
        hashes = {name: builder.sha256(root / name) for name in names}
        output = root / 'AK820-Windows'
        for app in ['AK820', 'AK820-cli']:
            (output / app).mkdir(parents=True)
            (output / app / (app + '.exe')).write_bytes(('exe:' + app).encode())
            for name in names:
                path = output / app / '_internal' / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((root / name).read_bytes())
        return names, hashes, output

    def test_complete_synthetic_package_contains_both_apps_reports_and_zip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names, hashes, output = self._synthetic_package(root)
            archive = Path(str(output) + '.zip')
            context = SimpleNamespace(profile='main', bundle=root/'releases/beta2/main')
            with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'release_contexts', return_value=(context,)), patch.object(builder.sys, 'version', '3.12.0'), \
                 patch.object(builder.subprocess, 'run') as run:
                builder.write_package(output, archive, names, hashes)
            self.assertEqual(run.call_count, 3)
            provenance = json.loads((output / 'build-provenance.json').read_text())
            smoke = json.loads((output / 'smoke-report.json').read_text())
            self.assertEqual(provenance['approved_inputs'], hashes)
            self.assertEqual(provenance['collected_inputs']['AK820'], hashes)
            self.assertEqual(provenance['collected_inputs']['AK820-cli'], hashes)
            self.assertEqual(smoke['native_tk_ui_smoke'], 'passed')
            self.assertIn('No USB enumeration', ' '.join(smoke['limits']))
            with zipfile.ZipFile(archive) as bundle:
                entries = set(bundle.namelist())
            self.assertIn(f'{output.name}/AK820/AK820.exe', entries)
            self.assertIn(f'{output.name}/AK820-cli/AK820-cli.exe', entries)
            self.assertIn(f'{output.name}/build-provenance.json', entries)
            self.assertIn(f'{output.name}/smoke-report.json', entries)
            self.assertIn(f'{output.name}/AK820.cmd', entries)

    def test_native_smoke_failure_writes_no_false_provenance_or_zip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names, hashes, output = self._synthetic_package(root)
            archive = Path(str(output) + '.zip')
            context = SimpleNamespace(profile='main', bundle=root/'releases/beta2/main')
            with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'release_contexts', return_value=(context,)), patch.object(builder.subprocess, 'run', side_effect=[None, None, RuntimeError('Tk failed')]):
                with self.assertRaisesRegex(RuntimeError, 'Tk failed'):
                    builder.write_package(output, archive, names, hashes)
            self.assertFalse((output / 'build-provenance.json').exists())
            self.assertFalse((output / 'smoke-report.json').exists())
            self.assertFalse(archive.exists())

    def test_each_cli_and_ui_smoke_failure_blocks_provenance(self):
        for failing_call in range(3):
            with self.subTest(failing_call=failing_call), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                names, hashes, output = self._synthetic_package(root)
                archive = Path(str(output) + '.zip')
                outcomes = [None, None, None]
                outcomes[failing_call] = RuntimeError('smoke failed')
                context = SimpleNamespace(profile='main', bundle=root/'releases/beta2/main')
                with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'release_contexts', return_value=(context,)), patch.object(builder.subprocess, 'run', side_effect=outcomes):
                    with self.assertRaisesRegex(RuntimeError, 'smoke failed'):
                        builder.write_package(output, archive, names, hashes)
                self.assertFalse((output / 'build-provenance.json').exists())
                self.assertFalse(archive.exists())

    def test_source_change_during_smoke_blocks_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names, hashes, output = self._synthetic_package(root)
            archive = Path(str(output) + '.zip')
            def mutate_on_final_smoke(*args, **kwargs):
                if args[0][1] == '--self-test':
                    (root / names[0]).write_bytes(b'changed')
            context = SimpleNamespace(profile='main', bundle=root/'releases/beta2/main')
            with patch.object(builder, 'ROOT', root), patch.object(builder.ak820, 'release_contexts', return_value=(context,)), patch.object(builder.subprocess, 'run', side_effect=mutate_on_final_smoke):
                with self.assertRaisesRegex(RuntimeError, 'changed during build'):
                    builder.write_package(output, archive, names, hashes)
            self.assertFalse((output / 'build-provenance.json').exists())
            self.assertFalse(archive.exists())

    def test_refuses_existing_output_before_any_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / 'package'
            output.mkdir()
            with patch.object(builder, 'sys') as mocked_sys:
                mocked_sys.platform = 'win32'
                mocked_sys.version = sys.version
                with patch.object(builder.importlib.metadata, 'version', return_value='6.16.0'):
                    with patch.object(builder, 'package_files', side_effect=AssertionError('must gate first')):
                        with self.assertRaises(SystemExit):
                            builder.main(['--output', str(output)])

    def test_rejects_non_windows_before_build(self):
        with patch.object(builder.sys, 'platform', 'linux'):
            with self.assertRaises(SystemExit):
                builder.main([])


if __name__ == '__main__':
    unittest.main()
