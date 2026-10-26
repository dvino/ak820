#!/usr/bin/env python3
"""Offline host traces using production tap engine, decoder, action/cache and owners."""
import differential
import argparse,hashlib,json,os,re,subprocess,tempfile
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
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--oneshot',action='store_true')
parser.add_argument('--space-cadet',action='store_true')
parser.add_argument('--negative-controls',action='store_true')
args=parser.parse_args()
inputs=[ROOT/p for p in ['quantum/action.c','quantum/action.h','quantum/action_layer.c','quantum/action_util.c','quantum/dynamic_keymap.c','quantum/vial.c','quantum/send_string/send_string.c','keyboards/ajazz/ak820/ak820_macro.c','quantum/keymap_common.c','quantum/quantum.c','quantum/repeat_key.c','quantum/tri_layer.c','quantum/process_keycode/process_repeat_key.c','quantum/process_keycode/process_tri_layer.c','keyboards/ajazz/ak820/ak820_combo.c','keyboards/ajazz/ak820/ak820_tapping.c','keyboards/ajazz/ak820/ak820_oneshot.c','keyboards/ajazz/ak820/config.h']]+[HERE/'run.py',HERE/'harness.c',HERE/'differential.py',HERE/'oracle.py',HERE/'oracle_harness.c',ROOT/'quantum/action_tapping.c',ROOT/'tmk_core/protocol/report.c',ROOT/'quantum/action_util.h',ROOT/'quantum/action_layer.h',ROOT/'quantum/tri_layer.h',ROOT/'quantum/process_keycode/process_tri_layer.h',ROOT/'keyboards/ajazz/ak820/ak820_tapping.h',ROOT/'quantum/caps_word.c',ROOT/'quantum/process_keycode/process_caps_word.c',ROOT/'quantum/process_keycode/process_grave_esc.c',ROOT/'quantum/process_keycode/process_grave_esc.h']
# Bind the production headers included directly by the combined fixture too.
for header in ['tmk_core/protocol/report.h','quantum/quantum_keycodes.h',
               'quantum/keymap_common.h',
               'quantum/keycode_config.h','tmk_core/protocol/host.h',
               'quantum/repeat_key.h','quantum/process_keycode/process_repeat_key.h',
               'quantum/qmk_settings.h','quantum/caps_word.h',
               'quantum/process_keycode/process_caps_word.h','platforms/timer.h',
               'quantum/send_string/send_string.h']:
    path=ROOT/header
    if path not in inputs:
        inputs.append(path)
