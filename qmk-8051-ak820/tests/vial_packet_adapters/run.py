#!/usr/bin/env python3
"""Compare production compact packet adapters with the prior copy adapters.

Native CPU/NVM model only. No device access or firmware-size qualification.
"""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]

def block(source, start):
    pos = source.index(start)
    end = source.index('{', pos) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[pos:end]

def function(source, name):
    match = re.search(r'^(?:static )?(?:int|bool|uint16_t|void) ' + name + r'\([^\n]*\) \{', source, re.M)
    assert match, name
    return block(source, match.group())

vial = (ROOT / 'quantum/vial.c').read_text()
header = (ROOT / 'quantum/vial.h').read_text()
dynamic = (ROOT / 'quantum/dynamic_keymap.c').read_text()
modules = ('tap_dance', 'key_override')
parts = []
for module in modules:
    typ = f'vial_{module}_entry_t'
    declaration = re.search(r'typedef struct \{[^}]*\} ' + typ + ';', header).group()
    parts.append('#ifdef __SDCC_mcs51\n#pragma pack(push, 1)\n#endif\n' + declaration +
                 '\n#ifdef __SDCC_mcs51\n#pragma pack(pop)\n#endif')
    source = (ROOT / f'keyboards/ajazz/ak820/ak820_{module}.c').read_text()
    validator = function(source, f'ak820_{module}_valid')
    if module == 'key_override':
        validator = '\n'.join(re.findall(r'^#define (?:basic\([^\n]*|ACTIVATIONS [^\n]*)', source, re.M)) + '\n' + validator
    parts.append('#ifdef AK820_COMPACT_' + module.upper() + '\n' + validator + '\n#endif')
parts.append(dynamic[dynamic.index('/* TD and KO retain'):dynamic.index('#ifdef VIAL_TAP_DANCE_ENABLE\n#ifdef AK820_COMPACT_TAP_DANCE\nint dynamic_keymap_get_tap_dance')])
for module in modules:
    parts.append('#ifdef AK820_COMPACT_' + module.upper())
    for op in ('get', 'set'):
        parts.append(function(dynamic, f'dynamic_keymap_{op}_{module}'))
    parts.append('#endif')
# Use the production KO reload and cancel, including its private cache writes.
ko = (ROOT / 'keyboards/ajazz/ak820/ak820_key_override.c').read_text()
parts.append('''#ifdef AK820_COMPACT_KEY_OVERRIDE
#define NONE 255
#define VIAL_KEY_OVERRIDE_ENTRIES 8
static vial_key_override_entry_t entries[8];
static uint8_t source, active, previous_mods;
static bool blocked, hidden;
'''+function(ko, 'ak820_key_override_cancel')+'\n'+function(ko, 'ak820_key_override_reload')+'''
static void reload_key_override(void) { trace(5,0,0,0); ak820_key_override_reload(); }
#endif
#define reload_tap_dance() trace(6,0,0,0)
''')
# Prior parser: fixed local zero GET and local copy SET, no compact firewall.
reference = []
production = []
for module in modules:
    reference.append('#ifdef AK820_COMPACT_' + module.upper())
    production.append('#ifdef AK820_COMPACT_' + module.upper())
    for op in ('get', 'set'):
        name = f'dynamic_vial_{module}_{op}'
        adapter = block(vial, f'case {name}: {{')
        guard = '#if defined(AK820_COMPACT_' + module.upper() + ') && defined(__SDCC_mcs51)'
        assert guard in adapter, f'{name}: direct adapter must be target guarded'
        assert f'_Alignof(vial_{module}_entry_t) == 1' in adapter, name
        production.append(adapter)
        if op == 'get':
            body = f'''vial_{module}_entry_t entry = {{0}};
msg[0] = dynamic_keymap_get_{module}(idx, &entry);
memcpy(msg+1, &entry, sizeof entry);'''
        else:
            body = f'''vial_{module}_entry_t entry;
memcpy(&entry, msg+4, sizeof entry);
msg[0] = dynamic_keymap_set_{module}(idx, &entry);
'''+('reload_tap_dance();' if module == 'tap_dance' else 'if (!msg[0]) reload_key_override();')
        reference.append(f'case {name}: {{ uint8_t idx=msg[3]; {body}\nbreak; }}')
    reference.append('#endif')
    production.append('#endif')
for name, cases in [('reference', reference), ('production', production)]:
    parts.append(f'static void {name}(uint8_t *msg) {{ switch(msg[2]) {{\n'+'\n'.join(cases)+'\n} }')
fixture = r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#define AK820_STATE_MEM
#define KC_A 4
#define KC_EXSEL 164
#define KC_LEFT_CTRL 224
#define KC_RIGHT_GUI 231
#include "ak820_extensions.h"
enum { dynamic_vial_tap_dance_get=1, dynamic_vial_tap_dance_set,
       dynamic_vial_key_override_get, dynamic_vial_key_override_set };
