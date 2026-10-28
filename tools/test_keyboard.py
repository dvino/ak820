"""Run AK820 offline regressions and record commands, hashes and outcomes.

No keyboard is opened. Host C and linked CPU tests are opt-in because they
require Linux/WSL and the pinned build. Hardware acceptance is documented in
docs/TESTING.md and is never inferred from this report.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'


def tool_environment(toolchain=None, *, required=False):
    """Select one compiler/simulator pair without changing the caller's PATH."""
    env = os.environ.copy()
    configured = toolchain is not None or bool(env.get('AK820_SDCC_BIN'))
    bindir = (toolchain.resolve() / 'bin' if toolchain is not None else
              Path(env['AK820_SDCC_BIN']).resolve() if env.get('AK820_SDCC_BIN') else
              ROOT / 'toolchains/sdcc-4.6.0/bin')
    paths = {name: bindir / name for name in ('sdcc', 's51')}
    available = all(path.is_file() for path in paths.values())
    if configured and not available:
        raise ValueError('Selected toolchain must contain both bin/sdcc and bin/s51')
    if available:
        env['AK820_SDCC_BIN'] = str(bindir)
        env['PATH'] = str(bindir) + os.pathsep + env.get('PATH', '')
    else:
        # Keep the ordinary offline command usable without downloaded tools.
        # Explicit qualification fails rather than quietly skipping CPU checks.
        paths = {name: Path(found) if (found := shutil.which(name)) else None
                 for name in ('sdcc', 's51')}
        if paths['sdcc'] and paths['s51'] and paths['sdcc'].parent == paths['s51'].parent:
            env['AK820_SDCC_BIN'] = str(paths['sdcc'].parent)
    if required and not all(paths.values()):
        raise ValueError('Install the pinned SDCC toolchain or pass --toolchain; CPU checks are required')
    records = {name: ({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                      if path is not None else None) for name, path in paths.items()}
    return env, records


def unittest_counts(output):
    """Keep unittest skips visible even when its process exits successfully."""
    ran = re.findall(r'^Ran (\d+) tests? in ', output, re.M)
    skipped = re.findall(r'^(?:OK|FAILED)\s*\([^\n]*\bskipped=(\d+)', output, re.M)
    return {'run': sum(map(int, ran)), 'skipped': sum(map(int, skipped))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', action='store_true', help='Also run Linux C harnesses')
    parser.add_argument('--build-dir', type=Path, help='Also test this linked QMK build')
    parser.add_argument('--toolchain', type=Path,
                        help='SDCC installation; defaults to AK820_SDCC_BIN or local SDCC 4.6.0')
    parser.add_argument('--require-toolchain', action='store_true',
                        help='Require compiler/CPU checks and fail if a unit suite reports skips')
    parser.add_argument('--iap-fault-profile', choices=('legacy-iap', 'guarded-erase'), default='legacy-iap',
                        help='Expected IAP failure path for the selected image; guarded-erase is the new candidate')
    parser.add_argument('--output', type=Path, default=ROOT / 'host/runs/offline-tests.json')
    args = parser.parse_args(argv)
    if args.require_toolchain and not args.host:
        parser.error('--require-toolchain requires --host so compiler and CPU checks run')
    try:
        env, tool_records = tool_environment(args.toolchain,
                                            required=args.require_toolchain or bool(args.build_dir))
    except ValueError as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    logdir = Path(tempfile.mkdtemp(prefix=args.output.stem + '-logs-', dir=args.output.parent))
    py = sys.executable
    suites = [
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools/installer', '-p', 'test_*.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_build_release_bundle.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_build_windows_installer.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_keyboard_runner.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_ak820_device_tests.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_ak820_device_protocol.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'qmk-8051-ak820/tests/ak820_package', '-p', 'test_*.py']),
        (ROOT, [py, '-B', '-m', 'unittest', 'discover', '-s', 'qmk-8051-ak820/tests/ak820_inventory', '-p', 'test_*.py']),
        (ROOT, [py, 'tools/check_docs.py']),
    ]
    if args.host:
        for name in ('ak820_usb', 'ak820_keymap', 'ak820_caps_word', 'ak820_macro_guard',
                     'ak820_diagnostic', 'ak820_optimization', 'ak820_rgb', 'ak820_via_decode', 'ak820_combo'):
            suites.append((QMK, [py, f'tests/{name}/run.py']))
        suites.append((QMK, [py, 'tests/ak820_macro_guard/parse.py']))
        suites.append((QMK, [py, 'tests/ak820_macro_guard/powercut.py']))
        tap_dance = [py, 'tests/ak820_tap_dance/host.py']
        if tool_records['sdcc']:
            tap_dance.extend(['--sdcc', tool_records['sdcc']['path']])
        suites.append((QMK, tap_dance))
        suites.append((QMK, [py, 'tests/ak820_bounded/run.py']))
        repeat_table = [py, 'tests/ak820_repeat/table.py']
        if tool_records['sdcc']:
            repeat_table.extend(['--sdcc', tool_records['sdcc']['path']])
        suites.append((QMK, repeat_table))
        if tool_records['sdcc'] and tool_records['s51']:
            for name in ('ak820_repeat', 'ak820_macro_guard', 'ak820_tap_dance'):
                suites.append((QMK, [py, f'tests/{name}/cpu.py', '--sdcc', tool_records['sdcc']['path'],
                                     '--simulator', tool_records['s51']['path']]))
            suites.append((QMK, [py, 'tests/ak820_tapping/compact_cpu.py', '--sdcc', tool_records['sdcc']['path'],
                                 '--simulator', tool_records['s51']['path']]))
        suites.append((QMK, [py, 'tests/ak820_tapping/run.py', '--negative-controls',
                            '--output', str((logdir / 'tapping-host.json').resolve())]))
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
        simulator = tool_records['s51']['path']
        for name in ('ak820_features', 'ak820_unlock', 'ak820_tri_layer', 'ak820_iap'):
            command = [py, f'tests/{name}/run.py', '--build-dir', str(build),
                       '--s51', str(simulator), '--output-dir', str((logdir / name).resolve())]
            if name == 'ak820_iap':
                command.extend(['--iap-fault-profile', args.iap_fault_profile])
            suites.append((QMK, command))
        suites.append((QMK, [py, 'tests/ak820_rgb/emitted.py', '--build-dir', str(build),
                            '--s51', str(simulator), '--output-dir', str((logdir / 'rgb').resolve())]))
        suites.append((QMK, [py, 'tests/ak820_bounded/emitted.py', '--build-dir', str(build),
                            '--s51', str(simulator), '--output-dir', str((logdir / 'bounded').resolve())]))
        suites.append((QMK, [py, 'tests/ak820_tapping/emitted.py', '--build-dir', str(build),
                            '--s51', str(simulator), '--output-dir', str((logdir / 'tapping').resolve())]))
        suites.append((QMK, [py, 'tests/ak820_combo/emitted.py', '--build-dir', str(build),
                            '--s51', str(simulator), '--output-dir', str((logdir / 'combo').resolve())]))
    records = []
    for index, (cwd, command) in enumerate(suites):
        started = time.monotonic()
        before_hashes = build_hashes() if build else {}
        print('RUN', ' '.join(command), flush=True)
        try:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True)
        except OSError as error:
            # A launch failure must still leave a complete failure report.
            result = subprocess.CompletedProcess(command, 127, f'{type(error).__name__}: {error}\n')
        log = logdir / f'{index:02d}.txt'
        log.write_text(result.stdout, encoding='utf-8')
        records.append({'cwd': str(cwd), 'command': command, 'exit_code': result.returncode,
                        'seconds': round(time.monotonic() - started, 3), 'log': str(log),
                        'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
                        'unit_tests': unittest_counts(result.stdout),
                        'build_before': before_hashes, 'build_after': build_hashes() if build else {}})
        print('PASS' if result.returncode == 0 else 'FAIL', log, flush=True)
    report = {'format': 'ak820-offline-tests-1', 'hardware_validated': False,
              'physical_device_commands': 0, 'tests': records,
              'tools': tool_records, 'require_toolchain': args.require_toolchain,
              'test_environment': {name: env[name] for name in
                                   ('CC', 'ASAN_OPTIONS', 'LSAN_OPTIONS', 'UBSAN_OPTIONS') if name in env},
              'unit_tests': {key: sum(r['unit_tests'][key] for r in records)
                             for key in ('run', 'skipped')},
              'passed': all(r['exit_code'] == 0 for r in records)}
    if args.host:
        for key, name in (('repeat_cpu_check', 'ak820_repeat'), ('macro_cpu_check', 'ak820_macro_guard'),
                          ('tap_dance_cpu_check', 'ak820_tap_dance')):
            cpu = next((r for r in records if f'tests/{name}/cpu.py' in r['command']), None)
            report[key] = ('passed' if cpu['exit_code'] == 0 else 'failed') if cpu else 'skipped: SDCC or s51 unavailable'
    if args.require_toolchain and report['unit_tests']['skipped']:
        report['passed'] = False
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
