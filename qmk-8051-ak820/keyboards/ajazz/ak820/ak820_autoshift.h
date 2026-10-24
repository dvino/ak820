// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
/* Physical events only; run before lookup and after tapping admission. */
bool ak820_autoshift_before(const keyevent_t AK820_STATE_MEM *event);
bool ak820_autoshift_process(keyrecord_t AK820_STATE_MEM *record);
/* Shared clear path also clears modifier/key refs and blocks held sources. */
void ak820_autoshift_cancel(void);
