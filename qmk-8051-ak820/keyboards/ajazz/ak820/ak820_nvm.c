#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

// SPDX-License-Identifier: GPL-2.0-or-later
// Persistent QMK EEPROM with one 64-byte redo journal. No USB or ISR calls.
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include "ak820_nvm.h"
#ifdef AK820_BOARD
#include "ak820_macro.h"
#endif

#if defined(__SDCC_mcs51)
#    define AK820_FLAG __bit
#else
#    define AK820_FLAG bool
#endif

static uint8_t page_data[AK820_FLASH_PAGE];
/* All cache callers validate offsets before selecting one of 160 pages.
 * Keep journal decoding 16-bit so malformed stored page numbers still fail. */
_Static_assert(AK820_NVM_SIZE / AK820_FLASH_PAGE < 256u, "cache page index must fit in a byte");
static uint8_t cached_page;
static AK820_FLAG page_valid, page_dirty, storage_failed;
static uint8_t batch_depth;
static uint8_t first_failure_stage;

static void nvm_fail(uint8_t stage) {
    if (!storage_failed) first_failure_stage = stage;
    storage_failed = true;
}

void ak820_nvm_diagnostic(uint8_t AK820_XDATA *out) {
    out[0] = storage_failed;
    out[1] = page_valid;
    out[2] = page_dirty;
    out[3] = batch_depth;
    out[4] = (uint8_t)cached_page;
    out[5] = (uint8_t)(cached_page >> 8);
    out[6] = first_failure_stage;
}

static uint16_t crc_byte(uint16_t crc, uint8_t value) {
    uint8_t bit;
    crc ^= (uint16_t)value << 8;
    for (bit = 0; bit != 8; ++bit) {
        crc = (crc & 0x8000u) ? (uint16_t)((crc << 1) ^ 0x1021u) : (uint16_t)(crc << 1);
    }
    return crc;
}

static uint16_t page_crc(void) {
    uint16_t crc = 0xFFFFu;
    uint8_t i;
    for (i = 0; i != AK820_FLASH_PAGE; ++i) crc = crc_byte(crc, page_data[i]);
    return crc;
}

static bool write_page(uint16_t address) {
    uint8_t i;
    if (!ak820_flash_erase(address)) return false;
    if (!ak820_flash_program_page(address, page_data)) return false;
    for (i = 0; i != AK820_FLASH_PAGE; ++i) {
        if (ak820_flash_read(address + i) != page_data[i]) return false;
    }
    return true;
}

static bool journal_header_valid(uint8_t AK820_XDATA *header) {
    uint8_t i;
    if (header[0] != 0xA5u) return false;
    for (i = 1; i != 5; ++i) {
        if ((uint8_t)(header[i] ^ header[i + 4]) != 0xFFu) return false;
    }
    return true;
}

static void recover_journal(void) {
    uint8_t header[9];
    uint8_t i;
    uint16_t page, crc;
    for (i = 0; i != sizeof(header); ++i) header[i] = ak820_flash_read(AK820_JOURNAL_HEADER + i);
    // Incomplete prepare or incomplete cleanup: target was not started, or
    // already verified. Only an exact committed record authorizes replay.
    if (!journal_header_valid(header)) return;
    page = (uint16_t)header[1] | ((uint16_t)header[2] << 8);
    crc = (uint16_t)header[3] | ((uint16_t)header[4] << 8);
    if (page >= AK820_NVM_SIZE / AK820_FLASH_PAGE) {
        nvm_fail(AK820_NVM_FAULT_RECOVERY_PAGE);
        return;
    }
    for (i = 0; i != AK820_FLASH_PAGE; ++i) page_data[i] = ak820_flash_read(AK820_JOURNAL_DATA + i);
    if (page_crc() != crc) nvm_fail(AK820_NVM_FAULT_RECOVERY_CRC);
    else if (!write_page(AK820_NVM_BASE + page * AK820_FLASH_PAGE)) nvm_fail(AK820_NVM_FAULT_RECOVERY_WRITE);
    else if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) nvm_fail(AK820_NVM_FAULT_RECOVERY_CLEANUP);
}

