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


def validate_getter_target(repo, audit, current):
    target = json.loads((audit / 'getter-linked.json').read_text())
    require(target['pass'] is True and target['cases'] == 2431 and target['shards'] == 8, 'linked getter aggregate')
    external = Path('/home/danil/ChatGPT/ak820-pass29-research-20261025/linked-getters')
    require((audit / 'getter-linked.json').read_bytes() == (external / 'results.json').read_bytes(), 'getter aggregate exact copy')
    require((audit / 'getter-linked-SHA256SUMS').read_bytes() == (external / 'SHA256SUMS').read_bytes(), 'getter manifest exact copy')
    manifest = (audit / 'getter-linked-SHA256SUMS').read_text().splitlines()
    require(len(manifest) == 102, 'getter retained file count')
    for line in manifest:
        value,path = line.split('  ',1)
        require(sha(external / path) == value, 'getter retained evidence ' + path)
    require((repo / 'tests/ak820_getter_bounds/linked.py').read_bytes() == (external / 'run.py').read_bytes(), 'installed getter CPU runner exact bytes')
    require(target['runner_sha256'] == sha(external / 'run.py') and target['image_sha256'] == sha(repo / 'qmk-8051-ak820/.build/resume29-getter-bounds/ajazz_ak820_vial.ihx') and target['build_manifest_sha256'] == sha(repo / 'qmk-8051-ak820/.build/resume29-getter-bounds/build-report.json'), 'getter aggregate input bindings')
    reports = [json.loads((external / f'final/shard-{i}/results.json').read_text()) for i in range(8)]
    allcases = []
    entries = 0
    for i,report in enumerate(reports):
        require(report['pass'] is True and report['immutable_inputs_unchanged'] is True, 'getter shard PASS')
        require(report['shard_index'] == i and report['shard_count'] == 8 and report['total_case_count'] == 2431, 'getter shard scope')
        require(report['code_before'] == report['code_after'] == target['code_before'] == target['code_after'] and report['code_before']['bytes'] == current['code_bytes'], 'getter full CODE preserved')
        require(report['immutable_inputs'] == reports[0]['immutable_inputs'], 'getter shared inputs')
        for path,value in report['immutable_inputs'].items():
            resolved = repo / path[len('/repo/'):] if path.startswith('/repo/') else external / path[len('/out/'):] if path.startswith('/out/') else Path(path)
            require(sha(resolved) == value, 'linked getter input ' + path)
        for item in report['authenticated_sources']:
            require(sha(repo / 'qmk-8051-ak820' / item['path']) == item['sha256'], 'linked getter source')
        cases = report['cases']
        require(report['case_count'] == len(cases) and all(c['pass'] for c in cases), 'getter shard cases')
        map_path = next(k for k in report['immutable_inputs'] if k.endswith('ajazz_ak820_vial.map'))
        mapping = (repo / map_path.removeprefix('/repo/')).read_text()
        reader = int(re.search(r'^\s*(?:C:)?\s*([0-9A-F]{8})\s+_eeprom_read_byte\b', mapping, re.M)[1],16)
        observed = []
        for block in re.split(r'(?=Stop at 0x)', (external / f'final/shard-{i}/cpu.log').read_text()):
            stop = re.match(r'Stop at 0x([0-9a-fA-F]+):',block)
            if not stop or int(stop[1],16) != reader:
                continue
            b = re.search(r'\bB= 0x([0-9a-fA-F]+)',block)
            dp = re.search(r'DPTR= 0x([0-9a-fA-F]+)',block)
            require(b and dp and int(b[1],16) == 0, 'getter actual reader pointer ABI')
            observed.append(int(dp[1],16))
        require(observed == [address for case in cases for address in case['reads']], 'getter actual ordered reads')
        require(target['trace_checks'][i] == {'shard':i,'reader_entries':len(observed),'generic_pointer_B_zero':True,'ordered_DPTR_matches_report':True}, 'getter aggregate trace binding')
        entries += len(observed)
        allcases.extend(cases)
    tuples = {(c['target'],*c['args']) for c in allcases}
    expected = {('keymap',l,r,c) for l in range(6) for r in range(16) for c in range(8)}
    expected |= {('keymap',*(bad if k == axis else 0 for k in range(3))) for axis,bound in enumerate((6,16,8)) for bad in (bound,bound+1,127,254,255)}
    expected |= {('encodermap',l,0,b) for l in range(6) for b in range(256)}
    expected |= {('encodermap',l,e,b) for l in (0,5,6,7,127,255) for e in (0,1,2,127,255) for b in (0,1,2,255) if l >= 6 or e != 0}
    require(len(allcases) == len(tuples) == 2431 and tuples == expected, 'getter exact case set')
    require(target['reader_entries'] == entries, 'getter aggregate reader count')
    require(target['valid_matrix'] == 768 and target['invalid_matrix_axis_boundaries'] == 15 and target['valid_encoder_all_raw_bytes'] == 1536 and target['invalid_encoder_boundary_samples'] == 112, 'getter aggregate coverage')


