#!/usr/bin/env python3
"""Assemble a public installer bundle from a freshly compiled CI build.

This reuses a previously reviewed, sanitized offline packing receipt. It does
not contain private OEM inputs, make a hardware claim, or authorize an update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(SOURCE / 'util'))
sys.path.insert(0, str(ROOT / 'tools'))

import ak820_diagnose as diagnostic
import ak820_ci_authorization as authorization
import ak820_release_safety as release_safety
import build_release_bundle as release
import build_capability_catalog as capability_catalog
from ak820_profiles import require_release_qualification, validate_configuration
from ak820_release_manifest import RELEASE, MANIFEST_FORMAT, host_manifest

PUBLIC_FILES = (
    'firmware/application.ihx', 'firmware/application.map', 'firmware/application.mem',
    'reports/build-report.json', 'reports/packing-validation.json',
    'reports/qualification.json', 'reports/build-attestation.json',
    'reference/info.json', 'reference/vial.json', 'reproduction/build_ak820.py',
    'reviews/program-policy.json', 'reviews/program-review.md',
    'reviews/independent-review.md', 'installer-release.json',
)
SDCC46_S51_SHA256 = '61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object: ' + str(path))
    return value


def _git_head() -> str:
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                          stdout=subprocess.PIPE, text=True).stdout.strip()


def _validate_source_commit(source_commit: str) -> None:
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Source commit must be a 40-character lowercase Git SHA')
    if source_commit != _git_head():
        raise ValueError('Source commit does not match the current committed HEAD')


def _git_blob(path: Path) -> bytes:
    try:
        lexical = Path(os.path.abspath(path if path.is_absolute() else ROOT / path))
        relative = lexical.relative_to(Path(os.path.abspath(ROOT))).as_posix()
    except ValueError as error:
        raise ValueError('Reviewed input must be inside the repository: ' + str(path)) from error
    current = Path(os.path.abspath(ROOT))
    for component in Path(relative).parts:
        current = current / component
        if current.is_symlink():
            raise ValueError('Reviewed input must not be a symlink: ' + relative)
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Reviewed input resolves outside the repository: ' + str(path))
    try:
        return subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=ROOT, check=True,
                              stdout=subprocess.PIPE).stdout
    except subprocess.CalledProcessError as error:
        raise ValueError('Reviewed input is not present in committed HEAD: ' + relative) from error


def _require_committed_input(path: Path, label: str) -> None:
    actual = path.read_bytes()
    if _git_blob(path) != actual:
        raise ValueError(label + ' differs from committed HEAD: ' + str(path))


def _review_record(review_bytes: bytes) -> dict:
    records = []
    for block in re.findall(rb'^```json\s*\n(.*?)^```\s*$', review_bytes, re.M | re.S):
        value = json.loads(block)
        if isinstance(value, dict) and value.get('format') == 'ak820-ci-program-review-1':
            records.append(value)
    if len(records) != 1:
        raise ValueError('Program review must contain exactly one ak820-ci-program-review-1 record')
    return records[0]


def _validate_policy_sources(policy: dict, report: dict) -> None:
    declared = policy.get('source_files')
    if not isinstance(declared, dict) or not declared:
        raise ValueError('Program policy lacks a source_files manifest')
    lufa_lock_name = 'qmk-8051-ak820/dependencies/lufa.json'
    if lufa_lock_name not in declared:
        raise ValueError('Program policy omits the committed LUFA dependency lock')
    lufa_lock_path = ROOT / lufa_lock_name
    if not lufa_lock_path.is_file() or _git_blob(lufa_lock_path) != lufa_lock_path.read_bytes():
        raise ValueError('LUFA dependency lock differs from committed HEAD')
    lufa_lock = load_json(lufa_lock_path)
    if (lufa_lock.get('format') != 'ak820-external-dependency-1'
            or lufa_lock.get('name') != 'lufa' or lufa_lock.get('destination') != 'lib/lufa'
            or lufa_lock.get('revision') != '549b97320d515bfca2f95c145a67bd13be968faa'
            or not isinstance(lufa_lock.get('required_files'), dict)):
        raise ValueError('Unsupported committed LUFA dependency lock')
    lufa_files = lufa_lock['required_files']
    for name, expected in declared.items():
        if (not isinstance(name, str) or not isinstance(expected, dict)
                or name.startswith('/') or '\\' in name or any(part in ('', '.', '..') for part in name.split('/'))
                or not isinstance(expected.get('size'), int)
                or not re.fullmatch(r'[0-9a-f]{64}', str(expected.get('sha256', '')))):
            raise ValueError('Invalid policy source record')
        raw_path = ROOT / name
        path = raw_path.resolve()
        current = ROOT
        symlinked = False
        for component in Path(name).parts:
            current = current / component
            symlinked = symlinked or current.is_symlink()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file() or symlinked:
            raise ValueError('Missing or unsafe policy source: ' + name)
        if path.stat().st_size != expected['size'] or sha(path) != expected['sha256']:
            raise ValueError('Program source differs from reviewed policy: ' + name)
        lufa_prefix = 'qmk-8051-ak820/lib/lufa/'
        if name.startswith(lufa_prefix):
            relative = name[len(lufa_prefix):]
            locked_sha = lufa_files.get(relative)
            if not locked_sha or expected['sha256'] != locked_sha:
                raise ValueError('External source is absent from the committed LUFA lock: ' + name)
        elif _git_blob(path) != path.read_bytes():
            raise ValueError('Program source differs from committed HEAD: ' + name)
    # The compiler report independently identifies the inputs actually used
    # by this link. Every source input must be represented in the policy.
    for item in report.get('sources', []):
        if item.get('origin') != 'source':
            continue
        source_path = item.get('path', '').replace('\\', '/')
        if source_path.startswith('.build/'):
            continue
        name = 'qmk-8051-ak820/' + source_path
        if name not in declared or declared[name].get('sha256') != item.get('sha256'):
            raise ValueError('Build source is absent from the reviewed policy: ' + name)
    required = set(host_manifest(ROOT)) | {
        '.github/workflows/windows-installer.yml', 'tools/ci_checks.py',
        'tools/test_keyboard.py', 'tools/build_ci_release.py', 'tools/build_ci_profiles.py',
    }
    if 'configuration' in report:
        # The independent policy must bind the safety review itself, including
        # its pinned witnesses. An uncommitted replacement is not a new review.
        safety_name = release_safety.manifest_name(report.get('configuration'))
        safety = load_json(ROOT / safety_name)
        required.add(safety_name)
        required.update(safety.get('source_files', {}))
        required.update(record['path'] for record in safety.get('witnesses', {}).values())
    if not required <= declared.keys():
        raise ValueError('Program policy omits required source or CI files')


def _qualification(report: dict, path: Path, ihx: Path, mapfile: Path, toolchain: Path) -> None:
    hashes = {'ihx': sha(ihx), 'map': sha(mapfile)}
    if (report.get('format') != 'ak820-offline-tests-1' or report.get('passed') is not True
            or report.get('require_toolchain') is not True
            or report.get('hardware_validated') is not False
            or report.get('iap_fault_profile') != 'guarded-erase'
            or report.get('physical_device_commands') != 0
            or report.get('build_unchanged') is not True
            or report.get('build_hashes') != hashes
            or report.get('unit_tests', {}).get('skipped') != 0
            or report.get('unit_tests', {}).get('run', 0) <= 0):
        raise ValueError('Qualification report does not prove a complete offline pass on this build')
    tools = report.get('tools', {})
    if not {'sdcc', 's51'} <= tools.keys() or any(not tools[name].get('sha256') for name in ('sdcc', 's51')):
        raise ValueError('Qualification report lacks pinned compiler and simulator evidence')
    expected_tools = {'sdcc': release.SDCC46_PINS['sdcc'], 's51': SDCC46_S51_SHA256}
    for name, expected in expected_tools.items():
        actual = tools[name].get('sha256')
        if actual != expected or sha(toolchain / 'bin' / name) != expected:
            raise ValueError('Qualification used an unexpected pinned tool: ' + name)
    tests = report.get('tests')
    if not isinstance(tests, list) or not tests:
        raise ValueError('Qualification report has no test results')
    for result in tests:
        if (result.get('exit_code') != 0 or result.get('unit_tests', {}).get('skipped', 0) != 0
                or result.get('build_before') != hashes or result.get('build_after') != hashes):
            raise ValueError('Qualification includes a failed, skipped or changed-build test')


def assemble(build_dir: Path, qualification_path: Path, policy_path: Path,
             program_review_path: Path, packing_receipt_path: Path, output: Path,
             toolchain: Path, source_commit: str, *, expected_profile: str | None = None) -> dict:
    _validate_source_commit(source_commit)
    original_inputs = (policy_path, program_review_path, packing_receipt_path)
    for path in original_inputs:
        _git_blob(path)
    build_dir, output, toolchain = build_dir.resolve(), output.resolve(), toolchain.resolve()
    qualification_path, policy_path = qualification_path.resolve(), policy_path.resolve()
    program_review_path, packing_receipt_path = program_review_path.resolve(), packing_receipt_path.resolve()
    if output.exists():
        raise ValueError('Output already exists; select a fresh directory')
    archive = output.with_suffix('.zip')
    checksum = output.with_suffix('.zip.sha256')
    if archive.exists() or checksum.exists():
        raise ValueError('Archive or checksum output already exists')
    if not build_dir.is_relative_to(SOURCE.resolve()) or not output.is_relative_to(ROOT.resolve()):
        raise ValueError('Build and output must remain inside this repository')
    for path in (qualification_path, policy_path, program_review_path, packing_receipt_path):
        if not path.is_file():
            raise ValueError('Missing CI input: ' + str(path))
    for path, label in ((policy_path, 'Program policy'), (program_review_path, 'Program review'),
                        (packing_receipt_path, 'Packing receipt')):
        _require_committed_input(path, label)

    report_path = build_dir / 'build-report.json'
    ihx, mapfile, mem = (build_dir / f'ajazz_ak820_vial.{ext}' for ext in ('ihx', 'map', 'mem'))
    report = load_json(report_path)
    require_release_qualification(report)
    actual_profile = report.get('configuration', {}).get('profile')
    if expected_profile is not None and actual_profile != expected_profile:
        raise ValueError(f'Build profile mismatch: expected {expected_profile}, got {actual_profile}')
    configuration = validate_configuration(report.get('configuration'))
    if expected_profile is not None and configuration['profile'] not in release_profile_names():
        raise ValueError('Build configuration is outside the release profile catalog')
    if report.get('keyboard') != 'ajazz/ak820' or report.get('keymap') != 'vial':
        raise ValueError('Wrong firmware build target')
    if (report.get('build_id') != configuration['nvm_schema']
            or report.get('hardware_validated') is not False):
        raise ValueError('Unexpected build schema or hardware-validation claim')
    diagnostic.diagnostic_build(ihx, mapfile, report_path)
    for artifact in (ihx, mapfile, mem):
        release.validate_build_artifact(report, artifact)
    release.validate_tools(report, toolchain)

    qualification_bytes = qualification_path.read_bytes()
    qualification = json.loads(qualification_bytes)
    _qualification(qualification, qualification_path, ihx, mapfile, toolchain)
    authorization.validate_qualification_contract(qualification)
    policy_bytes = policy_path.read_bytes()
    policy = json.loads(policy_bytes)
    if not isinstance(policy, dict):
        raise ValueError('Program policy must be a JSON object')
    receipt_bytes, review_bytes = packing_receipt_path.read_bytes(), program_review_path.read_bytes()
    current_host = host_manifest(ROOT)
    authorization.validate_policy(policy, current_host, receipt_bytes, review_bytes)
    if (type(policy['program'].get('schema')) is not int
            or policy['program']['schema'] != report.get('build_id')
            or policy['program']['schema'] != configuration['nvm_schema']):
        raise ValueError('Reviewed program schema differs from the actual build')
    _validate_policy_sources(policy, report)
    policy_source_snapshot = {name: sha(ROOT / name) for name in policy['source_files']}
    if _review_record(review_bytes).get('policy_sha256') != digest(policy_bytes):
        raise ValueError('Program review belongs to a different policy')
    if (policy['program']['ihx_sha256'] != sha(ihx)
            or policy['program']['symbols_sha256'] != authorization.symbols_sha256(mapfile)):
        raise ValueError('Fresh build does not match the independently reviewed program')

    # The machine review record is explicit that it is a reproduced build; it
    # does not claim a human reviewer or hardware validation.
    reproduced = {
        'format': 'ak820-reproduced-review-1', 'release': RELEASE, 'status': 'passed',
        'hardware_validated': False, 'source_commit': source_commit,
        'policy_sha256': digest(policy_bytes), 'program_review_sha256': digest(review_bytes),
    }
    files = {
        'firmware/application.ihx': ihx,
        'firmware/application.map': mapfile,
        'firmware/application.mem': mem,
        'reports/build-report.json': report_path,
        'reference/info.json': SOURCE / 'keyboards/ajazz/ak820/info.json',
        'reference/vial.json': SOURCE / 'keyboards/ajazz/ak820/keymaps/vial/vial.json',
        'reproduction/build_ak820.py': SOURCE / 'util/build_ak820.py',
    }
    for name, path in files.items():
        if not path.is_file():
            raise ValueError('Missing release input for ' + name)
    if (host_manifest(ROOT) != current_host
            or any(sha(ROOT / name) != value for name, value in policy_source_snapshot.items())
            or _git_head() != source_commit):
        raise ValueError('Host code changed while assembling the release')

    output.mkdir(parents=True)
    try:
        for name, path in files.items():
            dest = output / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
        (output / 'reports').mkdir(exist_ok=True)
        shutil.copyfile(packing_receipt_path, output / 'reports/packing-validation.json')
        shutil.copyfile(qualification_path, output / 'reports/qualification.json')
        (output / 'reviews').mkdir(exist_ok=True)
        shutil.copyfile(policy_path, output / 'reviews/program-policy.json')
        shutil.copyfile(program_review_path, output / 'reviews/program-review.md')
        review_doc = ('# Reproduced CI build\n\nThis record confirms that an offline CI run reproduced the program '
                      'approved by the program policy. It is a machine record, not a claim of independent human '
                      'review or hardware validation.\n\n```json\n'
                      + json.dumps(reproduced, ensure_ascii=False, indent=2) + '\n```\n')
        (output / 'reviews/independent-review.md').write_text(review_doc, encoding='utf-8')
        attestation = {
            'format': 'ak820-ci-build-attestation-1', 'source_commit': source_commit,
            'build': {'ihx_sha256': sha(ihx), 'map_sha256': sha(mapfile), 'mem_sha256': sha(mem),
                      'build_report_sha256': sha(report_path)},
            'policy_sha256': digest(policy_bytes), 'program_review_sha256': digest(review_bytes),
            'qualification_sha256': digest(qualification_bytes), 'host_files': current_host,
            'hardware_validated': False,
        }
        write_json(output / 'reports/build-attestation.json', attestation)
        if (host_manifest(ROOT) != current_host
                or any(sha(ROOT / name) != value for name, value in policy_source_snapshot.items())
                or _git_head() != source_commit):
            raise ValueError('Host or reviewed source code changed while assembling the release')
        bound = [name for name in PUBLIC_FILES if name not in ('installer-release.json',)]
        manifest = {
            'format': MANIFEST_FORMAT, 'release': RELEASE, 'host_files': current_host,
            'hardware': 'AJAZZ AK820 wired / VS11K28A / 320F:505B',
            'trial_only': False, 'install_modes': ['permanent', 'trial'], 'hardware_validated': False,
            'offline_review': {'status': 'passed', 'report': 'reviews/independent-review.md'},
            'files': {name: {'size': (output / name).stat().st_size, 'sha256': sha(output / name)}
                      for name in bound},
        }
        write_json(output / 'installer-release.json', manifest)
        record = dict(reproduced, build={
            'ihx_sha256': sha(ihx), 'map_sha256': sha(mapfile),
            'build_report_sha256': sha(report_path)}, host_files=current_host,
            attestation_sha256=sha(output / 'reports/build-attestation.json'))
        # Rebind the machine record with all generated evidence before running
        # the canonical installer validation gate.
        review_doc = ('# Reproduced CI build\n\nThis record confirms that an offline CI run reproduced the program '
                      'approved by the program policy. It is a machine record, not a claim of independent human '
                      'review or hardware validation.\n\n```json\n'
                      + json.dumps(record, ensure_ascii=False, indent=2) + '\n```\n')
        (output / 'reviews/independent-review.md').write_text(review_doc, encoding='utf-8')
        manifest['files']['reviews/independent-review.md'] = {
            'size': (output / 'reviews/independent-review.md').stat().st_size,
            'sha256': sha(output / 'reviews/independent-review.md')}
        write_json(output / 'installer-release.json', manifest)
        approval = {'format': 'ak820-installer-approval-1', 'release': RELEASE,
                    'manifest_sha256': sha(output / 'installer-release.json')}
        write_json(output / 'approved-release.json', approval)
        authorization.validate_bundle_authorization(output, manifest, record)
        if (host_manifest(ROOT) != current_host
                or any(sha(ROOT / name) != value for name, value in policy_source_snapshot.items())
                or _git_head() != source_commit):
            raise ValueError('Host or reviewed source code changed while assembling the release')
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zf:
            for name in PUBLIC_FILES:
                zf.write(output / name, name)
            zf.write(output / 'approved-release.json', 'approved-release.json')
        checksum.write_text(f'{sha(archive)}  {archive.name}\n', encoding='ascii')
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        archive.unlink(missing_ok=True)
        checksum.unlink(missing_ok=True)
        raise
    return {'directory': str(output), 'archive': str(archive), 'archive_sha256': sha(archive),
            'manifest_sha256': sha(output / 'installer-release.json'), 'trial_only': False,
            'hardware_validated': False, 'packing_receipt_reused': True,
            'private_oem_inputs_included': False, 'full_rom_included': False}


def release_profile_names() -> tuple[str, ...]:
    import ak820_profiles
    names = tuple(ak820_profiles.RELEASE_PROFILES)
    expected = ('main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios')
    if names != expected:
        raise ValueError('Release profile order differs from the reviewed ten-profile catalog')
    return names


def reproducible_identity(build: Path, measured_identity: dict) -> dict:
    """Bind a catalog row to linked content without path-dependent reports.

    The caller must obtain measured_identity from a fresh inspect of build.
    Keep raw artifact hashes in that inspection and its qualification reports.
    """
    fields = ('profile', 'configuration_sha256', 'ihx_sha256',
              'compiler_sha256', 'nvm_schema')
    if not isinstance(measured_identity, dict) or any(
            not isinstance(measured_identity.get(field), str) or not measured_identity[field]
            for field in fields if field != 'nvm_schema') or type(
                measured_identity.get('nvm_schema')) is not int:
        raise ValueError('Measured build lacks a reproducible identity field')
    if (any(not re.fullmatch(r'[0-9a-f]{64}', measured_identity[field])
            for field in ('configuration_sha256', 'ihx_sha256', 'compiler_sha256'))
            or not re.fullmatch(r'[a-z0-9-]+', measured_identity['profile'])
            or measured_identity['nvm_schema'] not in (authorization.pack.BUILD_ID,
                                                        authorization.pack.EXTENSION_BUILD_ID)
            or measured_identity['profile'] not in release_profile_names()):
        raise ValueError('Measured build has an invalid reproducible identity field')
    mapfile = build / 'ajazz_ak820_vial.map'
    if not mapfile.is_file() or mapfile.is_symlink():
        raise ValueError('Missing or unsafe MAP for reproducible identity')
    return {**{field: measured_identity[field] for field in fields},
            'symbols_sha256': authorization.symbols_sha256(mapfile)}


def settings_matrix_from_builds(builds_root: Path, toolchain: Path,
                                settings_catalog_path: Path) -> tuple[dict, dict]:
    """Rebuild measured rows from every exact configured image and bind static settings contracts.

    The CODE identities in settings-catalog.json are generated during source
    preparation with the protected local OEM reference. CI remeasures linked
    identities and qualification, then requires every catalog entry to match
    that exact IHX and configuration before any installer manifest is emitted.
    """
    import firmware_matrix
    import ak820_profiles
    sys.path.insert(0, str(ROOT / 'tools/installer'))
    import settings_backup
    names = release_profile_names()
    catalog = load_json(settings_catalog_path)
    if (catalog.get('format') != firmware_matrix.FORMAT or
            not isinstance(catalog.get('settings_transitions'), list) or
            not isinstance(catalog.get('profiles'), list)):
        raise ValueError('Settings catalog is not a trusted firmware matrix')
    catalog_entries = catalog['profiles']
    if (not all(isinstance(row, dict) for row in catalog_entries)
            or tuple(row.get('profile') for row in catalog_entries) != names):
        raise ValueError('Settings catalog must contain exactly ten unique profiles in catalog order')
    catalog_rows = {row['profile']: row for row in catalog_entries}
    catalog_images = settings_backup._catalog_images(catalog)
    builds = {}
    measured = {}
    for name in names:
        build = builds_root / name
        if not build.is_dir() or build.is_symlink():
            raise ValueError('Missing or unsafe profile build directory: ' + name)
        row = firmware_matrix.measured_row(build, toolchain)
        if (row.get('profile') != name or row.get('configuration') != ak820_profiles.configuration(name) or
                row.get('measurement_status') != 'linked-memory-pass' or
                row.get('runtime_status') != 'exact-image-pass' or
                row.get('offline_tests_status') != 'exact-image-pass'):
            raise ValueError('Profile lacks complete exact-image qualification: ' + name)
        approved = catalog_rows[name]
        identity = approved.get('settings_identity')
        catalog_identity = approved.get('reproducible_identity')
        static_artifact_identity = approved.get('identity')
        measured_identity = reproducible_identity(build, row.get('identity'))
        if (not isinstance(identity, dict) or not isinstance(catalog_identity, dict) or
                catalog_identity != measured_identity or
                not isinstance(static_artifact_identity, dict) or
                static_artifact_identity.get('ihx_sha256') != measured_identity['ihx_sha256'] or
                static_artifact_identity.get('nvm_schema') != measured_identity['nvm_schema'] or
                measured_identity['profile'] != name or
                approved.get('release_approved') is not False or approved.get('installable') is not False or
                identity.get('ihx_sha256') != row.get('identity', {}).get('ihx_sha256') or
                identity.get('nvm_schema') != ak820_profiles.configuration(name)['nvm_schema'] or
                approved.get('configuration') != row.get('configuration')):
            raise ValueError('Static settings contract does not bind the measured profile: ' + name)
        row['reproducible_identity'] = measured_identity
        row['settings_identity'] = identity
        row['settings_status'] = 'exact-image-contract'
        builds[name] = build
        measured[name] = row
    identities = [row['identity']['ihx_sha256'] for row in measured.values()]
    if len(identities) != len(set(identities)):
        raise ValueError('Release profiles do not have unique exact image identities')
    historical = {source['ihx_sha256'] for source in catalog.get('historical_sources', [])}
    if set(catalog_images) != set(identities) | historical:
        raise ValueError('Settings catalog does not contain exactly the measured and pinned historical identities')
    result = firmware_matrix.matrix(measured)
    result['settings_transitions'] = catalog['settings_transitions']
    if 'historical_sources' in catalog:
        result['historical_sources'] = catalog['historical_sources']
    if any(row.get('release_approved') is not False or row.get('installable') is not False
           for row in result['profiles']):
        raise ValueError('Measured candidate matrix must remain unapproved until bundle gates pass')
    return result, builds


def assemble_profiles(builds_root: Path, policies_root: Path, output_root: Path,
                      toolchain: Path, source_commit: str,
                      settings_catalog_path: Path | None = None) -> dict:
    """Assemble ten separately authorized profile bundles as one atomic output.

    Every profile carries its own committed exact-image policy, review and
    packing receipt. The existing single-image assembly gate validates each
    one without replacing its policy or approval checks.
    """
    names = release_profile_names()
    _validate_source_commit(source_commit)
    builds_root = builds_root.resolve()
    policies_root = policies_root.resolve()
    output_root = output_root.absolute()
    toolchain = toolchain.resolve()
    settings_catalog_path = (settings_catalog_path or ROOT / 'tools/installer/settings-catalog.json').resolve()
    if not builds_root.is_relative_to(SOURCE.resolve()) or not policies_root.is_relative_to(ROOT.resolve()):
        raise ValueError('Profile builds and policy inputs must remain inside the repository')
    if not output_root.is_relative_to(ROOT.resolve()) or output_root.exists() or output_root.is_symlink():
        raise ValueError('Choose a fresh profile-release output inside the repository')
    if not settings_catalog_path.is_file() or settings_catalog_path.is_symlink():
        raise ValueError('Missing or unsafe committed settings catalog')
    _require_committed_input(settings_catalog_path, 'Settings catalog')
    matrix, builds = settings_matrix_from_builds(builds_root, toolchain, settings_catalog_path)
    inputs = {}
    for profile in names:
        profile_dir = policies_root / profile
        if not profile_dir.is_dir() or profile_dir.is_symlink():
            raise ValueError('Missing or unsafe profile authorization directory: ' + profile)
        files = {'policy': profile_dir / 'release-policy.json',
                 'review': profile_dir / 'program-review.md',
                 'receipt': profile_dir / 'packing-validation.json'}
        for label, path in files.items():
            if not path.is_file() or path.is_symlink():
                raise ValueError(f'Missing or unsafe {profile} {label}')
            _require_committed_input(path, f'{profile} {label}')
        inputs[profile] = files

    capabilities = capability_catalog.catalog([builds[name] for name in names], toolchain)
    output_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.' + output_root.name + '.stage-', dir=output_root.parent) as temporary:
        stage = Path(temporary) / output_root.name
        profiles_dir = stage / 'profiles'
        profiles_dir.mkdir(parents=True)
        reports_dir = stage / 'reports'
        reports_dir.mkdir()
        write_json(reports_dir / 'firmware-matrix.json', matrix)
        write_json(reports_dir / 'capability-catalog.json', capabilities)
        write_json(reports_dir / 'settings-catalog-attestation.json', {
            'format': 'ak820-ci-settings-catalog-check-1',
            'settings_catalog_sha256': sha(settings_catalog_path),
            'profiles': {name: matrix['profiles'][index]['identity']['ihx_sha256']
                         for index, name in enumerate(names)},
            'hardware_validated': False, 'physical_device_commands': 0,
        })
        results = {}
        for profile in names:
            build = builds[profile]
            paths = inputs[profile]
            destination = profiles_dir / profile
            qualification = build / 'qualification.json'
            results[profile] = assemble(build, qualification, paths['policy'], paths['review'],
                                        paths['receipt'], destination, toolchain, source_commit,
                                        expected_profile=profile)
            # Per-profile ZIPs are retained separately from the deployable
            # ten-profile archive, avoiding archive files in the profile tree.
            profile_archive = Path(results[profile]['archive'])
            archive_dir = stage / 'profile-archives'
            archive_dir.mkdir(exist_ok=True)
            profile_archive.rename(archive_dir / (profile + '.zip'))
            Path(results[profile]['archive'] + '.sha256').unlink(missing_ok=True)
        archive = stage / 'firmware-bundle.zip'
        checksum = stage / 'firmware-bundle.zip.sha256'
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as package:
            for path in sorted(profiles_dir.rglob('*')):
                if not path.is_file():
                    continue
                entry = zipfile.ZipInfo(path.relative_to(stage).as_posix(), (1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                package.writestr(entry, path.read_bytes())
        checksum.write_text(f'{sha(archive)}  firmware-bundle.zip\n', encoding='ascii')
        if _git_head() != source_commit:
            raise ValueError('Committed source changed while assembling profile releases')
        if output_root.exists() or output_root.is_symlink():
            raise ValueError('Profile-release output appeared during assembly')
        stage.rename(output_root)
    return {'output': str(output_root), 'profiles': list(names),
            'archive': str(output_root / 'firmware-bundle.zip'),
            'archive_sha256': sha(output_root / 'firmware-bundle.zip'),
            'all_profile_approvals_written': True, 'hardware_validated': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--all-profiles', action='store_true',
                      help='Assemble ten independently authorized exact-profile bundles')
    mode.add_argument('--build-dir', type=Path)
    parser.add_argument('--qualification', type=Path)
    parser.add_argument('--policy', type=Path)
    parser.add_argument('--program-review', type=Path)
    parser.add_argument('--packing-receipt', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--builds-root', type=Path)
    parser.add_argument('--policies-root', type=Path, default=ROOT / 'ci/profiles')
    parser.add_argument('--settings-catalog', type=Path, default=ROOT / 'tools/installer/settings-catalog.json')
    parser.add_argument('--toolchain', type=Path, default=Path('toolchains/sdcc-4.6.0'))
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    def rooted(path):
        return path if path.is_absolute() else ROOT / path
    if args.all_profiles:
        if args.builds_root is None or args.output is None:
            parser.error('--all-profiles requires --builds-root and --output')
        result = assemble_profiles(rooted(args.builds_root), rooted(args.policies_root),
                                   rooted(args.output), rooted(args.toolchain), args.source_commit,
                                   rooted(args.settings_catalog))
    else:
        if any(path is None for path in (args.qualification, args.policy, args.program_review,
                                          args.packing_receipt, args.output)):
            parser.error('Single-profile mode requires --qualification, --policy, --program-review, --packing-receipt, and --output')
        result = assemble(rooted(args.build_dir), rooted(args.qualification), rooted(args.policy),
                          rooted(args.program_review), rooted(args.packing_receipt), rooted(args.output),
                          rooted(args.toolchain), args.source_commit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
