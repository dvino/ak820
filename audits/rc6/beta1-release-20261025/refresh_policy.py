"""Refresh policy inputs for independent review; never grants approval."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
from ak820_release_manifest import host_manifest
from ak820_ci_authorization import symbols_sha256


def record(path):
    data = path.read_bytes()
    return {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    args = parser.parse_args()
    build = args.build_dir.resolve()
    report = json.loads((build / 'build-report.json').read_bytes())
    policy_path = ROOT / 'ci/release-policy.json'
    previous = json.loads(policy_path.read_bytes())
    names = {n for n in previous['source_files'] if (ROOT / n).is_file()}
    safety = json.loads((ROOT / 'ci/release-safety.json').read_bytes())
    names.update(safety['source_files'])
    names.update(row['path'] for row in safety['witnesses'].values())
    transition = json.loads((ROOT / safety['witnesses']['transition']['path']).read_bytes())
    names.add(transition['actual_alpha2_preflight']['result_path'])
    names.update(test['log_path'] for test in transition['tests'])
    names.update(host_manifest(ROOT))
    names.update(('ci/release-safety.json', 'qmk-8051-ak820/dependencies/lufa.json',
                  '.github/workflows/windows-installer.yml', '.github/workflows/firmware-catalog.yml'))
    for directory in ('tools', 'qmk-8051-ak820/tests'):
        names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / directory).rglob('*')
                     if path.is_file() and path.suffix in ('.py', '.c', '.h', '.inc'))
    for row in report['sources']:
        if row['origin'] == 'source' and not row['path'].startswith('.build/'):
            name = 'qmk-8051-ak820/' + row['path']
            if record(ROOT / name)['sha256'] != row['sha256']:
                raise ValueError('Compiled input changed: ' + name)
            names.add(name)
    receipt = ROOT / 'ci/packing-receipt.json'
    policy = {'format': 'ak820-ci-program-policy-1',
              'program': {'ihx_sha256': record(build / 'ajazz_ak820_vial.ihx')['sha256'],
                          'symbols_sha256': symbols_sha256(build / 'ajazz_ak820_vial.map'),
                          'schema': report['build_id'], 'keyboard': 'ajazz/ak820',
                          'keymap': 'vial', 'sdcc_version': '4.6.0'},
              'host_files': host_manifest(ROOT),
              'packing_receipt_sha256': record(receipt)['sha256'],
              'source_files': {name: record(ROOT / name) for name in sorted(names)}}
    policy_path.write_text(json.dumps(policy, indent=2) + '\n')
    print(json.dumps({'policy_sha256': record(policy_path)['sha256'],
                      'source_records': len(names), 'host_records': len(policy['host_files']),
                      'approval_generated': False}))


if __name__ == '__main__':
    main()
