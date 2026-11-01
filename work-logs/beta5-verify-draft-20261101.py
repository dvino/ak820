#!/usr/bin/env python3
"""Read-only draft evidence cross-check; emits hashes and assertions, not ROM bytes."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path[:0] = ['/src/tools', '/src/qmk-8051-ak820/util']
import ak820_beta_transition_policy as policy
import pack_ak820 as pack

root = Path('/audit')
review = Path('/review')
private = Path('/private')
base = Path('/src/qmk-8051-ak820/.build')
archives = Path('/predecessor')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):
    return json.loads(path.read_text())

hashes = {}
for name in ('previous-beta4-catalog.json', 'packing-preflight.json', 'settings-catalog-draft.json', 'transition-preflight.json'):
    original, copied = root / name, review / name
    assert original.read_bytes() == copied.read_bytes(), name
    hashes[name] = sha(original)
assert hashes['previous-beta4-catalog.json'] == '8bf90526a51e9879870a61d7de1c59b1df38e3489b77a67e67496503f0307658'
assert sha(archives / 'AK820-Beta4.1-Catalog.zip') == '064ead1c4f5ec0aebdaa318b5a406e7caec9f597495b33c0d3f10dbccc859e9e'
assert sha(archives / 'firmware-bundle.zip') == 'fa18b3aa28fd9f805bfc99711f67dcf25dd85835a77982eed8d2d92c4f1e41ce'
with zipfile.ZipFile(archives / 'AK820-Beta4.1-Catalog.zip') as published:
    assert published.read('settings-catalog.json') == (root / 'previous-beta4-catalog.json').read_bytes()
catalog = load(root / 'settings-catalog-draft.json')
previous = load(root / 'previous-beta4-catalog.json')
transitions = load(root / 'transition-preflight.json')
packing = load(root / 'packing-preflight.json')
measured = load(base / 'requal-combined-measurements.json')
policy.validate_transition_matrix(transitions, catalog, previous)
current = {row['profile']: row for row in catalog['profiles']}
old = {row['profile']: row for row in previous['profiles']}
names = {'main', 'game', 'mmo', 'typing', 'code', 'pointer', 'onehand', 'creative', 'shortcuts', 'multios'}
assert set(current) == set(old) == names and len(catalog['historical_profiles']) == 10
assert catalog['historical_profiles'] == previous['profiles'] and not catalog['historical_sources']
assert catalog['complete_module_coverage'] and not catalog['uncovered_modules']
assert set(measured['profiles']) == names and measured['hardware_validated'] is False and measured['physical_device_commands'] == 0
assert transitions['hardware_validated'] is False and transitions['physical_device_commands'] == 0
assert packing['hardware_validated'] is False and packing['physical_device_commands'] == 0
for key in ('caps_word_combo_cases', 'macro_layer_tap_cases'):
    cases = transitions[key]
    assert len(cases) == 100 and {(x['source_profile'], x['target_profile']) for x in cases} == {(a, b) for a in names for b in names}
    assert all(x['passed'] is True for x in cases)
assert len(transitions['cases']) == 200 and all(x['passed'] is True for x in transitions['cases'])
assert len({(x['source'], x['target']) for x in transitions['cases']}) == 200
stock = Path('/reference/stock-full.bin').read_bytes()
assert hashlib.sha256(stock).hexdigest() == '1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1'
assert sha(Path('/reference/native-installed.bin')) == 'd7152819712470cf37a0c29d69b756edc4a51aca1d20c13e1fcf4b96f9638535'
assert Path('/reference/native-installed.bin').read_bytes() == stock[pack.APP_START:pack.APP_END]
profile_results = {}
assert len(packing['profiles']) == 10
for item in packing['profiles']:
    name = item['profile']
    assert name in names and name not in profile_results
    row = current[name]
    observed = measured['profiles'][name]
    assert row['settings_identity'] == observed['settings_identity']
    assert item['build'] == observed['identity']
    assert observed['measurement_status'] == 'linked-memory-pass' and observed['runtime_status'] == 'exact-image-pass' and observed['offline_tests_status'] == 'exact-image-pass'
    assert item['hardware_validated'] is False and item['physical_device_commands'] == 0
    folder = private / 'packed' / name
    for leaf, key in (('ak820-vial-permanent.bin', 'permanent'), ('ak820-vial-trial.bin', 'trial')):
        payload = (folder / leaf).read_bytes()
        assert pack.verify_payload(payload, target_build_id=item['schema']) == item[key], (name, key)
    assert (folder / 'restore-native.bin').read_bytes() == stock[pack.APP_START:pack.APP_END]
    assert item['recovery_sha256'] == hashlib.sha256(stock[pack.APP_START:pack.APP_END]).hexdigest()
    assert item['settings_code_sha256'] == row['settings_identity']['code_sha256']
    profile_results[name] = {'ihx_sha256': observed['identity']['ihx_sha256'], 'code_sha256': item['settings_code_sha256'],
                             'permanent_sha256': item['permanent']['sha256'], 'trial_sha256': item['trial']['sha256']}
assert set(profile_results) == names
assert (base / 'requal-source-before.json').read_bytes() == (base / 'requal-source-after.json').read_bytes()
assert (base / 'requal-identities-before.json').read_bytes() == (base / 'requal-identities-after.json').read_bytes()
for name in names:
    assert (base / 'requal-output' / (name + '.exit')).read_text().strip() == '0'
assert (base / 'requalification.exit').read_text().strip() == '0'
print(json.dumps({'status': 'passed', 'hashes': hashes, 'profiles': profile_results,
    'transition_cases': 200, 'caps_word_cases': 100, 'macro_layer_cases': 100,
    'predecessor_archive_sha256': ['064ead1c4f5ec0aebdaa318b5a406e7caec9f597495b33c0d3f10dbccc859e9e', 'fa18b3aa28fd9f805bfc99711f67dcf25dd85835a77982eed8d2d92c4f1e41ce'],
    'physical_device_commands': 0, 'release_approved': False}, indent=2, sort_keys=True))
