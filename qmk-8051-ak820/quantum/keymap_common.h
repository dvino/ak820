// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#include <stdint.h>
#include "keyboard.h"

// translates key to keycode
uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key);

#ifdef AK820_BOARD
/* Private scalar form for the pinned AK820 pipeline. Unlike keypos_t passed
 * by value, this travels through SDCC registers without a generic memcpy.
 * Callers pass a local position expression with no side effects. */
#define AK820_KEYPOS_VALUE(key) (((uint16_t)(key).row << 8) | (key).col)
uint16_t ak820_keycode_at(uint8_t layer, uint16_t position);
#endif
