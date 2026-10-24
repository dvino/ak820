// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "ak820_nvm.h"

#include "ak820_extensions.h"
#define AK820_SETTINGS_VERSION 1u
#define AK820_SETTINGS_CAPABILITIES 0x3Fu

/* Vial buffers may contain trailing packet padding; capacity is the buffer size,
 * not the setting width. Values themselves have exactly the documented width. */
void ak820_settings_init(void);
void ak820_settings_query(uint16_t greater_than, uint8_t AK820_XDATA *buffer, uint8_t size);
int ak820_settings_get(uint16_t qsid, uint8_t AK820_XDATA *buffer, uint8_t capacity);
int ak820_settings_set(uint16_t qsid, const uint8_t AK820_XDATA *buffer, uint8_t capacity);
int ak820_settings_reset(void);
uint8_t ak820_settings_grave_esc(void);
uint16_t ak820_settings_combo_term(void);
uint16_t ak820_settings_tapping_term(void);
uint16_t ak820_settings_tap_code_delay(void);
uint16_t ak820_settings_caps_delay(void);
uint16_t ak820_settings_autoshift_timeout(void);
