#!/usr/bin/env python3
"""Build standalone GUI/CLI folders from an approved release; never opens USB.

Install tools/installer/requirements-build-windows.txt in a dedicated Windows
Python environment, then run this script. Personal backups/runs are never added.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import shutil
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'installer'))
import ak820
from ak820_release_manifest import HOST_FILES


def package_files():
    """Use an allowlist, never copy a checkout or personal recovery directory."""
    manifest = ak820.load_release(approved=True)
    if manifest.get('install_modes') != ['permanent', 'trial']:
        raise ValueError('Standalone permanent installer requires a newly reviewed permanent-capable release')
    relative_bundle = ak820.BUNDLE.relative_to(ROOT)
    names = set(HOST_FILES)
    names.update((relative_bundle / name).as_posix() for name in manifest['files'])
    names.add((relative_bundle / 'installer-release.json').as_posix())
    names.add('tools/installer/approved-release.json')
    for name in names:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or path.parts[0] in ('evidence', 'host'):
            raise ValueError('Unsafe standalone package input: ' + name)
        if not (ROOT / path).is_file():
            raise ValueError('Missing standalone package input: ' + name)
    return sorted(names)


def build_commands(output: Path, work: Path, names: list[str]):
    common = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir',
              '--distpath', str(output), '--workpath', str(work / 'work'), '--specpath', str(work),
              '--paths', str(ROOT / 'tools/installer'),
              '--paths', str(ROOT / 'qmk-8051-ak820/util'), '--hidden-import', 'hid']
    for name in names:
        common.extend(['--add-data', str(ROOT / name) + ';' + str(Path(name).parent)])
    return [common + ['--windowed', '--name', 'AK820', str(ROOT / 'tools/installer/gui.py')],
            common + ['--console', '--name', 'AK820-cli', str(ROOT / 'tools/installer/ak820.py')]]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--work', type=Path, default=ROOT / '.build-windows-installer')
    args = parser.parse_args(argv)
    if sys.platform != 'win32':
        parser.error('Build on Windows; cross-compiling a Windows executable is unsupported')
    if importlib.metadata.version('pyinstaller') != '6.16.0':
        parser.error('Use the pinned requirements-build-windows.txt environment')
    names = package_files()
    args.work.mkdir(parents=True, exist_ok=True)
    for command in build_commands(args.output.resolve(), args.work.resolve(), names):
        subprocess.run(command, check=True, cwd=ROOT)
    console = args.output.resolve() / 'AK820-cli' / 'AK820-cli.exe'
    # Both smoke checks are entirely offline and must succeed before delivery.
    subprocess.run([str(console), '--help'], check=True)
    subprocess.run([str(console), 'verify'], check=True)
    subprocess.run([str(args.output.resolve() / 'AK820' / 'AK820.exe'), '--self-test'], check=True)
    shutil.copyfile(ROOT / 'AK820.cmd', args.output.resolve() / 'AK820.cmd')
    print('Standalone GUI:', args.output.resolve() / 'AK820' / 'AK820.exe')
    print('Standalone CLI:', console)
    print('Personal backups were not packaged. Runtime sessions use LocalAppData/AK820/runs.')


if __name__ == '__main__':
    main()
