"""Run AK820 offline regressions and record commands, hashes and outcomes.

No keyboard is opened. Host C and linked CPU tests are opt-in because they
require Linux/WSL and the pinned build. Hardware acceptance is documented in
docs/TESTING.md and is never inferred from this report.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', action='store_true', help='Also run Linux C harnesses')
    parser.add_argument('--build-dir', type=Path, help='Also test this linked QMK build')
    parser.add_argument('--iap-fault-profile', choices=('legacy-iap', 'guarded-erase'), default='legacy-iap',
                        help='Expected IAP failure path for the selected image; guarded-erase is the new candidate')
    parser.add_argument('--output', type=Path, default=ROOT / 'host/runs/offline-tests.json')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    logdir = Path(tempfile.mkdtemp(prefix=args.output.stem + '-logs-', dir=args.output.parent))
    py = sys.executable
    suites = [
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools/installer', '-p', 'test_*.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_build_release_bundle.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_build_windows_installer.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_keyboard_runner.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_ak820_device_tests.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'qmk-8051-ak820/tests/ak820_package', '-p', 'test_*.py']),
        (ROOT, [py, 'tools/check_docs.py']),
    ]
    if args.host:
        for name in ('ak820_usb', 'ak820_keymap', 'ak820_caps_word', 'ak820_macro_guard',
                     'ak820_diagnostic', 'ak820_optimization', 'ak820_rgb'):
            suites.append((QMK, [py, f'tests/{name}/run.py']))
    build = None
    initial_hashes = {}
    def build_hashes():
        return {suffix: hashlib.sha256((build / ('ajazz_ak820_vial.' + suffix)).read_bytes()).hexdigest()
                for suffix in ('ihx', 'map')}
    if args.build_dir:
        build = args.build_dir.resolve()
        if not (build / 'ajazz_ak820_vial.ihx').is_file():
            parser.error('Select a completed build directory containing ajazz_ak820_vial.ihx')
        initial_hashes = build_hashes()
        simulator = ROOT / 'toolchains/sdcc-4.4.0/bin/s51'
        for name in ('ak820_features', 'ak820_unlock', 'ak820_tri_layer', 'ak820_iap'):
            command = [py, f'tests/{name}/run.py', '--build-dir', str(build),
                       '--s51', str(simulator), '--output-dir', str((logdir / name).resolve())]
            if name == 'ak820_iap':
                command.extend(['--iap-fault-profile', args.iap_fault_profile])
            suites.append((QMK, command))
        suites.append((QMK, [py, 'tests/ak820_rgb/emitted.py', '--build-dir', str(build),
                            '--s51', str(simulator), '--output-dir', str((logdir / 'rgb').resolve())]))
    records = []
    for index, (cwd, command) in enumerate(suites):
        started = time.monotonic()
        before_hashes = build_hashes() if build else {}
        print('RUN', ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log = logdir / f'{index:02d}.txt'
        log.write_text(result.stdout, encoding='utf-8')
        records.append({'cwd': str(cwd), 'command': command, 'exit_code': result.returncode,
                        'seconds': round(time.monotonic() - started, 3), 'log': str(log),
                        'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
                        'build_before': before_hashes, 'build_after': build_hashes() if build else {}})
        print('PASS' if result.returncode == 0 else 'FAIL', log, flush=True)
    report = {'format': 'ak820-offline-tests-1', 'hardware_validated': False,
              'physical_device_commands': 0, 'tests': records,
              'passed': all(r['exit_code'] == 0 for r in records)}
    if build:
        report['iap_fault_profile'] = args.iap_fault_profile
        report['build_hashes'] = initial_hashes
        report['build_unchanged'] = (build_hashes() == initial_hashes and
            all(r['build_before'] == initial_hashes == r['build_after'] for r in records))
        report['passed'] &= report['build_unchanged']
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
