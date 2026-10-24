#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

/* Copyright 2017 Jason Williams (Wilba)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "dynamic_keymap.h"
#include "keymap_introspection.h"
#include "action.h"
#include "eeprom.h"
#include "progmem.h"
#include "send_string.h"
#include "keycodes.h"
#include "action_tapping.h"
#include "wait.h"
#include <string.h>

#ifdef AK820_BOARD
#    include "ak820_macro.h"
#    include "ak820_nvm.h"
#    include "ak820_extensions.h"
#    ifdef AK820_COMPACT_TAP_DANCE
#        include "ak820_tap_dance.h"
#    endif
#    ifdef AK820_COMPACT_KEY_OVERRIDE
#        include "ak820_key_override.h"
#    endif
#    ifdef AK820_QMK_SETTINGS
#        include "ak820_settings.h"
#    endif
#    ifdef AK820_COMPACT_COMBO
#        include "ak820_combo.h"
#    endif
#    ifdef AK820_COMPACT_TAPPING
#        include "action_util.h"
#    endif
#endif

#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* These three buffer APIs are reached only by the32-byte Raw HID dispatcher.
 * Keep their public generic-pointer ABI, but use the actual XDATA packet space
 * and explicitly validate the28-byte payload before narrowing loop counters. */
#    define DYNAMIC_BUFFER_MEM __xdata
typedef uint8_t dynamic_buffer_size_t;
#else
#    define DYNAMIC_BUFFER_MEM
typedef uint16_t dynamic_buffer_size_t;
#endif

#ifdef VIA_ENABLE
#    include "via.h"
#    define DYNAMIC_KEYMAP_EEPROM_START (VIA_EEPROM_CONFIG_END)
#else
#    include "eeconfig.h"
#    define DYNAMIC_KEYMAP_EEPROM_START (EECONFIG_SIZE)
#endif

#ifdef VIAL_ENABLE
#include "vial.h"
#endif

#ifdef ENCODER_ENABLE
#    include "encoder.h"
#else
#    define NUM_ENCODERS 0
#endif

#ifndef TOTAL_EEPROM_BYTE_COUNT
#    error Unknown total EEPROM size. Cannot derive maximum for dynamic keymaps.
#endif

#ifndef DYNAMIC_KEYMAP_EEPROM_MAX_ADDR
#    define DYNAMIC_KEYMAP_EEPROM_MAX_ADDR (TOTAL_EEPROM_BYTE_COUNT - 1)
#endif

#if DYNAMIC_KEYMAP_EEPROM_MAX_ADDR > (TOTAL_EEPROM_BYTE_COUNT - 1)
#    pragma message STR(DYNAMIC_KEYMAP_EEPROM_MAX_ADDR) " > " STR((TOTAL_EEPROM_BYTE_COUNT - 1))
#    error DYNAMIC_KEYMAP_EEPROM_MAX_ADDR is configured to use more space than what is available for the selected EEPROM driver
#endif

// Due to usage of uint16_t check for max 65535
#if DYNAMIC_KEYMAP_EEPROM_MAX_ADDR > 65535
#    pragma message STR(DYNAMIC_KEYMAP_EEPROM_MAX_ADDR) " > 65535"
#    error DYNAMIC_KEYMAP_EEPROM_MAX_ADDR must be less than 65536
#endif

// If DYNAMIC_KEYMAP_EEPROM_ADDR not explicitly defined in config.h,
#ifndef DYNAMIC_KEYMAP_EEPROM_ADDR
#    define DYNAMIC_KEYMAP_EEPROM_ADDR DYNAMIC_KEYMAP_EEPROM_START
#endif

// Encoders are located right after the dynamic keymap
#define VIAL_ENCODERS_EEPROM_ADDR (DYNAMIC_KEYMAP_EEPROM_ADDR + (DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2))
#define DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR VIAL_ENCODERS_EEPROM_ADDR

#define VIAL_ENCODERS_SIZE (NUM_ENCODERS * DYNAMIC_KEYMAP_LAYER_COUNT * 2 * 2)

// QMK settings area is just past encoders
#define VIAL_QMK_SETTINGS_EEPROM_ADDR (VIAL_ENCODERS_EEPROM_ADDR + VIAL_ENCODERS_SIZE)

#ifdef QMK_SETTINGS
#include "qmk_settings.h"
#define VIAL_QMK_SETTINGS_SIZE (sizeof(qmk_settings_t))
#else
#define VIAL_QMK_SETTINGS_SIZE 0
#endif

