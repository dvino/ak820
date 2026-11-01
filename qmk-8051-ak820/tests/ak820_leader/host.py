#!/usr/bin/env python3
"""Run real production Leader/action/Quantum code in the shared host fixture."""
import argparse, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def function(path,name):
    text=(ROOT/path).read_text()
    m=re.search(r'^.*\b'+name+r'\([^\n]*\) \{',text,re.M)
    assert m,name
    start=m.start(); pos=text.index('{',m.start()); depth=1; i=pos+1
    # Function braces inside comments/strings are balanced in these sources.
    while depth:
        if text[i]=='{': depth+=1
        elif text[i]=='}': depth-=1
        i+=1
    return text[start:i]
def stripped(path):
    return re.sub(r'^#\s*include[^\n]*\n','',(ROOT/path).read_text(),flags=re.M)
parts=[]
for path in ['tmk_core/protocol/report.c','quantum/action_util.c','quantum/caps_word.c','quantum/process_keycode/process_caps_word.c','quantum/process_keycode/process_grave_esc.c','quantum/send_string/send_string.c','quantum/action_layer.c','quantum/tri_layer.c','quantum/repeat_key.c','quantum/process_keycode/process_repeat_key.c','quantum/process_keycode/process_tri_layer.c','keyboards/ajazz/ak820/ak820_combo.c','keyboards/ajazz/ak820/ak820_tapping.c','keyboards/ajazz/ak820/ak820_oneshot.c']:
    parts.append(re.sub(r'\bkeyboard_report\b','fixture_report_ptr',stripped(path)) if path.endswith('/report.c') else stripped(path))
for path,names in [('quantum/keymap_common.c',['action_for_key','action_for_keycode']),('quantum/quantum.c',['extract_mod_bits','do_code16','register_code16','unregister_code16','get_record_keycode','get_event_keycode','pre_process_record_quantum','process_record_quantum','process_record_quantum_helper','post_process_record_quantum']),('quantum/vial.c',['vial_keycode_event','vial_keycode_down','vial_keycode_up','vial_keycode_tap']),('keyboards/ajazz/ak820/ak820_macro.c',['parse_byte']),('quantum/dynamic_keymap.c',['decode_keycode','dynamic_keymap_macro_send']),('quantum/action.c',['tap_code_delay','tap_code','action_exec','process_record','process_record_handler','process_action','register_code','unregister_code','register_mods','unregister_mods','register_weak_mods','unregister_weak_mods','clear_keyboard','clear_keyboard_but_mods','clear_keyboard_but_mods_and_keys'])]:
    for name in names:
        if name == 'process_record_quantum_helper':
            parts.append('#ifdef AK820_COMPACT_KEY_OVERRIDE\n' + function('quantum/quantum.c','process_ak820_override') + '\n#endif')
        parts.append(function(path,name))

parts.insert(0, '#ifdef AK820_COMPACT_KEY_OVERRIDE\n' + function('quantum/bitwise.c','biton') + '\n#endif')
parts.append(stripped('keyboards/ajazz/ak820/ak820_autoshift.c'))
parts.append(stripped('keyboards/ajazz/ak820/ak820_dynamic_macro.c'))
parts.append(stripped('keyboards/ajazz/ak820/ak820_leader.c'))
# Forward declarations are required before the extracted action functions.
prefix=(ROOT/'tests/ak820_tapping/harness.c').read_text().split('int main(int argc,char **argv) {')[0]
prefix=prefix.replace('#include "ak820_tapping.h"','#include "ak820_tapping.h"\n#include "ak820_autoshift.h"')
prefix=prefix.replace('bool process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r;return true; }',
    'static bool cancel_in_record;\nbool process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r; if(cancel_in_record) {cancel_in_record=false;clear_keyboard();return false;} return true; }')
