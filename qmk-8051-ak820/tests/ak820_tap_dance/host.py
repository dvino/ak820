#!/usr/bin/env python3
"""Compile the production compact TD engine against an offline event fixture."""
import argparse, pathlib, re, subprocess, tempfile
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--sdcc",type=pathlib.Path,help="Also compile the production engine for SDCC mcs51")
args=parser.parse_args()
ROOT=pathlib.Path(__file__).resolve().parents[2]
source=(ROOT/'keyboards/ajazz/ak820/ak820_tap_dance.c').read_text()
source=re.sub(r'^#include[^\n]*\n','',source,flags=re.M)
fixture=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#define AK820_STATE_MEM
#define MATRIX_ROWS 16
#define MATRIX_COLS 8
#define VIAL_TAP_DANCE_ENTRIES 8
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#define QK_MOD_TAP 0x2000
#define QK_TAP_DANCE 0x5700
#define QK_TAP_DANCE_MAX 0x57ff
#define KEY_EVENT 1
#define IS_NOEVENT(e) ((e).type==0)
typedef struct {uint8_t row,col;} keypos_t;
typedef struct {keypos_t key;bool pressed;uint16_t time;uint8_t type;} keyevent_t;
typedef struct {keyevent_t event;struct {uint8_t count;} tap;uint16_t keycode;} keyrecord_t;
typedef struct {uint16_t on_tap,on_hold,on_double_tap,on_tap_hold,custom_tapping_term;} vial_tap_dance_entry_t;
static vial_tap_dance_entry_t fixture[8];
static unsigned refs[256],downs[256];
static bool ak820_macro_primitive, cancel_on_down, reenter_on_down;
static void reenter(void);
void ak820_tap_dance_cancel(void);
static int get_repeat_key_count(void){return 0;}
static int dynamic_keymap_get_tap_dance(uint8_t i,vial_tap_dance_entry_t *e){*e=fixture[i];return 0;}
static void process_record(keyrecord_t *r){uint8_t k=r->keycode;if(r->event.pressed){refs[k]++;downs[k]++;if(reenter_on_down){reenter_on_down=false;reenter();}if(cancel_on_down){cancel_on_down=false;ak820_tap_dance_cancel();memset(refs,0,sizeof refs);}}else{assert(refs[k]);refs[k]--;}}
'''
cases=r'''
static void reenter(void) {
    /* Model a nested callback with a new pending gesture. The outer dispatch
     * must keep its work slot and the new gesture must finish later. */
    td_slots[1].source=1;td_slots[1].state=TD_DOWN+1;
    td_entry=fixture[1];td_wait=&td_slots[1];td_map_set(1,1);
    td_finish(false);
}
static uint16_t clock_now;
static void event(unsigned id,bool down,uint16_t code){keyrecord_t r={.event={.key={id/8,id%8},.pressed=down,.time=clock_now,.type=KEY_EVENT},.keycode=code};ak820_tap_dance_task(clock_now);if(ak820_tap_dance_before(&r.event)&&ak820_tap_dance_process(&r))process_record(&r);clock_now+=5;}
static void fresh(void){ak820_tap_dance_cancel();memset(refs,0,sizeof refs);memset(downs,0,sizeof downs);memset(fixture,0,sizeof fixture);clock_now=100;cancel_on_down=false;reenter_on_down=false;fixture[0]=(vial_tap_dance_entry_t){4,5,6,7,200};fixture[1]=fixture[0];}
static void expire(void){clock_now+=201;ak820_tap_dance_task(clock_now);}
int main(void){
const uint8_t expected_pattern[9]={0,1,2,3,4,5,6,7,8};uint8_t expected[TD_SOURCES];
assert(sizeof(td_map)==(TD_SOURCES+1)/2);
for(unsigned i=0;i<TD_SOURCES;i++){expected[i]=expected_pattern[i%9];td_map_set(i,expected[i]);}
for(unsigned i=0;i<TD_SOURCES;i++)assert(td_map_get(i)==expected[i]);
/* Every internal setter value must preserve the other packed source. */
for(unsigned i=0;i<TD_SOURCES;i++)for(unsigned prior=0;prior<=TD_MAP_NONE;prior++)
    for(unsigned value=0;value<=TD_MAP_NONE;value++){
        unsigned neighbor=i^1;td_map_set(neighbor,prior);td_map_set(i,value);
        assert(td_map_get(i)==value);assert(td_map_get(neighbor)==prior);
    }
/* Repeated press with a changed keycode can leave multiple live slots for
 * one physical source. The latest explicit map entry, not the first matching
 * source, determines which slot the release addresses. */
fresh();event(0,1,0x5700);event(0,1,0x5701);
assert(td_slots[0].state&&td_slots[1].state&&td_slots[0].source==0&&td_slots[1].source==0);
assert(td_map_get(0)==1);event(0,0,0x5701);assert(!(td_slots[1].state&TD_DOWN));assert(td_slots[0].state&TD_DOWN);
fresh();event(0,1,0x5700);event(0,0,0x5700);assert(!downs[4]);expire();assert(downs[4]==1&&!refs[4]);
fresh();event(0,1,0x5700);expire();assert(refs[5]==1);event(0,0,4);assert(!refs[5]);
fresh();event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5700);event(0,0,0x5700);expire();assert(downs[6]==1&&!refs[6]);
fresh();event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5700);expire();assert(refs[7]);event(0,0,0x5700);assert(!refs[7]);
fresh();fixture[0].on_double_tap=0;event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5700);event(0,0,0x5700);expire();assert(downs[4]==2);
fresh();fixture[0].on_tap_hold=0;event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5700);expire();assert(downs[4]==1&&refs[5]);event(0,0,0x5700);assert(!refs[5]);
fresh();event(0,1,0x5700);event(1,1,8);assert(refs[4]==1&&!refs[5]);event(0,0,0x5700);assert(!refs[4]);
fresh();event(0,1,0x5700);expire();event(1,1,0x5701);expire();assert(refs[5]==2);event(0,0,0x5700);assert(refs[5]==1);event(1,0,0x5701);assert(!refs[5]);
fresh();event(0,1,0x5700);expire();event(1,1,0x5700);event(1,0,4);assert(refs[5]==1);event(0,0,4);assert(!refs[5]);
fresh();clock_now=65520;event(0,1,0x5700);event(0,0,0x5700);clock_now=190;ak820_tap_dance_task(clock_now);assert(downs[4]==1);
fresh();event(0,1,0x5700);ak820_tap_dance_cancel();expire();assert(!downs[4]&&!downs[5]);
fresh();fixture[0].on_tap=0x5700;assert(!ak820_tap_dance_valid(&fixture[0]));fixture[0].on_tap=0x0104;assert(ak820_tap_dance_valid(&fixture[0]));fixture[0].custom_tapping_term=32768;assert(!ak820_tap_dance_valid(&fixture[0]));
fresh();fixture[0]=(vial_tap_dance_entry_t){0};event(0,1,0x5700);event(0,0,0x5700);expire();assert(!downs[4]);
fresh();event(0,1,0x5700);event(0,0,0x5700);event(0,1,8);assert(downs[4]==1&&refs[8]==1);event(0,0,8);assert(!refs[8]);
fresh();event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5701);expire();assert(downs[4]==1&&refs[5]==1);event(0,0,0x5701);assert(!refs[5]);
fresh();fixture[0].on_double_tap=0;event(0,1,0x5700);event(0,0,0x5700);event(0,1,0x5700);event(0,0,0x5700);cancel_on_down=true;expire();assert(downs[4]==1&&!refs[4]);
fresh();event(0,1,0x5700);cancel_on_down=true;expire();assert(downs[5]==1&&!refs[5]);event(0,0,0x5700);assert(!refs[5]);
fresh();fixture[1].on_hold=9;event(0,1,0x5700);reenter_on_down=true;expire();assert(refs[5]==1&&!downs[9]);expire();assert(refs[9]==1);event(0,0,0x5700);event(1,0,0x5701);assert(!refs[5]&&!refs[9]);
fresh();event(0,1,0x5700);cancel_on_down=true;expire();event(0,0,0x5700);event(0,1,0x5700);event(0,0,0x5700);expire();assert(downs[4]==1&&!refs[4]);
puts("compact Tap Dance host cases passed");return 0;}
'''
with tempfile.TemporaryDirectory(prefix='ak820-td-host-') as temp:
    p=pathlib.Path(temp);(p/'test.c').write_text(fixture+source+cases)
    subprocess.run(['cc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=undefined',str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True)

if args.sdcc:
    with tempfile.TemporaryDirectory(prefix='ak820-td-sdcc-') as temp:
        p=pathlib.Path(temp)
        target=fixture.replace('#define AK820_STATE_MEM\n','#define AK820_STATE_MEM __xdata\n')
        target=target.replace('vial_tap_dance_entry_t *e','vial_tap_dance_entry_t __xdata *e')
        (p/'module.c').write_text(target+source+'\nstatic void reenter(void) {}\n')
        subprocess.run([str(args.sdcc),'--std-c11','--model-large','-mmcs51','-c',str(p/'module.c'),'-o',str(p/'module.rel')],check=True)
        print('compact Tap Dance SDCC mcs51 compile passed (isolated ABI fixture)')

# Shared production storage regression; no device access.
import sys
subprocess.check_call([sys.executable, str(ROOT / "tests/ak820_extensions/storage.py")])
