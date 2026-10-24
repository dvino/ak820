// Copyright 2022-2023 Google LLC
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

#include "process_repeat_key.h"
#include "repeat_key.h"
#include "keycodes.h"
#include "quantum_keycodes.h"
#include "action_util.h"

// Default implementation of remember_last_key_user().
__attribute__((weak)) bool remember_last_key_user(uint16_t keycode, keyrecord_t* record, uint8_t* remembered_mods) {
    return true;
}

static bool remember_last_key(uint16_t keycode, keyrecord_t* record, uint8_t* remembered_mods) {
    /* Layer/modifier controls are not repeatable actions. Include LM and DF,
     * too: replaying LM from a Repeat key would create an unowned held layer. */
#ifdef AK820_BOARD
    _Static_assert(QK_TO == QK_LAYER_MOD_MAX + 1 && QK_MOMENTARY == QK_TO_MAX + 1 &&
                   QK_DEF_LAYER == QK_MOMENTARY_MAX + 1 && QK_TOGGLE_LAYER == QK_DEF_LAYER_MAX + 1 &&
                   QK_ONE_SHOT_LAYER == QK_TOGGLE_LAYER_MAX + 1 && QK_ONE_SHOT_MOD == QK_ONE_SHOT_LAYER_MAX + 1 &&
                   QK_LAYER_TAP_TOGGLE == QK_ONE_SHOT_MOD_MAX + 1,
                   "AK820 Repeat layer-control ranges must remain contiguous");
#endif
    if (keycode == KC_NO || keycode == KC_TRANSPARENT ||
#ifdef AK820_BOARD
#    if !defined(NO_ACTION_ONESHOT) || defined(AK820_COMPACT_ONESHOT)
        (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
#    else
        (keycode >= QK_LAYER_MOD && keycode <= QK_TOGGLE_LAYER_MAX) ||
        (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
#    endif
#else
        (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) ||
        (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) ||
        (keycode >= QK_DEF_LAYER && keycode <= QK_DEF_LAYER_MAX) ||
        (keycode >= QK_TO && keycode <= QK_TO_MAX) ||
        (keycode >= QK_TOGGLE_LAYER && keycode <= QK_TOGGLE_LAYER_MAX) ||
        (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
#endif
        (keycode >= KC_LCTL && keycode <= KC_RGUI) ||
        keycode == KC_HYPR || keycode == KC_MEH || keycode == QK_REPEAT_KEY
#ifndef NO_ALT_REPEAT_KEY
        || keycode == QK_ALT_REPEAT_KEY
#endif
#if !defined(AK820_BOARD) && (!defined(NO_ACTION_ONESHOT) || defined(AK820_COMPACT_ONESHOT))
        || (keycode >= QK_ONE_SHOT_LAYER && keycode <= QK_ONE_SHOT_LAYER_MAX)
        || (keycode >= QK_ONE_SHOT_MOD && keycode <= QK_ONE_SHOT_MOD_MAX)
#endif
#ifdef TRI_LAYER_ENABLE
        || keycode == QK_TRI_LAYER_LOWER || keycode == QK_TRI_LAYER_UPPER
#endif
        ) return false;
#ifndef NO_ACTION_TAPPING
    if (((keycode >= QK_MOD_TAP && keycode <= QK_MOD_TAP_MAX)
#ifndef NO_ACTION_LAYER
         || (keycode >= QK_LAYER_TAP && keycode <= QK_LAYER_TAP_MAX)
#endif
        ) && record->tap.count == 0) return false;
#endif
#ifdef SWAP_HANDS_ENABLE
    if (keycode >= QK_SWAP_HANDS && keycode <= QK_SWAP_HANDS_MAX &&
        (IS_SWAP_HANDS_KEYCODE(keycode) || record->tap.count == 0)) return false;
#endif

    return remember_last_key_user(keycode, record, remembered_mods);
}

bool process_last_key(uint16_t keycode, keyrecord_t* record) {
    if (get_repeat_key_count()) {
        return true;
    }

    if (record->event.pressed) {
        uint8_t remembered_mods = get_mods() | get_weak_mods();
#ifndef NO_ACTION_ONESHOT
        remembered_mods |= get_oneshot_mods();
#endif // NO_ACTION_ONESHOT

        if (remember_last_key(keycode, record, &remembered_mods)) {
            set_last_record(keycode, record);
            set_last_mods(remembered_mods);
        }
    }

    return true;
}

bool process_repeat_key(uint16_t keycode, keyrecord_t* record) {
    if (get_repeat_key_count()) {
        return true;
    }

    if (keycode == QK_REPEAT_KEY) {
        repeat_key_invoke(&record->event);
        return false;
#ifndef NO_ALT_REPEAT_KEY
    } else if (keycode == QK_ALT_REPEAT_KEY) {
        alt_repeat_key_invoke(&record->event);
        return false;
#endif // NO_ALT_REPEAT_KEY
    }

    return true;
}
