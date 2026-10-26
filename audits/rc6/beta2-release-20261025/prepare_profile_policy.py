"""Regenerate exact-image draft evidence; never creates independent approval.

Run again after source/test freeze. Optional --settings-run accepts an existing
successful test record with command, exit_code, source_files, log_path and
log_sha256; every source and log is checked before reuse.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
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

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings-run', type=Path)
    args = parser.parse_args()
    packing = json.loads((AUDIT / 'packing-preflight.json').read_text())
    transitions = json.loads((AUDIT / 'transition-preflight.json').read_text())
    require(packing['offline_only'] and packing['physical_device_commands'] == 0, "Preparation input check failed: packing['offline_only'] and packing['physical_device_commands'] == 0")
    require(len(transitions['cases']) == 130 and all(c['passed'] for c in transitions['cases']), "Preparation input check failed: len(transitions['cases']) == 130 and all(c['passed'] for c in transitions['cases'])")
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
            build = ROOT.parent / f'ak820-beta2-qualified-{group}-20261025/qmk-8051-ak820/.build/next-{profile}-release2-certified'
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
            require(len(cases) == 13 and all(c['target'] == ihx for c in cases), "Preparation input check failed: len(cases) == 13 and all(c['target'] == ihx for c in cases)")
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
            source_names = set(safety.REQUIRED_SOURCES) | set(summary['source_files']) | {relative(Path(__file__).resolve()), relative(AUDIT / 'verify_transition.py')}
            source_names |= {name for test in tests for name in test['source_files']}
            sources = {name: record(ROOT / name) for name in sorted(source_names)}
            symbols = authorization.symbols_sha256(build / 'ajazz_ak820_vial.map')
            program = {'ihx_sha256': ihx, 'symbols_sha256': symbols, 'schema': report['build_id']}
            dest = ROOT / 'ci/profiles' / profile
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
    write(AUDIT / 'profile-policy-preparation.json', {'format': 'ak820-beta2-policy-preparation-1',
        'hardware_validated': False, 'physical_device_commands': 0, 'profiles': outputs,
        'gates': ['Refresh source and test hashes after freeze', 'Complete full exact-image regression',
                  *(['Supply frozen settings test record'] if not tests else []), 'Obtain independent exact-tree policy review',
                  'Commit reviewed inputs before CI assembly']})

if __name__ == '__main__':
    main()
