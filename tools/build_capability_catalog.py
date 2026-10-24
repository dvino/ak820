#!/usr/bin/env python3
"""Offline exact-build development catalog; grants no device permissions."""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path
import sys
import configure_firmware as configured
import ak820_extension_settings as extensions

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
              'tap_dance': 'VIAL_TAP_DANCE_ENTRIES', 'key_overrides': 'VIAL_KEY_OVERRIDE_ENTRIES',
              'encoders': 'NUM_ENCODERS', 'rgb_leds': 'RGB_MATRIX_LED_COUNT',
              'rgb_maximum_brightness': 'RGB_MATRIX_MAXIMUM_BRIGHTNESS'}
    result = {}
    for key, define in fields.items():
        values = re.findall(r'^#define\s+' + define + r'\s+(0x[0-9a-fA-F]+|[0-9]+)\s*$',
                            path.read_text(), re.M)
        configured.require(len(values) == 1, 'Unknown fixed limit: ' + define)
        result[key] = int(values[0], 0)
    return result


def module_contract(configuration, limits):
    """Describe enabled consumers separately from dormant schema03 storage.

    This is descriptive metadata only. Entry qualification is still performed
    by inspect_entry's exact-image evidence pipeline.
    """
    configured.profiles.validate_configuration(configuration)
    enabled = set(configuration['optional_features'])
    schema03 = configuration['nvm_schema'] == extensions.SCHEMA
    modules = {}
    for kind, feature, define in (('tap_dance', 'tap-dance', 'tap_dance'),
                                 ('key_overrides', 'key-overrides', 'key_overrides')):
        count = limits[define] if schema03 else 0
        configured.require(count == (8 if schema03 else 0), 'Unknown typed module capacity')
        modules[kind] = {'enabled': feature in enabled,
            'stored_entries': count, 'enabled_entries': count if feature in enabled else 0,
            'entry_bytes': 10, 'codec': 'ak820_extension_settings.validate_entry', 'entry_offsets': [extensions.slot_offset(kind,i) for i in range(count)],
            'wire_get_operation': 1 if kind == 'tap_dance' else 5,
            'wire_set_operation': 2 if kind == 'tap_dance' else 6}
    names = {1: ('grave_escape_flags', ['grave-escape']),
             2: ('combo_term_ms', ['two-key-combos']),
             4: ('auto_shift_timeout_ms', ['compact-auto-shift']),
             7: ('tapping_term_ms', ['compact-mod-tap','compact-layer-tap','space-cadet']),
             18: ('tap_code_delay_ms', ['tap_code','tap_code16']),
             19: ('caps_lock_delay_ms', ['tap_code','tap_code16'])}
    qsids = configuration['runtime_qmk_settings']
    settings = []
    if schema03:
        for qsid, (offset,width,low,high,default) in sorted(extensions.FIELDS.items()):
            name, consumers = names[qsid]
            settings.append({'qsid': qsid, 'name': name, 'stored': True,
                'enabled': qsid in qsids, 'offset': extensions.SETTINGS_ADDR+offset,
                'width_bytes': width, 'encoding': 'uint8' if width == 1 else 'uint16-le',
                'minimum': low, 'maximum': high, 'default': default,
                'consumers': consumers if qsid in qsids else [],
                'consumer_key_filter': 'caps-lock' if qsid == 19 else ('except-caps-lock' if qsid == 18 else None)})
    modules['qmk_settings'] = {'enabled': 'qmk-settings' in enabled,
        'stored_record_bytes': 24 if schema03 else 0,
        'record_offset': extensions.SETTINGS_ADDR if schema03 else None,
        'enabled_qsids': list(qsids), 'fields': settings,
        'wire_commands': {'query': 9, 'get': 10, 'set': 11, 'reset': 12}}
    return {'format': 'ak820-module-storage-contract-1', 'schema': configuration['nvm_schema'],
        'address_space': 'NVM-relative', 'modules': modules,
        'migration': {'explicit_target_required': schema03,
            'accepted_source_schemas': [0x082001,0x082002,extensions.SCHEMA] if schema03 else [0x082001,0x082002],
            'schema03_downgrade_supported': False,
            'preserves': ['source-keymap-layers','source-encoder-map','schema02-nonempty-combos','published-macros'],
            'schema01_new_layers': 'transparent',
            'macro_capacity_check_required': True},
        'restore': {'backup_format': 'ak820-settings-backup-2' if schema03 else 'ak820-settings-backup-1',
            'exact_reviewed_image_required': True,
            'inactive_data': 'preserve; reject differences before any write',
            'legacy_target_extensions': 'require empty tables and default settings',
            'write_authorization_granted': False, 'failure_action': 'stop-without-retry'},
        'limits': {'tap_dance': {'maximum_waiting_gestures': 1, 'maximum_gesture_presses': 2,
            'term_zero_default_ms': 200, 'explicit_term_ms': [1,32767],
            'physical_sources_only': True, 'special_action_outputs': False},
            'key_overrides': {'maximum_captured_triggers': 1, 'first_matching_row_wins': True,
                'layer_mask': [1,63], 'runtime_enablement_persisted': False,
                'callbacks': False},
            'qmk_settings': {'delays_apply_to': ['tap_code','tap_code16'],
                'delays_do_not_apply_to': ['compact-tap-hold','space-cadet','tap-dance','vial-macro-down-up'],
                'tap_dance_term_uses_qsid7': False}},
        'physical_behavior_verified': False, 'power_loss_persistence_verified': False}


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
    limits = fixed_limits(build)
    result = {'model': MODEL, 'profile': configuration['profile'],
              'settings_schema': configuration['nvm_schema'],
              'code_identity': code_identity(code), 'build_identity': identity,
              'features': sorted(configuration['base_features'] + configuration['optional_features']),
              'timing_ms': configuration['timing_ms'], 'fixed_limits': limits,
              'module_storage': module_contract(configuration, limits),
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
