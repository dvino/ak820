"""Inventory retained local reports; canonical original-root measurement is separate."""
import hashlib
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parent
locations = json.loads((AUDIT / 'build-locations.json').read_text())
rows = []
for name, location in locations['profiles'].items():
    build = Path(locations['roots'][location['root']]) / location['build']
    path = build / 'configuration-report.json'
    row = {'profile': name, 'build': str(build), 'reported_offline_pass': False}
    if path.is_file():
        report = json.loads(path.read_text())
        if report.get('offline_tests_passed') is True:
            assert report['configuration']['profile'] == name
            qualification = json.loads((build / 'qualification.json').read_text())
            profiles = json.loads((build / 'profile-tests/results.json').read_text())
            assert qualification['passed'] is True and profiles['passed'] is True
            assert report['runtime_analysis']['whole_program_stack_qualified'] is True
            ihx = hashlib.sha256((build / 'ajazz_ak820_vial.ihx').read_bytes()).hexdigest()
            assert report['identity']['ihx_sha256'] == profiles['identity']['ihx_sha256'] == ihx
            row.update(reported_offline_pass=True, ihx_sha256=ihx,
                       configuration_report_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                       code_bytes=report['resources']['code_bytes'],
                       base_suites=len(qualification['tests']), unit_tests=qualification['unit_tests'],
                       profile_suites=len(profiles['tests']))
    rows.append(row)
result = {'scope': __doc__, 'profiles': rows,
          'reported_pass_count': sum(row['reported_offline_pass'] for row in rows),
          'physical_device_commands': 0, 'hardware_validated': False}
(AUDIT / 'local-build-inventory.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'reported_pass_count': result['reported_pass_count'], 'profiles': len(rows)}))
