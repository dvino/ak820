// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "action.h"
#include "action_util.h"
#include "vial.h"

bool ak820_key_override_valid(const vial_key_override_entry_t AK820_STATE_MEM *entry);
void ak820_key_override_reload(void);
void ak820_key_override_cancel(void);
/* Physical events after tapping/Repeat/Caps Word bookkeeping. false consumes
 * the event. mods is the unsuppressed effective modifier state. */
bool ak820_key_override_process(keyrecord_t AK820_STATE_MEM *record, uint8_t mods, uint8_t layer);
/* Before report projection, including reports caused by modifier changes. */
void ak820_key_override_sync(uint8_t mods, uint8_t layer);
/* Project this owner's key into the outgoing copy, without changing key refs.
 * Apply mods() to the aggregate before Mac/PC conversion. */
uint8_t ak820_key_override_key(void);
uint8_t ak820_key_override_mods(uint8_t mods);
bool ak820_key_override_enabled(void);
