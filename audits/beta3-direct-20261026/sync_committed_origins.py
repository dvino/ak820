from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path('/workspace/scratch/772c1403f0df/ak820')
BASE = 'b35b77cddbefdb509058f1fbaaeafaa3982ce172'
RECEIPT = Path('/tmp/ak820-beta3-committed-origin-sync.json')
commit = sys.argv[1]
if not re.fullmatch('[0-9a-f]{40}', commit):
    raise SystemExit('Pass the full committed source identity')
if RECEIPT.exists() or RECEIPT.is_symlink():
    raise SystemExit('Committed-origin sync receipt must be fresh')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def owned_path(origin, name):
    relative = Path(name)
    assert relative.parts and not relative.is_absolute() and '..' not in relative.parts
    target = origin / relative
    current = target
    while current != origin:
        assert not current.is_symlink(), str(current)
        current = current.parent
    assert origin.is_dir() and not origin.is_symlink() and origin.resolve() == origin
    return target

assert git(ROOT, 'rev-parse', 'HEAD').decode().strip() == commit
assert not git(ROOT, 'status', '--porcelain', '--untracked-files=no')
entries = []
for line in git(ROOT, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
    if not line:
        continue
    meta, name = line.split(b'\t', 1)
    mode, kind, oid = meta.split()
    assert mode in (b'100644', b'100755') and kind == b'blob'
    name = name.decode()
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    source = ROOT / name
    assert source.is_file() and not source.is_symlink()
    data = source.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid.decode()
    entries.append((name, int(mode, 8), oid.decode()))
names = {name for name, _, _ in entries}
reports = []
for group in 'abc':
    origin = Path('/tmp/ak820-beta3-isolated') / group
    assert origin.is_dir() and not origin.is_symlink() and origin.resolve() == origin
    assert git(origin, 'rev-parse', 'HEAD').decode().strip() == BASE
    assert git(origin, 'cat-file', '-t', commit).strip() == b'commit'
    old = {name.decode() for name in git(origin, 'ls-files', '-z').split(b'\0') if name}
    removed, copied, linked = [], [], []
    for name in sorted(old - names):
        target = owned_path(origin, name)
        target.unlink(missing_ok=True)
        removed.append(name)
    for name, mode, oid in entries:
        source, target = ROOT / name, owned_path(origin, name)
        source_data = source.read_bytes()
        if not target.is_file() or target.read_bytes() != source_data:
            target.parent.mkdir(parents=True, exist_ok=True)
            if name.startswith('audits/beta3-direct-20261026/final-linked-evidence/') and name.endswith('.tar.gz'):
                target.unlink(missing_ok=True)
                os.link(source, target)
                linked.append(name)
            else:
                shutil.copyfile(source, target)
                copied.append(name)
        target.chmod(mode & 0o777)
        data = target.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid
    git(origin, 'reset', '--mixed', commit)
    assert not git(origin, 'status', '--porcelain', '--untracked-files=no')
    reports.append({'group': group, 'origin': str(origin), 'source_commit': commit,
                    'tracked_files_verified': len(entries), 'copied': copied,
                    'linked_immutable_archives': linked, 'removed_old_tracked_paths': removed,
                    'tracked_tree_clean': True})
    print(group, 'exact committed source synced', len(entries), flush=True)
with RECEIPT.open('x', encoding='utf-8') as stream:
    stream.write(json.dumps({'status': 'PASS', 'source_commit': commit, 'groups': reports},
                           indent=2, sort_keys=True) + '\n')
