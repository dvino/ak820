#!/usr/bin/env python3
"""Verify downloaded AK820 alpha3 release assets without accessing USB."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
SOURCE_COMMIT = 'b17d7c8b52ec7a234a742a64380e22354698030b'
IHX_SHA256 = 'd505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18'
POLICY_SHA256 = '32092b9468e7474d77720e5989bbe8cf5b087f6a817cdc19719c5d278c7655ef'
SAFETY_MANIFEST_SHA256 = 'fe6c25880d51e19274e153dc2fda681ec26e9ae1ccd09f71fb93133032d6cd6a'
ASSETS = ('firmware-bundle.zip', 'AK820-Windows.zip', 'AK820-Linux-x86_64.tar.gz')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    if p.is_absolute() or not p.parts or any(part in ('', '.', '..') for part in p.parts) or '\\' in name or '\x00' in name or ':' in name:
        raise ValueError(f'Unsafe archive member name: {name!r}')
    return p


def find_asset(root: Path, name: str) -> Path:
    found = [p for p in root.rglob(name) if p.is_file() and p.name == name]
    if len(found) != 1:
        raise ValueError(f'Expected exactly one {name} below assets directory; found {len(found)}')
    checksum = found[0].with_name(name + '.sha256')
    if not checksum.is_file():
        raise ValueError(f'Missing checksum file beside {found[0]}')
    line = checksum.read_text(encoding='ascii').strip()
    match = re.fullmatch(r'([0-9a-f]{64})  ' + re.escape(name), line)
    if not match:
        raise ValueError(f'Unexpected checksum line in {checksum}')
    actual = digest(found[0].read_bytes())
    if actual != match.group(1):
        raise ValueError(f'Checksum mismatch: {found[0]}')
    return found[0]


def extract_zip(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        seen = set()
        for info in zf.infolist():
            rel = safe_name(info.filename.rstrip('/')) if info.filename.rstrip('/') else None
            if rel is None:
                continue
            if rel in seen:
                raise ValueError(f'Duplicate ZIP member: {info.filename}')
            seen.add(rel)
            mode = info.external_attr >> 16
            if mode and (mode & 0o170000) == 0o120000:
                raise ValueError(f'ZIP symlink is not permitted: {info.filename}')
        for info in zf.infolist():
            if not info.filename.rstrip('/'):
                continue
            target = destination.joinpath(*safe_name(info.filename.rstrip('/')).parts)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(info))


def validate_tar(tar: tarfile.TarFile) -> list[tarfile.TarInfo]:
    members = tar.getmembers()
    names: dict[PurePosixPath, tarfile.TarInfo] = {}
    for member in members:
        rel = safe_name(member.name.rstrip('/'))
        if rel in names:
            raise ValueError(f'Duplicate TAR member: {member.name}')
        names[rel] = member
        if not (member.isfile() or member.isdir() or member.issym()):
            raise ValueError(f'Unsupported TAR member type: {member.name}')
    for name in names:
        if any(parent in names and names[parent].issym() for parent in name.parents):
            raise ValueError(f'TAR member has a symlink parent: {name}')
    # Resolve relative symlinks lexically from their containing directory.
    for member in members:
        if not member.issym():
            continue
        if PurePosixPath(member.linkname).is_absolute() or '\\' in member.linkname:
            raise ValueError(f'Absolute or malformed Linux package symlink: {member.name}')
        stack = list(safe_name(member.name).parts[:-1])
        for part in member.linkname.split('/'):
            if part in ('', '.'):
                continue
            if part == '..':
                if not stack:
                    raise ValueError(f'Linux package symlink escapes archive: {member.name}')
                stack.pop()
            else:
                stack.append(part)
        resolved = PurePosixPath(*stack)
        seen_links = {safe_name(member.name)}
        while resolved in names and names[resolved].issym():
            if resolved in seen_links:
                raise ValueError(f'Linux package symlink cycle: {member.name}')
            seen_links.add(resolved)
            linked = names[resolved]
            if PurePosixPath(linked.linkname).is_absolute() or '\\' in linked.linkname:
                raise ValueError(f'Unsafe chained Linux package symlink: {linked.name}')
            parts = list(resolved.parts[:-1])
            for part in linked.linkname.split('/'):
                if part in ('', '.'):
                    continue
                if part == '..':
                    if not parts:
                        raise ValueError(f'Linux package symlink escapes archive: {linked.name}')
                    parts.pop()
                else:
                    parts.append(part)
            resolved = PurePosixPath(*parts)
        if resolved not in names and not any(other.is_relative_to(resolved) for other in names):
            raise ValueError(f'Linux package symlink target is absent: {member.name}')
    return members


def extract_tar(archive: Path, destination: Path) -> None:
    with tarfile.open(archive, 'r:gz') as tf:
        members = validate_tar(tf)
        for member in members:
            target = destination.joinpath(*safe_name(member.name.rstrip('/')).parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                source = tf.extractfile(member)
                if source is None:
                    raise ValueError(f'Cannot read TAR member: {member.name}')
                with source, target.open('xb') as out:
                    shutil.copyfileobj(source, out)
                target.chmod(member.mode & 0o777)
        # Create links only after regular files have been materialized.
        for member in members:
            if member.issym():
                target = destination.joinpath(*safe_name(member.name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(member.linkname, target)
        # Lexical normalization alone is insufficient: intermediate symlinks
        # must be resolved before interpreting a following '..' component.
        for member in members:
            if member.issym():
                target = destination.joinpath(*safe_name(member.name).parts)
                try:
                    resolved = target.resolve(strict=True)
                except (OSError, RuntimeError) as error:
                    raise ValueError(f'Unresolved Linux package symlink: {member.name}') from error
                if not resolved.is_relative_to(destination.resolve()):
                    raise ValueError(f'Linux package symlink escapes extracted root: {member.name}')


def json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def official_bundle_check(bundle: Path) -> None:
    spec = importlib.util.spec_from_file_location('asset_installer_validation', ROOT / 'tools/installer/ak820.py')
    installer = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = installer
    spec.loader.exec_module(installer)
    installer.BUNDLE = bundle
    installer.APPROVAL = bundle / 'approved-release.json'
    installer.load_release(approved=True)


def check_package(apps_root: Path, package_root: Path, manifest: dict, approved: bytes,
                  bundle: Path, host_files: dict, platform: str) -> dict:
    report = json_file(package_root / 'build-provenance.json')
    expected_format = 'ak820-windows-package-v1' if platform == 'windows' else 'ak820-linux-package-v1'
    if report.get('format') != expected_format:
        raise ValueError('Unsupported package report')
    required_checks = {'cli_help', 'offline_verify', 'native_tk_ui_smoke'} if platform == 'windows' else {
        'cli_help', 'offline_verify', 'native_tk_ui_smoke_xvfb', 'frozen_hidraw_import'}
    if any(report.get('checks', {}).get(key) != 'passed' for key in required_checks):
        raise ValueError('Package report has missing or failed smoke checks')
    collected = report.get('collected_inputs', {})
    if set(collected) != {'AK820', 'AK820-cli'}:
        raise ValueError('Report lacks GUI and CLI collected inputs')
    expected_names = (set(host_files) | {'releases/rc6/' + name for name in manifest['files']} | {
        'releases/rc6/installer-release.json', 'tools/installer/approved-release.json'})
    if set(report.get('approved_inputs', {})) != expected_names:
        raise ValueError('Approved input list differs from release manifest')
    for app in ('AK820', 'AK820-cli'):
        internal = apps_root / app / '_internal'
        if set(collected[app]) != expected_names:
            raise ValueError('Collected input list differs for ' + app)
        for name, expected_hash in collected[app].items():
            packaged = internal.joinpath(*safe_name(name).parts)
            if digest(packaged.read_bytes()) != expected_hash or expected_hash != report['approved_inputs'][name]:
                raise ValueError('Collected input mismatch: ' + app + '/' + name)
            if name == 'tools/installer/approved-release.json':
                expected = approved
            elif name.startswith('releases/rc6/'):
                expected = bundle.joinpath(*safe_name(name[len('releases/rc6/'):]).parts).read_bytes()
            elif name in host_files:
                expected = ROOT.joinpath(*safe_name(name).parts).read_bytes()
            else:
                raise ValueError('Unexpected collected input: ' + name)
            if packaged.read_bytes() != expected:
                raise ValueError('Packaged input differs from reviewed bundle/source: ' + name)
        executable = apps_root / app / (app + '.exe' if platform == 'windows' else app)
        recorded = (report['apps']['gui_exe_sha256' if app == 'AK820' else 'cli_exe_sha256']
                    if platform == 'windows' else report['apps'][app]['sha256'])
        if digest(executable.read_bytes()) != recorded:
            raise ValueError('Executable differs from native provenance report: ' + app)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets-dir', type=Path, required=True)
    parser.add_argument('--source-commit', default=SOURCE_COMMIT)
    parser.add_argument('--ihx', default=IHX_SHA256)
    parser.add_argument('--manifest-sha256', help='optional pin for the freshly generated installer manifest')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True, help='new, empty extraction directory')
    parser.add_argument('--smoke-linux', action='store_true', help='run only Linux CLI --help and offline verify')
    args = parser.parse_args()
    assets_dir = args.assets_dir.resolve()
    work = args.work.resolve()
    if work.exists() and any(work.iterdir()):
        parser.error('--work must be a fresh empty directory')
    work.mkdir(parents=True, exist_ok=True)
    assets = {name: find_asset(assets_dir, name) for name in ASSETS}
    extracted = work / 'extracted'
    for name, path in assets.items():
        dest = extracted / name.removesuffix('.zip').removesuffix('.tar.gz')
        dest.mkdir(parents=True)
        if name.endswith('.zip'):
            extract_zip(path, dest)
        else:
            extract_tar(path, dest)
    firmware_root = extracted / 'firmware-bundle'
    candidates = list(firmware_root.rglob('installer-release.json'))
    if len(candidates) != 1:
        raise ValueError('Firmware ZIP must contain exactly one installer-release.json')
    bundle = candidates[0].parent
    manifest_bytes = (bundle / 'installer-release.json').read_bytes()
    manifest_sha256 = digest(manifest_bytes)
    if args.manifest_sha256 and manifest_sha256 != args.manifest_sha256:
        raise ValueError('Fresh firmware release manifest differs from requested SHA256 pin')
    manifest = json.loads(manifest_bytes)
    if manifest.get('format') != 'ak820-installer-release-2' or not isinstance(manifest.get('files'), dict):
        raise ValueError('Unsupported release manifest')
    approved = (bundle / 'approved-release.json').read_bytes()
    approval = json.loads(approved)
    if approval.get('format') != 'ak820-installer-approval-1' or approval.get('release') != 'rc6':
        raise ValueError('Unsupported release approval record')
    if approval.get('manifest_sha256') != manifest_sha256:
        raise ValueError('Firmware bundle approval does not bind its exact installer manifest')
    host_files = manifest.get('host_files', {})
    policy = json_file(ROOT / 'ci/release-policy.json')
    if policy.get('host_files') != host_files:
        raise ValueError('Release manifest host files differ from the checked-in release policy')
    for name, record in host_files.items():
        source = ROOT.joinpath(*safe_name(name).parts)
        if not source.is_file() or {'size': source.stat().st_size, 'sha256': digest(source.read_bytes())} != record:
            raise ValueError(f'Current host source differs from release manifest: {name}')
    attestation = json_file(bundle / 'reports/build-attestation.json')
    if attestation.get('source_commit') != args.source_commit:
        raise ValueError('Firmware source commit differs from expected commit')
    # Documentation/evidence commits may follow a release. Anchor the expected
    # program policy to the actual release commit, rather than requiring HEAD
    # to stay at that commit forever. Host bytes are independently checked above.
    committed_policy = subprocess.run(
        ['git', '-C', str(ROOT), 'show', args.source_commit + ':ci/release-policy.json'],
        check=True, capture_output=True).stdout
    if digest(committed_policy) != POLICY_SHA256:
        raise ValueError('Expected source commit does not contain the reviewed policy')
    policy_path = ROOT / 'ci/release-policy.json'
    program_review_path = ROOT / 'ci/program-review.md'
    if digest(policy_path.read_bytes()) != POLICY_SHA256:
        raise ValueError('Current release policy differs from the reviewed policy SHA256')
    if digest((ROOT / 'ci/release-safety.json').read_bytes()) != SAFETY_MANIFEST_SHA256:
        raise ValueError('Current release-safety proof differs from its reviewed SHA256')
    if (bundle / 'reviews/program-policy.json').read_bytes() != policy_path.read_bytes():
        raise ValueError('Bundle program policy differs from the current checked-in policy')
    if (bundle / 'reviews/program-review.md').read_bytes() != program_review_path.read_bytes():
        raise ValueError('Bundle program review differs from the current checked-in review')
    if attestation.get('policy_sha256') != POLICY_SHA256:
        raise ValueError('Firmware attestation uses a different release policy')
    if attestation.get('program_review_sha256') != digest(program_review_path.read_bytes()):
        raise ValueError('Firmware attestation does not bind the current program review')
    ihx_candidates = [name for name in manifest['files'] if name.endswith('.ihx')]
    if len(ihx_candidates) != 1 or digest(bundle.joinpath(*safe_name(ihx_candidates[0]).parts).read_bytes()) != args.ihx:
        raise ValueError('Firmware IHX differs from expected image hash')
    for name, record in manifest['files'].items():
        rel = safe_name(name)
        path = bundle.joinpath(*rel.parts)
        if not path.is_file():
            raise ValueError(f'Manifest file missing from firmware bundle: {name}')
        if {'size': path.stat().st_size, 'sha256': digest(path.read_bytes())} != record:
            raise ValueError(f'Firmware bundle file differs from immutable manifest: {name}')
    official_bundle_check(bundle)
    winroot = extracted / 'AK820-Windows' / 'AK820-Windows'
    linuxroot = extracted / 'AK820-Linux-x86_64' / 'AK820-Linux-x86_64'
    windows_reports = check_package(winroot, winroot, manifest, approved, bundle, host_files, 'windows')
    linux_reports = check_package(linuxroot, linuxroot, manifest, approved, bundle, host_files, 'linux')
    for app in ('AK820', 'AK820-cli'):
        pe_path = winroot / app / (app + '.exe')
        with pe_path.open('rb') as stream:
            dos = stream.read(64)
            if len(dos) < 64 or dos[:2] != b'MZ':
                raise ValueError(f'Windows {app} executable is not a PE image')
            pe_offset = int.from_bytes(dos[0x3c:0x40], 'little')
            stream.seek(pe_offset)
            pe = stream.read(6)
        if pe[:4] != b'PE\0\0' or int.from_bytes(pe[4:6], 'little') != 0x8664:
            raise ValueError(f'Windows {app} executable is not AMD64')
        with (linuxroot / app / app).open('rb') as stream:
            elf = stream.read(20)
        if len(elf) < 20 or elf[:6] != b'\x7fELF\x02\x01' or int.from_bytes(elf[18:20], 'little') != 62:
            raise ValueError(f'Linux {app} executable is not ELF64 x86_64')
    for path in (ROOT / 'docs/INSTALL.md', ROOT / 'docs/ru/INSTALL.md'):
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f'Missing English or Russian installation instructions: {path}')
    if args.smoke_linux:
        cli = linuxroot / 'AK820-cli' / 'AK820-cli'
        subprocess.run([str(cli), '--help'], check=True, cwd=linuxroot)
        subprocess.run([str(cli), 'verify'], check=True, cwd=linuxroot)
    result = {'format': 'ak820-alpha3-assets-check-1', 'status': 'passed',
              'source_commit': args.source_commit, 'ihx_sha256': args.ihx,
              'checks': {'asset_sha256_files': 'passed', 'archive_paths_and_links': 'passed',
                         'firmware_attestation': 'passed', 'manifest_files': 'passed',
                         'official_bundle_validation': 'passed',
                         'windows_and_linux_collected_inputs': 'passed',
                         'native_architecture': 'passed', 'installation_instructions': 'passed'},
              'assets': {name: {'path': str(path), 'sha256': digest(path.read_bytes())} for name, path in assets.items()},
              'installer_manifest_sha256': manifest_sha256,
              'release_safety_proof_sha256': SAFETY_MANIFEST_SHA256,
              'manifest_files': len(manifest['files']),
              'host_files': len(host_files),
              'packages': {'windows': {'apps': ['AK820', 'AK820-cli'], 'architecture': 'PE AMD64'},
                           'linux': {'apps': ['AK820', 'AK820-cli'], 'architecture': 'ELF64 x86_64'}},
              'linux_cli_smoke': 'passed' if args.smoke_linux else 'skipped',
              'install_instructions': ['docs/INSTALL.md', 'docs/ru/INSTALL.md'],
              'device_access': 'none'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, tarfile.TarError) as error:
        raise SystemExit(f'asset check failed: {error}')
