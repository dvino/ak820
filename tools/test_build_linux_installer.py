"""Offline Linux archive, identity and executable smoke fixtures; no USB/build."""
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import build_linux_installer as builder


class LinuxBuildTests(unittest.TestCase):
    def fixture(self, root):
        names = ['releases/beta2/main/installer-release.json', 'releases/beta2/main/approved-release.json']
        for name in names:
            path = root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('approved:'+name).encode())
        output = root/'AK820-Linux-x86_64'
        for app in ('AK820', 'AK820-cli'):
            executable = output/app/app
            executable.parent.mkdir(parents=True)
            # Real executable fixture: checks mode/launch/arguments, no Python package.
            executable.write_text('#!/bin/sh\necho AK820_FROZEN_HIDRAW_OK\n')
            executable.chmod(0o755)
            for name in names:
                path = executable.parent/'_internal'/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((root/name).read_bytes())
        binaries = root/'bin'
        binaries.mkdir()
        xvfb = binaries/'xvfb-run'
        xvfb.write_text('#!/bin/sh\n[ "$1" = "-a" ] || exit 2\nshift\nexec "$@"\n')
        xvfb.chmod(0o755)
        hashes = {name: builder.sha256(root/name) for name in names}
        return names, hashes, output, binaries

    def context(self, root, binaries):
        return (patch.object(builder, 'ROOT', root),
                patch.object(builder.shared.ak820, 'release_contexts', return_value=(SimpleNamespace(profile='main', bundle=root/'releases/beta2/main'),)),
                patch.object(builder.shared, 'ROOT', root),
                patch.dict(os.environ, {'PATH': str(binaries)+os.pathsep+os.environ['PATH']}))

    def test_real_executable_smoke_and_tar_modes_hashes_and_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names, hashes, output, binaries = self.fixture(root)
            archive = Path(str(output)+'.tar.gz')
            builder_patch, context_patch, root_patch, env_patch = self.context(root, binaries)
            with builder_patch, context_patch, root_patch, env_patch:
                builder.write_package(output, archive, names, hashes)
            report = json.loads((output/'build-provenance.json').read_text())
            self.assertEqual(report['approved_inputs'], hashes)
            self.assertEqual(report['collected_inputs']['AK820'], hashes)
            self.assertEqual(report['checks']['frozen_hidraw_import'], 'passed')
            with tarfile.open(archive) as bundle:
                entry = bundle.getmember(output.name+'/AK820/AK820')
                self.assertTrue(entry.mode & 0o111)
                self.assertEqual(bundle.extractfile(entry).read(), (output/'AK820/AK820').read_bytes())
                member = output.name+'/AK820/_internal/'+names[0]
                self.assertEqual(bundle.extractfile(member).read(), (root/names[0]).read_bytes())

    def test_tampered_missing_or_nonexecutable_collected_files_block_archive(self):
        for failure in ('tamper', 'missing', 'mode'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                names, hashes, output, binaries = self.fixture(root)
                if failure == 'mode':
                    (output/'AK820/AK820').chmod(0o644)
                elif failure == 'missing':
                    (output/'AK820/_internal'/names[0]).unlink()
                else:
                    (output/'AK820/_internal'/names[0]).write_bytes(b'tampered')
                archive = Path(str(output)+'.tar.gz')
                builder_patch, context_patch, root_patch, env_patch = self.context(root, binaries)
                with builder_patch, context_patch, root_patch, env_patch, self.assertRaises(RuntimeError):
                    builder.write_package(output, archive, names, hashes)
                self.assertFalse(archive.exists())
                self.assertFalse((output/'build-provenance.json').exists())

    def test_safe_internal_library_symlink_preserved_and_escape_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names, hashes, output, binaries = self.fixture(root)
            library = output/'AK820/_internal/libfixture.so'
            library.write_bytes(b'ELF fixture')
            link = library.with_name('libalias.so')
            link.symlink_to(library.name)
            archive = Path(str(output)+'.tar.gz')
            builder_patch, context_patch, root_patch, env_patch = self.context(root, binaries)
            with builder_patch, context_patch, root_patch, env_patch:
                builder.write_package(output, archive, names, hashes)
            with tarfile.open(archive) as bundle:
                self.assertTrue(bundle.getmember(output.name+'/AK820/_internal/libalias.so').issym())
            link.unlink()
            link.symlink_to(root/names[0])
            with self.assertRaisesRegex(ValueError, 'Unsafe archive symlink'):
                builder.archive_members(output)

    def test_each_smoke_failure_blocks_archive_and_provenance(self):
        for stage in range(3):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                names, hashes, output, binaries = self.fixture(root)
                archive = Path(str(output)+'.tar.gz')
                result = subprocess.CompletedProcess([], 0, 'AK820_FROZEN_HIDRAW_OK')
                outcomes = [result]*3
                outcomes[stage] = subprocess.CalledProcessError(1, 'fixture')
                with patch.object(builder.shared.ak820, 'release_contexts', return_value=(SimpleNamespace(profile='main', bundle=root/'releases/beta2/main'),)), \
                     patch.object(builder.shared, 'ROOT', root), \
                     patch.object(builder.subprocess, 'run', side_effect=outcomes), self.assertRaises(subprocess.CalledProcessError):
                    builder.write_package(output, archive, names, hashes)
                self.assertFalse(archive.exists())
                self.assertFalse((output/'build-provenance.json').exists())

    def test_backend_proof_and_source_mutation_fail_closed(self):
        for mutation in (False, True):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                names, hashes, output, binaries = self.fixture(root)
                archive = Path(str(output)+'.tar.gz')
                def smoke(*args, **kwargs):
                    if mutation:
                        (root/names[0]).write_bytes(b'changed')
                    return subprocess.CompletedProcess([], 0, 'AK820_FROZEN_HIDRAW_OK' if mutation else '')
                with patch.object(builder.shared.ak820, 'release_contexts', return_value=(SimpleNamespace(profile='main', bundle=root/'releases/beta2/main'),)), \
                     patch.object(builder.shared, 'ROOT', root), patch.object(builder.subprocess, 'run', side_effect=smoke), \
                     self.assertRaises(RuntimeError):
                    builder.write_package(output, archive, names, hashes)
                self.assertFalse(archive.exists())

    def test_runtime_hook_imports_hidraw_without_enumerating(self):
        with tempfile.TemporaryDirectory() as temporary:
            extension = Path(temporary)/'hid.so'
            for data, accepted in ((b'ELF hidraw', True), (b'ELF libusb_init', False),
                                   (b'ELF hidraw libusb_init', False)):
                extension.write_bytes(data)
                hid = SimpleNamespace(__file__=str(extension),
                    enumerate=lambda: self.fail('Backend smoke must never enumerate USB'))
                with patch.dict(builder.sys.modules, {'hid': hid}),                      patch.dict(os.environ, {'AK820_CHECK_HIDRAW': '1'}):
                    if accepted:
                        with patch('builtins.print') as output:
                            exec(builder.HIDRAW_HOOK, {})
                        output.assert_called_once_with('AK820_FROZEN_HIDRAW_OK', flush=True)
                    else:
                        with self.assertRaisesRegex(RuntimeError, 'hidraw backend'):
                            exec(builder.HIDRAW_HOOK, {})

    def test_recipe_uses_colon_and_pinned_runtime_hook(self):
        commands = builder.build_commands(Path('out'), Path('work'), ['tools/installer/gui.py'])
        for command in commands:
            data = command[command.index('--add-data')+1]
            self.assertEqual(data, str(builder.ROOT/'tools/installer/gui.py')+os.pathsep+'tools/installer')
            self.assertIn('--runtime-hook', command)
            self.assertIn('--onedir', command)
        self.assertIn('--windowed', commands[0])
        self.assertIn('--console', commands[1])

    def test_platform_and_abi_guard(self):
        for system, machine, libc in [('win32', 'x86_64', ('glibc', '2.35')),
                                      ('linux', 'aarch64', ('glibc', '2.35')),
                                      ('linux', 'x86_64', ('glibc', '2.36')),
                                      ('linux', 'x86_64', ('musl', '1.2'))]:
            with patch.object(builder.sys, 'platform', system), patch.object(builder.platform, 'machine', return_value=machine), \
                 patch.object(builder.platform, 'libc_ver', return_value=libc), self.assertRaises(ValueError):
                builder.check_platform()
        with patch.object(builder.sys, 'platform', 'linux'), patch.object(builder.platform, 'machine', return_value='x86_64'), \
             patch.object(builder.platform, 'libc_ver', return_value=('glibc', '2.35')):
            builder.check_platform()

    def test_existing_output_or_archive_blocks_before_package_read(self):
        for kind in ('output', 'archive'):
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary)/'package'
                if kind == 'output':
                    output.mkdir()
                else:
                    Path(str(output)+'.tar.gz').write_bytes(b'existing')
                with patch.object(builder, 'check_platform'), patch.object(builder.importlib.metadata, 'version',
                     side_effect=lambda name: '6.16.0' if name == 'pyinstaller' else '0.15.0'), \
                     patch.object(builder, 'package_files', side_effect=AssertionError('gate first')), self.assertRaises(SystemExit):
                    builder.main(['--output', str(output)])


if __name__ == '__main__':
    unittest.main()
