#!/usr/bin/env python3
"""Offline linked C52 Combo/action/Vial ABI checks; never opens USB or builds."""
import argparse, hashlib, importlib.util, json, struct
from pathlib import Path
spec=importlib.util.spec_from_file_location('tapping',Path(__file__).parents[1]/'ak820_tapping/emitted.py')
tapping=importlib.util.module_from_spec(spec);spec.loader.exec_module(tapping)
linked=tapping.linked
BASE=0xc700+0x658

def vial_counts(fw):
    """Use the configured image identity; retain the legacy image contract."""
    path=fw.build/'configuration-report.json'
    if not path.exists():
        return [0,8,0]
    report=json.loads(path.read_text())
    if report.get('format')!='ak820-configured-build-1':
        raise ValueError('Unsupported configured build report')
    config=report['configuration'];identity=report['identity']
    canonical=(json.dumps(config,sort_keys=True,indent=2)+'\n').encode()
    if hashlib.sha256(canonical).hexdigest()!=identity['configuration_sha256']:
        raise ValueError('Configuration hash differs')
    for name,key in [('ajazz_ak820_vial.ihx','ihx_sha256'),('ajazz_ak820_vial.map','map_sha256'),('build-report.json','build_report_sha256')]:
        if hashlib.sha256((fw.build/name).read_bytes()).hexdigest()!=identity[key]:
            raise ValueError('Configured image identity differs: '+name)
    if config!=json.loads((fw.build/'build-report.json').read_text())['configuration']:
        raise ValueError('Configuration differs from compiled build report')
    options=config['make_options']
    names=('AK820_COMPACT_TAP_DANCE','AK820_COMPACT_KEY_OVERRIDE')
    schema=config['nvm_schema']
    if schema==0x082002:
        flags=[options.get(name,'no') for name in names]
        if flags!=['no','no']:raise ValueError('Legacy schema cannot enable optional Vial entries')
    elif schema==0x082003:
        if any(name not in options for name in names):raise ValueError('Missing optional Vial feature configuration')
        flags=[options[name] for name in names]
    else:raise ValueError('Unsupported configured NVM schema')
    if any(flag not in ('yes','no') for flag in flags):
        raise ValueError('Invalid optional Vial feature configuration')
    return [8 if flags[0]=='yes' else 0,8,8 if flags[1]=='yes' else 0]

def entry(a=4,b=5,out=6,marker=0x0820,version=1):return list(struct.pack('<5H',a,b,marker,version,out))
def setup(fw,name,out=6,nkro=False):
    t=tapping.Trace(fw,name)
    t.commands += [linked.memory('rom',BASE,entry(out=out))]+fw.call('_ak820_combo_reload')
    for p,c in [((0,0),4),((0,1),5),((0,2),7)]:t.map(p,c)
    if nkro:
        t.width=32;t.commands=[c.replace(f'{t.report_address+7:#x} 16;',f'{t.report_address+31:#x} 16;') for c in t.commands]
        t.commands+=fw.write('_keymap_config',[128,0])+fw.write('_keyboard_protocol',[1])
    return t