// Tap-dance
#ifdef AK820_COMPACT_TAP_DANCE
#define VIAL_TAP_DANCE_EEPROM_ADDR AK820_TAP_DANCE_ADDR
#else
#define VIAL_TAP_DANCE_EEPROM_ADDR (VIAL_QMK_SETTINGS_EEPROM_ADDR + VIAL_QMK_SETTINGS_SIZE)
#endif

#ifdef VIAL_TAP_DANCE_ENABLE
#define VIAL_TAP_DANCE_SIZE (sizeof(vial_tap_dance_entry_t) * VIAL_TAP_DANCE_ENTRIES)
#else
#define VIAL_TAP_DANCE_SIZE 0
#endif

// Combos
#ifdef AK820_COMPACT_COMBO
/* Additive v1 extension: each 10-byte slot stays within one journal page.
 * The standard packet reserves input[2:4] for more keys; storage uses them
 * as version markers, while the wire representation keeps them zero. */
#define AK820_COMBO_MARKER 0x0820
#define AK820_COMBO_VERSION 1
_Static_assert((VIAL_ENCODERS_EEPROM_ADDR + VIAL_ENCODERS_SIZE) == 0x658, "combo extension base");
_Static_assert(VIAL_COMBO_ENTRIES == 8, "combo extension slot count");
_Static_assert(sizeof(vial_combo_entry_t) == 10, "combo extension slot size");
#endif
#ifdef AK820_COMPACT_COMBO
#define VIAL_COMBO_EEPROM_ADDR 0x658
#else
#define VIAL_COMBO_EEPROM_ADDR (VIAL_TAP_DANCE_EEPROM_ADDR + VIAL_TAP_DANCE_SIZE)
#endif

#ifdef VIAL_COMBO_ENABLE
#define VIAL_COMBO_SIZE (sizeof(vial_combo_entry_t) * VIAL_COMBO_ENTRIES)
#else
#define VIAL_COMBO_SIZE 0
#endif

// Key overrides
#ifdef AK820_COMPACT_KEY_OVERRIDE
#define VIAL_KEY_OVERRIDE_EEPROM_ADDR AK820_KEY_OVERRIDE_ADDR
#else
#define VIAL_KEY_OVERRIDE_EEPROM_ADDR (VIAL_COMBO_EEPROM_ADDR + VIAL_COMBO_SIZE)
#endif

#ifdef VIAL_KEY_OVERRIDE_ENABLE
#define VIAL_KEY_OVERRIDE_SIZE (sizeof(vial_key_override_entry_t) * VIAL_KEY_OVERRIDE_ENTRIES)
#else
#define VIAL_KEY_OVERRIDE_SIZE 0
#endif

#ifdef AK820_BOARD
_Static_assert(VIAL_KEY_OVERRIDE_EEPROM_ADDR + VIAL_KEY_OVERRIDE_SIZE <= AK820_MACRO_BUSY_ADDR, "AK820 dynamic features overlap macro metadata");
_Static_assert(AK820_MACRO_BUSY_ADDR + 3 <= DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR, "AK820 macro metadata overlaps macro data");
#endif

// Dynamic macro
#ifndef DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR
#    define DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR (VIAL_KEY_OVERRIDE_EEPROM_ADDR + VIAL_KEY_OVERRIDE_SIZE)
#endif

// Sanity check that dynamic keymaps fit in available EEPROM
// If there's not 100 bytes available for macros, then something is wrong.
// The keyboard should override DYNAMIC_KEYMAP_LAYER_COUNT to reduce it,
// or DYNAMIC_KEYMAP_EEPROM_MAX_ADDR to increase it, *only if* the microcontroller has
// more than the default.
_Static_assert(DYNAMIC_KEYMAP_EEPROM_MAX_ADDR >= DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + 100, "Dynamic keymaps are configured to use more EEPROM than is available.");

// Dynamic macros are stored after the keymaps and use what is available
// up to and including DYNAMIC_KEYMAP_EEPROM_MAX_ADDR.
#ifndef DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE
#    define DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE (DYNAMIC_KEYMAP_EEPROM_MAX_ADDR - DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + 1)
#endif

#ifndef DYNAMIC_KEYMAP_MACRO_DELAY
#    define DYNAMIC_KEYMAP_MACRO_DELAY TAP_CODE_DELAY
#endif

uint8_t dynamic_keymap_get_layer_count(void) {
    return DYNAMIC_KEYMAP_LAYER_COUNT;
}

void *dynamic_keymap_key_to_eeprom_address(uint8_t layer, uint8_t row, uint8_t column) {
    // TODO: optimize this with some left shifts
    return ((uint8_t *)DYNAMIC_KEYMAP_EEPROM_ADDR) + (layer * MATRIX_ROWS * MATRIX_COLS * 2) + (row * MATRIX_COLS * 2) + (column * 2);
}

