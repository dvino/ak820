#!/usr/bin/env python3
"""Assemble beta catalog assets from exact, independently approved bundles."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import io
import json
import re
import shutil
import sys
import tempfile
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(SOURCE / 'util'))
sys.path.insert(0, str(ROOT / 'tools' / 'installer'))
import ak820_ci_authorization as authorization
from ak820_release_manifest import validate_host_manifest, read_review_record
import settings_backup as settings
import ak820
import ak820_profiles
import configure_firmware
import pack_ak820
from build_ci_release import PUBLIC_FILES as CI_PUBLIC_FILES
from build_windows_installer import guide_files
from ak820_release_manifest import HOST_FILES

CANDIDATE_ZIP = ROOT / 'audits/rc6/beta-catalog-20261024/final/ak820-beta-catalog-20261024.zip'
CANDIDATE_SHA256 = '6f165df7685f72c30d80536868af5827719880b923d3cfc8e13a193f34cbbe7c'
WORK_IHX = '652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880'
WORK_CODE = 'a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10'
WORK_IDENTITY = ROOT / 'audits/rc6/beta1-release-20261025/work-packed-identity.json'
FORMAT = 'ak820-beta-release-catalog-1'
RELEASE_PROFILES = ('main', 'game', 'mmo', 'typing', 'code', 'pointer',
                    'onehand', 'creative', 'shortcuts', 'multios')

PYTHON_PACKAGE_FILES = tuple(sorted(HOST_FILES | {
    'AK820.cmd', 'AK820.sh', 'tools/installer/ak820.py',
    'tools/installer/settings_backup.py', 'tools/installer/settings_workflow.py',
    'tools/installer/i18n.py', 'tools/installer/profile-catalog.json',
    'tools/installer/settings-catalog.json', 'tools/installer/requirements.txt',
    'tools/installer/70-ak820.rules',
}))

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode() + b'\n'

def standalone_guide(source: Path) -> bytes:
    """Keep relative guide links valid when the copy lives at archive root."""
    text = source.read_text(encoding='utf-8')
    base = source.parent.relative_to(ROOT)
    def replace(match):
        target = match.group(2)
        if target.startswith(('#', '/', 'http:', 'https:', 'mailto:')):
            return match.group(0)
        path, separator, fragment = target.partition('#')
        import posixpath
        rebased = posixpath.normpath(base.as_posix() + '/' + path)
        if rebased == '..' or rebased.startswith('../'):
            raise ValueError('Standalone guide link escapes the archive')
        return match.group(1) + rebased + (separator + fragment if separator else '') + ')'
    return re.sub(r'(\[[^\]\n]*\]\()([^\s)]+)\)', replace, text).encode('utf-8')


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

def python_package_files(contexts) -> dict[str, bytes]:
    """Collect Python source, launch scripts and approved profile inputs only."""
    files = {}
    for name in PYTHON_PACKAGE_FILES:
        path = _checked_file(ROOT, name)
        files[name] = path.read_bytes()
    for name in guide_files():
        path = _checked_file(ROOT, name)
        files[name] = path.read_bytes()
    for lang, source in (('en', ROOT / 'docs/INSTALL.md'), ('ru', ROOT / 'docs/ru/INSTALL.md')):
        files[f'INSTALL-{lang}.md'] = standalone_guide(source)
    for context in contexts:
        profile = context.profile
        bundle = _checked_bundle(context.bundle)
        manifest = json.loads((bundle / 'installer-release.json').read_bytes())
        for name in ('installer-release.json', *manifest['files'], 'approved-release.json'):
            path = _checked_file(bundle, name)
            data = path.read_bytes()
            if name in manifest['files']:
                item = manifest['files'][name]
                if len(data) != item['size'] or sha(data) != item['sha256']:
                    raise ValueError(f'Profile package input changed: {profile}/{name}')
            files[f'releases/beta3/{profile}/{name}'] = data
    return files

def write_python_packages(stage: Path, files: dict[str, bytes]) -> dict[str, str]:
    """Write deterministic source-only Windows ZIP and Linux tar.gz packages."""
    windows = stage / 'AK820-Windows.zip'
    with zipfile.ZipFile(windows, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('AK820-Python/' + _safe_name(name), (1980,1,1,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    linux = stage / 'AK820-Linux-x86_64.tar.gz'
    with linux.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode='w', format=tarfile.PAX_FORMAT) as archive:
                for name, data in sorted(files.items()):
                    info = tarfile.TarInfo('AK820-Python/' + _safe_name(name))
                    info.size = len(data)
                    info.mode = 0o755 if name == 'AK820.sh' else 0o644
                    info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))
    checksums = {}
    for name in (windows.name, linux.name):
        digest = sha((stage / name).read_bytes())
        (stage / (name + '.sha256')).write_text(f'{digest}  {name}\n', encoding='ascii')
        checksums[name] = digest
    return checksums

def _identity_from_bundle(context) -> tuple[dict, dict]:
    manifest = context.manifest
    files = manifest.get('files')
    if not isinstance(files, dict) or set(files) != set(CI_PUBLIC_FILES) - {'installer-release.json'}:
        raise ValueError('Approved profile bundle has an unexpected public dependency set: ' + context.profile)
    report_path = _checked_file(context.bundle, 'reports/build-report.json')
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    configuration = report.get('configuration')
    expected_configuration = ak820_profiles.configuration(context.profile)
    if configuration != expected_configuration:
        raise ValueError('Bundle build configuration differs from selected profile: ' + context.profile)
    sources = report.get('sources')
    if not isinstance(sources, list):
        raise ValueError('Build report lacks source identity: ' + context.profile)
    identity = {
        'profile': context.profile,
        'configuration_sha256': sha(configure_firmware.canonical(configuration)),
        'ihx_sha256': files['firmware/application.ihx']['sha256'],
        'map_sha256': files['firmware/application.map']['sha256'],
        'mem_sha256': files['firmware/application.mem']['sha256'],
        'build_report_sha256': files['reports/build-report.json']['sha256'],
        'source_manifest_sha256': sha(configure_firmware.canonical(sources)),
        'compiler_sha256': report.get('compiler_sha256'),
        'nvm_schema': configuration['nvm_schema'],
    }
    if (not identity['compiler_sha256'] or report.get('build_id') != identity['nvm_schema']
            or report.get('hardware_validated') is not False):
        raise ValueError('Build report does not identify an exact release image: ' + context.profile)
    return identity, configuration


def validate_profile_links(payload: dict[str, bytes], contexts,
                           settings_catalog: dict, capability_catalog: dict,
                           module_descriptions: dict | bytes | None = None) -> None:
    """Bind every published matrix/capability row to its exact approved bundle."""
    import firmware_matrix
    import build_capability_catalog as capability_builder
    names = tuple(context.profile for context in contexts)
    if names != RELEASE_PROFILES or len(set(names)) != len(RELEASE_PROFILES):
        raise ValueError('Approved contexts must be exactly the ten unique profiles in catalog order')
    matrix = json.loads(payload['firmware-matrix.json'])
    settings_catalog = settings_catalog if isinstance(settings_catalog, dict) else json.loads(settings_catalog)
    capability_catalog = capability_catalog if isinstance(capability_catalog, dict) else json.loads(capability_catalog)
    if module_descriptions is not None:
        validate_module_descriptions(module_descriptions)
    rows = matrix.get('profiles')
    settings_rows = settings_catalog.get('profiles')
    images = capability_catalog.get('images')
    if (not isinstance(rows, list) or tuple(row.get('profile') for row in rows) != RELEASE_PROFILES
            or not isinstance(settings_rows, list)
            or tuple(row.get('profile') for row in settings_rows) != RELEASE_PROFILES
            or not isinstance(images, list) or len(images) != len(RELEASE_PROFILES)
            or any(not isinstance(row, dict) for row in images)
            or len({row.get('profile') for row in images}) != len(RELEASE_PROFILES)
            or {row.get('profile') for row in images} != set(RELEASE_PROFILES)):
        raise ValueError('Matrix/settings catalogs need ten ordered profiles; capability catalog needs ten unique profiles')
    settings_rows = {row['profile']: row for row in settings_rows}
    matrix_rows = {row['profile']: row for row in rows}
    image_rows = {row['profile']: row for row in images}
    settings._catalog_images(settings_catalog)
    for context in contexts:
        profile = context.profile
        expected_identity, configuration = _identity_from_bundle(context)
        row, static = matrix_rows[profile], settings_rows[profile]
        expected_features = firmware_matrix.default_row(profile)
        settings_identity = static.get('settings_identity')
        if (not isinstance(settings_identity, dict)
                or row.get('configuration') != configuration or row.get('identity') != expected_identity
                or row.get('optional_features') != expected_features['optional_features']
                or row.get('capabilities') != expected_features['capabilities']
                or row.get('settings_identity') != settings_identity
                or settings_identity.get('ihx_sha256') != expected_identity['ihx_sha256']
                or settings_identity.get('nvm_schema') != configuration['nvm_schema']
                or static.get('configuration') != configuration):
            raise ValueError('Matrix or settings identity differs from approved image: ' + profile)
        image = image_rows[profile]
        image_hex = _checked_file(context.bundle, 'firmware/application.ihx')
        linked_code_identity = capability_builder.code_identity(pack_ak820.read_ihex(image_hex))
        if (image.get('build_identity') != expected_identity
                or image.get('settings_schema') != configuration['nvm_schema']
                or image.get('code_identity') != linked_code_identity
                or image.get('features') != sorted(configuration['base_features'] +
                                                   configuration['optional_features'])):
            raise ValueError('Capability image differs from approved profile: ' + profile)
        for suffix in ('ihx', 'map', 'mem'):
            path = f'profiles/{profile}/firmware/application.{suffix}'
            if path not in payload or sha(payload[path]) != expected_identity[suffix + '_sha256']:
                raise ValueError('Catalog profile firmware does not match approved image: ' + profile + '.' + suffix)


def validate_module_descriptions(value: dict | bytes) -> None:
    """Require module descriptions to cover the exact registry without dropping prose."""
    if isinstance(value, bytes):
        value = json.loads(value)
    import ak820_profiles
    descriptions = value.get('features')
    profiles = value.get('profiles')
    if (not isinstance(value, dict) or not isinstance(descriptions, list)
            or not isinstance(profiles, list) or len(profiles) != len(RELEASE_PROFILES)
            or any(not isinstance(row, dict) for row in profiles)):
        raise ValueError('Module descriptions must define ten profiles and a feature list')
    profile_ids = [row.get('id', row.get('profile')) for row in profiles]
    if len(set(profile_ids)) != len(RELEASE_PROFILES) or set(profile_ids) != set(RELEASE_PROFILES):
        raise ValueError('Module descriptions must define every release profile exactly once')
    feature_ids = [row.get('id') for row in descriptions if isinstance(row, dict)]
    expected_feature_ids = set()
    for profile in RELEASE_PROFILES:
        configuration = ak820_profiles.configuration(profile)
        features = sorted(configuration['base_features'] + configuration['optional_features'])
        row = profiles[profile_ids.index(profile)]
        if (row.get('profile', profile) != profile
                or row.get('configuration') != configuration
                or row.get('features') != features
                or row.get('optional_features') != configuration['optional_features']
                or row.get('default', profile == 'main') != (profile == 'main')):
            raise ValueError('Module description profile configuration/features differ from registry: ' + profile)
        expected_feature_ids.update(features)
    if (len(feature_ids) != len(set(feature_ids)) or not all(isinstance(name, str) for name in feature_ids)
            or not expected_feature_ids <= set(feature_ids)):
        raise ValueError('Module descriptions omit or duplicate a registered feature')

def build(bundles_root: Path, output: Path, tag: str) -> dict:
    if not re.fullmatch(r'v?\d+\.\d+\.\d+-beta\.\d+(?:\.\d+)?', tag):
        raise ValueError('Tag must be a beta version such as v0.6.0-beta.4 or v0.6.0-beta.4.1')
    contexts = ak820.release_contexts(approved=True)
    if len(contexts) != 10:
        raise ValueError('Beta.2 catalog requires all ten approved installer profiles')
    profile_ids = [context.profile for context in contexts]
    if tuple(profile_ids) != RELEASE_PROFILES or len(set(profile_ids)) != len(RELEASE_PROFILES):
        raise ValueError('Approved contexts differ from the exact ten-profile release catalog')
    bundles_root = Path(bundles_root).resolve(strict=True)
    for context in contexts:
        if not context.bundle.resolve(strict=True).is_relative_to(bundles_root):
            raise ValueError('Approved profile bundle is outside the supplied bundles root')
    payload = {name: (ROOT / 'web' / name).read_bytes() for name in
               ('firmware-matrix.json', 'module-descriptions.json', 'capability-catalog.json')}
    payload['profile-catalog.json'] = (ROOT / 'tools/installer/profile-catalog.json').read_bytes()
    payload['settings-catalog.json'] = (ROOT / 'tools/installer/settings-catalog.json').read_bytes()
    matrix = json.loads(payload['firmware-matrix.json'])
    by_profile = {item.get('profile'): item for item in matrix.get('profiles', [])
                  if isinstance(item, dict)}
    if tuple(row.get('profile') for row in matrix.get('profiles', [])) != RELEASE_PROFILES:
        raise ValueError('Firmware matrix must contain exactly the ten release profiles in catalog order')
    settings_catalog = json.loads(payload['settings-catalog.json'])
    capability_catalog = json.loads(payload['capability-catalog.json'])
    for context in contexts:
        bundle = context.bundle
        manifest = context.manifest
        row = by_profile[context.profile]
        identity, configuration = _identity_from_bundle(context)
        if row.get('identity') != identity or row.get('configuration') != configuration:
            raise ValueError('Web matrix identity differs from approved bundle: ' + context.profile)
        row['release_approved'] = True
        row['installable'] = True
        for name, item in manifest['files'].items():
            _safe_name(name)
            if name not in CI_PUBLIC_FILES or name == 'installer-release.json':
                raise ValueError('Approved bundle contains a non-public dependency: ' + context.profile + '/' + name)
            data = _checked_file(bundle, name).read_bytes()
            if len(data) != item['size'] or sha(data) != item['sha256']:
                raise ValueError('Approved bundle file changed: ' + context.profile + '/' + name)
            payload[f'profiles/{context.profile}/{name}'] = data
        for ext in ('ihx', 'map', 'mem'):
            name = f'firmware/application.{ext}'
            item = manifest['files'].get(name)
            if not item:
                raise ValueError(f'Approved bundle lacks {context.profile} {ext}')
            data = (bundle / name).read_bytes()
            if sha(data) != item['sha256']:
                raise ValueError(f'Approved bundle hash changed: {context.profile}/{name}')
            payload[f'profiles/{context.profile}/firmware/application.{ext}'] = data
        for name, path in (('installer-release.json', bundle / 'installer-release.json'),
                           ('approved-release.json', context.approval)):
            payload[f'profiles/{context.profile}/{name}'] = path.read_bytes()
    payload['firmware-matrix.json'] = canonical(matrix)
    for name in guide_files():
        payload[name] = (ROOT / name).read_bytes()
    validate_profile_links(payload, contexts, settings_catalog, capability_catalog,
                           payload['module-descriptions.json'])
    caps = capability_catalog
    caps['release_approved'] = False
    caps['hardware_validated'] = False
    caps['flashing_authorized'] = False
    caps['settings_writes_authorized'] = False
    caps['status'] = 'beta-catalog; physical operations require fresh consent'
    for image in caps.get('images', []):
        image['release_approved'] = image.get('profile') in profile_ids
        image['flashing_authorized'] = False
        image['settings_writes_authorized'] = False
        image['hardware_validated'] = False
    payload['capability-catalog.json'] = canonical(caps)
    for lang, source in (('en', ROOT / 'docs/INSTALL.md'), ('ru', ROOT / 'docs/ru/INSTALL.md')):
        payload['INSTALL-' + lang + '.md'] = standalone_guide(source)
    files = {name: {'sha256': sha(data), 'size': len(data)} for name, data in sorted(payload.items())}
    descriptor = {'format': FORMAT, 'tag': tag, 'status': 'beta', 'default_profile': 'main',
                  'installable_profiles': profile_ids, 'catalog_profiles': [r['profile'] for r in matrix['profiles']],
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
        python_files = python_package_files(contexts)
        package_hashes = write_python_packages(stage, python_files)
        archive = stage / 'AK820-Beta3-Catalog.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for name in sorted(payload):
                info = zipfile.ZipInfo(name, (1980,1,1,0,0,0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
                zf.writestr(info, payload[name])
        digest = sha(archive.read_bytes())
        (stage / 'AK820-Beta3-Catalog.zip.sha256').write_text(digest + '  AK820-Beta3-Catalog.zip\n')
        checksum_names = sorted(set(payload) | {'AK820-Beta3-Catalog.zip',
                                                'AK820-Windows.zip', 'AK820-Linux-x86_64.tar.gz'})
        (stage / 'SHA256SUMS').write_text(''.join(sha((stage / n).read_bytes()) + '  ' + n + '\n' for n in checksum_names))
        stage.rename(output)
    return {'output': str(output), 'tag': tag, 'profiles': len(profile_ids), 'installable_profiles': profile_ids, 'zip_sha256': digest, 'python_package_sha256': package_hashes}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundles-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--tag', required=True)
    args = parser.parse_args(argv)
    print(json.dumps(build(args.bundles_root, args.output, args.tag), sort_keys=True))
    return 0

if __name__ == '__main__': raise SystemExit(main())
