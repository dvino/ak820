#!/usr/bin/env python3
"""Offline C model of the compact engine; no device or firmware build."""
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'qmk-8051-ak820/keyboards/ajazz/ak820/ak820_key_override.c'
HEADER = '''#pragma once
#include <stdbool.h>
#include <stdint.h>
#define AK820_STATE_MEM
#define VIAL_KEY_OVERRIDE_ENTRIES 8
#define MATRIX_ROWS 6
#define MATRIX_COLS 16
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#define QK_MOD_TAP 0x2000
#define QK_KEY_OVERRIDE_TOGGLE 0x7c5d
#define QK_KEY_OVERRIDE_ON 0x7c5e
#define QK_KEY_OVERRIDE_OFF 0x7c5f
#define QK_MODS_GET_MODS(k) (((k)>>8)&31)
typedef struct { struct { struct { uint8_t row,col; } key; bool pressed; } event; uint16_t keycode; } keyrecord_t;
typedef struct { uint16_t trigger,replacement,layers; uint8_t trigger_mods,negative_mod_mask,suppressed_mods,options; } vial_key_override_entry_t;
'''
TEST = r'''
#include <assert.h>
#include <string.h>
static vial_key_override_entry_t store[8];
int dynamic_keymap_get_key_override(uint8_t i, vial_key_override_entry_t *e) { *e=store[i]; return 0; }
#include "ENGINE"
static bool event(uint8_t col,uint16_t key,bool down,uint8_t mods) {
    keyrecord_t r={0}; r.event.key.col=col;r.event.pressed=down;r.keycode=key;
    return ak820_key_override_process(&r,mods,0);
}
static void setup(uint8_t opts) {
    memset(store,0,sizeof(store));
    store[0]=(vial_key_override_entry_t){4,0x0205,63,1,4,1,opts|128};
    assert(ak820_key_override_valid(&store[0]));ak820_key_override_reload();
}
static bool reference_valid(const vial_key_override_entry_t *e) {
    if (!(e->trigger | e->replacement | e->layers | e->trigger_mods |
          e->negative_mod_mask | e->suppressed_mods | e->options)) return true;
    if (e->trigger < 4 || e->trigger > 164 || !e->layers || (e->layers & ~63u)) return false;
    if ((e->options & 64) || !(e->options & 7)) return false;
    return !e->replacement || (e->replacement < 0x2000 &&
           (uint8_t)e->replacement >= 4 && (uint8_t)e->replacement <= 164);
}
int main(void) {
    vial_key_override_entry_t probe={4,5,63,1,0,0,135};
    /* Exhaust each wide field and every option byte against the original
       semantic predicate, including invalid high bytes and disabled rows. */
    for (uint32_t v=0;v<65536;++v) {
        probe.trigger=v;assert(ak820_key_override_valid(&probe)==reference_valid(&probe));probe.trigger=4;
        probe.replacement=v;assert(ak820_key_override_valid(&probe)==reference_valid(&probe));probe.replacement=5;
        probe.layers=v;assert(ak820_key_override_valid(&probe)==reference_valid(&probe));probe.layers=63;
    }
    for (unsigned v=0;v<256;++v) {probe.options=v;assert(ak820_key_override_valid(&probe)==reference_valid(&probe));}
    /* Full-width non-basic keycodes sharing a trigger's low byte pass
       through; only the validator's byte predicate may truncate. */
    setup(7);assert(event(0,0x0104,true,1));assert(!ak820_key_override_key());
    assert(event(0,0x0104,false,1));assert(!ak820_key_override_key());
    setup(7);assert(!event(0,4,true,1));assert(ak820_key_override_key()==5);
    assert(ak820_key_override_mods(1|8)==(2|8));
    /* A physical/macro owner of replacement usage remains in its own report
       set when this owner's overlay disappears. No engine function mutates it. */
    uint8_t other_key=5,physical_mods=1,macro_mods=8;
    assert(!event(0,4,false,1));assert(!ak820_key_override_key());
    assert(other_key==5 && physical_mods==1 && macro_mods==8);
    setup(7);assert(!event(0,4,true,0));assert(ak820_key_override_key()==4);
    ak820_key_override_sync(1,0);assert(ak820_key_override_key()==5);
    ak820_key_override_sync(0,0);assert(ak820_key_override_key()==4);
    ak820_key_override_cancel();assert(!ak820_key_override_key());
    setup(7);assert(!event(0,4,true,5));assert(ak820_key_override_key()==4);
    ak820_key_override_sync(1,0);assert(ak820_key_override_key()==5);
    /* Unrelated modifier transitions cannot activate a required-mod-up row. */
    setup(4);assert(!event(0,4,true,1));ak820_key_override_sync(9,0);
    ak820_key_override_sync(1,0);assert(ak820_key_override_key()==4);
    /* A required modifier rising while an unrelated modifier falls cannot
       activate a row that enables only forbidden-modifier-release. */
    setup(4);event(0,4,true,8);ak820_key_override_sync(1,0);
    assert(ak820_key_override_key()==4);
    setup(7|16);event(0,4,true,1);ak820_key_override_sync(0,0);assert(!ak820_key_override_key());
    setup(7);event(0,4,true,1);assert(event(1,6,true,1));assert(ak820_key_override_key()==4);
    setup(7|32);event(0,4,true,1);assert(event(1,6,true,1));assert(ak820_key_override_key()==5);
    event(2,QK_KEY_OVERRIDE_OFF,true,1);assert(!ak820_key_override_enabled());assert(ak820_key_override_key()==4);
    event(0,4,false,1);event(2,QK_KEY_OVERRIDE_ON,true,1);assert(ak820_key_override_enabled());
    /* Compact One Shot owns its modifier until the captured physical source
       releases; passing that aggregate must leave the owner state intact. */
    setup(7);uint8_t oneshot_owner=1;event(0,4,true,oneshot_owner);
    ak820_key_override_sync(oneshot_owner,0);assert(ak820_key_override_key()==5);
    assert(ak820_key_override_mods(oneshot_owner|8)==10 && oneshot_owner==1);
    event(0,4,false,oneshot_owner);oneshot_owner=0;
    assert(ak820_key_override_mods(8)==8);
    setup(7);store[0].layers=64;assert(!ak820_key_override_valid(&store[0]));
    store[0].layers=63;store[0].replacement=0x5000;assert(!ak820_key_override_valid(&store[0]));
    memset(&store[0],0,sizeof(store[0]));assert(ak820_key_override_valid(&store[0]));
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-key-override-') as folder:
    d=Path(folder)
    for name in ('quantum.h','action.h','action_util.h','vial.h'):
        (d/name).write_text('#include "stub.h"\n')
    (d/'stub.h').write_text(HEADER)
    (d/'dynamic_keymap.h').write_text('#include "stub.h"\nint dynamic_keymap_get_key_override(uint8_t,vial_key_override_entry_t*);\n')
    (d/'test.c').write_text('#include "stub.h"\n'+TEST.replace('ENGINE',str(SOURCE)))
    subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-I',str(d),str(d/'test.c'),'-o',str(d/'test')],check=True)
    subprocess.run([str(d/'test')],check=True)
print('PASS compact Key Overrides host engine model')
