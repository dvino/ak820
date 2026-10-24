#!/usr/bin/env python3
"""Offline exact-build development catalog; grants no device permissions."""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path
import sys
import configure_firmware as configured

FORMAT = 'ak820-development-capability-catalog-1'
MODEL = 'ajazz/ak820'


def code_identity(code):
    """Bind both complete linked CODE windows, using the packer's zero fill."""
    configured.require(bool(code), 'Empty CODE image')
    for address, value in code.items():
        configured.require(type(address) is int and
                           any(lo <= address < hi for lo, hi in configured.WINDOWS) and
                           type(value) is int and 0 <= value <= 255, 'Invalid CODE record')
    records = bytearray(b'ak820-code-windows-zero-v1\0')
    for lo, hi in configured.WINDOWS:
        records.extend(lo.to_bytes(4, 'big'))
        records.extend(hi.to_bytes(4, 'big'))
        records.extend(code.get(address, 0) for address in range(lo, hi))
    return {'algorithm': 'sha256-code-windows-zero-v1',
            'sha256': hashlib.sha256(records).hexdigest(),
            'ranges': [{'start': lo, 'end_exclusive': hi} for lo, hi in configured.WINDOWS],
            'fill_byte': 0, 'covered_bytes': sum(hi - lo for lo, hi in configured.WINDOWS)}


def validate_base_logs(build):
    report = configured.load_json(build / 'qualification.json')
    totals = {'run': 0, 'skipped': 0}
    seen = set()
    for index, row in enumerate(report.get('tests', [])):
        path = Path(row.get('log', '')).resolve()
        configured.require(path.is_relative_to(build) and
                           path.parent.name.startswith('qualification-logs-') and
                           path.name == f'{index:02d}.txt' and path not in seen,
                           'Missing, escaping or duplicate base suite log')
        seen.add(path)
        configured.require(row.get('exit_code') == 0 and
                           configured.sha(path) == row.get('log_sha256'),
                           'Base suite log changed or suite failed')
        counts = configured.unittest_counts(path.read_text())
        configured.require(counts == row.get('unit_tests') and counts['skipped'] == 0,
                           'Base suite log counts differ or tests skipped')
        for key in totals:
            totals[key] += counts[key]
    configured.require(seen and totals == report.get('unit_tests'),
                       'Base suite aggregate counts differ')


def runtime_proof(build, inspected, toolchain):
    paths = {'foreground': build / 'runtime-stack.json',
             'startup': build / 'runtime-safety/startup.json',
             'irq': build / 'runtime-safety/irq/results.json'}
    proof = configured.combine_runtime_safety(
        *(configured.load_json(paths[key]) for key in ('foreground', 'startup', 'irq')),
        inspected['identity'], inspected['resources']['internal_ram'],
        configured.runtime_source_snapshot())
    proof['reports'] = {key: {'path': path.relative_to(build).as_posix(),
                              'sha256': configured.sha(path)} for key, path in paths.items()}
    proof['logs'] = {key: configured.sha(build / 'runtime-safety' / (key + '.log'))
                     for key in ('startup', 'irq')}
    proof['simulator_sha256'] = configured.sha(toolchain / 'bin/s51')
    configured.require(configured.load_json(build / 'runtime-safety/summary.json') == proof,
                       'Runtime summary differs from component evidence')
    configured.apply_runtime_safety(inspected, proof)
    return proof


def fixed_limits(build):
    path = configured.QMK / 'keyboards/ajazz/ak820/config.h'
    report = configured.load_json(build / 'build-report.json')
    matches = [row for row in report['sources'] if row.get('origin') == 'source' and
               row.get('path', '').replace('\\', '/') == 'keyboards/ajazz/ak820/config.h']
    configured.require(len(matches) == 1 and matches[0].get('sha256') == configured.sha(path),
                       'Fixed limits are not bound to compiled source')
    fields = {'layers': 'DYNAMIC_KEYMAP_LAYER_COUNT', 'macros': 'DYNAMIC_KEYMAP_MACRO_COUNT',
              'macro_bytes': 'DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE', 'combos': 'VIAL_COMBO_ENTRIES',
              'encoders': 'NUM_ENCODERS', 'rgb_leds': 'RGB_MATRIX_LED_COUNT',
              'rgb_maximum_brightness': 'RGB_MATRIX_MAXIMUM_BRIGHTNESS'}
    result = {}
    for key, define in fields.items():
        values = re.findall(r'^#define\s+' + define + r'\s+(0x[0-9a-fA-F]+|[0-9]+)\s*$',
                            path.read_text(), re.M)
        configured.require(len(values) == 1, 'Unknown fixed limit: ' + define)
        result[key] = int(values[0], 0)
    return result


