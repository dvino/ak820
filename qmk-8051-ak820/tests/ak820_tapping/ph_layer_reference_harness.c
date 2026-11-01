/* Host boundary callbacks only; retained lookup/classification lives in retained.inc. */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "action_code.h"
#include "quantum_keycodes.h"
typedef struct { uint8_t row, col; } keypos_t;
typedef struct { keypos_t key; uint16_t time; bool pressed; uint8_t type; } keyevent_t;
typedef struct { uint8_t count; bool interrupted; } tap_t;
typedef struct { keyevent_t event; tap_t tap; } keyrecord_t;
typedef uint32_t layer_state_t;
#define AK820_RECORD_MEM
#define MAX_LAYER 2
#define TAPPING_TERM 200
#define QUICK_TAP_TERM 0
#define PERMISSIVE_HOLD
#define NO_ACTION_ONESHOT
#define TIMER_DIFF_16(a,b) ((uint16_t)((a)-(b)))
#define KEYEQ(a,b) ((a).row==(b).row && (a).col==(b).col)
#define IS_EVENT(e) ((e).type != 0)
#define IS_NOEVENT(e) (!IS_EVENT(e))
#define IS_KEYEVENT(e) IS_EVENT(e)
#define ac_dprintf(...) ((void)0)
#define debug_record(...) ((void)0)
#define debug_event(...) ((void)0)
#include "action_tapping.h"
static uint16_t map[2][16], now;
static uint8_t cache[16];
static layer_state_t layer_state, default_layer_state=1;
static bool disable_action_cache;
uint16_t action_for_key(uint8_t, keypos_t);
uint16_t action_for_keycode(uint16_t);
uint8_t layer_switch_get_layer(keypos_t);
uint16_t layer_switch_get_action(keypos_t);
uint16_t get_record_keycode(keyrecord_t *, bool);
uint16_t get_event_keycode(keyevent_t, bool);
bool pre_process_record_quantum(keyrecord_t *);
static bool is_tap_record(keyrecord_t *);
static void process_record_tap_hint(keyrecord_t *);
static void process_record(keyrecord_t *);
static void clear_keyboard(void);
static uint16_t keycode_config(uint16_t k) { return k; }
static uint8_t mod_config(uint8_t m) { return m; }
static uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key) { return map[layer][key.col]; }
static void update_source_layers_cache(keypos_t key, uint8_t layer) { cache[key.col]=layer; }
static uint8_t read_source_layers_cache(keypos_t key) { return cache[key.col]; }
static bool pre_process_record_kb(uint16_t k, keyrecord_t *r) {
    printf("P %u %u %u %u %04x\n",r->event.time,now,r->event.key.col,r->event.pressed,k);
    return true;
}
#include "retained.inc"
/* Instrument the same two lookup boundaries used by process_record_quantum
 * and process_record_handler, without claiming to execute those functions. */
static void process_record(keyrecord_t *r) {
    if (IS_NOEVENT(r->event)) return;
    uint16_t k=get_record_keycode(r,true);
    action_t a; a.code=store_or_get_action(r->event.pressed,r->event.key);
    /* Stub only for ordinary LT(1, KC_ESC) holds in these traces. Retained
     * process_action opcode dispatch and layer helpers are not executed. */
    if (a.kind.id==ACT_LAYER_TAP && !r->tap.count) {
        uint32_t bit=1UL<<a.layer_tap.val;
        if(r->event.pressed) layer_state|=bit; else layer_state&=~bit;
    }
    printf("F %u %u %u %u %04x %04x %u %lx\n",r->event.time,now,r->event.key.col,r->event.pressed,k,a.code,r->tap.count,(unsigned long)layer_state);
}
static void clear_keyboard(void) { puts("OVERFLOW"); layer_state=0; }
/* Fresh physical input only; engine-managed replays retain their tap state. */
static void initialized_physical_record(keyevent_t event) {
    keyrecord_t record = {.event = event};
    if (IS_NOEVENT(record.event) || pre_process_record_quantum(&record)) {
        action_tapping_process(record);
    }
}
static void assert_pending_lt(uint8_t col) {
    assert(tapping_key.event.pressed && tapping_key.event.key.col == col);
    assert(tapping_key.tap.count == 0 && !tapping_key.tap.interrupted);
    assert(layer_state == 0);
    puts("PENDING LT count=0 interrupted=0 layer=0");
}
int main(void) {
    char op; unsigned a,b,c;
    while(scanf(" %c",&op)==1) {
        if(op=='M') { if(scanf("%u %u %x",&a,&b,&c)!=3 || a>=2 || b>=16 || c>65535) return 2; map[a][b]=c; }
        else if(op=='E') {
            if(scanf("%u %u %u",&a,&b,&c)!=3 || a>65535 || b>=16 || c>1) return 2;
            now=a; keyevent_t e={.key={0,b},.time=now,.pressed=c,.type=1}; initialized_physical_record(e);
        } else if(op=='S') { if(scanf("%u", &a)!=1 || a>=16) return 2; assert_pending_lt(a); } else return 2;
    }
    return 0;
}
