#!/usr/bin/env python3
"""Build and qualify the finite AK820 candidate catalog without accessing USB.

One small ZIP contains the linked applications and their exact capability
matrix. It is input for beta preparation, not an approved flashing bundle.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

import configure_firmware as configured
import firmware_matrix
import build_ci_profiles

ROOT, QMK = configured.ROOT, configured.QMK


def _stage_catalog(builds, rows, output):
    """Export only a complete, independently revalidated offline catalog."""
    names = firmware_matrix.candidate_names()
    if set(rows) != set(names) or set(builds) != set(names):
        raise ValueError('Every curated profile needs exact build evidence')
    for name in names:
        row = rows[name]
        if (row['measurement_status'], row['runtime_status'], row['offline_tests_status']) != (
                'linked-memory-pass', 'exact-image-pass', 'exact-image-pass'):
            raise ValueError('Incomplete offline qualification: ' + name)
    output.mkdir(parents=True, exist_ok=False)
    catalog = firmware_matrix.matrix(rows)
    (output / 'firmware-matrix.json').write_bytes(configured.canonical(catalog))
    shutil.copyfile(ROOT / 'web/module-descriptions.json', output / 'module-descriptions.json')
    for name in names:
        source, destination = builds[name], output / 'profiles' / name
        firmware = destination / 'firmware'
        firmware.mkdir(parents=True)
        for suffix in ('ihx', 'map', 'mem'):
            copied = firmware / ('application.' + suffix)
            shutil.copyfile(source / ('ajazz_ak820_vial.' + suffix), copied)
            if configured.sha(copied) != rows[name]['identity'][suffix + '_sha256']:
                raise ValueError('Copied artifact differs from measured identity: ' + name + '.' + suffix)
        (destination / 'configuration.json').write_bytes(configured.canonical(rows[name]['configuration']))
        for filename in ('configuration-report.json', 'qualification.json'):
            shutil.copyfile(source / filename, destination / filename)
        shutil.copyfile(source / 'runtime-safety/summary.json', destination / 'runtime-safety.json')
        reference = destination / 'reference'
        reference.mkdir()
        shutil.copyfile(QMK / 'keyboards/ajazz/ak820/keymaps/vial/vial.json', reference / 'vial.json')
    manifest = {
        'format': 'ak820-candidate-bundle-1', 'default_profile': configured.profiles.DEFAULT_PROFILE,
        'profiles': list(names), 'release_approved': False, 'installable': False,
        'hardware_validated': False, 'physical_device_commands': 0,
        'files': {path.relative_to(output).as_posix(): {
            'sha256': configured.sha(path), 'size': path.stat().st_size}
            for path in sorted(output.rglob('*')) if path.is_file()},
    }
    (output / 'candidate-manifest.json').write_bytes(configured.canonical(manifest))
    archive = output.with_suffix('.zip')
    if archive.exists():
        raise ValueError('Candidate archive already exists: ' + str(archive))
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for path in sorted(output.rglob('*')):
            if not path.is_file():
                continue
            entry = zipfile.ZipInfo(path.relative_to(output).as_posix(), (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            package.writestr(entry, path.read_bytes())
    archive.with_suffix('.zip.sha256').write_text(configured.sha(archive) + '  ' + archive.name + '\n')
    return catalog, archive


def final_paths(output):
    archive = output.with_suffix('.zip')
    return output, archive, archive.with_suffix('.zip.sha256')


def preflight_output(output):
    paths = final_paths(output)
    if len(set(paths)) != 3:
        raise ValueError('Candidate output and archive paths must differ')
    for path in paths:
        if os.path.lexists(path):
            raise ValueError('Select a fresh output path: ' + str(path))
    return paths


def export_catalog(builds, rows, output):
    """Stage all bytes and publish only a complete offline catalog.

    Roll back only paths published by this invocation if publication fails.
    """
    output = Path(output)
    finals = preflight_output(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    published = []
    with tempfile.TemporaryDirectory(prefix='.' + output.name + '-stage-', dir=output.parent) as temporary:
        staged = Path(temporary) / output.name
        catalog, _ = _stage_catalog(builds, rows, staged)
        preflight_output(output)
        try:
            for source, destination in zip(final_paths(staged), finals):
                if source.is_dir():
                    # Refuse even dangling symlinks before the directory rename.
                    if os.path.lexists(destination):
                        raise ValueError('Candidate output already exists: ' + str(destination))
                    source.rename(destination)
                else:
                    # Hard linking publishes each complete file without replacing
                    # an existing file or symlink, including a concurrent writer.
                    os.link(source, destination)
                published.append((destination, destination.stat()))
        except BaseException:
            for path, identity in reversed(published):
                try:
                    current = path.lstat()
                except FileNotFoundError:
                    continue
                if (current.st_dev, current.st_ino) != (identity.st_dev, identity.st_ino):
                    continue
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            raise
    return catalog, finals[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Print the finite CI build matrix and exit')
    parser.add_argument('--build-root', type=Path, default=QMK / '.build/catalog')
    parser.add_argument('--output', type=Path, default=ROOT / '.build/firmware-catalog')
    parser.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    parser.add_argument('--qmk-bin', type=Path, default=QMK / '.venv/bin/qmk')
    parser.add_argument('--python', type=Path, default=Path(sys.executable))
    parser.add_argument('--native-reference', type=Path)
    parser.add_argument('--resume', action='store_true', help='Requalify existing linked builds; never skip gates')
    args = parser.parse_args(argv)
    names = firmware_matrix.candidate_names()
    if args.list:
        print(json.dumps({'include': [{'profile': name, 'short_calls': True} for name in names]}))
        return 0
    build_root, output = args.build_root.resolve(), args.output.absolute()
    if not build_root.is_relative_to(QMK.resolve()):
        raise ValueError('Build root must remain beneath the QMK source root')
    preflight_output(output)
    toolchain = configured.validate_tools(args.toolchain)
    builds = {name: build_root / name for name in names}
    if args.resume:
        if not all(build.is_dir() for build in builds.values()):
            raise ValueError('Resume requires every linked profile; use a fresh build root after an interrupted build')
        for name, build in builds.items():
            print('QUALIFY', name, flush=True)
            configured.qualify(build, toolchain)
    else:
        build_ci_profiles.build_all(build_root, build_root / 'bootstrap', toolchain,
                                    args.qmk_bin, args.python)
    # Revalidate earlier entries after the last qualification, so a mid-run
    # source/checker edit cannot leave a mixed catalog marked successful.
    rows = {name: firmware_matrix.measured_row(builds[name], toolchain, args.native_reference)
            for name in names}
    _, archive = export_catalog(builds, rows, output)
    print(json.dumps({'catalog': str(output / 'firmware-matrix.json'), 'archive': str(archive),
                      'profiles': len(rows), 'release_approved': False, 'installable': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
