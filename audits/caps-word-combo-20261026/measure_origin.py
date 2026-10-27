"""Measure an unchanged build through the canonical tools in its original root."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'qmk-8051-ak820/util')]
import configure_firmware as configured


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(folder):
    result = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in measured build: ' + str(path))
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = sha(path)
    if not result:
        raise ValueError('Empty measured build')
    return result


def source_files(build):
    result = {**configured.test_source_snapshot(), **configured.runtime_source_snapshot()}
    report = json.loads((build / 'build-report.json').read_text())
    for row in report['sources']:
        if row.get('origin') == 'source' and not row['path'].startswith('.build/'):
            name = 'qmk-8051-ak820/' + row['path'].replace('\\', '/')
            path = (ROOT / name).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                raise ValueError('Invalid build source: ' + name)
            result[name] = sha(path)
    return result


def measured_row(build, origin, toolchain, native_reference, output):
    build, origin = build.resolve(), origin.resolve()
    relative = build.relative_to(ROOT)
    original = origin / relative
    original_tools = origin / toolchain.resolve().relative_to(ROOT)
    inputs = source_files(build)

    def compare_sources():
        if source_files(build) != inputs:
            raise ValueError('Central source changed during original-root measurement')
        for name, digest in inputs.items():
            path = (origin / name).resolve()
            if not path.is_relative_to(origin) or not path.is_file() or sha(path) != digest:
                raise ValueError('Original-root source differs: ' + name)

    compare_sources()
    snapshot = tree(build)
    if tree(original) != snapshot:
        raise ValueError('Copied build differs from its original tree')
    native_sha = sha(native_reference)
    output.mkdir(parents=True, exist_ok=False)
    matrix = output / 'matrix.json'
    retained = json.loads((original / 'profile-tests/results.json').read_text())
    interpreter = Path(retained['tests'][0]['command'][0])
    if not interpreter.is_absolute() or not interpreter.is_file() or sha(interpreter) != sha(Path(sys.executable)):
        raise ValueError('Original qualification used another Python binary')
    command = [str(interpreter),
               str(origin / 'tools/firmware_matrix.py'), '--build-dir', str(original),
               '--toolchain', str(original_tools), '--native-reference', str(native_reference),
               '--output', str(matrix)]
    log = output / 'measurement.log'
    with log.open('wb') as stream:
        completed = subprocess.run(command, cwd=origin, stdout=stream, stderr=subprocess.STDOUT)
    if completed.returncode:
        raise ValueError('Canonical original-root measurement failed: ' + str(log))
    compare_sources()
    if tree(build) != snapshot or tree(original) != snapshot or sha(native_reference) != native_sha:
        raise ValueError('Measurement inputs changed')
    measured = json.loads(matrix.read_text())
    name = json.loads((build / 'build-report.json').read_text())['configuration']['profile']
    rows = [row for row in measured['profiles'] if row['profile'] == name]
    if len(rows) != 1 or rows[0].get('runtime_status') != 'exact-image-pass' or rows[0].get('offline_tests_status') != 'exact-image-pass':
        raise ValueError('Original-root image is not fully qualified')
    receipt = {'command': command, 'exit_code': completed.returncode,
               'origin_root': str(origin), 'central_build': str(build),
               'source_files': inputs, 'build_tree': snapshot,
               'matrix_sha256': sha(matrix), 'log_sha256': sha(log),
               'native_reference_sha256': native_sha, 'python_sha256': sha(interpreter),
               'physical_device_commands': 0}
    (output / 'binding.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    return rows[0]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('build', 'origin', 'toolchain', 'native-reference', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    row = measured_row(args.build, args.origin, args.toolchain, args.native_reference, args.output)
    print(json.dumps({'profile': row['profile'], 'runtime_status': row['runtime_status'],
                      'offline_tests_status': row['offline_tests_status']}))
