#!/usr/bin/env python3
"""Exact linked settings API, real EEPROM cache and effective input timing.

Successful setters run inside an explicit outer NVM batch: cache/ABI execution
is checked, while unmodelled flash persistence is deliberately not claimed.
"""
import argparse
import binascii
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('tapping',ROOT/'tests/ak820_tapping/emitted.py')
tapping=importlib.util.module_from_spec(spec);spec.loader.exec_module(tapping)
emitted=tapping.linked
BUFFER=0x2400

def record(grave=0,combo=40,tapping_term=200,tap_delay=0,caps_delay=80,autoshift=175):
    result=bytearray(b'QS\x01\x0b\x3f'+bytes([grave]))
    for value in (combo,tapping_term,tap_delay,caps_delay,autoshift):result+=value.to_bytes(2,'little')
    result+=bytes(6)
    result+=binascii.crc_hqx(result,0xffff).to_bytes(2,'little')
    assert len(result)==24
    return list(result)

def setup(fw,name,**values):
    t=tapping.Trace(fw,name)
    t.commands += [emitted.memory('rom',0xc700+0x6a8,record(**values))]+fw.call('_ak820_settings_init')
    return t

def observe(t,label,address,expected,space='xram'):
    label += '@'
    alias='_settings_fixture_'+label;t.fw.symbols[alias]=address;t.fw.symbol_spaces[alias]=space
    t.commands+=t.fw.dump(label,space,address,len(expected));t.expected.append((label,alias,list(expected)))

def api(t,operation,qsid=0,data=None,capacity=2,expected=0,label='api'):
    fw=t.fw
    if data is not None:t.commands += [emitted.memory('xram',BUFFER,data)]
    t.commands+=fw.write('_ak820_settings_'+operation+'_PARM_2',[BUFFER&255,BUFFER>>8])
    t.commands+=fw.write('_ak820_settings_'+operation+'_PARM_3',[capacity])
    t.commands+=fw.call('_ak820_settings_'+operation,qsid)
    if operation!='query':observe(t,label,0x82,list((expected&65535).to_bytes(2,'little')),'sfr')

