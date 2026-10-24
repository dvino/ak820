// Copyright 2022-2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
// Unchanged behavior from dvino/ak820 38ad013, renamed for differential tests.
static bool reference_remember_last_key(uint16_t keycode, keyrecord_t* record, uint8_t* remembered_mods) {
    /* Layer/modifier controls are not repeatable actions. Include LM and DF,
     * too: replaying LM from a Repeat key would create an unowned held layer. */
    if (keycode == KC_NO || keycode == KC_TRANSPARENT ||
        (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) ||
        (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) ||
        (keycode >= QK_DEF_LAYER && keycode <= QK_DEF_LAYER_MAX) ||
        (keycode >= QK_TO && keycode <= QK_TO_MAX) ||
        (keycode >= QK_TOGGLE_LAYER && keycode <= QK_TOGGLE_LAYER_MAX) ||
        (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
        (keycode >= KC_LCTL && keycode <= KC_RGUI) ||
        keycode == KC_HYPR || keycode == KC_MEH || keycode == QK_REPEAT_KEY
#ifndef NO_ALT_REPEAT_KEY
        || keycode == QK_ALT_REPEAT_KEY
#endif
#if !defined(NO_ACTION_ONESHOT) || defined(AK820_COMPACT_ONESHOT)
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