void eeprom_driver_init(void) {
    storage_failed = false;
    first_failure_stage = AK820_NVM_FAULT_NONE;
    page_valid = page_dirty = false;
    batch_depth = 0;
    recover_journal();
#ifdef AK820_BOARD
    ak820_macro_init();
#endif
}

bool ak820_nvm_ok(void) { return !storage_failed; }

void ak820_nvm_schema_fault(void) { nvm_fail(AK820_NVM_FAULT_SCHEMA); }

void ak820_nvm_flush(void) {
    uint8_t header[9];
    uint16_t crc;
    uint8_t i;
    uint8_t stage;
    if (!page_dirty || storage_failed) return;
    crc = page_crc();
    header[0] = 0xA5u;
    header[1] = (uint8_t)cached_page;
    header[2] = (uint8_t)(cached_page >> 8);
    header[3] = (uint8_t)crc;
    header[4] = (uint8_t)(crc >> 8);
    for (i = 1; i != 5; ++i) header[i + 4] = (uint8_t)~header[i];
    // Erase and verify header BEFORE touching journal data. A previous valid
    // record can therefore never refer to a half-written next data page.
    stage = AK820_NVM_FAULT_HEADER_ERASE;
    if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
    stage = AK820_NVM_FAULT_HEADER_ZERO;
    for (i = 0; i != AK820_FLASH_PAGE; ++i) {
        if (ak820_flash_read(AK820_JOURNAL_HEADER + i)) goto failed;
    }
    stage = AK820_NVM_FAULT_JOURNAL_WRITE;
    if (!write_page(AK820_JOURNAL_DATA)) goto failed;
    stage = AK820_NVM_FAULT_METADATA_PROGRAM;
    for (i = 1; i != sizeof(header); ++i) {
        if (header[i] && !ak820_flash_program(AK820_JOURNAL_HEADER + i, header[i])) goto failed;
    }
    stage = AK820_NVM_FAULT_METADATA_READBACK;
    for (i = 1; i != sizeof(header); ++i) {
        if (ak820_flash_read(AK820_JOURNAL_HEADER + i) != header[i]) goto failed;
    }
    // Commit last. Every subsequent interruption can replay the full new page.
    stage = AK820_NVM_FAULT_COMMIT_PROGRAM;
    if (!ak820_flash_program(AK820_JOURNAL_HEADER, header[0])) goto failed;
    stage = AK820_NVM_FAULT_COMMIT_READBACK;
    if (ak820_flash_read(AK820_JOURNAL_HEADER) != header[0]) goto failed;
    stage = AK820_NVM_FAULT_TARGET_WRITE;
    if (!write_page(AK820_NVM_BASE + cached_page * AK820_FLASH_PAGE)) goto failed;
    stage = AK820_NVM_FAULT_CLEANUP;
    if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
    page_dirty = false;
    return;
failed:
    nvm_fail(stage);
}

void ak820_nvm_begin(void) {
    if (batch_depth == 255u) nvm_fail(AK820_NVM_FAULT_BATCH_OVERFLOW);
    else ++batch_depth;
}

void ak820_nvm_end(void) {
    if (batch_depth) --batch_depth;
    if (!batch_depth) ak820_nvm_flush();
}

static bool load_page(uint8_t page) {
    uint8_t i;
    if (page_valid && cached_page == page) return !storage_failed;
    ak820_nvm_flush();
    if (storage_failed) return false;
    for (i = 0; i != AK820_FLASH_PAGE; ++i) {
        page_data[i] = ak820_flash_read(AK820_NVM_BASE + page * AK820_FLASH_PAGE + i);
    }
    cached_page = page;
    page_valid = true;
    return true;
}

