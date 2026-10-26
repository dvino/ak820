// SPDX-License-Identifier: GPL-2.0-or-later
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "action.h"
#include "action_util.h"
#include "action_layer.h"
#include "keymap_common.h"
#include "quantum_keycodes.h"
#include "keycode_config.h"
#include "report.h"
#include "host.h"
#include "repeat_key.h"
#include "process_repeat_key.h"
#include "tri_layer.h"
#include "process_tri_layer.h"
#include "qmk_settings.h"
#include "ak820_tapping.h"
#include "ak820_combo.h"
void dynamic_keymap_macro_send(uint8_t id);
static vial_combo_entry_t fixture_combos[VIAL_COMBO_ENTRIES];
int dynamic_keymap_get_combo(uint8_t i, vial_combo_entry_t *entry) {*entry=fixture_combos[i];return 0;}
#include "caps_word.h"
#include "process_caps_word.h"
#include "timer.h"
#include "send_string.h"
#define VIAL_MATRIX_MAGIC 240
#define VIAL_MACRO_EXT_TAP 5
#define VIAL_MACRO_EXT_DOWN 6
#define VIAL_MACRO_EXT_UP 7
#define DYNAMIC_KEYMAP_MACRO_DELAY 0
#define AK820_XDATA
typedef struct {uint8_t terminated,arguments;} macro_parse_t;
bool vial_unlock_in_progress;
uint16_t g_vial_magic_keycode_override;
static uint8_t macro_bytes[8192];
static uint16_t macro_length;
static bool macro_available;
uint8_t eeprom_read_byte(const uint8_t *p) {uintptr_t addr=(uintptr_t)p;assert(addr>=0x800&&addr<0x800+sizeof(macro_bytes));return macro_bytes[addr-0x800];}
bool ak820_macro_ready(void) {return macro_available;}
uint16_t ak820_macro_length(void) {return macro_length;}
void vial_keycode_down(uint16_t);
void vial_keycode_up(uint16_t);
void vial_keycode_tap(uint16_t);
#define dprintf(...) ((void)0)
#define NUM_ENCODERS 1
static uint16_t now;
static uint16_t map[6][MATRIX_ROWS][MATRIX_COLS], enc[6][2];
static uint8_t log_reports[2048][sizeof(report_keyboard_t)];
volatile uint8_t keyboard_protocol = 1;
static unsigned log_count, systems, consumers;
static bool trace_mode, cancel_during_pre_release;
static uint16_t last_system,last_consumer;
static struct {uint8_t ns;uint16_t usage;} extra_log[2048];
static unsigned extra_count;
keymap_config_t keymap_config;
bool disable_action_cache;
uint16_t timer_read(void) { return now; }
uint16_t keycode_config(uint16_t k) { return k; }
uint8_t mod_config(uint8_t k) { return k; }
uint16_t keymap_key_to_keycode(uint8_t layer,keypos_t key) {
 if(key.row==VIAL_MATRIX_MAGIC&&key.col==VIAL_MATRIX_MAGIC)return g_vial_magic_keycode_override;
 if (key.row==KEYLOC_ENCODER_CW || key.row==KEYLOC_ENCODER_CCW) return enc[layer][key.row==KEYLOC_ENCODER_CCW];
 return map[layer][key.row][key.col];
}
uint16_t ak820_keycode_at(uint8_t layer, uint16_t position) {
 keypos_t key={.row=position>>8,.col=position};
 return keymap_key_to_keycode(layer,key);
}
void host_keyboard_send(report_keyboard_t *r) { assert(log_count<2048);memcpy(log_reports[log_count++],r,sizeof(*r)); if(trace_mode){printf("H %u",now);for(unsigned i=0;i<8;i++)printf(" %u",r->raw[i]);puts("");} }
void host_system_send(uint16_t x) {assert(extra_count<2048);extra_log[extra_count++]=(typeof(extra_log[0])){0,x};last_system=x;++systems;}
void host_consumer_send(uint16_t x) {assert(extra_count<2048);extra_log[extra_count++]=(typeof(extra_log[0])){1,x};last_consumer=x;++consumers;}
void register_mouse(uint8_t x,bool p) { (void)x;(void)p; }
bool process_action_kb(keyrecord_t *r) { (void)r; return true; }
bool command_proc(uint8_t x) { (void)x;return false; }
bool process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r;return true; }
bool pre_process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;if(cancel_during_pre_release&&!r->event.pressed){cancel_during_pre_release=false;clear_keyboard();}return true; }
void post_process_record_kb(uint16_t k,keyrecord_t *r) { (void)k;(void)r; }
void eeconfig_init(void) {}
void wait_ms(uint16_t x) { now+=x; }
void led_set(uint8_t x) { (void)x; }
uint8_t host_keyboard_leds(void) {return 0;}
uint16_t get_record_keycode(keyrecord_t *,bool);
uint16_t get_event_keycode(keyevent_t,bool);
bool pre_process_record_quantum(keyrecord_t *);
bool process_record_quantum_helper(uint16_t,keyrecord_t *);
/* PRODUCTION */
static void event(uint8_t id,bool down,uint16_t time) {
 keyevent_t e={0};e.key.row=id/MATRIX_COLS;e.key.col=id%MATRIX_COLS;e.type=KEY_EVENT;e.time=now=time;e.pressed=down;action_exec(e);
}
static void tick(uint16_t time) { keyevent_t e={0};e.type=TICK_EVENT;e.time=now=time;action_exec(e); }
static void reset(void) {
 clear_keyboard();caps_word_off();memset(source_state,0,sizeof(source_state));
 memset(fixture_combos,0,sizeof(fixture_combos));ak820_combo_reload();
 ak820_macro_primitive=false;repeat_key_cancel();set_tri_layer_layers(1,2,3);layer_clear();default_layer_set(0);memset(map,0,sizeof(map));memset(enc,0,sizeof(enc));log_count=extra_count=0;
}
static void assign(uint8_t id,uint16_t code) {for(unsigned l=0;l<6;l++)map[l][id/MATRIX_COLS][id%MATRIX_COLS]=code;}
static void encoder(bool ccw,bool down,uint16_t time) {
 keyevent_t e={0};e.key.row=ccw?KEYLOC_ENCODER_CCW:KEYLOC_ENCODER_CW;e.type=ccw?ENCODER_CCW_EVENT:ENCODER_CW_EVENT;e.time=now=time;e.pressed=down;action_exec(e);
}
static void macro_load(const uint8_t *body,unsigned length) {
 assert(length+16<=sizeof(macro_bytes));memcpy(macro_bytes,body,length);memset(macro_bytes+length,0,16);macro_length=length+16;macro_available=true;
 macro_parse_t state={0};for(unsigned i=0;i<macro_length;i++)assert(parse_byte(&state,macro_bytes[i]));assert(state.terminated==16&&!state.arguments);
}
static void macro_one(uint8_t op,uint16_t code) {
 uint8_t body[4]={1,op,code&255,code>>8};macro_load(body,op>=5?4:3);dynamic_keymap_macro_send(0);
}
static uint16_t usage(uint8_t key) {return key<KC_AUDIO_MUTE?KEYCODE2SYSTEM(key):KEYCODE2CONSUMER(key);}
static uint16_t current_usage(uint8_t key) {return key<KC_AUDIO_MUTE?last_system:last_consumer;}
static void clean(void) {for(unsigned i=0;i<USAGE_COUNT;i++)assert(!usage_refs[i]);assert(!usage_lengths[0]&&!usage_lengths[1]);for(unsigned i=0;i<=KC_EXSEL;i++)assert(!key_refs[i]);assert(!get_mods()&&!get_weak_mods()&&!layer_state&&pending==NONE);for(unsigned i=0;i<SOURCES;i++)assert(!(source_state_get(i)&(SOURCE_ACTIVE|SOURCE_HELD)));}
int main(int argc,char **argv) {
 assert(sizeof(source_state)==SOURCE_STATE_BYTES);
 const uint8_t expected_pattern[4]={0,8,16,31};uint8_t expected[SOURCES];
 for(unsigned i=0;i<SOURCES;i++){expected[i]=expected_pattern[i%4];source_state_set(i,expected[i]);}
 for(unsigned i=0;i<SOURCES;i++)assert(source_state_get(i)==expected[i]);
 assert(expected[127]==31&&expected[128]==0&&expected[129]==8);
 if(argc>1) {
  char op;unsigned a,b,c;reset();trace_mode=true;
  while(scanf(" %c",&op)==1) {
   if(op=='M'){assert(scanf("%u %x",&a,&b)==2);assign(a,b);}
   else if(op=='E'){assert(scanf("%u %u %u",&a,&b,&c)==3);event(b,c,a);}
   else if(op=='T'){assert(scanf("%u",&a)==1);tick(a);}
   else return 2;
  }
  printf("F %u %u\n",get_mods()|get_weak_mods(),layer_state);return 0;
 }

 /* Layer-tap macro: release fires once; hold switches layer only. */
 { const uint8_t body[]={1,SS_TAP_CODE,KC_A};
   reset(); macro_load(body,sizeof(body)); assign(0,0x41f0); event(0,1,10);
   assert(!key_refs[KC_A]&&!log_count); event(0,0,20); assert(log_count==2&&log_reports[0][2]==KC_A&&log_reports[1][2]==0); clean();
   reset(); macro_load(body,sizeof(body)); assign(0,0x41f0); event(0,1,10); tick(210);
   assert(layer_state==2&&!log_count); event(0,0,220); assert(!layer_state&&!log_count); clean();
   reset(); macro_load(body,sizeof(body)); assign(0,0x41f0); assign(1,0x7c73); assign(2,KC_A);
   event(0,1,10); event(1,1,20); assert(layer_state==2); event(1,0,21); event(2,1,22);
   assert(is_caps_word_on()&&key_refs[KC_A]); event(2,0,23); event(0,0,24); caps_word_off(); clean();
   reset(); macro_load(body,sizeof(body)); enc[0][0]=0x43f0; encoder(false,1,10); encoder(false,0,20);
   assert(!layer_state&&!log_count); clean();
   reset(); macro_load(body,sizeof(body)); enc[0][0]=0x43f0; encoder(false,1,10); tick(210);
   assert(!layer_state&&!log_count); encoder(false,0,220); assert(!layer_state&&!log_count); clean();
   for(unsigned i=0;i<3;i++) {
    uint16_t start=i==2?65500:100,elapsed=i==1?200:(i==2?100:199);
    reset();macro_load(body,sizeof(body));assign(0,0x41f0);event(0,1,start);tick((start+elapsed)&65535);
    if(elapsed==200) assert(layer_state==2&&!log_count);
    event(0,0,(start+elapsed)&65535);
    if(elapsed==200) assert(!layer_state&&!log_count);
    else assert(log_count==2&&log_reports[0][2]==KC_A&&log_reports[1][2]==0);
    clean();
   }
   reset();macro_load(body,sizeof(body));assign(0,0x41f0);event(0,1,10);clear_keyboard();event(0,0,20);assert(!log_count&&!layer_state);clean();
   reset();macro_load(body,sizeof(body));assign(0,0x41f0);event(0,1,10);vial_unlock_in_progress=true;ak820_tapping_cancel();event(0,0,20);vial_unlock_in_progress=false;assert(!log_count&&!layer_state);clean();
 }

#ifdef AK820_COMPACT_ONESHOT
 /* Every encoded modifier, including the right-hand group, uses owners. */
 for(unsigned mask=0;mask<32;mask++) {
  reset();assign(0,0x52a0|mask);assign(1,KC_A);assign(2,KC_B);
  unsigned mods=(mask&16)?((mask&15)<<4):mask;
  event(0,1,10);event(0,0,20);assert(get_mods()==mods);
  event(1,1,30);event(2,1,40);event(1,0,50);assert(!get_mods()&&key_refs[KC_B]);event(2,0,60);clean();
 }
 /* Queued masks combine; a repeated bit acquires no duplicate owner. */
 reset();assign(0,0x52a2);assign(1,0x52a3);assign(2,KC_A);event(0,1,1);event(0,0,2);event(1,1,3);event(1,0,4);assert(get_mods()==3);event(0,1,5);event(0,0,6);assert(get_mods()==3);event(2,1,7);event(2,0,8);clean();
 /* Modifier and layer controls leave the queue armed for a letter. */
 reset();assign(0,0x52a2);assign(1,KC_LCTL);assign(2,0x5221);assign(3,KC_A);event(0,1,1);event(0,0,2);event(1,1,3);event(1,0,4);event(2,1,5);event(2,0,6);assert(get_mods()==2&&!layer_state);event(3,1,7);assert(get_mods()==2);event(3,0,8);clean();
 /* MT/LT taps consume the queue through their resolved basic key. Holds
  * leave it armed until an actual key arrives and keep their own owners. */
 for(unsigned lt=0;lt<2;lt++) {
  reset();assign(0,0x52a2);assign(1,lt?0x4104:0x2104);assign(2,KC_B);event(0,1,1);event(0,0,2);event(1,1,10);event(1,0,20);assert(!get_mods()&&!layer_state);bool emitted_shift_a=false;for(unsigned i=0;i<log_count;i++)if(log_reports[i][0]==2&&log_reports[i][2]==KC_A)emitted_shift_a=true;assert(emitted_shift_a);clean();
  reset();assign(0,0x52a2);assign(1,lt?0x4104:0x2104);assign(2,KC_B);event(0,1,1);event(0,0,2);event(1,1,10);tick(210);assert(get_mods()==(lt?2:3));assert(layer_state==(lt?2:0));event(2,1,220);event(2,0,230);assert(get_mods()==(lt?0:1));assert(layer_state==(lt?2:0));event(1,0,240);clean();
 }
 /* Clear/unlock cleanup blocks late physical releases and cannot arm. */
 reset();assign(0,0x52a2);assign(1,KC_A);event(0,1,10);clear_keyboard();event(0,0,20);assert(!get_mods());event(1,1,30);assert(!get_mods());event(1,0,40);clean();
 reset();assign(0,0x52a2);assign(1,KC_A);event(0,1,10);event(0,0,20);event(1,1,30);clear_keyboard();event(1,0,40);assert(!get_mods());event(1,1,50);assert(!get_mods());event(1,0,60);clean();
 /* Encoder directions use distinct accepted source identities. */
 for(unsigned dir=0;dir<2;dir++) {reset();enc[0][dir]=0x52a2;assign(1,KC_A);encoder(dir,1,10);encoder(dir,0,20);assert(get_mods()==2);event(1,1,30);event(1,0,40);clean();}
 /* Busy fallback persists if the consuming key is released first. */
 reset();assign(0,0x52a2);assign(1,KC_A);assign(2,0x52a1);event(0,1,1);event(0,0,2);event(1,1,3);event(2,1,4);event(1,0,5);assert(get_mods()==1);event(2,0,6);assert(!get_mods());event(1,1,7);assert(!get_mods());event(1,0,8);clean();
 /* A held OSM is ordinary held state and must not arm after a chord. */
 reset();assign(0,0x52a2);assign(1,KC_A);event(0,1,10);event(1,1,20);event(1,0,30);event(0,0,40);clean();
 /* A physical owner survives consumption of the matching One Shot. */
 reset();assign(0,0x52a2);assign(1,KC_A);assign(2,KC_LSFT);event(2,1,1);event(0,1,10);event(0,0,20);event(1,1,30);event(1,0,40);assert(get_mods()==2);event(2,0,50);clean();
 /* While a consuming key is down a new OSM holds but does not arm. */
 reset();assign(0,0x52a2);assign(1,KC_A);assign(2,0x52a1);assign(3,KC_B);event(0,1,1);event(0,0,2);event(1,1,3);event(2,1,4);assert(get_mods()==3);event(2,0,5);assert(get_mods()==2);event(1,0,6);event(3,1,7);assert(!get_mods());event(3,0,8);clean();
 reset();assign(0,0x52a2);assign(1,KC_A);event(0,1,10);event(0,0,20);clear_keyboard();event(1,1,30);assert(!get_mods());event(1,0,40);clean();
 reset();assign(0,0x52a2);assign(1,KC_A);assign(2,QK_REPEAT_KEY);event(0,1,10);event(0,0,20);event(1,1,30);event(1,0,40);event(2,1,50);assert(get_mods()==0&&get_weak_mods()==2&&key_refs[KC_A]);event(2,0,60);clean();
 reset();assign(0,0x52a2);assign(1,KC_A);caps_word_on();event(0,1,10);event(0,0,20);event(1,1,30);assert(get_mods()==2&&get_weak_mods()==2);event(1,0,40);caps_word_off();clean();
 reset();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,0x52a2);assign(1,KC_A);assign(2,KC_B);event(0,1,1);event(0,0,2);event(1,1,10);event(2,1,20);assert(get_mods()==2&&key_refs[KC_C]);event(1,0,30);event(2,0,40);clean();
