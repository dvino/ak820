// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
#include "vial.h"

/* These internal predicates return carry on SDCC; host callers retain bool. */
#if defined(__SDCC_mcs51)
typedef __bit ak820_combo_result_t;
#else
typedef bool ak820_combo_result_t;
#endif
ak820_combo_result_t ak820_combo_valid(const vial_combo_entry_t AK820_STATE_MEM *entry);
void ak820_combo_reload(void);
void ak820_combo_tick(uint16_t now);
ak820_combo_result_t ak820_combo_process(keyrecord_t AK820_STATE_MEM *record);
void ak820_combo_cancel(void);
