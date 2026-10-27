// Copyright 2021-2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "process_caps_word.h"
#include "process_auto_shift.h"
#include "caps_word.h"
#include "keycodes.h"
#include "quantum_keycodes.h"
#include "modifiers.h"
#include "timer.h"
#ifdef AK820_BOARD
#include "repeat_key.h"
#endif
#include "action_tapping.h"
#include "action_util.h"

#ifdef AK820_BOARD
/* Language controls share this main CODE unit, leaving the small state
 * machine in its independently bounded low application window. */
#ifdef __SDCC_mcs51
__bit caps_word_ru;
#else
bool caps_word_ru;
#endif
void ak820_caps_word_configure(uint8_t ru) {
    if (caps_word_ru != (ru != 0)) caps_word_off();
    caps_word_ru = ru != 0;
}
void ak820_caps_word_select(uint16_t keycode) {
    ak820_caps_word_configure(keycode == AK820_CW_LANG_TOGGLE ? !caps_word_ru : keycode == AK820_CW_LANG_RU);
}
#endif

#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
/* A pending first press must be released before another press can finish. */
#ifdef __SDCC_mcs51
static __bit shift_tap_armed;
static __bit shift_tap_released;
#else
static bool shift_tap_armed;
static bool shift_tap_released;
#endif
static uint16_t shift_tap_deadline;

void caps_word_shift_cancel(void) {
    shift_tap_armed = false;
}

void caps_word_shift_task(void) {
    if (shift_tap_armed && timer_expired(timer_read(), shift_tap_deadline)) {
        shift_tap_armed = false;
    }
}
#endif

#ifdef CAPS_WORD_INVERT_ON_SHIFT
static uint8_t held_mods = 0;

static bool handle_shift(uint16_t keycode, keyrecord_t* record) {
    //switch (keycode) {
        if (keycode == OSM(MOD_LSFT)) {
            keycode = KC_LSFT;
        }
        else if(keycode == OSM(MOD_RSFT)) {
            keycode = KC_RSFT;
        }

#    ifndef NO_ACTION_TAPPING
        else if (keycode >= QK_MOD_TAP && keycode <= QK_MOD_TAP_MAX) {
            if (record->tap.count == 0) { // Mod-tap key is held.
                switch (QK_MOD_TAP_GET_MODS(keycode)) {
                    case MOD_LSFT:
                        keycode = KC_LSFT;
                        break;
                    case MOD_RSFT:
                        keycode = KC_RSFT;
                        break;
                }
            }
        }
#    endif // NO_ACTION_TAPPING
    //}

    if (keycode == KC_LSFT || keycode == KC_RSFT) {
        const uint8_t mod = MOD_BIT(keycode);

        if (is_caps_word_on()) {
            if (record->event.pressed) {
                held_mods |= mod;
            } else {
                held_mods &= ~mod;
            }
            return false;
        } else if ((held_mods & mod) != 0) {
            held_mods &= ~mod;
            del_mods(mod);
            return record->event.pressed;
        }
    }

    return true;
}
#endif // CAPS_WORD_INVERT_ON_SHIFT

