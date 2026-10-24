#!/usr/bin/env python3
"""Differential check of volatile Ctrl/GUI report swapping."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / 'quantum/action_util.c').read_text()
def function(name):
    begin = text.index(name)
    end = text.index('\n}\n', begin) + 3
    return text[begin:end]

source = r'''
#include <stdbool.h>
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#define AK820_COMPACT_GUI_LOCK
#define AK820_COMPACT_CTRL_GUI_SWAP
#define AK820_COMPACT_TAPPING
#define AK820_BOARD
#define NO_ACTION_ONESHOT
#define QK_MAGIC_GUI_ON 0x7009
#define QK_MAGIC_GUI_OFF 0x700a
#define QK_MAGIC_TOGGLE_GUI 0x700b
#define QK_MAGIC_SWAP_CTL_GUI 0x701b
#define QK_MAGIC_UNSWAP_CTL_GUI 0x701c
#define QK_MAGIC_TOGGLE_CTL_GUI 0x701d
#define KC_LGUI 0xe3
#define KC_RGUI 0xe7
#define MOD_BIT(k) (1u << ((k) & 7))
typedef struct { uint8_t mods, reserved, keys[6]; } report_keyboard_t;
static report_keyboard_t actual_keyboard_report, sent;
#define keyboard_report (&actual_keyboard_report)
static uint8_t real_mods, weak_mods, owned_mods, owned_weak_mods, oneshot_mods;
static bool gui_disabled, ctrl_gui_swapped;
static unsigned sends;
void host_keyboard_send(report_keyboard_t *report) { sent = *report; ++sends; }
void send_keyboard_report(void);
''' + function('bool ak820_gui_process(') + function('void send_keyboard_report(') + r'''
static uint8_t oracle(uint8_t m) {
    uint8_t out=m & (uint8_t)~0x99;
    if (m&0x01) out|=0x08;
    if (m&0x08) out|=0x01;
    if (m&0x10) out|=0x80;
    if (m&0x80) out|=0x10;
    return out;
}
int main(void) {
    /* Exact supported controls only: exhaustive domain, states and edges. */
    for (uint32_t code=0; code<=65535; ++code) for (unsigned state=0;state<2;++state)
      for (unsigned press=0;press<2;++press) {
        ctrl_gui_swapped=state; gui_disabled=false; unsigned n=sends;
        bool pass=ak820_gui_process(code,press);
        bool ctl=code==0x701b||code==0x701c||code==0x701d||
                 (code>=0x7009&&code<=0x700b);
        assert(pass==!ctl);
        bool expected=state;
        if (code==0x701b&&press) expected=true;
        if (code==0x701c&&press) expected=false;
        if (code==0x701d&&press) expected=!state;
        assert(ctrl_gui_swapped==expected);
        if (!ctl||!press) assert(sends==n);
    }
    /* All 256 effective bitsets, assembled across owner classes, both
       transformations, and GUI lock after the transform. Owners stay raw. */
    for (unsigned m=0;m<256;++m) for (unsigned split=0;split<16;++split)
      for (unsigned swap=0;swap<2;++swap) for (unsigned lock=0;lock<2;++lock) {
        real_mods=(split==0||split&1)?m:0; weak_mods=(split&2)?m:0;
        owned_mods=(split&4)?m:0; owned_weak_mods=(split&8)?m:0;
        oneshot_mods=0; ctrl_gui_swapped=swap; gui_disabled=lock;
        uint8_t want=swap?oracle(m):m; if(lock) want &= (uint8_t)~0x88;
        send_keyboard_report(); if(actual_keyboard_report.mods!=want) { fprintf(stderr,"m=%u split=%u swap=%u lock=%u got=%u want=%u\\n",m,split,swap,lock,actual_keyboard_report.mods,want); return 2; }
        assert((real_mods|weak_mods|owned_mods|owned_weak_mods)==m);
      }
    /* Set, reset and toggle while a physical Ctrl owner is held. Up edges
       never change a mode; every down edge publishes the current mapping. */
    real_mods=1; weak_mods=owned_mods=owned_weak_mods=oneshot_mods=0;
    ctrl_gui_swapped=false; gui_disabled=false;
    ak820_gui_process(0x701b,true); assert(ctrl_gui_swapped && sent.mods==8);
    ak820_gui_process(0x701c,false); assert(ctrl_gui_swapped && sent.mods==8);
    ak820_gui_process(0x701d,false); assert(ctrl_gui_swapped && sent.mods==8);
    ak820_gui_process(0x701d,true); assert(!ctrl_gui_swapped && sent.mods==1);
    ak820_gui_process(0x701d,true); assert(ctrl_gui_swapped && sent.mods==8);
    ak820_gui_process(0x701c,true); assert(!ctrl_gui_swapped && sent.mods==1);
    /* Mixed owners and immediate mode changes while held; each up edge leaves
       only the surviving owner, including a GUI lock applied after swap. */
    real_mods=0x11; weak_mods=0x08; owned_mods=0x80; owned_weak_mods=0x04;
    ctrl_gui_swapped=false; gui_disabled=false;
    ak820_gui_process(0x701b,true); assert(sent.mods==0x9d);
    assert(real_mods==0x11 && weak_mods==8 && owned_mods==0x80 && owned_weak_mods==4);
    ak820_gui_process(0x701b,false); assert(sent.mods==0x9d);
    ak820_gui_process(0x700a,true); assert(sent.mods==(uint8_t)(oracle(0x9d)&~0x88));
    ak820_gui_process(0x701c,true); assert(sent.mods==(uint8_t)(0x9d&~0x88));
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-ctrl-gui-host-') as directory:
    p=Path(directory); (p/'test.c').write_text(source)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined',
                    str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True)
print('PASS Ctrl/GUI: all keycodes and states; 256 masks across owner combinations; lock ordering and held transitions')
