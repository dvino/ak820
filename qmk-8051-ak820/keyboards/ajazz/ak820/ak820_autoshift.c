// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_autoshift.h"
#ifdef AK820_QMK_SETTINGS
#    include "ak820_settings.h"
#    define AK820_AUTOSHIFT_TERM ak820_settings_autoshift_timeout()
#else
#    define AK820_AUTOSHIFT_TERM 175
#endif

/* One source owns the deferred press and its eventual release. Generated
 * records never enter these hooks. Tapping's source guard rejects duplicates
 * and blocks held sources after clear_keyboard(). */
static keyrecord_t as_saved;
static uint8_t as_state; /* 0 idle, 1 pending, 2 plain down, 3 shifted down */
/* Upstream QSID 3 bits: enabled, no special, no numeric, no alpha. */
static uint8_t as_flags = 1;
void ak820_autoshift_configure(uint8_t flags) { as_flags = flags; }

static void as_emit(bool shifted) {
    as_state = shifted ? 3 : 2;
    if (shifted) add_owned_mods(MOD_BIT(KC_LEFT_SHIFT));
    process_record(&as_saved);
}
bool ak820_autoshift_before(const keyevent_t AK820_STATE_MEM *event) {
    if (!as_state) return true;
    if (as_state == 1 && (uint16_t)(event->time - as_saved.event.time) >= AK820_AUTOSHIFT_TERM) {
        as_emit(true);
        if (!as_state) return false;
    }
    if (IS_NOEVENT(*event)) return true;
    if (event->key.row == as_saved.event.key.row && event->key.col == as_saved.event.key.col) {
        if (!event->pressed) {
            if (as_state == 1) {
                as_emit(false);
                if (!as_state) return false;
            }
            uint8_t state = as_state;
            as_state = 0;
            as_saved.event.pressed = false;
            process_record(&as_saved);
            if (state == 3) {
                del_owned_mods(MOD_BIT(KC_LEFT_SHIFT));
                send_keyboard_report();
            }
        }
        return false;
    }
    if (as_state == 1 && event->pressed) as_emit(false);
    return true;
}
bool ak820_autoshift_process(keyrecord_t AK820_STATE_MEM *record) {
    uint16_t code = record->keycode;
    if (record->event.key.row >= MATRIX_ROWS || record->event.key.col >= MATRIX_COLS) return true;
    if (code >= QK_AUTO_SHIFT_ON && code <= QK_AUTO_SHIFT_TOGGLE) {
        if (record->event.pressed)
            as_flags = code == QK_AUTO_SHIFT_TOGGLE ? as_flags ^ 1 :
                (as_flags & ~1) | (code == QK_AUTO_SHIFT_ON);
        return false;
    }
    if (!(as_flags & 1) || as_state || !record->event.pressed || get_mods() || get_weak_mods()) return true;
    if (!((code >= KC_A && code <= KC_0) ||
          (code >= KC_MINUS && code <= KC_SLASH) || code == KC_NONUS_BACKSLASH)) return true;
    if (code <= KC_Z ? (as_flags & 16) :
        code <= KC_0 ? (as_flags & 8) : (as_flags & 4)) return true;
    as_saved = *record;
    as_state = 1;
    return false;
}
void ak820_autoshift_cancel(void) { as_state = 0; }
