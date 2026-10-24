// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include "process_tri_layer.h"
#include "tri_layer.h"
#include "action_layer.h"
#include "keymap_common.h"
#ifdef AK820_COMPACT_TAPPING
#include "action_util.h"
static uint8_t macro_targets[2] = {255, 255};
void clear_macro_tri_layer(void) { macro_targets[0] = macro_targets[1] = 255; }
#endif
#if defined(AK820_COMPACT_TAPPING) && defined(REPEAT_KEY_ENABLE)
#include "repeat_key.h"
#endif

bool process_tri_layer(uint16_t keycode, keyrecord_t *record_argument) {
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    keyrecord_t __xdata *record = (keyrecord_t __xdata *)record_argument;
#else
    keyrecord_t *record = record_argument;
#endif
    uint8_t layer;
    if (keycode == QK_TRI_LAYER_LOWER) {
        layer = get_tri_layer_lower_layer();
    } else if (keycode == QK_TRI_LAYER_UPPER) {
        layer = get_tri_layer_upper_layer();
    } else {
        return true;
    }
#ifdef AK820_COMPACT_TAPPING
    if (ak820_macro_primitive) {
        uint8_t role = keycode == QK_TRI_LAYER_UPPER;
        if (record->event.pressed) {
            if (macro_targets[role] == 255) macro_targets[role] = layer;
        } else if (macro_targets[role] == 255) return false;
        layer = macro_targets[role];
        if (!record->event.pressed) macro_targets[role] = 255;
    }
#endif
    if (record->event.pressed) {
#ifdef AK820_COMPACT_TAPPING
        /* Freeze the resolved target, not the mutable Lower/Upper role.
         * The cache rejects virtual positions; explicit Repeat records must
         * not replace the physical Repeat key's cache. */
#    ifdef REPEAT_KEY_ENABLE
        if (!get_repeat_key_count())
#    endif
            ak820_cache_keycode(AK820_KEYPOS_VALUE(record->event.key), QK_MOMENTARY + layer);
#endif
        layer_hold_on(layer);
    } else {
        layer_hold_off(layer);
    }
#ifndef AK820_COMPACT_TAPPING
    update_tri_layer(get_tri_layer_lower_layer(), get_tri_layer_upper_layer(), get_tri_layer_adjust_layer());
#endif
    return false;
}
