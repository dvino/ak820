// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_leader.h"
#include "dynamic_keymap.h"
#include "vial.h"

#define NONE 255
#define LEADER_SOURCES (MATRIX_ROWS * MATRIX_COLS)
_Static_assert(LEADER_SOURCES < NONE, "Leader source index width");
/* Suppress only releases whose press this engine consumed. Tapping admission
 * rejects duplicates and blocks held sources across shared cancellation. */
static uint8_t leader_suppressed[(LEADER_SOURCES + 7) / 8];
static bool leader_waiting, leader_running;
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
    if (leader_waiting && (uint16_t)(now - leader_started) >= 300) leader_waiting = false;
    if (leader_pending != NONE) {
        uint8_t slot = leader_pending;
        leader_pending = NONE; /* Interpreter-generated events cannot recurse. */
        leader_running = true;
        dynamic_keymap_macro_send(slot);
        leader_running = false;
    }
}
bool ak820_leader_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id, mask, index, slot = NONE;
    uint16_t code;
    if (record->event.type != KEY_EVENT || record->event.key.row >= MATRIX_ROWS ||
        record->event.key.col >= MATRIX_COLS || leader_running || ak820_macro_primitive || get_repeat_key_count()) return true;
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
    index = id >> 3;
    mask = 1u << (id & 7);
    if (leader_suppressed[index] & mask) {
        if (!record->event.pressed) leader_suppressed[index] &= ~mask;
        return false;
    }
    if (!record->event.pressed) return true; /* Preheld release keeps its owner. */
    code = record->keycode;
    if (code == QK_LEAD) {
        if (leader_pending == NONE) {
            leader_waiting = true;
            leader_started = record->event.time;
        }
    } else {
        if (!leader_waiting) return true;
        leader_waiting = false;
        if ((uint16_t)(record->event.time - leader_started) >= 300) return true;
        /* Non-basic controls cancel, then keep their normal action. */
        if (code < KC_A || code > KC_EXSEL) return true;
        if (code >= KC_1 && code <= KC_0) slot = code - KC_1;
        else if (code >= KC_A && code <= KC_F) slot = code - KC_A + 10;
        leader_pending = slot; /* Other basic keys are consumed without output. */
    }
    leader_suppressed[index] |= mask;
    return false;
}
