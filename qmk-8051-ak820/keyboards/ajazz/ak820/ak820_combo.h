// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
#include "vial.h"
bool ak820_combo_valid(const vial_combo_entry_t AK820_STATE_MEM *entry);
void ak820_combo_reload(void);
void ak820_combo_tick(uint16_t now);
bool ak820_combo_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_combo_cancel(void);
