/* SPDX-License-Identifier: GPL-2.0-or-later */
#include "ak820_autoshift.h"
#include "ak820_tap_dance.h"
static vial_tap_dance_entry_t fixture_td;
int dynamic_keymap_get_tap_dance(uint8_t index, vial_tap_dance_entry_t *entry) {
    assert(index == 0); *entry = fixture_td; return 0;
}
void body_action_exec(keyevent_t event);
void body_process_record(keyrecord_t *record);
bool process_record_via(uint16_t keycode, keyrecord_t *record);
/* CALLBACK TESTS */
static unsigned action_depth, record_depth, max_action, max_record;
static unsigned rejected, cancelled;
static unsigned reject_at;
static bool cancel_nested;
/* Instrumentation bounds are test watchdogs, NOT production capacity claims. */
void action_exec(keyevent_t event) {
    keyevent_t sentinel = event;
    assert(action_depth < 16);
    if (reject_at && action_depth == reject_at) { ++rejected; clear_keyboard(); return; }
    ++action_depth;
    if (action_depth > max_action) max_action = action_depth;
    body_action_exec(event);
    assert(memcmp(&sentinel, &event, sizeof(event)) == 0);
    --action_depth;
}
void process_record(keyrecord_t *record) {
    keyevent_t sentinel = record->event;
    assert(record_depth < 16);
    ++record_depth;
    if (record_depth > max_record) max_record = record_depth;
    if (cancel_nested && record_depth > 1) {
        cancel_nested = false; ++cancelled; clear_keyboard();
    } else body_process_record(record);
    /* These traces use no processor intentionally rewriting event identity. */
    assert(memcmp(&sentinel, &record->event, sizeof(sentinel)) == 0);
    --record_depth;
}
static void fresh(void) {
    reset(); ak820_autoshift_configure(0);
    max_action = max_record = rejected = cancelled = 0;
    reject_at = 0; cancel_nested = false;
    fixture_td = (vial_tap_dance_entry_t){0};
}
static void macro_repeat(void) {
    const uint8_t body[] = {1, VIAL_MACRO_EXT_TAP, QK_REPEAT_KEY & 255, QK_REPEAT_KEY >> 8};
    macro_load(body, sizeof(body));
}
int main(void) {
    /* Physical macro -> generated Repeat -> same macro, rejected by sending.
     * Physical macro admission has already replaced Repeat's remembered key. */
    fresh(); assign(0, KC_A); event(0, true, 10); event(0, false, 11);
    macro_repeat(); assign(1, QK_MACRO); event(1, true, 20); event(1, false, 21);
    assert(max_action == 2 && max_record == 3 && !key_refs[KC_A] && log_count == 2);
    printf("macro-repeat action=%u record=%u reports=%u\n", max_action, max_record, log_count);

    /* Repeat -> macro -> generated extended action. */
    fresh();
    const uint8_t body[] = {1, VIAL_MACRO_EXT_TAP, QK_TRI_LAYER_LOWER & 255, QK_TRI_LAYER_LOWER >> 8};
    macro_load(body, sizeof(body));
    keyrecord_t remembered = {0}; remembered.keycode = QK_MACRO;
    set_last_record(QK_MACRO, &remembered);
    assign(0, QK_REPEAT_KEY); event(0, true, 10); event(0, false, 11);
    assert(max_action == 2 && max_record == 3 && !layer_state);
    printf("repeat-macro action=%u record=%u\n", max_action, max_record);

    /* Actual Combo pending record is flushed by a generated action. */
    fresh(); fixture_combos[0] = (vial_combo_entry_t){{KC_A, KC_B, 0, 0}, KC_C};
    ak820_combo_reload(); assign(0, KC_A); event(0, true, 10);
    assert(first != NONE && !key_refs[KC_A]); now = 60;
    vial_keycode_down(QK_TRI_LAYER_LOWER);
    assert(first == NONE && key_refs[KC_A] == 1);
    vial_keycode_up(QK_TRI_LAYER_LOWER); event(0, false, 61);

    /* Actual TD pending snapshot is interrupted by generated input. */
    fresh(); fixture_td.on_tap = KC_D; fixture_td.on_hold = KC_E;
    assign(0, QK_TAP_DANCE); event(0, true, 10); assert(td_wait);
    now = 20; vial_keycode_down(QK_TRI_LAYER_LOWER);
    assert(!td_wait && key_refs[KC_D] == 1);
    vial_keycode_up(QK_TRI_LAYER_LOWER); event(0, false, 21); assert(!key_refs[KC_D]);

    /* Actual AS pending record is flushed by generated input. */
    fresh(); ak820_autoshift_configure(1); assign(0, KC_A); event(0, true, 10);
    assert(as_state == 1 && !key_refs[KC_A]); now = 20;
    vial_keycode_down(QK_TRI_LAYER_LOWER); assert(as_state == 2 && key_refs[KC_A]);
    vial_keycode_up(QK_TRI_LAYER_LOWER); event(0, false, 21); assert(!key_refs[KC_A]);

    /* Production board resolver caches press identity across a map change. */
    fresh(); assign(0, KC_A); event(0, true, 10);
    assert(ak820_cached_key(0) == KC_A); assign(0, KC_B);
    event(0, false, 11); assert(!key_refs[KC_A] && !key_refs[KC_B]);

    fresh(); assign(0, LT(1, KC_ESCAPE)); assign(1, KC_A); map[1][0][1] = KC_B;
    event(0, true, 10); tick(210); event(1, true, 220);
    assert(layer_state == 2 && key_refs[KC_B] == 1 && ak820_cached_key(1) == KC_B);
    event(0, false, 230); assert(!layer_state);
    event(1, false, 240); assert(!key_refs[KC_A] && !key_refs[KC_B]);

    /* Test-injected rejection/cancellation: observe existing cleanup only. */
    fresh(); macro_repeat(); set_last_keycode(KC_A); assign(0, QK_MACRO);
    reject_at = 1; event(0, true, 10); assert(rejected && !key_refs[KC_A]);
    fresh(); set_last_keycode(KC_A); assign(0, QK_REPEAT_KEY);
    cancel_nested = true; event(0, true, 10); assert(cancelled && !key_refs[KC_A]);
    /* Explicitly expose why cleanup alone is not transaction quarantine. */
    clear_keyboard(); add_owned_key(KC_B); assert(key_refs[KC_B] == 1);
    clear_keyboard();
    assert(!action_depth && !record_depth);
    puts("PASS: pending callbacks, board cache, injected rejection/cancellation; reacquisition remains possible");
    return 0;
}
