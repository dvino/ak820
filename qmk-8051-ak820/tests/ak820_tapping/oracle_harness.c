/* Host boundary for the retained QMK tapping engine. Not a decoder/HID oracle. */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "action_code.h"
typedef struct { uint8_t row, col; } keypos_t;
typedef struct { keypos_t key; uint16_t time; bool pressed; uint8_t type; } keyevent_t;
typedef struct { uint8_t count; bool interrupted; } tap_t;
typedef struct { keyevent_t event; tap_t tap; } keyrecord_t;
/* Host pointers have no SDCC address-space qualifier; action.h is stubbed here. */
#define AK820_RECORD_MEM
#define TAPPING_TERM 200
#define QUICK_TAP_TERM 0
#define HOLD_ON_OTHER_KEY_PRESS
#define NO_ACTION_ONESHOT
#define TIMER_DIFF_16(a,b) ((uint16_t)((a)-(b)))
#define KEYEQ(a,b) ((a).row==(b).row && (a).col==(b).col)
#define IS_EVENT(e) ((e).type != 0)
#define IS_NOEVENT(e) (!IS_EVENT(e))
#define IS_MODIFIER_KEYCODE(k) ((k)>=0xe0 && (k)<=0xe7)
#define ac_dprintf(...) ((void)0)
#define debug_record(...) ((void)0)
#define debug_event(...) ((void)0)
#include "action_tapping.h"
static uint16_t map[16], cached[16], now;
static uint8_t mods; static uint32_t layers;
static bool dual(uint16_t k) { return k>=0x2000 && k<0x5000; }
uint16_t get_record_keycode(keyrecord_t *r, bool update) { (void)update; return cached[r->event.key.col]; }
static bool is_tap_record(keyrecord_t *r) { return dual(map[r->event.key.col]); }
static void process_record_tap_hint(keyrecord_t *r) { (void)r; }
static uint16_t layer_switch_get_action(keypos_t p) {
    uint16_t k=cached[p.col];
    if (k>=0x4000 && k<0x5000) return 0xa000|(k&0xfff);
    if (k>=0x2000 && k<0x4000) return k;
    return k;
}
static void clear_keyboard(void) { puts("OVERFLOW"); mods=0; layers=0; }
static void process_record(keyrecord_t *r) {
    uint16_t k=cached[r->event.key.col]; bool down=r->event.pressed;
    if (k>=0x2000 && k<0x4000 && !r->tap.count) {
        uint8_t m=(k>>8)&31, bits=(m&15)<<((m&16)?4:0);
        if (down) mods|=bits; else mods&=~bits;
    } else if (k>=0x4000 && k<0x5000 && !r->tap.count) {
        uint32_t bit=1UL<<((k>>8)&15);
        if (down) layers|=bit; else layers&=~bit;
    } else if (IS_MODIFIER_KEYCODE(k)) {
        uint8_t bit=1<<(k-0xe0); if(down) mods|=bit; else mods&=~bit;
    }
    printf("%u %u %u %u %04x %02x %lx\n", now,r->event.key.col,down,r->tap.count,k,mods,(unsigned long)layers);
}
#include "retained_engine.inc"
int main(void) {
    char op; unsigned a,b,c;
    while(scanf(" %c",&op)==1) {
        if(op=='M') { if(scanf("%u %x",&a,&b)!=2 || a>=16) return 2; map[a]=b; }
        else if(op=='E') {
            if(scanf("%u %u %u",&a,&b,&c)!=3 || b>=16) return 2;
            now=a; if(c) cached[b]=map[b];
            keyrecord_t r={.event={.key={0,b},.time=now,.pressed=c,.type=1}};
            action_tapping_process(r);
        } else if(op=='T') {
            if(scanf("%u",&a)!=1) return 2;
            now=a;
            keyrecord_t r={.event={.time=now}}; action_tapping_process(r);
        } else return 2;
    }
    return 0;
}
