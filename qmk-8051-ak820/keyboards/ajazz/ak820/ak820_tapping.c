// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_tapping.h"
#include "encoder.h"
#ifdef VIAL_ENABLE
#    include "vial.h"
#endif

#define SOURCES (MATRIX_ROWS * MATRIX_COLS + 2 * NUM_ENCODERS)
#define SOURCE_ACTIVE 1
#define SOURCE_BLOCKED 2
#define SOURCE_HELD 4
_Static_assert(SOURCE_BLOCKED == (SOURCE_ACTIVE << 1), "cancel active-to-blocked shift");
#define NONE 255
_Static_assert(SOURCES < NONE, "tap source index width");
_Static_assert(MAX_LAYER == 6, "tap layer domain");
_Static_assert(QK_MOD_TAP == 0x2000 && QK_LAYER_TAP_MAX == 0x4fff, "dual-role byte namespace");
/* One pending decision; other presses resolve it before admission. No event
 * queue, replay recursion or rollover-dependent owner limit is needed. */
/* ACTIVE tracks admission until its accepted release. HELD is the resolved
 * dual-role owner. BLOCKED survives cancellation until the physical release.
 * A release clears ACTIVE before downstream hooks; cancellation must not
 * infer a still-pressed source from HELD alone. */
static uint8_t source_state[SOURCES];
static uint8_t pending = NONE;
static uint16_t pending_time, pending_code;

static uint8_t source(keypos_t key) {
    if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) return key.row * MATRIX_COLS + key.col;
    if (key.col < NUM_ENCODERS) {
        if (key.row == KEYLOC_ENCODER_CW) return MATRIX_ROWS * MATRIX_COLS + key.col;
        if (key.row == KEYLOC_ENCODER_CCW) return MATRIX_ROWS * MATRIX_COLS + NUM_ENCODERS + key.col;
    }
    return NONE;
}
static void hold(uint16_t code, bool pressed) {
    if (code < QK_LAYER_TAP) {
        uint8_t mods = (code >> 8) & 31;
        if (mods & 16) mods <<= 4;
        if (pressed) register_mods(mods);
        else unregister_mods(mods);
    } else {
        uint8_t layer = (code >> 8) & 15;
        if (pressed) layer_hold_on(layer);
        else layer_hold_off(layer);
    }
}
static void commit_pending(void) {
    uint8_t id = pending;
    pending = NONE; /* A report callback cannot resurrect the decision. */
    source_state[id] |= SOURCE_HELD;
    hold(pending_code, true);
}
bool ak820_tapping_before(const keyevent_t AK820_STATE_MEM *event) {
    uint8_t id = source(event->key);
#ifdef VIAL_ENABLE
    if (vial_unlock_in_progress) {
        if (IS_EVENT(*event) && id != NONE && !event->pressed) source_state[id] &= ~SOURCE_BLOCKED;
        return false;
    }
#endif
    if (pending != NONE && ((uint16_t)(event->time - pending_time) >= 200 ||
        (IS_EVENT(*event) && event->pressed && (id == NONE || id != pending)))) commit_pending();
    if (IS_NOEVENT(*event) || id == NONE) return true;
    if ((source_state[id] & SOURCE_BLOCKED)) {
        if (!event->pressed) source_state[id] &= ~SOURCE_BLOCKED;
        return false;
    }
    /* Duplicate presses and unmatched releases cannot acquire/drop owners. */
    if (event->pressed == ((source_state[id] & SOURCE_ACTIVE) != 0)) return false;
    source_state[id] ^= SOURCE_ACTIVE;
    return true;
}
bool ak820_tapping_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id, kind;
    uint16_t code;
    if (IS_NOEVENT(record->event)) return true;
    id = source(record->event.key);
    if (id == NONE) return true;
    code = record->keycode;
    kind = code >> 8;
    if (kind < 0x20 || kind >= 0x50) return true;
    if (kind >= 0x40 && (kind & 15) >= MAX_LAYER) return false;
    if (record->event.pressed) {
        pending = id;
        pending_time = record->event.time;
        pending_code = code;
    } else if (id == pending) {
        pending = NONE;
        /* NO and transparent are opaque dual-role taps that emit nothing.
         * All other accepted basic bytes use the real basic decoder/pipeline. */
        record->keycode = (uint8_t)code;
        if (record->keycode > KC_TRANSPARENT) {
            record->tap.count = 1;
            record->event.pressed = true;
            process_record(record);
            record->event.pressed = false;
            process_record(record);
        }
    } else if ((source_state[id] & SOURCE_HELD)) {
        source_state[id] &= ~SOURCE_HELD;
        hold(code, false);
    }
    return false;
}
void ak820_tapping_cancel(void) {
    pending = NONE;
    for (uint8_t i = 0; i < SOURCES; ++i) {
        uint8_t state = source_state[i];
        source_state[i] = (state & SOURCE_BLOCKED) | ((state & SOURCE_ACTIVE) << 1);
    }
}