source_snapshot={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
parts=[]
for path in ['tmk_core/protocol/report.c','quantum/action_util.c','quantum/caps_word.c','quantum/process_keycode/process_caps_word.c','quantum/process_keycode/process_grave_esc.c','quantum/send_string/send_string.c','quantum/action_layer.c','quantum/tri_layer.c','quantum/repeat_key.c','quantum/process_keycode/process_repeat_key.c','quantum/process_keycode/process_tri_layer.c','keyboards/ajazz/ak820/ak820_combo.c','keyboards/ajazz/ak820/ak820_tapping.c','keyboards/ajazz/ak820/ak820_oneshot.c']:
    parts.append(re.sub(r'\bkeyboard_report\b','fixture_report_ptr',stripped(path)) if path.endswith('/report.c') else stripped(path))
for path,names in [('quantum/keymap_common.c',['action_for_key','action_for_keycode']),('quantum/quantum.c',['extract_mod_bits','do_code16','register_code16','unregister_code16','get_record_keycode','get_event_keycode','pre_process_record_quantum','process_record_quantum','process_record_quantum_helper','post_process_record_quantum']),('quantum/vial.c',['vial_keycode_event','vial_keycode_down','vial_keycode_up','vial_keycode_tap']),('keyboards/ajazz/ak820/ak820_macro.c',['parse_byte']),('quantum/dynamic_keymap.c',['decode_keycode','dynamic_keymap_macro_send']),('quantum/action.c',['tap_code_delay','tap_code','action_exec','process_record','process_record_handler','process_action','register_code','unregister_code','register_mods','unregister_mods','register_weak_mods','unregister_weak_mods','clear_keyboard','clear_keyboard_but_mods','clear_keyboard_but_mods_and_keys'])]:
    for name in names:parts.append(function(path,name))
with tempfile.TemporaryDirectory(prefix='ak820-tapping-') as temp:
    work=Path(temp);(work/'protocol').mkdir();(work/'protocol/usb_descriptor.h').write_text('#define SHARED_EPSIZE 32\n');(work/'_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
    src=(HERE/'harness.c').read_text().replace('/* PRODUCTION */','\n'.join(parts));(work/'test.c').write_text(src)
    cmd=[os.environ.get('CC','cc'),'-std=gnu11','-O1','-g','-ffunction-sections','-fdata-sections','-Wl,--gc-sections','-Wno-implicit-function-declaration','-Wno-unused-function','-Wno-unknown-pragmas','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined','-DMAX_LAYER=6','-DCAPS_WORD_ENABLE','-DGRAVE_ESC_ENABLE','-DVIAL_ENABLE','-DEEPROM_CUSTOM','-DPROTOCOL_CH555','-DNKRO_ENABLE','-DREPEAT_KEY_ENABLE','-DTRI_LAYER_ENABLE','-DENCODER_MAP_ENABLE','-DEXTRAKEY_ENABLE','-DNO_RESET','-include',str(ROOT/'keyboards/ajazz/ak820/config.h'),*['-I'+str(p) for p in [work,ROOT/'keyboards/ajazz/ak820',ROOT/'quantum',ROOT/'quantum/keymap_extras',ROOT/'quantum/sequencer',ROOT/'quantum/send_string',ROOT/'quantum/process_keycode',ROOT/'platforms',ROOT/'tmk_core/protocol',ROOT]],str(work/'test.c'),'-o',str(work/'test')]
    if args.oneshot: cmd.insert(1,'-DAK820_COMPACT_ONESHOT')
    if args.space_cadet: cmd.insert(1,'-DAK820_COMPACT_SPACE_CADET')
    subprocess.run(cmd,check=True);subprocess.run([str(work/'test')],check=True)
    comparison=differential.check(work/'test',work)
    controls=[]
    if args.negative_controls:
        negative_control_specs=[
            ('grave-raw-owner','register_code(shifted ? KC_GRAVE : KC_ESCAPE);','add_key(shifted ? KC_GRAVE : KC_ESCAPE);'),
            ('grave-physical-cache','if (get_repeat_key_count()) {','if (record->keycode) {'),
            ('caps-cleanup-consumes-owner','del_weak_mods(MOD_MASK_SHIFT);\n    send_keyboard_report();','unregister_weak_mods(MOD_MASK_SHIFT);'),
            ('stale-derived-mask','tri_layer_changed();','ak820_layer_refresh();'),
            ('cancel-blocks-released-source','((state & SOURCE_ACTIVE) << 1)','((state & (SOURCE_ACTIVE | SOURCE_HELD)) ? SOURCE_BLOCKED : 0)'),
            ('macro-counter-wrap','ak820_macro_primitive = data[1] != SS_TAP_CODE;','ak820_macro_primitive = false;'),
            ('macro-tap-consumes-down','ak820_macro_primitive = data[1] != SS_TAP_CODE;','ak820_macro_primitive = true;'),
            ('early-hold','event->time - pending_time) >= AK820_TAPPING_TERM','event->time - pending_time) >= (AK820_TAPPING_TERM - 1)'),
            ('wrong-right-group','if (mods & 16) mods <<= 4;','if (mods & 16) mods &= 15;'),
            ('lost-release','if (event->pressed == ((source_state_get(id) & SOURCE_ACTIVE) != 0)) return false;','if (!event->pressed || event->pressed == ((source_state_get(id) & SOURCE_ACTIVE) != 0)) return false;'),
            ('premature-lookup','if (!ak820_tapping_before(&event)) return;','if (IS_EVENT(event) && event.pressed) update_source_layers_cache(event.key,layer_switch_get_layer(event.key));\n    if (!ak820_tapping_before(&event)) return;')]
        if args.space_cadet:
            negative_control_specs += [
                ('space-cadet-final-modifier-release-report','del_owned_mods(sc_mods);\n            send_keyboard_report();','del_owned_mods(sc_mods);'),
                ('space-cadet-held-modifier-report','if (pressed) register_mods(mods);','if (pressed) add_owned_mods(mods);')]
        for name,old,new in negative_control_specs:
            if name=='premature-lookup':
                mutated=src.replace(old,new).replace('uint16_t keycode = get_record_keycode(record, true);','uint16_t keycode = get_record_keycode(record, false);')
            else:
                assert old in src,name
                mutated=src.replace(old,new)
            (work/'test.c').write_text(mutated)
            subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            result=subprocess.run([str(work/'test')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            assert result.returncode != 0,name+' did not fail'
            controls.append({'name':name,'rejected':True})
    assert {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs} == source_snapshot, "Source changed during the host run; rerun against a stable snapshot"

    report={'pass':True,'fixture_config':{'NO_RESET':True,'ee_clear_limit':'Host clear branch only; production EEPROM-disable/reset path is not executed'},'level':'Host C/UBSan, production function bodies with hardware/user hooks stubbed','hardware_validated':False,'coverage':{'mt_masks':32,'lt_layers':6,'accepted_tap_bytes':201,'extra_same_namespace_pairs':738,'utility_extra_mask_release_cases':1920,'report_modes':['6KRO','NKRO'],'tri_layer_mutable_target_sources':['matrix','encoder_cw','encoder_ccw','macro_role'],'caps_word':['raw_cleanup_preserves_encoded_repeat_macro_weak_owners','idle_cleanup','MT_shift_hold_keeps_mode','MT_ctrl_next_key_ends_mode','LT_hold_and_resolved_layer_tap','MT_LT_capitalized_taps'],'macro_interpreter':{'stream_bytes':8192,'max_duplicate_basic_downs_per_stream':2725,'max_duplicate_extended_downs_per_stream':2044,'repeated_stream_execution':True,'unmatched_up':True,'tap_ascii_transient_owners':True,'all_encoded_modifier_masks':True,'generated_mt_lt_low_byte':True,'cancel_aborts_before_later_output':True}},'combos':{'configured':True,'report_modes':['6KRO','NKRO'],'cases':['both_release_orders','shared_output_owner','repeat_learning_replay','modified_output_physical_ctrl','caps_word','cancel_pending_active','mt_interruption','lt_lookup_ordering']},'negative_controls':controls,'qmk_comparison':comparison,'source_sha256':source_snapshot,'limits':'No linked 8051 ABI or physical timing/USB/NVM proof. QMK comparisons use eligible short traces and a boundary output adapter; ownership and immediate release intentionally differ.'}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