#endif
 for(unsigned mask=0;mask<32;mask++) {
  reset();assign(0,0x2004|(mask<<8));event(0,1,100);assert(!get_mods());tick(299);assert(!get_mods());tick(300);assert(get_mods()==((mask&16)?((mask&15)<<4):mask));event(0,0,301);clean();
  reset();assign(0,0x2004|(mask<<8));event(0,1,100);event(0,0,299);assert(log_count==2&&log_reports[0][2]==4&&!log_reports[1][2]);clean();
 }
 for(unsigned l=0;l<6;l++) {reset();assign(0,0x4004|(l<<8));event(0,1,65500);tick(163);assert(!layer_state);tick(164);assert(layer_state==(1u<<l));event(0,0,165);clean();}
 reset();assign(0,0x2204);assign(1,0x2205);assign(2,KC_LSFT);event(2,1,10);event(0,1,20);event(1,1,30);assert(get_mods()==2);tick(230);event(0,0,240);assert(get_mods()==2);event(2,0,250);assert(get_mods()==2);event(1,0,260);clean();
 reset();assign(0,0x2204);assign(1,KC_LSFT);event(1,1,10);event(0,1,20);event(1,0,30);event(0,0,40);assert(log_reports[log_count-2][0]==0);clean();
 reset();assign(0,0x4104);assign(1,5);map[1][0][1]=6;event(0,1,10);event(1,1,20);assert(actual_keyboard_report.raw[2]==6);event(1,0,30);event(0,0,40);clean();
 reset();assign(0,0x4104);event(0,1,10);assign(0,KC_LSFT);tick(210);assert(layer_state==2);event(0,0,220);clean();
 reset();assign(0,0x4104);event(0,1,10);tick(210);layer_invert(1);event(0,0,220);assert(layer_state==2);layer_clear();clean();
 reset();assign(0,0x4104);event(0,1,10);tick(210);layer_move(2);assert(layer_state==14);event(0,0,220);assert(layer_state==4);layer_clear();clean();
 reset();assign(0,0x2204);event(0,1,10);clear_keyboard();tick(300);event(0,0,310);assert(!get_mods()&&!log_count);event(0,1,320);tick(520);assert(get_mods()==2);event(0,0,530);clean();
 for(unsigned byte=0;byte<256;byte++) {
  if (!(byte<=1||(byte>=4&&byte<=0xc2)||(byte>=0xe0&&byte<=0xe7)))continue;
  reset();assign(0,0x2200|byte);unsigned ns=systems,nc=consumers;event(0,1,10);event(0,0,20);clean();
  if(byte>=0xa5&&byte<=0xa7)assert(systems==ns+2&&!last_system);
  if(byte>=0xa8&&byte<=0xc2)assert(consumers==nc+2&&!last_consumer);
  if(byte>=4&&byte<=0xa4)assert(log_count==2&&log_reports[0][2]==byte&&!log_reports[1][2]);
  if(byte>=0xe0&&byte<=0xe7)assert(log_count==2&&log_reports[0][0]==(1u<<(byte-0xe0))&&!log_reports[1][0]);
 }
 reset();assign(0,0x2204);event(0,1,10);event(0,0,20);event(0,1,30);tick(230);assert(get_mods()==2);event(0,0,240);clean();
 for(unsigned dir=0;dir<2;dir++) {
  reset();enc[0][dir]=0x2204;encoder(dir,1,10);encoder(dir,0,11);assert(log_count==2&&log_reports[0][2]==4);clean();
 }
 reset();assign(0,0x4104);enc[1][0]=0x2205;event(0,1,10);encoder(0,1,20);assert(layer_state==2);encoder(0,0,21);assert(log_reports[0][2]==5);event(0,0,30);clean();
 reset();for(unsigned l=0;l<6;l++){enc[l][0]=0x2204;enc[l][1]=0x2105;}
 for(unsigned i=0;i<100;i++){encoder(i&1,1,2*i);encoder(i&1,0,2*i+1);}clean();assert(log_count==200);
 reset();assign(0,0x2204);assign(1,QK_REPEAT_KEY);event(0,1,10);event(0,0,20);assert(get_last_keycode()==4);event(1,1,30);assert(actual_keyboard_report.raw[2]==4);event(1,0,40);clean();
 reset();assign(0,0x2204);assign(1,QK_REPEAT_KEY);assign(2,5);event(2,1,1);event(2,0,2);event(0,1,10);tick(210);assert(get_last_keycode()==5);event(1,1,220);assert(actual_keyboard_report.raw[2]==5&&get_mods()==2);event(0,0,230);assert(!get_mods());event(1,0,240);clean();
 reset();assign(0,0x0204);assign(1,0x0205);event(0,1,10);event(1,1,20);assert(get_weak_mods()==2);clear_weak_mods();set_weak_mods(0);assert(get_weak_mods()==2);event(0,0,30);assert(get_weak_mods()==2);event(1,0,40);clean();
 reset();assign(0,0x5042);assign(1,0x4104);event(0,1,10);event(1,1,20);tick(220);event(0,0,230);assert(layer_state==2&&!get_mods());event(1,0,240);clean();
 reset();layer_hold_on(1);layer_hold_on(2);layer_hold_on(3);assert(layer_state==14);layer_hold_off(1);assert(layer_state==12);layer_hold_off(2);assert(layer_state==8);layer_hold_off(3);clean();
 reset();for(unsigned i=0;i<20;i++)assign(i,0x2204);for(unsigned i=0;i<20;i++)event(i,1,i);tick(220);for(unsigned i=0;i<19;i++){event(i,0,230+i);assert(get_mods()==2);}event(19,0,250);clean();
 for(unsigned mode=0;mode<2;mode++) {
  reset();keymap_config.nkro=mode;assign(0,4);assign(1,4);assign(2,0x2204);
  event(0,1,10);event(1,1,20);event(2,1,30);event(2,0,40);assert(is_key_pressed(keyboard_report,4));event(0,0,50);assert(is_key_pressed(keyboard_report,4));event(1,0,60);assert(!is_key_pressed(keyboard_report,4));clean();
  reset();keymap_config.nkro=mode;for(unsigned i=0;i<8;i++)assign(i,4+i);
  for(unsigned i=0;i<6;i++)event(i,1,10+i);
  unsigned before=log_count;
  event(6,1,20);event(7,1,21);
  if(!mode){assert(log_count==before+1);for(unsigned j=2;j<8;j++)assert(log_reports[before][j]==1);}
  else for(unsigned i=0;i<8;i++)assert(is_key_pressed(keyboard_report,4+i));
  event(0,0,30);
  if(!mode)for(unsigned j=2;j<8;j++)assert(keyboard_report->raw[j]==1);
  event(1,0,31);for(unsigned i=2;i<8;i++)assert(is_key_pressed(keyboard_report,4+i));
  for(unsigned i=2;i<8;i++)event(i,0,40+i);clean();
  reset();keymap_config.nkro=mode;for(unsigned i=0;i<6;i++)assign(i,4+i);assign(6,0x220a);
  for(unsigned i=0;i<6;i++)event(i,1,10+i);before=log_count;
  event(6,1,20);event(6,0,21);
  assert(log_count==before+2);
  if(!mode)for(unsigned j=2;j<8;j++)assert(log_reports[before][j]==1);
  for(unsigned i=0;i<6;i++)assert(is_key_pressed(keyboard_report,4+i));
  assert(!is_key_pressed(keyboard_report,10));for(unsigned i=0;i<6;i++)event(i,0,30+i);clean();
 }
 keymap_config.nkro=0;
 for(unsigned layer=6;layer<16;layer++){reset();assign(0,0x4004|(layer<<8));event(0,1,10);tick(500);event(0,0,510);assert(!log_count);clean();}
 for(unsigned tap=0;tap<2;tap++){reset();assign(0,4);map[1][0][0]=0x4100|tap;layer_on(1);event(0,1,10);assert(pending==0);event(0,0,20);assert(!log_count);layer_clear();clean();}
 for(unsigned cancel=0;cancel<3;cancel++) {
  reset();assign(0,0x2204);assign(1,5);assign(2,QK_REPEAT_KEY);event(1,1,1);event(1,0,2);event(2,1,3);event(0,1,10);
  if(cancel==0)clear_keyboard();else if(cancel==1)clear_keyboard_but_mods();else clear_keyboard_but_mods_and_keys();
  assert(!registered_record.keycode&&!get_mods()&&!get_weak_mods());tick(500);event(0,0,510);event(2,0,520);assert(!is_key_pressed(keyboard_report,5));clean();
 }
 reset();default_layer_set(2);assert(!layer_state);layer_hold_on(2);assert(layer_state==12);default_layer_set(1);assert(layer_state==4);layer_hold_on(3);default_layer_set(2);assert(layer_state==12);default_layer_set(1);assert(layer_state==12);layer_hold_off(2);assert(layer_state==8);layer_hold_off(3);clean();
 for(unsigned ns=0;ns<2;ns++) {
  unsigned first=ns?KC_AUDIO_MUTE:KC_SYSTEM_POWER,last=ns?KC_LAUNCHPAD:KC_SYSTEM_WAKE;
  for(unsigned a=first;a<=last;a++)for(unsigned b=first;b<=last;b++)for(unsigned reverse=0;reverse<2;reverse++) {
   reset();assign(0,a);assign(1,b);event(0,1,10);assert(current_usage(a)==usage(a));event(1,1,20);assert(current_usage(a)==usage(b));
   unsigned before=extra_count;event(reverse?1:0,0,30);assert(current_usage(a)==usage(reverse?a:b));
   assert(extra_count==before+(a!=b&&reverse));event(reverse?0:1,0,40);assert(!current_usage(a));clean();
   reset();assign(0,a);assign(1,0x2200|b);event(0,1,10);before=extra_count;event(1,1,20);event(1,0,30);assert(current_usage(a)==usage(a));assert(extra_count==before+(a!=b?2:0));if(a!=b){assert(extra_log[before].usage==usage(b)&&extra_log[before+1].usage==usage(a));assert(extra_log[before].ns==ns&&extra_log[before+1].ns==ns);}event(0,0,40);assert(!current_usage(a));clean();
   reset();assign(0,a);assign(1,0x2200|b);assign(2,QK_REPEAT_KEY);event(0,1,10);event(1,1,20);event(1,0,30);assert(get_last_keycode()==b);event(2,1,40);assert(current_usage(a)==usage(b));event(reverse?2:0,0,50);assert(current_usage(a)==usage(reverse?a:b));event(reverse?0:2,0,60);assert(!current_usage(a));clean();
  }
 }
 reset();assign(0,KC_AUDIO_MUTE);event(0,1,10);unsigned ne=extra_count;register_code(KC_AUDIO_MUTE);assert(extra_count==ne);event(0,0,20);assert(current_usage(KC_AUDIO_MUTE)==usage(KC_AUDIO_MUTE));unregister_code(KC_AUDIO_MUTE);assert(!last_consumer);clean();
 reset();assign(0,KC_SYSTEM_POWER);assign(1,KC_AUDIO_MUTE);event(0,1,10);event(1,1,20);assert(last_system==SYSTEM_POWER_DOWN&&last_consumer==usage(KC_AUDIO_MUTE));event(0,0,30);assert(!last_system&&last_consumer==usage(KC_AUDIO_MUTE));event(1,0,40);assert(!last_consumer);clean();
 reset();assign(0,KC_AUDIO_MUTE);assign(1,KC_AUDIO_VOL_UP);assign(2,0x2200|KC_AUDIO_MUTE);event(0,1,10);event(1,1,20);ne=extra_count;event(2,1,30);event(2,0,40);assert(extra_count==ne&&last_consumer==usage(KC_AUDIO_VOL_UP));event(1,0,50);assert(last_consumer==usage(KC_AUDIO_MUTE));event(0,0,60);clean();
 reset();assign(0,KC_AUDIO_MUTE);assign(1,KC_SYSTEM_POWER);event(0,1,10);event(1,1,20);clear_keyboard();assert(!last_system&&!last_consumer&&!usage_lengths[0]&&!usage_lengths[1]);event(0,0,30);event(1,0,40);event(0,1,50);assert(last_consumer==usage(KC_AUDIO_MUTE));event(0,0,60);clean();
 reset();assign(0,QK_TRI_LAYER_LOWER);event(0,1,10);assert(layer_state==2);set_tri_layer_layers(4,2,3);event(0,0,20);clean();
 reset();layer_hold_on(1);layer_hold_on(2);assert(layer_state==14);set_tri_layer_layers(4,2,3);assert(layer_state==6);set_tri_layer_lower_layer(1);assert(layer_state==14);set_tri_layer_adjust_layer(5);assert(layer_state==38);set_tri_layer_upper_layer(4);assert(layer_state==6);layer_hold_off(1);layer_hold_off(2);clean();
 for(unsigned dir=0;dir<2;dir++){reset();enc[0][dir]=QK_TRI_LAYER_LOWER;encoder(dir,1,10);assert(layer_state==2);set_tri_layer_layers(4,2,3);encoder(dir,0,20);clean();}
 for(unsigned key=KC_SYSTEM_POWER;key<=KC_LAUNCHPAD;key++)for(unsigned mask=0;mask<32;mask++)for(unsigned reverse=0;reverse<2;reverse++) {
  reset();assign(0,key);event(0,1,10);uint16_t code=(mask<<8)|key;unsigned before=extra_count;register_code16(code);assert(extra_count==before&&current_usage(key)==usage(key));assert(get_weak_mods()==((mask&16)?((mask&15)<<4):mask));clear_weak_mods();assert(get_weak_mods()==((mask&16)?((mask&15)<<4):mask));
  if(reverse){unregister_code16(code);assert(current_usage(key)==usage(key));event(0,0,20);}else{event(0,0,20);assert(current_usage(key)==usage(key));unregister_code16(code);}assert(!current_usage(key));clean();
 }
 for(unsigned kind=0;kind<4;kind++) {
  reset();uint8_t key=kind==0?KC_A:kind==1?KC_LSFT:kind==2?KC_AUDIO_VOL_UP:KC_SYSTEM_POWER;assign(0,key);event(0,1,10);
  uint8_t body[8176];for(unsigned i=0;i<8175;i+=3){body[i]=1;body[i+1]=SS_DOWN_CODE;body[i+2]=key;}body[8175]='A';macro_load(body,sizeof(body));assert(macro_length==8192);
  for(unsigned repeat=0;repeat<4;repeat++)dynamic_keymap_macro_send(0);
  if(kind==0)assert(key_refs[key]==2&&is_key_pressed(keyboard_report,key));
  else if(kind==1)assert(owned_mod_refs[1]==2&&get_mods()==2);
  else assert(usage_refs[key-KC_SYSTEM_POWER]==2&&current_usage(key)==usage(key));
  macro_one(SS_UP_CODE,key);macro_one(SS_UP_CODE,key);if(kind<2)assert(kind==0?is_key_pressed(keyboard_report,key):get_mods()==2);else assert(current_usage(key)==usage(key));event(0,0,20);clean();
 }
 reset();assign(0,KC_A);assign(1,KC_LSFT);assign(2,KC_AUDIO_VOL_UP);assign(3,0x5221);event(0,1,10);event(1,1,20);event(2,1,30);event(3,1,40);
 for(unsigned i=0;i<300;i++){macro_one(SS_UP_CODE,KC_A);macro_one(SS_UP_CODE,KC_LSFT);macro_one(SS_UP_CODE,KC_AUDIO_VOL_UP);macro_one(VIAL_MACRO_EXT_UP,0x5221);}assert(is_key_pressed(keyboard_report,KC_A)&&get_mods()==2&&last_consumer==usage(KC_AUDIO_VOL_UP)&&layer_state==2);for(unsigned i=0;i<4;i++)event(i,0,50+i);clean();
 for(unsigned code=0x100;code<=0x1f00;code+=0x100) {
  reset();assign(0,KC_AUDIO_MUTE);event(0,1,10);uint8_t body[8176];for(unsigned i=0;i<sizeof(body);i+=4){body[i]=1;body[i+1]=VIAL_MACRO_EXT_DOWN;body[i+2]=KC_AUDIO_MUTE;body[i+3]=code>>8;}macro_load(body,sizeof(body));dynamic_keymap_macro_send(0);dynamic_keymap_macro_send(0);assert(usage_refs[KC_AUDIO_MUTE-KC_SYSTEM_POWER]==2);assert(get_weak_mods()==extract_mod_bits(code));macro_one(VIAL_MACRO_EXT_TAP,code|KC_AUDIO_MUTE);assert(get_weak_mods()==extract_mod_bits(code));macro_one(VIAL_MACRO_EXT_UP,code|KC_AUDIO_MUTE);assert(!get_weak_mods()&&last_consumer==usage(KC_AUDIO_MUTE));event(0,0,20);clean();
 }
 reset();macro_one(SS_DOWN_CODE,KC_A);macro_one(SS_DOWN_CODE,KC_LSFT);macro_one(SS_DOWN_CODE,KC_AUDIO_MUTE);macro_one(SS_DOWN_CODE,KC_SYSTEM_POWER);assert(is_key_pressed(keyboard_report,KC_A)&&get_mods()==2&&last_consumer&&last_system);macro_one(SS_TAP_CODE,KC_A);macro_one(SS_TAP_CODE,KC_LSFT);macro_one(SS_TAP_CODE,KC_AUDIO_MUTE);macro_one(SS_TAP_CODE,KC_SYSTEM_POWER);assert(is_key_pressed(keyboard_report,KC_A)&&get_mods()==2&&last_consumer&&last_system);for(unsigned key=0;key<4;key++)macro_one(SS_UP_CODE,key==0?KC_A:key==1?KC_LSFT:key==2?KC_AUDIO_MUTE:KC_SYSTEM_POWER);clean();
 for(unsigned code=0x2000;code<=0x4fff;code+=0x100) {
  reset();uint16_t key=code|KC_A;unsigned before=log_count;macro_one(VIAL_MACRO_EXT_TAP,key);assert(log_count==before+2&&pending==NONE);macro_one(VIAL_MACRO_EXT_DOWN,key);assert(is_key_pressed(keyboard_report,KC_A));macro_one(VIAL_MACRO_EXT_UP,key);assert(!is_key_pressed(keyboard_report,KC_A));clean();
 }
 reset();assign(0,0x2205);event(0,1,10);macro_one(VIAL_MACRO_EXT_TAP,0x2204);assert(pending==0&&!get_mods());event(0,0,20);clean();
 reset();assign(0,0x5221);event(0,1,10);for(unsigned i=0;i<300;i++)macro_one(VIAL_MACRO_EXT_DOWN,0x5221);assert(layer_refs[1]==2);macro_one(VIAL_MACRO_EXT_UP,0x5221);assert(layer_state==2);event(0,0,20);clean();
 reset();assign(0,KC_LCTL);assign(1,0x5221);event(0,1,10);event(1,1,20);for(unsigned i=0;i<300;i++)macro_one(VIAL_MACRO_EXT_DOWN,0x5021);assert(get_mods()==1&&owned_mod_refs[0]==2&&layer_refs[1]==2);macro_one(VIAL_MACRO_EXT_UP,0x5021);assert(get_mods()==1&&layer_state==2);event(0,0,30);event(1,0,40);clean();
 reset();macro_one(VIAL_MACRO_EXT_DOWN,QK_TRI_LAYER_LOWER);set_tri_layer_layers(4,2,3);macro_one(VIAL_MACRO_EXT_UP,QK_TRI_LAYER_LOWER);clean();
 reset();{uint8_t body[]={1,SS_DOWN_CODE,KC_A,1,VIAL_MACRO_EXT_TAP,3,0x7c,1,SS_DOWN_CODE,KC_B};macro_load(body,sizeof(body));dynamic_keymap_macro_send(0);assert(ak820_macro_cancelled&&!is_key_pressed(keyboard_report,KC_A)&&!is_key_pressed(keyboard_report,KC_B));clean();}
 {uint16_t repeated[]={KC_A,KC_SYSTEM_POWER,KC_AUDIO_MUTE,0x0204,0x02e3};
 for(unsigned k=0;k<sizeof(repeated)/sizeof(repeated[0]);k++)for(unsigned reverse=0;reverse<2;reverse++) {
  reset();uint16_t code=repeated[k];assign(0,code);assign(1,QK_REPEAT_KEY);event(0,1,10);event(0,0,20);event(1,1,30);uint8_t before_mods=get_mods(),before_weak=get_weak_mods();unsigned before_extra=extra_count;
  if(code<256)macro_one(SS_UP_CODE,code);else macro_one(VIAL_MACRO_EXT_UP,code);assert(get_mods()==before_mods&&get_weak_mods()==before_weak&&extra_count==before_extra);
  for(unsigned i=0;i<300;i++){if(code<256)macro_one(SS_DOWN_CODE,code);else macro_one(VIAL_MACRO_EXT_DOWN,code);}
  if(reverse){event(1,0,40);if(code<256)macro_one(SS_UP_CODE,code);else macro_one(VIAL_MACRO_EXT_UP,code);}else{if(code<256)macro_one(SS_UP_CODE,code);else macro_one(VIAL_MACRO_EXT_UP,code);assert(get_mods()==before_mods&&get_weak_mods()==before_weak);event(1,0,40);}clean();
 }}
 reset();assign(0,0x2204);event(0,1,10);tick(210);cancel_during_pre_release=true;event(0,0,220);assert(!(source_state_get(0)&SOURCE_BLOCKED));event(0,1,230);tick(430);assert(get_mods()==2);event(0,0,440);clean();
 reset();assign(0,0x0204);event(0,1,10);caps_word_on();add_weak_mods(2);caps_word_off();assert(!weak_mods&&get_weak_mods()==2);event(0,0,20);clean();
 reset();assign(0,KC_LSFT);assign(1,KC_A);assign(2,QK_REPEAT_KEY);event(0,1,10);event(1,1,20);event(0,0,30);event(1,0,40);event(2,1,50);caps_word_on();add_weak_mods(2);caps_word_off();assert(!weak_mods&&get_weak_mods()==2);event(2,0,60);clean();
 reset();macro_one(VIAL_MACRO_EXT_DOWN,0x0204);caps_word_on();add_weak_mods(2);caps_word_off();assert(!weak_mods&&get_weak_mods()==2);macro_one(VIAL_MACRO_EXT_UP,0x0204);clean();
 reset();assign(0,0x2204);caps_word_on();event(0,1,10);event(0,0,20);assert(is_caps_word_on()&&get_weak_mods()==2&&pending==NONE);caps_word_off();assert(!get_weak_mods());clean();
 reset();assign(0,0x0204);event(0,1,10);caps_word_on();add_weak_mods(2);now+=5001;caps_word_task();assert(!is_caps_word_on()&&!weak_mods&&get_weak_mods()==2);event(0,0,now+1);clean();
 reset();layer_hold_on(1);layer_hold_on(2);assert(layer_state==14);set_tri_layer_lower_layer(2);set_tri_layer_upper_layer(1);set_tri_layer_adjust_layer(2);set_tri_layer_lower_layer(6);set_tri_layer_upper_layer(255);set_tri_layer_adjust_layer(6);set_tri_layer_layers(4,4,3);set_tri_layer_layers(1,2,6);assert(get_tri_layer_lower_layer()==1&&get_tri_layer_upper_layer()==2&&get_tri_layer_adjust_layer()==3&&layer_state==14);layer_hold_off(1);layer_hold_off(2);clean();
 reset();assign(0,0x2204);assign(1,KC_B);caps_word_on();event(0,1,10);tick(210);assert(is_caps_word_on()&&get_mods()==2);event(1,1,220);assert(is_caps_word_on()&&actual_keyboard_report.raw[0]==2&&is_key_pressed(keyboard_report,KC_B));event(1,0,230);event(0,0,240);assert(is_caps_word_on()&&!get_mods());caps_word_off();clean();
 reset();assign(0,0x2104);assign(1,KC_B);caps_word_on();event(0,1,10);tick(210);assert(is_caps_word_on()&&get_mods()==1);event(1,1,220);assert(!is_caps_word_on()&&get_mods()==1&&!get_weak_mods()&&actual_keyboard_report.raw[0]==1&&is_key_pressed(keyboard_report,KC_B));event(1,0,230);event(0,0,240);clean();
 reset();assign(0,0x4104);assign(1,KC_B);map[1][0][1]=KC_C;caps_word_on();event(0,1,10);tick(210);assert(is_caps_word_on()&&layer_state==2);event(1,1,220);assert(is_caps_word_on()&&actual_keyboard_report.raw[0]==2&&is_key_pressed(keyboard_report,KC_C));event(1,0,230);event(0,0,240);assert(!layer_state&&is_caps_word_on());caps_word_off();clean();
 {uint16_t code[]={0x2204,0x2104,0x4104};for(unsigned i=0;i<3;i++){reset();assign(0,code[i]);caps_word_on();event(0,1,10);event(0,0,209);assert(is_caps_word_on()&&!get_mods()&&!layer_state&&log_count>=3&&log_reports[log_count-2][0]==2&&log_reports[log_count-2][2]==KC_A);caps_word_off();clean();}}
 reset();assign(0,0x2204);assign(1,KC_B);caps_word_on();event(0,1,10);event(1,1,20);assert(pending==NONE&&is_caps_word_on()&&get_mods()==2&&actual_keyboard_report.raw[0]==2&&is_key_pressed(keyboard_report,KC_B));event(0,0,30);assert(is_caps_word_on()&&!get_mods()&&is_key_pressed(keyboard_report,KC_B));event(1,0,40);caps_word_off();clean();
 reset();assign(0,0x2104);assign(1,KC_B);caps_word_on();event(0,1,10);event(1,1,20);assert(pending==NONE&&!is_caps_word_on()&&get_mods()==1&&!get_weak_mods()&&actual_keyboard_report.raw[0]==1&&is_key_pressed(keyboard_report,KC_B));event(0,0,30);assert(!get_mods()&&is_key_pressed(keyboard_report,KC_B));event(1,0,40);clean();
 reset();assign(0,0x4104);assign(1,KC_B);map[1][0][1]=KC_C;caps_word_on();event(0,1,10);event(1,1,20);assert(pending==NONE&&is_caps_word_on()&&layer_state==2&&actual_keyboard_report.raw[0]==2&&is_key_pressed(keyboard_report,KC_C));event(0,0,30);assert(!layer_state&&is_caps_word_on()&&is_key_pressed(keyboard_report,KC_C));event(1,0,40);caps_word_off();clean();


 for(unsigned shifted=0;shifted<2;shifted++)for(unsigned reverse=0;reverse<2;reverse++){
  reset();uint8_t basic=shifted?KC_GRAVE:KC_ESCAPE;assign(0,QK_GRAVE_ESCAPE);assign(1,basic);assign(2,KC_LSFT);if(shifted)event(2,1,10);event(0,1,20);event(1,1,30);assert(key_refs[basic]==2);event(reverse?0:1,0,40);assert(key_refs[basic]==1&&is_key_pressed(keyboard_report,basic));event(reverse?1:0,0,50);assert(!key_refs[basic]&&!is_key_pressed(keyboard_report,basic));if(shifted)event(2,0,60);clean();
 }
 /* Grave Escape resolves a physical cache separately from Repeat's retained
  * synthetic record. Releasing Shift first must not strand Grave. */
 reset();assign(0,QK_GRAVE_ESCAPE);assign(1,KC_LSFT);event(1,1,10);event(0,1,20);assert(is_key_pressed(keyboard_report,KC_GRAVE));event(1,0,30);assert(!get_mods()&&is_key_pressed(keyboard_report,KC_GRAVE));event(0,0,40);clean();
 reset();assign(0,QK_GRAVE_ESCAPE);assign(1,KC_LSFT);assign(2,QK_REPEAT_KEY);event(0,1,10);event(1,1,20);event(2,1,30);assert(is_key_pressed(keyboard_report,KC_ESCAPE)&&is_key_pressed(keyboard_report,KC_GRAVE));event(0,0,40);assert(!is_key_pressed(keyboard_report,KC_ESCAPE)&&is_key_pressed(keyboard_report,KC_GRAVE));event(2,0,50);assert(!is_key_pressed(keyboard_report,KC_GRAVE));event(1,0,60);clean();
 for(unsigned dir=0;dir<2;dir++){reset();assign(1,KC_LSFT);enc[0][dir]=QK_GRAVE_ESCAPE;event(1,1,10);encoder(dir,1,20);assert(is_key_pressed(keyboard_report,KC_GRAVE));event(1,0,30);encoder(dir,0,40);clean();}
 reset();assign(1,KC_LSFT);event(1,1,10);vial_keycode_down(QK_GRAVE_ESCAPE);assert(is_key_pressed(keyboard_report,KC_GRAVE));event(1,0,30);vial_keycode_up(QK_GRAVE_ESCAPE);clean();
 /* Configured Combos through real admission/cache/action/Repeat/owners. */
 for(unsigned mode=0;mode<2;mode++)for(unsigned reverse=0;reverse<2;reverse++) {
  reset();keymap_config.nkro=mode;fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,KC_A);assign(1,KC_B);assign(2,KC_C);assign(3,QK_REPEAT_KEY);
  event(2,1,1);event(0,1,10);assert(key_refs[KC_A]==0);event(1,1,20);assert(key_refs[KC_C]==2&&get_last_keycode()==KC_C);event(reverse?0:1,0,30);assert(key_refs[KC_C]==1);event(reverse?1:0,0,40);event(2,0,50);event(3,1,60);assert(key_refs[KC_C]==1);event(3,0,70);clean();
 }
 reset();keymap_config.nkro=0;fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},0x0106};ak820_combo_reload();assign(0,KC_A);assign(1,KC_B);assign(2,KC_LCTL);event(2,1,1);event(0,1,10);event(1,1,20);assert(get_mods()==1&&get_weak_mods()==1&&key_refs[KC_C]==1);event(0,0,30);assert(get_mods()==1&&!get_weak_mods()&&!key_refs[KC_C]);event(1,0,40);event(2,0,50);clean();
 reset();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,KC_A);assign(1,KC_B);caps_word_on();event(0,1,10);event(1,1,20);assert(is_caps_word_on()&&get_weak_mods()==2&&get_last_keycode()==KC_C);event(0,0,30);event(1,0,40);caps_word_off();clean();
 reset();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,KC_A);assign(1,KC_B);event(0,1,10);clear_keyboard();tick(100);event(0,0,110);assert(!key_refs[KC_A]&&!key_refs[KC_C]);event(0,1,120);event(1,1,130);assert(key_refs[KC_C]==1);clear_keyboard();event(0,0,140);event(1,0,150);clean();
 reset();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,KC_A);assign(1,0x2205);event(0,1,10);event(1,1,20);assert(key_refs[KC_A]==1&&!get_mods());tick(220);assert(get_mods()==2);event(0,0,230);event(1,0,240);clean();
 reset();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();assign(0,0x4107);assign(1,KC_A);map[1][0][1]=KC_B;event(0,1,10);event(1,1,20);assert(layer_state==2);tick(60);assert(key_refs[KC_B]==1&&!key_refs[KC_A]);event(1,0,70);event(0,0,80);clean();
