// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_tap_dance.h"
#include "dynamic_keymap.h"

#define TD_NONE 255
#define TD_DOWN 4
#define TD_DONE 8
#define TD_SOURCES (MATRIX_ROWS * MATRIX_COLS)
_Static_assert(VIAL_TAP_DANCE_ENTRIES == 8, "compact Tap Dance slot count");
_Static_assert(TD_SOURCES < TD_NONE, "Tap Dance source width");
/* One pending snapshot; resolved holds need only source and output. */
struct td_slot { uint16_t output; uint8_t source, state; };
static struct td_slot td_slots[VIAL_TAP_DANCE_ENTRIES];
static struct td_slot AK820_STATE_MEM *td_wait, *td_work;
static vial_tap_dance_entry_t td_entry;
static uint16_t td_time;
/* Values 0..7 select a slot; 8 means consumed until physical release. */
#define TD_MAP_NONE 8
static uint8_t td_map[(TD_SOURCES + 1) / 2];
static uint8_t td_map_get(uint8_t id) {
    uint8_t packed = td_map[id >> 1];
    return (id & 1) ? packed >> 4 : packed & 15;
}
/* Callers pass only slot indices 0..7 or TD_MAP_NONE. */
static void td_map_set(uint8_t id, uint8_t value) {
    uint8_t AK820_STATE_MEM *packed = td_map + (id >> 1);
    uint8_t shift = id & 1;
    uint8_t mask = shift ? 15 : 240;
    if (shift) value <<= 4;
    *packed = (*packed & mask) | value;
}
static keyrecord_t td_record;
static uint8_t td_step;
static bool ak820_td_invoking;

bool ak820_tap_dance_valid(const vial_tap_dance_entry_t AK820_STATE_MEM *entry) {
    const uint8_t AK820_STATE_MEM *bytes = (const uint8_t AK820_STATE_MEM *)entry;
    if (bytes[9] & 128) return false;
    for (uint8_t i = 0; i < 4; ++i, bytes += 2) {
        uint8_t basic = bytes[0], mods = bytes[1];
        if (!(basic | mods)) continue;
        if (mods >= 32 || !(((uint8_t)(basic - KC_A) <= (KC_EXSEL - KC_A)) ||
            ((uint8_t)(basic - KC_LEFT_CTRL) <= (KC_RIGHT_GUI - KC_LEFT_CTRL)))) return false;
    }
    return true;
}
/* process_record re-enters Quantum record processors, bypassing admission.
 * td_work/td_record are private to this engine; shared clear can cancel state. */
static void td_prepare(void) {
    td_record.event.key.row = td_work->source / MATRIX_COLS;
    td_record.event.key.col = td_work->source % MATRIX_COLS;
    td_record.event.type = KEY_EVENT;
    td_record.event.time = td_time;
    td_record.tap.count = 1;
}
static void td_finish(bool interrupted) {
    uint8_t choice = 0, state;
    bool extra = false;
    if (ak820_td_invoking) return;
    if (!td_wait) return;
    ak820_td_invoking = true;
    td_work = td_wait;
    td_wait = 0;
    state = td_work->state;
    td_work->state = state | TD_DONE;
    if ((state & 3) == 1) {
        if ((state & TD_DOWN) && !interrupted) choice = 1;
    } else if (interrupted) extra = true;
    else choice = (state & TD_DOWN) ? 3 : 2;
    td_work->output = ((uint16_t AK820_STATE_MEM *)&td_entry)[choice];
    if (!td_work->output) {
        if (choice >= 2) extra = true;
        td_work->output = choice == 3 && td_entry.on_hold ? td_entry.on_hold : td_entry.on_tap;
    }
    td_step = extra ? 0 : 2;
    td_record.keycode = td_entry.on_tap;
    td_prepare();
    /* No local is live across dispatch. A report callback may clear all
     * owners, but cannot re-enter this admission-only engine. */
    for (; td_step < 4; ++td_step) {
        if (td_step == 2) td_record.keycode = td_work->output;
        if (td_step == 3 && (td_work->state & TD_DOWN)) break;
        td_record.event.pressed = !(td_step & 1);
        if (td_record.keycode) process_record(&td_record);
        if (!td_work->state) goto done;
    }
    if (!(td_work->state & TD_DOWN)) td_work->state = 0;
done:
    ak820_td_invoking = false;
}
void ak820_tap_dance_task(uint16_t now) {
    uint16_t term = td_entry.custom_tapping_term;
    if (!term) term = 200;
    if (td_wait && (uint16_t)(now - td_time) >= term) td_finish(false);
}
bool ak820_tap_dance_before(const keyevent_t AK820_STATE_MEM *event) {
    uint8_t id;
    struct td_slot AK820_STATE_MEM *slot;
    if (IS_NOEVENT(*event)) return true;
    if (event->key.row >= MATRIX_ROWS || event->key.col >= MATRIX_COLS) {
        if (event->pressed) td_finish(true);
        return true;
    }
    id = event->key.row * MATRIX_COLS + event->key.col;
    if (td_map_get(id) == TD_MAP_NONE) {
        if (!event->pressed) td_map_set(id, 0);
        return false;
    }
    if (event->pressed && td_wait && (td_wait->source != id || (td_wait->state & 3) == 2)) td_finish(true);
    id = event->key.row * MATRIX_COLS + event->key.col;
    slot = td_slots + td_map_get(id);
    if (slot->state && slot->source == id) {
        if (event->pressed) return !(slot->state & TD_DONE);
        slot->state &= ~TD_DOWN;
        if (slot->state & TD_DONE) {
            td_work = slot;
            td_record.keycode = slot->output;
            slot->state = 0;
            td_prepare();
            td_record.event.pressed = false;
            if (td_record.keycode) process_record(&td_record);
        }
        return false;
    }
    return true;
}
bool ak820_tap_dance_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t index, id;
    struct td_slot AK820_STATE_MEM *slot;
    if (get_repeat_key_count() || ak820_macro_primitive || record->event.type != KEY_EVENT ||
        record->event.key.row >= MATRIX_ROWS || record->event.key.col >= MATRIX_COLS ||
        !record->event.pressed) return (record->keycode >> 8) != (QK_TAP_DANCE >> 8);
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
    /* Only id remains live across finishing the old gesture. */
    if (td_wait && !(td_wait->state & TD_DOWN) && td_wait->source == id &&
        record->keycode != (QK_TAP_DANCE | td_map_get(id))) td_finish(true);
    if ((record->keycode >> 8) != (QK_TAP_DANCE >> 8)) return true;
    index = (uint8_t)record->keycode;
    slot = td_slots + (index & 7);
    if (index >= VIAL_TAP_DANCE_ENTRIES || (slot->state && slot->source != id)) goto suppress;
    if (!slot->state) {
        if (dynamic_keymap_get_tap_dance(index, &td_entry)) goto suppress;
        slot->source = id;
    }
    slot->state = (slot->state & 3) + 1 + TD_DOWN;
    td_time = record->event.time;
    td_wait = slot;
    td_map_set(id, index);
    return false;
suppress:
    td_map_set(id, TD_MAP_NONE);
    return false;
}
void ak820_tap_dance_cancel(void) {
    td_wait = 0;
    for (uint8_t i = 0; i < VIAL_TAP_DANCE_ENTRIES; ++i) td_slots[i].state = 0;
    for (uint8_t i = 0; i < sizeof(td_map); ++i) td_map[i] = 0;
}
