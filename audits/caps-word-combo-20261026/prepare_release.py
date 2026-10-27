"""Prepare exact-image catalog, packing, transition and policy drafts offline.

Default execution writes audit evidence only. Review the draft catalog, install
its identical bytes in both catalog locations, freeze sources and run settings
tests before using --write-policies with a new private output directory.
--settings-run accepts a successful record with command, exit_code, source_files,
log_path and log_sha256; every source and log is checked before reuse. Public
historical bundles must be authenticated before this script is run. Their linked
IHX and reconstructed packed CODE are checked against retained exact identities.
No independent approval is generated. No device is opened.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
sys.path.insert(0, str(ROOT / 'tools'))
import configure_firmware as configured
import ak820_ci_authorization as authorization
import ak820_release_safety as safety
sys.path.insert(0, str(ROOT / 'tools'))
from build_windows_installer import guide_files
from ak820_release_manifest import host_manifest

GROUPS = {'a': ('main', 'game', 'mmo', 'creative'),
          'b': ('typing', 'code', 'multios'),
          'c': ('pointer', 'onehand', 'shortcuts')}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(path):
    return {'size': path.stat().st_size, 'sha256': digest(path)}

def relative(path):
    return str(path.relative_to(ROOT))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def require(value, message):
    if not value:
        raise ValueError(message)

def profile_build(args, name):
    path = args.build_overrides.get(name, args.builds_root / name)
    require(not path.is_symlink(), 'Symlinked profile build: ' + name)
    path = path.resolve()
    require(path.is_relative_to((ROOT / 'qmk-8051-ak820').resolve()) and path.is_dir(),
            'Missing or external profile build: ' + name)
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings-run', type=Path)
    preparation_arguments(parser)
    args = parser.parse_args()
    if args.settings_run:
        test = json.loads(args.settings_run.read_text())
        require(test['exit_code'] == 0 and test['command'] and test['source_files'], 'Failed or incomplete settings test record')
        for name, sha in test['source_files'].items():
            require(digest(safety.safe_path(ROOT, name)) == sha, 'Stale settings test source: ' + name)
        require(digest(safety.safe_path(ROOT, test['log_path'])) == test['log_sha256'], 'Stale settings test log')
    prepare(args)
    if not args.write_policies:
        print('Prepared draft catalog, packing and transitions; policies were not changed.')
        return
    packing = json.loads((AUDIT / 'packing-preflight.json').read_text())
    transitions = json.loads((AUDIT / 'transition-preflight.json').read_text())
    require(packing['offline_only'] and packing['physical_device_commands'] == 0, "Preparation input check failed: packing['offline_only'] and packing['physical_device_commands'] == 0")
    require(all(c['passed'] for c in transitions['cases']), 'Failed transition preflight')
    tests = []
    if args.settings_run:
        test = json.loads(args.settings_run.read_text())
        require(test['exit_code'] == 0 and test['command'] and test['source_files'], "Preparation input check failed: test['exit_code'] == 0 and test['command'] and test['source_files']")
        for name, sha in test['source_files'].items():
            require(digest(safety.safe_path(ROOT, name)) == sha, 'Preparation input check failed: digest(safety.safe_path(ROOT, name)) == sha')
        require(digest(safety.safe_path(ROOT, test['log_path'])) == test['log_sha256'], "Preparation input check failed: digest(safety.safe_path(ROOT, test['log_path'])) == test['log_sha256']")
        tests.append(test)
    outputs = []
    for group, profiles in GROUPS.items():
        for profile in profiles:
            build = profile_build(args, profile)
            report = json.loads((build / 'build-report.json').read_text())
            require(' 4.6.0 ' in report['compiler_version'], "Preparation input check failed: ' 4.6.0 ' in report['compiler_version']")
            summary = json.loads((build / 'runtime-safety/summary.json').read_text())
            ihx = digest(build / 'ajazz_ak820_vial.ihx')
            require(summary['passed'] and summary['identity']['ihx_sha256'] == ihx, "Preparation input check failed: summary['passed'] and summary['identity']['ihx_sha256'] == ihx")
            for name, expected_sha in summary['source_files'].items():
                require(digest(safety.safe_path(ROOT, name)) == expected_sha, 'Stale runtime proof source: ' + profile + '/' + name)
            require(report['configuration']['profile'] == profile, "Preparation input check failed: report['configuration']['profile'] == profile")
            pack = next(p for p in packing['profiles'] if p['profile'] == profile)
            require(pack['build']['ihx_sha256'] == ihx, "Preparation input check failed: pack['build']['ihx_sha256'] == ihx")
            cases = [c for c in transitions['cases'] if c['target_profile'] == profile]
            require(len(cases) == transitions['sources_per_target'] and all(c['target'] == ihx for c in cases), 'Incomplete target transition coverage')
            alpha = next(c for c in cases if c['source_case'] == 'alpha2-saved-rom')
            evidence = AUDIT / 'profiles' / profile
            evidence.mkdir(parents=True, exist_ok=True)
            for src, dst in [('runtime-stack.json', 'stack.json'),
                             ('runtime-safety/startup.json', 'startup.json'),
                             ('runtime-safety/irq/results.json', 'irq.json'),
                             ('runtime-safety/summary.json', 'runtime-summary.json')]:
                shutil.copyfile(build / src, evidence / dst)
            write(evidence / 'alpha2-preflight.json', alpha)
            transition = {'format': 'ak820-settings-transition-1', 'passed': bool(tests),
                'offline_only': True, 'physical_device_commands': 0,
                'scope': 'Offline exact-image preflight; complete frozen settings test record required. No device validation.',
                'target': {'ihx_sha256': ihx, 'schema': report['build_id'],
                           'optional_features': report['configuration']['optional_features'],
                           'code_sha256': pack['settings_code_sha256']},
                'source_images': sorted({c['source'] for c in cases}), 'tests': tests,
                'actual_alpha2_preflight': dict(alpha, result_path=relative(evidence / 'alpha2-preflight.json'),
                    result_sha256=digest(evidence / 'alpha2-preflight.json')),
                'preflight_matrix': dict(record(AUDIT / 'transition-preflight.json'), path=relative(AUDIT / 'transition-preflight.json'))}
            write(evidence / 'transition.json', transition)
            source_names = set(safety.REQUIRED_SOURCES) | set(summary['source_files']) | {relative(Path(__file__).resolve())}
            source_names |= {relative(AUDIT / leaf) for leaf in (
                'measure_origin.py', 'test_measure_origin.py', 'test_prepare_paths.py',
                'check_module_matrix.py', 'module-matrix-check.json')}
            source_names |= {relative(AUDIT / 'origin-measurements' / profile / leaf)
                             for leaf in ('binding.json', 'matrix.json', 'measurement.log')}
            source_names |= {name for test in tests for name in test['source_files']}
            sources = {name: record(ROOT / name) for name in sorted(source_names)}
            symbols = authorization.symbols_sha256(build / 'ajazz_ak820_vial.map')
            program = {'ihx_sha256': ihx, 'symbols_sha256': symbols, 'schema': report['build_id']}
            dest = ROOT / 'ci/profiles' / profile
            require(args.write_policies, 'Use --write-policies to replace current policy drafts after reviewing preparation inputs')
            write(dest / 'release-safety.json', {'format': 'ak820-release-safety-1',
                'program': {'ihx_sha256': ihx, 'symbols_sha256': symbols, 'configuration': report['configuration']},
                'source_files': sources, 'witnesses': {name: dict(record(evidence / (name + '.json')),
                    path=relative(evidence / (name + '.json'))) for name in ('stack', 'startup', 'irq', 'transition')}})
            receipt = {'format': 'ak820-ci-packing-receipt-1', 'hardware_validated': False,
                'program': program, 'host_files': host_manifest(ROOT),
                'packing': {'physical_usb_opened': False, 'hardware_validated': False,
                    'recovery_byte_equal': pack['recovery_byte_equal'], 'install_modes': ['permanent', 'trial'],
                    'images': {'ak820-vial-trial.bin': pack['trial'],
                        'restore-native.bin': {'size': pack['permanent']['size'], 'sha256': pack['recovery_sha256'],
                            'restores': 'native application/settings from the original recovery backup'}},
                    'permanent': pack['permanent'],
                    'reference_hashes': {'stock': packing['native_reference_sha256'], 'native': pack['recovery_sha256']},
                    'level': 'Offline exact-profile packing using private OEM references; no device operation'}}
            write(dest / 'packing-validation.json', receipt)
            required = set(host_manifest(ROOT)) | set(sources) | set(guide_files()) | {
                '.github/workflows/windows-installer.yml', '.github/workflows/firmware-catalog.yml',
                'tools/ci_checks.py', 'tools/test_keyboard.py', 'tools/build_ci_release.py', 'tools/build_ci_profiles.py',
                'qmk-8051-ak820/dependencies/lufa.json', relative(dest / 'release-safety.json')}
            required |= {relative(evidence / (name + '.json')) for name in ('stack', 'startup', 'irq', 'transition')}
            required |= {relative(evidence / 'alpha2-preflight.json'), relative(AUDIT / 'transition-preflight.json')}
            required |= {relative(AUDIT / name) for name in ('packing-preflight.json', 'historical-catalog.json')}
            required |= {t['log_path'] for t in tests}
            required |= set(configured.test_source_snapshot())
            required |= {'qmk-8051-ak820/' + row['path'].replace('\\', '/') for row in report['sources']
                         if row.get('origin') == 'source' and not row['path'].startswith('.build/')}
            write(dest / 'release-policy.json', {'format': 'ak820-ci-program-policy-1',
                'program': dict(program, keyboard='ajazz/ak820', keymap='vial', sdcc_version='4.6.0'),
                'host_files': host_manifest(ROOT), 'packing_receipt_sha256': digest(dest / 'packing-validation.json'),
                'source_files': {name: record(ROOT / name) for name in sorted(required)}})
            outputs.append({'profile': profile, 'ihx_sha256': ihx, 'runtime_passed': True,
                            'transition_tests_supplied': bool(tests), 'independently_reviewed': False})
    write(AUDIT / 'profile-policy-preparation.json', {'format': 'ak820-caps-word-policy-preparation-1',
        'hardware_validated': False, 'physical_device_commands': 0, 'profiles': outputs,
        'gates': ['Refresh source and test hashes after freeze', 'Complete full exact-image regression',
                  *(['Supply frozen settings test record'] if not tests else []), 'Obtain independent exact-tree policy review',
                  'Commit reviewed inputs before CI assembly']})

def preparation_arguments(parser):
    parser.add_argument('--builds-root', required=True, type=Path,
                        help='Qualified fresh builds in ten profile-named directories')
    parser.add_argument('--profile-build', action='append', default=[], metavar='PROFILE=PATH',
                        help='Explicit qualified build directory for a canonical profile')
    parser.add_argument('--profile-origin', action='append', default=[], metavar='PROFILE=PATH',
                        help='Original source root for a byte-identical copied build; canonical checks run there')
    parser.add_argument('--toolchain', required=True, type=Path)
    parser.add_argument('--oem-reference-dir', required=True, type=Path,
                        help='Private stock-full.bin and native-installed.bin directory')
    parser.add_argument('--private-output', required=True, type=Path,
                        help='New private directory outside the repository for packed ROMs and fixtures')
    parser.add_argument('--historical-catalog', required=True, type=Path,
                        help='Frozen previous catalog; prior exact identities remain source-only')
    parser.add_argument('--source-backups-root', required=True, type=Path,
                        help='Private validated backup directories for every historical source, including alpha2-saved-rom')
    parser.add_argument('--source-rom', action='append', default=[], metavar='NAME=FILE',
                        help='Known saved full ROM; derive a private backup without claiming a live capture')
    parser.add_argument('--source-bundle', action='append', default=[], metavar='NAME=DIR',
                        help='Authenticated historical bundle; derive an explicit offline packed-default fixture')
    historical = parser.add_mutually_exclusive_group()
    historical.add_argument('--historical-builds-root', type=Path,
                        help='Optional retained ten-profile builds for deriving old exact default fixtures')
    historical.add_argument('--historical-bundles-root', type=Path,
                        help='Extracted authenticated previous firmware-bundle profiles directory')
    parser.add_argument('--write-policies', action='store_true',
                        help='Also replace current catalogs and ci/profiles drafts; never writes review approval')


def make_backup(folder, rom, profile):
    """Derive an explicitly offline default fixture; never claims getter capture."""
    import settings_backup as s
    p = s.pack
    folder.mkdir(parents=True, exist_ok=False)
    s.validate_rom(rom, profile)
    nvm = rom[p.NVM_START:p.NVM_END]
    image = s._rom_identity(rom, profile)
    values = s.settings_from_nvm(nvm, s.rgb_wire(nvm[24:32], image=image),
                                 combos=s._combo_capable(profile, image['ihx_sha256']))
    files = {'settings.json': s.canonical(values), 'before-full-rom.bin': rom,
             'saved-nvm.bin': nvm, 'read-log.jsonl': s.canonical({
                 'offline_derived': True, 'physical_device_commands': 0}), '.gitignore': b'*\n'}
    manifest = {'format': s.FORMAT_V2 if image['build_id'] == s.extensions.SCHEMA else s.FORMAT,
        'created_utc': datetime.now(timezone.utc).isoformat(), 'device': s.DEVICE,
        'definition_sha256': profile['definition_sha256'], 'nvm_schema': image['build_id'],
        'source_build_id': image['build_id'], 'source_ihx_sha256': image['ihx_sha256'],
        'code_sha256': image['code_sha256'],
        'counts': {'layers': 6, 'physical_keys': 83, 'assignments': 498, 'encoder_assignments': 12,
                   'macros': 16, 'macro_capacity': 8192},
        'scope': 'Offline-derived full-ROM fixture; no device capture or getter validation',
        'files': {name: s._record(data) for name, data in files.items()}}
    for name, data in {**files, 'manifest.json': s.canonical(manifest)}.items():
        path = folder / name
        path.write_bytes(data)
        path.chmod(0o600)
    return s.validate_backup(folder, profile)


def prepare(args):
    """Remeasure every image, pack privately, and exercise explicit forward plans."""
    import copy
    import os
    sys.path.insert(0, str(ROOT / 'tools/installer'))
    import settings_backup as s
    import firmware_matrix as matrix
    import build_ci_release as ci
    p = s.pack
    os.umask(0o077)
    args.builds_root = args.builds_root.resolve()
    args.build_overrides = {}
    for item in args.profile_build:
        name, separator, path = item.partition('=')
        require(separator and path and name in matrix.candidate_names() and
                name not in args.build_overrides, 'Invalid or duplicate profile build override')
        args.build_overrides[name] = Path(path)
    args.profile_origins = {}
    for item in args.profile_origin:
        name, separator, path = item.partition('=')
        require(separator and path and name in matrix.candidate_names() and
                name not in args.profile_origins, 'Invalid or duplicate profile origin')
        args.profile_origins[name] = Path(path)
    private = args.private_output.resolve()
    require(not private.is_relative_to(ROOT), 'Private output must be outside the repository')
    require(not private.exists(), 'Private output must be a new directory')
    require(not args.write_policies or args.settings_run is not None,
            '--write-policies requires a frozen successful --settings-run record')
    stock = (args.oem_reference_dir / 'stock-full.bin').read_bytes()
    native = (args.oem_reference_dir / 'native-installed.bin').read_bytes()
    p.validate_native(stock, stock, native)
    old = json.loads(args.historical_catalog.read_text())
    # Validate old typed contracts without reinterpreting them as the new images.
    source_catalog = copy.deepcopy(old)
    source_catalog['historical_profiles'] = source_catalog.get('historical_profiles', []) + source_catalog['profiles']
    source_catalog['profiles'] = []
    source_catalog['settings_transitions'] = []
    s._catalog_images(source_catalog)
    require(tuple(row['profile'] for row in old['profiles']) == matrix.candidate_names(),
            'Historical catalog must retain the previous ten-profile catalog')
    private.mkdir(mode=0o700)
    (private / '.gitignore').write_text('*\n')
    rows, packs, profiles = [], [], {}
    for name in matrix.candidate_names():
        build = profile_build(args, name)
        require(build.is_dir() and not build.is_symlink(), 'Missing or unsafe build: ' + name)
        import measure_origin
        row = measure_origin.measured_row(build, args.profile_origins.get(name, ROOT), args.toolchain,
            args.oem_reference_dir / 'stock-full.bin', private / 'measurements' / name)
        evidence = private / 'measurements' / name
        require({path.name for path in evidence.iterdir()} == {'binding.json', 'matrix.json', 'measurement.log'},
                'Unexpected original-root measurement output')
        shutil.copytree(evidence, AUDIT / 'origin-measurements' / name, dirs_exist_ok=True)
        require(row['profile'] == name and row['runtime_status'] == 'exact-image-pass' and
                row['offline_tests_status'] == 'exact-image-pass', 'Unqualified exact image: ' + name)
        row['reproducible_identity'] = ci.reproducible_identity(build, row['identity'])
        rows.append(row)
        report = json.loads((build / 'build-report.json').read_text())
        code, symbols = p.read_ihex(build / 'ajazz_ak820_vial.ihx'), p.read_symbols(build / 'ajazz_ak820_vial.map')
        nvm, _ = p.migrate(stock, code, symbols)
        if report['build_id'] != p.BUILD_ID:
            nvm, _ = p.migrate_vial_nvm(nvm, p.BUILD_ID, target_build_id=report['build_id'])
        folder = private / 'packed' / name
        folder.mkdir(parents=True)
        packed = {}
        for leaf, trial in (('ak820-vial-permanent.bin', False), ('ak820-vial-trial.bin', True)):
            payload = p.pack(code, symbols, stock, nvm, trial, target_build_id=report['build_id'])
            (folder / leaf).write_bytes(payload)
            packed['trial' if trial else 'permanent'] = p.verify_payload(payload, target_build_id=report['build_id'])
        recovery = stock[p.APP_START:p.APP_END]
        (folder / 'restore-native.bin').write_bytes(recovery)
        permanent = (folder / 'ak820-vial-permanent.bin').read_bytes()
        code_sha = p.digest(permanent[:p.CODE_END-p.APP_START])
        require(code_sha == row['settings_identity']['code_sha256'], 'Packed CODE identity differs')
        packs.append({'profile': name, 'build': row['identity'], 'schema': report['build_id'],
            'settings_code_sha256': code_sha, **packed, 'recovery_byte_equal': True,
            'recovery_sha256': p.digest(recovery), 'hardware_validated': False, 'physical_device_commands': 0})
    catalog = matrix.matrix({row['profile']: row for row in rows})
    catalog['historical_sources'] = copy.deepcopy(old.get('historical_sources', []))
    catalog['historical_profiles'] = copy.deepcopy(old.get('historical_profiles', []) + old['profiles'])
    all_sources = {row['settings_identity']['ihx_sha256'] for row in rows + catalog['historical_profiles']}
    all_sources |= {row['ihx_sha256'] for row in catalog['historical_sources']}
    catalog['settings_transitions'] = [{'source': source, 'target': row['identity']['ihx_sha256']}
        for source in sorted(all_sources) for row in rows]
    s._catalog_images(catalog)
    # No historical target edges: old images cannot consume Caps Word combo actions.
    def load_build(build, name, contracts):
        bundle = private / 'bundles' / name
        for part in ('firmware', 'reports', 'reference'):
            (bundle / part).mkdir(parents=True, exist_ok=True)
        for source, dest in ((build / 'ajazz_ak820_vial.ihx', 'firmware/application.ihx'),
            (build / 'ajazz_ak820_vial.map', 'firmware/application.map'),
            (build / 'build-report.json', 'reports/build-report.json'),
            (ROOT / 'qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json', 'reference/vial.json')):
            shutil.copyfile(source, bundle / dest)
        return s.load_profile(bundle, stock, trusted_catalog=contracts)

    for name in matrix.candidate_names():
        profiles[name] = load_build(profile_build(args, name), name, catalog)
    first = profiles[matrix.candidate_names()[0]]
    backups = {}
    for folder in sorted(args.source_backups_root.iterdir()):
        if folder.is_dir() and (folder / 'manifest.json').is_file():
            backups[folder.name] = s.validate_backup(folder, first)
    for argument in args.source_rom:
        label, separator, filename = argument.partition('=')
        require(separator and label and label not in ('.', '..') and
                all(char.isalnum() or char in '-_' for char in label), 'Invalid source ROM label')
        require(label not in backups, 'Duplicate source fixture label: ' + label)
        backups[label] = make_backup(private / 'backups' / label, Path(filename).read_bytes(), first)
    for argument in args.source_bundle:
        label, separator, filename = argument.partition('=')
        require(separator and label and label not in ('.', '..') and
                all(char.isalnum() or char in '-_' for char in label), 'Invalid source bundle label')
        require(label not in backups, 'Duplicate source fixture label: ' + label)
        profile = s.load_profile(Path(filename), stock)
        require(profile['ihx_sha256'] in all_sources, 'Historical bundle image absent from retained catalog')
        rom = bytearray(stock)
        rom[p.APP_START:p.APP_END] = profile['payload']
        backups[label] = make_backup(private / 'backups' / label, bytes(rom), first)
    if args.historical_builds_root or args.historical_bundles_root:
        for name in matrix.candidate_names():
            profile = (load_build(args.historical_builds_root / name, 'historical-' + name, source_catalog)
                       if args.historical_builds_root else
                       s.load_profile(args.historical_bundles_root / name, stock, trusted_catalog=source_catalog))
            expected = next(row['settings_identity'] for row in old['profiles'] if row['profile'] == name)
            require(profile['ihx_sha256'] == expected['ihx_sha256'] and
                    profile['code_sha256'] == expected['code_sha256'], 'Historical build identity differs: ' + name)
            rom = bytearray(stock)
            rom[p.APP_START:p.APP_END] = profile['payload']
            label = 'historical-' + name
            require(label not in backups, 'Duplicate source fixture label: ' + label)
            make_backup(private / 'backups' / label, bytes(rom), profile)
            backups[label] = s.validate_backup(private / 'backups' / label, first)
    for name, profile in profiles.items():
        rom = bytearray(stock)
        rom[p.APP_START:p.APP_END] = profile['payload']
        label = 'fresh-' + name
        require(label not in backups, 'Duplicate source fixture label: ' + label)
        backups[label] = make_backup(private / 'backups' / label, bytes(rom), profile)
    require('alpha2-saved-rom' in backups, 'Missing exact alpha2-saved-rom source backup')
    require({b['source_identity'][0] for b in backups.values()} == all_sources,
            'Historical backups do not cover exactly every retained catalog image')
    cases = []
    for name, profile in profiles.items():
        for label, backup in backups.items():
            plan = s.plan_restore(backup, profile)
            cases.append({'source': backup['source_identity'][0], 'target': profile['ihx_sha256'],
                'source_case': label, 'target_profile': name, 'passed': True, 'offline_only': True,
                'physical_device_commands': 0, 'key_count': plan['key_count'],
                'encoder_count': plan['encoder_count'], 'combo_count': len(plan['combo_entries'] or []),
                'source_scope': backup['manifest'].get('scope', 'Validated saved backup; capture provenance not recorded'),
                'backup_manifest_sha256': backup['identity']})
    action_cases = []
    macro_layer_cases = []
    for name, profile in profiles.items():
        rom = bytearray(stock)
        rom[p.APP_START:p.APP_END] = profile['payload']
        at = p.NVM_START + s.DeviceAPI.COMBO_OFFSET
        action = bytes.fromhex('0400160000000000737c')
        rom[at:at+10] = s.DeviceAPI.stored_combo(action)
        backup = make_backup(private / 'backups' / ('caps-word-' + name), bytes(rom), profile)
        for target_name, target in profiles.items():
            plan = s.plan_restore(backup, target)
            require(plan['combo_entries'][0] == action.hex(), 'Caps Word Combo changed during planning')
            action_cases.append({'source_profile': name, 'target_profile': target_name,
                                 'source_ihx_sha256': profile['ihx_sha256'],
                                 'source_code_sha256': profile['code_sha256'],
                                 'target_ihx_sha256': target['ihx_sha256'],
                                 'target_code_sha256': target['code_sha256'],
                                 'passed': True, 'combo_hex': action.hex()})
        rom = bytearray(stock)
        rom[p.APP_START:p.APP_END] = profile['payload']
        at = p.NVM_START + s.DeviceAPI.key_offset(0, s.PHYSICAL[0])
        rom[at:at+2] = (0x43F0).to_bytes(2, 'big')
        stream = b'x' + bytes(16)
        at = p.NVM_START + p.MACRO_ADDR
        rom[at:at+len(stream)] = stream
        at = p.NVM_START + p.MACRO_BUSY_ADDR
        rom[at] = 0
        rom[at+1:at+3] = len(stream).to_bytes(2, 'little')
        backup = make_backup(private / 'backups' / ('macro-layer-' + name), bytes(rom), profile)
        require(any(key['keycode'] == 0x43F0 for key in backup['settings']['keys']),
                'Macro Layer-Tap fixture key was lost')
        for target_name, target in profiles.items():
            plan = s.plan_restore(backup, target)
            require(b''.join(chunk for offset, chunk in plan['macro_chunks']) == stream,
                    'Tap macro bytes changed during planning')
            require(s.image_keycode_supported(0x43F0,
                    target['compatible_images'][target['ihx_sha256']], context='matrix'),
                    'Target rejected macro Layer-Tap key')
            macro_layer_cases.append({'source_profile': name, 'target_profile': target_name,
                'source_ihx_sha256': profile['ihx_sha256'], 'source_code_sha256': profile['code_sha256'],
                'target_ihx_sha256': target['ihx_sha256'], 'target_code_sha256': target['code_sha256'],
                'matrix_keycode': '0x43f0', 'macro_data_sha256': p.digest(stream), 'passed': True})
    frozen = AUDIT / 'historical-catalog.json'
    if frozen.exists():
        require(json.loads(frozen.read_text()) == old, 'Frozen historical catalog differs from supplied input')
    else:
        write(frozen, old)
    write(AUDIT / 'settings-catalog-draft.json', catalog)
    write(AUDIT / 'packing-preflight.json', {'format': 'ak820-caps-word-packing-preflight-1',
        'offline_only': True, 'physical_device_commands': 0, 'hardware_validated': False,
        'native_reference_sha256': p.digest(stock), 'profiles': packs})
    write(AUDIT / 'transition-preflight.json', {'format': 'ak820-settings-transition-matrix-1',
        'offline_only': True, 'physical_device_commands': 0, 'hardware_validated': False,
        'sources_per_target': len(backups), 'cases': cases,
        'caps_word_combo_cases': action_cases,
        'macro_layer_tap_cases': macro_layer_cases,
        'limitations': ['Default packed fixtures and supplied offline backups; no physical restore proof.',
                        'No transition to historical images is authorized.']})
    if args.write_policies:
        for target in ('tools/installer/settings-catalog.json', 'web/firmware-matrix.json'):
            write(ROOT / target, catalog)


if __name__ == '__main__':
    main()
