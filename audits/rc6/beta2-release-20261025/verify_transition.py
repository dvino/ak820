"""Offline exact-image migration preflight; reads private files, emits no settings."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/installer'))
import settings_backup as settings

parser = argparse.ArgumentParser()
parser.add_argument('--build', required=True, type=Path)
parser.add_argument('--native', required=True, type=Path)
parser.add_argument('--backup', required=True, type=Path)
parser.add_argument('--trusted-catalog', type=Path,
                    default=ROOT / 'tools/installer/settings-catalog.json')
args = parser.parse_args()
with tempfile.TemporaryDirectory() as folder:
    bundle = Path(folder)
    for part in ('firmware', 'reference', 'reports'):
        (bundle / part).mkdir()
    for source, target in (
            (args.build / 'ajazz_ak820_vial.ihx', 'firmware/application.ihx'),
            (args.build / 'ajazz_ak820_vial.map', 'firmware/application.map'),
            (args.build / 'build-report.json', 'reports/build-report.json'),
            (ROOT / 'releases/rc6/reference/vial.json', 'reference/vial.json')):
        shutil.copyfile(source, bundle / target)
    catalog = json.loads(args.trusted_catalog.read_text())
    profile = settings.load_profile(bundle, args.native.read_bytes(), trusted_catalog=catalog)
    backup = settings.validate_backup(args.backup, profile)
    plan = settings.plan_restore(backup, profile)
    result = {
        'format': 'ak820-offline-transition-preflight-1',
        'result': 'PASS', 'device_commands': 0,
        'source_identity': list(backup['source_identity']),
        'backup_manifest_sha256': backup['identity'],
        'target_identity': [profile['ihx_sha256'], profile['code_sha256']],
        'nvm_schema': profile['schema'],
        'key_count': plan['key_count'], 'encoder_count': plan['encoder_count'],
        'combo_count': (len(plan['combo_entries']) if plan['combo_entries'] is not None else
                        len(settings.combo_settings(profile['payload'][settings.pack.NVM_START-settings.pack.APP_START:
                                                                      settings.pack.NVM_END-settings.pack.APP_START])['entries_hex'])),
        'combo_action': ('restore' if plan['combo_entries'] is not None else
                         'preserve verified empty target defaults'),
        'limitations': plan['limitations'],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
