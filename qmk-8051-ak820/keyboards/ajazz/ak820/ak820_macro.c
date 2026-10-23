/* SPDX-License-Identifier: GPL-2.0-or-later
 * Vial6 has no upload-begin/end command. Its GUI writes contiguous chunks
 * starting at offset0, ending after the16th macro terminator. Keep a separate
 * durable busy byte until that complete stream is durable. Publish its logical
 * length and clear busy together in one journaled metadata page; old tail bytes
 * are hidden from reads and execution without rewriting 128 flash pages.
 * Interrupted uploads disable macros; they do not roll back the previous set.
 */
#if defined(__SDCC_mcs51)
/* The preserved loader leaves this application code window free. The builder
 * binds it to 0x28a0 and proves the complete area ends before 0x3000. */
#pragma codeseg AK820LOW
#endif

#include "config.h"
#include "ak820_macro.h"
#include "ak820_nvm.h"
#include "eeprom.h"

#if DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR != 0x0800 || DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE != 8192 || DYNAMIC_KEYMAP_MACRO_COUNT != 16
#    error "AK820 macro journal requires the documented EEPROM layout"
#endif

typedef struct {
    uint8_t terminated;
    uint8_t arguments; /*0=text,1/2=nonzero operands,3=opcode after prefix1 */
} macro_parse_t;

static macro_parse_t parsed;
static uint16_t covered;
static uint16_t used_length;
static bool uploading;

static uint8_t macro_byte(uint16_t offset) {
    return eeprom_read_byte((const uint8_t *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset));
}

static void busy_write(uint8_t value) {
    eeprom_update_byte((uint8_t *)(uintptr_t)AK820_MACRO_BUSY_ADDR, value);
    ak820_nvm_flush();
}

static void commit_length(uint16_t length) {
    uint8_t metadata[3];
    metadata[0] = 0;
    metadata[1] = (uint8_t)length;
    metadata[2] = (uint8_t)(length >> 8);
    ak820_eeprom_write_block_xdata(metadata, (void *)(uintptr_t)AK820_MACRO_BUSY_ADDR, sizeof(metadata));
    ak820_nvm_flush();
    if (ak820_nvm_ok()) used_length = length;
}

/* Operand bytes cannot be zero: Vial encodes 16-bit keycodes and delays to
 * avoid embedded terminators. Unknown opcodes are never executable. */
static bool parse_byte(macro_parse_t AK820_XDATA *state, uint8_t value) {
    if (state->terminated == DYNAMIC_KEYMAP_MACRO_COUNT) return value == 0;
    if (state->arguments == 3) {
        if (value < 1 || value > 7) return false;
        state->arguments = value <= 3 ? 1 : 2;
    } else if (state->arguments) {
        if (!value) return false;
        --state->arguments;
    } else if (!value) {
        ++state->terminated;
    } else if (value == 1) {
        state->arguments = 3;
    } else if (value >= 128) {
        /* send_char() has ASCII tables. Binary keycode/delay operands were
         * handled above and may still use any nonzero byte, including 255. */
        return false;
    }
    return true;
}

static bool matches(uint16_t offset, uint16_t size, const uint8_t AK820_XDATA *data) {
    while (size--) {
        uint8_t value = !uploading && offset >= used_length ? 0 : macro_byte(offset);
        if (value != *data++) return false;
        ++offset;
    }
    return true;
}

void ak820_macro_init(void) {
    covered = 0;
    uploading = false;
    parsed.terminated = parsed.arguments = 0;
    used_length = eeprom_read_byte((const uint8_t *)(uintptr_t)AK820_MACRO_LENGTH_ADDR);
    used_length |= (uint16_t)eeprom_read_byte((const uint8_t *)(uintptr_t)(AK820_MACRO_LENGTH_ADDR + 1)) << 8;
}

bool ak820_macro_ready(void) {
    return ak820_nvm_ok() && used_length >= DYNAMIC_KEYMAP_MACRO_COUNT &&
        used_length <= DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE &&
        eeprom_read_byte((const uint8_t *)(uintptr_t)AK820_MACRO_BUSY_ADDR) == 0;
}

uint16_t ak820_macro_length(void) { return ak820_macro_ready() ? used_length : 0; }

bool ak820_macro_write(uint16_t offset, uint16_t size, const uint8_t *packet) {
    /* The only firmware caller passes the fixed Raw HID XDATA packet. Keep
     * the generic public ABI while avoiding generic-memory reads per byte. */
    const uint8_t AK820_XDATA *data = (const uint8_t AK820_XDATA *)packet;
    macro_parse_t next;
    uint16_t i, end;
    bool complete;

    /* Subtraction after the offset check prevents16-bit wraparound. */
    if (!ak820_nvm_ok() || !size || offset >= DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE ||
        size > DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE - offset) return false;
    end = offset + size;

    /* Repeated acknowledged chunks never restart a transfer or wear flash. */
    if (end <= covered && (uploading || offset || end == covered) && matches(offset, size, data)) return true;

    if (!uploading) {
        if (offset) {
            /* Some clients pad the already complete stream with zero chunks.
             * Its entire tail is logically zero; only contiguous padding
             * is accepted. Nonzero trailing data cannot be acknowledged. */
            if (!covered || offset != covered || !ak820_macro_ready()) return false;
            for (i = 0; i < size; ++i) if (data[i]) return false;
            covered = end;
            return true;
        }
        next.terminated = next.arguments = 0;
    } else {
        if (offset > covered) return false; /* A hole is never old EEPROM data. */
        if (offset == covered) {
            next.terminated = parsed.terminated;
            next.arguments = parsed.arguments;
        } else {
            /* A changed retransmission may rewind to an already received
             * prefix, but must validate that prefix again. This also permits
             * restarting an aborted GUI edit whose initial chunks match. */
            next.terminated = next.arguments = 0;
            for (i = 0; i < offset; ++i) if (!parse_byte(&next, macro_byte(i))) return false;
        }
    }
    for (i = 0; i < size; ++i) if (!parse_byte(&next, data[i])) return false;
    complete = next.terminated == DYNAMIC_KEYMAP_MACRO_COUNT;
    if (!complete && end == DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE) return false;

    ak820_nvm_begin();
    if (!uploading) {
        /* No macro data page may change before this durable barrier. */
        busy_write(1);
        if (!ak820_nvm_ok()) { ak820_nvm_end(); return false; }
    }
    ak820_eeprom_write_block_xdata(data, (void *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset), size);
    ak820_nvm_flush();
    if (complete && ak820_nvm_ok()) commit_length(end);
    ak820_nvm_end();
    if (!ak820_nvm_ok()) return false;
    covered = end;
    parsed.terminated = next.terminated;
    parsed.arguments = next.arguments;
    uploading = !complete;
    return true;
}

bool ak820_macro_reset(void) {
    uint16_t i;
    ak820_nvm_begin();
    busy_write(1);
    if (ak820_nvm_ok()) {
        for (i = 0; i < DYNAMIC_KEYMAP_MACRO_COUNT; ++i)
            eeprom_update_byte((uint8_t *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + i), 0);
        ak820_nvm_flush();
        if (ak820_nvm_ok()) commit_length(DYNAMIC_KEYMAP_MACRO_COUNT);
    }
    ak820_nvm_end();
    ak820_macro_init();
    return ak820_nvm_ok();
}
