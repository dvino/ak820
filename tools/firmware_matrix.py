#!/usr/bin/env python3
"""Exact module coverage and resource matrix for curated AK820 candidates.

Only RELEASE_PROFILES are selectable. Each supplied build is inspected against
its actual artifacts and current source. Memory fit, exact-image runtime proof,
release approval and installation eligibility remain separate decisions.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(QMK / 'util'))
import ak820_profiles as profiles

FORMAT = 'ak820-firmware-matrix-1'


def candidate_names():
    names = tuple(profiles.RELEASE_PROFILES)
    if not names or len(names) != len(set(names)) or set(names) - set(profiles.PROFILES):
        raise ValueError('Invalid curated profile catalog')
    return names


def resolve(features, names=None):
    """Return candidates containing every requested module, in preference order.

    Exact matches come first, then the fewest additional modules. Catalog order
    breaks ties, so adding a legacy development profile cannot change selection.
    """
    if len(features) != len(set(features)):
        raise ValueError('Repeated feature selection')
    unknown = set(features) - set(profiles.SWITCHES)
    if unknown:
        raise ValueError('Unknown modules: ' + ', '.join(sorted(unknown)))
    names = candidate_names() if names is None else tuple(names)
    requested = set(features)
    matches = [name for name in names if requested <= set(profiles.PROFILES[name])]
    return sorted(matches, key=lambda name: (len(set(profiles.PROFILES[name]) - requested), names.index(name)))


def default_row(name):
    configuration = profiles.configuration(name)
    return {'id': name, 'profile': name, 'configuration': configuration,
            'build_recipe': {'script': 'util/build_ak820.py', 'profile': name,
                             'make_options': configuration['make_options'],
                             'memory_windows': {'low_code': [0x28a0, 0x3000], 'main_code': [0x3027, 0xc700], 'xram': [0x400, 0x1000]},
                             'short_calls': True},
            'settings_identity': None, 'settings_status': 'not-packaged',
            'capabilities': {'optional_modules': {feature: feature in configuration['optional_features'] for feature in profiles.SWITCHES},
                             'dynamic_entries': {'combos': 8,
                                                 'tap_dance': 8 if 'tap-dance' in configuration['optional_features'] else 0,
                                                 'key_overrides': 8 if 'key-overrides' in configuration['optional_features'] else 0},
                             'runtime_qmk_settings_ids': configuration['runtime_qmk_settings']},
            'optional_features': configuration['optional_features'],
            'measurement_status': 'not-measured', 'resources': None,
            'runtime_status': 'not-proven', 'offline_tests_status': 'not-proven',
            'release_approved': False, 'installable': False}


def settings_identity(build, inspected, native_reference):
    """Derive permanent packed CODE identity using a validated local OEM ROM.

    The native erase helper remains part of CODE even for permanent images.
    Hashing sparse linked windows would omit that helper and loader callbacks.
    Native settings are neither exported nor used; a fresh empty NVM is enough
    because NVM starts at CODE_END and cannot affect the contiguous CODE hash.
    """
    import pack_ak820 as pack
    sys.path.insert(0, str(ROOT / 'tools/installer'))
    import settings_backup as settings
    native = Path(native_reference).read_bytes()
    pack.validate_native(native)
    schema = inspected['configuration']['nvm_schema']
    nvm = pack.empty_nvm()
    if schema != pack.BUILD_ID:
        nvm, _ = pack.migrate_vial_nvm(nvm, pack.BUILD_ID, target_build_id=schema)
    code = pack.read_ihex(build / 'ajazz_ak820_vial.ihx')
    symbols = pack.read_symbols(build / 'ajazz_ak820_vial.map')
    payload = pack.pack(code, symbols, native, nvm, False, target_build_id=schema)
    pack.verify_payload(payload, target_build_id=schema)
    definition = json.loads((QMK / 'keyboards/ajazz/ak820/keymaps/vial/vial.json').read_text())
    return settings.catalog_settings_identity(
        inspected['configuration'], inspected['identity']['ihx_sha256'],
        pack.digest(payload[:pack.CODE_END - pack.APP_START]),
        pack.digest(settings.canonical(definition)))


def measured_row(build, toolchain, native_reference=None):
    """Revalidate linked evidence; a saved report alone never supplies sizes."""
    import configure_firmware as configured
    build = Path(build).resolve()
    fresh = configured.inspect(build, toolchain)
    name = fresh['configuration']['profile']
    if name not in candidate_names():
        raise ValueError('Build is outside the curated catalog: ' + name)
    row = default_row(name)
    row.update(measurement_status='linked-memory-pass', resources=fresh['resources'],
               identity=fresh['identity'], short_calls=fresh['short_calls'])
    row['build_recipe']['short_calls'] = bool(fresh['short_calls'])
    if native_reference is not None:
        row['settings_identity'] = settings_identity(build, fresh, native_reference)
        row['settings_status'] = 'exact-image-contract'
    # Runtime summaries must bind the current image and checker sources, and
    # every component file must still have its recorded digest. Recombine the
    # individual witnesses rather than trusting a saved passed boolean.
    summary_path = build / 'runtime-safety/summary.json'
    if summary_path.exists():
        summary = configured.load_json(summary_path)
        components = {}
        for kind in ('foreground', 'startup', 'irq'):
            record = summary.get('reports', {}).get(kind, {})
            path = (build / record.get('path', '')).resolve()
            if not path.is_relative_to(build) or not path.is_file() or configured.sha(path) != record.get('sha256'):
                raise ValueError('Missing or changed runtime component: ' + kind)
            components[kind] = configured.load_json(path)
        proof = configured.combine_runtime_safety(
            *(components[kind] for kind in ('foreground', 'startup', 'irq')),
            fresh['identity'], fresh['resources']['internal_ram'], configured.runtime_source_snapshot())
        configured.apply_runtime_safety(fresh, proof)
        if any(summary.get(key) != proof.get(key) for key in proof):
            raise ValueError('Runtime summary differs from its component witnesses')
        row['runtime_status'] = 'exact-image-pass'
        row['resources'] = fresh['resources']
        row['runtime_evidence_sha256'] = configured.sha(summary_path)
    report = build / 'configuration-report.json'
    if report.exists():
        saved = configured.load_json(report)
        if saved.get('identity') != fresh['identity']:
            raise ValueError('Configuration report belongs to a different image')
        if saved.get('offline_tests_passed') is True:
            configured.validate_tests(build / 'qualification.json', fresh['identity'])
            profile_path = build / 'profile-tests/results.json'
            if not profile_path.is_file() or saved.get('profile_tests', {}).get('sha256') != configured.sha(profile_path):
                raise ValueError('Profile test report is missing or changed')
            configured.validate_profile_tests(configured.load_json(profile_path), name, fresh['identity'], build, toolchain)
            if row['runtime_status'] != 'exact-image-pass':
                raise ValueError('Offline suite success lacks current runtime proof')
            row['offline_tests_status'] = 'exact-image-pass'
    # This tool describes build candidates. Existing release/installer gates must
    # independently approve the exact image and its settings transition.
    return row


def matrix(measurements=None):
    measurements = {} if measurements is None else measurements
    names = candidate_names()
    if set(measurements) - set(names):
        raise ValueError('Measurement is outside the curated catalog')
    rows = []
    for name in names:
        row = copy.deepcopy(measurements.get(name, default_row(name)))
        if row.get('configuration') != profiles.configuration(name):
            raise ValueError('Measured configuration differs from catalog: ' + name)
        rows.append(row)
    modules = [{'feature': feature, 'make_switch': switch,
                'profiles': [name for name in names if feature in profiles.PROFILES[name]]}
               for feature, switch in profiles.SWITCHES.items()]
    uncovered = [row['feature'] for row in modules if not row['profiles']]
    pairs = []
    features = tuple(profiles.SWITCHES)
    for index, left in enumerate(features):
        for right in features[index + 1:]:
            matches = [name for name in names if {left, right} <= set(profiles.PROFILES[name])]
            pairs.append({'features': [left, right], 'profiles': matches,
                          'status': 'catalog-supported' if matches else 'no-catalog-profile',
                          'disabled_reason': None if matches else 'no_catalog_profile'})
    return {'format': FORMAT, 'catalog_version': 1, 'default_profile': profiles.DEFAULT_PROFILE,
            'profiles': rows, 'modules': modules, 'feature_pairs': pairs,
            'compatibility_scope': 'Membership in curated profiles; missing pairs do not prove hardware or source incompatibility.',
            'base_features': list(profiles.BASE_FEATURES), 'uncovered_modules': uncovered,
            'complete_module_coverage': not uncovered,
            'cost_policy': 'Exact linked measurements only; missing sizes are null.',
            'selection_policy': 'Curated candidates containing all requested modules; fewest extras first.',
            'settings_transitions': [],
            'release_policy': 'Build and runtime checks do not grant release or installation approval.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--build-dir', type=Path, action='append', default=[])
    parser.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    parser.add_argument('--resolve', nargs='*', metavar='MODULE')
    parser.add_argument('--native-reference', type=Path, help='Validated full OEM ROM used offline to derive permanent packed CODE hashes; never copied to output')
    args = parser.parse_args(argv)
    if args.output is None and args.resolve is None:
        parser.error('Select --output or --resolve')
    measurements = {}
    for build in args.build_dir:
        row = measured_row(build, args.toolchain, args.native_reference)
        if row['profile'] in measurements:
            raise ValueError('Multiple images for one profile require separate matrices: ' + row['profile'])
        measurements[row['profile']] = row
    result = matrix(measurements)
    if args.resolve is not None:
        matches = resolve(args.resolve)
        result['selection'] = {'requested_features': args.resolve, 'matching_profiles': matches,
                               'selected_profile': matches[0] if matches else None,
                               'status': 'candidate-found' if matches else 'no-curated-candidate',
                               'disabled_reason': None if matches else 'no_catalog_profile'}
    if args.output is not None:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result['selection'] if args.resolve is not None else
                     {'profiles': len(result['profiles']), 'complete_module_coverage': result['complete_module_coverage']}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
