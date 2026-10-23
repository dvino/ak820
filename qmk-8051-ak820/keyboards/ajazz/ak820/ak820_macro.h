/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once
#include <stdbool.h>
#include <stdint.h>

/* Schema 0x082002: outside six keymaps/encoders and all 8192 macro bytes.
 * The committed logical length is little endian at 07F1..07F2. */
#define AK820_MACRO_BUSY_ADDR 0x07F0u
#define AK820_MACRO_LENGTH_ADDR (AK820_MACRO_BUSY_ADDR + 1)

void ak820_macro_init(void);
bool ak820_macro_ready(void);
uint16_t ak820_macro_length(void);
bool ak820_macro_write(uint16_t offset, uint16_t size, const uint8_t *data);
bool ak820_macro_reset(void);
