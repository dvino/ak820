#!/usr/bin/env python3
"""Frozen-before/production Combo parser differential model; no device access."""
from pathlib import Path
import re, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[2]

def block(s,start):
 p=s.index(start); i=s.index('{',p)+1; depth=1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}'); i+=1
 return s[p:i]
def fun(s,name):
 m=re.search(r'^(?:static )?(?:int|bool|uint16_t|void) '+name+r'\([^\n]*\) \{',s,re.M)
 assert m,name
 return block(s,m.group())
before=subprocess.check_output(['git','show','09330ab:qmk-8051-ak820/quantum/vial.c'],cwd=ROOT.parent,text=True)
after=(ROOT/'quantum/vial.c').read_text()
get_adapter=block(after,'case dynamic_vial_combo_get: {')
assert '#if defined(AK820_COMPACT_COMBO) && defined(__SDCC_mcs51)' in get_adapter
assert '_Alignof(vial_combo_entry_t) == 1' in get_adapter
assert block(before,'case dynamic_vial_combo_set: {') == block(after,'case dynamic_vial_combo_set: {')
dynamic=(ROOT/'quantum/dynamic_keymap.c').read_text()
combo=(ROOT/'keyboards/ajazz/ak820/ak820_combo.c').read_text()
header=(ROOT/'quantum/vial.h').read_text()
typ=re.search(r'typedef struct \{[^}]*\} vial_combo_entry_t;',header).group()
fixture=r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#define AK820_STATE_MEM
#define AK820_COMPACT_COMBO
#define VIAL_COMBO_ENTRIES 8
#define VIAL_COMBO_EEPROM_ADDR 0x658
#define AK820_COMBO_MARKER 0x0820
#define AK820_COMBO_VERSION 1
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#define QK_MOD_TAP 0x2000
#define QK_BOOT 0x7c00
#define KC_NO 0
#define COMBO_INPUT(c) ((c)>=KC_A&&(c)<=KC_EXSEL)
#define COMBO_OUTPUT(c) ((c)<QK_MOD_TAP&&(COMBO_INPUT((uint8_t)(c))||((uint8_t)(c)>=KC_LEFT_CTRL&&(uint8_t)(c)<=KC_RIGHT_GUI)))
enum {dynamic_vial_combo_get=1,dynamic_vial_combo_set};
static bool vial_unlocked,healthy,fail_write,fail_flush;
static uint8_t memory[2048],packet[32],cache[80];
struct event {unsigned kind,address,size;uint8_t data[10];};
static struct event events[64];static unsigned count;
static void trace(unsigned k,unsigned a,unsigned n,const void *p){
 assert(count<64);struct event *e=&events[count++];memset(e,0,sizeof *e);
 e->kind=k;e->address=a;e->size=n;if(p)memcpy(e->data,p,n);
}
static bool ak820_nvm_ok(void){trace(1,healthy,0,0);return healthy;}
static void clear_keyboard(void){trace(2,0,0,0);}
static void ak820_eeprom_read_block_xdata(void *p,const void *a,size_t n){
 unsigned at=(uintptr_t)a;assert(at+n<=sizeof memory);memcpy(p,memory+at,n);trace(3,at,n,p);
}
static void ak820_eeprom_write_block_xdata(const void *p,void *a,size_t n){
 unsigned at=(uintptr_t)a;assert(at+n<=sizeof memory);trace(4,at,n,p);memcpy(memory+at,p,n);if(fail_write)healthy=false;
}
static void ak820_nvm_flush(void){trace(5,0,0,0);if(fail_flush)healthy=false;}
'''
parts=[typ,block(before,'static uint16_t vial_keycode_firewall'),fun(combo,'ak820_combo_valid'),fun(dynamic,'dynamic_keymap_get_combo'),fun(dynamic,'dynamic_keymap_set_combo')]
parts.append('''static void reload_combo(void){trace(6,0,0,0);for(uint8_t i=0;i<8;i++){vial_combo_entry_t e;assert(!dynamic_keymap_get_combo(i,&e));memcpy(cache+i*10,&e,10);}}''')
for name,src in [('reference',before),('production',after)]:
 cases='\n'.join(block(src,'case dynamic_vial_combo_'+op+': {') for op in ('get','set'))
 parts.append('static void '+name+'(uint8_t *msg){switch(msg[2]){'+cases+'}}')
cases=r'''
static void reset(unsigned cmd,unsigned idx,unsigned row,unsigned fault,unsigned unlocked){
 memset(memory,0xa5,sizeof memory);memset(cache,0x5a,sizeof cache);memset(events,0,sizeof events);count=0;
 healthy=fault!=1;fail_write=fault==2;fail_flush=fault==3;vial_unlocked=unlocked;
 vial_combo_entry_t e={{4,5,0,0},4};
 if(row==1)e.output=QK_BOOT;if(row==2)e.input[1]=4;if(row==3)e.input[2]=1;
 if(row==4)memset(&e,0,sizeof e);if(row==5)e.output=0x104;
 for(unsigned i=0;i<32;i++)packet[i]=0x80+i;
 packet[2]=cmd;packet[3]=idx;memcpy(packet+4,&e,10);
 e.input[2]=AK820_COMBO_MARKER;e.input[3]=row==6?2:AK820_COMBO_VERSION;
 if(row==7)e.input[2]=0;
 for(unsigned i=0;i<8;i++)memcpy(memory+VIAL_COMBO_EEPROM_ADDR+i*10,&e,10);
}
int main(void){unsigned runs=0;
 for(unsigned cmd=1;cmd<=2;cmd++)for(unsigned idx=0;idx<256;idx++)for(unsigned row=0;row<8;row++)for(unsigned fault=0;fault<4;fault++)for(unsigned unlock=0;unlock<2;unlock++){
 uint8_t reply[32],saved[2048],expected_cache[80];struct event expected[64];unsigned ec;bool eh;
 reset(cmd,idx,row,fault,unlock);reference(packet);memcpy(reply,packet,32);memcpy(saved,memory,2048);memcpy(expected_cache,cache,80);memcpy(expected,events,sizeof events);ec=count;eh=healthy;
 reset(cmd,idx,row,fault,unlock);production(packet);
 assert(!memcmp(reply,packet,32));assert(!memcmp(saved,memory,2048));assert(!memcmp(expected_cache,cache,80));assert(ec==count&&!memcmp(expected,events,count*sizeof *events));assert(eh==healthy);runs++;
 }
 printf("PASS Combo: %u differential cases; 256 indices, locked/unlocked boot output, corruption, complete reply, NVM/cache and ordered I/O/fault/reload traces\n",runs);
}
'''
for target in (False,True):
 with tempfile.TemporaryDirectory(prefix='combo-packet-') as d:
  work=Path(d); (work/'test.c').write_text(fixture+'\n'.join(parts)+cases)
  cmd=['cc','-std=c11','-O1','-Wall','-Wextra','-Werror','-Wno-misleading-indentation','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined']
  if target:cmd+=['-D__SDCC_mcs51','-fpack-struct=1']
  cmd += [str(work/'test.c'),'-o',str(work/'test')]
  subprocess.run(cmd,check=True);print('Mode: '+('SDCC byte-alignment model' if target else 'native fallback'),flush=True);subprocess.run([str(work/'test')],check=True)