static uint8_t memory[2048], packet[32];
static bool healthy, fail_update, fail_flush;
struct event { unsigned kind, address, size; uint8_t bytes[10]; };
static struct event events[64]; static unsigned count;
static void trace(unsigned kind, uintptr_t address, unsigned size, const void *p) {
 assert(count<64); struct event *e=&events[count++];
 memset(e,0,sizeof *e); e->kind=kind; e->address=address; e->size=size;
 if(p) memcpy(e->bytes,p,size);
}
static bool ak820_nvm_ok(void) { trace(7,healthy,0,0); return healthy; }
static void clear_keyboard(void) { trace(1,0,0,0); }
static void ak820_eeprom_read_block_xdata(void *p,const void *a,size_t n) {
 uintptr_t address=(uintptr_t)a; assert(address+n<=sizeof memory);
 memcpy(p,memory+address,n); trace(2,address,n,p);
}
static void ak820_eeprom_update_block_xdata(const void *p,void *a,size_t n) {
 uintptr_t address=(uintptr_t)a; assert(address+n<=sizeof memory);
 trace(3,address,n,p); memcpy(memory+address,p,n); if(fail_update)healthy=false;
}
static void ak820_nvm_flush(void) { trace(4,0,0,0); if(fail_flush)healthy=false; }
'''
cases = r'''
static void reset(unsigned command,unsigned index,const uint8_t *row,unsigned fault,unsigned stored) {
 memset(memory,stored,sizeof memory); memset(events,0,sizeof events); count=0;
 healthy=fault!=1; fail_update=fault==2; fail_flush=fault==3;
 for(unsigned i=0;i<32;++i) packet[i]=(uint8_t)(0xa0+i);
 packet[0]=0xfe; packet[1]=0x0d; packet[2]=command; packet[3]=index;
 memcpy(packet+4,row,10);
 if(stored==4 && index<8 && command>=1 && command<=4) {
  unsigned base=command<=2?AK820_TAP_DANCE_ADDR:AK820_KEY_OVERRIDE_ADDR;
  unsigned offset=index<6?index*10:64+(index-6)*10;
  memcpy(memory+base+offset,row,10);
 }
}
int main(void) {
 unsigned runs=0;
 const uint8_t rows[][10]={
  {0}, {4,0,5,1,224,0,0,0,200,0}, {4,0,5,1,1,0,2,0,2,0x87},
  {1,0,0,0,0,0,0,0,0,0}, {4,0,4,0x57,1,0,0,0,0,0x80},
  {4,0,5,1,0x40,0,2,0,2,0x87}, {4,0,5,1,1,0,2,0,2,0x40},
  {4,0,5,1,1,0,2,0,2,0x80}, {4,1,5,1,1,0,2,0,2,0x87},
  {4,0,5,1,1,0,2,0,2,0x07}, {4,0,5,1,224,0,0,0,0xff,0x7f},
  {4,0,5,1,224,0,0,0,0,0x80}
 };
 for(unsigned command=0;command<=5;++command) {
#ifndef AK820_COMPACT_TAP_DANCE
  if(command==1 || command==2)continue;
#endif
#ifndef AK820_COMPACT_KEY_OVERRIDE
  if(command==3 || command==4)continue;
#endif
  for(unsigned index=0;index<256;++index)
   for(unsigned row=0;row<sizeof rows/sizeof *rows;++row)
    for(unsigned fault=0;fault<4;++fault)
     for(unsigned stored=0;stored<3;++stored) {
      uint8_t reply[32], persisted[2048]; struct event expected[64]; unsigned expected_count;
      reset(command,index,rows[row],fault,stored==0?0:stored==1?0xa5:4);
      reference(packet); memcpy(reply,packet,32); memcpy(persisted,memory,2048);
      memcpy(expected,events,sizeof events); expected_count=count; bool expected_health=healthy;
      reset(command,index,rows[row],fault,stored==0?0:stored==1?0xa5:4);
      production(packet);
      assert(!memcmp(reply,packet,32)); assert(!memcmp(persisted,memory,2048));
      assert(expected_count==count && !memcmp(expected,events,count*sizeof *events));
      assert(expected_health==healthy); ++runs;
     }
 }
 printf("PASS: %u differential cases; complete 32-byte replies, NVM bytes, read/write/clear/flush/reload/fault traces\n",runs);
}
'''
for target in ('sdcc-byte-alignment-model', 'native-fallback'):
 for enabled in (('TAP_DANCE',), ('KEY_OVERRIDE',), ('TAP_DANCE', 'KEY_OVERRIDE')):
    with tempfile.TemporaryDirectory(prefix='vial-packet-') as temp:
        work=Path(temp); (work/'test.c').write_text(fixture+'\n'.join(parts)+cases)
        flags = ['-D__SDCC_mcs51'] if target == 'sdcc-byte-alignment-model' else []
        command = ['cc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-Wno-int-to-pointer-cast',
                   '-fsanitize=undefined','-fno-sanitize-recover=undefined', *flags,
                   *('-DAK820_COMPACT_'+m for m in enabled),
                   '-I'+str(ROOT/'keyboards/ajazz/ak820'),str(work/'test.c'),'-o',str(work/'test')]
        subprocess.run(command,check=True)
        # Inspect the actual preprocessed cases: no packet-to-structure cast may
        # survive on the native fallback, regardless of runtime test outcomes.
        preprocessed = subprocess.check_output(command[:1] + ['-E', '-P'] +
            [arg for arg in command[1:-2] if not arg.startswith('-fsanitize=')], text=True)
        for module in modules:
            if module.upper() not in enabled:
                continue
            for op in ('get', 'set'):
                adapter = block(function(preprocessed, 'production'), f'case dynamic_vial_{module}_{op}: {{')
                packet_cast = re.search(r'\(\s*(?:const )?vial_\w+_entry_t\s*\*\)\s*&msg', adapter)
                assert bool(packet_cast) == bool(flags), (target, module, op)
        print('Mode: '+target+'; enabled: '+', '.join(enabled),flush=True)
        subprocess.run([str(work/'test')],check=True)
