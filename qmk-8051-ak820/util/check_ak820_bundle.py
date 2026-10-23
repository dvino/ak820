#!/usr/bin/env python3
"""Verify the exact local release file set and SHA256; never opens USB."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def digest_file(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def checked_path(root, name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name or not path.parts:
        raise ValueError(f'Unsafe manifest path: {name!r}')
    target = (root / Path(*path.parts)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f'Manifest path escapes release: {name!r}')
    return target


def verify(directory):
    root = Path(directory).resolve()
    manifest = json.loads((root / 'CONTENT-MANIFEST.json').read_text(encoding='utf-8'))
    rows = manifest['files']
    if manifest['file_count'] != len(rows):
        raise ValueError('Wrong manifest file_count')
    expected = {}
    for row in rows:
        name = row['path']
        if name in expected or name in ('CONTENT-MANIFEST.json', 'SHA256SUMS'):
            raise ValueError(f'Duplicate or self-referential path: {name}')
        path = checked_path(root, name)
        if not path.is_file() or path.stat().st_size != row['bytes']:
            raise ValueError(f'Missing file or wrong size: {name}')
        value = digest_file(path)
        if value != row['sha256']:
            raise ValueError(f'SHA256 mismatch: {name}')
        expected[name] = value
    actual = set()
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Unexpected symbolic link: {path.relative_to(root)}')
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    declared = set(expected) | {'CONTENT-MANIFEST.json', 'SHA256SUMS'}
    if actual != declared:
        raise ValueError(f'File set mismatch: extra={sorted(actual - declared)[:5]}, missing={sorted(declared - actual)[:5]}')
    expected['CONTENT-MANIFEST.json'] = digest_file(root / 'CONTENT-MANIFEST.json')
    sums = {}
    for line in (root / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        value, name = line.split('  ', 1)
        checked_path(root, name)
        if name in sums or len(value) != 64:
            raise ValueError(f'Invalid SHA256SUMS entry: {name}')
        sums[name] = value
    if sums != expected:
        raise ValueError('SHA256SUMS does not agree with the complete manifest')
    return {'result': 'PASS', 'files_verified': len(rows), 'usb_opened': False,
            'physical_device_operations': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', default='.')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.directory), indent=2))
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(f'FAIL: {error}')


if __name__ == '__main__':
    main()
