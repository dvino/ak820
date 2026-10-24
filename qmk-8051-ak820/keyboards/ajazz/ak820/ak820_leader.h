// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
bool ak820_leader_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_leader_task(uint16_t now);
void ak820_leader_cancel(void);
