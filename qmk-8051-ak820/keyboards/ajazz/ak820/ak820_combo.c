// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_combo.h"
#if defined(AK820_COMBO_AUTOSHIFT) && (!defined(AK820_COMPACT_COMBO) || !defined(AK820_COMPACT_AUTOSHIFT) || !defined(AK820_COMPACT_TAPPING))
#    error "AK820_COMBO_AUTOSHIFT requires compact Combo, Auto Shift and tapping"
#endif
#ifdef AK820_COMPACT_AUTOSHIFT
#    include "ak820_autoshift.h"
#endif
#ifdef AK820_QMK_SETTINGS
#    include "ak820_settings.h"
#    define AK820_COMBO_TERM ak820_settings_combo_term()
#else
#    define AK820_COMBO_TERM 40
#endif
#include "dynamic_keymap.h"
#include <stddef.h>

#define NONE 255
/* Only ordinary nonmodifier keyboard usages enter the delayed path. Outputs
 * also allow modifiers, unmodified consumer usages and Caps Word toggle.
 * No generated record re-enters this engine. */
#define COMBO_INPUT(code) ((code) >= KC_A && (code) <= KC_EXSEL)
/* Validator inputs are bytes; event keycodes must use the full-width check. */
#define COMBO_INPUT_BYTE(code) ((uint8_t)((code) - KC_A) <= (KC_EXSEL - KC_A))
static struct { uint8_t a, b; uint16_t output; } combos[VIAL_COMBO_ENTRIES];
static keyrecord_t saved;
#ifdef __SDCC_mcs51
static __data uint8_t first = NONE;
#else
static uint8_t first = NONE;
#endif
static uint8_t second = NONE;
#ifdef AK820_COMBO_AUTOSHIFT
static bool combo_shift_owner;
#endif
static uint8_t combo_cancel_generation;
#if defined(__SDCC_mcs51)
static __bit active;
#else
static bool active;
#endif

#ifdef __SDCC_mcs51
static __bit enabled = true;
#else
static bool enabled = true;
#endif

ak820_combo_result_t ak820_combo_valid(const vial_combo_entry_t AK820_STATE_MEM *entry) {
    /* The packed Vial record uses little-endian 16-bit keycodes. Inputs are
     * basic bytes; inspect their high bytes once before the smaller checks. */
    const uint8_t AK820_STATE_MEM *bytes = (const uint8_t AK820_STATE_MEM *)entry;
    uint8_t a, b, lo, hi;
    _Static_assert(sizeof(vial_combo_entry_t) == 10 && offsetof(vial_combo_entry_t, output) == 8, "Combo wire layout");
    if (bytes[1] | bytes[3] | bytes[4] | bytes[5] | bytes[6] | bytes[7]) return false;
    a = bytes[0]; b = bytes[2]; lo = bytes[8]; hi = bytes[9];
    if (!(a | b)) return !(lo | hi);
    if (a == b || !COMBO_INPUT_BYTE(a) || !COMBO_INPUT_BYTE(b)) return false;
    if (hi == (QK_CAPS_WORD_TOGGLE >> 8) && lo == (uint8_t)QK_CAPS_WORD_TOGGLE) return true;
    if (!hi && lo >= KC_AUDIO_MUTE && lo <= KC_LAUNCHPAD) return true;
    return hi < (QK_MOD_TAP >> 8) && (COMBO_INPUT_BYTE(lo) || ((uint8_t)(lo - KC_LEFT_CTRL) <= (KC_RIGHT_GUI - KC_LEFT_CTRL)));
}
/* A Combo settings write or unlock calls clear_keyboard(), whose shared cancellation
 * path drops every owner and blocks still-held physical sources. */
void ak820_combo_cancel(void) {
    first = second = NONE; active = false;
#ifdef AK820_COMBO_AUTOSHIFT
    combo_shift_owner = false;
#endif
    ++combo_cancel_generation;
}
#ifdef AK820_COMBO_AUTOSHIFT
/* Tapping has admitted the release, but Auto Shift has not consumed it yet. */
bool ak820_combo_before(const keyevent_t AK820_STATE_MEM *event) {
    if (!active || IS_NOEVENT(*event) || event->pressed ||
        event->key.row >= MATRIX_ROWS || event->key.col >= MATRIX_COLS) return true;
    uint8_t id = event->key.row * MATRIX_COLS + event->key.col;
    if (id != first && id != second) return true;
    if (!combo_shift_owner && !ak820_autoshift_before(event)) return false;
    if (!active) return false; /* A callback may have cleared the keyboard. */
    if (id == first) first = NONE;
    else second = NONE;
    if (first == NONE && second == NONE) active = false;
    if (saved.event.pressed) {
        saved.event.pressed = false;
        if (combo_shift_owner) {
            keyevent_t owner_release = *event;
            owner_release.key = saved.event.key;
            combo_shift_owner = false;
            ak820_autoshift_before(&owner_release);
        } else {
            process_record(&saved);
        }
    }
    return false;
}
#endif
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
static bool flush(void) {
    uint8_t generation = combo_cancel_generation;
    first = NONE;
    process_record(&saved);
    return generation == combo_cancel_generation;
}
bool ak820_combo_tick(uint16_t now) {
    if (first != NONE && !active && (uint16_t)(now - saved.event.time) >= AK820_COMBO_TERM) return flush();
    return true;
}
ak820_combo_result_t ak820_combo_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id, code = record->keycode;
    if (IS_NOEVENT(record->event)) return true;
    /* Encoder pulses never become candidates. */
    if (record->event.key.row >= MATRIX_ROWS || record->event.key.col >= MATRIX_COLS) {
        if (first != NONE && !active) return flush();
        return true;
    }
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
    /* Controls are physical only and retain the full 16-bit namespace. Flush
     * before broad cancellation so a pending press is never silently lost. */
    if (record->keycode >= QK_COMBO_ON && record->keycode <= QK_COMBO_TOGGLE) {
        if (record->event.pressed) {
            bool next = record->keycode == QK_COMBO_ON || (record->keycode == QK_COMBO_TOGGLE && !enabled);
            if (next != enabled) {
                if (first != NONE && !active && !flush()) return false;
                enabled = next;
                /* Shared clear releases generated outputs and blocks their
                 * still-held physical sources, including unrelated actions. */
                clear_keyboard();
            }
        }
        return false;
    }
    if (!enabled) return true;
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
    ak820_combo_result_t eligible = false;
    if (record->event.pressed && COMBO_INPUT(record->keycode)) {
        uint8_t previous = saved.keycode;
        for (uint8_t i = 0; i < VIAL_COMBO_ENTRIES; ++i) {
            uint8_t a = combos[i].a, b = combos[i].b;
            if (a == code || b == code) {
                eligible = true;
                if (first != NONE && code != previous && (a == previous || b == previous)) {
                    second = id;
                    active = true;
#ifdef AK820_COMBO_AUTOSHIFT
                    saved = *record;
#endif
                    saved.keycode = combos[i].output;
#ifdef AK820_COMBO_AUTOSHIFT
                    combo_shift_owner = !ak820_autoshift_process(&saved);
                    if (!combo_shift_owner)
#endif
                        process_record(&saved);
                    return false;
                }
            }
        }
    }
    if (first != NONE && !flush()) return false;
    if (eligible) {
        first = id;
        saved = *record;
        return false;
    }
    return true;
}