#ifdef AK820_COMPACT_SPACE_CADET
 /* Shifted parenthesis taps pass through the normal record pipeline and keep
  * physical, weak and queued One Shot modifiers separate from the tap owner. */
 for (unsigned right=0; right<2; ++right) {
  reset(); assign(0,right?SC_RSPC:SC_LSPO); event(0,1,10); event(0,0,20);
  assert(!get_mods() && !is_key_pressed(keyboard_report,KC_9) && !is_key_pressed(keyboard_report,KC_0));
  bool saw=false; for(unsigned i=0;i<log_count;i++) if(log_reports[i][0]==(right?0x20:0x02) && log_reports[i][2]==(right?KC_0:KC_9)) saw=true;
  assert(saw && actual_keyboard_report.raw[0]==0); clean();
 }
 reset(); assign(0,SC_LSPO); assign(1,KC_LSFT); event(1,1,1); event(0,1,10); event(0,0,20);
 assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)); event(1,0,30); clean();
 reset(); assign(0,SC_RSPC); caps_word_on(); event(0,1,10); event(0,0,20);
 bool caps_saw_paren=false; for(unsigned i=0;i<log_count;i++) if(log_reports[i][2]==KC_0 && (log_reports[i][0]&MOD_BIT(KC_RIGHT_SHIFT))) caps_saw_paren=true;
 assert(caps_saw_paren); caps_word_off(); assert(!get_weak_mods()); clean();
