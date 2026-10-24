#!/usr/bin/env python3
"""Retain one exact-image evidence row; verify it without the original build tree."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def safe(name):
    path = Path(name)
    need(name and not path.is_absolute() and '..' not in path.parts and '\\' not in name,
         'Unsafe evidence path: ' + name)
    return path


def frozen_sources(root, commit, br, prefix, payload, snapshots):
    tracked = set(git(root, 'ls-tree', '-r', '--name-only', commit).decode().splitlines())
    lock = json.loads(git(root, 'show', commit + ':qmk-8051-ak820/dependencies/lufa.json'))
    def frozen(name, value):
        need(name in tracked and digest(git(root, 'show', commit + ':' + name)) == value,
             'Source is not frozen: ' + name)
        need(digest((root / name).read_bytes()) == value, 'Current source differs: ' + name)
    for row in br['sources']:
        if row['origin'] != 'source':
            continue
        name = row['path']
        safe(name)
        if name.startswith(prefix + '/'):
            need(digest(payload[name]) == row['sha256'], 'Generated source differs: ' + name)
        elif 'qmk-8051-ak820/' + name in tracked:
            frozen('qmk-8051-ak820/' + name, row['sha256'])
        else:
            need(name.startswith('lib/lufa/') and
                 lock['required_files'].get(name.removeprefix('lib/lufa/')) == row['sha256'],
                 'Unpinned compiler source: ' + name)
    for snapshot in snapshots:
        for name, value in snapshot.items():
            frozen(name, value)
    for name in ('tools/configure_firmware.py', 'tools/build_capability_catalog.py',
                 'tools/ak820_runtime_safety.py', 'qmk-8051-ak820/util/ak820_profiles.py',
                 'qmk-8051-ak820/util/ak820_ci_authorization.py',
                 'qmk-8051-ak820/util/ak820_build_inputs.py'):
        frozen(name, digest((root / name).read_bytes()))


def verify_payload(args, cf, rec, payload):
    prefix = rec['archive_prefix']
    def raw(name):
        return payload[prefix + '/' + safe(name).as_posix()]
    def report(name):
        return json.loads(raw(name))
    def hs(name, value):
        need(digest(raw(name)) == value, 'Evidence hash differs: ' + name)
    c = report('configuration-report.json')
    br = report('build-report.json')
    r = report('runtime-safety/summary.json')
    ident = c['identity']
    need(rec['identity'] == ident and rec['configuration'] == c['configuration'] and
         rec['resources'] == c['resources'], 'Record/configuration binding differs')
    need(c['configuration'] == cf.profiles.configuration(c['configuration']['profile']),
         'Configuration differs from current profile')
    need(rec['build_source'] == br.get('source') and rec['qualification_source'] == c.get('source'),
         'Descriptive source metadata changed')
    for row in br['artifacts']:
        need(row['path'].startswith(prefix + '/') and
             digest(payload[row['path']]) == row['sha256'] and
             len(payload[row['path']]) == row['size'], 'Build artifact differs')
    for suffix in ('ihx', 'map', 'mem'):
        hs('ajazz_ak820_vial.' + suffix, ident[suffix + '_sha256'])
    hs('build-report.json', ident['build_report_sha256'])
    need(digest(cf.canonical(br['sources'])) == ident['source_manifest_sha256'] and
         digest(cf.canonical(c['configuration'])) == ident['configuration_sha256'],
         'Source/configuration manifest differs')
    need(br['configuration'] == c['configuration'] and br.get('short_calls') == c['short_calls'],
         'Build/configuration mismatch')
    need(br['compiler_sha256'] == ident['compiler_sha256'] == cf.SDCC46_PINS['sdcc'] and
         br['assembler_sha256'] == cf.SDCC46_PINS['sdas8051'], 'Compiler pins differ')
    fg, start, irq = (report(name) for name in
        ('runtime-stack.json', 'runtime-safety/startup.json', 'runtime-safety/irq/results.json'))
    need(r == c['runtime_analysis'] and r['source_files'] == cf.runtime_source_snapshot(),
         'Runtime source/configuration mismatch')
    proof = cf.combine_runtime_safety(fg, start, irq, ident,
                                    c['resources']['internal_ram'], r['source_files'])
    need(all(r.get(key) == value for key, value in proof.items()) and r['passed'] and
         r['whole_program_stack_qualified'] and r['stack_margin'] >= 0,
         'Runtime combined contract failed')
    for row in r['reports'].values():
        hs(row['path'], row['sha256'])
    for name, value in r['logs'].items():
        hs('runtime-safety/' + name + '.log', value)
    for name, value in fg['identity']['listing_sha256'].items():
        hs(name, value)
    from pack_ak820 import read_ihex
    with tempfile.TemporaryDirectory(prefix='ak820-evidence-') as directory:
        image, mapfile = Path(directory) / 'image.ihx', Path(directory) / 'image.map'
        image.write_bytes(raw('ajazz_ak820_vial.ihx'))
        mapfile.write_bytes(raw('ajazz_ak820_vial.map'))
        code, symbols = read_ihex(image), cf.linked_symbols(mapfile)
        cf.validate_startup(code, symbols)
        measured = cf.memory_report(code, symbols, raw('ajazz_ak820_vial.mem').decode())
    for key in ('code_bytes', 'code_windows', 'xram', 'protected_windows_clear'):
        need(measured[key] == c['resources'][key], 'Linked resources differ: ' + key)
    for key in ('static_bytes', 'initial_sp', 'stack_capacity'):
        need(measured['internal_ram'][key] == c['resources']['internal_ram'][key],
             'Linked IRAM differs: ' + key)
    need(c['resources']['internal_ram']['runtime_stack_bound'] == r['stack_bound'] and
         c['resources']['internal_ram']['stack_margin'] == r['stack_margin'] and
         c['resources']['internal_ram']['stack_qualified'] is True, 'Runtime resource binding differs')
    snapshots = [r['source_files']]
    if rec['full_regression']:
        q, p = report('qualification.json'), report('profile-tests/results.json')
        need(c['offline_tests_passed'] is True and q['format'] == 'ak820-offline-tests-1' and
             q['require_toolchain'] is True and q['iap_fault_profile'] == 'guarded-erase' and
             q['unit_tests']['run'] > 0 and q.get('test_environment') == {} and
             p['format'] == 'ak820-profile-tests-1', 'Incomplete full qualification')
        cf.validate_qualification_contract(q)
        need(q['passed'] and q['build_unchanged'] and q['unit_tests']['skipped'] == 0 and
             q['build_hashes'] == {s: ident[s + '_sha256'] for s in ('ihx', 'map')},
             'Base qualification failed')
        hs('qualification.json', c['qualification']['sha256'])
        hs('profile-tests/results.json', c['profile_tests']['sha256'])
        totals = {'run': 0, 'skipped': 0}
        original = Path(rec['original_build'])
        seen = set()
        for index, row in enumerate(q['tests']):
            log = Path(row['log']).relative_to(original).as_posix()
            need(log not in seen and Path(log).parent.name.startswith('qualification-logs-') and
                 Path(log).name == f'{index:02d}.txt', 'Base log identity differs')
            seen.add(log)
            hs(log, row['log_sha256'])
            counts = cf.unittest_counts(raw(log).decode())
            need(counts == row['unit_tests'] and counts['skipped'] == 0 and row['exit_code'] == 0 and
                 row['build_before'] == row['build_after'] == q['build_hashes'], 'Base log/result differs')
            for key in totals:
                totals[key] += counts[key]
        need(totals == q['unit_tests'], 'Base aggregate differs')
        # Reconstruct original invocation paths in memory; retained bytes stay untouched.
        oldroot, oldqmk, oldpy = cf.ROOT, cf.QMK, sys.executable
        try:
            cf.ROOT = Path(rec['original_root'])
            cf.QMK = cf.ROOT / 'qmk-8051-ak820'
            sys.executable = rec['python_executable']
            plan = cf.profile_test_plan(c['configuration']['profile'], original, Path(rec['toolchain']))
        finally:
            cf.ROOT, cf.QMK, sys.executable = oldroot, oldqmk, oldpy
        need(p['identity'] == ident and p['passed'] and p['profile'] == ident['profile'] and
             len(p['tests']) == len(plan) and p['source_files'] == cf.test_source_snapshot(),
             'Profile source/suite identity differs')
        for row, (name, cwd, command) in zip(p['tests'], plan):
            need(row['id'] == name and row['cwd'] == str(cwd) and row['command'] == command and
                 row['exit_code'] == 0 and row['build_before'] == row['build_after'] == ident,
                 'Profile invocation differs')
            hs('profile-tests/' + name + '.log', row['log_sha256'])
            if name in ('gates', 'short-call-gates'):
                counts = cf.unittest_counts(raw('profile-tests/' + name + '.log').decode())
                need(counts['run'] > 0 and counts['skipped'] == 0, 'Empty/skipped profile gates')
        snapshots.append(p['source_files'])
        need(rec['catalog_entry']['build_identity'] == ident and
             rec['catalog_entry']['resources'] == c['resources'], 'Catalog identity differs')
    else:
        need(c['offline_tests_passed'] is False, 'Runtime-only row claims regression qualification')
    def offline(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('hardware_validated', 'release_approved', 'settings_writes_authorized',
                           'flashing_authorized'):
                    need(item is False, 'Unexpected approval: ' + key)
                if key == 'physical_device_commands':
                    need(type(item) is int and item == 0, 'Unexpected device command')
                offline(item)
        elif isinstance(value, list):
            for item in value:
                offline(item)
    for value in (rec, c, br, r, fg, start, irq):
        offline(value)
    if rec['full_regression']:
        offline(q)
        offline(p)
    frozen_sources(args.root, rec['source_commit'], br, prefix, payload, snapshots)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('retain', 'verify'))
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--source-commit', required=True)
    p.add_argument('--final-dir', type=Path, required=True)
    p.add_argument('--build-dir', type=Path)
    p.add_argument('--toolchain', type=Path)
    p.add_argument('--command-log', type=Path, action='append', default=[])
    p.add_argument('--full', action='store_true')
    args = p.parse_args()
    args.root = args.root.resolve()
    need(re.fullmatch('[0-9a-f]{40}', args.source_commit), 'Full source commit required')
    sys.path.insert(0, str(args.root / 'tools'))
    import configure_firmware as cf
    final = args.final_dir.resolve()
    if args.command == 'retain':
        need(args.build_dir and args.toolchain, 'Retention requires build directory and toolchain')
        need(git(args.root, 'rev-parse', 'HEAD').decode().strip() == args.source_commit and
             not git(args.root, 'status', '--porcelain', '--untracked-files=normal').strip(),
             'Retention requires current clean frozen source')
        need(not final.exists(), 'Refuse to overwrite retained evidence')
        build = args.build_dir.resolve()
        c, br = read(build / 'configuration-report.json'), read(build / 'build-report.json')
        inspected = cf.inspect(build, args.toolchain)
        import build_capability_catalog as catalog
        catalog.runtime_proof(build, inspected, args.toolchain)
        for key in ('configuration', 'identity', 'resources', 'runtime_analysis', 'short_calls'):
            need(c[key] == inspected[key], 'Stored inspection differs: ' + key)
        entry = None
        if args.full:
            cf.validate_tests(build / 'qualification.json', inspected['identity'])
            cf.validate_profile_tests(read(build / 'profile-tests/results.json'),
                c['configuration']['profile'], c['identity'], build, args.toolchain)
            entry = catalog.inspect_entry(build, args.toolchain)
        prefix = build.relative_to(cf.QMK).as_posix()
        names = {'build-report.json', 'configuration-report.json', 'runtime-stack.json', 'runtime-stack.log'}
        names.update(row['path'][len(prefix)+1:] for row in br['artifacts']
                     if row['path'].startswith(prefix + '/'))
        names.update(row['path'][len(prefix)+1:] for row in br['sources']
                     if row['path'].startswith(prefix + '/'))
        names.update(read(build / 'runtime-stack.json')['identity']['listing_sha256'])
        names.update(path.relative_to(build).as_posix() for path in (build / 'runtime-safety').rglob('*')
                     if path.is_file())
        if args.full:
            names = {path.relative_to(build).as_posix() for path in build.rglob('*') if path.is_file()}
        payload = {}
        for name in names:
            path = build / safe(name)
            need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(build),
                 'Missing/escaping build artifact: ' + name)
            payload[prefix + '/' + name] = path.read_bytes()
        rec = {'format': 'ak820-module-evidence-1', 'source_commit': args.source_commit,
               'build_source': br.get('source'), 'qualification_source': c.get('source'),
               'identity': c['identity'], 'configuration': c['configuration'], 'resources': c['resources'],
               'full_regression': args.full, 'archive_prefix': prefix, 'original_build': str(build),
               'original_root': str(args.root), 'toolchain': str(args.toolchain.resolve()),
               'python_executable': sys.executable, 'catalog_entry': entry,
               'hardware_validated': False, 'release_approved': False, 'physical_device_commands': 0}
        verify_payload(args, cf, rec, payload)
        final.mkdir(parents=True)
        archive = final / 'build.tar.xz'
        with tarfile.open(archive, 'w:xz', preset=6) as tf:
            for name in sorted(payload):
                tf.add(build / Path(name).relative_to(prefix), arcname=name, recursive=False)
        rec['files'] = {name: digest(data) for name, data in payload.items()}
        rec['archive_sha256'] = digest(archive.read_bytes())
        rec['command_logs'] = {}
        for index, path in enumerate(args.command_log):
            name = f'command-{index:02d}.log'
            data = path.read_bytes()
            need(data, 'Empty command log')
            (final / name).write_bytes(data)
            rec['command_logs'][name] = digest(data)
        (final / 'record.json').write_text(json.dumps(rec, indent=2, sort_keys=True) + '\n')
    rec = read(final / 'record.json')
    need(rec['source_commit'] == args.source_commit, 'Record source differs from supplied freeze')
    need(digest((final / 'build.tar.xz').read_bytes()) == rec['archive_sha256'], 'Archive differs')
    with tarfile.open(final / 'build.tar.xz') as tf:
        members = tf.getmembers()
        need(all(m.isfile() and safe(m.name) for m in members) and
             len(members) == len({m.name for m in members}), 'Unsafe/duplicate archive member')
        payload = {m.name: tf.extractfile(m).read() for m in members}
    need({name: digest(data) for name, data in payload.items()} == rec['files'], 'Archive file manifest differs')
    for name, value in rec['command_logs'].items():
        need(digest((final / safe(name)).read_bytes()) == value, 'Command log differs')
    verify_payload(args, cf, rec, payload)
    print('VERIFIED', c['identity']['profile'] if args.command == 'retain' else rec['identity']['profile'], final)


if __name__ == '__main__':
    main()
