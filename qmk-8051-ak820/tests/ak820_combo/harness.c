// SPDX-License-Identifier: GPL-2.0-or-later
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_combo.h"
static vial_combo_entry_t entries[VIAL_COMBO_ENTRIES];
static keyrecord_t logbuf[64];
static unsigned n, traces;
int dynamic_keymap_get_combo(uint8_t i,vial_combo_entry_t *e) {*e=entries[i];return 0;}
void process_record(keyrecord_t *r) {assert(n<64);logbuf[n++]=*r;}
void clear_keyboard(void) {ak820_combo_cancel();}
static void event(uint8_t id,uint16_t code,bool down,uint16_t time) {
    keyrecord_t r={.event={{id/8,id%8},down,time},.keycode=code};
    ak820_combo_tick(time);
    if(ak820_combo_process(&r)) process_record(&r);
}
static void reset(void) {traces++;ak820_combo_cancel();n=0;memset(entries,0,sizeof(entries));entries[0]=(vial_combo_entry_t){{4,5,0,0},6};ak820_combo_reload();}
static void expect(unsigned i,uint16_t code,bool down) {assert(i<n);assert(logbuf[i].keycode==code);assert(logbuf[i].event.pressed==down);}
int main(void) {
    reset();event(0,4,true,0);assert(!n);event(1,5,true,39);assert(n==1);expect(0,6,true);
    event(0,4,false,40);expect(1,6,false);event(1,5,false,41);assert(n==2);
    reset();event(1,5,true,0);event(0,4,true,1);event(1,5,false,2);event(0,4,false,3);assert(n==2);expect(0,6,true);expect(1,6,false);
    reset();event(0,4,true,0);ak820_combo_tick(39);assert(!n);ak820_combo_tick(40);expect(0,4,true);event(0,4,false,41);expect(1,4,false);
    reset();event(0,4,true,65520);ak820_combo_tick(23);assert(!n);ak820_combo_tick(24);expect(0,4,true);
    reset();event(0,4,true,0);event(0,4,false,1);assert(n==2);expect(0,4,true);expect(1,4,false);
    reset();event(0,4,true,0);event(2,7,true,1);assert(n==2);expect(0,4,true);expect(1,7,true);
    reset();event(0,4,true,0);event(2,0x2107,true,1);assert(n==2);expect(0,4,true);expect(1,0x2107,true);
    /* A full-width event sharing a trigger's low byte is not a combo input. */
    reset();event(0,0x0104,true,0);assert(n==1);expect(0,0x0104,true);
    reset();event(0,4,true,0);event(1,5,true,40);assert(n==1);expect(0,4,true);ak820_combo_tick(80);expect(1,5,true);
    reset();event(0,4,true,0);event(1,5,true,1);event(2,4,true,2);event(3,5,true,3);assert(n==3);expect(1,4,true);expect(2,5,true);
    reset();entries[1]=(vial_combo_entry_t){{4,5,0,0},7};ak820_combo_reload();event(0,4,true,0);event(1,5,true,1);expect(0,6,true);
    reset();event(0,4,true,0);ak820_combo_cancel();ak820_combo_tick(100);assert(!n);
    reset();event(0,4,true,0);event(1,5,true,1);ak820_combo_cancel();ak820_combo_tick(100);assert(n==1); /* external clear owns output cancellation */
    vial_combo_entry_t e={{0},0};assert(ak820_combo_valid(&e));e=(vial_combo_entry_t){{4,5,0,0},224};assert(ak820_combo_valid(&e));
    e.input[2]=7;assert(!ak820_combo_valid(&e));e.input[2]=0;e.input[1]=4;assert(!ak820_combo_valid(&e));e.input[1]=5;e.output=0x104;assert(ak820_combo_valid(&e));e.output=0x2004;assert(!ak820_combo_valid(&e));e.output=0x7c73;assert(ak820_combo_valid(&e));e.output=0x7c72;assert(!ak820_combo_valid(&e));e.output=0x7c00;assert(!ak820_combo_valid(&e));e.output=6;e.input[0]=0x2004;assert(!ak820_combo_valid(&e));
    /* Exhaust the byte input fields and 16-bit output against the original
       inclusive-range validator, with other fields held valid. */
    e=(vial_combo_entry_t){{4,5,0,0},6};
    for(unsigned v=0;v<256;++v) {
        e.input[0]=v;assert(ak820_combo_valid(&e)==(v>=KC_A && v<=KC_EXSEL && v!=5));
        e.input[0]=4;e.input[1]=v;assert(ak820_combo_valid(&e)==(v>=KC_A && v<=KC_EXSEL && v!=4));
        e.input[1]=5;
    }
    for(unsigned v=0;v<=0xffff;++v) {
        unsigned lo=v&255,hi=v>>8;
        bool expected=v==QK_CAPS_WORD_TOGGLE || (!hi && lo>=KC_AUDIO_MUTE && lo<=KC_LAUNCHPAD) ||
            (hi<(QK_MOD_TAP>>8) && ((lo>=KC_A && lo<=KC_EXSEL) || (lo>=KC_LEFT_CTRL && lo<=KC_RIGHT_GUI)));
        e.output=v;assert(ak820_combo_valid(&e)==expected);
    }
    reset();entries[0].input[1]=22;entries[0].output=0x7c73;ak820_combo_reload();event(0,4,true,0);assert(!n);event(1,22,true,1);assert(n==1);expect(0,0x7c73,true);event(1,22,false,2);event(0,4,false,3);assert(n==2);expect(1,0x7c73,false);
    reset();entries[0].input[1]=22;entries[0].output=0x7c73;ak820_combo_reload();event(1,22,true,0);event(0,4,true,1);assert(n==1);expect(0,0x7c73,true);event(0,4,false,2);event(1,22,false,3);assert(n==2);expect(1,0x7c73,false);
    reset();event(0,4,true,0);event(1,4,true,1);assert(n==1);expect(0,4,true);ak820_combo_tick(41);expect(1,4,true);
    reset();e=(vial_combo_entry_t){{4,5,0,0},KC_AUDIO_MUTE};assert(ak820_combo_valid(&e));e.output=KC_LAUNCHPAD;assert(ak820_combo_valid(&e));e.output=0x100|KC_AUDIO_MUTE;assert(!ak820_combo_valid(&e));
    reset();event(0,4,true,0);event(3,QK_COMBO_OFF,true,1);assert(n==1);expect(0,4,true);event(1,5,true,2);expect(1,5,true);event(3,QK_COMBO_ON,true,3);
    printf("compact combo production engine: %u traces and configuration validation PASS (host C/UBSan; no hardware)\n",traces);
}
