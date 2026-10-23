// SPDX-License-Identifier: GPL-2.0-or-later
// Runs the actual EEPROM backend against zero-erased, 0->1 flash, with
// power cuts during individual erase/program bits and journal recovery.
/* Run from qmk-8051-ak820 (without AK820_BOARD: isolate the journal backend):
 * cc -std=c11 -O1 -g -Wall -Wextra -Werror -Wno-clobbered \
 *    -fsanitize=address,undefined -fno-omit-frame-pointer \
 *    -Ikeyboards/ajazz/ak820 keyboards/ajazz/ak820/tests/nvm_powercut.c \
 *    keyboards/ajazz/ak820/ak820_nvm.c -o /tmp/ak820-nvm-test
 * ASAN_OPTIONS=detect_leaks=0 /tmp/ak820-nvm-test
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include "ak820_nvm.h"

static uint8_t flash_image[65536], original[65536], after_cut[65536];
static unsigned long operations, cut_at;
static unsigned erase_order;
static jmp_buf power_loss;
static bool inject;
static unsigned erase_count, program_count;

void eeprom_driver_init(void);
void eeprom_read_block(void *, const void *, size_t);
void eeprom_write_block(const void *, void *, size_t);
void eeprom_driver_erase(void);

static void step(void) {
    ++operations;
    if (inject && operations == cut_at) longjmp(power_loss, 1);
}

uint8_t ak820_flash_read(uint16_t address) { return flash_image[address]; }

bool ak820_flash_erase(uint16_t address) {
    unsigned i, bit;
    if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END || (address & 63)) abort();
    ++erase_count;
    for (i = 0; i < 64; ++i) {
        unsigned offset = erase_order == 0 ? i : erase_order == 1 ? 63 - i : (i * 17) % 64;
        for (bit = 0; bit < 8; ++bit) {
            flash_image[address + offset] &= (uint8_t)~(1u << bit);
            step();
        }
    }
    return true;
}

bool ak820_flash_program(uint16_t address, uint8_t value) {
    unsigned bit;
    if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END) abort();
    ++program_count;
    if (flash_image[address] & (uint8_t)~value) abort();
    for (bit = 0; bit < 8; ++bit) {
        flash_image[address] |= value & (uint8_t)(1u << bit);
        step();
    }
    return true;
}

bool ak820_flash_program_page(uint16_t address, const uint8_t *data) {
    unsigned i;
    if (address & 63) abort();
    /* A physical block may lose power partway through programming. Exercise
     * every byte/bit in three orders; do not treat one IAP as atomic. */
    for (i = 0; i != 64; ++i) {
        unsigned offset = erase_order == 0 ? i : erase_order == 1 ? 63 - i : (i * 17) % 64;
        if (!ak820_flash_program(address + offset, data[offset])) return false;
    }
    return true;
}

static void require(bool pass, const char *name) {
    if (!pass) { fprintf(stderr, "FAIL %s, cut=%lu, order=%u\n", name, cut_at, erase_order); exit(1); }
}

static void init_fixture(void) {
    unsigned i;
    for (i = 0; i < sizeof(flash_image); ++i) flash_image[i] = (uint8_t)((i * 29 + 113) >> 2);
    memset(flash_image + AK820_JOURNAL_DATA, 0, 128);
    memcpy(original, flash_image, sizeof(original));
    inject = false;
    operations = erase_count = program_count = 0;
    eeprom_driver_init();
}

