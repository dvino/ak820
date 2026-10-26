#!/usr/bin/env python3
"""Read-only existing-evidence validator. Never produces review or runs producers."""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, shutil, tempfile
from pathlib import Path
R = Path('/home/danil/ChatGPT/ak820-beta2-20261025')
T = Path('/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max/toolchains/sdcc-4.6.0')
sys.path[:0] = [str(R/'tools'), str(R/'qmk-8051-ak820/util')]
import configure_firmware as cf
import build_ci_release as ci
import ak820_release_safety as safety
import ak820_ci_authorization as auth
import ak820_profiles as profiles
from ak820_release_manifest import host_manifest
GROUPS = {'a':('main','game','mmo','creative'),'b':('typing','code','multios'),'c':('pointer','onehand','shortcuts')}
ORDER = ('main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios')
HISTORICAL_SOURCES = {
    'alpha2-saved-rom': ('f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e', '6ff7b1653925da7dc12bdb6f7ef5fc1dc4319c5b931def50c68b9cf45c4054d7'),
    'alpha3-packed': ('d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18', '01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d'),
    'beta1-work-packed': ('652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880', 'a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10'),
}
A = R/'audits/rc6/beta2-release-20261025'
seen = {}
PRECOMMIT = False
def sha(p):
    p=Path(p); data=p.read_bytes(); value=hashlib.sha256(data).hexdigest()
    if p in seen and seen[p] != value: raise ValueError('input changed during validation: '+str(p))
    seen[p]=value; return value
def load(p):
    sha(p); return cf.load_json(Path(p))
def need(v,m):
    if not v: raise ValueError(m)
def current(snapshot):
    need(isinstance(snapshot,dict) and snapshot,'empty source snapshot')
    for n,h in snapshot.items(): need(sha(safety.safe_path(R,n)) == h,'stale source: '+n)
def stage(out,name,fn):
    try: out[name]=fn()
    except Exception as e: out.setdefault('errors',[]).append({'gate':name,'error':type(e).__name__+': '+str(e)})
def copy(root,n,source):
    # Destination lexical validation before mkdir; no evidence symlinks accepted.
    need(not Path(n).is_absolute() and all(x not in ('','..','.') for x in n.split('/')),'unsafe scratch path')
    source=Path(source); need(source.is_file() and not source.is_symlink(),'unsafe/missing copy source '+str(source))
    sha(source); dest=root/n; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,dest)
