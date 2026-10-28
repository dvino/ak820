#!/usr/bin/env python3
"""Promote the verified beta.4 catalog payload to beta.4.1 metadata."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile
import zipfile

PROFILES = (
    'main', 'game', 'mmo', 'typing', 'code', 'pointer', 'onehand',
    'creative', 'shortcuts', 'multios',
)
SOURCE_TAG = 'v0.6.0-beta.4'
TARGET_TAG = 'v0.6.0-beta.4.1'
ARCHIVE = 'AK820-Beta3-Catalog.zip'


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')).encode('utf-8') + b'\n'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_records(payload: dict[str, bytes]) -> dict[str, dict[str, object]]:
    return {name: {'sha256': sha(data), 'size': len(data)}
            for name, data in sorted(payload.items())}


def promote(directory: Path, tag: str = TARGET_TAG) -> str:
    if tag != TARGET_TAG:
        raise ValueError('Only the exact beta.4.1 catalog may authorize flashing')
    archive_path = directory / ARCHIVE
    if archive_path.is_symlink() or not archive_path.is_file():
        raise ValueError('Missing regular beta.4 catalog archive')
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or any(name.startswith('/') or '\\' in name
                                                or '..' in Path(name).parts for name in names):
            raise ValueError('Catalog archive contains duplicate or unsafe paths')
        payload = {name: archive.read(name) for name in names}

    descriptor = json.loads(payload['release-catalog.json'])
    matrix = json.loads(payload['firmware-matrix.json'])
    capabilities = json.loads(payload['capability-catalog.json'])
    manifest = json.loads(payload['release-manifest.json'])
    for name in ('release-catalog.json', 'capability-catalog.json', 'release-manifest.json'):
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.read_bytes() != payload[name]:
            raise ValueError('Standalone metadata differs from its catalog archive: ' + name)
    if descriptor.get('tag') != SOURCE_TAG or descriptor.get('format') != 'ak820-beta-release-catalog-1':
        raise ValueError('Source catalog is not the published beta.4 format')
    if descriptor.get('assets') != file_records({name: data for name, data in payload.items()
                                                  if name not in ('release-catalog.json',
                                                                  'release-manifest.json')}):
        raise ValueError('Source release catalog file identities do not match the archive')
    if (manifest.get('tag') != SOURCE_TAG
            or manifest.get('files') != file_records({name: data for name, data in payload.items()
                                                        if name != 'release-manifest.json'})):
        raise ValueError('Source release manifest does not match the archive')
    if (descriptor.get('flashing_authorized') is not False
            or descriptor.get('settings_writes_authorized') is not False
            or descriptor.get('hardware_validated') is not False
            or descriptor.get('release_approved', False) is True
            or capabilities.get('release_approved') is not False
            or capabilities.get('flashing_authorized') is not False
            or capabilities.get('settings_writes_authorized') is not False
            or capabilities.get('hardware_validated') is not False):
        raise ValueError('Source beta.4 catalog is not the expected read-only release')
    rows = matrix.get('profiles')
    if not isinstance(rows, list) or [row.get('profile') for row in rows] != list(PROFILES):
        raise ValueError('Firmware matrix is not the exact ordered ten-profile set')
    profile_identities = []
    for row in rows:
        profile = row['profile']
        identity = row.get('settings_identity')
        if not isinstance(identity, dict):
            raise ValueError('Missing exact image identity: ' + profile)
        ihx = payload.get(f'profiles/{profile}/firmware/application.ihx')
        if ihx is None or sha(ihx) != identity.get('ihx_sha256'):
            raise ValueError('IHX does not match matrix identity: ' + profile)
        for key in ('ihx_sha256', 'code_sha256'):
            if not isinstance(identity.get(key), str) or not re.fullmatch(r'[0-9a-f]{64}', identity[key]):
                raise ValueError('Invalid exact image digest: ' + profile + '/' + key)
        profile_identities.append({'profile': profile,
                                   'ihx_sha256': identity['ihx_sha256'],
                                   'code_sha256': identity['code_sha256']})
    if descriptor.get('installable_profiles') != list(PROFILES):
        raise ValueError('Release catalog profile set differs from the matrix')
    images = capabilities.get('images')
    if not isinstance(images, list) or [image.get('profile') for image in images] != list(PROFILES):
        raise ValueError('Capability catalog profile set differs from the matrix')
    if any(image.get('flashing_authorized') is not False
           or image.get('settings_writes_authorized') is not False
           or image.get('hardware_validated') is not False for image in images):
        raise ValueError('Source beta.4 image capabilities are not read-only')

    capabilities['release_approved'] = True
    capabilities['flashing_authorized'] = True
    capabilities['hardware_validated'] = False
    capabilities['settings_writes_authorized'] = False
    capabilities['status'] = 'beta-catalog; installation requires fresh in-app confirmation'
    for image in images:
        image['release_approved'] = True
        image['flashing_authorized'] = True
        image['hardware_validated'] = False
        image['settings_writes_authorized'] = False
    payload['capability-catalog.json'] = canonical(capabilities)

    descriptor.update({
        'tag': TARGET_TAG,
        'release_approved': True,
        'flashing_authorized': True,
        'flashing_authorized_images': profile_identities,
        'hardware_validated': False,
        'settings_writes_authorized': False,
    })
    descriptor['assets'] = file_records({name: data for name, data in payload.items()
                                         if name not in ('release-catalog.json',
                                                         'release-manifest.json')})
    payload['release-catalog.json'] = canonical(descriptor)

    manifest['tag'] = TARGET_TAG
    manifest['files'] = file_records({name: data for name, data in payload.items()
                                      if name != 'release-manifest.json'})
    payload['release-manifest.json'] = canonical(manifest)

    for name in ('release-catalog.json', 'capability-catalog.json',
                 'release-manifest.json'):
        if (directory / name).is_symlink():
            raise ValueError('Refusing symlinked catalog metadata: ' + name)
        (directory / name).write_bytes(payload[name])
    with tempfile.NamedTemporaryFile(dir=directory, prefix='.beta41-', suffix='.zip',
                                     delete=False) as staged:
        staged_path = Path(staged.name)
    try:
        with zipfile.ZipFile(staged_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as output:
            for name in sorted(payload):
                info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                output.writestr(info, payload[name])
        staged_path.replace(archive_path)
    finally:
        staged_path.unlink(missing_ok=True)
    return sha(archive_path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog-dir', required=True, type=Path)
    parser.add_argument('--tag', required=True)
    args = parser.parse_args()
    print(json.dumps({'tag': args.tag, 'archive_sha256': promote(args.catalog_dir, args.tag)},
                     sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
