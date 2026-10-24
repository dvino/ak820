// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
bool ak820_dynamic_macro_process(uint16_t code, bool pressed);
void ak820_dynamic_macro_observe(uint8_t code, bool pressed);
void ak820_dynamic_macro_task(uint16_t now);
void ak820_dynamic_macro_cancel(void);
/* Scoped to physical action handlers; generated/macro output is excluded. */
extern bool ak820_dynamic_macro_source;
/* Latest report is pending, or USB is suspended/unconfigured/resetting. */
bool ak820_keyboard_report_pending(void);
