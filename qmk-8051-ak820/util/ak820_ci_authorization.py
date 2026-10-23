"""Offline consistency gates for CI reproduction of a reviewed program.

Hashes bind evidence; they are not signatures and cannot establish reviewer
independence. These checks grant no permission to access hardware.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import pack_ak820 as pack

CI_EXTRA_FILES = frozenset(('reviews/program-policy.json', 'reviews/program-review.md',
                            'reports/build-attestation.json', 'reports/qualification.json'))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def symbols_sha256(mapfile: Path) -> str:
    symbols = pack.read_symbols(mapfile)
    if not symbols:
        raise ValueError('MAP has no packing symbols')
    return digest(json.dumps(symbols, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _record(data: bytes, format: str) -> dict:
    records = []
    for block in re.findall(r'^```json\s*\n(.*?)^```\s*$', data.decode('utf-8'), re.M | re.S):
        item = json.loads(block)
        if isinstance(item, dict) and item.get('format') == format:
            records.append(item)
    require(len(records) == 1, 'Expected one ' + format + ' record')
    return records[0]


def validate_policy(policy: dict, host_files: dict, receipt_bytes: bytes,
                    program_review_bytes: bytes) -> None:
    require(policy.get('format') == 'ak820-ci-program-policy-1', 'Unknown program policy')
    program = policy.get('program', {})
    require(program.get('keyboard') == 'ajazz/ak820' and program.get('keymap') == 'vial'
            and program.get('sdcc_version') == '4.6.0' and program.get('schema') == pack.BUILD_ID,
            'Unsupported policy target or schema')
    for field in ('ihx_sha256', 'symbols_sha256'):
        require(isinstance(program.get(field), str) and re.fullmatch('[0-9a-f]{64}', program[field]),
                'Invalid policy program hash')
    require(policy.get('host_files') == host_files, 'Policy host code differs')
    require(policy.get('packing_receipt_sha256') == digest(receipt_bytes), 'Packing receipt hash differs')
    receipt = json.loads(receipt_bytes)
    require(receipt.get('format') == 'ak820-ci-packing-receipt-1'
            and receipt.get('hardware_validated') is False, 'Unsupported packing receipt')
    require(receipt.get('program') == {k: program[k] for k in ('ihx_sha256', 'symbols_sha256', 'schema')},
            'Packing receipt belongs to a different program')
    require(receipt.get('host_files') == host_files, 'Packing receipt host code differs')
    packing = receipt.get('packing', {})
    require(packing.get('physical_usb_opened') is False and packing.get('hardware_validated') is False
            and packing.get('recovery_byte_equal') is True
            and packing.get('install_modes') == ['permanent', 'trial']
            and isinstance(packing.get('images'), dict)
            and set(packing['images']) == {'ak820-vial-trial.bin', 'restore-native.bin'}
            and isinstance(packing.get('permanent'), dict)
            and packing['permanent'].get('trial') is False, 'Packing receipt lacks successful packing evidence')
    for image in (packing['images']['ak820-vial-trial.bin'],
                  packing['images']['restore-native.bin'], packing['permanent']):
        require(isinstance(image, dict) and image.get('size') == pack.APP_END - pack.APP_START
                and isinstance(image.get('sha256'), str)
                and re.fullmatch('[0-9a-f]{64}', image['sha256']), 'Invalid packing image evidence')
    require(packing['images']['ak820-vial-trial.bin'].get('trial') is True
            and packing['images']['ak820-vial-trial.bin'].get('build_id') == pack.BUILD_ID
            and packing['permanent'].get('build_id') == pack.BUILD_ID,
            'Packing trial or permanent schema differs')
    review = _record(program_review_bytes, 'ak820-ci-program-review-1')
    require(review.get('status') == 'passed' and review.get('hardware_validated') is False,
            'Program review is not a completed offline pass')
    # Policy uses file bytes, including its final newline; checked by bundle gate.


def validate_bundle_authorization(bundle: Path, manifest: dict, record: dict) -> None:
    """Validate CI evidence after ordinary manifest/file/build/host validation."""
    files = manifest['files']
    is_ci = record.get('format') == 'ak820-reproduced-review-1'
    require((set(files) & CI_EXTRA_FILES) == (CI_EXTRA_FILES if is_ci else set()),
            'Mixed exact-build and CI authorization evidence')
    if not is_ci:
        return
    def data(name):
        return (bundle / name).read_bytes()
    def sha(name):
        return digest(data(name))
    policy_bytes = data('reviews/program-policy.json')
    policy = json.loads(policy_bytes)
    review_bytes = data('reviews/program-review.md')
    validate_policy(policy, manifest['host_files'], data('reports/packing-validation.json'), review_bytes)
    program = policy['program']
    require(program['ihx_sha256'] == sha('firmware/application.ihx')
            and program['symbols_sha256'] == symbols_sha256(bundle / 'firmware/application.map'),
            'Fresh build differs from the reviewed program')
    policy_sha = digest(policy_bytes)
    review = _record(review_bytes, 'ak820-ci-program-review-1')
    require(review.get('policy_sha256') == policy_sha, 'Program review belongs to another policy')
    attestation = json.loads(data('reports/build-attestation.json'))
    build = {key + '_sha256': sha(name) for key, name in (
        ('ihx', 'firmware/application.ihx'), ('map', 'firmware/application.map'),
        ('mem', 'firmware/application.mem'), ('build_report', 'reports/build-report.json'))}
    require(attestation.get('format') == 'ak820-ci-build-attestation-1'
            and attestation.get('hardware_validated') is False
            and isinstance(attestation.get('source_commit'), str)
            and re.fullmatch('[0-9a-f]{40}', attestation['source_commit'])
            and attestation.get('build') == build
            and attestation.get('host_files') == manifest['host_files']
            and attestation.get('policy_sha256') == policy_sha
            and attestation.get('program_review_sha256') == digest(review_bytes)
            and attestation.get('qualification_sha256') == sha('reports/qualification.json'),
            'Build attestation differs from bundle evidence')
    require(record.get('policy_sha256') == policy_sha
            and record.get('program_review_sha256') == digest(review_bytes)
            and record.get('attestation_sha256') == sha('reports/build-attestation.json'),
            'Reproduction record differs from authorization evidence')
    qualification = json.loads(data('reports/qualification.json'))
    hashes = {'ihx': build['ihx_sha256'], 'map': build['map_sha256']}
    require(qualification.get('format') == 'ak820-offline-tests-1'
            and qualification.get('passed') is True and qualification.get('require_toolchain') is True
            and qualification.get('hardware_validated') is False
            and qualification.get('physical_device_commands') == 0
            and qualification.get('iap_fault_profile') == 'guarded-erase'
            and qualification.get('build_unchanged') is True
            and qualification.get('build_hashes') == hashes
            and qualification.get('unit_tests', {}).get('skipped') == 0
            and qualification.get('unit_tests', {}).get('run', 0) > 0
            and set(qualification.get('tools', {})) >= {'sdcc', 's51'}
            and all(qualification['tools'][tool].get('sha256') for tool in ('sdcc', 's51')),
            'Qualification did not pass with required tools and unchanged build')
    validate_qualification_contract(qualification)
    tests = qualification.get('tests')
    require(isinstance(tests, list) and bool(tests), 'Qualification has no tests')
    for test in tests:
        require(test.get('exit_code') == 0 and test.get('unit_tests', {}).get('skipped', 0) == 0
                and test.get('build_before') == hashes and test.get('build_after') == hashes,
                'Qualification contains failed, skipped or mixed-build checks')


def validate_qualification_contract(report: dict) -> None:
    """Require every command in test_keyboard.py's full host/CPU contract.

    Interpreter and absolute workspace/output paths may vary across CI hosts.
    Suite identities, arguments and common build/tool paths may not vary.
    The policy's source_files separately binds the runner implementation.
    """
    discovery = {
        ('tools/installer', 'test_*.py'),
        ('tools', 'test_build_release_bundle.py'),
        ('tools', 'test_build_windows_installer.py'),
        ('tools', 'test_keyboard_runner.py'),
        ('tools', 'test_ak820_device_tests.py'),
        ('tools', 'test_ak820_device_protocol.py'),
        ('qmk-8051-ak820/tests/ak820_package', 'test_*.py'),
        ('qmk-8051-ak820/tests/ak820_inventory', 'test_*.py'),
    }
    host = {'tests/' + name + '/run.py' for name in (
        'ak820_usb', 'ak820_keymap', 'ak820_caps_word', 'ak820_macro_guard',
        'ak820_diagnostic', 'ak820_optimization', 'ak820_rgb', 'ak820_via_decode', 'ak820_bounded')}
    cpu = {'tests/' + name + '/run.py' for name in (
        'ak820_features', 'ak820_unlock', 'ak820_tri_layer', 'ak820_iap')}
    cpu |= {'tests/ak820_rgb/emitted.py', 'tests/ak820_bounded/emitted.py', 'tests/ak820_tapping/emitted.py'}
    tapping_host = 'tests/ak820_tapping/run.py'
    expected = {('discover', *item) for item in discovery} | {('host', item) for item in host}
    expected |= {('cpu', item) for item in cpu} | {('docs', 'tools/check_docs.py'), ('host', tapping_host)}
    tests = report.get('tests')
    require(isinstance(tests, list), 'Qualification has no test records')
    seen, roots, qmk_roots, builds = set(), set(), set(), set()
    total = {'run': 0, 'skipped': 0}
    tools = report.get('tools', {})
    require(isinstance(tools, dict) and isinstance(tools.get('s51'), dict)
            and isinstance(tools['s51'].get('path'), str) and bool(tools['s51']['path']),
            'Qualification lacks simulator path')
    for test in tests:
        command = test.get('command')
        require(isinstance(command, list) and len(command) >= 2
                and all(isinstance(arg, str) and bool(arg) for arg in command),
                'Invalid qualification command')
        args = command[1:]
        if len(args) == 8 and args[:5] == ['-B', '-m', 'unittest', 'discover', '-s'] and args[6] == '-p':
            identity = ('discover', args[5], args[7])
            roots.add(test.get('cwd'))
        elif args == ['tools/check_docs.py']:
            identity = ('docs', args[0]); roots.add(test.get('cwd'))
        elif len(args) == 1 and args[0] in host:
            identity = ('host', args[0]); qmk_roots.add(test.get('cwd'))
        elif args[0] == tapping_host:
            require(len(args) == 4 and args[1:3] == ['--negative-controls', '--output']
                    and PurePosixPath(args[3]).is_absolute(), 'Tapping host qualification needs negative controls and output')
            identity = ('host', tapping_host); qmk_roots.add(test.get('cwd'))
        elif args[0] in cpu:
            iap = args[0] == 'tests/ak820_iap/run.py'
            require(len(args) == (9 if iap else 7)
                    and args[1] == '--build-dir' and args[3] == '--s51'
                    and args[5] == '--output-dir'
                    and args[4] == tools['s51']['path']
                    and PurePosixPath(args[2]).is_absolute() and PurePosixPath(args[6]).is_absolute()
                    and (not iap or args[7:] == ['--iap-fault-profile', 'guarded-erase']),
                    'CPU qualification arguments differ from required build/simulator/profile')
            builds.add(args[2]); qmk_roots.add(test.get('cwd'))
            identity = ('cpu', args[0])
        else:
            raise ValueError('Unknown qualification suite command')
        require(identity in expected and identity not in seen, 'Unknown or duplicate qualification suite')
        seen.add(identity)
        counts = test.get('unit_tests')
        require(isinstance(counts, dict)
                and all(type(counts.get(key)) is int and counts[key] >= 0 for key in total)
                and counts['skipped'] == 0
                and (identity[0] != 'discover' or counts['run'] > 0),
                'Qualification has skipped or empty unittest discovery')
        for key in total:
            total[key] += counts[key]
    require(seen == expected, 'Qualification is missing required suite identities')
    require(len(roots) == 1 and len(qmk_roots) == 1 and len(builds) == 1,
            'Qualification uses mixed workspace or build paths')
    root = next(iter(roots)); qmk = next(iter(qmk_roots))
    require(isinstance(root, str) and PurePosixPath(root).is_absolute()
            and qmk == str(PurePosixPath(root) / 'qmk-8051-ak820'), 'Qualification working directories differ')
    require(report.get('unit_tests') == total, 'Qualification aggregate unittest counts differ')
