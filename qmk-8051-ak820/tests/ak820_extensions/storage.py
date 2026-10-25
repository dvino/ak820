#!/usr/bin/env python3
"""Production TD/KO storage and validators in a host NVM model; no USB or durable hardware proof."""
from pathlib import Path
import re
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[2]

def function(source, name):
    match = re.search(r'^(?:static )?(?:int|bool|uint16_t) ' + name + r'\([^\n]*\) \{', source, re.M)
    if not match:
        raise RuntimeError('Missing production function: ' + name)
    end = source.index('{', match.start()) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[match.start():end]

vial = (ROOT / 'quantum/vial.h').read_text()
types = []
for name in ('vial_tap_dance_entry_t', 'vial_key_override_entry_t'):
    match = re.search(r'typedef struct \{[^}]*\} ' + name + ';', vial)
    if not match:
        raise RuntimeError('Missing production type: ' + name)
    types.append(match.group())
dynamic = (ROOT / 'quantum/dynamic_keymap.c').read_text()
production = [dynamic[dynamic.index('/* TD and KO retain'):dynamic.index('#ifdef VIAL_TAP_DANCE_ENABLE\n#ifdef AK820_COMPACT_TAP_DANCE\nint dynamic_keymap_get_tap_dance')]]
for module in ('tap_dance', 'key_override'):
    source = (ROOT / f'keyboards/ajazz/ak820/ak820_{module}.c').read_text()
    validator = function(source, f'ak820_{module}_valid')
    if module == 'key_override':
        validator = '\n'.join(re.findall(r'^#define (?:basic\([^\n]*|ACTIVATIONS [^\n]*)', source, re.M)) + '\n' + validator
    production.insert(0, '#ifdef AK820_COMPACT_' + module.upper() + '\n' + validator + '\n#endif')
    production.append('#ifdef AK820_COMPACT_' + module.upper())
    for operation in ('get', 'set'):
        production.append(function(dynamic, f'dynamic_keymap_{operation}_{module}'))
    production.append('#endif')