uint16_t dynamic_keymap_get_keycode(uint8_t layer, uint8_t row, uint8_t column) {
    if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || row >= MATRIX_ROWS || column >= MATRIX_COLS) return KC_NO;
    uint8_t *address = dynamic_keymap_key_to_eeprom_address(layer, row, column);
    // Big endian, so we can read/write EEPROM directly from host if we want
    uint16_t keycode = eeprom_read_byte(address) << 8;
    keycode |= eeprom_read_byte(address + 1);
    return keycode;
}

void dynamic_keymap_set_keycode(uint8_t layer, uint8_t row, uint8_t column, uint16_t keycode) {
    if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || row >= MATRIX_ROWS || column >= MATRIX_COLS) return;
    uint8_t *address = dynamic_keymap_key_to_eeprom_address(layer, row, column);
    // Big endian, so we can read/write EEPROM directly from host if we want
    eeprom_update_byte(address, (uint8_t)(keycode >> 8));
    eeprom_update_byte(address + 1, (uint8_t)(keycode & 0xFF));
}

#ifdef ENCODER_MAP_ENABLE
void *dynamic_keymap_encoder_to_eeprom_address(uint8_t layer, uint8_t encoder_id) {
    return ((uint8_t *)DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR) + (layer * NUM_ENCODERS * 2 * 2) + (encoder_id * 2 * 2);
}

uint16_t dynamic_keymap_get_encoder(uint8_t layer, uint8_t encoder_id, bool clockwise) {
    if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || encoder_id >= NUM_ENCODERS) return KC_NO;
    uint8_t *address = dynamic_keymap_encoder_to_eeprom_address(layer, encoder_id);
    // Big endian, so we can read/write EEPROM directly from host if we want
    uint16_t keycode = ((uint16_t)eeprom_read_byte(address + (clockwise ? 0 : 2))) << 8;
    keycode |= eeprom_read_byte(address + (clockwise ? 0 : 2) + 1);
    return keycode;
}

void dynamic_keymap_set_encoder(uint8_t layer, uint8_t encoder_id, bool clockwise, uint16_t keycode) {
    if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || encoder_id >= NUM_ENCODERS) return;
    uint8_t *address = dynamic_keymap_encoder_to_eeprom_address(layer, encoder_id);
    // Big endian, so we can read/write EEPROM directly from host if we want
    eeprom_update_byte(address + (clockwise ? 0 : 2), (uint8_t)(keycode >> 8));
    eeprom_update_byte(address + (clockwise ? 0 : 2) + 1, (uint8_t)(keycode & 0xFF));
}
#endif // ENCODER_MAP_ENABLE

#ifdef QMK_SETTINGS
uint8_t dynamic_keymap_get_qmk_settings(uint16_t offset) {
    if (offset >= VIAL_QMK_SETTINGS_SIZE)
        return 0;

    uint8_t *address = (uint8_t *)(VIAL_QMK_SETTINGS_EEPROM_ADDR + offset);
    return eeprom_read_byte(address);
}

void dynamic_keymap_set_qmk_settings(uint16_t offset, uint8_t value) {
    if (offset >= VIAL_QMK_SETTINGS_SIZE)
        return;

    uint8_t *address = (uint8_t *)(VIAL_QMK_SETTINGS_EEPROM_ADDR + offset);
    eeprom_update_byte(address, value);
}
#endif

#ifdef VIAL_TAP_DANCE_ENABLE
#ifdef AK820_COMPACT_TAP_DANCE
int dynamic_keymap_get_tap_dance(uint8_t index, vial_tap_dance_entry_t *buffer) {
    vial_tap_dance_entry_t AK820_STATE_MEM *entry = (vial_tap_dance_entry_t AK820_STATE_MEM *)buffer;
    if (index >= AK820_EXTENSION_ENTRIES) return -1;
    ak820_eeprom_read_block_xdata(entry, (const void *)(VIAL_TAP_DANCE_EEPROM_ADDR + AK820_EXTENSION_OFFSET(index)), sizeof(*entry));
    if (!ak820_tap_dance_valid(entry)) memset(entry, 0, sizeof(*entry));
    return 0;
}
int dynamic_keymap_set_tap_dance(uint8_t index, const vial_tap_dance_entry_t *buffer) {
    const vial_tap_dance_entry_t AK820_STATE_MEM *entry = (const vial_tap_dance_entry_t AK820_STATE_MEM *)buffer;
    if (index >= AK820_EXTENSION_ENTRIES || !ak820_tap_dance_valid(entry) || !ak820_nvm_ok()) return -1;
    clear_keyboard();
    ak820_eeprom_update_block_xdata(entry, (void *)(VIAL_TAP_DANCE_EEPROM_ADDR + AK820_EXTENSION_OFFSET(index)), sizeof(*entry));
    ak820_nvm_flush();
    return ak820_nvm_ok() ? 0 : -1;
}
#else
int dynamic_keymap_get_tap_dance(uint8_t index, vial_tap_dance_entry_t *entry) {
    if (index >= VIAL_TAP_DANCE_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_TAP_DANCE_EEPROM_ADDR + index * sizeof(vial_tap_dance_entry_t));
    eeprom_read_block(entry, address, sizeof(vial_tap_dance_entry_t));

    return 0;
}

