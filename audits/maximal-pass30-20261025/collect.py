#!/usr/bin/env python3
"""Validate fresh paired builds and bounded evidence; no build or device access."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(Path(path).read_bytes())


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text())


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def ihx_bytes(path):
    result, base = {}, 0
    for line in Path(path).read_text().splitlines():
        raw = bytes.fromhex(line[1:])
        require(line.startswith(':') and sum(raw) % 256 == 0 and len(raw) == raw[0]+5, 'IHX record')
        address, kind = int.from_bytes(raw[1:3], 'big'), raw[3]
        if kind == 0:
            for i, value in enumerate(raw[4:-1]):
                require(base+address+i not in result, 'overlapping IHX')
                result[base+address+i] = value
        elif kind == 4:
            base = int.from_bytes(raw[4:-1], 'big') << 16
        else:
            require(kind == 1, 'unsupported IHX record')
    return result


def identity(obj, build):
    require(obj['ihx_sha256'] == sha(build/'ajazz_ak820_vial.ihx'), 'IHX binding')
    require(obj['map_sha256'] == sha(build/'ajazz_ak820_vial.map'), 'map binding')
    for path, value in obj.get('listing_sha256', {}).items():
        require(sha(build/path) == value, 'listing binding '+path)


def generation(qmk, build, report):
    gen = load(build/'default-keymap/generation.json')
    helper = module(qmk/'util/ak820_default_keymap.py', 'default_generator')
    require(gen['generator_sha256'] == sha(qmk/'util/ak820_default_keymap.py'), 'generator identity')
    require(gen['compiler_sha256'] == sha(gen['bootstrap_command'][0]) == report['compiler_sha256'], 'generator compiler')
    for name, field in [('bootstrap.asm','bootstrap_sha256'),('bootstrap.d','dependency_sha256'),('ak820_default_keymap.inc','include_sha256'),('final-discovery.d','final_dependency_sha256')]:
        require(sha(build/'default-keymap'/name) == gen[field], 'generation artifact '+name)
    for field in ('dependencies','final_dependencies'):
        for path, value in gen[field].items():
            require(sha(path) == value, 'generation dependency '+path)
    for command in ('dependency_command','bootstrap_command','final_command','final_dependency_command'):
        require(gen[command][0] == gen['bootstrap_command'][0], 'compiler command identity')
    require('-DAK820_DEFAULT_KEYMAP_EXTRACT' in gen['bootstrap_command'] and '-DAK820_DEFAULT_KEYMAP_EXTRACT' not in gen['final_command'], 'private extraction phase')
    include = str((build/'default-keymap/ak820_default_keymap.inc').resolve())
    bootstrap_paths, final_paths = set(gen['dependencies']),set(gen['final_dependencies'])
    require(final_paths-bootstrap_paths == {include} and not bootstrap_paths-final_paths, 'compiler dependency closure difference')
    require(gen['generated_dependency_difference'] == gen['final_only_dependencies'] == [include] and gen['bootstrap_only_dependencies'] == [], 'recorded phase difference')
    require(gen['final_tables_verified'] is True, 'final table marker')
    bootstrap = (build/'default-keymap/bootstrap.asm').read_text()
    final = (build/'obj_ajazz_ak820_vial/quantum/keymap_introspection.asm').read_text()
    require(helper.literal_block(bootstrap,'_ak820_default_metadata') == [16,8,2,2,0,1], 'resolved dimensions/constants')
    original = helper.literal_block(bootstrap,'_keymaps')
    require(len(original) == 512, 'resolved 256 default words')
    expected = helper.encode(original,[16,8,2,2,0,1])
    helper.verify_final(final, bootstrap)
    require(helper.generate(bootstrap) == (build/'default-keymap/ak820_default_keymap.inc').read_text(), 'generated include exact bytes')
    code = ihx_bytes(build/'ajazz_ak820_vial.ihx')
    mapping = (build/'dce/quantum/keymap_introspection.rst').read_text()
    for name, values in zip(('classes','payload','offsets'),expected):
        symbol = '_ak820_default_'+name
        match = re.search(r'^\s*([0-9A-Fa-f]{6})\s+\d+\s+'+symbol+r':',mapping,re.M)
        require(match, 'linked compressed symbol '+symbol)
        address=int(match[1],16)
        require([code.get(address+i) for i in range(len(values))] == values, 'linked compressed bytes '+name)
    require(not re.search(r'^\s*(?:C:)?\s*[0-9A-Fa-f]{8}\s+_keymaps\b',mapping,re.M), 'original defaults not linked')
    manifest = {x['path']:x for x in report['sources'] if x['origin']=='source'}
    require('util/ak820_default_keymap.py' in manifest, 'generator in input manifest')
    return {'resolved_words':256,'classes_bytes':len(expected[0]),'payload_bytes':len(expected[1]),'offsets_bytes':len(expected[2]),'bootstrap_sha256':sha(build/'default-keymap/bootstrap.asm'),'generation_sha256':sha(build/'default-keymap/generation.json'),'command_sha256':{key:digest(json.dumps(gen[key],sort_keys=True).encode()) for key in ('dependency_command','bootstrap_command','final_command','final_dependency_command')},'bootstrap_dependency_count':len(bootstrap_paths),'final_dependency_count':len(final_paths),'linked_tables_exact':True,'original_defaults_linked':False}


def validate_cpu(repo, audit, rows):
    qmk=repo/'qmk-8051-ak820'
    for label, filename, external_name in [('30','linked-checks.json','default30-linked-checks'),('work','work-irq.json','default30-work-irq')]:
        row=next(x for x in rows if x['label']==label);build=qmk/'.build'/row['build']
        path=audit/filename;checks=load(path)
        require(path.read_bytes()==(repo.parent/external_name/'results.json').read_bytes(),'original CPU report '+filename)
        require(checks['pass'] is True and checks['image_sha256']==sha(build/'ajazz_ak820_vial.ihx') and checks['map_sha256']==sha(build/'ajazz_ak820_vial.map'),'CPU image binding')
        require(checks['s51_sha256']==sha(repo/'toolchains/sdcc-4.6.0/bin/s51'),'CPU simulator')
        runner_name=('runner-' if label=='30' else 'work-irq-runner-')+checks['runner_sha256']+'.py'
        require(sha(repo.parent/'continuation-artifacts/linked-checks'/runner_name)==checks['runner_sha256'],'executed CPU runner')
        for path,value in checks.get('support_sha256',{}).items():
            require(sha(qmk/path)==value,'CPU support '+path)
        for path,value in checks.get('immutable_input_sha256',{}).items():
            require(sha(path)==value,'CPU immutable input '+path)
        if label=='30':
            require(checks['immutable_inputs_unchanged'] is True and checks['code_integrity_sessions']==20,'max CPU sessions')
            require(checks['occupied_code_ge_c700_bytes']==row['main_overflow_bytes'] and checks['occupied_code_ge_c700_unchanged_per_session']==[row['main_overflow_bytes']]*20,'max CPU overflow preservation')
        else:
            require(checks['build_report_sha256']==sha(build/'build-report.json') and checks['inputs_unchanged'] is True,'work CPU manifest')
            require(checks['full_occupied_CODE_integrity_sessions']==[row['code_bytes']]*17,'work full CODE preservation')
    external=repo.parent/'default30-linked-decoder';summary=load(audit/'decoder-linked.json')
    require((audit/'decoder-linked.json').read_bytes()==(external/'summary.json').read_bytes(),'decoder summary original bytes')
    require((audit/'decoder-linked-SHA256SUMS').read_bytes()==(external/'SHA256SUMS').read_bytes(),'decoder external manifest original bytes')
    for line in (audit/'decoder-linked-SHA256SUMS').read_text().splitlines():
        value,path=line.split('  ',1);require(sha(external/path)==value,'decoder retained file '+path)
    require(summary['pass'] is True and summary['shards']==4 and summary['cases_per_image']==275 and summary['total_cpu_invocations']==550,'decoder summary scope')
    require(summary['runner_sha256']==sha(external/'run.py'),'decoder executed runner')
    require((repo/'tests/ak820_default_keymap/linked.py').read_bytes()==(external/'run.py').read_bytes(),'installed linked runner exact executed bytes')
    images=[qmk/'.build'/name for name in ('resume30-default-keymap','resume30-default-keymap-control')]
    require(summary['image_sha256']==[sha(x/'ajazz_ak820_vial.ihx') for x in images],'decoder summary images')
    helper=module(qmk/'util/ak820_default_keymap.py','decoder_generator')
    bootstrap=(images[0]/'default-keymap/bootstrap.asm').read_text();raw=helper.literal_block(bootstrap,'_keymaps')
    expected={(l,r,c) for l in range(2) for r in range(16) for c in range(8)}
    expected|={(l,0,0) for l in (2,3,4,5,6,127,254,255)}
    expected|={(0,r,0) for r in (16,17,127,254,255)}
    expected|={(0,0,c) for c in (8,9,127,254,255)}
    expected.add((255,255,255));require(len(expected)==275,'decoder expected coverage')
    cases=[[],[]]
    for shard in range(4):
        report=load(external/f'accepted-shard-{shard}/results.json')
        require(report['pass'] is True and report['immutable_inputs_unchanged'] is True and report['total_cases_per_image']==275,'decoder shard pass')
        for path,value in report['immutable_inputs'].items():
            require(sha(path)==value,'decoder immutable '+path)
        for index, image in enumerate(report['images']):
            require(image['image_sha256']==summary['image_sha256'][index] and image['pass'] is True,'decoder shard image')
            require(image['code_before']==image['code_after'] and image['code_before']['bytes']==len(ihx_bytes(images[index]/'ajazz_ak820_vial.ihx')),'decoder complete CODE preserved')
            for case in image['cases']:
                l,r,c=case['args'];valid=l<2 and r<16 and c<8;i=((l*16+r)*8+c)*2
                value=(raw[i]|raw[i+1]<<8) if valid else 1
                require(case['pass'] is True and case['return']==value and case['DPL']+(case['DPH']<<8)==value and case['valid'] is valid,'decoder exact return')
            cases[index]+=image['cases']
    for image_cases in cases:
        require(len(image_cases)==275 and {tuple(c['args']) for c in image_cases}==expected,'decoder all exact cases')
    ordered=[{tuple(c['args']):c for c in values} for values in cases]
    valid=[x for x in expected if x[0]<2 and x[1]<16 and x[2]<8]
    for field in ('ticks','instructions'):
        left=[ordered[0][x][field] for x in valid];right=[ordered[1][x][field] for x in valid];delta=[a-b for a,b in zip(left,right)]
        measured={'decoder_min':min(left),'decoder_max':max(left),'decoder_sum_256':sum(left),'control_min':min(right),'control_max':max(right),'control_sum_256':sum(right),'delta_min':min(delta),'delta_max':max(delta),'delta_sum_256':sum(delta),'delta_mean':sum(delta)/256}
        require(summary['cost_reset_default_lookup_component_only'][field]==measured,'decoder measured component cost '+field)
    require(summary['raw_layer_count']=={'value':2,'cpu_executable':False,'reason':'DCE eliminated keymap_layer_count_raw; bootstrap metadata and linked bounds prove two.'},'raw count static-only scope')
    for item in load(audit/'external-evidence.json'):
        require(Path(item['path']).stat().st_size==item['bytes'] and sha(item['path'])==item['sha256'],'external evidence '+item['path'])


def validate_host_and_extra(repo,audit):
    host=load(audit/'host-checks.json')
    require(host['pass'] is True and len(host['commands'])==3,'native host result')
    require((audit/'host-checks.json').read_bytes()==(repo.parent/'default30-host-checks.json').read_bytes(),'host report original bytes')
    for path,value in host['input_sha256'].items():
        require(sha(path)==value,'native current input '+path)
    for index,command in enumerate(host['commands']):
        require(command['returncode']==0 and '--network=none' in command['argv'] and 'sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d' in command['argv'],'offline host command')
        require(sha(command['log'])==command['log_sha256']==sha(audit/f'host-check-{index}.log'),'native log '+str(index))
    require('Ran 7 tests' in (audit/'host-check-0.log').read_text() and 'OK' in (audit/'host-check-0.log').read_text(),'seven generator tests')
    require('PASS: integrated getter, all 16777216 uint8 triples' in (audit/'host-check-1.log').read_text(),'native decoder exhaustive PASS')
    require(re.search(r'[0-9a-f]{64}\s+/usr/bin/gcc',(audit/'host-check-2.log').read_text()),'native compiler binary identity')
    checks=load(audit/'translation-unit-checks.json')
    require(all(checks[k] is True for k in ('clean','incremental_stale_replaced','option_off_table_original','encoder_unchanged','led_unchanged','private_phase_indirect_rejected','final_only_header_change_rejected')) and checks['hardware'] is False,'actual TU checks')
    require((audit/'translation-unit-checks.json').read_bytes()==(repo/'qmk-8051-ak820/.build/default30-tu-fix-final/checks.json').read_bytes(),'actual TU checks bytes')
    research=Path('/home/danil/ChatGPT/ak820-bounded-final-passes-20261025')
    first=load(audit/'extra-pass1-event.json');second=load(audit/'extra-pass2-protocol.json')
    for number,name in ((1,'pass1-event'),(2,'pass2-protocol')):
        stem='extra-pass1-event' if number==1 else 'extra-pass2-protocol'
        for suffix,external in (('.json','results.json'),('.md','README.md')):
            require((audit/(stem+suffix)).read_bytes()==(research/name/external).read_bytes(),'extra pass exact report')
    require(first['cases']==12288 and first['baseline']['trace_sha256']==first['candidate']['trace_sha256'],'event bounded trace equality')
    require(all(first[k]['killed'] is True for k in ('no_zero_fallback','wrong_update','missing_consumed_post')),'event mutants')
    for path,value in first['sha256'].items():
        require(sha(research/'pass1-event'/path)==value,'event actual input '+path)
    for field,path in [('git-bb91d89-action.c','quantum/action.c'),('git-bb91d89-quantum.c','quantum/quantum.c')]:
        require(sha(repo/'qmk-8051-ak820'/path)==first['source_sha256'][field],'event actual source unchanged '+path)
    def area(item,name):
        return int(next(re.fullmatch(r'A '+name+r' size ([0-9a-fA-F]+) flags \w+ addr \w+',s)[1] for s in item['areas'] if s.startswith('A '+name+' size ')),16)
    require(area(first['baseline'],'CSEG')==565 and area(first['candidate'],'CSEG')==627,'event component growth')
    require(all(area(first['baseline'],n)==area(first['candidate'],n) for n in ('DSEG','BSEG','XSEG')),'event component RAM unchanged')
    require(second['status']=='NO_ELIGIBLE_WEIGHTY_VARIANT' and second['candidate_patch'] is None and second['full_build_run'] is False and second['component_compile_run'] is False and second['variant_count']==0,'protocol no candidate')
    for item in second['source_proof']:
        require(sha(repo/'qmk-8051-ak820'/item['path'])==item['current_sha256']==item['frozen_sha256'] and item['current_matches_frozen'] is True,'protocol current source '+item['path'])
    for item in second['authenticated_listings']:
        require(sha(item['path'])==item['sha256'],'protocol historical listing')
    require(second['image29_ihx_sha256']==sha(repo/'qmk-8051-ak820/.build/resume29-getter-bounds/ajazz_ak820_vial.ihx'),'protocol historical image')
    require(second['loop_total_bytes']==42 and second['idealized_loop_sharing_ceiling_bytes']==28,'protocol specific loops only')
    return {'additional_passes_completed':2,'extra_pass1':'REJECTED: one event-chain candidate grows standalone CSEG 565 to 627; no integration/full build','extra_pass2':'NO_ELIGIBLE_WEIGHTY_VARIANT: no patch or compile; three specific loops total42/ideal sharing ceiling28 only','integrated_code_saving_bytes':201,'substantial_gain_reference_bytes':512,'conditional_stop':'Pause after recording and reviewing this packet; objective remains incomplete. No claim of a global compression minimum.'}


def collect(repo):
    qmk=repo/'qmk-8051-ak820'
    audit=repo/'audits/maximal-pass30-20261025'
    def record(path):
        return {'path':str(path.relative_to(repo)),'sha256':sha(path),'bytes':path.stat().st_size}
    rows=[]
    sys.path.insert(0,str(qmk/'util'))
    validator=module(qmk/'util/ak820_parameter_spills.py','spill_validator')
    for name in ('maximal-context.json','work-context.json','source-context-review.md','work-context-review.md'):
        require((audit/name).read_bytes() == (repo/'audits/maximal-pass29-20261025'/name).read_bytes(), 'retained certificate exact '+name)
    for label,name,enabled in [('control','resume30-default-keymap-control',False),('30','resume30-default-keymap',True),('work','resume30-default-keymap-work',True),('work-control','resume30-default-keymap-work-control',False)]:
        build=qmk/'.build'/name
        report=load(build/'build-report.json')
        require(report['compress_default_keymap'] is enabled,'paired compression flag')
        require(report['builder_sha256'] == sha(qmk/'util/build_ak820.py'),'current builder')
        for item in report['artifacts']:
            path=qmk/item['path']
            require(path.stat().st_size == item['size'] and sha(path) == item['sha256'],'build artifact '+str(path))
        for item in report['sources']:
            path=(qmk if item['origin']=='source' else repo/'toolchains/sdcc-4.6.0')/item['path']
            require(sha(path) == item['sha256'],'current build source '+str(path))
        stack=load(build/'parameter-spills-stack.json');identity(stack['identity'],build)
        require(all(not v['unresolved'] for v in stack['roots'].values()),'resolved stack roots')
        mem=(build/'ajazz_ak820_vial.mem').read_text();mapping=(build/'ajazz_ak820_vial.map').read_text()
        ordinary=int(re.search(r'EXTERNAL RAM\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\d+)',mem,re.I)[1])
        capacity=int(re.search(r'with (\d+) bytes available',mem)[1])
        stage=re.search(r'([0-9A-Fa-f]{8})\s+_ak820_flash_stage\s',mapping)
        require(stage and report['xram_window'][0]-int(stage[1],16)==64,'flash stage extent')
        row={'label':label,'build':name,'configuration':report['configuration'],'compress_default_keymap':enabled,'code_bytes':report['code_bytes'],'code_low_bytes':report['code_low_bytes'],'code_main_bytes':report['code_main_bytes'],'main_highest_address':hex(report['code_max_inclusive']),'main_overflow_bytes':max(0,report['code_max_inclusive']+1-0xc700),'main_trailing_free_bytes':max(0,0xc700-report['code_max_inclusive']-1),'ordinary_xram_bytes':ordinary,'flash_stage_bytes':64,'physical_xram_bytes':ordinary+64,'stack_capacity_bytes':capacity,'roots':{k:v['bound'] for k,v in stack['roots'].items()},'artifacts':[record(build/f) for f in ('build-report.json','ajazz_ak820_vial.ihx','ajazz_ak820_vial.map','ajazz_ak820_vial.mem','parameter-spills-stack.json')],'verified_artifacts':len(report['artifacts']),'verified_source_and_toolchain_inputs':len(report['sources']),'source_manifest_sha256':digest(json.dumps(report['sources'],sort_keys=True).encode()),'builder_sha256':report['builder_sha256']}
        if enabled:
            row['default_generation']=generation(qmk,build,report)
            context=audit/('maximal-context.json' if label=='30' else 'work-context.json')
            require(context.read_bytes() == (build/'parameter-spills-context.json').read_bytes(),'retained build context')
            validator.validate_context(qmk,build/'obj_ajazz_ak820_vial',build/'obj_ajazz_ak820_vial',repo/'toolchains/sdcc-4.6.0',context)
            require(report['parameter_spills']['context_sha256']==sha(context) and report['parameter_spills']['postlink_qualified'] is True,'postlink context qualification')
            spill=load(build/'parameter-spills.json')
            with tempfile.TemporaryDirectory(prefix='ak820-pass30-collect-') as temporary:
                validator.postlink_audit(qmk,build,context,Path(temporary)/'postlink.json',spill,build/'parameter-spills-stack.json')
                require(load(build/'parameter-spills.json')['postlink']==spill['postlink'],'fresh actual postlink audit')
            row['context_certificate_provenance']='Byte-identical retained pass27 certificate; actual compiler ASM, tools, map and provenance revalidated; actual30 postlink audit rechecked.'
            startup=load(audit/('startup.json' if label=='30' else 'work-startup.json'));identity(startup['identity'],build)
            require(startup['interrupt_enables_unchanged_until_main'],'startup interrupt enable state')
            require(startup['checker_sha256']==sha(qmk/'tests/ak820_startup/stack_contract.py') and startup['analyzer_sha256']==sha(qmk/'tests/ak820_stack/analyze.py'),'startup tools')
            require(stack['analyzer_sha256']==sha(qmk/'tests/ak820_stack/analyze.py'),'stack analyzer')
            total=sum(row['roots'].values())+startup['main_entry_frame_bound']+3*17
            row.update(conditional_stack_bound_bytes=total,conditional_margin_bytes=capacity-total)
        rows.append(row)
    helper=module(qmk/'util/ak820_default_keymap.py','paired_default_generator')
    for on,off in ((rows[1],rows[0]),(rows[2],rows[3])):
        enabled=qmk/'.build'/on['build'];control=qmk/'.build'/off['build']
        bootstrap=(enabled/'default-keymap/bootstrap.asm').read_text()
        enabled_asm=(enabled/'obj_ajazz_ak820_vial/quantum/keymap_introspection.asm').read_text()
        control_asm=(control/'obj_ajazz_ak820_vial/quantum/keymap_introspection.asm').read_text()
        require(helper.literal_block(bootstrap,'_keymaps')==helper.literal_block(control_asm,'_keymaps'),'paired current original defaults')
        for symbol in ('_encoder_map','_ak820_led_points'):
            original=helper.literal_block(control_asm,symbol)
            require(helper.literal_block(enabled_asm,symbol)==original,'paired original encoder/LED ASM')
            for build in (enabled,control):
                listing=(build/'dce/quantum/keymap_introspection.rst').read_text()
                match=re.search(r'^\s*([0-9A-Fa-f]{6})\s+\d+\s+'+symbol+r':',listing,re.M)
                require(match,'paired linked encoder/LED symbol')
                address=int(match[1],16);code=ihx_bytes(build/'ajazz_ak820_vial.ihx')
                require([code.get(address+i) for i in range(len(original))]==original,'paired linked encoder/LED exact bytes')
    require(rows[0]['configuration']==rows[1]['configuration'] and rows[2]['configuration']==rows[3]['configuration'],'paired feature/storage configuration')
    require(len(rows[1]['configuration']['optional_features'])==14,'all optional modules')
    reader=load(audit/'read-hook.json');identity(reader['code_input_hashes'],qmk/'.build/resume30-default-keymap')
    require(reader['status']=='PASS' and len(reader['proof']['reachable_instructions'])==45 and len(reader['mutations'])==7 and all(v['rejected'] for v in reader['mutations'].values()),'reader proof and mutants')
    require(reader['checker_sha256']==sha(qmk/'tests/ak820_linked_read_hook/check.py') and reader['analyzer_sha256']==sha(qmk/'tests/ak820_stack/analyze.py'),'reader tools')
    validate_cpu(repo,audit,rows)
    stopping=validate_host_and_extra(repo,audit)
    evidence=[record(p) for p in sorted(audit.iterdir()) if p.is_file() and p.name not in ('collect.py','measurements.json','README.md')]
    return {'format':'ak820-pass30-measurements-1','collector_sha256':sha(Path(__file__)),'builds':rows,'bounded_passes_and_stop':stopping,'evidence':evidence,'physical_code_windows':[[0x28a0,0x3000],[0x3027,0xc700]],'xram_limit_bytes':3072,'baseline_source_scope':'All four fresh paired builds use the current source/toolchain manifest; no historical source fallback. Compression is off for the control pair and on for the current pair.','whole_program_qualified':False,'hardware_validated':False,'physical_device_commands':0,'installer_or_release_changes':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--current-output',type=Path)
    args=parser.parse_args();repo=args.repo.resolve();result=collect(repo)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if args.current_output:
        baseline,current,work,baseline_work=result['builds'];ledger=dict(current)
        ledger.update(format='ak820-maximal-current-5',diagnostic_only=True,installable=False,profile='maximal',module_count=14,whole_program_qualified=False,hardware_validated=False,physical_device_commands=0,installer_or_release_changes=False,iram_overlay_enabled=False,physical_code_windows=result['physical_code_windows'],xram_limit_bytes=result['xram_limit_bytes'],xram_remaining_bytes=result['xram_limit_bytes']-current['physical_xram_bytes'],delta_from_same_source_control={k:current[k]-baseline[k] for k in ('code_bytes','physical_xram_bytes','stack_capacity_bytes','main_overflow_bytes')},same_source_control=baseline,same_source_work_control=baseline_work,catalog_control=work,work_code_delta_from_same_source_control=work['code_bytes']-baseline_work['code_bytes'],bounded_passes_and_stop=result['bounded_passes_and_stop'],evidence=result['evidence'],measurements={'path':str(args.output.relative_to(repo)) if args.output.is_absolute() else str(args.output),'sha256':sha(args.output)},qualification_gates_open=[f"main CODE overflow {current['main_overflow_bytes']} bytes",'complete OEM startup and IRQ routing/non-reentry contract','opaque-writer and application-bank gates','full configured functional regressions','physical validation'])
        args.current_output.write_text(json.dumps(ledger,indent=2)+'\n')
    print('Verified current paired default-keymap builds and bounded evidence.')
