#!/usr/bin/env python3
"""Bounded exact-linked checks. Never seed flash, run main, or initialize NVM."""
import argparse, hashlib, importlib.util, itertools, json, re, sys
from pathlib import Path

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--build', type=Path, required=True); ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--sections', default='rgb,combo,update,irq')
    ap.add_argument('--source-root',type=Path,help='Exact source tree/checkpoint used by the build; defaults to repo/qmk-8051-ak820')
    a = ap.parse_args(); root=a.repo.resolve()/ 'qmk-8051-ak820'; out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    source_root=a.source_root.resolve() if a.source_root else root
    manifest_path=a.build.resolve()/'build-report.json'; manifest=json.loads(manifest_path.read_text())
    fixture_sources=['keyboards/ajazz/ak820/config.h','quantum/vialrgb.c','quantum/vial.c','keyboards/ajazz/ak820/ak820_nvm.c','keyboards/ajazz/ak820/ak820_nvm_update_block.c','quantum/dynamic_keymap.c','quantum/repeat_key.c','keyboards/ajazz/ak820/ak820_tap_dance.c']
    source_provenance=[]
    for rel in fixture_sources:
        matches=[r for r in manifest['sources'] if r['path']==rel and r['origin']=='source']
        assert len(matches)==1 and digest(source_root/rel)==matches[0]['sha256'],('Build source manifest mismatch',rel)
        source_provenance.append({'path':rel,'sha256':matches[0]['sha256'],'matches_build_manifest':True})
    iap=module('focused_iap',root/'tests/ak820_iap/run.py'); emitted=iap.emitted
    irq=module('focused_irq',root/'tests/ak820_irq/run.py')
    stack=module('focused_stack',root/'tests/ak820_stack/analyze.py')
    fw=emitted.Firmware(a.build.resolve(), a.repo.resolve()/'toolchains/sdcc-4.6.0/bin/s51',out)
    immutable_paths=[source_root/rel for rel in fixture_sources]+[fw.image,fw.build/'ajazz_ak820_vial.map',manifest_path]
    immutable_before={str(p):digest(p) for p in immutable_paths}
    mem=emitted.memory
    fw.initialize=lambda:[f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}",mem('sfr',0xa8,[0]),mem('sfr',0xe8,[0])]
    high=sorted(p for p in fw.code if p>=0xc700)
    groups=[]
    for p in high:
        if not groups or p!=groups[-1][-1]+1: groups.append([])
        groups[-1].append(p)
    checks=[]; original=iap.Console
    class SafeConsole(original):
        def command(self, commands):
            rows=[commands] if isinstance(commands,str) else commands
            for row in rows:
                m=re.match(r'(?:set memory|fill) rom (0x[\da-f]+)',row)
                if m:
                    p=int(m[1],16)
                    assert (0x2600<=p<0x2700 or p==irq.HELPER_ADDRESS or
                            any(p==v[0] for v in wrappers.values()) or 0x3000<=p<=0x3026),row
            return super().command(commands)
        def close(self):
            try:
                for g in groups:
                    for j in range(0,len(g),512):
                        sl=g[j:j+512]
                        assert self.read('rom',sl[0],len(sl))==[fw.code[p] for p in sl],('occupied CODE changed',sl[0])
                checks.append(len(high))
            finally: super().close()
    wrappers,wrapper_source=irq.load_wrappers()
    iap.Console=SafeConsole; irq.iap.Console=SafeConsole
    def write(c,name,data): c.command(fw.write(name,data))
    def read(c,name,n): return c.read(fw.symbol_space(name),fw.address(name),n)
    def cache(c,page,data,dirty=0,failed=0):
        for name,value in [('_page_valid',1),('_page_dirty',dirty),('_storage_failed',failed),('_cached_page',page),('_batch_depth',1)]:write(c,name,[value])
        write(c,'_page_data',data)
    def setup(c):
        c.command(fw.initialize()); c.command(mem('iram',0xfe,[0x79,0x96]))
        c.return_sp=c.read('sfr',0x81,1)
        assert c.return_sp==[fw.initial_sp+2],('CRT return frame',c.return_sp)
    def call(c,name,arg):
        log=c.command(fw.call(name,arg)); assert '0x2700' in log,log
        assert c.read('sfr',0x81,1)==c.return_sp,('SP',name)
        assert c.read('iram',0xfe,2)==[0x79,0x96],('stack canary',name)
    def batch(c,commands,observations):
        all_obs=[('SP','sfr',0x81,1),('stack_guard','iram',0xfe,2)]+observations
        for label,space,address,count in all_obs:commands+=fw.dump(label,space,address,count)
        # File console prevents piped command echo from splicing dump rows.
        command_file=out/'current-case.sim';command_file.write_text('\n'.join(commands)+'\n')
        log=c.command('exec '+json.dumps(str(command_file)));assert '0x2700' in log,log
        actual={}
        for label,space,address,count in all_obs:
            if space=='sfr':
                tail=log.rsplit('@@'+label,1)[1]
                actual[label]=[int(re.search(r'0x81 SP:\s+0b[01]+\s+0x([0-9a-f]+)',tail)[1],16)]
            else:actual[label]=fw.extract(log,label,address,count)
        assert actual['SP']==c.return_sp
        assert actual['stack_guard']==[0x79,0x96]
        return actual
    def session(name,fn):
        c=SafeConsole(fw.simulator,fw.image)
        try:setup(c); return fn(c)
        finally:
            c.close(); (out/(name+'.log')).write_text(c.log)
    results={'image_sha256':digest(fw.image),'map_sha256':digest(fw.build/'ajazz_ak820_vial.map'),
             'runner_sha256':digest(Path(__file__)),'s51_sha256':digest(fw.simulator),
             'support_sha256':{str(p.relative_to(root)):digest(p) for p in [root/'tests/ak820_iap/run.py',root/'tests/ak820_emitted/run.py',root/'tests/ak820_irq/run.py',root/'tests/ak820_stack/analyze.py']},
             'initial_sp':fw.initial_sp,'stack_capacity':fw.stack_capacity,
             'immutable_input_sha256':immutable_before,
             'source_provenance':{'source_root':str(source_root),'build_report_sha256':digest(manifest_path),'relevant_fixture_sources':source_provenance,'scope':'Selected fixture and private-guard sources authenticated against build manifest; not a separate whole-source build reproduction.'},
             'occupied_code_ge_c700_bytes':len(high),'sections':{},
             'limits':['Oversized diagnostic image; not a flashable release or device qualification.',
                       'CRT executes to main entry; main, board and NVM initialization are not executed.',
                       'No physical flash or NVM image is supplied; ROM at/above c700 is never written.',
                       'Only bounded component paths are checked; no full configured regression.']}
    try:
        results['startup_entry']=session('startup-entry',lambda c:{'observed_main_entry_sp':c.return_sp[0],'crt_entry_frame_bytes':c.return_sp[0]-fw.initial_sp})
        if 'rgb' in a.sections.split(','):
            config=source_root/'keyboards/ajazz/ak820/config.h'
            brightness=int(re.search(r'^#define RGB_MATRIX_MAXIMUM_BRIGHTNESS (\d+)',config.read_text(),re.M)[1])
            before=digest(config); hsv=fw.address('_g_direct_mode_colors')
            seed=[(i*37+19)&255 for i in range(82*3)]
            cases=[(length,0,9,177) for length in range(256)]
            cases += [(32,first,n,159) for first in (0,1,72,80,81,82,255,256,65535) for n in (*range(12),255)]
            cases += [(32,((0,9),(72,9),(80,9),(81,1))[v%4][0],((0,9),(72,9),(80,9),(81,1))[v%4][1],v) for v in range(256)]
            def rgb(c):
                for num,(length,first,n,v) in enumerate(cases):
                    if num%64==0:(out/'progress.json').write_text(json.dumps({'section':'rgb','completed':num,'total':len(cases)}))
                    packet=[0xa1,0x42,first&255,first>>8,n]+[(v+j*29)&255 for j in range(27)]
                    packet[7]=v
                    commands=[mem('xram',0x7fff,[0xb9]+packet+[0x6d]),mem('xram',hsv-1,[0x93]+seed+[0x5c])]
                    commands+=fw.write('_vialrgb_set_value_PARM_2',[length])+fw.call('_vialrgb_set_value',0x8000)
                    actual=batch(c,commands,[('colors','xram',hsv-1,248),('packet','xram',0x7fff,34)])
                    expected=seed.copy()
                    if length==32 and first<82 and n<=9:
                        for j in range(min(n,82-first)):
                            expected[(first+j)*3:(first+j+1)*3]=packet[5+j*3:7+j*3]+[min(packet[7+j*3],brightness)]
                    assert actual['colors']==[0x93]+expected+[0x5c],('rgb',num,length,first,n,v)
                    assert actual['packet']==[0xb9]+packet+[0x6d],('packet modified',num)
                return {'pass':True,'cases':len(cases),'all_packet_lengths':256,'value_sweep':256,'brightness':brightness,'config_sha256':before,'all_hsv_and_packet_guards_checked':True}
            results['sections']['rgb']=session('rgb',rgb); assert digest(config)==before
        if 'combo' in a.sections.split(','):
            def combo(c):
                count=0; whole=0; crosses=0
                for unlocked in (0,1):
                    write(c,'_vial_unlocked',[unlocked])
                    for kind in ('valid','marker','version','duplicate','empty'):
                        for index in (range(256) if kind=='valid' else range(8)):
                            if count%64==0:(out/'progress.json').write_text(json.dumps({'section':'combo','completed':count,'total':576}))
                            offset=0x658+index*10; page=offset//64; start=offset%64
                            data=[0]*64
                            row=[4,0,5,0,0x20,8,1,0,6,0]
                            if kind=='marker':row[4]=0
                            if kind=='version':row[6]=2
                            if kind=='duplicate':row[2]=4
                            if kind=='empty':row=[0,0,0,0,0x20,8,1,0,0,0]
                            fits=start+10<=64
                            if fits:data[start:start+10]=row
                            else:
                                # A split record cannot be fully supplied by one cache page.
                                # Prime the page holding marker and invalidate both marker bytes.
                                marker=offset+4; page=marker//64; data[(marker%64)]=0
                            commands=[]
                            for name,value in [('_page_valid',1),('_page_dirty',0),('_storage_failed',0),('_cached_page',page&255),('_batch_depth',1)]:commands+=fw.write(name,[value])
                            commands+=fw.write('_page_data',data)
                            packet=[0xfe,0x0d,3,index]+[(i*11+3)&255 for i in range(28)]
                            commands+=[mem('xram',0x7fff,[0xb9]+packet+[0x6d])]+fw.write('_vial_handle_cmd_PARM_2',[32])+fw.call('_vial_handle_cmd',0x8000)
                            obs=[('packet','xram',0x7fff,34),('cache','xram',fw.address('_page_data'),64)]
                            obs += [(name,fw.symbol_space(name),fw.address(name),1) for name in ('_cached_page','_page_valid','_page_dirty','_storage_failed')]
                            actual=batch(c,commands,obs)
                            expected=packet.copy(); expected[0]=0 if index<8 else 255;expected[1:11]=[0]*10
                            if index<8 and fits and kind=='valid':expected[1:11]=[4,0,5,0,0,0,0,0,6,0]
                            assert actual['packet']==[0xb9]+expected+[0x6d],('combo',unlocked,kind,index)
                            assert actual['cache']==data
                            assert actual['_cached_page']==[page&255]
                            assert actual['_page_valid']==[1] and actual['_page_dirty']==[0] and actual['_storage_failed']==[0]
                            count+=1;whole+=int(index<8 and fits);crosses+=int(index<8 and not fits)
                return {'pass':True,'cases':count,'all_indices':256,'lock_states':2,'row_forms':5,'wholly_cached_valid_index_cases':whole,'split_record_corrupt_marker_cases':crosses,'limitation':'Split records are forced invalid at a cached marker byte; valid cross-page records and physical flash reads are not qualified.'}
            results['sections']['combo']=session('combo',combo)
        if 'update' in a.sections.split(','):
            def update(c):
                forbidden=[]
                for name in ('_ak820_flash_erase','_ak820_flash_program','_ak820_flash_program_page','_write_page'):
                    if name in fw.symbols:c.command(f'break {fw.address(name):#x}')
                    if name in fw.symbols:forbidden.append({'symbol':name,'address':fw.address(name)})
                total=0; rn_observations=[]
                entry=fw.address('_ak820_eeprom_update_block_xdata')
                stack_kernel=bytes(fw.code.get(entry+i,0) for i in range(4))==bytes.fromhex('c082c083')
                for failed,dirty in itertools.product((0,1),repeat=2):
                    paths=[(64,0,'zero'),(64,16,'equal'),(64,16,'first'),(64,16,'last'),(127,1,'equal'),(127,1,'first'),(120,8,'last'),(128,0,'zero'),(0x2800,4,'outside-equal'),(0xffff,1,'outside-equal'),(127,2,'cross-equal'),(0xffff,2,'wrap-equal')]
                    for offset,length,kind in paths:
                        data=[(i*13+7)&255 for i in range(64)]
                        page=0 if kind=='wrap-equal' else 1
                        source=[]
                        for j in range(length):
                            at=(offset+j)&65535
                            source.append(0 if at>=0x2800 else data[at%64] if at//64==page else fw.code.get(0xc700+at,255))
                        if kind=='first':source[0]^=0x5a
                        if kind=='last':source[-1]^=0x5a
                        cache(c,page,data,dirty,failed)
                        src=source+[0x55]*(32-len(source));c.command(mem('xram',0x7fff,[0xa4]+src+[0x4a]))
                        tag=(0,0x80,0xff)[total%3];args=[offset&255,offset>>8,tag]
                        write(c,'_ak820_eeprom_update_block_xdata_PARM_2',args);write(c,'_ak820_eeprom_update_block_xdata_PARM_3',list(length.to_bytes(2,'little')))
                        write(c,'_ak820_eeprom_write_block_xdata_PARM_2',[0x91]*3);write(c,'_ak820_eeprom_write_block_xdata_PARM_3',[0x92]*2)
                        c.command(mem('iram',0,[0x3c,0xc3]));call(c,'_ak820_eeprom_update_block_xdata',0x8000)
                        rn=c.read('iram',0,2);rn_observations.append({'failed':failed,'dirty':dirty,'kind':kind,'offset':offset,'R0_R1':rn})
                        if stack_kernel and kind not in ('first','last'):assert rn==[0x3c,0xc3],('R0/R1',failed,dirty,kind)
                        assert c.read('xram',0x7fff,34)==[0xa4]+src+[0x4a]
                        mismatch=kind in ('first','last')
                        expected=data.copy()
                        if mismatch and not failed:
                            for j,value in enumerate(source):expected[(offset+j)%64]=value
                        assert read(c,'_page_data',64)==expected,(failed,dirty,kind,'cache')
                        assert read(c,'_page_dirty',1)==[int(bool(dirty or (mismatch and not failed)))]
                        assert read(c,'_storage_failed',1)==[failed]
                        assert read(c,'_cached_page',1)==[page] and read(c,'_page_valid',1)==[1] and read(c,'_batch_depth',1)==[1]
                        assert read(c,'_ak820_eeprom_write_block_xdata_PARM_2',3)==(args if mismatch else [0x91]*3)
                        assert read(c,'_ak820_eeprom_write_block_xdata_PARM_3',2)==(list(length.to_bytes(2,'little')) if mismatch else [0x92]*2)
                        total+=1
                return {'pass':True,'cases':total,'stack_kernel':stack_kernel,'physical_writer_invocation':'breakpoint forbidden','forbidden_flash_breakpoints':forbidden,'source_guards_SP_checked':True,'R0_R1_observations':rn_observations,'limits':['R0/R1 preservation asserted for empty/equal stack kernels; baseline C and unchanged C tailwriter may clobber caller-scratch R0/R1.','No dirty cross-page transition that requires flash; equal crossing reads immutable linked CODE as the physical-read fixture.','ffff wrap checked with primed cache0.']}
            results['sections']['update']=session('update',update)
        if 'irq' in a.sections.split(','):
            instructions,symbols,code,provenance=stack.load(fw.build);analyzer=stack.Analyzer(instructions,code,provenance['compact_callback_spills'])
            private_guards={}
            for prefix,rel,variable in (('_dynamic_keymap_macro_send_sending_','quantum/dynamic_keymap.c','sending'),('_ak820_repeat_invoking','quantum/repeat_key.c','ak820_repeat_invoking'),('_ak820_td_invoking','keyboards/ajazz/ak820/ak820_tap_dance.c','ak820_td_invoking')):
                assert stack.private_guard_source_contract((source_root/rel).read_text(),variable),('private guard contract',rel)
                for name,address in symbols.items():
                    if name.startswith(prefix):private_guards[address]={'symbol':name,'source':rel,'source_sha256':digest(source_root/rel)}
            analyzer.configure_guards(private_guards)
            foreground=analyzer.bound(fw.address('_main'))
            assert foreground['bound'] is not None and not foreground['unresolved'],('Unresolved foreground',foreground['unresolved'])
            (out/'foreground-stack.json').write_text(json.dumps({'image_sha256':digest(fw.image),'analyzer_sha256':digest(root/'tests/ak820_stack/analyze.py'),'foreground':foreground,'private_guards':private_guards},indent=2)+'\n')
            main_calls=[pc for pc,raw in instructions.items() if (raw[0]==0x12 or raw[0]&0x1f==0x11) and irq.direct_target(pc,raw)==fw.address('_main')]
            assert len(main_calls)==1,('Expected one CRT call to main',main_calls)
            crt_frame=results['startup_entry']['crt_entry_frame_bytes'];assert crt_frame==2
            callbacks={name:analyzer.bound(fw.address(symbol)) for name,(_,symbol) in irq.IRQ.items()}
            for name,report in callbacks.items():
                assert report['bound'] is not None,(name,report['unresolved'])
                for pc in report['reachable']:
                    irq.reject_priority_write(analyzer.instruction(pc),pc);assert analyzer.instruction(pc)[0]!=0x32
            bounds={name:17+report['bound'] for name,report in callbacks.items()};reserve=foreground['bound']+crt_frame
            assert reserve+sum(bounds.values())<=fw.stack_capacity,(reserve,bounds,fw.stack_capacity)
            contracts=irq.emitted_contracts(fw,analyzer,callbacks)
            cases=[irq.cpu_case(fw,wrappers,order,reserve) for n in range(1,4) for order in itertools.permutations(irq.IRQ,n)]
            for case in cases:assert case['irq_stack_bytes']<=sum(bounds[name] for name in case['irq_order'])
            selectors=irq.selector_cases(fw,analyzer)
            results['sections']['irq']={'pass':True,'foreground_bound':foreground['bound'],'foreground_unresolved':foreground['unresolved'],'crt_frame_bytes':crt_frame,'crt_main_call_pc':main_calls[0],'crt_main_call_hex':instructions[main_calls[0]].hex(),'callback_bounds':{n:r['bound'] for n,r in callbacks.items()},'wrapper_stack_bytes':17,'irq_bounds':bounds,'ordered_nests':cases,'selector':selectors,'contracts':contracts,'wrapper_source':wrapper_source,'main_reserved':reserve,'total_reserved':reserve+sum(bounds.values()),'limits':['Foreground bound freshly derived from the same linked image and authenticated private guard sources.','CRT entry frame confirmed by actual startup and unique linked call to main.','Hardware nesting, peripheral ACK and interrupt timing remain model assumptions.']}
        assert {str(p):digest(p) for p in immutable_paths}==immutable_before,'Source or linked input modified during checks'
        results['immutable_inputs_unchanged']=True
        results['pass']=True
    except Exception as exc:
        results['pass']=False; results['failure']=repr(exc);raise
    finally:
        results['code_integrity_sessions']=len(checks);results['occupied_code_ge_c700_unchanged_per_session']=checks
        (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({k:v for k,v in results.items() if k not in ('support_sha256','sections')},indent=2))

if __name__=='__main__': main()