int dynamic_keymap_set_tap_dance(uint8_t index, const vial_tap_dance_entry_t *entry) {
    if (index >= VIAL_TAP_DANCE_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_TAP_DANCE_EEPROM_ADDR + index * sizeof(vial_tap_dance_entry_t));
    eeprom_write_block(entry, address, sizeof(vial_tap_dance_entry_t));

    return 0;
}
#endif
#endif

#ifdef VIAL_COMBO_ENABLE
int dynamic_keymap_get_combo(uint8_t index, vial_combo_entry_t *buffer) {
#ifdef AK820_COMPACT_COMBO
    /* Every board caller passes a model-large automatic XDATA entry. */
    vial_combo_entry_t AK820_STATE_MEM *entry = (vial_combo_entry_t AK820_STATE_MEM *)buffer;
#else
    vial_combo_entry_t *entry = buffer;
#endif
    if (index >= VIAL_COMBO_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_COMBO_EEPROM_ADDR + index * sizeof(vial_combo_entry_t));
#ifdef AK820_COMPACT_COMBO
    ak820_eeprom_read_block_xdata(entry, address, sizeof(vial_combo_entry_t));
#else
    eeprom_read_block(entry, address, sizeof(vial_combo_entry_t));
#endif
#ifdef AK820_COMPACT_COMBO
    bool marked = entry->input[2] == AK820_COMBO_MARKER && entry->input[3] == AK820_COMBO_VERSION;
    entry->input[2] = entry->input[3] = 0;
    if (!marked || !ak820_combo_valid(entry)) memset(entry, 0, sizeof(*entry));
#endif

    return 0;
}

int dynamic_keymap_set_combo(uint8_t index, const vial_combo_entry_t *buffer) {
#ifdef AK820_COMPACT_COMBO
    const vial_combo_entry_t AK820_STATE_MEM *entry = (const vial_combo_entry_t AK820_STATE_MEM *)buffer;
#else
    const vial_combo_entry_t *entry = buffer;
#endif
#ifdef AK820_COMPACT_COMBO
    if (!ak820_combo_valid(entry) || !ak820_nvm_ok()) return -1;
#endif
    if (index >= VIAL_COMBO_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_COMBO_EEPROM_ADDR + index * sizeof(vial_combo_entry_t));
#ifdef AK820_COMPACT_COMBO
    clear_keyboard();
    vial_combo_entry_t stored = *entry;
    stored.input[2] = AK820_COMBO_MARKER;
    stored.input[3] = AK820_COMBO_VERSION;
    ak820_eeprom_write_block_xdata(&stored, address, sizeof(stored));
#else
    eeprom_write_block(entry, address, sizeof(vial_combo_entry_t));
#endif
#ifdef AK820_COMPACT_COMBO
    ak820_nvm_flush();
    if (!ak820_nvm_ok()) return -1;
    /* flush() verifies the entire journal target page before success. */
#endif

    return 0;
}
#endif

