from pathlib import Path
import re
import argparse, subprocess, hashlib, json
HERE=Path(__file__).resolve().parent
R=HERE.parents[1]/'qmk-8051-ak820'
parser=argparse.ArgumentParser(description='Compare production direct action backend against the frozen pre-change C oracle.')
parser.add_argument('--output', type=Path, required=True)
args=parser.parse_args()
W=args.output.resolve(); W.mkdir(parents=True,exist_ok=True)
def fn(p,n):
 t=(R/p).read_text();m=re.search(r'^.*\b'+n+r'\([^\n]*\) \{',t,re.M);a=m.start();i=t.index('{',a)+1;d=1
 while d:
  if t[i]=='{':d+=1
  elif t[i]=='}':d-=1
  i+=1
 return t[a:i]
pre='''#include <stdint.h>
#include <stdbool.h>
#include "keycode.h"
#include "quantum_keycodes.h"
#include "action_code.h"
#define AK820_BOARD
#define NO_ACTION_TAPPING
#define NO_ACTION_ONESHOT
#define AK820_COMPACT_TAPPING
#define EXTRAKEY_ENABLE
#define LAYER_STATE_8BIT
#define NO_DEBUG
#define REPEAT_KEY_ENABLE
#define AK820_KEYPOS_VALUE(k) (k)
#ifdef __SDCC_mcs51
#define AK820_RECORD_MEM __xdata
#else
#define AK820_RECORD_MEM
#endif
#define ac_dprintf(...)
#define keycode_config(k) (k)
#define mod_config(k) (k)
#define TAP_HOLD_CAPS_DELAY 0
#define TAP_CODE_DELAY 0
typedef uint8_t layer_state_t;
typedef struct { struct { uint16_t key; bool pressed; } event; uint16_t keycode; } keyrecord_t;
'''
report=(R/'tmk_core/protocol/report.h').read_text()
pre+='\n'.join(re.search(r'enum '+name+r' \{.*?\n\};',report,re.S).group(0) for name in ['consumer_usages','desktop_usages'])+'\n'
pre+=fn('tmk_core/protocol/report.h','KEYCODE2SYSTEM')+'\n'+fn('tmk_core/protocol/report.c','KEYCODE2CONSUMER')+'\n'
leaves={'add_owned_mods':8,'add_owned_weak_mods':8,'del_owned_mods':8,'del_owned_weak_mods':8,'register_code':8,'unregister_code':8,'register_mods':8,'unregister_mods':8,'default_layer_and':8,'default_layer_or':8,'default_layer_xor':8,'default_layer_set':8,'layer_and':8,'layer_or':8,'layer_xor':8,'layer_state_set':8,'layer_hold_on':8,'layer_hold_off':8,'layer_off':8,'layer_on':8,'layer_move':8,'wait_ms':16,'host_system_send':16,'host_consumer_send':16,'led_set':8}
proto='void send_keyboard_report(void); void layer_clear(void); uint8_t host_keyboard_leds(void); void owned_usage_key(uint8_t k,bool p); void register_mouse(uint8_t k,bool p);\n'+''.join(f'void {n}(uint{b}_t v);\n' for n,b in leaves.items())
oracle=(HERE/'fixtures/oracle.c').read_text()
direct='static uint16_t resolved; uint16_t ak820_resolve_key(uint16_t position,bool pressed) {return resolved;}\n'+fn('quantum/action.c','process_record_handler')+'\nvoid backend(keyrecord_t AK820_RECORD_MEM *r,uint16_t keycode){ resolved=keycode; process_record_handler(r); }\n'
for name,body in [('oracle',oracle),('direct',direct)]: (W/(name+'.c')).write_text(pre+proto+body)
host='''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned trace[64],length;
static void emit(unsigned id,unsigned v) {trace[length++]=(id<<16)|v;}
'''
for i,(n,b) in enumerate(leaves.items(),1):
 host+=f'void {n}(uint{b}_t v) {{'+('if(!v)return;' if n in ('register_code','unregister_code') else '')+f'emit({i},v);}}\n'
host+='''void send_keyboard_report(void){emit(40,0);} void layer_clear(void){emit(41,0);} uint8_t host_keyboard_leds(void){return 3;} void owned_usage_key(uint8_t k,bool p){emit(42,k|((unsigned)p<<8));} void register_mouse(uint8_t k,bool p){emit(43,k|((unsigned)p<<8));}
'''
# Rename oracle backend only, so function names and types shared.
both=pre+proto+oracle.replace('void backend(','void oracle_backend(')+direct+host+'''int main(void) {unsigned k,p,v,cases=0;keyrecord_t r;unsigned expected[64],n;for(k=0;k<65536;k++)for(p=0;p<2;p++)for(v=0;v<4;v++){r.keycode=v==0?k:v==1?0:v==2?KC_SYSTEM_POWER:KC_AUDIO_MUTE;r.event.pressed=p;length=0;oracle_backend(&r,r.keycode?r.keycode:k);n=length;memcpy(expected,trace,n*sizeof(*trace));length=0;backend(&r,k);if(n!=length||memcmp(expected,trace,n*sizeof(*trace))){fprintf(stderr,"mismatch %04x %u expected=%u actual=%u\\n",k,p,n,length);return 1;}cases++;}printf("PASS %u exhaustive keycode/edge trace comparisons\\n",cases);return 0;}'''
(W/'differential.c').write_text(both)

command=['gcc','-std=c11','-O1','-fsanitize=undefined','-fno-sanitize=shift-base','-fno-sanitize-recover=all',*['-I'+str(R/d) for d in ['quantum','quantum/keymap_extras','quantum/sequencer']],str(W/'differential.c'),'-o',str(W/'differential')]
subprocess.run(command,check=True)
subprocess.run([str(W/'differential')],check=True)

inputs=[R/'quantum/action.c', HERE/'fixtures/oracle.c',Path(__file__)]
(W/'result.json').write_text(json.dumps({'pass':True,'cases':524288,'comparison':'Ordered leaf calls, arguments and report boundaries; all 65536 keycodes, both edges, four explicit/cache record variants','limits':'Native C model only; unchanged leaf implementations, arbitrary initial states implied by identical leaf traces. No 8051 execution, linked stack proof, full-module or physical qualification. Native oracle signed shift-base sanitizer disabled because high invalid layers promote 8-bit layer masks to signed 32-bit int.','source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}},indent=2)+'\n')