def check_profile(p,g,snapshot,packing,matrix,catalog):
    out={'profile':p}; B=R.parent/f'ak820-beta2-qualified-{g}-20261025/qmk-8051-ak820/.build/next-{p}-release2-certified'
    original=B.parents[2]; directory=R/'ci/profiles'/p
    def run():
        d=load(B.parent/'beta2-qualification-final'/f'{p}.json')
        need(d.get('profile')==p and d.get('build')==str(B),'wrong final run profile/build')
        need(d.get('exit_code')==0 and d.get('capture_streams_separated') is True and d.get('image_unchanged') is True and d.get('compiler_tmp_on_large_storage') is True,'final run incomplete/failed/unsafe capture')
        need(d.get('ihx_sha256')==sha(B/'ajazz_ak820_vial.ihx'),'final run image hash differs')
        need(d.get('capture_module_sha256')==sha(R/'qmk-8051-ak820/util/ak820_parameter_spills.py'),'stale final capture utility')
        need(d.get('hardware_validated') is False and d.get('physical_device_commands')==0,'invalid device scope')
        log=Path(d['log']); need(log==B.parent/'beta2-qualification-final'/f'{p}.log','wrong final log path'); sha(log)
        return {'record_sha256':sha(B.parent/'beta2-qualification-final'/f'{p}.json'),'log_sha256':sha(log)}
    stage(out,'final_run',run)
    try:
        report=load(B/'build-report.json'); config=load(B/'configuration-report.json'); ident=config['identity']
    except Exception as e: out.setdefault('errors',[]).append({'gate':'inputs','error':str(e)}); out['passed']=False; return out
    def build():
        selected=profiles.configuration(p)
        need(report['configuration']==selected and config['configuration']==selected,'configuration differs')
        need(report['keyboard']=='ajazz/ak820' and report['keymap']=='vial' and ' 4.6.0 ' in report['compiler_version'] and report['build_id']==selected['nvm_schema'] and report['hardware_validated'] is False,'wrong target/toolchain/schema/scope')
        for row in report['artifacts']:
            n=row['path']; need(n.startswith('.build/'+B.name+'/'),'artifact outside canonical build')
            need(sha(safety.safe_path(original/'qmk-8051-ak820',n))==row['sha256'] and (original/'qmk-8051-ak820'/n).stat().st_size==row['size'],'artifact mismatch '+n)
        expected={'profile':p,'configuration_sha256':hashlib.sha256(cf.canonical(selected)).hexdigest(),'build_report_sha256':sha(B/'build-report.json'),'source_manifest_sha256':hashlib.sha256(cf.canonical(report['sources'])).hexdigest(),'compiler_sha256':report['compiler_sha256'],'nvm_schema':selected['nvm_schema']}
        expected.update({e+'_sha256':sha(B/('ajazz_ak820_vial.'+e)) for e in ('ihx','map','mem')})
        need(ident==expected,'stable configuration identity differs')
        need(config.get('hardware_validated') is False and config.get('physical_device_commands')==0,'configuration device scope differs')
        return expected
    def toolchain_mapping():
        producer=original/'toolchains/sdcc-4.6.0'
        pins={'sdcc':ci.release.SDCC46_PINS['sdcc'],'sdas8051':ci.release.SDCC46_PINS['sdas8051'],'s51':ci.SDCC46_S51_SHA256}
        actual={name:sha(T/'bin'/name) for name in pins}
        need(actual==pins,'actual mapped toolchain differs from binary pins')
        need(report['compiler_sha256']==pins['sdcc'] and report['assembler_sha256']==pins['sdas8051'],'build compiler/assembler hashes differ from mapped tools')
        q=load(B/'qualification.json')
        for name in ('sdcc','s51'):
            need(q['tools'][name]=={'path':str(producer/'bin'/name),'sha256':pins[name]},'qualification recorded tool path/hash differs: '+name)
        extra=load(B/'profile-tests/results.json')
        need(extra['identity']['compiler_sha256']==pins['sdcc'],'profile evidence compiler differs from mapped tool')
        # Exact profile command/cwd/argument checks occur in profile_tests below;
        # their toolchain paths refer to this declared read-only container mount.
        references=[]
        for row in extra['tests']:
            for argument in row['command']:
                if isinstance(argument,str) and '/toolchains/' in argument:
                    need(argument.startswith(str(producer)+'/'),'profile command references another toolchain')
                    references.append(argument)
        worker=Path('/tmp/ak820-beta2-streams-build-qualify.py')
        worker_text=worker.read_text()
        required="f'{original}/ak820-max/toolchains:{canonical}/toolchains:ro'"
        need(required in worker_text and "original=Path('/home/danil/ChatGPT/ak820-pass26b-restored-20261025')" in worker_text,'producer worker mount contract changed')
        return {'producer_toolchain':str(producer),'actual_toolchain':str(T),
                'docker_read_only_mount':str(T.parent)+':'+str(original/'toolchains')+':ro',
                'mapping_basis':'explicit Docker producer mount contract; no host group-path resolution',
                'producer_worker_sha256':sha(worker),'binary_sha256':actual,
                'profile_command_toolchain_arguments':sorted(set(references))}
    stage(out,'toolchain_path_mapping',toolchain_mapping)
    stage(out,'build',build)
    def full():
        q=load(B/'qualification.json'); ci._qualification(q,B/'qualification.json',B/'ajazz_ak820_vial.ihx',B/'ajazz_ak820_vial.map',T); auth.validate_qualification_contract(q)
        need(config.get('offline_tests_passed') is True,'configuration lacks full pass')
        for row in q['tests']:
            log=Path(row['log']); need(log.is_relative_to(B),'qualification log escapes build'); need(sha(log)==row['log_sha256'],'qualification log mismatch')
        return {'suites':len(q['tests']),'unit_tests':q['unit_tests'],'sha256':sha(B/'qualification.json')}
    stage(out,'qualification',full)
    def profile_tests():
        q=load(B/'profile-tests/results.json'); old=(cf.ROOT,cf.QMK,cf.test_source_snapshot,sys.executable)
        try:
            cf.ROOT=original; cf.QMK=original/'qmk-8051-ak820'; cf.test_source_snapshot=lambda:snapshot
            sys.executable=q['tests'][0]['command'][0]
            # Producer's toolchain mount path, checked against real pinned binaries separately.
            cf.validate_profile_tests(q,p,ident,B,original/'toolchains/sdcc-4.6.0')
        finally: cf.ROOT,cf.QMK,cf.test_source_snapshot,sys.executable=old
        for row in q['tests']: need(sha(B/'profile-tests'/(row['id']+'.log'))==row['log_sha256'],'profile log differs')
        return {'suites':len(q['tests']),'sha256':sha(B/'profile-tests/results.json')}
    stage(out,'profile_tests',profile_tests)
    def policy_sources():
        policy=load(directory/'release-policy.json')
        for n,rec in policy['source_files'].items(): safety.checked_record(R,n,rec); sha(R/n)
        old_blob=ci._git_blob
        try:
            if PRECOMMIT:
                # Defer commit admission only; preserve the real committed LUFA lock.
                lock=R/'qmk-8051-ak820/dependencies/lufa.json'
                ci._git_blob=lambda path: old_blob(path) if path==lock else path.read_bytes()
            ci._validate_policy_sources(policy,report)
        finally: ci._git_blob=old_blob
        need(policy['program']['ihx_sha256']==sha(B/'ajazz_ak820_vial.ihx') and policy['program']['symbols_sha256']==auth.symbols_sha256(B/'ajazz_ak820_vial.map'),'policy program mismatch')
        return {'sha256':sha(directory/'release-policy.json')}
    stage(out,'policy_sources',policy_sources)
    def committed_inputs():
        for path,label in [(directory/'release-policy.json','policy'),(directory/'packing-validation.json','packing receipt'),(directory/'program-review.md','program review'),(R/'tools/installer/settings-catalog.json','settings catalog')]:
            ci._require_committed_input(path,label)
        return {'passed':True}
    if PRECOMMIT: out.setdefault('deferred',[]).append('committed_inputs')
    else: stage(out,'committed_inputs',committed_inputs)
    def proof():
        summary=load(B/'runtime-safety/summary.json'); need(summary['passed'] is True and summary['identity']==ident,'runtime summary identity/pass differs'); current(summary['source_files']); need(summary['source_files']==cf.runtime_source_snapshot(),'incomplete runtime snapshot')
        need(summary['simulator_sha256']==sha(T/'bin/s51'),'runtime simulator hash differs')
        for row in summary['reports'].values(): need(sha(safety.safe_path(B,row['path']))==row['sha256'],'runtime report hash differs')
        for n,h in summary['logs'].items(): need(sha(B/'runtime-safety'/(n+'.log'))==h,'runtime log differs')
        manifest_name=safety.manifest_name(report['configuration']); manifest=load(R/manifest_name)
        required=set(safety.REQUIRED_SOURCES)|{str((A/'verify_transition.py').relative_to(R))}
        need(required <= manifest['source_files'].keys(),'missing legacy/current transition closure')
        with tempfile.TemporaryDirectory(prefix='ak820-evidence-') as tmp:
            root=Path(tmp); copy(root,manifest_name,R/manifest_name)
            for n in manifest['source_files']: copy(root,n,safety.safe_path(R,n))
            for row in manifest['witnesses'].values(): copy(root,row['path'],safety.safe_path(R,row['path']))
            transition=load(R/manifest['witnesses']['transition']['path'])
            for test in transition['tests']: copy(root,test['log_path'],safety.safe_path(R,test['log_path']))
            for n in (transition['actual_alpha2_preflight']['result_path'],transition['preflight_matrix']['path']): copy(root,n,safety.safe_path(R,n))
            for row in report['artifacts']:
                if Path(row['path']).suffix in ('.ihx','.map','.mem'): copy(root,'qmk-8051-ak820/'+row['path'],B/Path(row['path']).name)
            result=safety.validate(report,root)
            # require_release_qualification delegates to same checker with a default root.
            old=safety.validate
            try:
                safety.validate=lambda r:old(r,root); profiles.require_release_qualification(report)
            finally:safety.validate=old
        return result
    stage(out,'safety',proof)
    def transitions():
        pack=next(x for x in packing['profiles'] if x['profile']==p); cases=[c for c in matrix['cases'] if c['target_profile']==p]
        need(len(cases)==13 and len({c['source_case'] for c in cases})==13,'transition source cases incomplete/duplicate')
        need(all(c['passed'] is True and c['target']==ident['ihx_sha256'] and c['offline_only'] is True and c['physical_device_commands']==0 for c in cases),'transition scope/image/failure')
        alpha=next(c for c in cases if c['source_case']=='alpha2-saved-rom'); need([alpha[k] for k in ('key_count','encoder_count','combo_count')]==[498,12,8],'alpha2 counts differ')
        need(all(pack['build'].get(k)==ident[k] for k in ('profile','ihx_sha256','map_sha256','mem_sha256','configuration_sha256','compiler_sha256','nvm_schema')),'packing build identity differs')
        row=next(x for x in catalog['profiles'] if x['profile']==p)
        need(row['configuration']==report['configuration'] and row['reproducible_identity']==ci.reproducible_identity(B,ident),'catalog reproducible identity differs')
        need(row['settings_identity']['ihx_sha256']==ident['ihx_sha256'] and row['settings_identity']['code_sha256']==pack['settings_code_sha256'],'settings CODE identity differs')
        import pack_ak820 as packer
        private=Path('/home/danil/.codex/private/ak820-beta2-20261026')
        stockpath=private/'host/runs/20261023-as-is-flash/stock-full.bin'
        need(sha(stockpath)==packing['native_reference_sha256'],'packing reference differs')
        stock=stockpath.read_bytes(); packed=private/'beta2-packing-preflight'/p
        linked=packer.read_ihex(B/'ajazz_ak820_vial.ihx')
        for leaf,record in [('ak820-vial-permanent.bin',pack['permanent']),('ak820-vial-trial.bin',pack['trial'])]:
            path=packed/leaf; payload=path.read_bytes()
            need(sha(path)==record['sha256'] and len(payload)==record['size'],'actual packed payload differs')
            measured=packer.verify_payload(payload,target_build_id=report['build_id'])
            need(measured==record,'packed payload metadata differs')
            need(all(payload[address-packer.APP_START]==value for address,value in linked.items()),'packed CODE differs from linked image')
            if not record['trial']: need(packer.digest(payload[:packer.CODE_END-packer.APP_START])==pack['settings_code_sha256'],'measured settings CODE differs')
        recovery=packed/'restore-native.bin'
        need(sha(recovery)==pack['recovery_sha256'] and recovery.read_bytes()==stock[packer.APP_START:packer.APP_END],'recovery bytes differ')
        receipt=load(directory/'packing-validation.json'); rp=receipt['packing']
        need(pack['recovery_byte_equal'] is True and rp['recovery_byte_equal'] is True and rp['install_modes']==['permanent','trial'],'packing mode/recovery differs')
        need(rp['permanent']==pack['permanent'] and rp['images']['ak820-vial-trial.bin']==pack['trial'] and rp['images']['restore-native.bin']['sha256']==pack['recovery_sha256'] and rp['images']['restore-native.bin']['size']==pack['permanent']['size'],'packing images differ')
        return {'cases':13,'settings_code_sha256':pack['settings_code_sha256']}
    stage(out,'transitions_packing_catalog',transitions)
    def review():
        policy=load(directory/'release-policy.json'); receipt=(directory/'packing-validation.json').read_bytes(); raw=(directory/'program-review.md').read_bytes(); record=ci._review_record(raw)
        need(record['policy_sha256']==sha(directory/'release-policy.json'),'review policy byte hash differs'); auth.validate_policy(policy,host_manifest(R),receipt,raw)
        return {'sha256':sha(directory/'program-review.md')}
    if PRECOMMIT: out.setdefault('deferred',[]).append('independent_review_record')
    else: stage(out,'independent_review_record',review)
    out['all_other_evidence_passed']=not out.get('errors')
    out['passed']=out['all_other_evidence_passed'] and not out.get('deferred'); return out

