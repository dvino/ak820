#!/usr/bin/env python3
"""Check retained bytes and source identities without running firmware or USB."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(base, name):
    path = (base / name).resolve()
    require(path.is_relative_to(base), 'Path escapes evidence root: ' + name)
    return path


def main():
    checked_files = 0
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        require(sha(local(HERE, name).read_bytes()) == expected, 'Changed file: ' + name)
        checked_files += 1
    frozen = read(HERE / 'frozen-sources.json')['repository_files']
    for name, expected in frozen.items():
        require(sha(local(ROOT, name).read_bytes()) == expected, 'Changed source: ' + name)
    matrix = read(HERE / 'matrix.json')
    rows = matrix['variants']
    require(len(rows) == matrix['variant_count'] == 12, 'Wrong variant count')
    require(len({r['profile'] for r in rows}) == matrix['profile_count'] == 11,
            'Wrong profile count')
    require(len({r['id'] for r in rows}) == len(rows), 'Duplicate variant')
    raw_count = raw_bytes = 0
    for row in rows:
        directory = local(HERE, row['evidence_directory'])
        ledger = read(directory / 'files.json')
        archive = local(directory, ledger['archive']['path'])
        require(archive.stat().st_size == ledger['archive']['size'] and
                sha(archive.read_bytes()) == ledger['archive']['sha256'],
                'Changed raw archive: ' + row['id'])
        expected = {'build/' + item['path']: item for item in ledger['files']}
        require(len(expected) == len(ledger['files']), 'Duplicate raw path')
        seen = set()
        with gzip.open(archive, 'rb') as stream:
            with tarfile.open(fileobj=stream, mode='r|') as tar:
                for member in tar:
                    require(member.isfile() and member.name in expected and
                            member.name not in seen, 'Unexpected raw member: ' + member.name)
                    item = expected[member.name]
                    content = tar.extractfile(member).read()
                    require(len(content) == item['size'] == member.size and
                            sha(content) == item['sha256'] and member.mode == item['mode'],
                            'Changed raw member: ' + member.name)
                    seen.add(member.name)
                    raw_count += 1
                    raw_bytes += len(content)
        require(seen == set(expected), 'Missing raw members: ' + row['id'])
        for original, copied in ledger['copies'].items():
            require(sha(local(directory, copied).read_bytes()) == expected['build/' + original]['sha256'],
                    'Changed report copy: ' + copied)
        config = read(directory / 'configuration-report.json')
        require(config['identity'] == row['identity'] and config['resources'] == row['resources'],
                'Matrix differs from exact configuration: ' + row['id'])
        require(config['offline_tests_passed'] and not config['release_approved'] and
                not config['hardware_validated'] and config['physical_device_commands'] == 0,
                'Wrong qualification boundary: ' + row['id'])
        qualification = read(directory / 'qualification.json')
        require(qualification['passed'] and qualification['build_unchanged'] and
                len(qualification['tests']) == 28 and
                qualification['unit_tests'] == {'run': 273, 'skipped': 0},
                'Base qualification differs: ' + row['id'])
        profile = read(directory / 'profile-tests.json')
        require(profile['passed'] and profile['identity'] == config['identity'] and
                [test['id'] for test in profile['tests']] == row['profile_tests']['suites'] and
                all(test['exit_code'] == 0 for test in profile['tests']),
                'Supplemental qualification differs: ' + row['id'])
        for test in profile['tests']:
            item = expected['build/profile-tests/' + test['id'] + '.log']
            require(item['sha256'] == test['log_sha256'] and
                    test['build_before'] == test['build_after'] == config['identity'],
                    'Changed supplemental log or build identity: ' + test['id'])
    print(json.dumps({'passed': True, 'variant_count': len(rows),
                      'profile_count': matrix['profile_count'],
                      'checked_evidence_files': checked_files,
                      'checked_repository_sources': len(frozen),
                      'checked_raw_files': raw_count, 'checked_raw_bytes': raw_bytes,
                      'physical_device_commands': 0}, indent=2))


if __name__ == '__main__':
    main()
