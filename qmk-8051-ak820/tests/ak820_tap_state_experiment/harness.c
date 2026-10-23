/* Differential event traces for the isolated process_action common-tail study.
 * Host C semantics only: this does not prove SDCC ABI or tapping timing. */
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "action_code.h"
#include "keycode.h"

typedef uint8_t layer_state_t;
typedef struct { uint8_t row, col; } keypos_t;
typedef struct { uint8_t type; keypos_t key; bool pressed; uint16_t time; } keyevent_t;
typedef struct { bool interrupted:1; bool reserved2:1; bool reserved1:1; bool reserved0:1; uint8_t count:4; } tap_t;
typedef struct { keyevent_t event; tap_t tap; uint16_t keycode; } keyrecord_t;
struct { bool oneshot_enable; } keymap_config;
#define ac_dprintf(...) ((void)0)
#define EXTRAKEY_ENABLE
#define ONESHOT_PRESSED 1
#define ONESHOT_OTHER_KEY_PRESSED 2
#define ONESHOT_START 3
#define ONESHOT_TOGGLED 4
static uint8_t QS_oneshot_tap_toggle, QS_tapping_toggle;
#define QS_tap_code_delay 7
#define QS_tap_hold_caps_delay 80
#define TAP_CODE_DELAY 7
#define TAP_HOLD_CAPS_DELAY 80
static uint8_t retro_tapping_counter;
static bool hold_on_interrupt;
struct observations { uint32_t trace[128]; uint8_t n, mods, weak, oneshot, locked, layer, default_layer, os_layer, os_state; } obs;
static void emit(unsigned op, unsigned value) {
    if(obs.n >= 128) abort();
    obs.trace[obs.n++] = ((uint32_t)op << 16) | value;
}
static uint8_t get_mods(void) { return obs.mods; }
static void register_code(uint8_t v) { emit(1,v); }
static void unregister_code(uint8_t v) { emit(2,v); }
static void qs_wait_ms(uint16_t v) { emit(3,v); }
static void wait_ms(uint16_t v) { emit(38,v); }
static void send_keyboard_report(void) { emit(4,0); }
static void add_mods(uint8_t v) { emit(5,v); obs.mods |= v; }
static void del_mods(uint8_t v) { emit(6,v); obs.mods &= ~v; }
static void add_weak_mods(uint8_t v) { emit(7,v); obs.weak |= v; }
static void del_weak_mods(uint8_t v) { emit(8,v); obs.weak &= ~v; }
static void register_mods(uint8_t v) { emit(9,v); obs.mods |= v; }
static void unregister_mods(uint8_t v) { emit(10,v); obs.mods &= ~v; }
static void add_oneshot_mods(uint8_t v) { emit(11,v); obs.oneshot |= v; }
static void del_oneshot_mods(uint8_t v) { emit(12,v); obs.oneshot &= ~v; }
static void add_oneshot_locked_mods(uint8_t v) { emit(13,v); obs.locked |= v; }
static void del_oneshot_locked_mods(uint8_t v) { emit(14,v); obs.locked &= ~v; }
static void layer_on(uint8_t v) { emit(15,v); if (v < 8) obs.layer |= 1u << v; }
static void layer_off(uint8_t v) { emit(16,v); if (v < 8) obs.layer &= ~(1u << v); }
static void layer_invert(uint8_t v) { emit(17,v); if (v < 8) obs.layer ^= 1u << v; }
static void layer_move(uint8_t v) { emit(18,v); obs.layer = v < 8 ? 1u << v : 0; }
static void layer_clear(void) { emit(19,0); obs.layer = 0; }
static void default_layer_and(uint8_t v) { emit(20,v); obs.default_layer &= v; }
static void default_layer_or(uint8_t v) { emit(21,v); obs.default_layer |= v; }
static void default_layer_xor(uint8_t v) { emit(22,v); obs.default_layer ^= v; }
static void default_layer_set(uint8_t v) { emit(23,v); obs.default_layer = v; }
static void layer_and(uint8_t v) { emit(24,v); obs.layer &= v; }
static void layer_or(uint8_t v) { emit(25,v); obs.layer |= v; }
static void layer_xor(uint8_t v) { emit(26,v); obs.layer ^= v; }
static void layer_state_set(uint8_t v) { emit(27,v); obs.layer = v; }
static bool is_oneshot_layer_active(void) { return obs.os_state != 0; }
static uint8_t get_oneshot_layer_state(void) { return obs.os_state; }
static uint8_t get_oneshot_layer(void) { return obs.os_layer; }
static void clear_oneshot_layer_state(uint8_t v) { emit(28,v); obs.os_state &= ~v; }
static void reset_oneshot_layer(void) { emit(29,0); obs.os_state = 0; }
static void set_oneshot_layer(uint8_t v,uint8_t s) { emit(30,(v << 8)|s);obs.os_layer=v;obs.os_state=s; }
static void process_record(keyrecord_t *r) { emit(31,r->event.pressed); }
static void register_mouse(uint8_t v,bool p) { emit(32,v|((unsigned)p << 8)); }
static void host_system_send(uint16_t v) { emit(33,v); }
static void host_consumer_send(uint16_t v) { emit(34,v); }
static uint8_t host_keyboard_leds(void) { return 3; }
static void led_set(uint8_t v) { emit(35,v); }
static uint16_t get_event_keycode(keyevent_t e,bool p) { (void)e;(void)p;return 0x2104; }
static bool get_hold_on_other_key_press(uint16_t k,keyrecord_t *r) { (void)k;(void)r;return hold_on_interrupt; }
static bool get_retro_tapping(uint16_t k,keyrecord_t *r) { (void)k;(void)r;return true; }
static void neutralize_flashing_modifiers(uint8_t v) { emit(36,v); }
static void tap_code(uint8_t v) { emit(37,v); }
/* IS_TAP_ACTION */