#ifdef VIAL_KEY_OVERRIDE_ENABLE
#ifdef AK820_COMPACT_KEY_OVERRIDE
int dynamic_keymap_get_key_override(uint8_t index, vial_key_override_entry_t *buffer) {
    vial_key_override_entry_t AK820_STATE_MEM *entry = (vial_key_override_entry_t AK820_STATE_MEM *)buffer;
    if (index >= AK820_EXTENSION_ENTRIES) return -1;
    ak820_eeprom_read_block_xdata(entry, (const void *)(VIAL_KEY_OVERRIDE_EEPROM_ADDR + AK820_EXTENSION_OFFSET(index)), sizeof(*entry));
    if (!ak820_key_override_valid(entry)) memset(entry, 0, sizeof(*entry));
    return 0;
}
int dynamic_keymap_set_key_override(uint8_t index, const vial_key_override_entry_t *buffer) {
    const vial_key_override_entry_t AK820_STATE_MEM *entry = (const vial_key_override_entry_t AK820_STATE_MEM *)buffer;
    if (index >= AK820_EXTENSION_ENTRIES || !ak820_key_override_valid(entry) || !ak820_nvm_ok()) return -1;
    clear_keyboard();
    ak820_eeprom_update_block_xdata(entry, (void *)(VIAL_KEY_OVERRIDE_EEPROM_ADDR + AK820_EXTENSION_OFFSET(index)), sizeof(*entry));
    ak820_nvm_flush();
    return ak820_nvm_ok() ? 0 : -1;
}
#else
int dynamic_keymap_get_key_override(uint8_t index, vial_key_override_entry_t *entry) {
    if (index >= VIAL_KEY_OVERRIDE_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_KEY_OVERRIDE_EEPROM_ADDR + index * sizeof(vial_key_override_entry_t));
    eeprom_read_block(entry, address, sizeof(vial_key_override_entry_t));

    return 0;
}

int dynamic_keymap_set_key_override(uint8_t index, const vial_key_override_entry_t *entry) {
    if (index >= VIAL_KEY_OVERRIDE_ENTRIES)
        return -1;

    uint8_t *address = (uint8_t *)(VIAL_KEY_OVERRIDE_EEPROM_ADDR + index * sizeof(vial_key_override_entry_t));
    eeprom_write_block(entry, address, sizeof(vial_key_override_entry_t));

    return 0;
}
#endif
#endif

void dynamic_keymap_reset(void) {
#ifdef AK820_BOARD
    /* The on-wire dimensions fit one byte. Wider signed counters otherwise
     * introduce needless 16-bit arithmetic in every reset iteration on 8051. */
    _Static_assert(DYNAMIC_KEYMAP_LAYER_COUNT < 256 && MATRIX_ROWS < 256 && MATRIX_COLS < 256 && NUM_ENCODERS < 256, "AK820 keymap index width");
    typedef uint8_t reset_index_t;
#else
    typedef int reset_index_t;
#endif
#ifdef VIAL_ENABLE
    /* temporarily unlock the keyboard so we can set hardcoded QK_BOOT keycode */
    bool vial_unlocked_prev = vial_unlocked;
    vial_unlocked = 1;
#endif

    // Reset the keymaps in EEPROM to what is in flash.
    for (reset_index_t layer = 0; layer < DYNAMIC_KEYMAP_LAYER_COUNT; layer++) {
        for (reset_index_t row = 0; row < MATRIX_ROWS; row++) {
            for (reset_index_t column = 0; column < MATRIX_COLS; column++) {
                dynamic_keymap_set_keycode(layer, row, column, keycode_at_keymap_location_raw(layer, row, column));
            }
        }
#ifdef ENCODER_MAP_ENABLE
        for (reset_index_t encoder = 0; encoder < NUM_ENCODERS; encoder++) {
            dynamic_keymap_set_encoder(layer, encoder, true, keycode_at_encodermap_location_raw(layer, encoder, true));
            dynamic_keymap_set_encoder(layer, encoder, false, keycode_at_encodermap_location_raw(layer, encoder, false));
        }
#endif // ENCODER_MAP_ENABLE
    }

#ifdef AK820_QMK_SETTINGS
    ak820_settings_reset();
#endif
#ifdef QMK_SETTINGS
    qmk_settings_reset();
#endif

#ifdef VIAL_TAP_DANCE_ENABLE
    vial_tap_dance_entry_t td = { KC_NO, KC_NO, KC_NO, KC_NO, TAPPING_TERM };
    for (reset_index_t i = 0; i < VIAL_TAP_DANCE_ENTRIES; ++i) {
        dynamic_keymap_set_tap_dance(i, &td);
    }
#endif

#ifdef VIAL_COMBO_ENABLE
    vial_combo_entry_t combo = { { 0 }, 0 };
    for (reset_index_t i = 0; i < VIAL_COMBO_ENTRIES; ++i)
        dynamic_keymap_set_combo(i, &combo);
#endif

#ifdef VIAL_KEY_OVERRIDE_ENABLE
    vial_key_override_entry_t ko = { 0 };
#ifndef AK820_COMPACT_KEY_OVERRIDE
    ko.layers = ~0;
    ko.options = vial_ko_option_activation_negative_mod_up | vial_ko_option_activation_required_mod_down | vial_ko_option_activation_trigger_down;
#endif
    for (reset_index_t i = 0; i < VIAL_KEY_OVERRIDE_ENTRIES; ++i)
        dynamic_keymap_set_key_override(i, &ko);
#endif

#ifdef VIAL_ENABLE
    /* re-lock the keyboard */
    vial_unlocked = vial_unlocked_prev;
#endif
}

