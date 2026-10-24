#!/usr/bin/env python3
"""Build native Linux x86_64 standalone GUI/CLI; smoke checks never access USB."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import tarfile

import build_windows_installer as shared
from build_windows_installer import (package_files, snapshot_inputs, verify_sources_unchanged,
                                     verify_collected, sha256)
ROOT = shared.ROOT
FORMAT = 'ak820-linux-package-v1'
# Executed inside each frozen interpreter, before its application entry point.
# Importing hid does not enumerate or open USB. hidraw and libusb are distinct
# hidapi build backends; reject the libusb symbol rather than trusting pip flags.
HIDRAW_HOOK = '''import os
if os.environ.get("AK820_CHECK_HIDRAW") == "1":
    import hid
    from pathlib import Path
    image = Path(hid.__file__).read_bytes()
    if not callable(hid.enumerate) or b"hidraw" not in image or b"libusb_init" in image:
        raise RuntimeError("Frozen hid extension is not the required hidraw backend")
    print("AK820_FROZEN_HIDRAW_OK", flush=True)
'''


def check_platform():
    if sys.platform != 'linux' or platform.machine().lower() not in ('x86_64', 'amd64'):
        raise ValueError('Build on native Linux x86_64; cross-compiling is unsupported')
    libc, version = platform.libc_ver()
    if libc != 'glibc' or version != '2.35':
        raise ValueError('Build on glibc 2.35 (Ubuntu 22.04) for the supported ABI baseline')


def build_commands(output, work, names):
    hook = work / 'check_hidraw.py'
    common = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir',
              '--contents-directory', '_internal', '--distpath', str(output),
              '--workpath', str(work/'work'), '--specpath', str(work),
              '--paths', str(ROOT/'tools/installer'), '--paths', str(ROOT/'tools'),
              '--paths', str(ROOT/'qmk-8051-ak820/util'), '--hidden-import', 'hid',
              '--runtime-hook', str(hook)]
    for name in names:
        common.extend(['--add-data', str(ROOT/name) + os.pathsep + str(Path(name).parent)])
    return [common + ['--windowed', '--name', 'AK820', str(ROOT/'tools/installer/gui.py')],
            common + ['--console', '--name', 'AK820-cli', str(ROOT/'tools/installer/ak820.py')]]


def archive_members(output):
    """Accept regular files/directories and internal relative links only.

    PyInstaller uses shared-library symlinks. Keep these links but reject links
    outside the archive root, special files and unsafe archive member names.
    """
    output = output.resolve()
    paths = sorted(output.rglob('*'))
    for path in paths:
        relative = path.relative_to(output)
        if '..' in relative.parts or relative.is_absolute():
            raise ValueError('Unsafe archive member')
        if path.is_symlink():
            target = os.readlink(path)
            if os.path.isabs(target) or not path.resolve().is_relative_to(output) or not path.resolve().is_file():
                raise ValueError('Unsafe archive symlink: ' + str(relative))
        elif not (path.is_file() or path.is_dir()):
            raise ValueError('Special file in package: ' + str(relative))
    return paths


def write_package(output, archive, names, initial_hashes):
    if archive.exists() or archive.is_symlink():
        raise ValueError('Refusing to overwrite existing archive')
    archive_members(output)
    apps = {name: output/name/name for name in ('AK820', 'AK820-cli')}
    for executable in apps.values():
        if executable.is_symlink() or not executable.is_file() or not executable.stat().st_mode & stat.S_IXUSR:
            raise RuntimeError('Missing native executable or executable permission: ' + str(executable))
    collected = {name: verify_collected(output/name, names) for name in apps}
    if any(value != initial_hashes for value in collected.values()):
        raise RuntimeError('Collected inputs differ from pre-build approved hashes')
    environment = os.environ | {'AK820_CHECK_HIDRAW': '1'}
    commands = [[str(apps['AK820-cli']), '--help'], [str(apps['AK820-cli']), 'verify'],
                ['xvfb-run', '-a', str(apps['AK820']), '--self-test']]
    for command in commands:
        result = subprocess.run(command, check=True, cwd=output, env=environment,
                                capture_output=True, text=True)
        if 'AK820_FROZEN_HIDRAW_OK' not in result.stdout:
            raise RuntimeError('Frozen hidraw import check did not run')
    verify_sources_unchanged(initial_hashes)
    if {name: verify_collected(output/name, names) for name in apps} != collected:
        raise RuntimeError('Packaged inputs changed during smoke checks')
    checks = {'cli_help': 'passed', 'offline_verify': 'passed',
              'native_tk_ui_smoke_xvfb': 'passed', 'frozen_hidraw_import': 'passed'}
    limits = ['No USB enumeration or access was performed.',
              'Xvfb smoke creates Tk widgets; manual interaction and physical behavior were not tested.',
              'No firmware update or durable device storage was tested.']
    report = {'format': FORMAT, 'platform': {'system': 'Linux', 'architecture': 'x86_64',
              'glibc_baseline': '2.35', 'python': sys.version.split()[0], 'pyinstaller': '6.16.0'},
              'approved_inputs': initial_hashes, 'collected_inputs': collected,
              'apps': {name: {'sha256': sha256(path)} for name, path in apps.items()},
              'checks': checks, 'limits': limits,
              'private_data': 'OEM backups and runtime sessions were not included.'}
    (output/'build-provenance.json').write_text(json.dumps(report, indent=2)+'\n')
    (output/'smoke-report.json').write_text(json.dumps(checks | {'limits': limits}, indent=2)+'\n')
    members = archive_members(output)
    with archive.open('xb') as stream:
        with tarfile.open(fileobj=stream, mode='w:gz', dereference=False) as bundle:
            bundle.add(output, arcname=output.name, recursive=False)
            for path in members:
                bundle.add(path, arcname=(Path(output.name)/path.relative_to(output)).as_posix(), recursive=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist/AK820-Linux-x86_64')
    parser.add_argument('--work', type=Path, default=ROOT/'.build-linux-installer')
    args = parser.parse_args(argv)
    try:
        check_platform()
    except ValueError as error:
        parser.error(str(error))
    for name, version in (('pyinstaller', '6.16.0'), ('hidapi', '0.15.0')):
        if importlib.metadata.version(name) != version:
            parser.error('Use requirements-build-linux.txt with the pinned hidraw source build')
    output, work = args.output.absolute(), args.work.absolute()
    archive = Path(str(output)+'.tar.gz')
    if output.exists() or output.is_symlink() or archive.exists() or archive.is_symlink():
        parser.error('Refusing to overwrite output or archive')
    if work.exists():
        parser.error('Choose a fresh work directory')
    names = package_files()
    for name in names:
        if not (ROOT/name).resolve().is_relative_to(ROOT.resolve()):
            parser.error('Approved source symlink escapes the repository')
    initial = snapshot_inputs(names)
    work.mkdir(parents=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    (work/'check_hidraw.py').write_text(HIDRAW_HOOK)
    for command in build_commands(output, work, names):
        subprocess.run(command, check=True, cwd=ROOT)
    write_package(output, archive, names, initial)
    print('Standalone Linux package:', archive)


if __name__ == '__main__':
    main()
