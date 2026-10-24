// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
#include "vial.h"
bool ak820_tap_dance_valid(const vial_tap_dance_entry_t AK820_STATE_MEM *entry);
bool ak820_tap_dance_before(const keyevent_t AK820_STATE_MEM *event);
bool ak820_tap_dance_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_tap_dance_task(uint16_t now);
void ak820_tap_dance_cancel(void);
