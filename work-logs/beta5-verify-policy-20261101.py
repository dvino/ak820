#!/usr/bin/env python3
"""Cross-check the staged offline policy tree; committed-HEAD checks remain separate."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'qmk-8051-ak820/util')]
import ak820_beta_transition_policy as transition_policy
import ak820_release_safety as safety


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


evidence = ROOT / 'audits/beta5-proof-policy-20261101'
settings = load(ROOT / 'audits/beta5-proof-settings-20261101/settings-run.json')
assert settings['exit_code'] == 0 and settings['unit_tests'] == {'run': 249, 'skipped': 0}
assert settings['offline_only'] is True and settings['physical_device_commands'] == 0
for name, digest in settings['source_files'].items():
    assert sha(safety.safe_path(ROOT, name)) == digest
assert sha(safety.safe_path(ROOT, settings['log_path'])) == settings['log_sha256']
catalog_bytes = (ROOT / 'tools/installer/settings-catalog.json').read_bytes()
assert catalog_bytes == (ROOT / 'web/firmware-matrix.json').read_bytes()
assert catalog_bytes == (evidence / 'settings-catalog-draft.json').read_bytes()
catalog = json.loads(catalog_bytes)
transitions = load(evidence / 'transition-preflight.json')
previous = load(evidence / 'previous-beta4-catalog.json')
transition_policy.validate_transition_matrix(transitions, catalog, previous)
assert len(transitions['cases']) == 200
assert len(transitions['caps_word_combo_cases']) == len(transitions['macro_layer_tap_cases']) == 100
assert transitions['hardware_validated'] is False and transitions['physical_device_commands'] == 0
names = 'main game mmo typing code pointer onehand creative shortcuts multios'.split()
results = {}
for name in names:
    installed = ROOT / 'ci/profiles' / name
    staged = evidence / 'policies' / name
    for leaf in ('release-safety.json', 'release-policy.json', 'packing-validation.json'):
        assert (installed / leaf).read_bytes() == (staged / leaf).read_bytes(), (name, leaf)
    policy = load(installed / 'release-policy.json')
    receipt = load(installed / 'packing-validation.json')
    witness = load(installed / 'release-safety.json')
    assert policy['packing_receipt_sha256'] == sha(installed / 'packing-validation.json')
    assert receipt['hardware_validated'] is False and receipt['packing']['physical_usb_opened'] is False
    assert policy['program']['ihx_sha256'] == witness['program']['ihx_sha256'] == receipt['program']['ihx_sha256']
    for records in (policy['source_files'], witness['source_files']):
        for path, expected in records.items():
            safety.checked_record(ROOT, path, expected)
    group = 'proof-profiles' if name in names[:5] else 'proof-retry-profiles'
    build = ROOT / 'qmk-8051-ak820/.build' / group / name
    report = load(build / 'build-report.json')
    safety.validate(report, root=ROOT)
    results[name] = {'ihx_sha256': witness['program']['ihx_sha256'],
                     'policy_source_records': len(policy['source_files']),
                     'safety_source_records': len(witness['source_files'])}
print(json.dumps({'status': 'passed', 'profiles': results, 'settings_tests': settings['unit_tests'],
                  'catalog_sha256': hashlib.sha256(catalog_bytes).hexdigest(),
                  'transition_cases': 200, 'caps_word_cases': 100, 'macro_layer_cases': 100,
                  'hardware_validated': False, 'physical_device_commands': 0,
                  'committed_head_validation': 'not performed', 'release_approved': False},
                 indent=2, sort_keys=True))
