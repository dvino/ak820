#!/usr/bin/env python3
"""Exhaust the 16-bit keycode ABI on the host and in the actual linked 8051 image.

The only intentional action-decoder difference from RC4 is the independently
specified LM right-modifier fix. CPU scratch RAM/ROM is simulator-only.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAMES = ('extract_mod_bits', 'do_code16', 'register_code16', 'unregister_code16')

def function(path, name):
    text = path.read_text()
    match = re.search(r'^.*\b' + name + r'\([^\n]*\) \{', text, re.M)
    if not match:
        raise ValueError(f'Missing production function {name}')
    return text[match.start():text.index('\n}', match.end()) + 2]

PREFIX = r"""
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "action_layer.h"
#include "quantum_keycodes.h"
#include "report.h"
uint16_t keycode_config(uint16_t keycode) { return keycode; }
uint8_t mod_config(uint8_t mods) { return mods; }
typedef struct { uint8_t type, value; } event_t;
static event_t events[8];
static unsigned count;
static void emit(uint8_t type, uint8_t value) {
    assert(count < 8); events[count++] = (event_t){type,value};
}
void register_code(uint8_t x) { emit(1,x); }
void unregister_code(uint8_t x) { emit(2,x); }
void register_mods(uint8_t x) { emit(3,x); }
void unregister_mods(uint8_t x) { emit(4,x); }
void register_weak_mods(uint8_t x) { emit(5,x); }
void unregister_weak_mods(uint8_t x) { emit(6,x); }
"""
ORACLE = r"""
static uint16_t expected_action(uint16_t keycode) {
    if (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) {
        /* Independent 16-layer x 32-encoded-modifier contract: the marker
         * chooses a HID nibble; it must never become part of the layer. */
        uint8_t layer = (keycode >> 5) & 15;
        uint8_t mods = keycode & 31;
        uint8_t hid = (mods & 16) ? ((mods & 15) << 4) : mods;
        return 0x9000 | ((uint16_t)layer << 8) | hid;
    }
    return rc4_action_for_keycode(keycode);
}
int main(void) {
    unsigned changed = 0;
    event_t actual[8]; unsigned actual_count;
    for (uint32_t code = 0; code <= UINT16_MAX; ++code) {
        uint16_t expected = expected_action(code);
        changed += expected != rc4_action_for_keycode(code);
        assert(action_for_keycode(code) == expected);
        assert(extract_mod_bits(code) == rc4_extract_mod_bits(code));
        count=0; register_code16(code);
        actual_count=count; memcpy(actual,events,sizeof(events));
        count=0; rc4_register_code16(code);
        assert(count==actual_count && !memcmp(actual,events,count*sizeof(event_t)));
        count=0; unregister_code16(code);
        actual_count=count; memcpy(actual,events,sizeof(events));
        count=0; rc4_unregister_code16(code);
        assert(count==actual_count && !memcmp(actual,events,count*sizeof(event_t)));
        /* Binary golden table for the CPU comparison: action LE16, mods U8. */
        putchar(expected & 255); putchar(expected >> 8); putchar(rc4_extract_mod_bits(code));
    }
    assert(changed == 128);
    return 0;
}
"""

def trampoline(high, target, width):
    # Counter 0x2f00 and output table 0x3000 are outside firmware RAM.
    code = [0x90,0x2f,0,0xe4,0xf0]
    loop = len(code)
    code += [0x90,0x2f,0,0xe0,0xf5,0x82,0x75,0x83,high,
             0x12,target >> 8,target & 255,0xae,0x82,0xaf,0x83,
             0x90,0x2f,0,0xe0]
    if width == 2:
        code += [0x25,0xe0,0xf5,0x82,0xe4,0x34,0x30,0xf5,0x83]
    else:
        code += [0xf5,0x82,0x75,0x83,0x30]
    code += [0xee,0xf0]  # Low result R6 -> MOVX output.
    if width == 2:
        code += [0xa3,0xef,0xf0]  # High result R7.
    code += [0x90,0x2f,0,0xe0,0x04,0xf0,0x70,0]
    relative = loop - len(code)
    assert -128 <= relative < 128
    code[-1] = relative & 255
    return code + [0x02,0x27,0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path,default=ROOT)
    parser.add_argument('--build-dir',type=Path)
    parser.add_argument('--s51',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    root,output=args.source_root.resolve(),args.output_dir.resolve()
    output.mkdir(parents=True,exist_ok=True)
    if bool(args.build_dir) != bool(args.s51):
        parser.error('--build-dir and --s51 are required together')
    inputs=[root/'quantum/quantum.c',root/'quantum/keymap_common.c',
            root/'tmk_core/protocol/report.c',root/'keyboards/ajazz/ak820/config.h',
            HERE/'code16_rc4.c',HERE.parent/'ak820_optimization/fixtures/keycode_decoder_rc4.c',Path(__file__)]
    source=PREFIX+'\n'+function(inputs[2],'KEYCODE2CONSUMER')+'\n'
    source+='\n'.join(function(inputs[0],name) for name in NAMES)+'\n'
    source+=function(inputs[1],'action_for_keycode')+'\n'+inputs[4].read_text()+'\n'+inputs[5].read_text()+ORACLE
    with tempfile.TemporaryDirectory(prefix='ak820-keycode-') as temporary:
        directory=Path(temporary); c=directory/'oracle.c'; binary=directory/'oracle'
        c.write_text(source)
        (directory/'_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
        command=[os.environ.get('CC','cc'),'-std=gnu11','-O2','-g','-Wall','-Wextra','-Werror',
                 '-Wno-unused-parameter','-Wno-old-style-declaration','-Wno-unknown-pragmas',
                 '-fsanitize=address,undefined','-fno-omit-frame-pointer','-DEXTRAKEY_ENABLE',
                 '-include',str(inputs[3]),*[ '-I'+str(p) for p in
                 (directory,root/'quantum',root/'quantum/keymap_extras',root/'quantum/sequencer',
                  root/'quantum/send_string',root/'platforms',root/'tmk_core/protocol',root)],str(c),'-o',str(binary)]
        subprocess.run(command,check=True)
        env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
        golden=subprocess.check_output([str(binary)],env=env)
    assert len(golden)==65536*3
    report={'pass':True,'hardware_validated':False,
            'host':{'pass':True,'keycodes':65536,'unchanged_actions':65408,'corrected_right_lm_actions':128,
                    'modifier_extractions':65536,'register_unregister_traces':131072},
            'source_sha256':{str(p.relative_to(root) if p.is_relative_to(root) else p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
            'golden_table_sha256':hashlib.sha256(golden).hexdigest()}
    if args.build_dir:
        spec=importlib.util.spec_from_file_location('ak820_emitted',HERE.parent/'ak820_emitted/run.py')
        emitted=importlib.util.module_from_spec(spec);spec.loader.exec_module(emitted)
        fw=emitted.Firmware(args.build_dir.resolve(),args.s51.resolve(),output)
        report['linked_image_sha256']=hashlib.sha256(fw.image.read_bytes()).hexdigest()
        report['cpu']=[]
        for symbol,width,offset in [('_action_for_keycode',2,0),('_extract_mod_bits',1,2)]:
            target=fw.address(symbol)
            commands=[f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"]
            for high in range(256):
                commands += [emitted.memory('rom',0x2000,trampoline(high,target,width)),'run 0x2000 0x2700']
                commands += fw.dump(f'result_{high:03d}@','xram',0x3000,width*256)
            log,stack=fw.execute(symbol[1:]+'-all-inputs',commands)
            for high in range(256):
                actual=bytes(fw.extract(log,f'result_{high:03d}@',0x3000,width*256))
                expected=b''.join(golden[3*((high<<8)|low)+offset:3*((high<<8)|low)+offset+width] for low in range(256))
                if actual != expected:
                    bad=next(i for i in range(len(actual)) if actual[i]!=expected[i])
                    raise AssertionError(f'{symbol} differs for keycode {((high<<8)|(bad//width)):04x}: {actual[bad]} != {expected[bad]}')
            report['cpu'].append({'name':symbol,'pass':True,'cases':65536,**stack})
    report['limits']='Host semantics and linked generic C52 instructions; no physical USB, flash, IRQ timing or global stack bound.'
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
