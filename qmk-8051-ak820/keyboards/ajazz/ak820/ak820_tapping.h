// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
/* before() runs before any press-time layer lookup. process() consumes only
 * physical dual-role records; generated Repeat records bypass both hooks. */
bool ak820_tapping_before(const keyevent_t AK820_STATE_MEM *event);
bool ak820_tapping_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_tapping_cancel(void);
