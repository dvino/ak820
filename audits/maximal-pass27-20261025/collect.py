#!/usr/bin/env python3
"""Verify retained inputs and collect measurements; no build or device access."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def collect(repo):
    qmk = repo / 'qmk-8051-ak820'
    audit = repo / 'audits/maximal-pass27-20261025'
    def record(path):
        return {'path': str(path.relative_to(repo)), 'sha256': sha(path), 'bytes': path.stat().st_size}
    def identity(obj, build):
        require(obj['ihx_sha256'] == sha(build / 'ajazz_ak820_vial.ihx'), 'IHX identity')
        require(obj['map_sha256'] == sha(build / 'ajazz_ak820_vial.map'), 'map identity')
        for path, value in obj.get('listing_sha256', {}).items():
            require(sha(build / path) == value, path)
    rows = []
    for label, name in [('26b', 'resume27-baseline26b'), ('27', 'resume27-classifier'), ('work', 'resume27-classifier-work')]:
        build = qmk / '.build' / name
        report = json.loads((build / 'build-report.json').read_text())
        historical = []
        for item in report['artifacts']:
            path = qmk / item['path']
            require(path.stat().st_size == item['size'] and sha(path) == item['sha256'], str(path))
        for item in report['sources']:
            path = (qmk if item['origin'] == 'source' else repo / 'toolchains/sdcc-4.6.0') / item['path']
            if sha(path) != item['sha256']:
                require(label == '26b' and item['origin'] == 'source', str(path))
                blob = subprocess.check_output(['git', '-C', str(repo), 'show', 'cfd05a0:qmk-8051-ak820/' + item['path']])
                require(digest(blob) == item['sha256'], 'historical blob: ' + item['path'])
                historical.append(item['path'])
        mem = (build / 'ajazz_ak820_vial.mem').read_text()
        ordinary = int(re.search(r'EXTERNAL RAM\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\d+)', mem, re.I)[1])
        capacity = int(re.search(r'with (\d+) bytes available', mem)[1])
        stack = json.loads((build / 'parameter-spills-stack.json').read_text())
        identity(stack['identity'], build)
        roots = {k: v['bound'] for k, v in stack['roots'].items()}
        require(all(not v['unresolved'] for v in stack['roots'].values()), 'unresolved roots')
        stage = re.search(r'([0-9A-Fa-f]{8})\s+_ak820_flash_stage\s', (build / 'ajazz_ak820_vial.map').read_text())
        require(stage is not None, 'missing flash stage')
        stage_bytes = report['xram_window'][0] - int(stage[1], 16)
        require(stage_bytes == 64, 'flash stage extent')
        artifacts = [record(build / f) for f in ['build-report.json', 'ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map', 'ajazz_ak820_vial.mem', 'parameter-spills-stack.json']]
        rows.append({'label': label, 'build': name, 'configuration': report['configuration'], 'code_bytes': report['code_bytes'], 'code_low_bytes': report['code_low_bytes'], 'code_main_bytes': report['code_main_bytes'], 'main_highest_address': hex(report['code_max_inclusive']), 'main_overflow_bytes': max(0, report['code_max_inclusive'] + 1 - 0xc700), 'main_trailing_free_bytes': max(0, 0xc700 - report['code_max_inclusive'] - 1), 'ordinary_xram_bytes': ordinary, 'flash_stage_bytes': stage_bytes, 'physical_xram_bytes': ordinary + stage_bytes, 'stack_capacity_bytes': capacity, 'roots': roots, 'artifacts': artifacts, 'verified_artifacts': len(report['artifacts']), 'verified_source_and_toolchain_inputs': len(report['sources']), 'historical_git_blob_inputs': historical, 'source_manifest_sha256': digest(json.dumps(report['sources'], sort_keys=True).encode()), 'builder_sha256': report['builder_sha256']})
        if label in ('27', 'work'):
            context_name = 'maximal-context.json' if label == '27' else 'work-context.json'
            require((audit / context_name).read_bytes() == (build / 'parameter-spills-context.json').read_bytes(), 'context certificate bytes')
            startup = json.loads((audit / ('startup.json' if label == '27' else 'work-startup.json')).read_text())
            identity(startup['identity'], build)
            require(startup['interrupt_enables_unchanged_until_main'], 'startup IRQ enables')
            total = roots['_main'] + startup['main_entry_frame_bound'] + 3 * 17 + sum(v for k,v in roots.items() if k != '_main')
            rows[-1].update(conditional_stack_bound_bytes=total, conditional_margin_bytes=capacity-total)
            checks = json.loads((audit / ('linked-checks.json' if label == '27' else 'work-irq.json')).read_text())
            require(checks['pass'] is True, 'CPU checks')
            require(checks['image_sha256'] == sha(build / 'ajazz_ak820_vial.ihx') and checks['map_sha256'] == sha(build / 'ajazz_ak820_vial.map'), 'CPU identity')
            for path,value in checks.get('support_sha256', {}).items():
                require(sha(qmk / path) == value, path)
            for path,value in checks.get('immutable_input_sha256', {}).items():
                require(sha(Path(path)) == value, path)
    require(rows[0]['artifacts'][1]['sha256'] == '47400365dfe8e7e56fd46a548938ca8c9024467ca13120f506cb7213e9f7ef10', 'baseline reproduction')
    require(len(rows[1]['configuration']['optional_features']) == 14, 'module count')
    reader = json.loads((audit / 'read-hook.json').read_text())
    require(reader['status'] == 'PASS', 'reader proof')
    identity(reader['code_input_hashes'], qmk / '.build/resume27-classifier')
    for line in (audit / 'host-regression.jsonl').read_text().splitlines():
        item = json.loads(line)
        for path,value in item.get('sha256', {}).items():
            require(sha(Path(path)) == value, path)
    require(item.get('status') == 'PASS' and item.get('mutants_detected') == 2, 'host regression')
    evidence = [record(p) for p in sorted(audit.iterdir()) if p.is_file() and p.name not in ('collect.py', 'measurements.json', 'README.md')]
    return {'format': 'ak820-pass27-measurements-1', 'collector_sha256': sha(Path(__file__)), 'builds': rows, 'evidence': evidence, 'physical_code_windows': [[0x28a0,0x3000],[0x3027,0xc700]], 'xram_limit_bytes':3072, 'baseline_source_scope':'Current matching inputs plus cfd05a0 Git blobs for differing baseline source inputs; generated build files and artifacts verified in place.', 'whole_program_qualified':False, 'hardware_validated':False, 'physical_device_commands':0, 'installer_or_release_changes':False}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--current-output',type=Path)
    args=parser.parse_args()
    result=collect(args.repo.resolve())
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if args.current_output:
        baseline,current,work=result['builds']
        ledger=dict(current)
        ledger.update(format='ak820-maximal-current-3', diagnostic_only=True, installable=False, profile='maximal', module_count=14, whole_program_qualified=False, hardware_validated=False, physical_device_commands=0, installer_or_release_changes=False, iram_overlay_enabled=False, physical_code_windows=result['physical_code_windows'], xram_limit_bytes=result['xram_limit_bytes'], xram_remaining_bytes=result['xram_limit_bytes']-current['physical_xram_bytes'], delta_from_reproduced26b={k:current[k]-baseline[k] for k in ('code_bytes','physical_xram_bytes','stack_capacity_bytes','main_overflow_bytes')}, baseline26b=baseline, catalog_control=work, evidence=result['evidence'], measurements={'path':str(args.output.relative_to(args.repo)) if args.output.is_absolute() else str(args.output), 'sha256':sha(args.output)}, qualification_gates_open=[f"main CODE overflow {current['main_overflow_bytes']} bytes",'complete OEM startup and IRQ routing/non-reentry contract','opaque-writer and application-bank gates','full configured functional regressions','physical validation'])
        args.current_output.write_text(json.dumps(ledger,indent=2)+'\n')
    print('Verified retained baseline, maximal and work inputs and evidence.')
