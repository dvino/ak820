/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once

#include <stdbool.h>
#include <stdint.h>

/* EP81 keyboard, EP82 shared HID, EP83 Raw HID IN; Raw OUT uses EP0. */
/* Private target API: all callers own model-large XDATA report storage. */
bool ak820_usb_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length);
/* Main-loop retries must never wait on an occupied endpoint or publish an
 * old report while a reset/protocol/resume cleanup is pending. */
bool ak820_usb_try_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length);
void ak820_usb_raw_task(void);
void ak820_usb_raw_send(const uint8_t *report, uint8_t length);
bool ak820_usb_take_keyboard_reset(void);

/* Written only by main; EP0 exposes a read-only 8-byte AKBT Feature report. */
extern volatile __xdata uint8_t ak820_boot_stage;
extern volatile __xdata uint8_t ak820_main_heartbeat;


#ifdef AK820_COMPACT_DYNAMIC_MACRO
bool ak820_usb_keyboard_blocked(void);
#endif
