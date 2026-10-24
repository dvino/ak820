#!/usr/bin/env python3
"""Assemble the beta.1 catalog assets from pinned, reviewed local inputs."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(SOURCE / 'util'))
sys.path.insert(0, str(ROOT / 'tools' / 'installer'))
import ak820_ci_authorization as authorization
from ak820_release_manifest import validate_host_manifest, read_review_record
import settings_backup as settings

CANDIDATE_ZIP = ROOT / 'audits/rc6/beta-catalog-20261024/final/ak820-beta-catalog-20261024.zip'
CANDIDATE_SHA256 = '6f165df7685f72c30d80536868af5827719880b923d3cfc8e13a193f34cbbe7c'
WORK_IHX = '652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880'
WORK_CODE = 'a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10'
WORK_IDENTITY = ROOT / 'audits/rc6/beta1-release-20261025/work-packed-identity.json'
FORMAT = 'ak820-beta-release-catalog-1'

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode() + b'\n'

def _safe_name(name: str) -> str:
    parts = name.split('/') if isinstance(name, str) else []
    if (not name or name.startswith('/') or '\\' in name or
            any(part in ('', '.', '..') for part in parts) or '/'.join(parts) != name):
        raise ValueError('Unsafe archive path: ' + repr(name))
    return name

def _checked_file(base: Path, name: str) -> Path:
    """Resolve one relative file while rejecting symlinks at every component."""
    _safe_name(name)
    base = Path(base).resolve(strict=True)
    path = base
    for part in name.split('/'):
        path = path / part
        if path.is_symlink():
            raise ValueError('Symlink in protected path: ' + name)
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(base) or not resolved.is_file():
        raise ValueError('Protected path escapes its root or is not a file: ' + name)
    return resolved

def _checked_bundle(bundle: Path) -> Path:
    """Require the bundle itself and its ancestors to be ordinary directories."""
    candidate = Path(bundle).absolute()
    try:
        relative = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError('Bundle must remain inside the repository root') from exc
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlink in bundle path: ' + str(current))
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(ROOT.resolve()) or not resolved.is_dir():
        raise ValueError('Bundle escapes the repository root or is not a directory')
    return resolved

def validate_bundle(bundle: Path) -> dict:
    """Check manifest, review, CI authorization and the pinned work image."""
    bundle = _checked_bundle(bundle)
    manifest_path = _checked_file(bundle, 'installer-release.json')
    if not manifest_path.is_file():
        raise ValueError('Bundle has no manifest.json')
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    files = manifest.get('files')
    if not isinstance(files, dict) or not files:
        raise ValueError('Bundle manifest has no files')
    for name, item in files.items():
        try:
            path = _checked_file(bundle, name)
        except (ValueError, FileNotFoundError) as exc:
            raise ValueError('Missing or unsafe bundle file: ' + name) from exc
        data = path.read_bytes()
        if item.get('size') != len(data) or item.get('sha256') != sha(data):
            raise ValueError('Bundle file hash/size mismatch: ' + name)
    ihx = files.get('firmware/application.ihx', {}).get('sha256')
    if ihx != WORK_IHX:
        raise ValueError('Bundle is not the pinned beta.1 work image')
    validate_work_identity()
    validate_host_manifest(manifest, ROOT)
    try:
        review_path = _checked_file(bundle, 'reviews/independent-review.md')
    except (ValueError, FileNotFoundError) as exc:
        raise ValueError('Bundle has no independent review') from exc
    record = read_review_record(review_path.read_text(encoding='utf-8'))
    if record.get('format') != 'ak820-reproduced-review-1':
        raise ValueError('Beta promotion requires CI reproduced-review authorization')
    if record.get('host_files') != manifest.get('host_files') or record.get('build') != {
            'ihx_sha256': ihx,
            'map_sha256': files.get('firmware/application.map', {}).get('sha256'),
            'build_report_sha256': files.get('reports/build-report.json', {}).get('sha256')}:
        raise ValueError('Independent review does not bind this bundle')
    try:
        policy_path = _checked_file(bundle, 'reviews/program-policy.json')
        current_policy_path = _checked_file(ROOT, 'ci/release-policy.json')
        safety_path = _checked_file(ROOT, 'ci/release-safety.json')
    except (ValueError, FileNotFoundError) as exc:
        raise ValueError('Required CI policy or safety evidence is missing or unsafe') from exc
    if policy_path.read_bytes() != current_policy_path.read_bytes():
        raise ValueError('CI program policy differs from current reviewed policy')
    policy = json.loads(policy_path.read_bytes())
    safety = json.loads(safety_path.read_text(encoding='utf-8'))
    if safety.get('program', {}).get('ihx_sha256') != WORK_IHX:
        raise ValueError('Current release-safety evidence does not bind the work image')
    for name, item in safety.get('source_files', {}).items():
        _safe_name(name)
        try:
            path = _checked_file(ROOT, name)
        except (ValueError, FileNotFoundError) as exc:
            raise ValueError('Current release-safety source pin differs: ' + name) from exc
        if {'sha256': sha(path.read_bytes()), 'size': path.stat().st_size} != item:
            raise ValueError('Current release-safety source pin differs: ' + name)
    for witness in safety.get('witnesses', {}).values():
        name = witness.get('path')
        _safe_name(name)
        try:
            path = _checked_file(ROOT, name)
        except (ValueError, FileNotFoundError) as exc:
            raise ValueError('Current release-safety witness pin differs: ' + str(name)) from exc
        if sha(path.read_bytes()) != witness.get('sha256'):
            raise ValueError('Current release-safety witness pin differs: ' + str(name))
    if not isinstance(policy.get('source_files'), dict):
        raise ValueError('CI policy has no source pins')
    for name, item in policy['source_files'].items():
        _safe_name(name)
        try:
            path = _checked_file(ROOT, name)
        except (ValueError, FileNotFoundError) as exc:
            raise ValueError('Current CI policy source pin differs: ' + name) from exc
        if {'sha256': sha(path.read_bytes()), 'size': path.stat().st_size} != item:
            raise ValueError('Current CI policy source pin differs: ' + name)
    authorization.validate_bundle_authorization(bundle, manifest, record)
    return manifest

def validate_work_identity() -> dict:
    identity = json.loads(WORK_IDENTITY.read_text(encoding='utf-8'))
    if identity.get('ihx_sha256') != WORK_IHX or identity.get('code_sha256') != WORK_CODE:
        raise ValueError('Pinned packed CODE identity does not match the approved work record')
    return identity

def validate_profile_links(payload: dict[str, bytes]) -> None:
    matrix = json.loads(payload['firmware-matrix.json'])
    if len(matrix.get('profiles', [])) != 9:
        raise ValueError('Frozen catalog must contain nine profiles')
    work = next((row for row in matrix['profiles'] if row['profile'] == 'work'), None)
    if work is None or work['identity']['ihx_sha256'] != WORK_IHX:
        raise ValueError('Frozen catalog has no exact work image')
    for row in matrix['profiles']:
        for suffix in ('ihx', 'map', 'mem'):
            path = 'profiles/' + row['profile'] + '/firmware/application.' + suffix
            if sha(payload[path]) != row['identity'][suffix + '_sha256']:
                raise ValueError('Catalog profile firmware does not match matrix: ' + row['profile'] + '.' + suffix)

def _catalog_payload() -> dict[str, bytes]:
    if not CANDIDATE_ZIP.is_file() or sha(CANDIDATE_ZIP.read_bytes()) != CANDIDATE_SHA256:
        raise ValueError('Frozen candidate archive hash mismatch')
    with zipfile.ZipFile(CANDIDATE_ZIP) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate candidate archive member')
        for name in names: _safe_name(name)
        manifest = json.loads(zf.read('candidate-manifest.json'))
        expected = manifest.get('files', {})
        payload = {name: zf.read(name) for name in names if name != 'candidate-manifest.json'}
        if set(expected) != set(payload):
            raise ValueError('Candidate archive members differ from frozen manifest')
        for name, data in payload.items():
            item = expected[name]
            if item.get('sha256') != sha(data) or item.get('size') != len(data):
                raise ValueError('Candidate member integrity mismatch: ' + name)
    for name in ('firmware-matrix.json', 'module-descriptions.json'):
        if payload[name] != (ROOT / 'web' / name).read_bytes():
            raise ValueError('Candidate archive differs from current web catalog: ' + name)
    validate_profile_links(payload)
    return payload

def build(bundle: Path, output: Path, tag: str) -> dict:
    if not re.fullmatch(r'v?\d+\.\d+\.\d+-beta\.\d+', tag):
        raise ValueError('Tag must be a beta version such as v0.6.0-beta.1')
    validate_bundle(bundle)
    validate_work_identity()
    payload = _catalog_payload()
    matrix = json.loads(payload['firmware-matrix.json'])
    row = next(item for item in matrix['profiles'] if item['profile'] == 'work')
    for candidate in matrix['profiles']:
        candidate['release_approved'] = False
        candidate['installable'] = False
    definition = json.loads(payload['profiles/work/reference/vial.json'])
    row['settings_identity'] = settings.catalog_settings_identity(
        row['configuration'], WORK_IHX, WORK_CODE, sha(settings.canonical(definition)))
    row['settings_status'] = 'reviewed-exact-packed-code'
    row['release_approved'] = True
    row['installable'] = True
    payload['firmware-matrix.json'] = canonical(matrix)
    caps = json.loads((ROOT / 'web/capability-catalog.json').read_text(encoding='utf-8'))
    caps['release_approved'] = False
    caps['hardware_validated'] = False
    caps['flashing_authorized'] = False
    caps['settings_writes_authorized'] = False
    caps['status'] = 'beta-catalog; physical operations require fresh consent'
    for image in caps.get('images', []):
        image['release_approved'] = image.get('profile') == 'work'
        image['flashing_authorized'] = False
        image['settings_writes_authorized'] = False
        image['hardware_validated'] = False
    payload['capability-catalog.json'] = canonical(caps)
    for lang, source in (('en', ROOT / 'docs/INSTALL.md'), ('ru', ROOT / 'docs/ru/INSTALL.md')):
        text = source.read_text(encoding='utf-8')
        text = text.replace('ak820-beta-catalog-20261024.zip', 'AK820-Beta1-Catalog.zip')
        text = text.replace('ak820-beta-catalog-20261024.zip.sha256', 'AK820-Beta1-Catalog.zip.sha256')
        payload['INSTALL-' + lang + '.md'] = text.encode('utf-8')
    files = {name: {'sha256': sha(data), 'size': len(data)} for name, data in sorted(payload.items())}
    descriptor = {'format': FORMAT, 'tag': tag, 'status': 'beta', 'default_profile': 'work',
                  'installable_profiles': ['work'], 'catalog_profiles': [r['profile'] for r in matrix['profiles']],
                  'hardware_validated': False, 'flashing_authorized': False,
                  'settings_writes_authorized': False, 'assets': files}
    payload['release-catalog.json'] = canonical(descriptor)
    manifest = {'format': 'ak820-beta-release-manifest-1', 'tag': tag, 'files': {
        name: {'sha256': sha(data), 'size': len(data)} for name, data in sorted(payload.items())}}
    payload['release-manifest.json'] = canonical(manifest)
    output = Path(output).absolute()
    if output.exists() or output.is_symlink(): raise ValueError('Output must be a new directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.' + output.name + '.stage-', dir=output.parent) as tmp:
        stage = Path(tmp) / 'assets'; stage.mkdir()
        for name, data in payload.items():
            dest = stage / _safe_name(name); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
        archive = stage / 'AK820-Beta1-Catalog.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for name in sorted(payload):
                info = zipfile.ZipInfo(name, (1980,1,1,0,0,0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
                zf.writestr(info, payload[name])
        digest = sha(archive.read_bytes())
        (stage / 'AK820-Beta1-Catalog.zip.sha256').write_text(digest + '  AK820-Beta1-Catalog.zip\n')
        (stage / 'SHA256SUMS').write_text(''.join(sha((stage / n).read_bytes()) + '  ' + n + '\n' for n in sorted(payload)) + digest + '  AK820-Beta1-Catalog.zip\n')
        stage.rename(output)
    return {'output': str(output), 'tag': tag, 'profiles': 9, 'installable_profiles': ['work'], 'zip_sha256': digest}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--tag', required=True)
    args = parser.parse_args(argv)
    print(json.dumps(build(args.bundle, args.output, args.tag), sort_keys=True))
    return 0

if __name__ == '__main__': raise SystemExit(main())
