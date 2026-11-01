#!/usr/bin/env python3
"""Run real production Auto Shift/action/Quantum code in the shared host fixture."""
import argparse, hashlib, json, os, re, shlex, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
inputs={}
def record(path):
    path=Path(path).resolve()
    if path.is_relative_to(ROOT) and path.is_file():
        name=str(path.relative_to(ROOT)); digest=hashlib.sha256(path.read_bytes()).hexdigest()
        assert name not in inputs or inputs[name]==digest, f'input changed during test: {name}'
        inputs[name]=digest
for path in (Path(__file__), HERE/'host.c', HERE/'combo_boundaries.c', ROOT/'tests/ak820_tapping/harness.c'):
    record(path)
def function(path,name):
    record(ROOT/path)
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
    record(ROOT/path)
    return re.sub(r'^#\s*include[^\n]*\n','',(ROOT/path).read_text(),flags=re.M)
parts=[]
for path in ['tmk_core/protocol/report.c','quantum/action_util.c','quantum/caps_word.c','quantum/process_keycode/process_caps_word.c','quantum/process_keycode/process_grave_esc.c','quantum/send_string/send_string.c','quantum/action_layer.c','quantum/tri_layer.c','quantum/repeat_key.c','quantum/process_keycode/process_repeat_key.c','quantum/process_keycode/process_tri_layer.c','keyboards/ajazz/ak820/ak820_combo.c','keyboards/ajazz/ak820/ak820_tapping.c','keyboards/ajazz/ak820/ak820_oneshot.c']:
    parts.append(re.sub(r'\bkeyboard_report\b','fixture_report_ptr',stripped(path)) if path.endswith('/report.c') else stripped(path))
for path,names in [('quantum/keymap_common.c',['action_for_key','action_for_keycode']),('quantum/quantum.c',['extract_mod_bits','do_code16','register_code16','unregister_code16','get_record_keycode','get_event_keycode','pre_process_record_quantum','process_record_quantum','process_record_quantum_helper','post_process_record_quantum']),('quantum/vial.c',['vial_keycode_event','vial_keycode_down','vial_keycode_up','vial_keycode_tap']),('keyboards/ajazz/ak820/ak820_macro.c',['parse_byte']),('quantum/dynamic_keymap.c',['decode_keycode','dynamic_keymap_macro_send']),('quantum/action.c',['tap_code_delay','tap_code','action_exec','process_record','process_record_handler','process_action','register_code','unregister_code','register_mods','unregister_mods','register_weak_mods','unregister_weak_mods','clear_keyboard','clear_keyboard_but_mods','clear_keyboard_but_mods_and_keys'])]:
    for name in names:parts.append(function(path,name))

parts.append(stripped('keyboards/ajazz/ak820/ak820_autoshift.c'))
# Forward declarations are required before the extracted action functions.
prefix=(ROOT/'tests/ak820_tapping/harness.c').read_text().split('int main(int argc,char **argv) {')[0]
prefix=prefix.replace('#include "ak820_tapping.h"','#include "ak820_tapping.h"\n#include "ak820_autoshift.h"')
prefix=prefix.replace('bool process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r;return true; }',
    'static bool cancel_in_record;\nbool process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r; if(cancel_in_record) {cancel_in_record=false;clear_keyboard();return false;} return true; }')
