#!/usr/bin/env python3
"""Execute OS indicator production code in a supplied linked image, offline.

The generic C52 CPU runs the real SDCC instructions. USB registers, timer and
Raw32 ready state are memory fixtures. No physical USB/IRQ timing is modeled.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('os_unlock',ROOT/'tests/ak820_unlock/run.py')
unlock=importlib.util.module_from_spec(spec); spec.loader.exec_module(unlock)
emitted=unlock.emitted

def request(fw,mode=0,action=1,packet=None):
    data=packet if packet is not None else [0xfd,2,1,action,mode]+[0]*27
    return (fw.write('_raw_buffer',data)+fw.write('_raw_state',[2])+  # RAW_READY
            [emitted.memory('xram',0x2203,[0x12])]+fw.call('_ak820_usb_raw_task'))

def expected_dma(caps,w,os):
    data=[0x69]*36
    data[0:2]=[caps,caps];data[32:34]=[255 if w or os else 0,w];data[35]=os
    return data

def run_case(fw,name,setup,checks):
    commands=list(setup);observations=[]
    for label,space,addr,expected,transition in checks:
        commands+=transition+fw.dump(label+'@',space,addr,len(expected))
        observations.append((label,addr,expected))
    log,stack=fw.execute(name,commands)
    actual={}
    for label,addr,expected in observations:
        tail=log.rsplit('@@'+label+'@',1)[1]
        sfr=re.search(r'^0x'+format(addr,'x')+r'\s+\w+:.*?0x([0-9a-f]{2})',tail,re.M)
        actual[label]=[int(sfr[1],16)] if sfr and len(expected)==1 else fw.extract(log,label+'@',addr,len(expected))
    expected={label:value for label,addr,value in observations}
    return {'name':name,'pass':actual==expected,'observations':actual,'expected':expected,**stack}

def pulse_angles(fw):
    """Exhaust the actual linked helper; scratch ROM/RAM exists only in C52."""
    target=fw.address('_gui_pulse_angle')
    # 0x2000 is simulator scratch code, 0x2700 is its stop address, and
    # XRAM 0x3000..0x37cf holds results. The supplied IHX file is never changed.
    commands=fw.initialize()
    for phase in range(2000):
        code=[]
        for register in range(8):
            code += [0x78+register,0x11*(register+1)]
        code += [0x90,phase>>8,phase&255,0x12,target>>8,target&255,
                 0x85,0x82,0xf0,0x90,0x30+(phase>>8),phase&255,0xe5,0xf0,0xf0]
        for register in range(8):
            # Equal sentinels skip the failure loop; a clobber times out.
            code += [0xe8+register,0xb4,0x11*(register+1),2,0x80,3,0x02,0x20,0]
        code += [0x02,0x27,0]
        commands += [emitted.memory('rom',0x2000,code),'run 0x2000 0x2700']
    commands += fw.dump('pulse_angles@','xram',0x3000,2000)
    log,stack=fw.execute('gui-lock-all-angles-registers',commands)
    actual=fw.extract(log,'pulse_angles@',0x3000,2000)
    expected=[(192+phase*16//125)&255 for phase in range(2000)]
    return {'name':'gui-lock-all-angles-registers','pass':actual==expected,
            'cases':2000,'helper_address':target,
            'preserved_registers':[f'R{i}' for i in range(8)],**stack}

def cases(fw):
    dma=fw.address('_ak820_led_dma')+0x11c
    mode=fw.address('_ak820_os_indicator_mode')
    setup=fw.initialize()+fw.write('_USB_SleepStatus',[0])
    # When compact GUI lock is in this exact image, exercise its production
    # state accessor together with the shared W indicator and breathing curve.
    # The 2 s cycle is sampled at quarter periods; timer fixtures wrap at 16 bits.
    if '_ak820_gui_lock_is_active' in fw.symbols:
        yield pulse_angles(fw)
        def gui_lock_call(active):
            return (fw.write('_ak820_gui_process_PARM_2',[1])+
                    fw.call('_ak820_gui_process',0x700a if active else 0x7009))
        pulse_dma=fw.address('_ak820_led_dma')+0x13c
        yield run_case(fw,'gui-lock-default-disabled',setup,[
            ('normal-base','xram',pulse_dma,[0,0],fw.clock(100)+
             fw.write_scalar('_layer_state',1)+fw.write_scalar('_default_layer_state',1)+
             fw.call('_ak820_update_indicators'))])
        pulse_checks=[]
        for t,w in ((100,1),(600,128),(1100,255),(1600,128),(2100,1)):
            transition=(fw.clock(t)+(gui_lock_call(True) if t==100 else [])+
                        fw.write_scalar('_layer_state',1)+fw.write_scalar('_default_layer_state',1)+
                        fw.call('_ak820_update_indicators'))
            pulse_checks.append((f'gui-lock-pulse-{t}','xram',pulse_dma,[255,w],transition))
        pulse_checks.append(('gui-lock-caps-independent','xram',
                             fw.address('_ak820_led_dma')+0x11c,[255,255],
                             fw.write('_KB_USB_SetReport',[2])+fw.call('_ak820_update_indicators')))
        pulse_checks.append(('gui-lock-layer-priority','xram',pulse_dma,[255,255],
                             fw.clock(2200)+fw.write_scalar('_layer_state',2)+
                             fw.call('_ak820_update_indicators')))
        pulse_checks.append(('gui-lock-default-layer-priority','xram',pulse_dma,[255,255],
                             fw.write_scalar('_layer_state',1)+fw.write_scalar('_default_layer_state',4)+
                             fw.call('_ak820_update_indicators')))
        pulse_checks.append(('gui-lock-suspend-clears','xram',pulse_dma,[0,0],
                             fw.write('_USB_SleepStatus',[2])+fw.call('_ak820_update_indicators')))
        yield run_case(fw,'gui-lock-w-pulse-priority-suspend',setup,pulse_checks)
        wrap_checks=[]
        wrap_checks.append(('timer-wrap-quarter-cycle','xram',pulse_dma,[255,128],
                            fw.clock(65500)+gui_lock_call(True)+fw.write_scalar('_layer_state',1)+
                            fw.write_scalar('_default_layer_state',1)+fw.call('_ak820_update_indicators')+
                            fw.clock(66000)+fw.call('_ak820_update_indicators')))
        yield run_case(fw,'gui-lock-w-pulse-timer-wrap',setup,wrap_checks)
    # The production wire task owns the request, validates it and sets the lease.
    for mac in ((0,1) if "_ak820_mac_mode" in fw.symbols else (0,)):
        for caps in (0,255):
            for layers,defaults in ((1,1),(2,1),(1,4)):
                checks=[]
                for override,os in ((0,255 if mac else 0),(1,0),(2,255),(3,128)):
                    transition=((fw.write('_ak820_mac_mode',[mac]) if '_ak820_mac_mode' in fw.symbols else [])+fw.clock(1024)+request(fw,override)+
                        [emitted.memory('xram',dma,[0x69]*36)]+
                        fw.write('_KB_USB_SetReport',[2 if caps else 0])+
                        fw.write_scalar('_layer_state',layers)+fw.write_scalar('_default_layer_state',defaults)+
                        fw.call('_ak820_update_indicators'))
                    checks.append(('mode_'+str(override),'xram',dma,expected_dma(caps,255 if (layers|defaults)&~1 else 0,os),transition))
                yield run_case(fw,f'dma-mac-{mac}-caps-{caps}-layer-{layers}-default-{defaults}',setup,checks)
    checks=[]
    for irq in (0,1):
        checks.append((f'led_irq_{irq}','sfr',0xe8,[0x05 | (irq<<5)],
                       [emitted.memory('sfr',0xe8,[0x05 | (irq<<5)])]+fw.call('_ak820_update_indicators')))
        checks.append((f'global_irq_{irq}','sfr',0xa8,[irq<<7],
                       [emitted.memory('sfr',0xa8,[irq<<7])]+fw.clock(100)+request(fw,2)))
    yield run_case(fw,'interrupt-enable-state-restored',setup,checks)
    # A GET near expiry and a malformed SET must neither renew nor mutate.
    checks=[]
    def check(label,expected,transition):
        checks.append((label,'xram',mode,[expected],transition+fw.call('_ak820_os_indicator_get')))
    check('set',2,fw.clock(100)+request(fw,2))
    check('get_before_expiry',2,fw.clock(3099)+request(fw,0,0))
    check('get_at_expiry',0,fw.clock(3100)+request(fw,0,0))
    check('wrap_set',1,fw.clock(0xfffffff0)+request(fw,1))
    check('wrap_before',1,fw.clock(0xba7))
    check('wrap_expiry',0,fw.clock(0xba8))
    check('long_set',2,fw.clock(10)+request(fw,2))
    check('long_gap',0,fw.clock(65546))
    check('malformed_set_base',1,fw.clock(80000)+request(fw,1))
    bad=[0xfd,2,1,1,2]+[0]*27;bad[31]=1
    check('malformed_preserves',1,fw.clock(82000)+request(fw,packet=bad))
    check('malformed_no_renew',0,fw.clock(83000))
    check('unlock_set',2,fw.clock(84000)+request(fw,2))
    check('unlock_cancels',0,unlock.vial(fw,6))
    check('unlock_cancel_stays_normal',0,unlock.vial(fw,8))
    yield run_case(fw,'lease-wrap-long-gap-get-malformed-unlock',setup,checks)
    # Refresh throughout a full waveform; phase continues across refresh.
    checks=[]
    for t,w in ((0,0),(1024,128),(2032,254),(2048,254),(3072,126),(4080,0),(4096,0),(5120,128)):
        transition=(fw.clock(t)+request(fw,3)+fw.write_scalar('_layer_state',1)+
                    fw.write_scalar('_default_layer_state',1)+fw.call('_ak820_update_indicators'))
        checks.append((f't_{t}','xram',dma+35,[w],transition))
    checks.append(('expired','xram',dma+35,[0],fw.clock(8120)+fw.call('_ak820_update_indicators')))
    yield run_case(fw,'breathe-refresh-keeps-global-phase',setup,checks)
    # These are the retained production functions used by lifecycle handlers.
    checks=[]
    for name in ('_endpoints_reset','_USB_Device_Init'):
        checks.append((name,'xram',mode,[0],fw.clock(100)+request(fw,2)+fw.call(name)))
    yield run_case(fw,'production-reset-and-init-clear',setup,checks)
    # Standard SET_CONFIGURATION parser, using its actual EP0 packet.
    checks=[]
    for value in (0,1):
        transition=(fw.write('_USB_EnumStatus',[1])+fw.write('_D0UsbConfig',[1])+fw.clock(100)+request(fw,2)+
                    [emitted.memory('xram',0x1000,[0,9,value,0,0,0,0,0])]+fw.call('_control_setup'))
        checks.append((f'configuration_{value}','xram',mode,[0],transition))
    yield run_case(fw,'production-set-configuration-clear',setup,checks)
    # uCsim stores MMIO as RAM. Retire write-one-to-clear flags at the native
    # acknowledge write, without replacing any production instruction.
    for event,flag in (('reset',1),('suspend',0x0c)):
        commands=(fw.clock(100)+request(fw,2)+
                  ['break xram w 0x223d',
                   'commands 1 "delete 1; step; set memory xram 0x223d 0; run"',
                   emitted.memory('xram',0x223d,[flag])]+
                  fw.call('_USB_DeviceInterrupt'))
        yield run_case(fw,'production-irq-'+event+'-clear',setup,
                       [(event,'xram',mode,[0],commands)])

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-dir',required=True,type=Path);p.add_argument('--s51',required=True,type=Path)
    p.add_argument('--output-dir',required=True,type=Path);args=p.parse_args()
    fw=emitted.Firmware(args.build_dir.resolve(),args.s51.resolve(),args.output_dir.resolve())
    result={'linked_image_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),
            'level':'uCsim C52 production instructions; simulated timer/USB registers, no hardware validation',
            'tests':list(cases(fw)),'hardware_validated':False}
    result['pass']=all(t['pass'] for t in result['tests'])
    (fw.output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__':main()
