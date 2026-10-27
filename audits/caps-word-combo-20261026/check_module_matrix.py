"""Check both documented module matrices against the current profile registry."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
import ak820_profiles as profiles

names = profiles.RELEASE_PROFILES
enabled = {name: set(profiles.configuration(name)['optional_features']) for name in names}
modules = set().union(*enabled.values())
documents = {}
for relative in ('docs/MODULE-MATRIX.md', 'docs/ru/MODULE-MATRIX.md'):
    path = ROOT / relative
    rows = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| '):
            continue
        cells = [value.strip() for value in line.strip('|').split('|')]
        if cells[0] in modules:
            assert cells[0] not in rows, 'Duplicate module: ' + relative
            rows[cells[0]] = cells[1:]
    assert set(rows) == modules, 'Missing module: ' + relative
    for module, cells in rows.items():
        assert cells == ['✓' if module in enabled[name] else '—' for name in names], (relative, module)
    documents[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
result = {'passed': True, 'profiles': list(names), 'modules': sorted(modules),
          'document_sha256': documents, 'physical_device_commands': 0}
Path(__file__).with_name('module-matrix-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
