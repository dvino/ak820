"""Record frozen offline settings regressions and their complete source snapshot."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'qmk-8051-ak820/util')]
import configure_firmware
import ak820_release_safety
from ak820_release_manifest import HOST_FILES


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    names = (set(configure_firmware.test_source_snapshot()) |
             set(ak820_release_safety.REQUIRED_SOURCES) | set(HOST_FILES))
    names.add(Path(__file__).relative_to(ROOT).as_posix())
    return {name: digest(ROOT / name) for name in sorted(names)}


before = snapshot()
command = [sys.executable, '-B', '-m', 'unittest', 'discover',
           '-s', 'tools/installer', '-p', 'test*.py', '-v']
log = AUDIT / 'settings-tests.log'
with log.open('wb') as output:
    result = subprocess.run(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
if snapshot() != before:
    raise SystemExit('Settings test sources changed during the run')
counts = configure_firmware.unittest_counts(log.read_text())
if result.returncode == 0 and (counts['run'] == 0 or counts['skipped'] != 0):
    raise SystemExit('Settings tests are empty or skipped')
record = {'command': command, 'exit_code': result.returncode, 'source_files': before,
          'unit_tests': counts,
          'log_path': log.relative_to(ROOT).as_posix(), 'log_sha256': digest(log),
          'offline_only': True, 'physical_device_commands': 0}
(AUDIT / 'settings-run.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
raise SystemExit(result.returncode)
