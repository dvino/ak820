#!/usr/bin/env python3
"""Inspect an authentic archive; never execute packaged programs."""
import importlib.util
import json
from pathlib import Path
import sys
import tarfile

repo = Path(__file__).resolve().parents[2]
verifier = repo / 'audits/rc6/beta2-release-20261025/verify-public-assets.py'
spec = importlib.util.spec_from_file_location('verifier', verifier)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
archive = Path(sys.argv[1]).resolve()
v.check_sidecar(archive.parent, archive.name)
files, modes = v.tar_contents(archive)
with tarfile.open(archive, 'r:gz') as t:
    members = t.getmembers()
    for m in members:
        if not m.isdir():
            assert files[m.name] == t.extractfile(m).read(), m.name
            if m.isfile():
                assert modes[m.name] == m.mode, m.name
print(json.dumps({
    'format': 'ak820-public-tar-real-fixture-1',
    'archive_path': str(archive),
    'archive_sha256': v.sha(archive.read_bytes()),
    'sidecar_verified': True,
    'members': len(members),
    'flattened_files': len(files),
    'symlinks': sum(m.issym() for m in members),
    'hardlinks': sum(m.islnk() for m in members),
    'all_non_directory_bytes_match_tarfile_reference': True,
    'regular_modes_match': True,
    'verifier_sha256': v.sha(verifier.read_bytes()),
    'executed_native_binaries': False,
    'hardware_access': False,
}, indent=2))
