#!/usr/bin/env python3
"""Exact linked Vial settings packet API, real EEPROM cache and effective input timing.

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

def record(grave=0,combo=40,tapping_term=200,tap_delay=0,caps_delay=80,autoshift=175,
           autoshift_flags=1,caps_word_language=0,oneshot_timeout=0,version=2):
    result=bytearray((b'QS\x01\x0b\x3f' if version==1 else b'QS\x02\x0f\x7f')+bytes([grave]))
    for value in (combo,tapping_term,tap_delay,caps_delay,autoshift):result+=value.to_bytes(2,'little')
    result+=(bytes(6) if version==1 else bytes([autoshift_flags,caps_word_language])+
             oneshot_timeout.to_bytes(2,'little')+bytes(2))
    result+=binascii.crc_hqx(result,0xffff).to_bytes(2,'little')
    assert len(result)==24
    return list(result)

def setup(fw,name,active_autoshift=False,**values):
    t=tapping.Trace(fw,name)
    t.settings_record=record(**values)
    if values.get('version')==1:t.settings_record[16]=1
    t.commands += [emitted.memory('rom',0xc700+0x6a8,record(**values))]+fw.call('_ak820_settings_init')
    if fw.has_auto_shift and not active_autoshift:
        # Reinitialization applies saved admission flags. General settings
        # traces explicitly select immediate input through the real key path.
        t.map((15,7),0x7c14);t.event((15,7),1,0);t.event((15,7),0,0);t.map((15,7),0)
    return t

def observe(t,label,address,expected,space='xram'):
    if address==BUFFER:address=t.fw.address('_raw_buffer')+1
    label += '@'
    alias='_settings_fixture_'+label;t.fw.symbols[alias]=address;t.fw.symbol_spaces[alias]=space
    t.commands+=t.fw.dump(label,space,address,len(expected));t.expected.append((label,alias,list(expected)))

def api(t,operation,qsid=0,data=None,expected=0,label='api'):
    fw=t.fw
    opcode={'query':9,'get':10,'set':11,'reset':12}[operation]
    packet=[0xfe,opcode,qsid&255,qsid>>8]+[0xa5]*28
    if data is not None:packet[4:4+len(data)]=data
    t.commands+=fw.write('_raw_buffer',packet)
    t.commands+=fw.write('_vial_handle_cmd_PARM_2',[32])
    t.commands+=fw.call('_vial_handle_cmd',fw.address('_raw_buffer'))
    if operation!='query':
        # The transport changes only status plus the width bytes of a Get.
        reply=packet[:];reply[0]=expected&255
        if operation=='get' and expected==0:
            positions={1:5,2:6,3:16,4:14,6:18,7:8,18:10,19:12,22:17}
            pos=positions[qsid];width=1 if qsid in (1,3,22) else 2
            reply[1:1+width]=t.settings_record[pos:pos+width]
        if operation=='reset' and expected==0:t.settings_record=record(caps_word_language=1)
        if operation=='set' and expected==0:
            positions={1:5,2:6,3:16,4:14,6:18,7:8,18:10,19:12,22:17}
            pos=positions[qsid];width=1 if qsid in (1,3,22) else 2
            t.settings_record[pos:pos+width]=data[:width]
        observe(t,label+'-full-packet',fw.address('_raw_buffer'),reply)


def compiled_grave_escape(fw):
    """Bind the option to this image and require its linked handler to agree."""
    report=json.loads((fw.build/'build-report.json').read_text())
    for filename in ('ajazz_ak820_vial.ihx','ajazz_ak820_vial.map'):
        rows=[row for row in report['artifacts'] if Path(row['path']).name==filename]
        digest=hashlib.sha256((fw.build/filename).read_bytes()).hexdigest()
        if len(rows)!=1 or rows[0]['sha256']!=digest:
            raise ValueError('Grave Escape configuration is not bound to linked artifact: '+filename)
    option=report['configuration']['make_options']['AK820_GRAVE_ESCAPE']
    if option not in ('yes','no'):
        raise ValueError('Invalid compiled Grave Escape option')
    enabled=option=='yes'
    if enabled!=('_process_grave_esc' in fw.symbols):
        raise ValueError('Configured Grave Escape differs from linked handler')
    return enabled

def cases(fw):
    results=[]
    has_grave_escape=compiled_grave_escape(fw)
    t=setup(fw,'settings-packet-width-range-query')
    has_autoshift='_ak820_autoshift_process' in fw.symbols
    has_oneshot='_ak820_oneshot_process' in fw.symbols
    ids=[1,2]+([3,4] if has_autoshift else [])+([6] if has_oneshot else [])+[7,18,19,22]
    api(t,'query',0,label='query')
    expected=sum(([v,0] for v in ids),[])+[255]*(32-len(ids)*2)
    observe(t,'query-values',fw.address('_raw_buffer'),expected)
    fields=[(1,0,1),(2,40,2),(7,200,2),(18,0,2),(19,80,2),(22,0,1)]
    if has_autoshift:fields += [(3,1,1),(4,175,2)]
    if has_oneshot:fields += [(6,0,2)]
    for qsid,value,width in fields:
        api(t,'get',qsid,label=f'get-{qsid}')
        observe(t,f'value-{qsid}',BUFFER,list(value.to_bytes(width,'little')))
    for qsid in (0,5,8,21,23,0x101,0xffff):
        api(t,'get',qsid,expected=-1,label=f'get-unsupported-{qsid}')
        api(t,'set',qsid,[40,0],expected=-1,label=f'set-unsupported-{qsid}')
    for qsid in (1,2,21,22,0x100,0xffff):
        api(t,'query',qsid,label=f'query-after-{qsid}')
        wanted=sum(([v,0] for v in ids if v>qsid),[])
        observe(t,f'query-after-{qsid}-full-packet',fw.address('_raw_buffer'),wanted+[255]*(32-len(wanted)))
    for qsid,data in [(1,[16]),(2,[0,0]),(3,[2]),(6,[49,117]),(7,[233,3]),(18,[101,0]),(19,[101,0]),(22,[2])]:
        api(t,'set',qsid,data,expected=-1,label=f'invalid-{qsid}')
    observe(t,'no-dirty-page',fw.address('_page_dirty'),[0],fw.symbol_space('_page_dirty'));results.append(t.run())
    t=setup(fw,'settings-packet-guards-and-reset',combo=60)
    for size in (0,1,3,31,33,255):
        packet=[0xfe,11,2,0,70,0]+[0xa5]*26
        t.commands+=fw.write('_raw_buffer',packet)+fw.write('_vial_handle_cmd_PARM_2',[size])
        t.commands+=fw.call('_vial_handle_cmd',fw.address('_raw_buffer'))
        observe(t,f'reject-length-{size}',fw.address('_raw_buffer'),packet)
    packet=[0xfe,11,2,0,70,0]+[0xa5]*26
    t.commands+=[emitted.memory('xram',BUFFER,packet)]
    t.commands+=fw.write('_vial_handle_cmd_PARM_2',[32])+fw.call('_vial_handle_cmd',BUFFER)
    observe(t,'reject-foreign-buffer',fw.address('_raw_buffer'),packet)
    t.commands+=fw.dump('foreign-packet@','xram',BUFFER,32)
    alias='_settings_fixture_foreign-packet@';fw.symbols[alias]=BUFFER;fw.symbol_spaces[alias]='xram'
    t.expected.append(('foreign-packet@',alias,packet))
    page=[0x5a]*40+record(combo=60)
    t.commands+=fw.write('_page_data',page)+fw.write_scalar('_cached_page',0x6a8//64)+fw.write('_page_valid',[1])+fw.write('_batch_depth',[1])
    api(t,'reset',label='reset-packet')
    t.check_memory('reset-cached-record','_page_data',0,[0x5a]*40+record(caps_word_language=1))
    api(t,'get',2,label='reset-value');observe(t,'reset-combo',BUFFER,[40,0])
    results.append(t.run())
    t=setup(fw,'settings-v1-ram-migration',version=1,combo=60)
    api(t,'get',2,label='legacy-value');observe(t,'legacy-combo',BUFFER,[60,0])
    api(t,'get',22,label='legacy-language');observe(t,'default-language',BUFFER,[0])
    if has_autoshift:
        api(t,'get',3,label='legacy-flags');observe(t,'default-flags',BUFFER,[1])
    if has_oneshot:
        api(t,'get',6,label='legacy-oneshot');observe(t,'default-timeout',BUFFER,[0,0])
    api(t,'set',2,[60,0],label='legacy-noop')
    observe(t,'legacy-not-written',0xc700+0x6a8,record(version=1,combo=60),'rom')
    observe(t,'legacy-no-dirty-page',fw.address('_page_dirty'),[0],fw.symbol_space('_page_dirty'))
    t.commands+=fw.write('_page_data',[0x5a]*40+record(version=1,combo=60))+fw.write_scalar('_cached_page',0x6a8//64)+fw.write('_page_valid',[1])+fw.write('_batch_depth',[1])
    api(t,'set',22,[1],label='legacy-upgrade-on-change')
    t.check_memory('upgraded-v2-record','_page_data',0,[0x5a]*40+record(combo=60,caps_word_language=1))
    results.append(t.run())
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
    t.settings_record=record(caps_word_language=1)
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
        name='settings-grave-escape-consumer-' if has_grave_escape else 'settings-grave-escape-disabled-'
        t=setup(fw,name+str(flags),grave=flags)
        api(t,'get',1,label='grave-setting-readable')
        observe(t,'grave-setting-value',BUFFER,[flags])
        t.map((0,0),0x7c16);t.map((0,1),0xe1)
        t.event((0,1),1,100);t.event((0,0),1,110)
        t.check('grave-or-escape' if has_grave_escape else 'disabled-key-retains-shift',
                tapping.packet(2,usage) if has_grave_escape else tapping.packet(2))
        t.event((0,0),0,120);t.event((0,1),0,130);t.check('grave-release',tapping.packet());results.append(t.run())
    t=setup(fw,'settings-tapping-consumer',tapping_term=60)
    t.map((0,0),0x2104);t.event((0,0),1,100);t.tick(159);t.check('early',tapping.packet())
    t.tick(160);t.check('new-threshold',tapping.packet(1));t.event((0,0),0,170);t.check('released',tapping.packet());results.append(t.run())
    if '_ak820_combo_reload' in fw.symbols:
        t=setup(fw,'settings-combo-consumer',combo=20)
        t.commands += [emitted.memory('rom',0xc700+0x658,[4,0,5,0,0x20,8,1,0,6,0])]+fw.call('_ak820_combo_reload')
        t.map((0,0),4);t.event((0,0),1,100);t.tick(119);t.check('combo-waiting',tapping.packet())
        t.tick(120);t.check('combo-flush-at-setting',tapping.packet(0,4));t.event((0,0),0,130);t.check('combo-released',tapping.packet());results.append(t.run())
    if has_autoshift:
        t=setup(fw,'settings-autoshift-consumer',autoshift=60)
        t.map((0,0),4);t.map((0,1),0x7c13)
        t.event((0,1),1,90);t.event((0,1),0,91)
        t.event((0,0),1,100);t.tick(159);t.check('as-early',tapping.packet())
        t.tick(160);t.check('as-new-threshold',tapping.packet(2,4))
        t.event((0,0),0,170);t.check('as-released',tapping.packet());results.append(t.run())
        for flags,code,shifted in ((0,4,False),(1,4,True),(17,4,False),(9,0x1e,False),(5,0x2f,False)):
            t=setup(fw,f'settings-autoshift-category-{flags}-{code}',active_autoshift=True,autoshift=60,autoshift_flags=flags)
            t.map((0,0),code);t.event((0,0),1,100)
            t.check('admission',tapping.packet() if shifted else tapping.packet(0,code))
            t.tick(160);t.check('held',tapping.packet(2 if shifted else 0,code))
            t.event((0,0),0,170);t.check('released',tapping.packet());results.append(t.run())
    for language in (0,1):
        for code in (0x2f,0x30,0x33,0x34,0x36,0x37,0x35):
            t=setup(fw,f'settings-caps-word-{language}-{code}',caps_word_language=language)
            t.map((0,0),0x7c73);t.map((0,1),code);t.map((0,2),4)
            t.event((0,0),1,90);t.event((0,0),0,91);t.event((0,1),1,100)
            t.check('ru-letter-or-en-punctuation',tapping.packet(2 if language else 0,code))
            t.event((0,1),0,101);t.event((0,2),1,102)
            t.check('word-continues-only-in-ru',tapping.packet(2 if language else 0,4));results.append(t.run())
    # Shift gestures activate the same language-specific Caps Word callback
    # as the dedicated toggle. Check every Russian letter position after both
    # activation paths, and verify English leaves those positions unshifted.
    for language in (0,1):
        for gesture in ('both-shifts','double-left-shift'):
            for index,code in enumerate((0x2f,0x30,0x33,0x34,0x36,0x37,0x35)):
                t=setup(fw,f'settings-caps-word-{gesture}-{language}-{code}',caps_word_language=language)
                t.map((0,0),0xe1);t.map((0,1),0xe5);t.map((0,2),code)
                t.map((0,3),4)
                if gesture=='both-shifts':
                    t.event((0,0),1,100);t.event((0,1),1,110)
                    t.check('activated-by-both-shifts',tapping.packet(0x22))
                    t.event((0,1),0,111);t.event((0,0),0,112)
                    code_time=120
                else:
                    # The second tap must be the same physical left Shift;
                    # row 1 remains mapped to right Shift for both-shifts.
                    t.event((0,0),1,100);t.event((0,0),0,110)
                    t.event((0,0),1,150);t.event((0,0),0,151)
                    code_time=152
                # An A proves both activation paths work in both languages
                # before testing the seven Russian physical letter positions.
                t.event((0,3),1,code_time)
                t.check('activated-language-start',tapping.packet(2,4))
                t.event((0,3),0,code_time+1)
                t.event((0,2),1,code_time+2)
                t.check('letter-position-'+str(index),tapping.packet(2 if language else 0,code))
                t.event((0,2),0,code_time+3)
                t.event((0,3),1,code_time+4)
                t.check('language-admission-after-letter',tapping.packet(2 if language else 0,4))
                t.event((0,3),0,code_time+5)
                results.append(t.run())
    if has_oneshot:
        for timeout,start in ((0,100),(60,100),(60,65500)):
            t=setup(fw,f'settings-oneshot-timeout-{timeout}-{start}',oneshot_timeout=timeout)
            t.map((0,0),0x52a1);t.map((0,1),4)
            t.commands+=fw.clock(start)
            t.event((0,0),1,start);t.event((0,0),0,start)
            t.tick((start+59)&65535);t.check('queued-before-deadline',tapping.packet(1))
            t.tick((start+60)&65535);t.check('timeout-or-unlimited',tapping.packet(0 if timeout else 1))
            t.event((0,1),1,(start+61)&65535);t.check('next-key',tapping.packet(0 if timeout else 1,4))
            t.event((0,1),0,(start+62)&65535);t.check('released',tapping.packet());results.append(t.run())
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
    report=dict(level='exact linked C52 Vial 32-byte packet API, EEPROM batched cache and real handler timing consumers',image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),tests=tests,helper_delay_comparisons=timings,limits='Successful setters use an explicit outer batch and prove cache updates, not durable IAP. Separate ROM fixtures model restart. No physical flash, USB, IRQ overlap or physical latency proof.',pass_=all(t['pass'] for t in tests))
    report['pass']=report.pop('pass_');(fw.output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass':report['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']]},indent=2));return int(not report['pass'])
if __name__=='__main__':raise SystemExit(main())