def collect(repo):
    qmk = repo / 'qmk-8051-ak820'
    audit = repo / 'audits/maximal-pass29-20261025'
    def record(path):
        return {'path': str(path.relative_to(repo)), 'sha256': sha(path), 'bytes': path.stat().st_size}
    def identity(obj, build):
        require(obj['ihx_sha256'] == sha(build / 'ajazz_ak820_vial.ihx'), 'IHX identity')
        require(obj['map_sha256'] == sha(build / 'ajazz_ak820_vial.map'), 'map identity')
        for path, value in obj.get('listing_sha256', {}).items():
            require(sha(build / path) == value, path)
    prior = repo / 'audits/maximal-pass28-20261025'
    for name in ('maximal-context.json', 'work-context.json', 'source-context-review.md', 'work-context-review.md'):
        require((audit / name).read_bytes() == (prior / name).read_bytes(), 'retained pass28 bytes: ' + name)
    rows = []
    for label, name in [('28', 'resume28-keymap-firewall'), ('29', 'resume29-getter-bounds'), ('work', 'resume29-getter-bounds-work'), ('28-work', 'resume28-keymap-firewall-work')]:
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
                require(label in ('28', '28-work') and item['origin'] == 'source' and item['path'] == 'quantum/dynamic_keymap.c', str(path))
                blob = subprocess.check_output(['git', '-C', str(repo), 'show', '6c2cdc0452b664e37cd32a30b31e3e5f800c49cc:qmk-8051-ak820/' + item['path']])
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
        if label in ('29', 'work'):
            context_name = 'maximal-context.json' if label == '29' else 'work-context.json'
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
            with tempfile.TemporaryDirectory(prefix='ak820-pass29-collect-') as temporary:
                validator.postlink_audit(qmk, build, audit / context_name, Path(temporary) / 'postlink.json', spill, build / 'parameter-spills-stack.json')
                require(json.loads((build / 'parameter-spills.json').read_text())['postlink'] == spill['postlink'], 'actual postlink audit')
            rows[-1]['context_certificate_provenance'] = 'Byte-identical retained pass27 certificate; actual compiler ASM, tools, map and provenance revalidated; actual29 postlink audit rechecked.'

            startup = json.loads((audit / ('startup.json' if label == '29' else 'work-startup.json')).read_text())
            identity(startup['identity'], build)
            require(startup['interrupt_enables_unchanged_until_main'], 'startup IRQ enables')
            require(startup['checker_sha256'] == sha(qmk / 'tests/ak820_startup/stack_contract.py') and startup['analyzer_sha256'] == sha(qmk / 'tests/ak820_stack/analyze.py'), 'startup tools')
            total = roots['_main'] + startup['main_entry_frame_bound'] + 3 * 17 + sum(v for k,v in roots.items() if k != '_main')
            rows[-1].update(conditional_stack_bound_bytes=total, conditional_margin_bytes=capacity-total)
            checks = json.loads((audit / ('linked-checks.json' if label == '29' else 'work-irq.json')).read_text())
            require(checks['pass'] is True, 'CPU checks')
            if label == '29':
                require(checks['immutable_inputs_unchanged'] is True, 'CPU inputs unchanged')
                require(checks['code_integrity_sessions'] == 20 and checks['occupied_code_ge_c700_bytes'] == rows[-1]['main_overflow_bytes'] and all(n == rows[-1]['main_overflow_bytes'] for n in checks['occupied_code_ge_c700_unchanged_per_session']), 'CPU overflow CODE sessions')
            else:
                require(checks['build_report_sha256'] == sha(build / 'build-report.json') and checks['inputs_unchanged'] is True, 'work CPU identity')
                require(len(checks['full_occupied_CODE_integrity_sessions']) == 17 and all(n == report['code_bytes'] for n in checks['full_occupied_CODE_integrity_sessions']), 'work full occupied CODE sessions')
            runner_name = 'linked-checks/runner-' + checks['runner_sha256'] + '.py' if label == '29' else 'linked-checks/work-irq-runner-' + checks['runner_sha256'] + '.py'
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
    require(reader['status'] == 'PASS' and len(reader['proof']['reachable_instructions']) == 45 and len(reader['mutations']) == 7 and all(v['rejected'] is True for v in reader['mutations'].values()), 'reader proof and mutants')
    require(reader['checker_sha256'] == sha(qmk / 'tests/ak820_linked_read_hook/check.py') and reader['analyzer_sha256'] == sha(qmk / 'tests/ak820_stack/analyze.py'), 'reader checker identity')
    identity(reader['code_input_hashes'], qmk / '.build/resume29-getter-bounds')
    host_rows = [json.loads(line) for line in (audit / 'host-regression.jsonl').read_text().splitlines()]
    host = next(r for r in host_rows if r['kind'] == 'sources')
    runner = repo / 'tests/ak820_getter_bounds/run.py'
    require(sha(runner) == host['test_runner_sha256'], 'host executed runner')
    spec = importlib.util.spec_from_file_location('getter_host', runner)
    host_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(host_module)
    require(digest(host_module.wrappers((qmk / 'quantum/dynamic_keymap.c').read_text()).encode()) == host['candidate_wrappers_sha256'], 'host extracted wrappers')
    require(bool(host['compiler_version']) and bool(host['compiler']), 'host compiler identity')
    if host['compiler'][0] == 'docker':
        require(re.fullmatch(r'sha256:[0-9a-f]{64}', host['container_image_id']) is not None, 'host Docker image identity')
    else:
        context = json.loads((audit / 'host-execution-context.json').read_text())
        require((audit / 'host-execution-context.json').read_bytes() == (repo.parent / 'getter29-host-execution-context.json').read_bytes(), 'outer host execution context')
        require(context['probe_return_code'] == 0 and context['network'] == 'none' and re.fullmatch(r'sha256:[0-9a-f]{64}', context['image_id']) is not None, 'outer compiler container identity')
        require(host['compiler_version'] in context['compiler_identity_probe_stdout'] and re.search(r'[0-9a-f]{64}  /usr/bin/gcc',context['compiler_identity_probe_stdout']), 'outer compiler binary identity')
    for path,value in host['current_sha256'].items():
        require(sha(repo / path) == value, 'getter host source ' + path)
    require(host['oracle_commit'] == '6c2cdc0452b664e37cd32a30b31e3e5f800c49cc', 'getter oracle commit')
    blob = subprocess.check_output(['git','-C',str(repo),'show',host['oracle_commit']+':qmk-8051-ak820/quantum/dynamic_keymap.c'])
    require(digest(blob) == host['oracle_file_sha256'] and digest(host_module.wrappers(blob.decode()).encode()) == host['oracle_wrappers_sha256'], 'getter oracle blob/wrappers')
    variants = [r for r in host_rows if r['kind'] == 'variant']
    require(len(variants) == 4 and all(r['result'].startswith('PASS cases=33554432 ') for r in variants), 'getter host variants')
    coverage = next(r for r in host_rows if r['kind'] == 'coverage')
    require(coverage['exhaustive_comparisons'] == 134217728 and coverage['target_cpu_execution'] is False, 'getter host coverage')
    negatives = [r for r in host_rows if r['kind'] == 'negative_control']
    require(len(negatives) == 3 and all(r['rejected'] is True for r in negatives), 'getter host mutants')
    sanitizer = next(r for r in host_rows if r['kind'] == 'sanitizers')
    require(sanitizer['flags'] == ['address','undefined'] and sanitizer['result'].startswith('PASS cases=33554432 '), 'getter generic sanitizers')
    for item in json.loads((audit / 'verification-tools.json').read_text()):
        require(sha(Path(item['path'])) == item['sha256'], 'verification tool ' + item['path'])
    validate_getter_target(repo, audit, rows[1])
    evidence = [record(p) for p in sorted(audit.iterdir()) if p.is_file() and p.name not in ('collect.py', 'measurements.json', 'README.md')]
    return {'format': 'ak820-pass29-measurements-1', 'collector_sha256': sha(Path(__file__)), 'builds': rows, 'evidence': evidence, 'physical_code_windows': [[0x28a0,0x3000],[0x3027,0xc700]], 'xram_limit_bytes':3072, 'baseline_source_scope':'Retained pass28 maximal/work reports: only dynamic_keymap.c may use the full 6c2cdc0452b664e37cd32a30b31e3e5f800c49cc Git blob; all unchanged dependencies and current29 sources/tools/artifacts are verified in place.', 'whole_program_qualified':False, 'hardware_validated':False, 'physical_device_commands':0, 'installer_or_release_changes':False}


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
        ledger.update(format='ak820-maximal-current-4', diagnostic_only=True, installable=False, profile='maximal', module_count=14, whole_program_qualified=False, hardware_validated=False, physical_device_commands=0, installer_or_release_changes=False, iram_overlay_enabled=False, physical_code_windows=result['physical_code_windows'], xram_limit_bytes=result['xram_limit_bytes'], xram_remaining_bytes=result['xram_limit_bytes']-current['physical_xram_bytes'], delta_from_retained28={k:current[k]-baseline[k] for k in ('code_bytes','physical_xram_bytes','stack_capacity_bytes','main_overflow_bytes')}, baseline28=baseline, baseline28_work=baseline_work, catalog_control=work, work_code_delta_from_retained28=work['code_bytes']-baseline_work['code_bytes'], evidence=result['evidence'], measurements={'path':str(args.output.relative_to(args.repo)) if args.output.is_absolute() else str(args.output), 'sha256':sha(args.output)}, qualification_gates_open=[f"main CODE overflow {current['main_overflow_bytes']} bytes",'complete OEM startup and IRQ routing/non-reentry contract','opaque-writer and application-bank gates','full configured functional regressions','physical validation'])
        args.current_output.write_text(json.dumps(ledger,indent=2)+'\n')
    print('Verified retained pass28 and current pass29 maximal/work inputs and bounded evidence.')
