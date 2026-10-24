/* Copyright 2020
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "process_grave_esc.h"
#include "qmk_settings.h"
#include "keycodes.h"
#include "modifiers.h"
#include "action_util.h"
#ifdef AK820_BOARD
#    include "action_layer.h"
#    include "keymap_common.h"
#    if defined(AK820_COMPACT_TAPPING) && defined(REPEAT_KEY_ENABLE)
#        include "repeat_key.h"
#    endif
#endif

/* true if the last press of QK_GRAVE_ESCAPE was shifted (i.e. GUI or SHIFT were pressed), false otherwise.
 * Used to ensure that the correct keycode is released if the key is released.
 */
static bool grave_esc_was_shifted = false;

bool process_grave_esc(uint16_t keycode, keyrecord_t *record_argument) {
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    keyrecord_t __xdata *record = (keyrecord_t __xdata *)record_argument;
#else
    keyrecord_t *record = record_argument;
#endif
    if (keycode == QK_GRAVE_ESCAPE) {
        /* Repeat restores remembered modifiers as weak mods. Use the
         * effective state so shifted Grave repeats Grave, not Escape. */
        const uint8_t mods    = get_mods() | get_weak_mods();
        uint8_t       shifted = mods & MOD_MASK_SG;

if (QS_grave_esc_alt_override) {
        // if ALT is pressed, ESC is always sent
        // this is handy for the cmd+opt+esc shortcut on macOS, among other things.
        if (mods & MOD_MASK_ALT) {
            shifted = 0;
        }
}

if (QS_grave_esc_ctrl_override) {
        // if CTRL is pressed, ESC is always sent
        // this is handy for the ctrl+shift+esc shortcut on windows, among other things.
        if (mods & MOD_MASK_CTRL) {
            shifted = 0;
        }
}

if (QS_grave_esc_gui_override) {
        // if GUI is pressed, ESC is always sent
        if (mods & MOD_MASK_GUI) {
            shifted = 0;
        }
}

if (QS_grave_esc_shift_override) {
        // if SHIFT is pressed, ESC is always sent
        if (mods & MOD_MASK_SHIFT) {
            shifted = 0;
        }
}

        if (record->event.pressed) {
#ifdef AK820_BOARD
            /* A physical GESC and a repeated/second GESC can overlap with
             * different modifiers. Save each resolved release separately. */
            uint16_t resolved = shifted ? KC_GRAVE : KC_ESCAPE;
#    if defined(COMBO_ENABLE) || defined(REPEAT_KEY_ENABLE)
#        if defined(AK820_COMPACT_TAPPING) && defined(REPEAT_KEY_ENABLE)
            /* Compact physical records also carry a keycode. Only Repeat
             * stores its resolved action in a retained synthetic record;
             * physical/encoder releases need the source cache updated. */
            if (get_repeat_key_count()) {
#        else
            if (record->keycode) {
#        endif
                record->keycode = resolved;
            } else
#    endif
            if (!ak820_cache_keycode(AK820_KEYPOS_VALUE(record->event.key), resolved)) {
                grave_esc_was_shifted = shifted;
            }
#else
            grave_esc_was_shifted = shifted;
#endif
#ifdef AK820_COMPACT_TAPPING
            register_code(shifted ? KC_GRAVE : KC_ESCAPE);
#else
            add_key(shifted ? KC_GRAVE : KC_ESCAPE);
#endif
        } else {
#ifdef AK820_COMPACT_TAPPING
            unregister_code(grave_esc_was_shifted ? KC_GRAVE : KC_ESCAPE);
#else
            del_key(grave_esc_was_shifted ? KC_GRAVE : KC_ESCAPE);
#endif
        }

#ifndef AK820_COMPACT_TAPPING
        send_keyboard_report();
#endif
        return false;
    }

    // Not a grave keycode so continue processing
    return true;
}
