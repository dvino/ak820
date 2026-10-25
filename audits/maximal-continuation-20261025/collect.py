#!/usr/bin/env python3
"""Collect retained exact-build measurements; never build or access a device."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(repo):
    qmk = repo / 'qmk-8051-ak820'
    toolchain = repo / 'toolchains/sdcc-4.6.0'
    builds = [
        ('22-read-on', 'resume22-read-on', 'reproduced control'),
        ('22-read-off', 'resume22-read-off', 'same-source option control'),
        ('23', 'resume23-packets-update', 'measured intermediate; not selected'),
        ('24', 'resume24-fixed-led', 'measured intermediate'),
        ('25', 'resume25-dptr', 'measured intermediate'),
        ('26b', 'resume26b-state-bytes', 'current oversized diagnostic'),
        ('work-bootstrap', 'resume26-work-bootstrap', 'trim-off context bootstrap'),
        ('work', 'resume26-work', 'current catalog control; not released'),
    ]
    rows = []
    for label, name, scope in builds:
        build = qmk / '.build' / name
        report_path = build / 'build-report.json'
        report = json.loads(report_path.read_text())
        mem = (build / 'ajazz_ak820_vial.mem').read_text()
        ordinary = int(re.search(r'EXTERNAL RAM\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\d+)', mem, re.I)[1])
        capacity = int(re.search(r'with (\d+) bytes available', mem)[1])
        artifacts = []
        for path in [report_path, *[build / ('ajazz_ak820_vial.' + ext) for ext in ('ihx', 'map', 'mem')]]:
            artifacts.append({'path': path.relative_to(repo).as_posix(), 'sha256': sha(path), 'bytes': path.stat().st_size})
        stack_path = build / 'parameter-spills-stack.json'
        roots = None
        if stack_path.exists():
            stack = json.loads(stack_path.read_text())
            assert stack['identity']['ihx_sha256'] == sha(build / 'ajazz_ak820_vial.ihx')
            roots = {name: {'bound': result['bound'], 'unresolved': result['unresolved']} for name, result in stack['roots'].items()}
            artifacts.append({'path': stack_path.relative_to(repo).as_posix(), 'sha256': sha(stack_path), 'bytes': stack_path.stat().st_size})
        checked = None
        if label in ('26b', 'work'):
            for item in report['artifacts']:
                path = qmk / item['path']
                assert path.stat().st_size == item['size'] and sha(path) == item['sha256'], path
            for item in report['sources']:
                path = (qmk if item['origin'] == 'source' else toolchain) / item['path']
                assert sha(path) == item['sha256'], path
            checked = {'all_artifacts': len(report['artifacts']), 'all_source_and_toolchain_inputs': len(report['sources'])}
        highest = report['code_max_inclusive']
        rows.append({
            'label': label, 'scope': scope, 'build': name,
            'configuration': report['configuration'],
            'code_bytes': report['code_bytes'], 'code_low_bytes': report['code_low_bytes'],
            'code_main_bytes': report['code_main_bytes'], 'main_highest_address': hex(highest),
            'main_overflow_bytes': max(0, highest + 1 - 0xc700),
            'main_trailing_free_bytes': max(0, 0xc700 - highest - 1),
            'ordinary_xram_bytes': ordinary, 'flash_stage_bytes': 64,
            'physical_xram_bytes': ordinary + 64, 'stack_capacity_bytes': capacity,
            'roots': roots, 'builder_sha256': report['builder_sha256'],
            'parameter_spills': report.get('parameter_spills'),
            'nvm_read_block_asm': report['nvm_read_block_asm'],
            'nvm_update_block_asm': report.get('nvm_update_block_asm', False),
            'source_manifest_sha256': hashlib.sha256(json.dumps(report['sources'], sort_keys=True).encode()).hexdigest(),
            'current_full_manifest_verification': checked, 'artifacts': artifacts,
        })
    baseline, current = rows[0], next(row for row in rows if row['label'] == '26b')
    assert baseline['artifacts'][1]['sha256'] == '576fd31f4ccbe85f722cf0837c688aee69c5a517694f5d8828bdc0a8d3067fe8'
    assert len(current['configuration']['optional_features']) == 14
    return {
        'format': 'ak820-continuation-measurements-1', 'date': '2026-10-25',
        'baseline_commit': '09330ab708e1eb3671571f63894c583e01743eef',
        'collector_sha256': sha(Path(__file__)), 'physical_code_windows': [[0x28a0, 0x3000], [0x3027, 0xc700]],
        'xram_limit_bytes': 3072, 'iram_overlay_enabled': False,
        'current_label': '26b', 'builds': rows,
        'delta_from_reproduced22': {key: current[key] - baseline[key] for key in ('code_bytes', 'physical_xram_bytes', 'stack_capacity_bytes', 'main_overflow_bytes')},
        'failed_attempts': [{'build': 'resume26-state-bytes', 'reason': 'Empty dce-input staging directory existed after rename; copytree rejected it. Fresh26b completed without weakening guards.'}],
        'whole_program_qualified': False, 'hardware_validated': False,
        'full_configured_regressions': 'blocked by maximal CODE and incomplete OEM startup/IRQ, bank and opaque-writer contracts',
        'physical_device_commands': 0, 'installer_or_release_changes': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.repo.resolve())
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'current': result['current_label'], 'delta': result['delta_from_reproduced22'], 'builds': len(result['builds'])}))
