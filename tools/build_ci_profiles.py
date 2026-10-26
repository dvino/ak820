#!/usr/bin/env python3
"""Build and qualify every release profile for the approved CI bundle gate.

Each image gets a fresh bootstrap build and source/IRQ context certificate. The
bootstrap is never packaged; it exists only to bind the audited spill transform
to this checkout, pinned toolchain and protected IRQ source closure.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(QMK / 'util'))
sys.path.insert(0, str(ROOT / 'tools'))

import ak820_profiles
import ak820_parameter_spills
import configure_firmware


def build_all(builds_root: Path, bootstrap_root: Path, toolchain: Path,
              qmk_bin: Path, python: Path, selected_profiles=None) -> dict:
    profiles = tuple(ak820_profiles.RELEASE_PROFILES)
    if profiles != ('main', 'game', 'mmo', 'typing', 'code', 'pointer',
                    'onehand', 'creative', 'shortcuts', 'multios'):
        raise ValueError('Release profiles differ from the approved ten-profile catalog')
    if selected_profiles is not None:
        selected_profiles = tuple(selected_profiles)
        if (not selected_profiles or len(set(selected_profiles)) != len(selected_profiles)
                or any(name not in profiles for name in selected_profiles)):
            raise ValueError('Select distinct canonical release profiles')
        profiles = tuple(name for name in profiles if name in selected_profiles)
    builds_root, bootstrap_root = builds_root.resolve(), bootstrap_root.resolve()
    toolchain = configure_firmware.validate_tools(toolchain)
    qmk_bin, python = qmk_bin.resolve(), python.resolve()
    for root in (builds_root, bootstrap_root):
        if not root.is_relative_to(QMK.resolve()) or root.exists() or root.is_symlink():
            raise ValueError('Build output roots must be fresh directories beneath the QMK source root')
    if not qmk_bin.is_file() or not python.is_file():
        raise ValueError('Missing pinned QMK build environment')
    builds_root.mkdir(parents=True)
    bootstrap_root.mkdir(parents=True)
    built = {}
    for name in profiles:
        configuration = ak820_profiles.configuration(name)
        bootstrap = bootstrap_root / name
        destination = builds_root / name
        # The diagnostic seed omits only context-dependent spill trimming.
        # Other proven passes keep it compact; the enlarged CODE window is
        # for IRQ closure only and cannot qualify an installable image.
        subprocess.run([
            str(python), str(QMK / 'util/build_ak820.py'), '--profile', name,
            '--toolchain', str(toolchain), '--qmk-bin', str(qmk_bin),
            '--build-dir', str(bootstrap), '--code-end', '0xe000',
            '--compress-default-keymap', '--short-calls',
            '--nvm-update-block-asm', '--nvm-read-block-asm', '--keymap-words-asm',
            '--trim-register-saves', '--tail-share', '--outline-max-helpers', '400',
        ], cwd=QMK, check=True)
        stack_path = bootstrap / 'runtime-stack.json'
        configure_firmware.run_runtime_analysis(
            bootstrap, {'ihx_sha256': configure_firmware.sha(bootstrap / 'ajazz_ak820_vial.ihx'),
                        'map_sha256': configure_firmware.sha(bootstrap / 'ajazz_ak820_vial.map')})
        context = bootstrap / 'parameter-spills-context.json'
        ak820_parameter_spills.make_context_certificate(
            QMK, bootstrap, stack_path, toolchain, context)
        subprocess.run([
            str(python), str(ROOT / 'tools/configure_firmware.py'), 'build',
            '--profile', name, '--toolchain', str(toolchain),
            '--qmk-bin', str(qmk_bin), '--python', str(python),
            '--parameter-spills-context', str(context), '--build-dir', str(destination),
        ], cwd=ROOT, check=True)
        report = configure_firmware.load_json(destination / 'configuration-report.json')
        if (report.get('configuration') != configuration
                or report.get('offline_tests_passed') is not True
                or report.get('runtime_analysis', {}).get('whole_program_stack_qualified') is not True
                or not (destination / 'qualification.json').is_file()
                or not (destination / 'profile-tests/results.json').is_file()):
            raise ValueError('Final configured build is incomplete: ' + name)
        built[name] = {'build': str(destination), 'bootstrap': str(bootstrap),
                       'context_sha256': configure_firmware.sha(context),
                       'identity': report['identity']}
    return {'format': 'ak820-ci-profile-builds-1', 'profiles': built, 'selected_profiles': list(profiles),
            'hardware_validated': False, 'physical_device_commands': 0}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--builds-root', type=Path, default=QMK / '.build/ci-profiles')
    parser.add_argument('--bootstrap-root', type=Path, default=QMK / '.build/ci-profile-bootstrap')
    parser.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    parser.add_argument('--qmk-bin', type=Path, default=QMK / '.venv/bin/qmk')
    parser.add_argument('--python', type=Path, default=Path(sys.executable))
    parser.add_argument('--profile', action='append', choices=ak820_profiles.RELEASE_PROFILES,
                        help='Select a canonical profile; repeat for distinct profiles (default: all ten)')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args(argv)
    result = build_all(args.builds_root, args.bootstrap_root, args.toolchain,
                       args.qmk_bin, args.python, args.profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'profiles': len(result['profiles']),
                      'physical_device_commands': 0, 'hardware_validated': False}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
