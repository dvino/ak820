// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include "tri_layer.h"
#include <stdint.h>
#ifdef AK820_COMPACT_TAPPING
#include "action_layer.h"
_Static_assert(TRI_LAYER_LOWER_LAYER < MAX_LAYER && TRI_LAYER_UPPER_LAYER < MAX_LAYER && TRI_LAYER_ADJUST_LAYER < MAX_LAYER && TRI_LAYER_LOWER_LAYER != TRI_LAYER_UPPER_LAYER && TRI_LAYER_LOWER_LAYER != TRI_LAYER_ADJUST_LAYER && TRI_LAYER_UPPER_LAYER != TRI_LAYER_ADJUST_LAYER, "distinct supported Tri Layer configuration");
#endif

static uint8_t tri_layer_lower_layer  = TRI_LAYER_LOWER_LAYER;
static uint8_t tri_layer_upper_layer  = TRI_LAYER_UPPER_LAYER;
static uint8_t tri_layer_adjust_layer = TRI_LAYER_ADJUST_LAYER;
#ifdef AK820_COMPACT_TAPPING
/* Only the validated setters below change these targets. Cache their masks
 * there so every layer owner update needs one derived-bit test. */
static uint8_t tri_inputs = (1u << TRI_LAYER_LOWER_LAYER) | (1u << TRI_LAYER_UPPER_LAYER);
static uint8_t tri_adjust = 1u << TRI_LAYER_ADJUST_LAYER;
uint8_t ak820_tri_layer_derived(uint8_t state) {
    return (state & tri_inputs) == tri_inputs ? tri_adjust : 0;
}
static void tri_layer_changed(void) {
    tri_inputs = (1u << tri_layer_lower_layer) | (1u << tri_layer_upper_layer);
    tri_adjust = 1u << tri_layer_adjust_layer;
    ak820_layer_refresh();
}
#endif


void set_tri_layer_lower_layer(uint8_t layer) {
#ifdef AK820_COMPACT_TAPPING
    if (layer >= MAX_LAYER || layer == tri_layer_upper_layer || layer == tri_layer_adjust_layer) return;
#endif
    tri_layer_lower_layer = layer;
#ifdef AK820_COMPACT_TAPPING
    tri_layer_changed();
#endif
}

void set_tri_layer_upper_layer(uint8_t layer) {
#ifdef AK820_COMPACT_TAPPING
    if (layer >= MAX_LAYER || layer == tri_layer_lower_layer || layer == tri_layer_adjust_layer) return;
#endif
    tri_layer_upper_layer = layer;
#ifdef AK820_COMPACT_TAPPING
    tri_layer_changed();
#endif
}

void set_tri_layer_adjust_layer(uint8_t layer) {
#ifdef AK820_COMPACT_TAPPING
    if (layer >= MAX_LAYER || layer == tri_layer_lower_layer || layer == tri_layer_upper_layer) return;
#endif
    tri_layer_adjust_layer = layer;
#ifdef AK820_COMPACT_TAPPING
    tri_layer_changed();
#endif
}

void set_tri_layer_layers(uint8_t lower, uint8_t raise, uint8_t adjust) {
#ifdef AK820_COMPACT_TAPPING
    if (lower >= MAX_LAYER || raise >= MAX_LAYER || adjust >= MAX_LAYER || lower == raise || lower == adjust || raise == adjust) return;
#endif
    tri_layer_lower_layer  = lower;
    tri_layer_upper_layer  = raise;
    tri_layer_adjust_layer = adjust;
#ifdef AK820_COMPACT_TAPPING
    tri_layer_changed();
#endif
}

uint8_t get_tri_layer_lower_layer(void) {
    return tri_layer_lower_layer;
}

uint8_t get_tri_layer_upper_layer(void) {
    return tri_layer_upper_layer;
}

uint8_t get_tri_layer_adjust_layer(void) {
    return tri_layer_adjust_layer;
}
