#!/usr/bin/env python3
"""Differential native VIA parser model; no firmware or device qualification."""
from pathlib import Path
import re, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def function(s):
    a=s.index('void raw_hid_receive('); b=s.index('{',a)+1; depth=1
    while depth:
        depth+=(s[b]=='{')-(s[b]=='}'); b+=1
    return s[a:b]

header=(ROOT/'qmk-8051-ak820/quantum/via.h').read_text()
enums='\n'.join(re.findall(r'enum via_(?:command_id|keyboard_value_id) \{.*?\};',header,re.S))
vial=(ROOT/'qmk-8051-ak820/quantum/vial.h').read_text()
enums+='\n'+re.search(r'enum \{\s*vial_get_keyboard_id.*?\};',vial,re.S).group()
fixture=r'''
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define AK820_BOARD
#define VIAL_ENABLE
#define MATRIX_COLS 8
#define MATRIX_ROWS 4
#define VIA_PROTOCOL_VERSION 9
#define QK_BOOT 0x7c00
static bool vial_unlocked,vial_unlock_in_progress,write_ok;
static unsigned trace[512], used;
static void event(unsigned a,unsigned b,unsigned c){ if(used+3>512) abort();trace[used++]=a;trace[used++]=b;trace[used++]=c; }
static uint32_t timer_read32(void){event(1,0,0);return 0x89abcdef;}
static uint32_t via_get_layout_options(void){event(2,0,0);return 0xfedcba98;}
static void via_set_layout_options(uint32_t x){event(3,x,0);}
typedef uint8_t matrix_row_t;
static matrix_row_t matrix_get_row(uint8_t x){event(4,x,0);return x+15;}
static uint16_t dynamic_keymap_get_keycode(uint8_t a,uint8_t b,uint8_t c){event(5,a,b);return c+0x8900;}
static void dynamic_keymap_set_keycode(uint8_t a,uint8_t b,uint8_t c,uint16_t d){event(6,a,b);event(7,c,d);}
static void dynamic_keymap_reset(void){event(8,0,0);}
static uint8_t dynamic_keymap_macro_get_count(void){event(9,0,0);return 16;}
static uint16_t dynamic_keymap_macro_get_buffer_size(void){event(10,0,0);return 8192;}
static uint8_t dynamic_keymap_get_layer_count(void){event(11,0,0);return 6;}
static void dynamic_keymap_macro_reset(void){event(12,0,0);}
static void raw_hid_receive_kb(uint8_t *p,uint8_t n){event(13,n,0);p[0]=255;}
static void vial_handle_cmd(uint8_t *p,uint8_t n){event(14,n,p[1]);p[0]=42;}
static void raw_hid_send(uint8_t *p,uint8_t n){event(15,n,p[0]);}
static void wait_ms(unsigned n){event(16,n,0);}
static void bootloader_jump(void){event(17,0,0);}
static bool buffer(unsigned k,uint16_t o,uint16_t n,uint8_t *p){event(k,o,n);for(unsigned i=0;i<n;i++){event(30,i,p[i]);if(k==20||k==22)p[i]=(uint8_t)(o+i);}return write_ok;}
#define dynamic_keymap_macro_get_buffer(o,n,p) buffer(20,o,n,p)
#define dynamic_keymap_macro_set_buffer(o,n,p) buffer(21,o,n,p)
#define dynamic_keymap_get_buffer(o,n,p) buffer(22,o,n,p)
#define dynamic_keymap_set_buffer(o,n,p) buffer(23,o,n,p)
'''
ref=function((HERE/'via.before.c').read_text()).replace('void raw_hid_receive(', 'void reference(')
prod=function((ROOT/'qmk-8051-ak820/quantum/via.c').read_text()).replace('void raw_hid_receive(', 'void production(')
main=r'''
static uint32_t seed=0x89515;static uint8_t rnd(void){seed=seed*1664525+1013904223;return seed>>24;}
int main(void){unsigned count=0;for(unsigned cmd=0;cmd<256;cmd++)for(unsigned size=0;size<256;size++)for(unsigned state=0;state<8;state++){
 uint8_t a[32],b[32];unsigned old[512],oldused;for(unsigned i=0;i<32;i++)a[i]=rnd();a[0]=cmd;a[3]=size;memcpy(b,a,32);
 vial_unlocked=state&1;vial_unlock_in_progress=state&2;write_ok=state&4;uint8_t n=(size%17==0)?31:32;
 used=0;reference(a,n);oldused=used;memcpy(old,trace,used*sizeof(unsigned));used=0;production(b,n);
 if(memcmp(a,b,32)||used!=oldused||memcmp(old,trace,used*sizeof(unsigned))){fprintf(stderr,"Mismatch cmd=%u size=%u state=%u\n",cmd,size,state);return 1;}count++;
 }printf("PASS %u differential packets, full reply and ordered call trace\n",count);}
'''
with tempfile.TemporaryDirectory() as td:
    c=Path(td)/'test.c'; exe=Path(td)/'test';c.write_text(fixture+enums+ref+prod+main)
    subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined,address',str(c),'-o',str(exe)],check=True)
    subprocess.run([str(exe)],check=True)
