// SPDX-License-Identifier: GPL-2.0-or-later
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include "ak820_combo.h"
#define AK820_COMPACT_COMBO
#define VIAL_COMBO_EEPROM_ADDR 0x658
#define AK820_COMBO_MARKER 0x0820
#define AK820_COMBO_VERSION 1
static uint8_t bytes[0x800];
static unsigned writes, clears, flushes;
static bool healthy=true, fail_flush;
void process_record(keyrecord_t *r) {(void)r;}
bool ak820_nvm_ok(void) {return healthy;}
void ak820_nvm_flush(void) {flushes++;if(fail_flush)healthy=false;}
void clear_keyboard(void) {clears++;ak820_combo_cancel();}
void ak820_eeprom_read_block_xdata(void *dst,const void *addr,size_t len) {assert((uintptr_t)addr+len<=sizeof(bytes));memcpy(dst,bytes+(uintptr_t)addr,len);}
void ak820_eeprom_write_block_xdata(const void *src,void *addr,size_t len) {assert((uintptr_t)addr+len<=sizeof(bytes));writes++;memcpy(bytes+(uintptr_t)addr,src,len);}
/* PRODUCTION */
int main(void) {
 vial_combo_entry_t e={{4,5,0,0},0x104}, got;
 memset(bytes,0xFF,sizeof(bytes));assert(!dynamic_keymap_get_combo(0,&got));assert(!got.input[0]&&!got.output);assert(!writes);
 for(unsigned i=0;i<8;i++) {assert((0x658+i*10)/64==(0x658+i*10+9)/64);assert(!dynamic_keymap_set_combo(i,&e));assert(!dynamic_keymap_get_combo(i,&got));assert(!memcmp(&e,&got,sizeof(e)));assert(bytes[0x658+i*10+4]==0x20&&bytes[0x658+i*10+5]==8&&bytes[0x658+i*10+6]==1);}
 assert(writes==8&&clears==8&&flushes==8);
 unsigned old=writes;assert(dynamic_keymap_set_combo(8,&e));assert(writes==old);
 e.input[2]=7;assert(dynamic_keymap_set_combo(0,&e));assert(writes==old);e.input[2]=0;
 e.output=0x7c73;assert(!dynamic_keymap_set_combo(0,&e));assert(!dynamic_keymap_get_combo(0,&got));assert(got.output==0x7c73);old=writes;
 e.output=0x7c72;assert(dynamic_keymap_set_combo(0,&e));assert(writes==old);e.output=0x104;
 healthy=false;assert(dynamic_keymap_set_combo(0,&e));assert(writes==old);healthy=true;
 bytes[0x658]=0xff;assert(!dynamic_keymap_get_combo(0,&got));assert(!got.input[0]);assert(!dynamic_keymap_set_combo(0,&e));
 bytes[0x65c]=0;assert(!dynamic_keymap_get_combo(0,&got));assert(!got.input[0]);
 assert(!dynamic_keymap_set_combo(0,&e));bytes[0x65e]=2;old=writes;
 assert(!dynamic_keymap_get_combo(0,&got));assert(!got.input[0]&&!got.output);assert(writes==old);
 assert(!dynamic_keymap_set_combo(0,&e));
 fail_flush=true;assert(dynamic_keymap_set_combo(0,&e));fail_flush=false;healthy=true;
 memset(&e,0,sizeof(e));assert(!dynamic_keymap_set_combo(0,&e));assert(!dynamic_keymap_get_combo(0,&got));assert(!got.input[0]&&!got.output);
 puts("compact combo production storage: bounds/markers/validation/fault/verified-flush PASS (host model; no flash hardware)");
}