def cases(fw):
    results=[]
    t=setup(fw,'settings-api-width-range-query')
    ids=[1,2]+([4] if '_ak820_autoshift_process' in fw.symbols else [])+[7,18,19]
    api(t,'query',0,capacity=16,label='query')
    expected=sum(([v,0] for v in ids),[])+[255]*(16-len(ids)*2)
    observe(t,'query-values',BUFFER,expected)
    for qsid,value,width in [(1,0,1),(2,40,2),(7,200,2),(18,0,2),(19,80,2)]:
        api(t,'get',qsid,capacity=width,label=f'get-{qsid}')
        observe(t,f'value-{qsid}',BUFFER,list(value.to_bytes(width,'little')))
    api(t,'get',2,capacity=1,expected=-1,label='get-short')
    api(t,'get',21,capacity=4,expected=-1,label='get-unsupported')
    for qsid,data in [(1,[16]),(2,[0,0]),(7,[233,3]),(18,[101,0]),(19,[101,0])]:
        api(t,'set',qsid,data,capacity=len(data),expected=-1,label=f'invalid-{qsid}')
    api(t,'set',2,[40,0],capacity=1,expected=-1,label='set-short')
    observe(t,'no-dirty-page',fw.address('_page_dirty'),[0],fw.symbol_space('_page_dirty'));results.append(t.run())
    t=setup(fw,'settings-noop-and-batched-transaction')
    t.map((0,0),4);t.event((0,0),1,100)
    api(t,'set',2,[40,0],label='unchanged')
    t.check('noop-retains-owner',tapping.packet(0,4))
    page=[0x5a]*40+record()
    t.commands+=fw.write('_page_data',page)+fw.write_scalar('_cached_page',0x6a8//64)+fw.write('_page_valid',[1])+fw.write('_batch_depth',[1])
    api(t,'set',2,[60,0],label='batch-set')
    t.check('changed-cancels-owner',tapping.packet())
    t.check_memory('cached-record','_page_data',0,[0x5a]*40+record(combo=60))
    observe(t,'dirty-cache',fw.address('_page_dirty'),[1],fw.symbol_space('_page_dirty'))
    api(t,'get',2,label='get-changed');observe(t,'changed-value',BUFFER,[60,0])
    t.event((0,0),1,110);t.check('held-source-blocked',tapping.packet())
    t.event((0,0),0,120);t.event((0,0),1,130);t.check('fresh-source',tapping.packet(0,4))
    results.append(t.run())
    t=setup(fw,'settings-malformed-reboot')
    bad=record(combo=60);bad[6]^=1
    t.commands += [emitted.memory('rom',0xc700+0x6a8,bad)]+fw.call('_ak820_settings_init')
    observe(t,'schema-fault',fw.address('_storage_failed'),[1],fw.symbol_space('_storage_failed'))
    api(t,'get',2,label='fault-default-get');observe(t,'fault-default-value',BUFFER,[40,0])
    api(t,'set',2,[60,0],expected=-1,label='fault-refuses-write');results.append(t.run())
    t=setup(fw,'settings-real-flash-not-ready')
    # Generic C52 provides no ready flash controller. Production NVM must
    # reject, latch a fault and keep the old runtime value, never claim success.
    t.commands += [emitted.memory('sfr',0x86,[0])]
    api(t,'set',2,[60,0],expected=-1,label='not-ready')
    observe(t,'write-fault',fw.address('_storage_failed'),[1],fw.symbol_space('_storage_failed'))
    api(t,'get',2,label='old-runtime');observe(t,'old-runtime-value',BUFFER,[40,0]);results.append(t.run())
    for flags,usage in ((0,0x35),(8,0x29)):
        t=setup(fw,'settings-grave-escape-consumer-'+str(flags),grave=flags)
        t.map((0,0),0x7c16);t.map((0,1),0xe1)
        t.event((0,1),1,100);t.event((0,0),1,110)
        t.check('grave-or-escape',tapping.packet(2,usage))
        t.event((0,0),0,120);t.event((0,1),0,130);t.check('grave-release',tapping.packet());results.append(t.run())
    t=setup(fw,'settings-tapping-consumer',tapping_term=60)
    t.map((0,0),0x2104);t.event((0,0),1,100);t.tick(159);t.check('early',tapping.packet())
    t.tick(160);t.check('new-threshold',tapping.packet(1));t.event((0,0),0,170);t.check('released',tapping.packet());results.append(t.run())
    if '_ak820_combo_reload' in fw.symbols:
        t=setup(fw,'settings-combo-consumer',combo=20)
        t.commands += [emitted.memory('rom',0xc700+0x658,[4,0,5,0,0x20,8,1,0,6,0])]+fw.call('_ak820_combo_reload')
        t.map((0,0),4);t.event((0,0),1,100);t.tick(119);t.check('combo-waiting',tapping.packet())
        t.tick(120);t.check('combo-flush-at-setting',tapping.packet(0,4));t.event((0,0),0,130);t.check('combo-released',tapping.packet());results.append(t.run())
    if '_ak820_autoshift_process' in fw.symbols:
        t=setup(fw,'settings-autoshift-consumer',autoshift=60)
        t.map((0,0),4);t.map((0,1),0x7c13)
        t.event((0,1),1,90);t.event((0,1),0,91)
        t.event((0,0),1,100);t.tick(159);t.check('as-early',tapping.packet())
        t.tick(160);t.check('as-new-threshold',tapping.packet(2,4))
        t.event((0,0),0,170);t.check('as-released',tapping.packet());results.append(t.run())
    # Check real tap_code helpers consume each delay by comparing instruction
    # clocks with otherwise identical ROM-seeded records. No hardware ms claim.
    timings=[]
    for caps in (False,True):
        samples=[]
        for delay in (0,3):
            values={'caps_delay':delay} if caps else {'tap_delay':delay}
            t=setup(fw,f'settings-helper-delay-{caps}-{delay}',**values)
            code=0x39 if caps else 4
            t.commands+=['timer add helper','timer set helper 0','timer start helper']+fw.call('_tap_code',code)+['timer stop helper','timer get helper']
            t.check('helper-released',tapping.packet());r=t.run()
            import re
            log=(fw.output/(t.name+'.log')).read_text()
            clocks=[int(n) for n in re.findall(r'timer #\d+\("helper"\).*?\((\d+) clks\)',log)]
            if len(clocks)!=1:raise ValueError('Missing linked tap_code timer sample')
            r['helper_clocks']=clocks[0];samples.append(r);results.append(r)
        ok=samples[1]['helper_clocks']>samples[0]['helper_clocks']
        for sample in samples:sample['pass_'] &= ok
        timings.append(dict(caps=caps,zero_clocks=samples[0]['helper_clocks'],three_ms_clocks=samples[1]['helper_clocks'],pass_=ok))
    return results,timings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for option in ('build-dir','s51','output-dir'):p.add_argument('--'+option,type=Path,required=True)
    a=p.parse_args();fw=emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    fw.address('_ak820_settings_init')
    tests,timings=cases(fw)
    for t in tests:t['pass']=t.pop('pass_')
    report=dict(level='exact linked C52 API, EEPROM batched cache and real handler timing consumers',image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),tests=tests,helper_delay_comparisons=timings,limits='Successful setters use an explicit outer batch and prove cache updates, not durable IAP. Separate ROM fixtures model restart. No physical flash, USB, IRQ overlap or physical latency proof.',pass_=all(t['pass'] for t in tests))
    report['pass']=report.pop('pass_');(fw.output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass':report['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']]},indent=2));return int(not report['pass'])
if __name__=='__main__':raise SystemExit(main())