def inspect_entry(build, toolchain):
    build = Path(build).resolve()
    inspected = configured.inspect(build, toolchain)
    stored = configured.load_json(build / 'configuration-report.json')
    runtime_proof(build, inspected, toolchain)
    identity = inspected['identity']
    qualification = configured.validate_tests(build / 'qualification.json', identity)
    validate_base_logs(build)
    profile_path = build / 'profile-tests/results.json'
    configured.validate_profile_tests(configured.load_json(profile_path),
        inspected['configuration']['profile'], identity, build, toolchain)
    inspected.update(offline_tests_passed=True, qualification=qualification,
        profile_tests={'sha256': configured.sha(profile_path),
                       'suites': [row[0] for row in configured.profile_test_plan(
                           inspected['configuration']['profile'], build, toolchain)],
                       'hardware_validated': False})
    # Compare independently reconstructed fields; source Git metadata is descriptive.
    for key in ('format', 'configuration', 'identity', 'short_calls', 'resources',
                'runtime_analysis', 'qualification', 'offline_tests_passed',
                'hardware_validated', 'physical_device_commands', 'release_approved',
                'release_blockers', 'settings_compatibility'):
        configured.require(stored.get(key) == inspected[key], 'Configuration report differs: ' + key)
    configured.require(stored.get('profile_tests', {}).get('sha256') == configured.sha(profile_path) and
                       stored['profile_tests'].get('suites') == inspected['profile_tests']['suites'],
                       'Configuration profile evidence differs')
    code = configured.diagnostic_build(build / 'ajazz_ak820_vial.ihx',
        build / 'ajazz_ak820_vial.map', build / 'build-report.json')
    configuration = inspected['configuration']
    result = {'model': MODEL, 'profile': configuration['profile'],
              'settings_schema': configuration['nvm_schema'],
              'code_identity': code_identity(code), 'build_identity': identity,
              'features': sorted(configuration['base_features'] + configuration['optional_features']),
              'timing_ms': configuration['timing_ms'], 'fixed_limits': fixed_limits(build),
              'resources': inspected['resources'],
              'runtime_qmk_settings': configuration['runtime_qmk_settings'],
              'evidence_sha256': {'configuration': configured.sha(build / 'configuration-report.json'),
                  'base_suites': qualification['sha256'], 'supplemental_suites': configured.sha(profile_path),
                  'runtime': configured.sha(build / 'runtime-safety/summary.json')},
              'status': 'development', 'project_verified': True,
              'release_approved': False, 'hardware_validated': False,
              'compatible_transitions': [], 'settings_writes_authorized': False,
              'flashing_authorized': False}
    configured.require(configured.inspect(build, toolchain)['identity'] == identity,
                       'Build changed during catalog verification')
    return result


def catalog(builds, toolchain):
    toolchain = configured.validate_tools(toolchain)
    entries = [inspect_entry(build, toolchain) for build in builds]
    configured.require(bool(entries), 'No builds supplied')
    fingerprints = [entry['code_identity']['sha256'] for entry in entries]
    configured.require(len(fingerprints) == len(set(fingerprints)), 'Duplicate CODE image identity')
    return {'format': FORMAT, 'status': 'development-only',
            'release_approved': False, 'hardware_validated': False,
            'settings_writes_authorized': False, 'flashing_authorized': False,
            'images': sorted(entries, key=lambda entry: entry['code_identity']['sha256'])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, action='append', required=True)
    parser.add_argument('--toolchain', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    result = configured.canonical(catalog(args.build_dir, args.toolchain))
    args.output.write_bytes(result)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
