#!/usr/bin/env python3
"""Exercise an existing linked 8051 image. Never opens USB or builds firmware."""
import argparse, hashlib, importlib.util, json, re
from pathlib import Path
spec=importlib.util.spec_from_file_location('linked',Path(__file__).parents[1]/'ak820_emitted/run.py')
linked=importlib.util.module_from_spec(spec);spec.loader.exec_module(linked)
pack_spec=importlib.util.spec_from_file_location('packer',Path(__file__).parents[2]/'util/pack_ak820.py')
packer=importlib.util.module_from_spec(pack_spec);pack_spec.loader.exec_module(packer)

class Trace:
    def __init__(self,fw,name):
        self.fw,self.name=fw,name;self.commands=fw.initialize();self.expected=[];self.event_index=0;self.width=8;self.extra_address=None;self.macro_fixtures=[]
        # Observe every production keyboard send, including the immediate tap
        # pulse which has already disappeared when action_exec returns.
        addr=fw.address('_actual_keyboard_report')
        self.commands += ['timer add event','timer add macro',f'break {fw.address("_host_keyboard_send"):#x}',f'commands 1 "echo @@HID; dump xram {addr:#x} {addr+7:#x} 16; fill xram 0x2201 0x2203 0x12; run"']
        self.commands += [linked.memory('rom',0xc740,[0]*256)]
        for layer in range(1,6):self.commands += [linked.memory('rom',0xc740+layer*256,[0,1]*128)]
    def capture_extra(self):
        self.extra_address=self.fw.address(next(n for n in self.fw.symbols if n.startswith('_host_extra_send_report_100')))
        self.commands += [f'break {self.fw.address("_send_extra"):#x}',f'commands 2 "echo @@EXTRA; dump xram {self.extra_address:#x} {self.extra_address+2:#x} 16; fill xram 0x2201 0x2203 0x12; run"']
    def macro(self,body):
        stream=bytes(body)+bytes(packer.MACRO_COUNT)
        length=packer.macro_stream_length(stream)
        if length>packer.MACRO_SIZE:raise ValueError('Macro fixture exceeds published storage')
        self.macro_fixtures.append({'logical_length':length,'stream_sha256':hashlib.sha256(stream).hexdigest(),'grammar_validated':True,'busy':0,'metadata_address':packer.NVM_START+packer.MACRO_BUSY_ADDR,'stream_address':packer.NVM_START+packer.MACRO_ADDR})
        self.commands += [linked.memory('rom',packer.NVM_START+packer.MACRO_BUSY_ADDR,[0,length&255,length>>8])]
        self.commands += [linked.memory('rom',packer.NVM_START+packer.MACRO_ADDR+i,stream[i:i+32]) for i in range(0,length,32)]
        self.commands += self.fw.call('_ak820_macro_init')+['timer set macro 0','timer start macro']+self.fw.call('_dynamic_keymap_macro_send',0)+['timer stop macro','timer get macro']
    def check_memory(self,label,symbol,offset,expected):
        # Reuse observation parsing with a stable synthetic symbol alias.
        alias=f'_fixture_{label}';self.fw.symbols[alias]=self.fw.address(symbol)+offset
        self.commands+=self.fw.dump_symbol(label,alias,len(expected));self.expected.append((label,alias,expected))
    def map(self,pos,code,layer=0):
        row,col=pos;self.commands += [linked.memory('rom',0xc740+layer*256+(row*8+col)*2,[code>>8,code&255])]
    def event(self,pos,down,time):
        row,col=pos;kind=2 if row==253 else 3 if row==252 else 1
        self.commands += ['fill xram 0x2201 0x2203 0x12']+self.fw.write('_action_exec_PARM_1',[col,row,time&255,time>>8,kind,int(down)])+['timer set event 0','timer start event']+self.fw.call('_action_exec')+['timer stop event',f'echo @@EVENT-{self.event_index}','timer get event'];self.event_index+=1
    def tick(self,time):
        self.commands += ['fill xram 0x2201 0x2203 0x12']+self.fw.write('_action_exec_PARM_1',[0,0,time&255,time>>8,0,0])+['timer set event 0','timer start event']+self.fw.call('_action_exec')+['timer stop event',f'echo @@EVENT-{self.event_index}','timer get event'];self.event_index+=1
    def check(self,label,report=None,layer=None):
        for suffix,symbol,value in [('report','_actual_keyboard_report',report),('layer','_layer_state',None if layer is None else [layer])]:
            if value is not None:
                tag=label+'_'+suffix;self.commands+=self.fw.dump_symbol(tag,symbol,len(value));self.expected.append((tag,symbol,value))
    def run(self):
        log,stack=self.fw.execute(self.name,self.commands)
        checks=[{'label':tag,'actual':self.fw.extract(log,tag,self.fw.address(sym),len(value)),'expected':value} for tag,sym,value in self.expected]
        hid=[]
        for section in log.split('@@HID\n')[1:]:
            try:hid.append(self.fw.extract('@@packet\n'+section,'packet',self.fw.address('_actual_keyboard_report'),self.width))
            except ValueError:pass
        extra=[]
        if self.extra_address is not None:
            for section in log.split('@@EXTRA\n')[1:]:
                extra.append(self.fw.extract('@@packet\n'+section,'packet',self.extra_address,3))
        # Total ticks are the emulator's instruction clocks, not wall latency.
        macro_clocks=[int(n) for n in re.findall(r'timer #\d+\("macro"\).*?\((\d+) clks\)',log)]
        event_clocks=[int(n) for n in re.findall(r'timer #\d+\("event"\).*?\((\d+) clks\)',log)]
        clocks=re.findall(r'Total time since last reset=.*?\((\d+) clks\)',log)
        return dict(name=self.name,pass_=all(c['actual']==c['expected'] for c in checks),checks=checks,hid_send_trace=hid,extra_callback_trace=extra,macro_fixtures=self.macro_fixtures,macro_clock_samples=macro_clocks,event_clock_samples=event_clocks,max_event_clocks=max(event_clocks,default=0),simulated_clocks=int(clocks[-1]) if clocks else None,**stack)

