#!/usr/bin/env python3
"""Verify retained inputs and collect measurements; no build or device access."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def collect(repo):
    qmk = repo / 'qmk-8051-ak820'
    audit = repo / 'audits/maximal-pass28-20261025'
    def record(path):
        return {'path': str(path.relative_to(repo)), 'sha256': sha(path), 'bytes': path.stat().st_size}
    def identity(obj, build):
        require(obj['ihx_sha256'] == sha(build / 'ajazz_ak820_vial.ihx'), 'IHX identity')
        require(obj['map_sha256'] == sha(build / 'ajazz_ak820_vial.map'), 'map identity')
        for path, value in obj.get('listing_sha256', {}).items():
            require(sha(build / path) == value, path)
    prior = repo / 'audits/maximal-pass27-20261025'
    for name in ('maximal-context.json', 'work-context.json', 'source-context-review.md', 'work-context-review.md'):
        require((audit / name).read_bytes() == (prior / name).read_bytes(), 'retained pass27 bytes: ' + name)
    rows = []
    for label, name in [('27', 'resume27-classifier'), ('28', 'resume28-keymap-firewall'), ('work', 'resume28-keymap-firewall-work'), ('27-work', 'resume27-classifier-work')]:
        build = qmk / '.build' / name
        report = json.loads((build / 'build-report.json').read_text())
        require(report['builder_sha256'] == sha(qmk / 'util/build_ak820.py'), 'builder identity')
        historical = []
        for item in report['artifacts']:
            path = qmk / item['path']
            require(path.stat().st_size == item['size'] and sha(path) == item['sha256'], str(path))
        for item in report['sources']:
            path = (qmk if item['origin'] == 'source' else repo / 'toolchains/sdcc-4.6.0') / item['path']
            if sha(path) != item['sha256']:
                require(label in ('27', '27-work') and item['origin'] == 'source' and item['path'] == 'quantum/dynamic_keymap.c', str(path))
                blob = subprocess.check_output(['git', '-C', str(repo), 'show', 'eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e:qmk-8051-ak820/' + item['path']])
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
        if label in ('28', 'work'):
            context_name = 'maximal-context.json' if label == '28' else 'work-context.json'
            require((audit / context_name).read_bytes() == (build / 'parameter-spills-context.json').read_bytes(), 'context certificate bytes')
            sys.path.insert(0, str(qmk / 'util'))
            spec = importlib.util.spec_from_file_location('spill_validator', qmk / 'util/ak820_parameter_spills.py')
            validator = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = validator
            spec.loader.exec_module(validator)
            validator.validate_context(qmk, build / 'obj_ajazz_ak820_vial', build / 'obj_ajazz_ak820_vial', repo / 'toolchains/sdcc-4.6.0', audit / context_name)
            require(report['parameter_spills']['context_sha256'] == sha(audit / context_name) and report['parameter_spills']['postlink_qualified'] is True, 'postlink context qualification')
            require(stack['analyzer_sha256'] == sha(qmk / 'tests/ak820_stack/analyze.py'), 'stack analyzer')
            spill = json.loads((build / 'parameter-spills.json').read_text())
            require(spill['postlink_qualified'] is True, 'spill postlink flag')
            with tempfile.TemporaryDirectory(prefix='ak820-pass28-collect-') as temporary:
                validator.postlink_audit(qmk, build, audit / context_name, Path(temporary) / 'postlink.json', spill, build / 'parameter-spills-stack.json')
                require(json.loads((build / 'parameter-spills.json').read_text())['postlink'] == spill['postlink'], 'actual postlink audit')
            rows[-1]['context_certificate_provenance'] = 'Byte-identical retained pass27 certificate; actual compiler ASM, tools, map and provenance revalidated; actual28 postlink audit rechecked.'

            startup = json.loads((audit / ('startup.json' if label == '28' else 'work-startup.json')).read_text())
            identity(startup['identity'], build)
            require(startup['interrupt_enables_unchanged_until_main'], 'startup IRQ enables')
            total = roots['_main'] + startup['main_entry_frame_bound'] + 3 * 17 + sum(v for k,v in roots.items() if k != '_main')
            rows[-1].update(conditional_stack_bound_bytes=total, conditional_margin_bytes=capacity-total)
            checks = json.loads((audit / ('linked-checks.json' if label == '28' else 'work-irq.json')).read_text())
            require(checks['pass'] is True, 'CPU checks')
            runner_name = 'linked-checks/runner-' + checks['runner_sha256'] + '.py' if label == '28' else 'linked-checks/work-irq-runner-' + checks['runner_sha256'] + '.py'
            require(sha(repo.parent / 'continuation-artifacts' / runner_name) == checks['runner_sha256'], 'CPU runner identity')
            require(checks['s51_sha256'] == sha(repo / 'toolchains/sdcc-4.6.0/bin/s51'), 'CPU simulator identity')
            require(checks['image_sha256'] == sha(build / 'ajazz_ak820_vial.ihx') and checks['map_sha256'] == sha(build / 'ajazz_ak820_vial.map'), 'CPU identity')
            for path,value in checks.get('support_sha256', {}).items():
                require(sha(qmk / path) == value, path)
            for path,value in checks.get('immutable_input_sha256', {}).items():
                require(sha(Path(path)) == value, path)
    require(len(rows[1]['configuration']['optional_features']) == 14, 'module count')
    require(rows[0]['configuration'] == rows[1]['configuration'] and rows[2]['configuration'] == rows[3]['configuration'], 'feature/storage configuration unchanged')
    reader = json.loads((audit / 'read-hook.json').read_text())
    require(reader['status'] == 'PASS', 'reader proof')
    require(reader['checker_sha256'] == sha(qmk / 'tests/ak820_linked_read_hook/check.py') and reader['analyzer_sha256'] == sha(qmk / 'tests/ak820_stack/analyze.py'), 'reader checker identity')
    identity(reader['code_input_hashes'], qmk / '.build/resume28-keymap-firewall')
    # The host report is one evidence object, not the prior pass's hash-map JSONL format.
    spec = importlib.util.spec_from_file_location('firewall_host', repo / 'tests/ak820_keymap_firewall/run.py')
    host_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(host_module)
    host_rows = [json.loads(line) for line in (audit / 'host-regression.jsonl').read_text().splitlines()]
    require(len(host_rows) == 1, 'host evidence rows')
    host = host_rows[0]
    host_paths = {'source_file_sha256': qmk / 'quantum/dynamic_keymap.c', 'config_file_sha256': qmk / 'keyboards/ajazz/ak820/config.h', 'keycodes_file_sha256': qmk / 'quantum/keycodes.h', 'oracle_sha256': repo / 'tests/ak820_keymap_firewall/oracle.inc', 'harness_sha256': repo / 'tests/ak820_keymap_firewall/harness.c', 'runner_sha256': repo / 'tests/ak820_keymap_firewall/run.py'}
    for key,path in host_paths.items():
        require(sha(path) == host['hashes'][key], 'host ' + key)
    require(digest(host_module.extract_function((qmk / 'quantum/dynamic_keymap.c').read_text()).encode()) == host['hashes']['current_function_sha256'], 'host function')
    require(host['base_oracle_commit'] == 'eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e', 'oracle commit')
    oracle_blob = subprocess.check_output(['git', '-C', str(repo), 'show', host['base_oracle_commit'] + ':qmk-8051-ak820/quantum/dynamic_keymap.c'])
    require(digest(host_module.extract_function(oracle_blob.decode()).encode()) == host['hashes']['oracle_sha256'], 'oracle Git identity')
    require(host['status'] == 'PASS' and host['sanitizers'] is True and len(host['mutant_checks']) == 3 and all(v['status'] == 'REJECTED' for v in host['mutant_checks'].values()) and host['qk_boot_alias_drift_check'] == 'REJECTED', 'host regression')
    target = json.loads((audit / 'keymap-linked.json').read_text())
    require(target['s51_sha256'] == sha(repo / 'toolchains/sdcc-4.6.0/bin/s51'), 'setter simulator identity')
    require(target['pass'] is True and target['case_count'] == len(target['cases']) == 600 and all(c['pass'] for c in target['cases']), 'linked firewall cases')
    require(target['immutable_inputs_unchanged'] is True and target['code_before'] == target['code_after'] and target['code_before']['bytes'] == rows[1]['code_bytes'], 'linked firewall CODE')
    external_runner = next(Path(path) for path in target['immutable_inputs'] if path.endswith('/linked-firewall/runner.py'))
    require((repo / 'tests/ak820_keymap_firewall/linked.py').read_bytes() == external_runner.read_bytes(), 'installed CPU runner bytes')
    for path,value in target['immutable_inputs'].items():
        require(sha(Path(path)) == value, 'linked firewall ' + path)
    for item in target['authenticated_sources']:
        require(item['unique_build_source_match'] and sha(qmk / item['path']) == item['sha256'], 'linked firewall source')
    require(all(c['rejected'] for c in target['keycode_alias']['in_memory_negative_checks']), 'linked alias checks')
    evidence = [record(p) for p in sorted(audit.iterdir()) if p.is_file() and p.name not in ('collect.py', 'measurements.json', 'README.md')]
    return {'format': 'ak820-pass28-measurements-1', 'collector_sha256': sha(Path(__file__)), 'builds': rows, 'evidence': evidence, 'physical_code_windows': [[0x28a0,0x3000],[0x3027,0xc700]], 'xram_limit_bytes':3072, 'baseline_source_scope':'Retained pass27 maximal/work reports: only dynamic_keymap.c may use the full eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e Git blob; all unchanged dependencies and current28 sources/tools/artifacts are verified in place.', 'whole_program_qualified':False, 'hardware_validated':False, 'physical_device_commands':0, 'installer_or_release_changes':False}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--current-output',type=Path)
    args=parser.parse_args()
    result=collect(args.repo.resolve())
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if args.current_output:
        baseline,current,work,baseline_work=result['builds']
        ledger=dict(current)
        ledger.update(format='ak820-maximal-current-4', diagnostic_only=True, installable=False, profile='maximal', module_count=14, whole_program_qualified=False, hardware_validated=False, physical_device_commands=0, installer_or_release_changes=False, iram_overlay_enabled=False, physical_code_windows=result['physical_code_windows'], xram_limit_bytes=result['xram_limit_bytes'], xram_remaining_bytes=result['xram_limit_bytes']-current['physical_xram_bytes'], delta_from_retained27={k:current[k]-baseline[k] for k in ('code_bytes','physical_xram_bytes','stack_capacity_bytes','main_overflow_bytes')}, baseline27=baseline, baseline27_work=baseline_work, catalog_control=work, work_code_delta_from_retained27=work['code_bytes']-baseline_work['code_bytes'], evidence=result['evidence'], measurements={'path':str(args.output.relative_to(args.repo)) if args.output.is_absolute() else str(args.output), 'sha256':sha(args.output)}, qualification_gates_open=[f"main CODE overflow {current['main_overflow_bytes']} bytes",'complete OEM startup and IRQ routing/non-reentry contract','opaque-writer and application-bank gates','full configured functional regressions','physical validation'])
        args.current_output.write_text(json.dumps(ledger,indent=2)+'\n')
    print('Verified retained pass27 and current pass28 maximal/work inputs and bounded evidence.')
