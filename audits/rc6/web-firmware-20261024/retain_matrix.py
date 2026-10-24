#!/usr/bin/env python3
"""Retain four frozen development builds and their complete offline evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile

EXPECTED = {'full', 'full-mac-pc', 'full-os-indicators', 'full-mac-pc-os-indicators'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--build-dir', type=Path, action='append', required=True)
    parser.add_argument('--command-log', type=Path, action='append', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--final-dir', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    final = args.final_dir.resolve()
    require(re.fullmatch('[0-9a-f]{40}', args.source_commit), 'Full source commit required')
    subprocess.run(['git', 'cat-file', '-e', args.source_commit + '^{commit}'], cwd=root, check=True)
    require(len(args.build_dir) == len(args.command_log) == 4, 'Exactly four builds and paired command logs required')
    require(not final.exists(), 'Final directory already exists; refuse to overwrite evidence')
    sys.path.insert(0, str(root / 'tools'))
    import configure_firmware as cf
    for name in ('tools/configure_firmware.py', 'tools/build_capability_catalog.py',
                 'qmk-8051-ak820/util/ak820_profiles.py'):
        blob = subprocess.check_output(['git', 'show', args.source_commit + ':' + name], cwd=root)
        require(hashlib.sha256(blob).hexdigest() == sha(root / name), 'Frozen validator changed: ' + name)
    catalog = read(args.catalog)
    require(len(catalog['images']) == 4 and {e['profile'] for e in catalog['images']} == EXPECTED,
            'Catalog must contain exactly the four required profiles')
    builds = []
    for build_arg, log_arg in zip(args.build_dir, args.command_log):
        build, log = build_arg.resolve(), log_arg.resolve()
        c = read(build / 'configuration-report.json')
        q = read(build / 'qualification.json')
        p = read(build / 'profile-tests/results.json')
        runtime = read(build / 'runtime-safety/summary.json')
        require(c['source'] == {'commit': args.source_commit, 'dirty': False}, 'Build source is dirty or not frozen')
        require(c['configuration']['profile'] in EXPECTED and not c['short_calls'], 'Unexpected profile or short calls')
        require(c['offline_tests_passed'] and q['passed'] and q['build_unchanged'] and p['passed'] and
                runtime['passed'] and runtime['whole_program_stack_qualified'] and runtime['stack_margin'] >= 0,
                'Build failed qualification')
        require(len(q['tests']) == 28 and q['unit_tests'] == {'run': 273, 'skipped': 0}, 'Incomplete base tests')
        cf.validate_qualification_contract(q)
        require(log.is_file() and log.stat().st_size > 0, 'Missing command log')
        require(all(not f.is_symlink() for f in build.rglob('*')), 'Symlink in raw build')
        builds.append((build, log, c, q, p, runtime))
    require({item[2]['configuration']['profile'] for item in builds} == EXPECTED, 'Duplicate/missing build profile')
    final.mkdir(parents=True)
    shutil.copyfile(args.catalog, final / 'capability-catalog.json')
    catalog_hash = sha(final / 'capability-catalog.json')
    rows = []
    for build, log, c, q, p, runtime in builds:
        profile = c['configuration']['profile']
        folder = final / profile
        folder.mkdir()
        # Reports remain available without unpacking the complete raw build.
        for name in ('ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map', 'ajazz_ak820_vial.mem',
                     'build-report.json', 'configuration-report.json', 'qualification.json', 'runtime-stack.json'):
            shutil.copyfile(build / name, folder / name)
        shutil.copytree(build / 'runtime-safety', folder / 'runtime-safety')
        for logs in build.glob('qualification-logs-*'):
            shutil.copytree(logs, folder / logs.name)
        shutil.copyfile(build / 'profile-tests/results.json', folder / 'profile-results.json')
        for path in (build / 'profile-tests').glob('*.log'):
            target = folder / path.relative_to(build)
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(path, target)
        for path in (build / 'profile-tests').glob('*/results.json'):
            shutil.copyfile(path, folder / (path.parent.name + '-linked.json'))
        shutil.copyfile(log, folder / 'qualification-command.log')
        br = read(build / 'build-report.json')
        ihx_rows = [row for row in br['artifacts'] if row['path'].endswith('/ajazz_ak820_vial.ihx')]
        require(len(ihx_rows) == 1, 'Cannot identify raw build archive root')
        prefix = Path(ihx_rows[0]['path']).parent.as_posix()
        require(not Path(prefix).is_absolute() and '..' not in Path(prefix).parts, 'Unsafe archive root')
        archive = folder / 'raw-build.tar.xz'
        with tarfile.open(archive, 'w:xz', preset=6) as tf:
            tf.add(build, arcname=prefix)
        entry = next(e for e in catalog['images'] if e['profile'] == profile)
        require(entry['build_identity'] == c['identity'] and entry['resources'] == c['resources'], 'Catalog build mismatch')
        record = {'profile': profile, 'short_calls': False, 'source': c['source'],
                  'identity': c['identity'], 'resources': c['resources'], 'runtime': runtime,
                  'optional_features': c['configuration']['optional_features'],
                  'base_suites': len(q['tests']), 'base_unit_tests': q['unit_tests'],
                  'profile_suites': [row['id'] for row in p['tests']], 'offline_tests_passed': True,
                  'hardware_validated': False, 'release_approved': False, 'physical_device_commands': 0,
                  'raw_build': {'path': 'raw-build.tar.xz', 'sha256': sha(archive), 'bytes': archive.stat().st_size},
                  'command_log_sha256': sha(folder / 'qualification-command.log'),
                  'catalog': {'sha256': catalog_hash, 'entry_sha256': hashlib.sha256(cf.canonical(entry)).hexdigest()}}
        write(folder / 'record.json', record)
        rows.append({'variant': profile, 'profile': profile, 'short_calls': False,
                     'code_bytes': c['resources']['code_bytes'], 'xram_bytes': c['resources']['xram']['bytes'],
                     'stack_bound': runtime['stack_bound'], 'stack_capacity': runtime['stack_capacity'],
                     'stack_margin': runtime['stack_margin'], 'ihx_sha256': c['identity']['ihx_sha256'],
                     'record_sha256': sha(folder / 'record.json'), 'raw_build_sha256': sha(archive)})
    rows.sort(key=lambda item: item['variant'])
    index = {'format': 'ak820-qualified-development-matrix-1', 'source_commit': args.source_commit,
             'qualified_profiles': 4, 'available_named_profiles': len(cf.profiles.PROFILES), 'build_variants': 4, 'base_suites_per_variant': 28,
             'base_unit_tests_per_variant': 273, 'base_unit_skips': 0,
             'supplemental_suites_total': sum(len(item[4]['tests']) for item in builds),
             'minimum_stack_margin': min(row['stack_margin'] for row in rows),
             'catalog_sha256': catalog_hash, 'release_approved': False,
             'hardware_validated': False, 'physical_device_commands': 0, 'variants': rows}
    write(final / 'matrix.json', index)
    table = '\n'.join('| {profile} | {code_bytes} | {xram_bytes} | {stack_bound}/{stack_capacity} | {stack_margin} |'.format(**row) for row in rows)
    (final / 'README.md').write_text(
        '# Four-image development evidence\n\nFrozen source: `' + args.source_commit + '`.\n\n'
        '| Profile | CODE bytes | XRAM bytes | Stack bound/capacity | Stack margin |\n'
        '|---|---:|---:|---:|---:|\n' + table + '\n\n'
        'Each image retains complete compressed build files, qualification logs, runtime proofs and linked test results. '
        'The catalog binds exact images, features and resources.\n\n'
        'Verification: `python audits/rc6/web-firmware-20261024/verify_matrix.py --root .`.\n\n'
        'Offline static analysis and CPU/host tests only. Physical validation and release approval are false; '
        'no physical device commands were issued. Independent review of this evidence remains pending.\n')
    verifier = Path(__file__).with_name('verify_matrix.py')
    subprocess.run([sys.executable, str(verifier), '--root', str(root), '--final-dir', str(final)], check=True)
    print('RETAINED AND VERIFIED', final)

if __name__ == '__main__':
    main()