def vial(fw,command):
    return [linked.memory('xram',fw.address('_raw_buffer'),[0xfe,command]+[0]*30)]+fw.write('_vial_handle_cmd_PARM_2',[32])+fw.call('_vial_handle_cmd',fw.address('_raw_buffer'))
def packet(mod=0,*keys):return [mod,0,*keys,*([0]*(6-len(keys)))]
def cases(fw):
    out=[]
    for duration,start in [(199,100),(200,100),(199,65500),(200,65500)]:
        t=Trace(fw,f'boundary-{duration}-{start}');t.map((0,0),0x2104);t.event((0,0),1,start);t.tick((start+duration)&65535)
        t.check('decision',packet(1 if duration>=200 else 0));t.event((0,0),0,(start+duration)&65535);t.check('released',packet());r=t.run()
        r['expected_hid_send_trace']=[packet(0,4),packet()] if duration<200 else [packet(1),packet()];r['pass_'] &= r['hid_send_trace']==r['expected_hid_send_trace'];out.append(r)
    for mask in range(32):
        t=Trace(fw,f'mt-mask-{mask}');t.map((0,0),0x2004|(mask<<8));t.event((0,0),1,100);t.tick(300);t.check('hold',packet((mask<<4)&255 if mask&16 else mask));t.event((0,0),0,301);t.check('release',packet());out.append(t.run())
    for layer in range(6):
        t=Trace(fw,f'lt-target-{layer}');t.map((0,0),0x4004|(layer<<8));t.event((0,0),1,100);t.tick(300);t.check('hold',layer=1<<layer);t.event((0,0),0,301);t.check('release',layer=0);out.append(t.run())
    t=Trace(fw,'nested-modtaps');t.map((0,0),0x2104);t.map((0,1),0x2205);t.event((0,0),1,100);t.event((0,1),1,101);t.check('first-committed',packet(1));t.tick(301);t.check('both-held',packet(3));t.event((0,0),0,302);t.check('second-survives',packet(2));t.event((0,1),0,303);t.check('empty',packet());out.append(t.run())
    t=Trace(fw,'nested-frozen-remap');t.map((0,0),0x4104);t.map((0,1),5);t.map((0,1),6,1);t.map((0,0),1,1);t.event((0,0),1,100);t.event((0,1),1,110);t.check('lookup-after-hold',packet(0,6),2);t.map((0,0),0x4204);t.event((0,0),0,120);t.check('frozen-lt-release',packet(0,6),0);t.map((0,1),7);t.event((0,1),0,130);t.check('frozen-basic-release',packet());out.append(t.run())
    t=Trace(fw,'duplicate-rollover-promotion')
    for i in range(8):t.map((i//4,i%4),4+max(0,i-1))
    for i in range(8):t.event((i//4,i%4),1,100+i)
    t.check('seven-distinct',packet(0,*([1]*6)));t.event((0,0),0,120);t.check('duplicate-survives',packet(0,*([1]*6)));t.event((0,1),0,121);t.check('promotion',packet(0,5,6,7,8,9,10))
    for i in range(2,8):t.event((i//4,i%4),0,130+i)
    t.check('empty',packet());out.append(t.run())
    t=Trace(fw,'physical-mt-lm-weak-repeat-overlap')
    for pos,code in [((0,0),0xe1),((0,1),0x2204),((0,2),0x5022),((0,3),0x0205),((1,0),4),((1,1),0x7c79)]:t.map(pos,code)
    # LM layer1 must preserve all fixture positions through transparency.
    for i in range(8):t.map((i//4,i%4),1,1)
    t.event((0,0),1,100);t.event((0,1),1,101);t.tick(301);t.event((0,2),1,302);t.event((0,3),1,303);t.check('owners',packet(2,5),2);t.event((1,1),1,303)
    t.event((0,0),0,304);t.event((0,1),0,305);t.check('lm-weak-survive',packet(2,5),2);t.event((0,2),0,306);t.check('weak-survives',packet(2,5),0);t.event((0,3),0,307);t.check('repeat-weak-owner-survives',packet(2,5));t.event((1,1),0,308);t.check('repeat-weak-owner-released',packet())
    t.event((1,0),1,310);t.event((1,1),1,311);t.event((1,0),0,312);t.check('repeat-retains-basic',packet(0,4));t.event((1,1),0,313);t.check('repeat-release',packet());out.append(t.run())
    for row in (253,252):
        t=Trace(fw,f'encoder-{row}');addr=0xcd40+(0 if row==253 else 2);t.commands+=[linked.memory('rom',addr,[0,4])];t.event((row,0),1,100);t.check('down',packet(0,4));t.event((row,0),0,101);t.check('up',packet());out.append(t.run())
    for unlock in (False,True):
        t=Trace(fw,'cancel-'+str(unlock));t.map((0,0),4);t.map((0,1),0x7c79);t.event((0,0),1,100);t.event((0,1),1,101);t.commands+=vial(fw,6) if unlock else fw.call('_clear_keyboard')
        t.event((0,0),1,102);t.event((0,1),1,103);t.check('blocked',packet())
        if unlock:t.commands+=vial(fw,8)
        t.event((0,0),0,104);t.event((0,1),0,105);t.event((0,0),1,106);t.check('fresh',packet(0,4));t.event((0,0),0,107);t.check('released',packet());t.event((0,1),1,108);t.check('fresh-repeat',packet(0,4));t.event((0,1),0,109);t.check('fresh-repeat-release',packet());out.append(t.run())
    t=Trace(fw,'to-tg-held-layer-overlap');t.map((0,0),0x4104);t.map((0,1),0x5202);t.map((0,2),0x5262);t.event((0,0),1,100);t.tick(300);t.check('held-lower',layer=2);t.event((0,1),1,301);t.check('to-with-held-lower',layer=14);t.event((0,1),0,302);t.event((0,0),0,303);t.check('persistent-upper-survives',layer=4);t.event((0,2),1,304);t.event((0,2),0,305);t.check('toggle-off',layer=0);out.append(t.run())
    t=Trace(fw,'default-tri-explicit-overlap');t.map((0,0),0x5222);t.map((0,1),0x5263);t.map((0,2),0x5204)
    t.map((0,3),0x5241);t.event((0,3),1,90);t.event((0,3),0,91);t.check('default-not-copied',layer=0)
    t.event((0,0),1,100);t.check('default-lower-held-upper',layer=12)
    t.map((0,3),0x5240);t.event((0,3),1,110);t.event((0,3),0,111);t.check('default-away',layer=4)
    t.map((0,3),0x5241);t.event((0,3),1,112);t.event((0,3),0,113);t.event((0,1),1,114);t.event((0,1),0,115);t.event((0,0),0,116);t.check('explicit-adjust-survives',layer=8)
    t.event((0,2),1,117);t.check('to-replaces-persistent',layer=16);out.append(t.run())
    t=Trace(fw,'nkro-seven-owners');t.width=32;t.commands=[c.replace(f'{fw.address("_actual_keyboard_report")+7:#x} 16;',f'{fw.address("_actual_keyboard_report")+31:#x} 16;') for c in t.commands];t.commands+=fw.write('_keymap_config',[128,0])+fw.write('_keyboard_protocol',[1])
    for i in range(8):t.map((i//4,i%4),4+max(0,i-1));t.event((i//4,i%4),1,100+i)
    # Shared NKRO report: id6, modifier byte, then usages4..10 bitmap.
    t.check('bitmap', [6,0,240,7]+[0]*28);t.event((0,0),0,120);t.check('duplicate', [6,0,240,7]+[0]*28);t.event((0,1),0,121);t.check('last-owner', [6,0,224,7]+[0]*28);out.append(t.run())
    for code,usage,kind in [(0xa5,0x81,'system'),(0xa8,0xe2,'consumer')]:
        t=Trace(fw,'extra-duplicate-'+kind);t.extra_address=fw.address(next(n for n in fw.symbols if n.startswith('_host_extra_send_report_100')));t.commands += [f'break {fw.address("_send_extra"):#x}',f'commands 2 "echo @@EXTRA; dump xram {t.extra_address:#x} {t.extra_address+2:#x} 16; fill xram 0x2201 0x2203 0x12; run"'];t.map((0,0),code);t.map((0,1),code);t.map((0,2),code+1)
        def extra(label,value):
            symbol='_last_'+kind+'_usage';expected=list(value.to_bytes(2,'little'));t.commands+=fw.dump_symbol(label,symbol,2);t.expected.append((label,symbol,expected))
        t.event((0,0),1,100);t.event((0,1),1,101);extra('duplicate-down',usage);t.event((0,0),0,102);extra('one-owner-remains',usage);t.event((0,1),0,103);extra('last-owner-released',0);t.event((0,0),1,110);t.event((0,2),1,111);next_usage=0x82 if kind=='system' else 0xe9;extra('newest-owner',next_usage);t.event((0,2),0,112);extra('previous-owner-promoted',usage);t.event((0,0),0,113);extra('final-empty',0);r=t.run();report_id=3 if kind=='system' else 4;r['expected_extra_callback_trace']=[[report_id,usage,0],[report_id,0,0],[report_id,usage,0],[report_id,next_usage,0],[report_id,usage,0],[report_id,0,0]];r['pass_'] &= r['extra_callback_trace']==r['expected_extra_callback_trace'];out.append(r)
    t=Trace(fw,'tri-config-frozen-release');t.map((0,0),0x7c77);t.event((0,0),1,100);t.check('lower-held',layer=2);t.commands+=fw.write('_tri_layer_lower_layer',[4]);t.check('configuration-does-not-move-owner',layer=2);t.event((0,0),0,101);t.check('frozen-release',layer=0);out.append(t.run())
    t=Trace(fw,'all-sources-cancel-admission')
    sources=[(row,col) for row in range(16) for col in range(8)]+[(253,0),(252,0)]
    for pos in sources[:128]:t.map(pos,4)
    t.commands += [linked.memory('rom',0xcd40,[0,4,0,4])]
    for i,pos in enumerate(sources):t.event(pos,1,100+i)
    t.check('all-held',packet(0,4));t.commands+=fw.call('_clear_keyboard')
    for i,pos in enumerate(sources):t.event(pos,1,300+i)
    t.check('all-blocked',packet())
    for i,pos in enumerate(sources):t.event(pos,0,500+i)
    t.event((0,0),1,700);t.check('fresh-after-release',packet(0,4));t.event((0,0),0,701);t.check('empty',packet());out.append(t.run())
    t=Trace(fw,'protocol-full-matrix-scan')
    for row in range(16):
        for col in range(8):t.map((row,col),4)
    t.commands += ['timer add scan','timer set scan 0','timer start scan']+fw.transition([255]*16,100)+['timer stop scan','timer get scan'];t.check('debounced-all-down',packet(0,4))
    t.commands += ['timer set scan 0','timer start scan']+fw.transition([0]*16,200)+['timer stop scan','timer get scan'];t.check('debounced-all-up',packet());r=t.run();log=(fw.output/(t.name+'.log')).read_text();r['two_task_scan_clock_samples']=[int(n) for n in re.findall(r'timer #\d+\("scan"\).*?\((\d+) clks\)',log)];out.append(r)
    # Real interpreter streams, accepted by the same grammar used by packer.
    # Holds persist across separate published streams; duplicate DOWN must not
    # wrap byte-sized owner counters even after the 256th primitive.
    for key,kind,report,ref_symbol,ref_offset in [(4,'key',packet(0,4),'_key_refs',4),(0xe1,'modifier',packet(2),'_owned_mod_refs',1),(0xa9,'consumer',packet(),'_usage_refs',0xa9-0xa5),(0xa5,'system',packet(),'_usage_refs',0)]:
        t=Trace(fw,'macro-256-down-'+kind);t.map((0,0),key)
        if kind in ('consumer','system'):t.capture_extra()
        t.event((0,0),1,100);t.macro([1,3,key]);t.check('unmatched-up-retains-physical',report);t.check_memory('unmatched-owner',ref_symbol,ref_offset,[1])
        t.macro([1,2,key]*257);t.check('repeated-down',report);t.check_memory('two-owners',ref_symbol,ref_offset,[2])
        t.macro([1,1,key]);t.check('tap-retains-macro-hold',report);t.check_memory('tap-owner-count',ref_symbol,ref_offset,[2])
        t.macro([1,3,key]);t.macro([1,3,key]);t.check('separate-stream-up',report);t.check_memory('physical-owner',ref_symbol,ref_offset,[1]);t.event((0,0),0,200);t.check('physical-release',packet());r=t.run()
        if kind in ('consumer','system'):
            usage=0xe9 if kind=='consumer' else 0x81;rid=4 if kind=='consumer' else 3;r['expected_extra_callback_trace']=[[rid,usage,0],[rid,0,0]];r['pass_'] &= r['extra_callback_trace']==r['expected_extra_callback_trace']
        else:
            r['expected_hid_final']=packet();r['pass_'] &= bool(r['hid_send_trace']) and r['hid_send_trace'][-1]==packet() and all(value==report for value in r['hid_send_trace'][:-1])
        out.append(r)
    for code in (0x2204,0x4104):
        t=Trace(fw,f'macro-extended-low-byte-{code:04x}');ext=lambda op:[1,op,code&255,code>>8]
        t.macro(ext(5));t.check('tap-ended',packet(),0);t.macro(ext(6));t.check('down-basic-only',packet(0,4),0);t.macro(ext(5));t.check('tap-retains-down',packet(0,4),0);t.macro(ext(7));t.check('up-basic-only',packet(),0);r=t.run();r['expected_hid_send_trace']=[packet(0,4),packet(),packet(0,4),packet()];r['pass_'] &= r['hid_send_trace']==r['expected_hid_send_trace'];out.append(r)
    out.append(macro_cancel_case(fw))
    return out

def macro_cancel_case(fw):
    # Inject a public clear immediately after the interpreter's first DOWN.
    # Match the emitted caller's saves/restores rather than a fixed address.
    register=fw.address('_register_code');clear=fw.address('_clear_keyboard')
    pattern=[0xc0,7,0xc0,6,0xc0,5,0x12,register>>8,register&255,0xd0,5,0xd0,6,0xd0,7]
    begin=fw.address('_dynamic_keymap_macro_send')
    matches=[a+6 for a in range(begin,begin+0x400) if [fw.code.get(a+i) for i in range(len(pattern))]==pattern]
    if len(matches)!=1:raise ValueError('Expected one macro DOWN call with preserved r5/r6/r7')
    patched=matches[0];original=[fw.code[patched+i] for i in range(3)];hook=0x2640
    registers=list(range(8))+[0xe0,0xf0,0x82,0x83,0xd0]
    trampoline=[0x12,register>>8,register&255]
    for reg in registers:trampoline += [0xc0,reg]
    trampoline += [0x12,clear>>8,clear&255]
    for reg in reversed(registers):trampoline += [0xd0,reg]
    trampoline += [0x22]
    # Firmware.call owns 0x2600..0x2605 and stops at 0x2700.
    if hook < 0x2606 or hook+len(trampoline) > 0x2700:raise ValueError('Macro cancellation hook overlaps call trampoline or stop')
    if any(a in fw.code for a in range(hook,hook+len(trampoline))):raise ValueError('Macro cancellation hook overlaps linked image')
    t=Trace(fw,'macro-cancel-stops-stream');t.capture_extra()
    t.commands += [linked.memory('rom',hook,trampoline),linked.memory('rom',patched,[0x12,hook>>8,hook&255])]
    t.map((0,0),0xe1);t.map((0,1),0xa9);t.event((0,0),1,100);t.event((0,1),1,101)
    t.macro([1,2,4,1,2,5]);t.check('cancelled-empty',packet());t.check_memory('cancelled-flag','_ak820_macro_cancelled',0,[1]);t.check_memory('cancel-key-owner','_key_refs',4,[0]);t.check_memory('later-key-not-executed','_key_refs',5,[0]);t.check_memory('cancel-modifier-owner','_owned_mod_refs',1,[0]);t.check_memory('cancel-consumer-owner','_usage_refs',4,[0])
    t.map((0,0),5);t.event((0,0),0,200);t.event((0,1),0,201);t.event((0,0),1,202);t.check('fresh-key-after-cancel',packet(0,5));t.event((0,0),0,203);t.check('fresh-release',packet());r=t.run()
    r['expected_hid_send_trace']=[packet(2),packet(2,4),packet(),packet(0,5),packet()];r['expected_extra_callback_trace']=[[4,0xe9,0],[4,0,0]]
    r['simulator_patch']={'symbol':'_dynamic_keymap_macro_send','address':patched,'original_bytes':original,'replacement_bytes':[0x12,hook>>8,hook&255],'trampoline_address':hook,'trampoline_bytes':trampoline,'preserved_direct_registers':registers,'reason':'Model a public clear_keyboard call after the first actual macro DOWN output, then resume the real interpreter','limits':'Injected call timing only; no EE_CLR dispatch, reset, EEPROM, NVM persistence, IRQ overlap, power-fail or physical hardware proof. Other cases execute the original image.'}
    r['pass_'] &= r['hid_send_trace']==r['expected_hid_send_trace'] and r['extra_callback_trace']==r['expected_extra_callback_trace']
    return r

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    fw=linked.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    if any(0x2600<=address<0x2703 or address>=0xc700 for address in fw.code):raise ValueError('Image overlaps simulator trampoline or simulated NVM fixture')
    tests=cases(fw)
    for t in tests:t['pass']=t.pop('pass_')
    report=dict(level='linked SDCC 8051 CPU, real action_exec and production report pipeline',image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),initial_sp=fw.initial_sp,stack_capacity=fw.stack_capacity,runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),support_sha256=hashlib.sha256(Path(linked.__file__).read_bytes()).hexdigest(),packer_sha256=hashlib.sha256(Path(packer.__file__).read_bytes()).hexdigest(),linked_map_sha256=hashlib.sha256((fw.build/'ajazz_ak820_vial.map').read_bytes()).hexdigest(),simulator_sha256=hashlib.sha256(a.s51.read_bytes()).hexdigest(),tests=tests,limits='No physical matrix/encoder, IRQ overlap, USB, NVM persistence or physical timing proof. Simulated ROM fixtures and USB-ready state only.',pass_=all(t['pass'] for t in tests));report['pass']=report.pop('pass_');(fw.output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass':report['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']],'peak_sp':max(t['peak_sp'] for t in tests)},indent=2));return 0 if report['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
