"""Audit-only original-root assembly; never creates policies or independent reviews.

After this helper and all release inputs are independently reviewed, committed,
and synchronized into every origin, run from the central repository, for example:
  python audits/beta3-direct-20261026/assemble_origins.py \
    --builds-root qmk-8051-ak820/.build/beta3 \
    --profile-origin main=/tmp/ak820-beta3-isolated/a [repeat for all ten] \
    --toolchain toolchains/sdcc-4.6.0 --source-commit COMMIT --output audits/beta3-direct-20261026/assembled
Build locations are repository-relative and identical in every relevant root.
No compilation, device access, policy editing, or approval bypass is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HELPER = Path(__file__).resolve().relative_to(ROOT)
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'qmk-8051-ak820/util'), str(ROOT / 'tools/installer')]
import build_ci_release as ci
import firmware_matrix as matrix
import build_capability_catalog as capability
import ak820_profiles as profiles
import settings_backup as settings
import build_beta_release_assets as beta
import ak820
import measure_origin


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def relative(value):
    path = Path(value)
    require(not path.is_absolute() and path.parts and all(p not in ('.', '..') for p in path.parts),
            'Expected a safe repository-relative path')
    return path


def checked(root, rel):
    rel = relative(rel)
    current = root
    for part in rel.parts:
        current /= part
        require(not current.is_symlink(), 'Symlink in protected path: ' + str(current))
    require(current.resolve().is_relative_to(root.resolve()), 'Path escapes repository')
    return current


def origins(items):
    result = {}
    for item in items:
        name, sep, root = item.partition('=')
        require(sep and root and name in ci.release_profile_names() and name not in result,
                'Invalid or duplicate profile origin')
        path = Path(root).absolute()
        require(path.is_dir() and path.resolve() == path, 'Origin must be an actual absolute directory')
        result[name] = path
    require(set(result) == set(ci.release_profile_names()), 'Supply exactly ten profile origins')
    return result


def source_snapshot(root, commit):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    require(git('rev-parse', 'HEAD').decode().strip() == commit, 'Origin HEAD differs from reviewed commit')
    require(not git('diff', '--name-only', 'HEAD'), 'Tracked source differs from reviewed commit')
    snapshot = {}
    for raw in git('ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if not raw:
            continue
        metadata, raw_name = raw.split(b'\t', 1)
        mode, kind, object_id = metadata.split()
        require(kind == b'blob' and mode in (b'100644', b'100755'), 'Unsupported committed source kind')
        name = raw_name.decode()
        path = checked(root, name)
        require(path.is_file(), 'Missing committed source: ' + name)
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == object_id.decode(), 'Committed source bytes differ: ' + name)
        snapshot[name] = hashlib.sha256(data).hexdigest()
    require(HELPER.as_posix() in snapshot, 'Assembly helper must be committed')
    return snapshot


def catalog_rows(catalog):
    require(catalog.get('format') == matrix.FORMAT and isinstance(catalog.get('settings_transitions'), list),
            'Invalid trusted settings catalog')
    rows = catalog.get('profiles')
    require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows)
            and tuple(row.get('profile') for row in rows) == ci.release_profile_names(),
            'Settings catalog must contain exactly ten ordered profiles')
    settings._catalog_images(catalog)
    return {row['profile']: row for row in rows}


def bind_row(name, row, approved, identity):
    configuration = profiles.configuration(name)
    static = approved.get('identity')
    contract = approved.get('settings_identity')
    require(row.get('profile') == name and row.get('configuration') == configuration
            and row.get('measurement_status') == 'linked-memory-pass'
            and row.get('runtime_status') == 'exact-image-pass'
            and row.get('offline_tests_status') == 'exact-image-pass', 'Incomplete exact-profile qualification: ' + name)
    require(isinstance(contract, dict) and isinstance(static, dict)
            and approved.get('reproducible_identity') == identity
            and static.get('ihx_sha256') == identity['ihx_sha256']
            and static.get('nvm_schema') == identity['nvm_schema']
            and identity['profile'] == name
            and approved.get('release_approved') is False and approved.get('installable') is False
            and contract.get('ihx_sha256') == row['identity']['ihx_sha256']
            and contract.get('nvm_schema') == configuration['nvm_schema']
            and approved.get('configuration') == configuration,
            'Static settings contract differs from exact image: ' + name)
    require(row.get('release_approved') is False and row.get('installable') is False,
            'Measured row claims approval')
    return dict(row, reproducible_identity=identity, settings_identity=contract,
                settings_status='exact-image-contract')


def combine(results, catalog):
    names = ci.release_profile_names()
    require(len(results) == 10 and tuple(r.get('profile') for r in results) == names,
            'Worker results must contain exactly ten ordered profiles')
    approved = catalog_rows(catalog)
    measured = {}
    images = []
    for result in results:
        name = result['profile']
        row = result['row']
        measured[name] = bind_row(name, row, approved[name], row['reproducible_identity'])
        image = result['capability']
        require(image.get('profile') == name and image.get('build_identity') == row['identity']
                and image.get('status') == 'development' and image.get('project_verified') is True
                and image.get('compatible_transitions') == []
                and all(image.get(flag) is False for flag in ('release_approved', 'hardware_validated',
                                    'settings_writes_authorized', 'flashing_authorized')),
                'Invalid capability row: ' + name)
        images.append(image)
    ihx = [r['identity']['ihx_sha256'] for r in measured.values()]
    code = [r['code_identity']['sha256'] for r in images]
    require(len(set(ihx)) == 10 and len(set(code)) == 10, 'Duplicate exact IHX or CODE identity')
    historical = {r['ihx_sha256'] for r in catalog.get('historical_sources', [])}
    historical.update(r['settings_identity']['ihx_sha256'] for r in catalog.get('historical_profiles', []))
    require(set(settings._catalog_images(catalog)) == set(ihx) | historical,
            'Catalog image set differs from current and historical exact images')
    merged = matrix.matrix(measured)
    merged['settings_transitions'] = catalog['settings_transitions']
    for section in ('historical_sources', 'historical_profiles'):
        if section in catalog:
            merged[section] = catalog[section]
    capabilities = {'format': capability.FORMAT, 'status': 'development-only',
                    'release_approved': False, 'hardware_validated': False,
                    'settings_writes_authorized': False, 'flashing_authorized': False,
                    'images': sorted(images, key=lambda r: r['code_identity']['sha256'])}
    return merged, capabilities


def archive_tree(folder, output, prefix=''):
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob('*')):
            require(not path.is_symlink(), 'Symlink in public bundle')
            if path.is_file():
                entry = zipfile.ZipInfo(prefix + path.relative_to(folder).as_posix(), (1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes())
    output.with_suffix(output.suffix + '.sha256').write_text(f'{sha(output)}  {output.name}\n')


def require_fresh_worker_output(output):
    """Reserve no existing directory, archive, checksum, or worker metadata."""
    paths = [output] + [output.with_suffix(suffix)
                        for suffix in ('.zip', '.zip.sha256', '.worker.json')]
    require(all(not path.exists() and not path.is_symlink() for path in paths),
            'Worker output already exists')


def worker(args):
    output = checked(ROOT, args.output)
    require_fresh_worker_output(output)
    name = args.worker
    before = source_snapshot(ROOT, args.source_commit)
    catalog_path = checked(ROOT, args.settings_catalog)
    ci._require_committed_input(catalog_path, 'Settings catalog')
    catalog = json.loads(catalog_path.read_bytes())
    build = checked(ROOT, relative(args.builds_root) / name)
    snapshot = measure_origin.tree(build)
    toolchain = (ROOT / relative(args.toolchain)).resolve()
    row = matrix.measured_row(build, toolchain)
    image = capability.inspect_entry(build, toolchain)
    row = bind_row(name, row, catalog_rows(catalog)[name], ci.reproducible_identity(build, row['identity']))
    policies = checked(ROOT, relative(args.policies_root) / name)
    result = ci.assemble(build, build / 'qualification.json', policies / 'release-policy.json',
                         policies / 'program-review.md', policies / 'packing-validation.json',
                         output, toolchain, args.source_commit, expected_profile=name)
    require(source_snapshot(ROOT, args.source_commit) == before and measure_origin.tree(build) == snapshot,
            'Inputs changed during worker assembly')
    write(output.with_suffix('.worker.json'), {'profile': name, 'row': row, 'capability': image,
          'source_files': before, 'build_tree': snapshot, 'bundle_tree': measure_origin.tree(output), 'assembly': result})


def orchestrate(args):
    mapping = origins(args.profile_origin)
    before = source_snapshot(ROOT, args.source_commit)
    catalog_path = checked(ROOT, args.settings_catalog)
    ci._require_committed_input(catalog_path, 'Settings catalog')
    catalog = json.loads(catalog_path.read_bytes())
    catalog_rows(catalog)
    output = checked(ROOT, args.output)
    require(not output.exists() and not output.is_symlink(), 'Select a fresh aggregate output')
    snapshots = {}
    builds = {}
    for name, origin in mapping.items():
        require(source_snapshot(origin, args.source_commit) == before, 'Central/origin committed sources differ')
        central = checked(ROOT, relative(args.builds_root) / name)
        original = checked(origin, relative(args.builds_root) / name)
        snapshot = measure_origin.tree(central)
        require(snapshot == measure_origin.tree(original), 'Central/origin build bytes differ: ' + name)
        require((central / 'qualification.json').is_file(), 'Missing profile qualification: ' + name)
        for leaf in ('release-policy.json', 'program-review.md', 'packing-validation.json'):
            policy = checked(ROOT, relative(args.policies_root) / name / leaf)
            require(policy.is_file(), 'Missing profile authorization: ' + name + '/' + leaf)
            ci._require_committed_input(policy, name + ' ' + leaf)
        snapshots[name] = snapshot
        builds[name] = (central, original)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.' + output.name + '.stage-', dir=output.parent) as temporary:
        stage = Path(temporary) / output.name
        (stage / 'profiles').mkdir(parents=True)
        (stage / 'reports').mkdir()
        (stage / 'profile-archives').mkdir()
        results = []
        contexts = []
        worker_outputs = []
        try:
            for name in ci.release_profile_names():
                origin = mapping[name]
                original = builds[name][1]
                retained = json.loads((original / 'profile-tests/results.json').read_bytes())
                interpreter = Path(retained['tests'][0]['command'][0])
                require(interpreter.is_absolute() and interpreter.is_file() and sha(interpreter) == sha(Path(sys.executable)),
                        'Original qualification used another Python binary')
                worker_rel = stage.parent.relative_to(ROOT) / ('worker-' + name)
                work = origin / worker_rel
                require_fresh_worker_output(work)
                worker_outputs.append(work)
                command = [str(interpreter), str(origin / HELPER), '--worker', name,
                           '--builds-root', args.builds_root, '--policies-root', args.policies_root,
                           '--settings-catalog', args.settings_catalog, '--toolchain', args.toolchain,
                           '--source-commit', args.source_commit, '--output', worker_rel.as_posix()]
                log = stage / 'reports' / (name + '.log')
                with log.open('wb') as stream:
                    subprocess.run(command, cwd=origin, stdout=stream, stderr=subprocess.STDOUT, check=True)
                work = origin / worker_rel
                result = json.loads(work.with_suffix('.worker.json').read_bytes())
                require(result['source_files'] == before and result['build_tree'] == snapshots[name], 'Worker input binding differs')
                target = stage / 'profiles' / name
                shutil.copytree(work, target)
                require(measure_origin.tree(target) == result['bundle_tree'] == measure_origin.tree(work), 'Copied approved bundle differs')
                manifest = ak820._load_release(target, target / 'approved-release.json', approved=True)
                contexts.append(ak820.ReleaseContext(name, target, target / 'approved-release.json', manifest,
                                nvm_schema=profiles.configuration(name)['nvm_schema']))
                result['command'] = command
                result['cwd'] = str(origin)
                results.append(result)
                write(stage / 'reports' / (name + '-worker.json'), result)
                archive_tree(target, stage / 'profile-archives' / (name + '.zip'))
            merged, capabilities = combine(results, catalog)
            payload = {'firmware-matrix.json': json.dumps(merged).encode()}
            for context in contexts:
                for suffix in ('ihx', 'map', 'mem'):
                    leaf = 'firmware/application.' + suffix
                    payload[f'profiles/{context.profile}/{leaf}'] = (context.bundle / leaf).read_bytes()
            beta.validate_profile_links(payload, contexts, catalog, capabilities)
            write(stage / 'reports/firmware-matrix.json', merged)
            write(stage / 'reports/capability-catalog.json', capabilities)
            write(stage / 'reports/settings-catalog-attestation.json', {
                'format': 'ak820-ci-settings-catalog-check-1', 'settings_catalog_sha256': sha(catalog_path),
                'profiles': {r['profile']: r['row']['identity']['ihx_sha256'] for r in results},
                'hardware_validated': False, 'physical_device_commands': 0})
            archive_tree(stage / 'profiles', stage / 'firmware-bundle.zip', 'profiles/')
            require(source_snapshot(ROOT, args.source_commit) == before, 'Central source changed')
            for name, origin in mapping.items():
                require(source_snapshot(origin, args.source_commit) == before, 'Origin source changed')
                require(all(measure_origin.tree(build) == snapshots[name] for build in builds[name]), 'Build changed')
            require(not output.exists() and not output.is_symlink(), 'Aggregate output appeared during assembly')
            stage.rename(output)
        finally:
            # Worker bundles are private staging copies, never installed catalog paths.
            for work in worker_outputs:
                shutil.rmtree(work, ignore_errors=True)
                for suffix in ('.zip', '.zip.sha256', '.worker.json'):
                    work.with_suffix(suffix).unlink(missing_ok=True)
    print(json.dumps({'output': str(output), 'archive_sha256': sha(output / 'firmware-bundle.zip'),
                      'hardware_validated': False, 'physical_device_commands': 0}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', choices=ci.release_profile_names(), help=argparse.SUPPRESS)
    parser.add_argument('--profile-origin', action='append', default=[])
    parser.add_argument('--builds-root', required=True)
    parser.add_argument('--policies-root', default='ci/profiles')
    parser.add_argument('--settings-catalog', default='tools/installer/settings-catalog.json')
    parser.add_argument('--toolchain', required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    (worker if args.worker else orchestrate)(args)


if __name__ == '__main__':
    main()
