/* SPDX-License-Identifier: GPL-3.0-only */
#pragma once
#include <stdint.h>

#define AK820_OS_INDICATOR_LEASE_MS 3000u
#define AK820_OS_INDICATOR_PERIOD_MS 4096u
enum { AK820_OS_NORMAL, AK820_OS_OFF, AK820_OS_ON, AK820_OS_BREATHE };

/* USB lifecycle callbacks only clear this byte. No foreground helper is
 * called by an interrupt; timestamp and waveform work stay in main. */
extern volatile uint8_t ak820_os_indicator_mode;
/* Caller owns the Raw HID request and excludes interrupts while publishing. */
void ak820_os_indicator_set(uint8_t mode);
uint8_t ak820_os_indicator_get(void);
uint8_t ak820_os_indicator_value(uint8_t normal);