def report(nkro=False,mod=0,*keys):
    if not nkro:return tapping.packet(mod,*keys)
    data=[6,mod]+[0]*30
    for k in keys:data[2+k//8]|=1<<(k%8)
    return data

def finish(t,trace=None):
    r=t.run()
    if trace is not None:r['expected_hid_send_trace']=trace;r['pass_'] &= r['hid_send_trace']==trace
    return r

def dispatch(t,op,index=0,data=(),label='reply',expected=None):
    fw=t.fw;buf=[0xfe,0x0d,op,index]+list(data);buf += [0]*(32-len(buf))
    t.commands += fw.write('_raw_buffer',buf)+fw.write('_vial_handle_cmd_PARM_2',[32])+fw.call('_vial_handle_cmd',fw.address('_raw_buffer'))
    if expected is not None:t.check_memory(label,'_raw_buffer',0,expected)

def cases(fw):
    tests=[]
    options=json.loads((fw.build/'build-report.json').read_text())['configuration']['make_options']
    for nkro in ((False,True) if options.get('AK820_NKRO')=='yes' else (False,)):
        for order in ((0,1),(1,0)):
            for release in ((0,1),(1,0)):
                p=lambda mod=0,*k:report(nkro,mod,*k)
                t=setup(fw,f'chord-{int(nkro)}-{order[0]}-{release[0]}',nkro=nkro)
                t.event((0,order[0]),1,100);t.check('pending',[0]*32 if nkro else p());t.event((0,order[1]),1,139);t.check('active',p(0,6))
                if nkro and t.report_symbol!='_actual_keyboard_report':
                    t.check_memory('unprojected-owner-report-id','_actual_keyboard_report',0,[0])
                t.event((0,release[0]),0,140);t.check('first-release',p());t.event((0,release[1]),0,141);t.check('remaining-suppressed',p())
                tests.append(finish(t,[p(0,6),p()]))
    for start in (100,65520):
        t=setup(fw,f'timeout-wrap-{start}');t.event((0,0),1,start);t.tick((start+39)&65535);t.check('39-pending',report());t.tick((start+40)&65535);t.check('40-flushed',report(False,0,4));t.event((0,0),0,(start+41)&65535);t.check('released',report());tests.append(finish(t,[report(False,0,4),report()]))
    t=setup(fw,'second-at-40-does-not-match');t.event((0,0),1,100);t.event((0,1),1,140);t.check('first-flushed',report(False,0,4));t.tick(180);t.check('both-ordinary',report(False,0,4,5));t.event((0,0),0,181);t.event((0,1),0,182);t.check('released',report());tests.append(finish(t))
    for kind,code,pos in [('basic',7,(0,2)),('modifier',0xe1,(0,2)),('modtap',0x2107,(0,2)),('encoder',7,(253,0))]:
        t=setup(fw,'flush-before-'+kind);t.map(pos,code) if pos[0]<16 else t.commands.append(linked.memory('rom',0xcd40,[0,7]))
        t.event((0,0),1,100);t.event(pos,1,101)
        if kind=='modtap':t.tick(301);expected=[report(False,0,4),report(False,1,4)]
        else:expected=[report(False,0,4),report(False,2,4) if kind=='modifier' else report(False,0,4,7)]
        t.event(pos,0,302);t.event((0,0),0,303);t.check('released',report());r=finish(t);r['expected_hid_prefix']=expected;r['pass_'] &= r['hid_send_trace'][:len(expected)]==expected;tests.append(r)
    for output in (0xe1,0x0206):
        t=setup(fw,f'output-{output:04x}',out=output);t.event((0,0),1,100);t.event((0,1),1,101);t.check('active',report(False,2,*([6] if output==0x0206 else [])));t.event((0,0),0,102);t.event((0,1),0,103);t.check('released',report());tests.append(finish(t))
    t=setup(fw,'physical-output-owner');t.map((0,2),6);t.event((0,2),1,90);t.event((0,0),1,100);t.event((0,1),1,101);t.event((0,0),0,102);t.check('physical-survives',report(False,0,6));t.event((0,1),0,103);t.event((0,2),0,104);t.check('last-owner',report());tests.append(finish(t))
    t=setup(fw,'repeat-output-owner');t.map((0,2),0x7c79);t.event((0,0),1,100);t.event((0,1),1,101);t.event((0,2),1,102);t.event((0,0),0,103);t.check('repeat-survives',report(False,0,6));t.event((0,1),0,104);t.event((0,2),0,105);t.check('repeat-release',report());tests.append(finish(t))
    t=setup(fw,'caps-word-output');t.commands+=fw.call('_caps_word_on');t.event((0,0),1,100);t.event((0,1),1,101);t.check('shifted-output',report(False,2,6));t.event((0,0),0,102);t.event((0,1),0,103);t.check('caps-word-weak-shift',report(False,2));t.commands+=fw.call('_clear_keyboard');t.check('cleared',report());tests.append(finish(t))
    for active in (False,True):
        t=setup(fw,'clear-'+str(active));t.event((0,0),1,100)
        if active:t.event((0,1),1,101)
        t.commands+=fw.call('_clear_keyboard');t.tick(200);t.event((0,0),1,201);t.check('blocked-held',report());t.event((0,0),0,202)
        if active:t.event((0,1),0,203)
        t.event((0,0),1,210);t.event((0,1),1,211);t.check('fresh',report(False,0,6));t.event((0,0),0,212);t.event((0,1),0,213);t.check('fresh-release',report());tests.append(finish(t))
    t=setup(fw,'vial-count-get-marker-bounds');dispatch(t,0,expected=vial_counts(fw)+[0]*28+[1],label='counts');dispatch(t,3,expected=[0]+entry(marker=0,version=0),label='masked');dispatch(t,3,7,expected=[0]*11,label='last-empty');dispatch(t,3,8,expected=[255]+[0]*10,label='out-of-range');tests.append(finish(t))
    t=setup(fw,'vial-invalid-set-keeps-live-table');t.event((0,0),1,100)
    dispatch(t,4,data=entry(a=4,b=4,marker=0,version=0),expected=[255],label='invalid')
    dispatch(t,4,8,entry(marker=0,version=0),expected=[255],label='bounds')
    t.event((0,1),1,101);t.check('pending-preserved',report(False,0,6));t.event((0,0),0,102);t.event((0,1),0,103);tests.append(finish(t))
    # Seed only simulated ROM. An identical setter loads the cache without
    # changing bytes: the production flush stays clean and executes no IAP.
    t=tapping.Trace(fw,'vial-identical-set-reloads-without-iap')
    t.commands += [linked.memory('rom',BASE,entry())]
    t.map((0,0),4);t.map((0,1),5)
    dispatch(t,4,data=entry(marker=0,version=0),expected=[0],label='success')
    t.commands += fw.call('_ak820_nvm_diagnostic',fw.address('_raw_buffer'))
    t.check_memory('clean-cache','_raw_buffer',0,[0,1,0,0,0x658//64,0,0])
    t.event((0,0),1,100);t.event((0,1),1,101);t.check('reloaded-table',report(False,0,6));t.event((0,0),0,102);t.event((0,1),0,103);t.check('released',report());tests.append(finish(t))
    t=setup(fw,'unsupported-version-empty');t.commands+=[linked.memory('rom',BASE,entry(version=2))]+fw.call('_ak820_combo_reload');dispatch(t,3,expected=[0]*11,label='empty');t.event((0,0),1,100);t.check('ordinary',report(False,0,4));t.event((0,0),0,101);tests.append(finish(t))
    return tests

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build-dir','s51','output-dir'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();fw=linked.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    if any(0x2600<=address<0x2703 or address>=0xc700 for address in fw.code):raise ValueError('Image overlaps simulator fixture')
    tests=cases(fw)
    for t in tests:t['pass']=t.pop('pass_')
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    result=dict(level='linked SDCC 8051 C52 production action/report and Vial dispatch',image_sha256=digest(fw.image),runner_sha256=digest(__file__),tapping_support_sha256=digest(tapping.__file__),firmware_support_sha256=digest(linked.__file__),linked_map_sha256=digest(fw.build/'ajazz_ak820_vial.map'),simulator_sha256=digest(a.s51),initial_sp=fw.initial_sp,stack_capacity=fw.stack_capacity,tests=tests,limits='Simulated ROM NVM fixtures and USB-ready state. No physical USB, IAP writes, persistence, power-loss, IRQ overlap or physical timing proof. Identical-record valid setter exercises clean cache and reload without IAP; changed writes covered by separate host fixture.',passed=all(t['pass'] for t in tests))
    result['pass']=result.pop('passed');(fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['pass'],tests=len(tests),failed=[t['name'] for t in tests if not t['pass']],peak_sp=max(t['peak_sp'] for t in tests)),indent=2));return 0 if result['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
