#!/usr/bin/env python3
"""Exact linked work-profile IRQ check; CRT to main entry only, no NVM init."""
import argparse, hashlib, importlib.util, itertools, json, re
from pathlib import Path

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();repo=a.repo.resolve();root=repo/'qmk-8051-ak820';build=a.build.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    irq=load('work_irq_support',root/'tests/ak820_irq/run.py');stack=load('work_stack_support',root/'tests/ak820_stack/analyze.py');emitted=irq.emitted;iap=irq.iap
    fw=emitted.Firmware(build,repo/'toolchains/sdcc-4.6.0/bin/s51',out)
    manifest_path=build/'build-report.json';manifest=json.loads(manifest_path.read_text())
    instructions,symbols,code,identity=stack.load(build)
    source_checks=[];private_guards={}
    for prefix,rel,var in (('_dynamic_keymap_macro_send_sending_','quantum/dynamic_keymap.c','sending'),('_ak820_repeat_invoking','quantum/repeat_key.c','ak820_repeat_invoking'),('_ak820_td_invoking','keyboards/ajazz/ak820/ak820_tap_dance.c','ak820_td_invoking')):
        cells={name:address for name,address in symbols.items() if name.startswith(prefix)}
        if not cells:continue
        matches=[r for r in manifest['sources'] if r['path']==rel and r['origin']=='source']
        assert len(matches)==1 and sha(root/rel)==matches[0]['sha256'],('Compiled private guard source missing or differs',rel)
        assert stack.private_guard_source_contract((root/rel).read_text(),var),('Private guard source contract',rel)
        source_checks.append({'path':rel,'sha256':matches[0]['sha256'],'compiled_symbols':sorted(cells),'matches_build_manifest':True})
        private_guards.update({address:{'symbol':name,'source':rel,'source_sha256':matches[0]['sha256']} for name,address in cells.items()})
    immutable=[fw.image,build/'ajazz_ak820_vial.map',manifest_path]+[root/r['path'] for r in source_checks]
    before={str(p):sha(p) for p in immutable}
    wrappers,wrapper_source=irq.load_wrappers();helper=irq.HELPER_BYTES;mem=emitted.memory
    allowed={irq.HELPER_ADDRESS:helper,**{at:raw for at,raw in wrappers.values()}}
    for name,(ordinal,symbol) in irq.IRQ.items():allowed[0x3000+ordinal*3]=irq.packer.ljmp(fw.address(symbol))
    assert all(not set(range(at,at+len(raw))).intersection(code) for at,raw in allowed.items()),'Fixture overlaps occupied application CODE'
    assert not set(range(0x2600,0x2700)).intersection(code),'Trampoline overlaps occupied application CODE'
    fw.initialize=lambda:[f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}",mem('sfr',0xa8,[0]),mem('sfr',0xe8,[0])]
    sessions=[];Original=iap.Console
    class Console(Original):
        def command(self,commands):
            for row in ([commands] if isinstance(commands,str) else commands):
                m=re.match(r'set memory rom (0x[0-9a-f]+) (.*)$',row)
                if m:
                    at=int(m[1],16);raw=bytes(int(b,0) for b in m[2].split())
                    assert at+len(raw)<=0xc700 and not set(range(at,at+len(raw))).intersection(code)
                    assert (0x2600<=at and at+len(raw)<=0x2700) or allowed.get(at)==raw,('Unreviewed ROM patch',row)
                assert not row.startswith('fill rom'),'ROM fill forbidden'
            return super().command(commands)
        def close(self):
            try:
                # Full occupied image comparison, not merely the legal window end.
                addresses=sorted(code);groups=[]
                for at in addresses:
                    if not groups or at!=groups[-1][-1]+1:groups.append([])
                    groups[-1].append(at)
                for group in groups:
                    for pos in range(0,len(group),512):
                        sl=group[pos:pos+512];assert self.read('rom',sl[0],len(sl))==[code[at] for at in sl],('Application CODE changed',sl[0])
                sessions.append(len(code))
            finally:super().close()
    iap.Console=Console
    result={'pass':False,'scope':'Exact linked work-profile static stack and modeled IRQ CPU checks only','image_sha256':sha(fw.image),'map_sha256':sha(build/'ajazz_ak820_vial.map'),'build_report_sha256':sha(manifest_path),'runner_sha256':sha(Path(__file__)),'s51_sha256':sha(fw.simulator),'support_sha256':{str(p.relative_to(root)):sha(p) for p in [root/'tests/ak820_irq/run.py',root/'tests/ak820_stack/analyze.py',root/'tests/ak820_iap/run.py',root/'tests/ak820_emitted/run.py']},'guard_source_manifest_checks':source_checks,'initial_sp':fw.initial_sp,'stack_capacity':fw.stack_capacity,'occupied_CODE_bytes':len(code),'occupied_CODE_ge_c700':len([p for p in code if p>=0xc700]),'wrapper_source':wrapper_source,'limits':['Generic C52 CPU; no physical IRQ routing, timing, USB transport, LED DMA or device qualification.','Pinned OEM wrapper instructions and explicit USB ACK side effect supply the interrupt model.','CRT executes to main entry only; main and board/NVM/settings initialization do not run.','Only compiled private guard sources used by the fresh bound are required and authenticated.','IRQ-only component check; no full configured regression or storage check.']}
    try:
        analyzer=stack.Analyzer(instructions,code,identity['compact_callback_spills']);analyzer.configure_guards(private_guards)
        foreground=analyzer.bound(fw.address('_main'));assert foreground['bound'] is not None and not foreground['unresolved'],foreground['unresolved']
        (out/'foreground-stack.json').write_text(json.dumps({'image_sha256':sha(fw.image),'foreground':foreground,'private_guards':private_guards},indent=2)+'\n')
        console=Console(fw.simulator,fw.image)
        try:
            console.command(fw.initialize());entry_sp=console.read('sfr',0x81,1)[0]
        finally:console.close();(out/'crt-entry.log').write_text(console.log)
        frame=entry_sp-fw.initial_sp;assert frame==2,('Observed CRT frame',frame)
        calls=[pc for pc,raw in instructions.items() if (raw[0]==0x12 or raw[0]&0x1f==0x11) and irq.direct_target(pc,raw)==fw.address('_main')];assert len(calls)==1,calls
        callbacks={name:analyzer.bound(fw.address(symbol)) for name,(_,symbol) in irq.IRQ.items()}
        for name,report in callbacks.items():
            assert report['bound'] is not None and not report['unresolved'],(name,report['unresolved'])
            for pc in report['reachable']:irq.reject_priority_write(analyzer.instruction(pc),pc);assert analyzer.instruction(pc)[0]!=0x32
        bounds={name:17+r['bound'] for name,r in callbacks.items()};reserve=foreground['bound']+frame;total=reserve+sum(bounds.values());assert total<=fw.stack_capacity
        contracts=irq.emitted_contracts(fw,analyzer,callbacks)
        cases=[irq.cpu_case(fw,wrappers,order,reserve) for n in range(1,4) for order in itertools.permutations(irq.IRQ,n)]
        for case in cases:assert case['irq_stack_bytes']<=sum(bounds[name] for name in case['irq_order'])
        selector=irq.selector_cases(fw,analyzer)
        assert {str(p):sha(p) for p in immutable}==before,'Source/image inputs changed during checks'
        result.update(pass_=True,foreground_bound=foreground['bound'],foreground_unresolved=foreground['unresolved'],observed_main_entry_sp=entry_sp,crt_frame_bytes=frame,crt_main_call_pc=calls[0],crt_main_call_hex=instructions[calls[0]].hex(),foreground_reserved=reserve,callback_bounds={n:r['bound'] for n,r in callbacks.items()},irq_bounds=bounds,irq_total=sum(bounds.values()),total_stack_bound=total,remaining_stack_bytes=fw.stack_capacity-total,cpu_cases=cases,selector_cases=selector,emitted_contracts=contracts,inputs_unchanged=True)
        result['pass']=result.pop('pass_')
    except Exception as exc:result['failure']=repr(exc);raise
    finally:
        result['full_occupied_CODE_integrity_sessions']=sessions
        (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('cpu_cases','emitted_contracts','support_sha256','wrapper_source')},indent=2))

if __name__=='__main__':main()