#ifdef AK820_COMPACT_ONESHOT
 reset(); assign(0,0x52a1); assign(1,SC_LSPO); event(0,1,1); event(0,0,2); event(1,1,10); event(1,0,20);
 assert(!get_mods() && !get_weak_mods()); bool saw_osm_paren=false;
 for(unsigned i=0;i<log_count;i++) if(log_reports[i][0]==(MOD_BIT(KC_LEFT_SHIFT)|MOD_BIT(KC_LEFT_CTRL)) && log_reports[i][2]==KC_9) saw_osm_paren=true;
 assert(saw_osm_paren); clean();
#endif
 /* Two held Space Cadet sources own the same modifier independently. */
 for(unsigned reverse=0;reverse<2;reverse++) {
  reset(); assign(0,SC_LSPO); assign(1,SC_LSPO); event(0,1,10); event(1,1,20); tick(220); assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)&&actual_keyboard_report.raw[0]==MOD_BIT(KC_LEFT_SHIFT));
  event(reverse?1:0,0,230); assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)&&actual_keyboard_report.raw[0]==MOD_BIT(KC_LEFT_SHIFT)); event(reverse?0:1,0,240); assert(!get_mods()&&actual_keyboard_report.raw[0]==0); clean();
 }
 for(unsigned reverse=0;reverse<2;reverse++) {
  reset(); assign(0,SC_LSPO); assign(1,KC_LSFT); event(0,1,10); tick(210); event(1,1,220); assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)&&actual_keyboard_report.raw[0]==MOD_BIT(KC_LEFT_SHIFT));
  event(reverse?1:0,0,230); assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)&&actual_keyboard_report.raw[0]==MOD_BIT(KC_LEFT_SHIFT)); event(reverse?0:1,0,240); assert(!get_mods()&&actual_keyboard_report.raw[0]==0); clean();
 }
 reset(); assign(0,SC_SENT); event(0,1,10); event(0,0,20); bool saw_enter=false;
 for(unsigned i=0;i<log_count;i++) if(log_reports[i][2]==KC_ENTER) saw_enter=true; assert(saw_enter && !get_mods()); clean();
 for(unsigned dir=0;dir<2;dir++) { reset(); enc[0][dir]=SC_LSPO; encoder(dir,1,10); encoder(dir,0,11); bool saw_encoder_paren=false; for(unsigned i=0;i<log_count;i++) if(log_reports[i][0]==MOD_BIT(KC_LEFT_SHIFT)&&log_reports[i][2]==KC_9) saw_encoder_paren=true; assert(saw_encoder_paren&&actual_keyboard_report.raw[0]==0); clean(); }
 reset(); assign(0,SC_SENT); event(0,1,10); tick(210); assert(get_mods()==MOD_BIT(KC_RIGHT_SHIFT)); event(0,0,220); assert(!get_mods()); clean();
 reset(); assign(0,SC_LSPO); event(0,1,10); tick(210); assert(get_mods()==MOD_BIT(KC_LEFT_SHIFT)); clear_keyboard(); event(0,0,220); assert(!get_mods()); event(0,1,230); assert(!get_mods()); event(0,0,240); clean();
 reset(); assign(0,SC_LSPO); assign(1,QK_REPEAT_KEY); event(0,1,10); event(0,0,20); assert(get_last_keycode()==KC_9); event(1,1,30); assert(is_key_pressed(keyboard_report,KC_9)); bool repeated_shift=false; for(unsigned i=0;i<log_count;i++) if(log_reports[i][0]==MOD_BIT(KC_LEFT_SHIFT)&&log_reports[i][2]==KC_9) repeated_shift=true; assert(repeated_shift); event(1,0,40); clean();
#endif
 puts("PASS: production host tap/cache/action/ownership/configured-combo traces");return 0;
}