src=prefix.replace('/* PRODUCTION */','\n'.join(parts))+(HERE/'host.c').read_text()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
with tempfile.TemporaryDirectory(prefix='ak820-autoshift-') as temp:
    work=Path(temp);(work/'protocol').mkdir();(work/'protocol/usb_descriptor.h').write_text('#define SHARED_EPSIZE 32\n');(work/'_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
    (work/'test.c').write_text(src)
    cmd=[os.environ.get('CC','cc'),'-DAK820_COMPACT_AUTOSHIFT','-DAK820_COMPACT_ONESHOT','-DAK820_COMPACT_SPACE_CADET','-std=gnu11','-O1','-g','-ffunction-sections','-fdata-sections','-Wl,--gc-sections','-Wno-implicit-function-declaration','-Wno-unused-function','-Wno-unknown-pragmas','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined','-DMAX_LAYER=6','-DCAPS_WORD_ENABLE','-DGRAVE_ESC_ENABLE','-DVIAL_ENABLE','-DEEPROM_CUSTOM','-DPROTOCOL_CH555','-DNKRO_ENABLE','-DREPEAT_KEY_ENABLE','-DTRI_LAYER_ENABLE','-DENCODER_MAP_ENABLE','-DEXTRAKEY_ENABLE','-DNO_RESET','-include',str(ROOT/'keyboards/ajazz/ak820/config.h'),*['-I'+str(p) for p in [work,ROOT/'keyboards/ajazz/ak820',ROOT/'quantum',ROOT/'quantum/keymap_extras',ROOT/'quantum/sequencer',ROOT/'quantum/send_string',ROOT/'quantum/process_keycode',ROOT/'platforms',ROOT/'tmk_core/protocol',ROOT]],str(work/'test.c'),'-o',str(work/'test')]
    depfile=work/'dependencies.d'
    cmd[1:1]=['-MMD','-MF',str(depfile)]
    def collect_dependencies():
        dependencies=depfile.read_text().replace('\\\n',' ').partition(':')[2]
        for name in shlex.split(dependencies): record(name)
    subprocess.run(cmd,check=True)
    collect_dependencies()
    subprocess.run([str(work/'test')],check=True)
    # Model the two settings-controlled terms in the extracted host translation unit.
    boundary_src = src[:-len((HERE/'host.c').read_text())] + (HERE/'combo_boundaries.c').read_text()
    model_src = boundary_src
    for old, new in (('#    define AK820_COMBO_TERM 40', '#    define AK820_COMBO_TERM TEST_COMBO_TERM'), ('#    define AK820_AUTOSHIFT_TERM 175', '#    define AK820_AUTOSHIFT_TERM TEST_SHIFT_TERM')):
        assert model_src.count(old) == 1, old
        model_src = model_src.replace(old, new)
    # The fixture's settings getters supply controlled values; storage and QSID are not exercised.
    old = 'uint16_t ak820_settings_combo_term(void) {return 40;}'
    assert boundary_src.count(old) == 1
    settings_src = boundary_src.replace(old, 'uint16_t ak820_settings_combo_term(void) {return TEST_COMBO_TERM;}\nuint16_t ak820_settings_autoshift_timeout(void) {return TEST_SHIFT_TERM;}')
    for mode, test_src in (('model', model_src), ('settings getters', settings_src)):
        for opt in (False, True):
            for combo, shift in ((40, 175), (175, 40), (40, 40)):
                (work/'test.c').write_text(test_src)
                flags = [f'-DTEST_COMBO_TERM={combo}', f'-DTEST_SHIFT_TERM={shift}']
                if mode == 'settings getters': flags.append('-DAK820_QMK_SETTINGS')
                if opt: flags.append('-DAK820_COMBO_AUTOSHIFT')
                subprocess.run(cmd[:1] + flags + cmd[1:],check=True)
                collect_dependencies()
                subprocess.run([str(work/'test')],check=True)
                print(f'{mode}: opt-in={opt}, combo={combo}, shift={shift}', flush=True)
    # Dropping cancelled events without source bookkeeping must fail both modes.
    discard = '        ak820_tapping_discard(&event);'
    assert discard in model_src
    for kind in ('pressed', 'released'):
        condition = '!event.pressed' if kind == 'pressed' else 'event.pressed'
        (work/'test.c').write_text(model_src.replace(discard, f'        if ({condition}) ak820_tapping_discard(&event);'))
        for opt in (False, True):
            flags = ['-DTEST_COMBO_TERM=40', '-DTEST_SHIFT_TERM=175']
            if opt: flags.append('-DAK820_COMBO_AUTOSHIFT')
            subprocess.run(cmd[:1] + flags + cmd[1:],check=True)
            assert subprocess.run([str(work/'test')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode != 0, (kind, opt)
    # Removing the release coordinator must expose the swallowed owner release.
    hook = '    if (!ak820_combo_before(&event)) return;'
    assert hook in model_src
    (work/'test.c').write_text(model_src.replace(hook, ''))
    subprocess.run(cmd[:1] + ['-DAK820_COMBO_AUTOSHIFT', '-DTEST_COMBO_TERM=40', '-DTEST_SHIFT_TERM=175'] + cmd[1:],check=True)
    assert subprocess.run([str(work/'test')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode != 0
    (work/'test.c').write_text(src)
    invalid = [arg for arg in cmd if arg != '-DAK820_COMPACT_AUTOSHIFT']
    result = subprocess.run(invalid[:1] + ['-DAK820_COMBO_AUTOSHIFT'] + invalid[1:],capture_output=True,text=True)
    assert result.returncode != 0 and 'AK820_COMBO_AUTOSHIFT requires' in result.stderr
    mutations=[('threshold','>= AK820_AUTOSHIFT_TERM','>= (AK820_AUTOSHIFT_TERM - 1)'),('frozen-release','as_saved.event.pressed = false;','as_saved.keycode = KC_B; as_saved.event.pressed = false;'),('modifier-owner','del_owned_mods(MOD_BIT(KC_LEFT_SHIFT));','/* mutation */'),('cancel','void ak820_autoshift_cancel(void) { as_state = 0; }','void ak820_autoshift_cancel(void) {}'),('category-mask','if (code <= KC_Z ? (as_flags & 16) :','if (code <= KC_Z ? 0 :'),('ru-letters','caps_word_ru && ((key >= KC_LBRC','false && ((key >= KC_LBRC'),('language-cleanup','if (caps_word_ru != (ru != 0)) caps_word_off();','/* mutation */')]
    controls=['cancelled-press-bookkeeping-both-configurations', 'cancelled-release-bookkeeping-both-configurations', 'combo-owner-release', 'missing-autoshift-build-guard']
    for name,old,new in mutations:
        assert old in src,name
        (work/'test.c').write_text(src.replace(old,new))
        subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        result=subprocess.run([str(work/'test')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        assert result.returncode != 0,name
        controls.append(name)
    compiler=subprocess.run([cmd[0], '--version'],check=True,capture_output=True,text=True).stdout.splitlines()[0]
    flags=[arg.replace(str(work),'$WORK').replace(str(ROOT),'$ROOT') for arg in cmd[1:]]
for name, digest in list(inputs.items()):
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, f'input changed during test: {name}'
report={'pass':True,'level':'Host production C with UBSan; hardware hooks stubbed','hardware_validated':False,
        'negative_controls':controls,
        'manifest':{'source_sha256':dict(sorted(inputs.items())), 'compiler':compiler, 'command_arguments':flags,
                    'translation_units_sha256':{name:hashlib.sha256(text.encode()).hexdigest() for name,text in (('host',src),('boundary_model',model_src),('boundary_settings_getters',settings_src))},
                    'boundary_matrix':{'modes':['model','settings getters'], 'combo_autoshift':[False,True], 'terms_ms':[[40,175],[175,40],[40,40]]},
                    'host_configuration':'default without AK820_COMBO_AUTOSHIFT',
                    'negative_controls_configuration':'default except cancelled-event-bookkeeping (both), combo-owner-release (opt-in), and missing-autoshift-build-guard (invalid opt-in)'},
        'production_engine_sha256':inputs['keyboards/ajazz/ak820/ak820_autoshift.c']}
report['manifest_sha256']=hashlib.sha256(json.dumps(report['manifest'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
print(json.dumps(report,indent=2))
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