bool process_caps_word(uint16_t keycode, keyrecord_t* event_record) {
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    /* action_exec()/encoder/Vial records live in XDATA under model-large.
     * Retain the generic public ABI and avoid generic reads in this handler. */
    keyrecord_t __xdata* record = (keyrecord_t __xdata*)event_record;
#else
    keyrecord_t* record = event_record;
#endif
#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
#    ifdef __SDCC_mcs51
    __bit eligible;
#    else
    bool eligible;
#    endif
    eligible = record->event.key.row < MATRIX_ROWS && record->event.key.col < MATRIX_COLS
#    ifdef REPEAT_KEY_ENABLE
        && !get_repeat_key_count()
#    endif
        && !ak820_macro_primitive;
    /* Generated events cannot trigger gestures or language selection. */
    if ((keycode >> 8) == (AK820_CW_LANG_EN >> 8) && (uint8_t)keycode <= (uint8_t)AK820_CW_LANG_TOGGLE) {
        shift_tap_armed = false;
        if (eligible && record->event.pressed) ak820_caps_word_select(keycode);
        return false;
    }

#else
#ifdef AK820_BOARD
    if ((keycode >> 8) == (AK820_CW_LANG_EN >> 8) && (uint8_t)keycode <= (uint8_t)AK820_CW_LANG_TOGGLE) {
        if (record->event.pressed && record->event.key.row < MATRIX_ROWS && record->event.key.col < MATRIX_COLS
#ifdef REPEAT_KEY_ENABLE
            && !get_repeat_key_count()
#endif
#ifdef AK820_COMPACT_TAPPING
            && !ak820_macro_primitive
#endif
        ) ak820_caps_word_select(keycode);
        return false;
    }
#endif
#endif
    if (keycode == QK_CAPS_WORD_TOGGLE) {
#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
        shift_tap_armed = false;
#endif
        if (record->event.pressed) {
            caps_word_toggle();
        }
        return false;
    }
#ifdef CAPS_WORD_INVERT_ON_SHIFT
    if (!handle_shift(keycode, record)) {
        return false;
    }
#endif // CAPS_WORD_INVERT_ON_SHIFT

#ifndef NO_ACTION_ONESHOT
    const uint8_t mods = get_mods() | get_oneshot_mods();
#else
    const uint8_t mods = get_mods();
#endif // NO_ACTION_ONESHOT

    if (!is_caps_word_on()) {
#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
        if (!eligible) {
            shift_tap_armed = false;
        } else if (keycode != KC_LSFT && keycode != KC_RSFT) {
            if (record->event.pressed) shift_tap_armed = false;
        } else if (!record->event.pressed) {
            if (keycode == KC_LSFT && shift_tap_armed) shift_tap_released = true;
        } else {
            uint8_t shift_mods = mods | (keycode == KC_LSFT ? MOD_BIT(KC_LSFT) : MOD_BIT(KC_RSFT));
            caps_word_shift_task();
            if (shift_mods == MOD_MASK_SHIFT ||
                (keycode == KC_LSFT && shift_tap_armed && shift_tap_released && !(shift_mods & ~MOD_MASK_SHIFT))) {
                shift_tap_armed = false;
                caps_word_on();
                return true;
            }
            shift_tap_armed = false;
            if (keycode == KC_LSFT && shift_mods == MOD_BIT(KC_LSFT)) {
                shift_tap_armed = true;
                shift_tap_released = false;
                shift_tap_deadline = record->event.time + GET_TAPPING_TERM(keycode, record);
            }
        }
#endif
        // The following optionally turns on Caps Word by holding left and
        // right shifts or by double tapping left shift. This way Caps Word
        // may be used without needing a dedicated key and also without
        // needing combos or tap dance.

#if defined(BOTH_SHIFTS_TURNS_ON_CAPS_WORD) && !defined(AK820_COMPACT_TAPPING)
        // Many keyboards enable the Command feature by default, which also
        // uses left+right shift. It can be configured to use a different
        // key combination by defining IS_COMMAND(). We make a non-fatal
        // warning if Command is enabled but IS_COMMAND() is *not* defined.
#    if defined(COMMAND_ENABLE) && !defined(IS_COMMAND)
#        pragma message "BOTH_SHIFTS_TURNS_ON_CAPS_WORD and Command should not be enabled at the same time, since both use the Left Shift + Right Shift key combination. Please disable Command, or ensure that `IS_COMMAND` is not set to (get_mods() == MOD_MASK_SHIFT)."
#    else
        if (mods == MOD_MASK_SHIFT
#        ifdef COMMAND_ENABLE
            // Don't activate Caps Word at the same time as Command.
            && !(IS_COMMAND())
#        endif // COMMAND_ENABLE
        ) {
            caps_word_on();
        }
#    endif     // defined(COMMAND_ENABLE) && !defined(IS_COMMAND)
#endif         // BOTH_SHIFTS_TURNS_ON_CAPS_WORD

#if defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD) && !defined(AK820_COMPACT_TAPPING)
        // Double tapping left shift turns on Caps Word.
        //
        // NOTE: This works with KC_LSFT and one-shot left shift. It
        // wouldn't make sense with mod-tap or Space Cadet shift since
        // double tapping would of course trigger the tapping action.
        if (record->event.pressed) {
            static bool     tapped = false;
            static uint16_t timer  = 0;
            if (keycode == KC_LSFT || keycode == OSM(MOD_LSFT)) {
                if (tapped && !timer_expired(record->event.time, timer)) {
                    // Left shift was double tapped, activate Caps Word.
                    caps_word_on();
                }
                tapped = true;
                timer  = record->event.time + GET_TAPPING_TERM(keycode, record);
            } else {
                tapped = false; // Reset when any other key is pressed.
            }
        }
#endif // DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD

        return true;
    }

#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
    shift_tap_armed = false;
#endif
#if CAPS_WORD_IDLE_TIMEOUT > 0
    caps_word_reset_idle_timer();
#endif // CAPS_WORD_IDLE_TIMEOUT > 0

    // From here on, we only take action on press events.
    if (!record->event.pressed) {
        return true;
    }

    if (!(mods & ~(MOD_MASK_SHIFT | MOD_BIT(KC_RALT)))) {
        //switch (keycode) {
            // Ignore MO, TO, TG, TT, and OSL layer switch keys.
            if ( (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) ||
                 (keycode >= QK_TO               && keycode <= QK_TO_MAX) ||
                 (keycode >= QK_TOGGLE_LAYER     && keycode <= QK_TOGGLE_LAYER_MAX) ||
                 (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
                 (keycode >= QK_ONE_SHOT_LAYER   && keycode <= QK_ONE_SHOT_LAYER_MAX) ||
                 (keycode >= QK_TRI_LAYER_LOWER  && keycode <= QK_TRI_LAYER_UPPER) ||
            // Ignore AltGr.
                 (keycode == KC_RALT) ||
                 (keycode == OSM(MOD_RALT)) )
                return true;

#ifndef NO_ACTION_TAPPING
            // Corresponding to mod keys above, a held mod-tap is handled as:
            // * For shift mods, pass KC_LSFT or KC_RSFT to
            //   caps_word_press_user() to determine whether to continue.
            // * For Shift + AltGr (MOD_RSFT | MOD_RALT), pass RSFT(KC_RALT).
            // * AltGr (MOD_RALT) is ignored.
            // * Otherwise stop Caps Word.
            else if (keycode >= QK_MOD_TAP && keycode <= QK_MOD_TAP_MAX) {
                if (record->tap.count == 0) { // Mod-tap key is held.
                    const uint8_t mods = QK_MOD_TAP_GET_MODS(keycode);
                    switch (mods) {
#    ifndef CAPS_WORD_INVERT_ON_SHIFT
                        case MOD_LSFT:
                            keycode = KC_LSFT;
                            break;
                        case MOD_RSFT:
                            keycode = KC_RSFT;
                            break;
#    endif // CAPS_WORD_INVERT_ON_SHIFT
                        case MOD_RSFT | MOD_RALT:
                            keycode = RSFT(KC_RALT);
                            break;
                        case MOD_RALT:
                            return true;
                        default:
                            caps_word_off();
#    ifdef CAPS_WORD_INVERT_ON_SHIFT
                            add_mods(held_mods);
#    endif // CAPS_WORD_INVERT_ON_SHIFT
                            return true;
                    }
                } else {
                    keycode = QK_MOD_TAP_GET_TAP_KEYCODE(keycode);
                }
                //break;
            }

#    ifndef NO_ACTION_LAYER
            else if (keycode >= QK_LAYER_TAP && keycode <= QK_LAYER_TAP_MAX) {
#    endif // NO_ACTION_LAYER
                if (record->tap.count == 0) {
                    return true;
                }
                keycode = QK_LAYER_TAP_GET_TAP_KEYCODE(keycode);
            //    break;
            }
#endif // NO_ACTION_TAPPING

#ifdef SWAP_HANDS_ENABLE
            else if (keycode >= QK_SWAP_HANDS && keycode <= QK_SWAP_HANDS_MAX) {
                // Note: IS_SWAP_HANDS_KEYCODE() actually tests for the special action keycodes like SH_TOGG, SH_TT, ...,
                // which currently overlap the SH_T(kc) range.
                if (IS_SWAP_HANDS_KEYCODE(keycode)
#    ifndef NO_ACTION_TAPPING
                    || record->tap.count == 0
#    endif // NO_ACTION_TAPPING
                ) {
                    return true;
                }
                keycode = QK_SWAP_HANDS_GET_TAP_KEYCODE(keycode);
            //    break;
            }
#endif // SWAP_HANDS_ENABLE
        //}

#ifdef AUTO_SHIFT_ENABLE
        del_weak_mods(get_autoshift_state() ? ~MOD_BIT(KC_LSFT) : 0xff);
#else
        clear_weak_mods();
#endif // AUTO_SHIFT_ENABLE
        if (caps_word_press_user(keycode)) {
#ifdef CAPS_WORD_INVERT_ON_SHIFT
            if (held_mods) {
                set_weak_mods(get_weak_mods() ^ MOD_BIT(KC_LSFT));
            }
#endif // CAPS_WORD_INVERT_ON_SHIFT
            send_keyboard_report();
            return true;
        }
    }

    caps_word_off();
#ifdef CAPS_WORD_INVERT_ON_SHIFT
    add_mods(held_mods);
#endif // CAPS_WORD_INVERT_ON_SHIFT
    return true;
}