#ifdef AK820_BOARD
/* One backend read per HID chunk. The board backend already bounds logical
 * EEPROM addresses and reads its dirty cache without committing a page. */
static void ak820_dynamic_read_buffer(uint16_t base, uint16_t limit, uint16_t offset, uint16_t size, uint8_t *data) {
    uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)data;
    uint8_t available = 0;
    if (size > 28) return;
    if (offset < limit) {
        uint16_t remaining = limit - offset;
        available = remaining < size ? remaining : size;
    }
    if (available) ak820_eeprom_read_block_xdata(target, (const void *)(uintptr_t)(base + offset), available);
    for (uint8_t i = available; i < size; ++i) target[i] = 0;
}
#endif

void dynamic_keymap_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
#ifdef AK820_BOARD
    ak820_dynamic_read_buffer(DYNAMIC_KEYMAP_EEPROM_ADDR,
        DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2, offset, size, data);
#else
    uint16_t dynamic_keymap_eeprom_size = DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2;
    uint16_t available = offset < dynamic_keymap_eeprom_size ? dynamic_keymap_eeprom_size - offset : 0;
    uint8_t DYNAMIC_BUFFER_MEM *source = (uint8_t DYNAMIC_BUFFER_MEM *)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset);
    uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)data;
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    if (size > 28) return;
#endif
    if (available > size) available = size;
    dynamic_buffer_size_t count = size;
    dynamic_buffer_size_t valid = available;
    for (dynamic_buffer_size_t i = 0; i < count; i++) {
        if (i < valid) {
            *target = eeprom_read_byte(source);
        } else {
            *target = 0x00;
        }
        source++;
        target++;
    }
#endif
}

void dynamic_keymap_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    uint16_t dynamic_keymap_eeprom_size = DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2;
    uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset);
    uint8_t DYNAMIC_BUFFER_MEM *buffer = (uint8_t DYNAMIC_BUFFER_MEM *)data;
#ifndef AK820_BOARD
    uint8_t DYNAMIC_BUFFER_MEM *source = buffer;
#endif
    if (!size) return;
#ifdef AK820_BOARD
    if (size > 28) return;
#endif
    dynamic_buffer_size_t count = size;

#ifdef VIAL_ENABLE
    /* ensure the writes are bounded */
    if (offset >= dynamic_keymap_eeprom_size || dynamic_keymap_eeprom_size - offset < size)
        return;

#ifndef VIAL_INSECURE
    /* Check whether it is trying to send a QK_BOOT keycode; only allow setting these if unlocked */
    if (!vial_unlocked) {
        /* how much of the input array we'll have to check in the loop */
        dynamic_buffer_size_t chk_offset = 0;
        dynamic_buffer_size_t chk_sz = count;

        /* initial byte misaligned -- this means the first keycode will be a combination of existing and new data */
        if (offset % 2 != 0) {
            uint16_t kc = (eeprom_read_byte(target - 1) << 8) | buffer[0];
            if (kc == QK_BOOT)
                buffer[0] = 0xFF;

            /* no longer have to check the first byte */
            chk_offset += 1;
        }

        /* final byte misaligned -- this means the last keycode will be a combination of new and existing data */
        if ((offset + size) % 2 != 0) {
            uint16_t kc = (buffer[count - 1] << 8) | eeprom_read_byte(target + count);
            if (kc == QK_BOOT)
                buffer[count - 1] = 0xFF;

            /* no longer have to check the last byte */
            chk_sz -= 1;
        }

        /* check the entire array, replace any instances of QK_BOOT with invalid keycode 0xFFFF */
        for (dynamic_buffer_size_t i = chk_offset; i < chk_sz; i += 2) {
            uint16_t kc = (buffer[i] << 8) | buffer[i + 1];
            if (kc == QK_BOOT) {
                buffer[i] = 0xFF;
                buffer[i + 1] = 0xFF;
            }
        }
    }
#endif
#endif

#ifdef AK820_BOARD
    /* The board backend compares each byte, batches pages and verifies the
     * durable write. Repeating its comparison through byte wrappers adds no
     * guarantee and is costly on the 8051 generic-pointer ABI. */
    ak820_eeprom_write_block_xdata(buffer, (void *)(uintptr_t)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset), size);
#else
    for (dynamic_buffer_size_t i = 0; i < count; i++) {
        if (offset + i < dynamic_keymap_eeprom_size) {
            eeprom_update_byte(target, *source);
        }
        source++;
        target++;
    }
