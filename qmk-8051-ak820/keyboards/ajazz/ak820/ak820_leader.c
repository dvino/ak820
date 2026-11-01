// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_leader.h"
#include "dynamic_keymap.h"
#include "vial.h"

#include "ak820_leader_timeout.h"
#ifdef AK820_QMK_SETTINGS
#    include "ak820_settings.h"
#    define LEADER_TIMEOUT ak820_settings_leader_timeout()
#else
#    define LEADER_TIMEOUT AK820_LEADER_TIMEOUT
#endif
#define NONE 255
_Static_assert(KC_A <= KC_EXSEL && KC_EXSEL <= 0xff, "Leader keycode range must fit in one byte");
#define LEADER_SOURCES (MATRIX_ROWS * MATRIX_COLS)
_Static_assert(LEADER_SOURCES < NONE, "Leader source index width");
/* Suppress only releases whose press this engine consumed. Tapping admission
 * rejects duplicates and blocks held sources across shared cancellation. */
#ifdef AK820_COMPACT_KEY_OVERRIDE
static uint8_t leader_suppressed[LEADER_SOURCES];
#else
static uint8_t leader_suppressed[(LEADER_SOURCES + 7) / 8];
#endif
#ifdef __SDCC_mcs51
static __bit leader_waiting;
#else
static bool leader_waiting;
#endif
static bool leader_running;
static uint16_t leader_started;
static uint8_t leader_pending = NONE;

void ak820_leader_cancel(void) {
    leader_waiting = false;
    leader_pending = NONE;
    for (uint8_t i = 0; i < sizeof(leader_suppressed); ++i) leader_suppressed[i] = 0;
}
void ak820_leader_task(uint16_t now) {
    if (vial_unlock_in_progress) { ak820_leader_cancel(); return; }
    if (leader_running) return;
    if (leader_waiting && (uint16_t)(now - leader_started) >= LEADER_TIMEOUT) leader_waiting = false;
    if (leader_pending != NONE) {
        uint8_t slot = leader_pending;
        leader_pending = NONE; /* Interpreter-generated events cannot recurse. */
        leader_running = true;
        dynamic_keymap_macro_send(slot);
        leader_running = false;
    }
}
bool ak820_leader_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id;
#ifndef AK820_COMPACT_KEY_OVERRIDE
    uint8_t mask, index;
#endif
    uint16_t code;
    if (record->event.type != KEY_EVENT || record->event.key.row >= MATRIX_ROWS ||
        record->event.key.col >= MATRIX_COLS || leader_running || ak820_macro_primitive || get_repeat_key_count()) return true;
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
#ifdef AK820_COMPACT_KEY_OVERRIDE
    if (leader_suppressed[id]) {
        if (!record->event.pressed) leader_suppressed[id] = 0;
#else
    index = id >> 3;
    mask = 1u << (id & 7);
    if (leader_suppressed[index] & mask) {
        if (!record->event.pressed) leader_suppressed[index] &= ~mask;
#endif
        return false;
    }
    if (!record->event.pressed) return true; /* Preheld release keeps its owner. */
    if (record->keycode == QK_LEAD) {
        if (leader_pending == NONE) {
            leader_waiting = true;
            leader_started = record->event.time;
        }
    } else {
        if (!leader_waiting) return true;
        leader_waiting = false;
        if ((uint16_t)(record->event.time - leader_started) >= LEADER_TIMEOUT) return true;
        code = record->keycode;
        /* Non-basic controls cancel, then keep their normal action. */
        if ((code >> 8) != 0 || (uint8_t)((uint8_t)code - KC_A) > (KC_EXSEL - KC_A)) return true;
        if ((uint8_t)code >= KC_1 && (uint8_t)code <= KC_0) leader_pending = (uint8_t)code - KC_1;
        else if ((uint8_t)code <= KC_F) leader_pending = (uint8_t)code - KC_A + 10;
        else leader_pending = NONE; /* Other basic keys are consumed without output. */
    }
#ifdef AK820_COMPACT_KEY_OVERRIDE
    leader_suppressed[id] = 1;
#else
    leader_suppressed[index] |= mask;
#endif
    return false;
}
