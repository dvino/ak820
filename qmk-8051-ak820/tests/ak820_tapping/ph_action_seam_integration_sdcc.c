// SPDX-License-Identifier: GPL-2.0-or-later
/* Actual tapping.c, scoped pool and source-extracted action continuation.
 * Other hooks and output are mocks; nested callback reachability is constructed. */
#include "quantum.h"
#include "ak820_ph_frame.h"
#include "ak820_tapping.h"
#include "ak820_autoshift.h"
#include "ak820_combo.h"
#include "ak820_dynamic_macro.h"
#include "ak820_leader.h"
#include "ak820_settings.h"
#include "dynamic_keymap.h"
#include "vial.h"

__xdata __at (0x0e00) volatile uint8_t result[64];
static uint8_t count, nested, failure;
static uint16_t clock_value;
static keyrecord_t __xdata *outer_record;
bool vial_unlock_in_progress;
static void mark(uint8_t value) { result[4 + count++] = value; }
uint16_t timer_read(void) { return ++clock_value; }
uint16_t ak820_settings_tapping_term(void) { return 200; }
uint16_t ak820_settings_oneshot_timeout(void) { return 0; }
int8_t get_repeat_key_count(void) { return 0; }
void add_owned_mods(uint8_t mods) { (void)mods; }
void unregister_mods(uint8_t mods) { (void)mods; mark(0x32); }
void register_mods(uint8_t mods) {
    (void)mods; mark(0x31);
#if TEST_CASE == 1
    nested = 1;
    if (!ak820_ph_action_run(0, 3, false, KEY_EVENT)) failure = 1;
    nested = 0;
#endif
}
void layer_hold_on(uint8_t layer) { (void)layer; }
void layer_hold_off(uint8_t layer) { (void)layer; }
void dynamic_keymap_macro_send(uint8_t id) { (void)id; }
void ak820_dynamic_macro_task(uint16_t time) { (void)time; mark(0x11); }
bool ak820_combo_tick(uint16_t time) { (void)time; mark(0x12); return true; }
bool ak820_autoshift_before(const keyevent_t __xdata *event) { (void)event; mark(0x13); return true; }
bool ak820_autoshift_process(keyrecord_t __xdata *record) { (void)record; mark(0x14); return true; }
void ak820_leader_task(uint16_t time) { (void)time; mark(0x15); }
void clear_weak_mods(void) { mark(0x16); }
bool pre_process_record_quantum(keyrecord_t __xdata *record) {
    mark(0x20 | record->event.key.col);
    record->keycode = record->event.key.col == 1 ? 0x2104 : 0x0005;
    return true;
}
void process_record(keyrecord_t __xdata *record) {
    mark((record->event.pressed ? 0x40 : 0x60) | record->event.key.col);
#if TEST_CASE == 2
    if (!nested && record->event.key.col == 2 && record->event.pressed) {
        outer_record = record;
        nested = 1;
        if (!ak820_ph_action_run(0, 3, true, KEY_EVENT)) failure = 1;
        nested = 0;
        if (outer_record->event.key.row != 0 || outer_record->event.key.col != 2 || outer_record->event.time != 2 || outer_record->event.type != KEY_EVENT || !outer_record->event.pressed || outer_record->keycode != 5 || outer_record->tap.count) failure = 2;
    }
#endif
}
void main(void) {
#if TEST_CASE == 1
    mark(0x93); if (!ak820_ph_action_run(0, 3, true, KEY_EVENT)) failure = 9;
#endif
    mark(0xa1); if (!ak820_ph_action_run(0, 1, true, KEY_EVENT)) failure = 3;
    mark(0xa2); if (!ak820_ph_action_run(0, 2, true, KEY_EVENT)) failure = 4;
    mark(0xb2); if (!ak820_ph_action_run(0, 2, true, KEY_EVENT)) failure = 5;
    mark(0xc2); if (!ak820_ph_action_run(0, 2, false, KEY_EVENT)) failure = 6;
#if TEST_CASE == 2
    mark(0xc3); if (!ak820_ph_action_run(0, 3, false, KEY_EVENT)) failure = 7;
#endif
    mark(0xc1); if (!ak820_ph_action_run(0, 1, false, KEY_EVENT)) failure = 8;
    result[0] = 0xa5; result[1] = failure; result[2] = count; result[3] = nested;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
