#!/usr/bin/env python3
"""Wrap already verified release assets and reports; never builds or flashes."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import zipfile


BASE = 'b35b77cddbefdb509058f1fbaaeafaa3982ce172'
PROFILES = 'main game mmo typing code pointer onehand creative shortcuts multios'.split()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('root', 'assets', 'assembled', 'bundle', 'bundle-verification', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--source-commit', required=True)
    args = p.parse_args()
    root = args.root.resolve(strict=True)
    audit = root / 'audits/beta3-direct-20261026'
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
    subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', args.source_commit, head], check=True)
    if subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain']):
        raise ValueError('Deliver only from a clean committed tree')
    receipt = json.loads(args.bundle_verification.read_bytes())
    bundle = args.bundle.read_bytes()
    if (receipt.get('status') != 'PASS' or receipt.get('base') != BASE or
            receipt.get('head') != head or receipt.get('bundle_sha256') != sha(bundle)):
        raise ValueError('Bundle verification does not bind the final tree and bytes')
    package_result = json.loads((audit / 'final-package-verification.json').read_bytes())
    if package_result.get('status') != 'PASS':
        raise ValueError('Platform verification is not complete')
    package_names = set()
    for item in package_result['packages']:
        package_names.add(item['file'])
        if (sha((args.assets / item['file']).read_bytes()) != item['sha256'] or
                sha((args.assets / (item['file'] + '.sha256')).read_bytes()) != item['checksum_file_sha256']):
            raise ValueError('Verified platform archive/checksum changed')
    with zipfile.ZipFile(args.assets / 'AK820-Beta3-Catalog.zip') as catalog:
        catalog_payload = {name: catalog.read(name) for name in catalog.namelist()}
    expected_assets = set(catalog_payload) | package_names | {name + '.sha256' for name in package_names} | {'SHA256SUMS'}
    actual_assets = {p.relative_to(args.assets).as_posix() for p in args.assets.rglob('*') if p.is_file()}
    if actual_assets != expected_assets:
        raise ValueError('Verified release asset inventory changed')
    for name, data in catalog_payload.items():
        if (args.assets / name).read_bytes() != data:
            raise ValueError('Uncompressed catalog payload changed: ' + name)
    sums = {}
    for line in (args.assets / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if name in sums or name not in set(catalog_payload) | package_names:
            raise ValueError('Invalid release checksum inventory')
        sums[name] = digest
        if sha((args.assets / name).read_bytes()) != digest:
            raise ValueError('Release checksum mismatch: ' + name)
    if set(sums) != set(catalog_payload) | package_names:
        raise ValueError('Incomplete release checksums')
    assembly = json.loads((audit / 'assembly-run.json').read_bytes())
    firmware_archive = args.assembled / 'firmware-bundle.zip'
    firmware_digest = sha(firmware_archive.read_bytes())
    if (assembly.get('status') != 'passed' or assembly.get('source_commit') != args.source_commit or
            assembly.get('archive_sha256') != firmware_digest):
        raise ValueError('Verified firmware bundle changed')
    if (args.assembled / 'firmware-bundle.zip.sha256').read_bytes() != (
            firmware_digest + '  firmware-bundle.zip\n').encode('ascii'):
        raise ValueError('Firmware checksum file does not match the verified archive')
    payload = {}

    def add(name, source):
        source = Path(source)
        if source.is_symlink() or not stat.S_ISREG(source.stat().st_mode):
            raise ValueError('Expected a regular public file: ' + str(source))
        if name in payload or name.startswith('/') or '..' in Path(name).parts:
            raise ValueError('Invalid or duplicate delivery name: ' + name)
        payload[name] = source.read_bytes()

    for source in sorted(args.assets.rglob('*')):
        if source.is_symlink():
            raise ValueError('Symlink in verified assets')
        if source.is_file():
            add('release/' + source.relative_to(args.assets).as_posix(), source)
    for name in ('firmware-bundle.zip', 'firmware-bundle.zip.sha256'):
        add('firmware/' + name, args.assembled / name)
    for name in ('final-generated-admission-review.md', 'delivery-verification-review.md',
                 'final-package-verification.json', 'assembly-run.json',
                 'module-catalog-refresh.json', 'module-catalog-review.md'):
        add('verification/' + name, audit / name)
    add('verification/bundle-verification.json', args.bundle_verification)
    qualified = json.loads((audit / 'final-qualification.json').read_bytes())
    if not qualified['passed'] or [row['profile'] for row in qualified['profiles']] != PROFILES:
        raise ValueError('Final qualification is incomplete')
    summary = {'format': 'ak820-beta3-delivery-resources-1', 'hardware_validated': False,
               'physical_device_commands': 0,
               'profiles': [{key: row[key] for key in ('profile', 'identity', 'resources',
                            'base_suites', 'unit_tests', 'runtime_passed')}
                            for row in qualified['profiles']]}
    payload['verification/resources.json'] = canonical(summary)
    payload['README.txt'] = f'''AK820 v0.6.0-beta.3

Все десять подготовленных профилей сохранены без изменения состава.
Direct v1: main, game, mmo, creative. Пульсация W: game и mmo.

Пакеты Python для установки находятся в release/:
  AK820-Windows.zip
  AK820-Linux-x86_64.tar.gz
Рядом находятся их SHA256-файлы и инструкции INSTALL-ru.md / INSTALL-en.md.
Полные инструкции и нужные скрипты также включены внутрь каждого пакета.
Отдельный GUI-установщик и его среда исполнения в выпуск не включены.

release/AK820-Beta3-Catalog.zip содержит каталог и десять одобренных наборов.
firmware/firmware-bundle.zip — комплект образов и точных манифестов.
verification/ содержит результаты проверки готовых файлов.
Полные исходники и машинные доказательства сохранены в Git bundle,
который предоставляется рядом с этим архивом: {args.bundle.name}

Исходный коммит одобренных образов прошивки и файлов Python: {args.source_commit}
Итоговая вершина Git с каталогом выпуска и отчётами: {head}
База инкрементального bundle: {BASE}

В существующем репозитории с этой базой:
  git bundle verify /path/to/{args.bundle.name}
  git fetch /path/to/{args.bundle.name} codex/beta3-direct-w
  git switch -c beta3-ready FETCH_HEAD

Сборка и проверки выполнены офлайн. Проверка на устройстве не заявляется.
Публикация в GitHub и прошивка устройства в этой работе не выполнялись.

English
All ten prepared profile compositions are unchanged. Use the matching Python
package and its checksum in release/, then follow the included English or
Russian installation guide. No standalone GUI installer/runtime is included.
The companion application is separate. Verification is offline; no hardware
validation, GitHub publication or device flashing is claimed.
Firmware images and Python host files were approved from source commit
{args.source_commit}. The final Git HEAD {head} contains the release catalog
and reports, including a metadata-only catalog correction; firmware and Python
host files are unchanged by that correction.
'''.encode('utf-8')
    manifest = {'format': 'ak820-beta3-delivery-manifest-1', 'tag': 'v0.6.0-beta.3',
                'git': {'base': BASE, 'source_commit': args.source_commit,
                        'source_scope': 'Approved firmware images and Python host files; excludes the later metadata-only web/module-descriptions.json catalog correction.',
                        'head': head,
                        'bundle': args.bundle.name, 'bundle_sha256': sha(bundle),
                        'bundle_size': len(bundle), 'branch': 'codex/beta3-direct-w'},
                'hardware_validated': False, 'physical_device_commands': 0,
                'files': {name: {'size': len(data), 'sha256': sha(data)}
                          for name, data in sorted(payload.items())}}
    payload['DELIVERY-MANIFEST.json'] = canonical(manifest)
    output = args.output.absolute()
    record_path = output.with_suffix('.delivery-record.json')
    if any(path.exists() or path.is_symlink() for path in (output, record_path)):
        raise ValueError('Delivery output and record must be fresh')
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(payload):
            raise ValueError('Delivery archive integrity failed')
        for name, data in payload.items():
            if archive.read(name) != data:
                raise ValueError('Delivery archive changed bytes: ' + name)
    result = {'status': 'PASS', 'file': str(output), 'size': output.stat().st_size,
              'sha256': sha(output.read_bytes()), 'members': len(payload),
              'source_commit': args.source_commit, 'head': head}
    with record_path.open('xb') as stream:
        stream.write(canonical(result))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
