"""Shared offline release identities; no USB access or approval generation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

RELEASE = 'rc6'
MANIFEST_FORMAT = 'ak820-installer-release-2'
HOST_FILES = frozenset((
    'AK820.sh', 'AK820.cmd',
    'tools/build_ci_release.py', 'qmk-8051-ak820/util/ak820_ci_authorization.py',
    'tools/build_release_bundle.py', 'tools/build_windows_installer.py', 'tools/installer/requirements-build-windows.txt',
    'tools/build_linux_installer.py', 'tools/installer/requirements-build-linux.txt',
    'qmk-8051-ak820/util/ak820_profiles.py', 'qmk-8051-ak820/util/ak820_extension_settings.py',
    'tools/installer/ak820.py', 'tools/installer/gui.py', 'tools/installer/i18n.py',
    'tools/ak820_device_protocol.py', 'tools/installer/settings_backup.py',
    'tools/installer/settings_workflow.py',
    'tools/installer/profile-catalog.json', 'tools/installer/settings-catalog.json',
    'tools/installer/requirements.txt', 'tools/installer/70-ak820.rules',
    'qmk-8051-ak820/util/ak820_tool.py', 'qmk-8051-ak820/util/ak820_diagnose.py',
    'qmk-8051-ak820/util/pack_ak820.py', 'qmk-8051-ak820/util/prepare_ak820_trial.py',
    'qmk-8051-ak820/util/native_macro_import.py', 'qmk-8051-ak820/util/ak820_release_manifest.py',
))


def host_manifest(root: Path) -> dict:
    records = {}
    for name in sorted(HOST_FILES):
        data = (root / name).read_bytes()
        records[name] = {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return records


def validate_host_manifest(manifest: dict, root: Path) -> None:
    recorded = manifest.get('host_files')
    if not isinstance(recorded, dict) or set(recorded) != HOST_FILES:
        raise ValueError('Incomplete or unexpected host-code manifest')
    actual = host_manifest(root)
    for name in sorted(HOST_FILES):
        if recorded[name] != actual[name]:
            raise ValueError('Host code differs from the reviewed release: ' + name)


def read_review_record(text: str) -> dict:
    records = []
    for block in re.findall(r'^```json\s*\n(.*?)^```\s*$', text, flags=re.MULTILINE | re.DOTALL):
        record = json.loads(block)
        if isinstance(record, dict) and record.get('format') in ('ak820-offline-review-2', 'ak820-reproduced-review-1'):
            records.append(record)
    if len(records) != 1:
        raise ValueError('Review must contain exactly one supported offline review JSON record')
    record = records[0]
    if (record.get('status') != 'passed' or record.get('hardware_validated') is not False
            or record.get('release') != RELEASE):
        raise ValueError('Review is not a completed offline pass')
    return record
