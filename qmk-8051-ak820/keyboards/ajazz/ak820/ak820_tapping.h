// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
/* before() runs before any press-time layer lookup. process() consumes only
 * physical dual-role records; generated Repeat records bypass both hooks. */
bool ak820_tapping_before(const keyevent_t AK820_STATE_MEM *event);
bool ak820_tapping_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_tapping_cancel(void);
#ifdef __SDCC_mcs51
uint8_t ak820_tapping_source_ptr(const keypos_t AK820_STATE_MEM *key);
#endif

#ifdef AK820_COMPACT_ONESHOT
uint8_t ak820_tapping_source(keypos_t key);
bool ak820_oneshot_process(uint16_t code, uint8_t id, bool pressed);
void ak820_oneshot_tick(uint16_t now);
void ak820_oneshot_post(uint8_t id, bool pressed);
void ak820_oneshot_cancel(void);
#endif