prefix=prefix.replace('/* PRODUCTION */','#include "ak820_leader_timeout.h"\n#include "ak820_dynamic_macro.h"\n#include "ak820_leader.h"\n#ifdef AK820_COMPACT_KEY_OVERRIDE\n#include "ak820_key_override.h"\n/* No configured overrides: leave events and reports unchanged. */\nak820_key_override_result_t ak820_key_override_process(keyrecord_t *record, uint8_t mods, uint8_t layer) { (void)record; (void)mods; (void)layer; return true; }\nvoid ak820_key_override_sync(uint8_t mods, uint8_t layer) { (void)mods; (void)layer; }\nvoid ak820_key_override_cancel(void) {}\nuint8_t ak820_key_override_key(void) { return 0; }\nuint8_t ak820_key_override_mods(uint8_t mods) { return mods; }\n#endif\nstatic bool dm_busy;\nbool ak820_keyboard_report_pending(void) { return dm_busy; }\n/* PRODUCTION */')
src=prefix.replace('/* PRODUCTION */','\n'.join(parts))+(HERE/'host.c').read_text()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
with tempfile.TemporaryDirectory(prefix='ak820-dynamic-macro-') as temp:
    work=Path(temp);(work/'protocol').mkdir();(work/'protocol/usb_descriptor.h').write_text('#define SHARED_EPSIZE 32\n');(work/'_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
    (work/'test.c').write_text(src)
    cmd=[os.environ.get('CC','cc'),'-DAK820_COMPACT_LEADER','-DAK820_COMPACT_DYNAMIC_MACRO','-DAK820_COMPACT_AUTOSHIFT','-DAK820_COMPACT_ONESHOT','-DAK820_COMPACT_SPACE_CADET','-std=gnu11','-O1','-g','-ffunction-sections','-fdata-sections','-Wl,--gc-sections','-Wno-implicit-function-declaration','-Wno-unused-function','-Wno-unknown-pragmas','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined','-DMAX_LAYER=6','-DCAPS_WORD_ENABLE','-DGRAVE_ESC_ENABLE','-DVIAL_ENABLE','-DEEPROM_CUSTOM','-DPROTOCOL_CH555','-DNKRO_ENABLE','-DREPEAT_KEY_ENABLE','-DTRI_LAYER_ENABLE','-DENCODER_MAP_ENABLE','-DEXTRAKEY_ENABLE','-DNO_RESET','-include',str(ROOT/'keyboards/ajazz/ak820/config.h'),*['-I'+str(p) for p in [work,ROOT/'keyboards/ajazz/ak820',ROOT/'quantum',ROOT/'quantum/keymap_extras',ROOT/'quantum/sequencer',ROOT/'quantum/send_string',ROOT/'quantum/process_keycode',ROOT/'platforms',ROOT/'tmk_core/protocol',ROOT]],str(work/'test.c'),'-o',str(work/'test')]
    for override in (False, True):
        for opt in (False, True):
            for timeout in (None, 1, 200, 500, 1000):
                flags = [] if timeout is None else [f'-DAK820_LEADER_TIMEOUT={timeout}']
                if opt: flags.append('-DAK820_COMBO_AUTOSHIFT')
                if override: flags.append('-DAK820_COMPACT_KEY_OVERRIDE')
                print(f'override={override} combo_autoshift={opt} timeout={timeout}', flush=True)
                subprocess.run(cmd[:1] + flags + cmd[1:],check=True)
                subprocess.run([str(work/'test')],check=True)
    for timeout in (0, 1001):
        print(f'expected compile rejection: timeout={timeout}', flush=True)
        result = subprocess.run(cmd[:1] + [f'-DAK820_LEADER_TIMEOUT={timeout}'] + cmd[1:], capture_output=True, text=True)
        assert result.returncode and 'Leader timeout must be 1..1000 ms' in result.stderr
report={'pass':True,'level':'Host production C with UBSan; hardware hooks stubbed','hardware_validated':False}

print(json.dumps(report,indent=2))
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
