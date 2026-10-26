#!/usr/bin/env python3
"""Linked Direct v1 CPU fixtures; never access a keyboard or fake NVM."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def run(fw, support):
    if '_ak820_direct_request' not in fw.symbols:
        return {'available': False, 'pass': True, 'reason': 'Direct v1 entry point is absent in this profile'}
    commands = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"]
    commands += fw.write('_USB_EnumStatus', [1]) + fw.write('_D0UsbConfig', [1])
    commands += fw.write('_rgb_matrix_config', [20, 0, 255, 80, 96, 255, 0, 0])
    commands += fw.clock(100)
    observations = []
    unchanged = []
    def preserve_before(label, space, address, size):
        nonlocal commands
        commands += fw.dump(label+'_BEFORE_END', space, address, size)
        unchanged.append((label, space, address, size))
    def preserve_after():
        nonlocal commands
        for label, space, address, size in unchanged:
            commands += fw.dump(label+'_AFTER_END', space, address, size)
    def check(label, symbol, expected):
        nonlocal commands
        label += '_END'
        commands += fw.dump_symbol(label, symbol, len(expected))
        observations.append((label, fw.address(symbol), expected))
    def request(label, kind, op, args=(), expected=None, raw=False):
        nonlocal commands
        packet = [kind, op] + list(args)
        packet += [0] * (32-len(packet))
        commands += fw.write('_raw_buffer', packet)
        if raw:
            # Fixture only the received-packet boundary; execute the real RAW
            # classifier, Direct handler and USB reply path.
            commands += fw.write('_raw_state', [2]) + fw.call('_ak820_usb_raw_task')
        else:
            commands += fw.call('_ak820_direct_request')
        if expected is not None:
            reply = packet[:]
            # Accepted chunks clamp brightness in their shared RAW argument
            # buffer before copying/comparing the staged HSV bytes.
            if kind == 7 and op == 0x44 and isinstance(expected, int) and expected in (0, 1):
                for i in range(8, min(6 + packet[5] * 3, 32), 3):
                    reply[i] = min(reply[i], 160)
            if isinstance(expected, int): reply[2] = expected
            else: reply[2:2+len(expected)] = expected
            check(label, '_raw_buffer', reply)
    le = lambda n, width: list(n.to_bytes(width, 'little'))
    def begin(label, ident=17, generation=0, result=0):
        request(label,7,0x43,[1,82]+le(ident,2)+le(generation,4),result)
    def chunk(label, first, colors, ident=17, result=0):
        request(label,7,0x44,le(ident,2)+[first,len(colors)//3]+colors,result)
    def status(label,state,coverage,ident,generation,flags=2):
        request(label,8,0x47,expected=[state,coverage]+le(ident,2)+le(generation,4)+[flags])
    def upload(label, ident, generation, colors):
        begin(label+'_begin',ident,generation)
        for first in range(0,82,8): chunk(label+f'_chunk_{first}',first,colors[first*3:min(first+8,82)*3],ident)
        request(label+'_commit',7,0x45,le(ident,2),0)
    palette = [item for i in range(82) for item in (i,255,255)]
    clamped = [min(v,160) if i%3==2 else v for i,v in enumerate(palette)]
    request('capabilities',8,0x45,expected=[65,68,1,3,82,1,1,160,7,8,232,3])
    status('initial',0,0,0,0)
    # Failed transactions must leave all 246 active bytes unchanged.
    begin('begin'); chunk('first',0,palette[:24]); chunk('duplicate_clamped',0,clamped[:24])
    chunk('wrong_id',8,palette[24:48],18,5); status('wrong_id_preserves',1,8,17,0)
    request('missing_commit',7,0x45,le(17,2),4); status('missing_cancelled',6,8,17,0)
    begin('conflict_begin'); chunk('conflict_first',0,palette[:24]); chunk('conflict',0,[99]+palette[1:24],result=1)
    for first,count in [(1,1),(82,1),(0,9),(0,0),(80,3)]:
        begin(f'range_begin_{first}_{count}')
        request(f'range_{first}_{count}',7,0x44,le(17,2)+[first,count]+[0]*min(count*3,24),1)
    check('errors_preserve_palette','_g_direct_mode_colors',[0]*246)
    begin('abort_begin'); request('wrong_abort',7,0x46,le(18,2),5)
    request('abort',7,0x46,le(17,2),0); status('aborted',6,0,17,0)
    commands += fw.clock(65500); begin('wrap_begin')
    commands += fw.clock(66499); status('before_timeout',1,0,17,0)
    commands += fw.clock(66500); status('timeout_wrap',6,0,17,0)
    upload('dark',19,0,palette); status('dark_done',5,82,19,1)
    check('dark_palette','_g_direct_mode_colors',clamped)
    preserve_before('get_nvm_rom', 'rom', 0xc700, 0x2880)
    preserve_before('get_stage', 'xram', fw.address('_ak820_direct_stage'), 246)
    preserve_before('get_flash_diagnostic', 'xram', fw.address('_ak820_flash_diagnostic'), fw.symbol_sizes['_ak820_flash_diagnostic'])
    request('stale_get',8,0x46,le(0,4)+[0,1], [3,0,1,2]+le(1,4))
    for first in range(0,82,7):
        count=min(7,82-first)
        request(f'full_read_{first}',8,0x46,le(1,4)+[first,count], [0,first,count,2]+le(1,4)+clamped[first*3:(first+count)*3])
    for first,count in [(0,0),(0,8),(82,1),(81,2)]:
        request(f'bad_get_{first}_{count}',8,0x46,le(1,4)+[first,count],[1,first,count,2]+le(1,4))
    preserve_after()
    # GETs cannot mutate RGB mode, lock state, palette, stage or generation.
    check('gets_config','_rgb_matrix_config',[20,0,255,80,96,255,0,0])
    check('gets_lock','_vial_unlock_in_progress',[0])
    check('gets_palette','_g_direct_mode_colors',clamped)
    begin('legacy_begin',20,1)
    def legacy(label):
        nonlocal commands
        commands += fw.write('_raw_buffer',[7,0x42,0,0,1,85,255,80]+[0]*24)
        commands += fw.write('_vialrgb_set_value_PARM_2',[32])+fw.call('_vialrgb_set_value',fw.address('_raw_buffer'))
    legacy('legacy'); status('legacy_invalidates',6,0,20,2)
    # Seed every physical slot, including indicators and unused slots.
    old=[17,18,19,20]*128
    commands += fw.write('_ak820_led_dma',old)+fw.write('_rgb_matrix_config',[21,0,255,80,96,255,0,0])
    red=[0,255,80]*82
    upload('visible',21,2,red); status('render',2,82,21,3,3)
    request('duplicate_commit',7,0x45,le(21,2),0)
    begin('pending_cannot_reuse',22,3,2)
    legacy('postcommit_legacy')
    commands += fw.clock(67000)
    for i in range(11):
        commands += fw.call('_rgb_matrix_task')
        check(f'conversion_dma_{i}','_ak820_led_dma',old)
    status('queued',3,82,21,4,3)
    begin('queued_cannot_reuse',22,4,2)
    request('accepted_abort_rejected',7,0x46,le(21,2),2)
    # A nonzero row must never begin publishing a queued frame.
    commands += [support.memory('sfr',0xa6,[4])]+fw.call('_ak820_led_irq')
    check('nonzero_row_preserves','_ak820_led_dma',old)
    expected=old[:]
    slots=[fw.code[fw.address('_ak820_rgb_slots')+i] for i in range(82)]
    for row in range(16):
        commands += [support.memory('sfr',0xa6,[(row-1)&15])]+fw.call('_ak820_led_irq')
        for slot in slots:
            if slot//8==row: expected[slot*4:slot*4+4]=[255,18,0,0]
        check(f'publication_row_{row}','_ak820_led_dma',expected[:])
        if row == 0: begin('publication_cannot_reuse',22,4,2)
    status('published',5,82,21,4,3)
    upload('back_to_back',22,4,red)
    # Change mode during conversion: cursor must still complete and release stage.
    commands += fw.call('_rgb_matrix_task')+fw.write('_rgb_matrix_config',[5,0,255,80,96,255,0,0])
    for _ in range(10): commands += fw.call('_rgb_matrix_task')
    status('mode_change_completed',5,82,22,5,1)
    begin('after_conversion_begin',23,5)
    # Exercise production cancellation at every pending stage. SET_CONFIGURATION
    # enters the real USB setup handler and raises its private reset latch;
    # protocol_pre_task must consume it. Calling the ISR is unsuitable here:
    # generic C52 does not implement the controller's write-one-to-clear flags.
    generation = 5
    retained = red
    for lifecycle in ('suspend', 'reset'):
        for state in (1, 2, 3, 4):
            label = f'{lifecycle}_{state}'
            ident = 30 + state + (10 if lifecycle == 'reset' else 0)
            colors = [item for i in range(82) for item in (i + state, 200, 60 + state)]
            commands += fw.write('_rgb_matrix_config', [21,0,255,80,96,255,0,0])
            commands += fw.call('_rgb_matrix_set_suspend_state', 0)
            if state == 1:
                begin(label+'_begin', ident, generation)
                chunk(label+'_partial', 0, colors[:24], ident)
                coverage = 8
            else:
                upload(label, ident, generation, colors)
                generation += 1
                retained = colors
                coverage = 82
                # RENDER includes an interrupted, partially converted stage.
                for _ in range(1 if state == 2 else 11):
                    commands += fw.call('_rgb_matrix_task')
                if state == 4:
                    commands += [support.memory('sfr',0xa6,[15])] + fw.call('_ak820_led_irq')
            status(label+'_pending', state, coverage, ident, generation, 3)
            if lifecycle == 'suspend':
                commands += fw.call('_rgb_matrix_set_suspend_state', 1)
            else:
                commands += [support.memory('xram',0x1000,[0,9,1,0,0,0,0,0])]
                commands += fw.call('_control_setup')
                check(label+'_reset_raised', '_keyboard_reset', [1])
                commands += fw.call('_protocol_pre_task')
                check(label+'_reset_consumed', '_keyboard_reset', [0])
            status(label+'_cancelled', 6, coverage, ident, generation, 7 if lifecycle == 'suspend' else 3)
            check(label+'_retains_all_hsv', '_g_direct_mode_colors', retained)
            # BEGIN and CHUNK must immediately regain staging ownership. Its
            # replacement bytes must never be mistaken for a queued RGB frame.
            begin(label+'_reuse', ident+100, generation)
            chunk(label+'_reuse_chunk', 0, [99,201,73]*8, ident+100)
            commands += fw.write('_ak820_led_dma', old)
            for row in range(32):
                commands += [support.memory('sfr',0xa6,[(row-1)&15])] + fw.call('_ak820_led_irq')
            check(label+'_no_old_publication', '_ak820_led_dma', old)
            commands += fw.write('_rgb_matrix_config', [20,0,255,80,96,255,0,0])
            for _ in range(12): commands += fw.call('_rgb_matrix_task')
            status(label+'_tasks_do_not_resurrect', 1, 8, ident+100, generation, 6 if lifecycle == 'suspend' else 2)
            check(label+'_tasks_retain_hsv', '_g_direct_mode_colors', retained)
            # Even after foreground rendering, IRQ must not publish reused stage.
            commands += fw.write('_ak820_led_dma', old)
            for row in range(16):
                commands += [support.memory('sfr',0xa6,[(row-1)&15])] + fw.call('_ak820_led_irq')
            check(label+'_later_no_publication', '_ak820_led_dma', old)
            commands += fw.call('_rgb_matrix_set_suspend_state', 0)
    # Actual production RAW routing must bypass NVM for both readers and setters,
    # with the store left in its CRT-only fixture state.
    raw_guards = [('raw_nvm_diagnostic','xram',fw.address('_raw_buffer'),7),
                  ('raw_nvm_rom','rom',0xc700,0x2880),
                  ('raw_flash_diagnostic','xram',fw.address('_ak820_flash_diagnostic'),fw.symbol_sizes['_ak820_flash_diagnostic'])]
    commands += fw.call('_ak820_nvm_diagnostic', fw.address('_raw_buffer'))
    for label,space,address,size in raw_guards:
        commands += fw.dump(label+'_BEFORE_END',space,address,size)
        unchanged.append((label,space,address,size))
    request('raw_capabilities',8,0x45,expected=[65,68,1,3,82,1,1,160,7,8,232,3],raw=True)
    request('raw_begin',7,0x43,[1,82]+le(200,2)+le(generation,4),0,raw=True)
    request('raw_chunk',7,0x44,le(200,2)+[0,1,35,240,75],0,raw=True)
    request('raw_status',8,0x47,expected=[1,1]+le(200,2)+le(generation,4)+[2],raw=True)
    request('raw_hsv',8,0x46,le(generation,4)+[0,7],[0,0,7,2]+le(generation,4)+retained[:21],raw=True)
    request('raw_abort',7,0x46,le(200,2),0,raw=True)
    commands += fw.call('_ak820_nvm_diagnostic', fw.address('_raw_buffer'))
    for label,space,address,size in raw_guards:
        commands += fw.dump(label+'_AFTER_END',space,address,size)
    log,stack=fw.execute('direct-v1',commands)
    for label,address,expected in observations:
        actual=fw.extract(log,label,address,len(expected))
        assert actual==expected,(label,actual,expected)
    for label, space, address, size in unchanged:
        assert fw.extract(log,label+'_BEFORE_END',address,size)==fw.extract(log,label+'_AFTER_END',address,size), label
    return {'available':True,'pass':True,'observations':len(observations), 'unchanged_region_guards':len(unchanged),
            'coverage':['full 82 LED HSV reads and generation', 'brightness clamping and duplicate equivalence',
                        'malformed, incomplete, wrong-ID, stale, abort and timeout-wrap transactions',
                        'disabled palette and read-only GET region guards', 'legacy fastset invalidation',
                        'frozen post-commit frame and staging ownership', 'all 16 scan rows and indicator preservation',
                        'back-to-back commits and mode change during conversion',
                        'production suspend and USB reset-latch cancellation in UPLOAD, RENDER, QUEUED and PUBLISH',
                        'complete accepted HSV retention, immediate staging reuse and no cancelled-frame resurrection',
                        'production RAW task read/set routing with unchanged NVM ROM, NVM diagnostics and flash diagnostics'], 'ihx_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),**stack,
            'limits':'CRT and linked CPU execution with RAM/SFR fixtures; no NVM fixture writes or storage calls. Generic C52 does not model native DMA, USB endpoint timing, physical LEDs or IRQ nesting. Row memory publication is checked; native DMA hardware contract requires separate static and hardware checks.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build-dir','s51','output-dir'): p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    spec=importlib.util.spec_from_file_location('support',Path(__file__).resolve().parents[1]/'ak820_emitted/run.py')
    support=importlib.util.module_from_spec(spec); spec.loader.exec_module(support)
    fw=support.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    result=run(fw,support)
    (fw.output/'direct-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
