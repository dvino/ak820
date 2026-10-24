#!/usr/bin/env python3
"""Differential check of volatile Mac/PC report swapping."""
from pathlib import Path
import subprocess
import tempfile
import argparse, json
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path)
args=parser.parse_args()

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
#define AK820_MAC_PC
#define AK820_COMPACT_CTRL_GUI_SWAP
#define AK820_COMPACT_TAPPING
#define AK820_BOARD
#define NO_ACTION_ONESHOT
#define QK_MAGIC_GUI_ON 0x7009
#define QK_MAGIC_GUI_OFF 0x700a
#define QK_MAGIC_TOGGLE_GUI 0x700b
#define QK_MAGIC_SWAP_ALT_GUI 0x7014
#define QK_MAGIC_UNSWAP_ALT_GUI 0x7015
#define QK_MAGIC_TOGGLE_ALT_GUI 0x7016
#define KC_LGUI 0xe3
#define KC_RGUI 0xe7
#define MOD_BIT(k) (1u << ((k) & 7))
typedef struct { uint8_t mods, reserved, keys[6]; } report_keyboard_t;
static report_keyboard_t actual_keyboard_report, sent;
#define keyboard_report (&actual_keyboard_report)
static uint8_t real_mods, weak_mods, owned_mods, owned_weak_mods, oneshot_mods;
static bool gui_disabled, ak820_mac_mode, ctrl_gui_swapped;
#define QK_MAGIC_SWAP_CTL_GUI 0x701b
#define QK_MAGIC_UNSWAP_CTL_GUI 0x701c
#define QK_MAGIC_TOGGLE_CTL_GUI 0x701d
#define AK820_STATE_MEM
static uint8_t owned_mod_refs[8], owned_weak_refs[8], macro_mods[2];
bool ak820_macro_primitive, ak820_macro_cancelled;
static unsigned sends;
void host_keyboard_send(report_keyboard_t *report) { sent = *report; ++sends; }
void send_keyboard_report(void);
''' + text[text.index('static void change_owned('):text.index('/* Keyboard usages need ownership')] + function('bool ak820_gui_process(') + function('void send_keyboard_report(') + r'''
static uint8_t oracle(uint8_t m) {
    uint8_t out=m & (uint8_t)~0xcc;
    if (m&0x04) out|=0x08;
    if (m&0x08) out|=0x04;
    if (m&0x40) out|=0x80;
    if (m&0x80) out|=0x40;
    return out;
}
int main(void) {
    /* Exact supported controls only: exhaustive domain, states and edges. */
    for (uint32_t code=0; code<=65535; ++code) for (unsigned state=0;state<2;++state)
      for (unsigned press=0;press<2;++press) {
        ak820_mac_mode=state; gui_disabled=false; unsigned n=sends;
        bool pass=ak820_gui_process(code,press);
        ctrl_gui_swapped=false;
        bool ctl=code==0x7014||code==0x7015||code==0x7016||
                 (code>=0x7009&&code<=0x700b)||(code>=0x701b&&code<=0x701d);
        assert(pass==!ctl);
        bool expected=state;
        if (code==0x7014&&press) expected=true;
        if (code==0x7015&&press) expected=false;
        if (code==0x7016&&press) expected=!state;
        assert(ak820_mac_mode==expected);
        if (!ctl||!press) assert(sends==n);
    }
    /* All 256 effective bitsets, assembled across owner classes, both
       transformations, and GUI lock after the transform. Owners stay raw. */
    for (unsigned m=0;m<256;++m) for (unsigned split=0;split<16;++split)
      for (unsigned swap=0;swap<2;++swap) for (unsigned lock=0;lock<2;++lock) for(unsigned cg=0;cg<2;++cg) {
        real_mods=(split==0||split&1)?m:0; weak_mods=(split&2)?m:0;
        owned_mods=(split&4)?m:0; owned_weak_mods=(split&8)?m:0;
        oneshot_mods=0; ak820_mac_mode=swap; gui_disabled=lock;
        ctrl_gui_swapped=cg;
        uint8_t want=swap?oracle(m):m;
        if(cg) want=(want&0x66)|((want&0x11)<<3)|((want&0x88)>>3);
        if(lock) want &= (uint8_t)~0x88;
        send_keyboard_report(); if(actual_keyboard_report.mods!=want) { fprintf(stderr,"m=%u split=%u swap=%u lock=%u got=%u want=%u\\n",m,split,swap,lock,actual_keyboard_report.mods,want); return 2; }
        assert((real_mods|weak_mods|owned_mods|owned_weak_mods)==m);
      }
    /* Set, reset and toggle while a physical Alt owner is held. Up edges
       never change a mode; every down edge publishes the current mapping. */
    real_mods=4; weak_mods=owned_mods=owned_weak_mods=oneshot_mods=0;
    ak820_mac_mode=false; gui_disabled=false; ctrl_gui_swapped=false;
    ak820_gui_process(0x7014,true); assert(ak820_mac_mode && sent.mods==8);
    ak820_gui_process(0x7015,false); assert(ak820_mac_mode && sent.mods==8);
    ak820_gui_process(0x7016,false); assert(ak820_mac_mode && sent.mods==8);
    ak820_gui_process(0x7016,true); assert(!ak820_mac_mode && sent.mods==4);
    ak820_gui_process(0x7016,true); assert(ak820_mac_mode && sent.mods==8);
    ak820_gui_process(0x7015,true); assert(!ak820_mac_mode && sent.mods==4);
    /* Mixed owners and immediate mode changes while held; each up edge leaves
       only the surviving owner, including a GUI lock applied after swap. */
    real_mods=0x11; weak_mods=0x08; owned_mods=0x80; owned_weak_mods=0x04;
    ak820_mac_mode=false; gui_disabled=false; ctrl_gui_swapped=false;
    ak820_gui_process(0x7014,true); assert(sent.mods==oracle(0x9d));
    assert(real_mods==0x11 && weak_mods==8 && owned_mods==0x80 && owned_weak_mods==4);
    ak820_gui_process(0x7014,false); assert(sent.mods==oracle(0x9d));
    ak820_gui_process(0x700a,true); assert(sent.mods==(uint8_t)(oracle(0x9d)&~0x88));
    ak820_gui_process(0x7015,true); assert(sent.mods==(uint8_t)(0x9d&~0x88));
    /* Compact One Shot is an owned modifier. A queued owner, a held
       action, a weak action, and an encoded macro can overlap on one bit. */
    clear_owned_mods();
    real_mods=weak_mods=0; ak820_mac_mode=true; gui_disabled=ctrl_gui_swapped=false;
    add_owned_mods(4); /* queued One Shot Alt */
    add_owned_mods(4); /* held physical/Mod-Tap Alt */
    add_owned_weak_mods(8); /* weak GUI action */
    ak820_macro_primitive=true;
    add_owned_mods(4); add_owned_mods(4); /* duplicate macro-down is one owner */
    assert(owned_mod_refs[2]==3 && owned_weak_refs[3]==1);
    send_keyboard_report(); assert(sent.mods==12);
    ak820_gui_process(0x7015,true); assert(sent.mods==12);
    assert(owned_mod_refs[2]==3 && macro_mods[0]==4);
    del_owned_mods(4); del_owned_mods(4); /* duplicate macro-up changes once */
    ak820_macro_primitive=false;
    assert(owned_mod_refs[2]==2 && owned_mods==4);
    del_owned_mods(4); /* consume One Shot */
    ak820_gui_process(0x7014,true); assert(sent.mods==12);
    del_owned_weak_mods(8); send_keyboard_report(); assert(sent.mods==8);
    del_owned_mods(4); send_keyboard_report(); assert(sent.mods==0);
    clear_owned_mods(); assert(ak820_mac_mode); /* cleanup retains session */
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-mac-pc-host-') as directory:
    p=Path(directory); (p/'test.c').write_text(source)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined',
                    str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True)
result={'level':'host production function extraction; no device validation','pass':True,'checks':['all 65536 keycodes, both edges/states','all 256 modifier masks across real/weak/owned owner combinations','held mapping transitions and GUI lock ordering','production owned refcounts: OneShot, weak, held and macro overlap/cleanup']}
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