fixture = r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#define AK820_STATE_MEM
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#include "ak820_extensions.h"
#define VIAL_TAP_DANCE_EEPROM_ADDR AK820_TAP_DANCE_ADDR
#define VIAL_KEY_OVERRIDE_EEPROM_ADDR AK820_KEY_OVERRIDE_ADDR
static uint8_t memory[2048], before[2048];
static bool healthy, fail_update, fail_flush;
static unsigned sequence, clears, writes, flushes, reads;
static uintptr_t address;
static void reset(void) { memset(memory,0xa5,sizeof memory); healthy=true; fail_update=fail_flush=false; sequence=clears=writes=flushes=reads=0; }
static bool ak820_nvm_ok(void) { return healthy; }
static void clear_keyboard(void) { assert(sequence==0); sequence=1; ++clears; }
static void ak820_eeprom_update_block_xdata(const void *p,void *a,size_t n) {
    assert(sequence==1); sequence=2; ++writes; address=(uintptr_t)a;
    assert(address+n<=sizeof memory); assert(address/64==(address+n-1)/64);
    memcpy(memory+address,p,n); if(fail_update) healthy=false;
}
static void ak820_nvm_flush(void) { assert(sequence==2); sequence=3; ++flushes; if(fail_flush) healthy=false; }
static void ak820_eeprom_read_block_xdata(void *p,const void *a,size_t n) {
    ++reads; address=(uintptr_t)a; assert(address+n<=sizeof memory); memcpy(p,memory+address,n);
}
'''
cases = r'''
#define TEST(TYPE,NAME,BASE,GOOD,BAD) do { \
 TYPE good=GOOD, bad=BAD, out; \
 assert(sizeof(TYPE)==10); \
 for(unsigned i=0;i<8;++i) { \
  reset(); memcpy(before,memory,sizeof memory); \
  uintptr_t expected=(BASE)+(i<6?i*10:64+(i-6)*10); \
  assert(dynamic_keymap_set_##NAME(i,&good)==0); \
  assert(address==expected && clears==1 && writes==1 && flushes==1 && sequence==3); \
  assert(!memcmp(memory+expected,&good,10)); \
  assert(!memcmp(memory,before,expected)); \
  assert(!memcmp(memory+expected+10,before+expected+10,sizeof memory-expected-10)); \
  memset(&out,0x5a,10); assert(dynamic_keymap_get_##NAME(i,&out)==0); \
  assert(!memcmp(&out,&good,10)); \
  memcpy(memory+expected,&bad,10); assert(dynamic_keymap_get_##NAME(i,&out)==0); \
  TYPE zero={0}; assert(!memcmp(&out,&zero,10)); \
 } \
 for(unsigned i=8;i<256;++i) { \
  reset(); memset(&out,0x5a,10); TYPE keep=out; \
  assert(dynamic_keymap_get_##NAME(i,&out)==-1 && !memcmp(&out,&keep,10)); \
  assert(dynamic_keymap_set_##NAME(i,&good)==-1); \
  assert(!reads && !clears && !writes && !flushes); \
 } \
 reset(); assert(dynamic_keymap_set_##NAME(0,&bad)==-1); assert(!clears&&!writes&&!flushes); \
 reset(); healthy=false; assert(dynamic_keymap_set_##NAME(0,&good)==-1); assert(!clears&&!writes&&!flushes); \
 reset(); fail_update=true; assert(dynamic_keymap_set_##NAME(0,&good)==-1); assert(!healthy&&clears==1&&writes==1&&flushes==1); \
 reset(); fail_flush=true; assert(dynamic_keymap_set_##NAME(0,&good)==-1); assert(!healthy&&clears==1&&writes==1&&flushes==1); \
 assert(dynamic_keymap_set_##NAME(0,&good)==-1); assert(clears==1&&writes==1&&flushes==1); \
 reset(); TYPE empty={0}; assert(dynamic_keymap_set_##NAME(7,&empty)==0); \
} while(0)
int main(void) {
 uint16_t endian=1; assert(*(uint8_t *)&endian==1);
#ifdef AK820_COMPACT_TAP_DANCE
 vial_tap_dance_entry_t td={4,0x0105,224,0,200}, td_bad=td; td_bad.on_tap=1;
#endif
#ifdef AK820_COMPACT_KEY_OVERRIDE
 vial_key_override_entry_t ko={4,0x0105,1,2,0,2,0x87}, ko_bad=ko; ko_bad.trigger=1;
#endif
#ifdef AK820_COMPACT_TAP_DANCE
 TEST(vial_tap_dance_entry_t,tap_dance,AK820_TAP_DANCE_ADDR,td,td_bad);
#endif
#ifdef AK820_COMPACT_KEY_OVERRIDE
 TEST(vial_key_override_entry_t,key_override,AK820_KEY_OVERRIDE_ADDR,ko,ko_bad);
#endif
 const uint16_t invalid[]={1,2,3,165,223,232,255,0x2004,0x5700,0xffff};
 for(unsigned i=0;i<sizeof invalid/sizeof *invalid;++i) {
#ifdef AK820_COMPACT_TAP_DANCE
  td_bad=td;td_bad.on_tap=invalid[i];reset();assert(dynamic_keymap_set_tap_dance(0,&td_bad)==-1);assert(!clears&&!writes&&!flushes);
#endif
#ifdef AK820_COMPACT_KEY_OVERRIDE
  ko_bad=ko;ko_bad.replacement=invalid[i];reset();assert(dynamic_keymap_set_key_override(0,&ko_bad)==-1);assert(!clears&&!writes&&!flushes);
#endif
 }
#ifdef AK820_COMPACT_TAP_DANCE
 for(unsigned field=0;field<5;++field) {
  td_bad=td; ((uint16_t *)&td_bad)[field]=field==4?32768:0x5700;
  reset();assert(dynamic_keymap_set_tap_dance(0,&td_bad)==-1);assert(!clears&&!writes&&!flushes);
 }
#endif
#ifdef AK820_COMPACT_KEY_OVERRIDE
 for(unsigned field=0;field<4;++field) {
  ko_bad=ko;
  if(field==0)ko_bad.trigger=0x0104;
  if(field==1)ko_bad.layers=0x40;
  if(field==2)ko_bad.options=0x40;
  if(field==3)ko_bad.options=0x80;
  reset();assert(dynamic_keymap_set_key_override(0,&ko_bad)==-1);assert(!clears&&!writes&&!flushes);
 }
#endif
 puts("compact TD/KO production storage: 8 padded slots, neighbors, validation, sanitization and NVM failure PASS (host model; no hardware durability)");
 return 0;
}
'''
for modules in (('TAP_DANCE', 'KEY_OVERRIDE'), ('TAP_DANCE',), ('KEY_OVERRIDE',)):
    with tempfile.TemporaryDirectory(prefix='ak820-extension-storage-') as temp:
        work = Path(temp)
        (work / 'storage.c').write_text(fixture + '\n'.join(types + production) + cases)
        subprocess.run(['cc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-Wno-int-to-pointer-cast','-fsanitize=undefined','-fno-sanitize-recover=undefined',
                        *('-DAK820_COMPACT_' + module for module in modules),
                        '-I'+str(ROOT/'keyboards/ajazz/ak820'),str(work/'storage.c'),'-o',str(work/'storage')],check=True)
        print('Enabled: ' + ', '.join(modules), flush=True)
        subprocess.run([str(work/'storage')],check=True)
