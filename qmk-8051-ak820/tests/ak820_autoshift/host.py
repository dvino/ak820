#!/usr/bin/env python3
"""Run real production Auto Shift/action/Quantum code in the shared host fixture."""
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
for path,names in [('quantum/keymap_common.c',['action_for_key','action_for_keycode']),('quantum/quantum.c',['extract_mod_bits','do_code16','register_code16','unregister_code16','get_record_keycode','get_event_keycode','pre_process_record_quantum','process_record_quantum','process_record_quantum_helper','post_process_record_quantum']),('quantum/vial.c',['vial_keycode_down','vial_keycode_up','vial_keycode_tap']),('keyboards/ajazz/ak820/ak820_macro.c',['parse_byte']),('quantum/dynamic_keymap.c',['decode_keycode','dynamic_keymap_macro_send']),('quantum/action.c',['tap_code_delay','tap_code','action_exec','process_record','process_record_handler','process_action','register_code','unregister_code','register_mods','unregister_mods','register_weak_mods','unregister_weak_mods','clear_keyboard','clear_keyboard_but_mods','clear_keyboard_but_mods_and_keys'])]:
    for name in names:parts.append(function(path,name))

parts.append(stripped('keyboards/ajazz/ak820/ak820_autoshift.c'))
# Forward declarations are required before the extracted action functions.
prefix=(ROOT/'tests/ak820_tapping/harness.c').read_text().split('int main(int argc,char **argv) {')[0]
prefix=prefix.replace('#include "ak820_tapping.h"','#include "ak820_tapping.h"\n#include "ak820_autoshift.h"')
src=prefix.replace('/* PRODUCTION */','\n'.join(parts))+(HERE/'host.c').read_text()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
with tempfile.TemporaryDirectory(prefix='ak820-autoshift-') as temp:
    work=Path(temp);(work/'protocol').mkdir();(work/'protocol/usb_descriptor.h').write_text('#define SHARED_EPSIZE 32\n');(work/'_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
    (work/'test.c').write_text(src)
    cmd=[os.environ.get('CC','cc'),'-DAK820_COMPACT_AUTOSHIFT','-DAK820_COMPACT_ONESHOT','-DAK820_COMPACT_SPACE_CADET','-std=gnu11','-O1','-g','-ffunction-sections','-fdata-sections','-Wl,--gc-sections','-Wno-implicit-function-declaration','-Wno-unused-function','-Wno-unknown-pragmas','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined','-DMAX_LAYER=6','-DCAPS_WORD_ENABLE','-DGRAVE_ESC_ENABLE','-DVIAL_ENABLE','-DEEPROM_CUSTOM','-DPROTOCOL_CH555','-DNKRO_ENABLE','-DREPEAT_KEY_ENABLE','-DTRI_LAYER_ENABLE','-DENCODER_MAP_ENABLE','-DEXTRAKEY_ENABLE','-DNO_RESET','-include',str(ROOT/'keyboards/ajazz/ak820/config.h'),*['-I'+str(p) for p in [work,ROOT/'keyboards/ajazz/ak820',ROOT/'quantum',ROOT/'quantum/keymap_extras',ROOT/'quantum/sequencer',ROOT/'quantum/send_string',ROOT/'quantum/process_keycode',ROOT/'platforms',ROOT/'tmk_core/protocol',ROOT]],str(work/'test.c'),'-o',str(work/'test')]
    subprocess.run(cmd,check=True)
    subprocess.run([str(work/'test')],check=True)
    mutations=[('threshold','>= 175','>= 174'),('frozen-release','as_saved.event.pressed = false;','as_saved.keycode = KC_B; as_saved.event.pressed = false;'),('modifier-owner','del_owned_mods(MOD_BIT(KC_LEFT_SHIFT));','/* mutation */'),('cancel','void ak820_autoshift_cancel(void) { as_state = 0; }','void ak820_autoshift_cancel(void) {}')]
    controls=[]
    for name,old,new in mutations:
        assert old in src,name
        (work/'test.c').write_text(src.replace(old,new))
        subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        result=subprocess.run([str(work/'test')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        assert result.returncode != 0,name
        controls.append(name)
report={'pass':True,'level':'Host production C with UBSan; hardware hooks stubbed','hardware_validated':False,'negative_controls':controls,'production_engine_sha256':hashlib.sha256((ROOT/'keyboards/ajazz/ak820/ak820_autoshift.c').read_bytes()).hexdigest()}
print(json.dumps(report,indent=2))
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
