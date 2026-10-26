#!/usr/bin/env python3
"""Replay the strict profile-suite contract using the authentic CI main archive.

Only the log lookup directory is relocated. Expected commands retain the original
CI checkout/build/toolchain paths. No report fields or validator rules change.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import tarfile
import tempfile
from unittest.mock import patch

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', type=Path)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / 'tools'))
import configure_firmware as config

sources = config.test_source_snapshot()
ci_root = Path('/home/runner/work/ak820/ak820')
ci_qmk = ci_root / 'qmk-8051-ak820'
ci_build = ci_qmk / '.build/ci-profiles/main'
toolchain = ci_root / 'toolchains/sdcc-4.6.0'
outer_python = '/opt/hostedtoolcache/Python/3.12.15/x64/bin/python'
resolved_python = '/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3.12'
original_plan = config.profile_test_plan
checks = []
args.scratch.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(dir=args.scratch) as temporary:
    build = Path(temporary)
    output = build / 'profile-tests'
    output.mkdir()
    prefix = 'qmk-8051-ak820/.build/ci-profiles/main/profile-tests/'
    with tarfile.open(args.archive) as archive:
        for member in archive:
            if member.isfile() and member.name.startswith(prefix):
                name = member.name[len(prefix):]
                if '/' in name:
                    continue
                if name in ('', '.', '..'):
                    raise ValueError('Unexpected archive member')
                (output / name).write_bytes(archive.extractfile(member).read())
    report = config.load_json(output / 'results.json')
    if report['source_files'] != sources:
        raise ValueError('Authentic source snapshot differs from this checkout')

    def expected_plan(name, unused_build, selected_toolchain):
        return original_plan(name, ci_build, selected_toolchain)

    def validate(value):
        config.validate_profile_tests(value, 'main', report['identity'], build, toolchain)

    def reject(label, value):
        try:
            validate(value)
        except ValueError as error:
            checks.append({'case': label, 'result': 'rejected', 'reason': str(error)})
        else:
            raise AssertionError('Accepted mismatch: ' + label)

    with patch.object(config, 'ROOT', ci_root), patch.object(config, 'QMK', ci_qmk), \
            patch.object(config, 'test_source_snapshot', return_value=sources), \
            patch.object(config, 'profile_test_plan', side_effect=expected_plan):
        with patch.object(sys, 'executable', outer_python):
            expected = expected_plan('main', build, toolchain)
            differences = []
            for row, (identifier, cwd, command) in zip(report['tests'], expected):
                if row['id'] != identifier or row['cwd'] != str(cwd):
                    raise AssertionError('Unexpected suite/cwd mismatch')
                for index, (actual, wanted) in enumerate(zip(row['command'], command)):
                    if actual != wanted:
                        differences.append({'suite': identifier, 'argument': index,
                                            'actual': actual, 'expected': wanted})
                if len(row['command']) != len(command):
                    raise AssertionError('Unexpected command length mismatch')
            if len(differences) != len(expected) or any(d['argument'] != 0 for d in differences):
                raise AssertionError('Failure is not exclusively executable spelling')
            reject('original assembly interpreter', report)
        with patch.object(sys, 'executable', resolved_python):
            validate(report)
            checks.append({'case': 'resolved qualification interpreter', 'result': 'passed'})
            for label, mutation in (
                ('wrong interpreter', lambda r: r['tests'][0]['command'].__setitem__(0, outer_python)),
                ('missing flag', lambda r: r['tests'][0]['command'].remove('-B')),
                ('wrong module', lambda r: r['tests'][0]['command'].__setitem__(3, 'other_module')),
                ('wrong cwd', lambda r: r['tests'][0].__setitem__('cwd', '/tmp')),
                ('wrong image', lambda r: r['tests'][0].__setitem__('build_after', {})),
                ('wrong log hash', lambda r: r['tests'][0].__setitem__('log_sha256', '0' * 64)),
            ):
                bad = copy.deepcopy(report)
                mutation(bad)
                reject(label, bad)
    receipt = {'format': 'ak820-ci-command-reproduction-1', 'run': 40258163824,
               'assembly_job': 121379439444, 'profile': 'main',
               'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
               'source_files': len(sources), 'suites': len(report['tests']),
               'differences': differences, 'checks': checks,
               'hardware_validated': False, 'physical_device_commands': 0}
    print(json.dumps(receipt, indent=2, sort_keys=True))
