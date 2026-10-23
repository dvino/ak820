// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include "process_tri_layer.h"
#include "tri_layer.h"
#include "action_layer.h"

bool process_tri_layer(uint16_t keycode, keyrecord_t *record) {
    uint8_t layer;
    if (keycode == QK_TRI_LAYER_LOWER) {
        layer = get_tri_layer_lower_layer();
    } else if (keycode == QK_TRI_LAYER_UPPER) {
        layer = get_tri_layer_upper_layer();
    } else {
        return true;
    }
    if (record->event.pressed) {
        layer_on(layer);
    } else {
        layer_off(layer);
    }
    update_tri_layer(get_tri_layer_lower_layer(), get_tri_layer_upper_layer(), get_tri_layer_adjust_layer());
    return false;
}
