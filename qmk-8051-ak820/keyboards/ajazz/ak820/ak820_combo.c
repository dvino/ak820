// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_combo.h"
#ifdef AK820_QMK_SETTINGS
#    include "ak820_settings.h"
#    define AK820_COMBO_TERM ak820_settings_combo_term()
#else
#    define AK820_COMBO_TERM 40
#endif
#include "dynamic_keymap.h"

#define NONE 255
/* Only ordinary nonmodifier keyboard usages enter the delayed path. Outputs
 * also allow modifiers. No generated record re-enters this engine. */
#define COMBO_INPUT(code) ((code) >= KC_A && (code) <= KC_EXSEL)
#define COMBO_OUTPUT(code) \
    ((code) < QK_MOD_TAP && (COMBO_INPUT((uint8_t)(code)) || ((uint8_t)(code) >= KC_LEFT_CTRL && (uint8_t)(code) <= KC_RIGHT_GUI)))
static struct { uint8_t a, b; uint16_t output; } combos[VIAL_COMBO_ENTRIES];
static keyrecord_t saved;
static uint8_t first = NONE, second = NONE;
static bool active;

bool ak820_combo_valid(const vial_combo_entry_t AK820_STATE_MEM *entry) {
    if (entry->input[2] || entry->input[3]) return false;
    if (!(entry->input[0] | entry->input[1])) return !entry->output;
    if (entry->input[0] == entry->input[1]) return false;
    if (!COMBO_INPUT(entry->input[0])) return false;
    if (!COMBO_INPUT(entry->input[1])) return false;
    return COMBO_OUTPUT(entry->output);
}
/* A Combo settings write or unlock calls clear_keyboard(), whose shared cancellation
 * path drops every owner and blocks still-held physical sources. */
void ak820_combo_cancel(void) { first = second = NONE; active = false; }
void ak820_combo_reload(void) {
    for (uint8_t i = 0; i < VIAL_COMBO_ENTRIES; ++i) {
        vial_combo_entry_t entry;
        combos[i].a = 0;
        if (!dynamic_keymap_get_combo(i, &entry)) {
            combos[i].a = entry.input[0];
            combos[i].b = entry.input[1];
            combos[i].output = entry.output;
        }
    }
}
static void flush(void) {
    first = NONE;
    process_record(&saved);
}
void ak820_combo_tick(uint16_t now) {
    if (first != NONE && !active && (uint16_t)(now - saved.event.time) >= AK820_COMBO_TERM) flush();
}
bool ak820_combo_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id, code = record->keycode;
    if (IS_NOEVENT(record->event)) return true;
    /* Encoder pulses never become candidates. */
    if (record->event.key.row >= MATRIX_ROWS || record->event.key.col >= MATRIX_COLS) {
        if (first != NONE && !active) flush();
        return true;
    }
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
    if (active) {
        if (id != first && id != second) return true;
        if (!record->event.pressed) {
            if (saved.event.pressed) {
                saved.event.pressed = false;
                process_record(&saved);
            }
            if (id == first) first = NONE;
            else second = NONE;
            if (first == NONE && second == NONE) active = false;
        }
        return false;
    }
    bool eligible = false;
    if (record->event.pressed && COMBO_INPUT(record->keycode)) {
        uint8_t previous = saved.keycode;
        for (uint8_t i = 0; i < VIAL_COMBO_ENTRIES; ++i) {
            uint8_t a = combos[i].a, b = combos[i].b;
            if (a == code || b == code) {
                eligible = true;
                if (first != NONE && code != previous && (a == previous || b == previous)) {
                    second = id;
                    active = true;
                    saved.keycode = combos[i].output;
                    process_record(&saved);
                    return false;
                }
            }
        }
    }
    if (first != NONE) flush();
    if (eligible) {
        first = id;
        saved = *record;
        return false;
    }
    return true;
}