static uint8_t read_offset(uint16_t offset) {
    if (offset >= AK820_NVM_SIZE) return 0;
    if (page_valid && (offset / AK820_FLASH_PAGE) == cached_page)
        return page_data[offset % AK820_FLASH_PAGE];
    return ak820_flash_read(AK820_NVM_BASE + offset);
}

#if defined(AK820_BOARD) || defined(AK820_NVM_SCALAR_TEST)
uint8_t eeprom_read_byte(const uint8_t *addr) {
    return read_offset((uint16_t)(uintptr_t)addr);
}

#endif

void eeprom_read_block(void *buf, const void *addr, size_t len) {
    uint16_t offset = (uint16_t)(uintptr_t)addr;
    uint8_t *out = (uint8_t *)buf;
    while (len--) {
        if (offset >= AK820_NVM_SIZE) { *out++ = 0; continue; }
        *out++ = read_offset(offset);
        ++offset;
    }
}

void eeprom_write_block(const void *buf, void *addr, size_t len) {
    uint16_t offset = (uint16_t)(uintptr_t)addr;
    const uint8_t *in = (const uint8_t *)buf;
    // Reject the complete request before changing any page; no wrap/clamping.
    if (offset > AK820_NVM_SIZE || len > AK820_NVM_SIZE - offset) {
        nvm_fail(AK820_NVM_FAULT_WRITE_RANGE);
        return;
    }
    while (len--) {
        uint8_t value = *in++;
        if (!load_page(offset / AK820_FLASH_PAGE)) return;
        if (page_data[offset % AK820_FLASH_PAGE] != value) {
            page_data[offset % AK820_FLASH_PAGE] = value;
            page_dirty = true;
        }
        ++offset;
    }
    if (!batch_depth) ak820_nvm_flush();
}

void ak820_eeprom_read_block_xdata(void AK820_XDATA *buf, const void *addr, size_t len) {
    uint16_t offset = (uint16_t)(uintptr_t)addr;
    uint8_t AK820_XDATA *out = (uint8_t AK820_XDATA *)buf;
    while (len--) {
        if (offset >= AK820_NVM_SIZE) { *out++ = 0; continue; }
        *out++ = read_offset(offset);
        ++offset;
    }
}

void ak820_eeprom_write_block_xdata(const void AK820_XDATA *buf, void *addr, size_t len) {
    uint16_t offset = (uint16_t)(uintptr_t)addr;
    const uint8_t AK820_XDATA *in = (const uint8_t AK820_XDATA *)buf;
    // Reject the complete request before changing any page; no wrap/clamping.
    if (offset > AK820_NVM_SIZE || len > AK820_NVM_SIZE - offset) {
        nvm_fail(AK820_NVM_FAULT_WRITE_RANGE);
        return;
    }
    while (len--) {
        uint8_t value = *in++;
        if (!load_page(offset / AK820_FLASH_PAGE)) return;
        if (page_data[offset % AK820_FLASH_PAGE] != value) {
            page_data[offset % AK820_FLASH_PAGE] = value;
            page_dirty = true;
        }
        ++offset;
    }
    if (!batch_depth) ak820_nvm_flush();
}

void ak820_eeprom_update_block_xdata(const void AK820_XDATA *buf, void *addr, size_t len) {
    const uint8_t AK820_XDATA *source = (const uint8_t AK820_XDATA *)buf;
    uint16_t offset = (uint16_t)(uintptr_t)addr;
    size_t i;
    for (i = 0; i < len; ++i) {
        if (read_offset(offset + i) != source[i]) {
            ak820_eeprom_write_block_xdata(buf, addr, len);
            return;
        }
    }
}

void eeprom_driver_erase(void) {
    uint8_t page;
    uint8_t i;
    ak820_nvm_flush();
    for (page = 0; page != AK820_NVM_SIZE / AK820_FLASH_PAGE && !storage_failed; ++page) {
        if (!load_page(page)) return;
        for (i = 0; i != AK820_FLASH_PAGE; ++i) {
            if (page_data[i]) { page_data[i] = 0; page_dirty = true; }
        }
        ak820_nvm_flush();
    }
}

