#!/usr/bin/env python3
"""Offline production compact combo engine traces; no device access."""
from pathlib import Path
import subprocess,tempfile,re
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='ak820-combo-') as d:
    work=Path(d)
    (work/'action.h').write_text('''#pragma once
#include <stdint.h>
#include <stdbool.h>
#define AK820_STATE_MEM
#define MATRIX_ROWS 16
#define MATRIX_COLS 8
#define VIAL_COMBO_ENTRIES 8
#define QK_COMBO_ON 0x7c50
#define QK_COMBO_OFF 0x7c51
#define QK_COMBO_TOGGLE 0x7c52
#define KC_AUDIO_MUTE 0xa8
#define KC_LAUNCHPAD 0xc2
void clear_keyboard(void);
#define QK_MOD_TAP 0x2000
#define QK_CAPS_WORD_TOGGLE 0x7c73
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#define IS_NOEVENT(e) ((e).key.row==255)
typedef struct {uint8_t row,col;} keypos_t;
typedef struct {keypos_t key;bool pressed;uint16_t time;} keyevent_t;
typedef struct {keyevent_t event; struct {uint8_t count;} tap;uint16_t keycode;} keyrecord_t;
void process_record(keyrecord_t *);
''')
    (work/'action_util.h').write_text('')
    (work/'vial.h').write_text('#pragma once\n#include "action.h"\ntypedef struct {uint16_t input[4], output;} vial_combo_entry_t;\n')
    (work/'quantum.h').write_text('#include "action.h"\n')
    (work/'dynamic_keymap.h').write_text('#include "vial.h"\nint dynamic_keymap_get_combo(uint8_t,vial_combo_entry_t *);\n')
    cmd=['cc','-std=c11','-Wall','-Wno-int-to-pointer-cast','-Wextra','-Werror','-fsanitize=undefined','-I'+str(work),'-I'+str(ROOT/'keyboards/ajazz/ak820'),str(ROOT/'keyboards/ajazz/ak820/ak820_combo.c'),str(HERE/'harness.c'),'-o',str(work/'test')]
    subprocess.run(cmd,check=True)
    subprocess.run([str(work/'test')],check=True)

    source=(ROOT/'quantum/dynamic_keymap.c').read_text()
    parts=[source[source.index("/* TD and KO retain"):source.index("#ifdef VIAL_TAP_DANCE_ENABLE\n#ifdef AK820_COMPACT_TAP_DANCE\nint dynamic_keymap_get_tap_dance")]]
    for name in ['dynamic_keymap_get_combo','dynamic_keymap_set_combo']:
        m=re.search(r'^int '+name+r'\([^\n]*\) \{',source,re.M)
        i=source.index('{',m.start())+1; depth=1
        while depth:
            if source[i]=='{': depth+=1
            elif source[i]=='}': depth-=1
            i+=1
        parts.append(source[m.start():i])
    (work/'storage.c').write_text((HERE/'storage.c').read_text().replace('/* PRODUCTION */','\n'.join(parts)))
    cmd[-3]=str(work/'storage.c')
    cmd[-1]=str(work/'storage')
    subprocess.run(cmd,check=True)
    subprocess.run([str(work/'storage')],check=True)