int main(void) {
    uint8_t desired[64], before[64], readback[64], cross[91];
    unsigned i, order;
    unsigned long max_operations, cut, cases = 0;
    const uint16_t offset = 7 * 64;
    for (i = 0; i < sizeof(desired); ++i) desired[i] = (uint8_t)(i * 7 + 41);
    for (i = 0; i < sizeof(cross); ++i) cross[i] = (uint8_t)(251 - i * 2);

    init_fixture();
    memcpy(before, flash_image + AK820_NVM_BASE + offset, 64);
    eeprom_write_block(desired, (void *)(uintptr_t)offset, sizeof(desired));
    require(ak820_nvm_ok(), "full write");
    max_operations = operations;
    eeprom_driver_init();
    eeprom_read_block(readback, (void *)(uintptr_t)offset, sizeof(readback));
    require(!memcmp(desired, readback, 64), "power-cycle persistence");

    // Every bit operation in prepare/commit/target/cleanup, for three erase
    // orders. Recover with a fresh backend state, using the same implementation.
    for (order = 0; order < 3; ++order) {
        erase_order = order;
        for (cut = 1; cut <= max_operations; ++cut) {
            memcpy(flash_image, original, sizeof(original));
            inject = false;
            eeprom_driver_init();
            operations = 0; cut_at = cut; inject = true;
            if (!setjmp(power_loss)) eeprom_write_block(desired, (void *)(uintptr_t)offset, 64);
            inject = false;
            eeprom_driver_init();
            require(ak820_nvm_ok(), "recovery after power cut");
            eeprom_read_block(readback, (void *)(uintptr_t)offset, 64);
            require(!memcmp(readback, before, 64) || !memcmp(readback, desired, 64), "page is old or new, never torn");
            require(!memcmp(flash_image, original, AK820_NVM_BASE), "code and boot unchanged");
            require(!memcmp(flash_image + AK820_NVM_WRITE_END, original + AK820_NVM_WRITE_END,
                            sizeof(flash_image) - AK820_NVM_WRITE_END), "manifest and tail unchanged");
            ++cases;
        }
    }

    // Interrupt replay itself after a valid committed record is left behind.
    erase_order = 0;
    memcpy(flash_image, original, sizeof(original));
    eeprom_driver_init(); operations = 0; cut_at = max_operations - 800; inject = true;
    if (!setjmp(power_loss)) eeprom_write_block(desired, (void *)(uintptr_t)offset, 64);
    inject = false;
    memcpy(after_cut, flash_image, sizeof(after_cut));
    operations = 0; eeprom_driver_init(); max_operations = operations;
    for (cut = 1; cut <= max_operations; ++cut) {
        memcpy(flash_image, after_cut, sizeof(after_cut));
        operations = 0; cut_at = cut; inject = true;
        if (!setjmp(power_loss)) eeprom_driver_init();
        inject = false; eeprom_driver_init();
        require(ak820_nvm_ok(), "repeated recovery");
        eeprom_read_block(readback, (void *)(uintptr_t)offset, 64);
        require(!memcmp(readback, desired, 64), "committed journal replays new page");
        ++cases;
    }

    init_fixture();
    ak820_nvm_begin();
    for (i = 0; i < 64; ++i) eeprom_write_block(desired + i, (void *)(uintptr_t)(offset + i), 1);
    require(operations == 0, "batch coalesces bytes");
    ak820_nvm_flush();
    require(ak820_nvm_ok() && erase_count == 4, "one journal transaction for page");
    ak820_nvm_end();
    operations = 0;
    eeprom_write_block(desired, (void *)(uintptr_t)offset, 64);
    require(operations == 0, "retry of durable same data does not erase");
    eeprom_write_block(cross, (void *)(uintptr_t)(offset + 53), sizeof(cross));
    eeprom_driver_init();
    for (i = 0; i < sizeof(cross); ++i) require(ak820_flash_read(AK820_NVM_BASE + offset + 53 + i) == cross[i], "cross-page write");
    operations = 0;
    eeprom_write_block(cross, (void *)(uintptr_t)(AK820_NVM_SIZE - 5), 6);
    require(!ak820_nvm_ok() && operations == 0, "out-of-bounds request rejected before mutation");
    printf("PASS: %lu power-cut cases plus persistence, batching, retry, bounds, cross-page checks\n", cases);
    return 0;
}
