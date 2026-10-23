/* SPDX-License-Identifier: GPL-2.0-or-later
 * Production NVM with a deterministic memory-only Flash backend. This checks
 * diagnostics and failure latching, not the electrical IAP implementation.
 */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "ak820_nvm.h"

void eeprom_driver_init(void);
void eeprom_read_block(void *, const void *, size_t);
void eeprom_write_block(const void *, void *, size_t);

static uint8_t code[65536];
static unsigned erases, programs, reads;
static uint8_t inject;
static unsigned cleanup;

uint8_t ak820_flash_read(uint16_t address) {
    ++reads;
    if (inject == AK820_NVM_FAULT_HEADER_ZERO && address == AK820_JOURNAL_HEADER && erases)
        return 1;
    if (inject == AK820_NVM_FAULT_METADATA_READBACK && address == AK820_JOURNAL_HEADER + 1 && programs > 1)
        return code[address] ^ 1;
    if (inject == AK820_NVM_FAULT_COMMIT_READBACK && address == AK820_JOURNAL_HEADER && code[address] == 0xa5)
        return 0;
    return code[address];
}

bool ak820_flash_erase(uint16_t address) {
    assert(address >= AK820_NVM_BASE && address < AK820_NVM_WRITE_END && !(address & 63));
    ++erases;
    if (address == AK820_JOURNAL_HEADER) {
        ++cleanup;
        if ((inject == AK820_NVM_FAULT_HEADER_ERASE && cleanup == 1) ||
            (inject == AK820_NVM_FAULT_CLEANUP && cleanup == 2) ||
            (inject == AK820_NVM_FAULT_RECOVERY_CLEANUP && cleanup == 1)) return false;
    }
    if (inject == AK820_NVM_FAULT_JOURNAL_WRITE && address == AK820_JOURNAL_DATA) return false;
    if ((inject == AK820_NVM_FAULT_TARGET_WRITE || inject == AK820_NVM_FAULT_RECOVERY_WRITE) && address < AK820_NVM_END) return false;
    memset(code + address, 0, 64);
    return true;
}

bool ak820_flash_program(uint16_t address, uint8_t value) {
    assert(address >= AK820_NVM_BASE && address < AK820_NVM_WRITE_END);
    ++programs;
    if (inject == AK820_NVM_FAULT_METADATA_PROGRAM && address > AK820_JOURNAL_HEADER) return false;
    if (inject == AK820_NVM_FAULT_COMMIT_PROGRAM && address == AK820_JOURNAL_HEADER) return false;
    assert(!(code[address] & (uint8_t)~value));
    code[address] |= value;
    return true;
}

bool ak820_flash_program_page(uint16_t address, const uint8_t *data) {
    assert(!(address & 63));
    for (uint8_t i = 0; i != 64; ++i) {
        if (!ak820_flash_program(address + i, data[i])) return false;
    }
    return true;
}

static void fresh(void) {
    memset(code, 0, sizeof(code));
    erases = programs = reads = cleanup = inject = 0;
    eeprom_driver_init();
}

static void snapshot(uint8_t expected_stage, uint8_t dirty) {
    uint8_t a[7], b[7];
    unsigned before = reads + erases + programs;
    ak820_nvm_diagnostic(a);
    ak820_nvm_diagnostic(b);
    assert(!memcmp(a, b, sizeof(a)));
    assert(reads + erases + programs == before); /* even readback is forbidden */
    assert(a[0] == (expected_stage != 0) && a[2] == dirty && a[6] == expected_stage);
}

int main(void) {
    uint8_t value = 0x35, status[7], cached;
    fresh();
    snapshot(AK820_NVM_FAULT_NONE, 0);
    ak820_nvm_begin();
    eeprom_write_block(&value, (void *)0x40, 1);
    snapshot(AK820_NVM_FAULT_NONE, 1);
    ak820_nvm_diagnostic(status);
    assert(status[1] == 1 && status[3] == 1 && status[4] == 1 && status[5] == 0);
    assert(code[AK820_NVM_BASE + 0x40] == 0 && !erases && !programs);
    ak820_nvm_end();
    assert(code[AK820_NVM_BASE + 0x40] == value);
    snapshot(AK820_NVM_FAULT_NONE, 0);

    for (uint8_t failure = AK820_NVM_FAULT_HEADER_ERASE; failure <= AK820_NVM_FAULT_CLEANUP; ++failure) {
        fresh(); inject = failure;
        ak820_nvm_begin();
        eeprom_write_block(&value, (void *)0x40, 1);
        ak820_nvm_end();
        snapshot(failure, 1);
        /* A normal getter still exposes RAM: that is not persistence proof. */
        eeprom_read_block(&cached, (void *)0x40, 1);
        assert(cached == value);
        if (failure < AK820_NVM_FAULT_CLEANUP) assert(code[AK820_NVM_BASE + 0x40] == 0);
        else assert(code[AK820_NVM_BASE + 0x40] == value);
        unsigned operations = erases + programs;
        /* New range faults and retries cannot replace the first error. */
        eeprom_write_block(&value, (void *)AK820_NVM_SIZE, 1);
        ak820_nvm_flush();
        ak820_nvm_end();
        snapshot(failure, 1);
        assert(erases + programs == operations);
    }

    fresh();
    eeprom_write_block(&value, (void *)AK820_NVM_SIZE, 1);
    snapshot(AK820_NVM_FAULT_WRITE_RANGE, 0);
    fresh();
    for (unsigned i = 0; i < 256; ++i) ak820_nvm_begin();
    snapshot(AK820_NVM_FAULT_BATCH_OVERFLOW, 0);
    ak820_nvm_diagnostic(status); assert(status[3] == 255);

    /* CRC16-CCITT(0xffff, 0x35 followed by 63 zero bytes) = 0x1c34.
     * Literal records exercise recovery diagnostics independently of the
     * firmware's header construction and CRC implementation. */
    for (uint8_t failure = AK820_NVM_FAULT_RECOVERY_PAGE; failure <= AK820_NVM_FAULT_RECOVERY_CLEANUP; ++failure) {
        fresh();
        const uint8_t header[9] = {0xa5, 0, 0, 0x34, 0x1c, 0xff, 0xff, 0xcb, 0xe3};
        memcpy(code + AK820_JOURNAL_HEADER, header, sizeof(header));
        code[AK820_JOURNAL_DATA] = 0x35;
        if (failure == AK820_NVM_FAULT_RECOVERY_PAGE) {
            code[AK820_JOURNAL_HEADER + 1] = 160;
            code[AK820_JOURNAL_HEADER + 5] = (uint8_t)~160;
        }
        if (failure == AK820_NVM_FAULT_RECOVERY_CRC) code[AK820_JOURNAL_DATA] ^= 1;
        inject = failure;
        eeprom_driver_init();
        snapshot(failure, 0);
    }
    puts("PASS: read-only NVM snapshots preserve dirty cache, first failure stage, blocked retries, and distinguish cached getter from CODE persistence");
    return 0;
}
