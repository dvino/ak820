#!/usr/bin/env python3
"""Check that post-release program policy changes bind only the publication docs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path('/home/agent/work/ak820')
base = 'dfd0770f9ef64bf5c7ab6d40e9f9e7b4354cd2cd'
sys.path[:0] = [str(root / 'tools'), str(root / 'qmk-8051-ak820/util')]
import ak820_ci_authorization as authorization
from ak820_release_manifest import host_manifest

def digest(data):
    return hashlib.sha256(data).hexdigest()

def old(path):
    return subprocess.check_output(['git', 'show', base + ':' + path], cwd=root)

def review(data):
    return json.loads(data.decode().split('```json\n', 1)[1].split('\n```', 1)[0])

docs = ('README.md', 'docs/ru/README.md', 'docs/STATUS.md', 'docs/ru/STATUS.md')
names = 'main game mmo typing code pointer onehand creative shortcuts multios'.split()
result = {}
for name in names:
    prefix = f'ci/profiles/{name}/'
    policy_bytes = (root / prefix / 'release-policy.json').read_bytes()
    current = json.loads(policy_bytes)
    previous = json.loads(old(prefix + 'release-policy.json'))
    for path in docs:
        content = (root / path).read_bytes()
        assert current['source_files'][path] == {'sha256': digest(content), 'size': len(content)}
        current['source_files'][path] = previous['source_files'][path]
    assert current == previous, name
    review_bytes = (root / prefix / 'program-review.md').read_bytes()
    now = review(review_bytes)
    before = review(old(prefix + 'program-review.md'))
    assert now['policy_sha256'] == digest(policy_bytes)
    assert now['scope'].startswith(before['scope'])
    now['scope'] = before['scope']
    now['policy_sha256'] = before['policy_sha256']
    assert now == before, name
    authorization.validate_policy(json.loads(policy_bytes), host_manifest(root),
                                  (root / prefix / 'packing-validation.json').read_bytes(), review_bytes)
    result[name] = {'previous_policy_sha256': digest(old(prefix + 'release-policy.json')),
                    'current_policy_sha256': digest(policy_bytes)}
print(json.dumps({'format': 'ak820-doc-policy-rebind-check-1', 'base_commit': base,
                  'documentation_paths': list(docs), 'profiles': result, 'status': 'passed',
                  'committed_head_validation': 'not performed', 'hardware_validated': False,
                  'physical_device_commands': 0}, indent=2, sort_keys=True))