#endif
}

uint16_t keycode_at_keymap_location(uint8_t layer_num, uint8_t row, uint8_t column) {
    if (layer_num < DYNAMIC_KEYMAP_LAYER_COUNT && row < MATRIX_ROWS && column < MATRIX_COLS) {
        return dynamic_keymap_get_keycode(layer_num, row, column);
    }
    return KC_NO;
}

#ifdef ENCODER_MAP_ENABLE
uint16_t keycode_at_encodermap_location(uint8_t layer_num, uint8_t encoder_idx, bool clockwise) {
    if (layer_num < DYNAMIC_KEYMAP_LAYER_COUNT && encoder_idx < NUM_ENCODERS) {
        return dynamic_keymap_get_encoder(layer_num, encoder_idx, clockwise);
    }
    return KC_NO;
}
#endif // ENCODER_MAP_ENABLE

uint8_t dynamic_keymap_macro_get_count(void) {
    return DYNAMIC_KEYMAP_MACRO_COUNT;
}

uint16_t dynamic_keymap_macro_get_buffer_size(void) {
    return DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE;
}

void dynamic_keymap_macro_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
#ifdef AK820_BOARD
    ak820_dynamic_read_buffer(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR,
                             ak820_macro_length(), offset, size, data);
#else
    uint16_t macro_size = DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE;
    uint16_t available = offset < macro_size ? macro_size - offset : 0;
    uint8_t DYNAMIC_BUFFER_MEM *source = (uint8_t DYNAMIC_BUFFER_MEM *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset);
    uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)data;
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    if (size > 28) return;
#endif
    if (available > size) available = size;
    dynamic_buffer_size_t count = size;
    dynamic_buffer_size_t valid = available;
    for (dynamic_buffer_size_t i = 0; i < count; i++) {
        if (i < valid) {
            *target = eeprom_read_byte(source);
        } else {
            *target = 0x00;
        }
        source++;
        target++;
    }
#endif
}

#ifdef AK820_BOARD
bool dynamic_keymap_macro_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    return ak820_macro_write(offset, size, data);
}
#else
void dynamic_keymap_macro_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    uint8_t *target = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset);
    uint8_t *source = data;
    for (uint16_t i = 0; i < size; i++) {
        if (offset + i < DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE) {
            eeprom_update_byte(target, *source);
        }
        source++;
        target++;
    }
}
#endif

void dynamic_keymap_macro_reset(void) {
#ifdef AK820_BOARD
    ak820_macro_reset();
#else
    uint8_t *p = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR);
    uint8_t *end = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE);
    while (p != end) {
        eeprom_update_byte(p, 0);
        ++p;
    }
#endif
}

static uint16_t decode_keycode(uint16_t kc) {
    /* map 0xFF01 => 0x0100; 0xFF02 => 0x0200, etc */
    if (kc > 0xFF00)
        return (kc & 0xFF) << 8;
    return kc;
}

void dynamic_keymap_macro_send(uint8_t id) {
#ifdef AK820_BOARD
    /* Extended keycodes can dispatch a macro again through action_exec.
     * SDCC's static interpreter locals cannot support nested playback. */
    static bool sending;
    if (sending) return;
#endif
    if (id >= DYNAMIC_KEYMAP_MACRO_COUNT) {
        return;
    }

#ifdef AK820_BOARD
    // The Vial GUI never writes the upstream last-byte busy marker.
    // AK820 commits only complete validated streams using a separate byte.
    if (!ak820_macro_ready()) return;
    uint16_t p;
#else
    // Check the last byte of the buffer.
    // If it's not zero, then we are in the middle
    // of buffer writing, possibly an aborted buffer
    // write. So do nothing.
    uint8_t *p = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE - 1);
    if (eeprom_read_byte(p) != 0) {
        return;
    }
#endif

    // Skip N null characters
    // p will then point to the Nth macro
#ifdef AK820_BOARD
    /* EEPROM tokens are 16-bit offsets, never generic C memory addresses. */
    p = DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR;
    uint16_t end = DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + ak820_macro_length();
#else
    p = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR);
    uint8_t *end = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE);
#endif
    while (id > 0) {
        // If we are past the end of the buffer, then the buffer
        // contents are garbage, i.e. there were not DYNAMIC_KEYMAP_MACRO_COUNT
        // nulls in the buffer.
        if (p == end) {
            return;
        }
        if (eeprom_read_byte((const uint8_t *)(uintptr_t)p) == 0) {
            --id;
        }
        ++p;
    }