def main():
    global PRECOMMIT
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',type=Path); parser.add_argument('--precommit',action='store_true',help='Defer committed-input admission and independent review; never yields overall passed'); args=parser.parse_args(); PRECOMMIT=args.precommit
    result={'format':'ak820-beta2-existing-evidence-validation-1','hardware_validated':False,'physical_device_commands':0,'independence_established_by_validator':False}
    snapshot=cf.test_source_snapshot()
    stage(result,'toolchain',lambda: str(cf.validate_tools(T)))
    def global_inputs():
        packing=load(A/'packing-preflight.json'); matrix=load(A/'transition-preflight.json'); catalog=load(R/'tools/installer/settings-catalog.json')
        need(packing['offline_only'] is True and packing['physical_device_commands']==0 and packing['hardware_validated'] is False,'packing scope differs')
        need(len(catalog.get('historical_sources',[]))==3,'catalog historical source count differs')
        need(all(set(x)=={'ihx_sha256','code_sha256'} for x in catalog['historical_sources']),'catalog historical source record shape differs')
        actual_history={(x.get('ihx_sha256'),x.get('code_sha256')) for x in catalog['historical_sources']}
        need(actual_history==set(HISTORICAL_SOURCES.values()),'catalog historical source identities differ')
        expected_edges=set()
        for source in ORDER:
            source_hash=catalog['profiles'][ORDER.index(source)]['identity']['ihx_sha256']
            for target in ORDER:
                target_hash=catalog['profiles'][ORDER.index(target)]['identity']['ihx_sha256']
                expected_edges.add((source,source_hash,target,target_hash))
        for source_case,(source_hash,_code_hash) in HISTORICAL_SOURCES.items():
            for target in ORDER:
                target_hash=catalog['profiles'][ORDER.index(target)]['identity']['ihx_sha256']
                expected_edges.add((source_case,source_hash,target,target_hash))
        actual_edges={(c.get('source_case'),c.get('source'),c.get('target_profile'),c.get('target')) for c in matrix['cases']}
        need(len(matrix['cases'])==130 and len(actual_edges)==130 and actual_edges==expected_edges,'full transition edge set incomplete, duplicated, or contains an unexpected edge')
        need(all(c['passed'] is True for c in matrix['cases']),'full transition matrix contains failed case')
        need(tuple(x['profile'] for x in catalog['profiles'])==ORDER,'catalog profile order differs')
        need(len(packing['profiles'])==10 and {x['profile'] for x in packing['profiles']}==set(ORDER),'packing profile set differs')
        return packing,matrix,catalog
    try: packing,matrix,catalog=global_inputs()
    except Exception as e:
        result['errors']=[{'gate':'global_inputs','error':str(e)}]; packing={'profiles':[]}; matrix={'cases':[]}; catalog={'profiles':[]}
    def settings():
        d=load(A/'settings-final-run.json'); need(d['exit_code']==0 and d['run']>0 and d['command']==['python','-B','-m','unittest','discover','-s','tools/installer','-p','test*settings*.py','-v'],'settings run differs'); current(d['source_files']); need(sha(safety.safe_path(R,d['log_path']))==d['log_sha256'],'settings log differs'); return {'sha256':sha(A/'settings-final-run.json'),'run':d['run']}
    stage(result,'settings',settings)
    result['profiles']=[check_profile(p,next(g for g,ps in GROUPS.items() if p in ps),snapshot,packing,matrix,catalog) for p in ORDER]
    def unchanged():
        need(cf.test_source_snapshot()==snapshot,'test sources changed during validation')
        for p,h in list(seen.items()): need(sha(p)==h,'input changed: '+str(p))
        return {'input_count':len(seen),'test_snapshot_sha256':hashlib.sha256(cf.canonical(snapshot)).hexdigest()}
    stage(result,'unchanged',unchanged)
    result['all_other_evidence_passed']=not result.get('errors') and all(x.get('all_other_evidence_passed',False) for x in result['profiles'])
    result['deferred']=['committed_inputs','independent_review_record'] if PRECOMMIT else []
    result['mode']='precommit' if PRECOMMIT else 'final'
    result['passed']=not result.get('errors') and all(x['passed'] for x in result['profiles']) and not PRECOMMIT
    result['input_hashes']={str(p):h for p,h in sorted(seen.items())}
    raw=json.dumps(result,separators=(',',':'),sort_keys=True)+'\n'
    if args.output:
        need(args.output.resolve().is_relative_to(Path('/tmp')),'output must be external /tmp evidence'); args.output.write_text(raw)
    print(raw,end=''); return 0 if result['passed'] else 1
if __name__=='__main__': sys.exit(main())