/* FUNCTIONS */

static void reset(unsigned seed) {
    memset(&obs,0,sizeof(obs));
    obs.mods = (seed & 1) ? 0xA5 : 0x5A;
    obs.weak=0x42;obs.oneshot=0xA3;obs.locked=0x35;obs.layer=0xC2;obs.default_layer=0x81;
    obs.os_layer=2;obs.os_state=(seed>>1)&7;
    keymap_config.oneshot_enable=seed&1;
    QS_oneshot_tap_toggle=(seed&2)?1:5;QS_tapping_toggle=(seed&4)?2:5;
    hold_on_interrupt=seed&8;retro_tapping_counter=(seed&1)?2:0;
}
int main(void) {
    unsigned long cases=0;
    for(unsigned code=0;code<65536;code++) {
        unsigned kind=code>>12;
        if(kind!=ACT_LMODS && kind!=ACT_RMODS && kind!=ACT_LMODS_TAP && kind!=ACT_RMODS_TAP && kind!=ACT_LAYER_MODS && kind!=ACT_LAYER_TAP && kind!=ACT_LAYER_TAP_EXT) continue;
        for(unsigned pressed=0;pressed<2;pressed++) {
            for(unsigned count=0;count<16;count++) {
                for(unsigned seed=0;seed<16;seed++) {
                    action_t a;a.code=code;
                    keyrecord_t r;memset(&r,0,sizeof(r));r.event.pressed=pressed;r.event.key.row=3;r.event.key.col=4;r.event.time=123;r.tap.count=count;r.tap.interrupted=seed&4;r.keycode=0x2104;
                    keyrecord_t rr=r;
                    reset(seed);baseline_action(&r,a);
                    struct observations before=obs;uint8_t before_retro=retro_tapping_counter;
                    reset(seed);factored_action(&rr,a);
                    if(memcmp(&before,&obs,sizeof(obs)) || memcmp(&r,&rr,sizeof(r)) || before_retro!=retro_tapping_counter) {
                        fprintf(stderr,"Mismatch action=%04x pressed=%u count=%u seed=%u traces=%u/%u\n",code,pressed,count,seed,before.n,obs.n);return 1;
                    }
                    cases++;
                }
            }
        }
    }
    printf("PASS %lu action/event/state combinations\n",cases);return 0;
}