#ifdef AK820_BOARD
    /* All preflight returns precede this point; every interpreter exit
     * below reaches the release at the end of the function. */
    sending = true;
#    ifdef AK820_COMPACT_TAPPING
    ak820_macro_cancelled = ak820_macro_primitive = false;
#    endif
#endif
    // Send the macro string one or three chars at a time
    // by making temporary 1 or 3 char strings
    char data[4] = {0, 0, 0, 0};
    // AK820 validates the complete grammar before publication; retain the
    // explicit boundary as a second bound on the main interpreter loop.
    while (p < end
#ifdef AK820_COMPACT_TAPPING
           && !ak820_macro_cancelled
#endif
    ) {
        data[0] = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
        data[1] = 0;
        // Stop at the null terminator of this macro string
        if (data[0] == 0) {
            break;
        }
        if (data[0] == SS_QMK_PREFIX) {
            // If the char is magic, process it as indicated by the next character
            // (tap, down, up, delay)
            data[1] = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
            if (data[1] == 0)
                break;
            if (data[1] == SS_TAP_CODE || data[1] == SS_DOWN_CODE || data[1] == SS_UP_CODE) {
                // For tap, down, up, just stuff it into the array and send_string it
                data[2] = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
#ifdef AK820_BOARD
                /* The Vial stream is already decoded. Avoid parsing a second
                 * synthetic send-string byte stream for the same action. */
                if (data[2] != 0) {
#    ifdef AK820_COMPACT_TAPPING
                    ak820_macro_primitive = data[1] != SS_TAP_CODE;
#    endif
                    if (data[1] == SS_TAP_CODE) tap_code((uint8_t)data[2]);
                    else if (data[1] == SS_DOWN_CODE) register_code((uint8_t)data[2]);
                    else unregister_code((uint8_t)data[2]);
#    ifdef AK820_COMPACT_TAPPING
                    ak820_macro_primitive = false;
#    endif
                }
#else
                /* An earlier extended action used the fourth byte as data. */
                data[3] = 0;
                if (data[2] != 0) send_string(data);
#endif
            } else if (data[1] == VIAL_MACRO_EXT_TAP || data[1] == VIAL_MACRO_EXT_DOWN || data[1] == VIAL_MACRO_EXT_UP) {
                data[2] = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
                if (data[2] != 0) {
                    data[3] = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
                    if (data[3] != 0) {
                        uint16_t kc;
#ifdef AK820_BOARD
                        kc = (uint8_t)data[2] | ((uint16_t)(uint8_t)data[3] << 8);
#else
                        memcpy(&kc, &data[2], sizeof(kc));
#endif
                        kc = decode_keycode(kc);
#ifdef AK820_COMPACT_TAPPING
                        ak820_macro_primitive = data[1] != VIAL_MACRO_EXT_TAP;
#endif
                        switch (data[1]) {
                        case VIAL_MACRO_EXT_TAP:
                            vial_keycode_tap(kc);
                            break;
                        case VIAL_MACRO_EXT_DOWN:
                            vial_keycode_down(kc);
                            break;
                        case VIAL_MACRO_EXT_UP:
                            vial_keycode_up(kc);
                            break;
                        }
#ifdef AK820_COMPACT_TAPPING
                        ak820_macro_primitive = false;
#endif
                    }
                }
            } else if (data[1] == SS_DELAY_CODE) {
                // For delay, decode the delay and wait_ms for that amount
                uint8_t d0 = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
                uint8_t d1 = eeprom_read_byte((const uint8_t *)(uintptr_t)p++);
                if (d0 == 0 || d1 == 0)
                    break;
                // we cannot use 0 for these, need to subtract 1 and use 255 instead of 256 for delay calculation
                uint16_t ms = (uint16_t)(d0 - 1) + (uint16_t)(d1 - 1) * 255u;
                while (ms--) wait_ms(1);
            }
        } else {
#ifdef AK820_BOARD
            /* Stored streams from older firmware also need the ASCII bound;
             * publication validation alone cannot protect their playback. */
            if ((uint8_t)data[0] >= 128) break;
#endif
            // If the char wasn't magic, just send it
#ifdef AK820_BOARD
            send_char(data[0]);
            for (uint8_t delay = DYNAMIC_KEYMAP_MACRO_DELAY; delay; --delay) wait_ms(1);
#else
            send_string_with_delay(data, DYNAMIC_KEYMAP_MACRO_DELAY);
#endif
        }
    }
#ifdef AK820_BOARD
#    ifdef AK820_COMPACT_TAPPING
    ak820_macro_primitive = false;
#    endif
    sending = false;
#endif
}
