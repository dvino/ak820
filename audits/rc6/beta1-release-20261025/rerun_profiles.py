"""Repeat the complete supplemental phase after the isolated asset-tool fix."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import configure_firmware as cf

build = ROOT / 'qmk-8051-ak820/.build/beta-final/work'
tools = ROOT / 'toolchains/sdcc-4.6.0'
audit = Path(__file__).resolve().parent
change = json.loads((audit / 'supplemental-source-change.json').read_bytes())
assert set(change['changed_files']) == {'tools/build_beta_release_assets.py',
                                       'tools/test_build_beta_release_assets.py'}
assert all(cf.sha(ROOT / name) == record['after'] for name, record in change['changed_files'].items())
before = cf.source_identity()
result = cf.inspect(build, tools)
result['source'] = before
# Recheck the unchanged exact runtime proof before all supplemental regressions.
proof = cf.load_json(build / 'runtime-safety/summary.json')
cf.apply_runtime_safety(result, proof)
# The 28 base suite inputs did not change. Revalidate every passed suite/log/identity.
result['qualification'] = cf.validate_tests(build / 'qualification.json', result['identity'])
result['profile_tests'] = cf.run_profile_tests('work', build, tools, result['identity'])
cf.require(cf.source_identity() == before, 'Git source changed during supplemental rerun')
cf.apply_runtime_safety(result, proof)
result['offline_tests_passed'] = True
(build / 'configuration-report.json').write_bytes(cf.canonical(result))
cf.require_release_approval(result, cf.load_json(build / 'build-report.json'), build, tools)
record = {'format': 'ak820-beta1-current-work-qualification-1', 'passed': True,
          'scope': '28 passed base suites reused after exact validation; all30 supplemental suites rerun on final source snapshot',
          'base_qualification_sha256': cf.sha(build / 'qualification.json'),
          'configuration_sha256': cf.sha(build / 'configuration-report.json'),
          'profile_tests_sha256': cf.sha(build / 'profile-tests/results.json'),
          'runtime_summary_sha256': cf.sha(build / 'runtime-safety/summary.json'),
          'identity': result['identity'], 'base_suite_count': 28,
          'base_unit_tests': cf.load_json(build / 'qualification.json')['unit_tests'],
          'profile_suite_count': len(result['profile_tests']['suites']),
          'hardware_validated': False, 'physical_device_commands': 0}
(audit / 'current-work-qualification.json').write_bytes(cf.canonical(record))
print(json.dumps(record, sort_keys=True), flush=True)
