// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once

/* Schema 3 extends only the previously unused post-Combo gap. Each typed
 * record fits a single 64-byte journal page, including entries 6 and 7. */
#define AK820_SETTINGS_ADDR 0x06a8u
#define AK820_SETTINGS_SIZE 24u
#define AK820_TAP_DANCE_ADDR 0x06c0u
#define AK820_KEY_OVERRIDE_ADDR 0x0740u
#define AK820_EXTENSION_ENTRIES 8u
#define AK820_EXTENSION_SLOT_SIZE 10u
#define AK820_EXTENSION_OFFSET(i) ((i) < 6 ? (i) * 10u : 64u + ((i) - 6u) * 10u)
