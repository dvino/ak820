#!/usr/bin/env python3
"""Verify downloaded beta.5 release assets and compare ten IHX files to retained builds."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path('/home/agent/ak820-beta5-release-verification-20261101')
PROOF = Path('/home/agent/ak820-beta5-proof-20261101')
assets = ROOT / 'assets'
metadata = json.loads((ROOT / 'release-metadata.json').read_text())
assert metadata['tagName'] == 'v0.6.0-beta.5' and metadata['isPrerelease'] is True
commit = 'dfd0770f9ef64bf5c7ab6d40e9f9e7b4354cd2cd'
ci = json.loads((ROOT / 'ci-run.json').read_text())
assert ci['headSha'] == commit and ci['event'] == 'push' and ci['headBranch'] == 'v0.6.0-beta.5'
assert ci['status'] == 'completed' and ci['conclusion'] == 'success'
assert next(j for j in ci['jobs'] if j['name'] == 'Publish tagged version from main')['conclusion'] == 'success'
refs = dict(line.split('\t', 1)[::-1] for line in (ROOT / 'tag-ref.txt').read_text().splitlines())
assert refs['refs/tags/v0.6.0-beta.5^{}'] == commit

def digest(data):
    return hashlib.sha256(data).hexdigest()

items = {}
for item in metadata['assets']:
    data = (assets / item['name']).read_bytes()
    value = digest(data)
    assert item['size'] == len(data) and item['digest'] == 'sha256:' + value, item['name']
    items[item['name']] = {'size': len(data), 'sha256': value}
assert len(items) == 16 and {p.name for p in assets.iterdir()} == set(items)
for path in assets.glob('*.sha256'):
    expected, target = path.read_text().split()
    assert digest((assets / target.lstrip('*')).read_bytes()) == expected

with zipfile.ZipFile(assets / 'AK820-Beta5-Catalog.zip') as catalog:
    assert len(catalog.namelist()) == len(set(catalog.namelist()))
    catalog_names = set(catalog.namelist())
    lines = (assets / 'SHA256SUMS').read_text().splitlines()
    for line in lines:
        expected, name = line.split('  ', 1)
        assert not name.startswith('/') and '..' not in Path(name).parts
        data = catalog.read(name) if name in catalog_names else (assets / name).read_bytes()
        assert digest(data) == expected, name

names = 'main game mmo typing code pointer onehand creative shortcuts multios'.split()
profiles = {}
with zipfile.ZipFile(assets / 'firmware-bundle.zip') as bundle:
    assert len(bundle.namelist()) == len(set(bundle.namelist()))
    present = {name.split('/')[1] for name in bundle.namelist()
               if name.startswith('profiles/') and name.endswith('/firmware/application.ihx')}
    assert present == set(names)
    for name in names:
        group = 'proof-profiles' if name in names[:5] else 'proof-retry-profiles'
        local = PROOF / 'qmk-8051-ak820/.build' / group / name / 'ajazz_ak820_vial.ihx'
        remote = bundle.read(f'profiles/{name}/firmware/application.ihx')
        assert remote == local.read_bytes(), name
        profiles[name] = digest(remote)

print(json.dumps({'format': 'ak820-beta5-downloaded-release-check-1',
                  'release': metadata['url'], 'published_at': metadata['publishedAt'],
                  'tag': metadata['tagName'], 'source_commit': commit,
                  'ci_run': ci['url'], 'provenance': 'checked against retained GitHub run and remote tag query',
                  'assets': items, 'sha256sums_entries': len(lines), 'profiles': profiles,
                  'comparison': 'downloaded IHX byte-for-byte equals retained offline-qualified build',
                  'hardware_validated': False, 'physical_device_commands': 0, 'status': 'passed'},
                 indent=2, sort_keys=True))
