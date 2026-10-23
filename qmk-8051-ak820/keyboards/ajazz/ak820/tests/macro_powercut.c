/* SPDX-License-Identifier: GPL-2.0-or-later
 * Executes the actual board parser/upload code and actual EEPROM backend.
 * Run from qmk-8051-ak820 (memory-only, no USB):
 * cc -std=c11 -O1 -g -Wall -Wextra -Werror -Wno-clobbered \
 *    -Wno-int-to-pointer-cast -fsanitize=address,undefined \
 *    -fno-omit-frame-pointer -DAK820_BOARD= \
 *    -Ikeyboards/ajazz/ak820/tests/include \
 *    -Ikeyboards/ajazz/ak820 keyboards/ajazz/ak820/tests/macro_powercut.c \
 *    keyboards/ajazz/ak820/ak820_macro.c keyboards/ajazz/ak820/ak820_nvm.c \
 *    -o /tmp/ak820-macro-test
 * ASAN_OPTIONS=detect_leaks=0 /tmp/ak820-macro-test
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include "config.h"
#include "ak820_macro.h"
#include "ak820_nvm.h"
#include "eeprom.h"

#define MACRO_BASE (AK820_NVM_BASE + DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR)
#define MACRO_SIZE DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE
#define BUSY_ADDRESS (AK820_NVM_BASE + AK820_MACRO_BUSY_ADDR)

static uint8_t flash_image[65536], initial[65536], expected[MACRO_SIZE];
static uint8_t new_stream[52];
static unsigned long operations, cut_at;
static unsigned erase_order;
static bool inject;
static jmp_buf power_loss;

static void require(bool valid, const char *label) {
    if (!valid) {
        fprintf(stderr, "FAIL %s, cut=%lu order=%u\n", label, cut_at, erase_order);
        exit(1);
    }
}

static void bit_step(void) {
    ++operations;
    if (inject && operations == cut_at) longjmp(power_loss, 1);
}

static void validate_flash_address(uint16_t address) {
    require(address >= AK820_NVM_BASE && address < AK820_NVM_WRITE_END, "flash write bounds");
    if (address >= MACRO_BASE && address < MACRO_BASE + MACRO_SIZE)
        require(flash_image[BUSY_ADDRESS] == 1, "busy durable before macro target mutation");
}

uint8_t ak820_flash_read(uint16_t address) { return flash_image[address]; }

bool ak820_flash_erase(uint16_t address) {
    unsigned byte, bit;
    validate_flash_address(address);
    require(!(address & 63), "page alignment");
    for (byte = 0; byte < 64; ++byte) {
        unsigned offset = erase_order ? (byte * 17) % 64 : byte;
        for (bit = 0; bit < 8; ++bit) {
            flash_image[address + offset] &= (uint8_t)~(1u << bit);
            bit_step();
        }
    }
    return true;
}

bool ak820_flash_program(uint16_t address, uint8_t value) {
    unsigned bit;
    validate_flash_address(address);
    require(!(flash_image[address] & (uint8_t)~value), "zero-erased flash programming");
    for (bit = 0; bit < 8; ++bit) {
        flash_image[address] |= value & (uint8_t)(1u << bit);
        bit_step();
    }
    return true;
}

bool ak820_flash_program_page(uint16_t address, const uint8_t *data) {
    unsigned i;
    require(!(address & 63), "block-program page alignment");
    for (i = 0; i != 64; ++i) {
        unsigned offset = erase_order ? (i * 17) % 64 : i;
        if (!ak820_flash_program(address + offset, data[offset])) return false;
    }
    return true;
}

static void fixture(void) {
    memset(flash_image, 0, sizeof(flash_image));
    memset(flash_image + MACRO_BASE, 'O', 110); /* old macro plus16 empty terminators */
    flash_image[BUSY_ADDRESS + 1] = 126;
    memcpy(initial, flash_image, sizeof(initial));
    inject = false;
    operations = 0;
    cut_at = 0;
    eeprom_driver_init();
    require(ak820_macro_ready(), "initial complete macros enabled");
}

static void write_chunks(const uint8_t *data, uint16_t size) {
    uint16_t offset;
    for (offset = 0; offset < size;) {
        uint16_t count = size - offset;
        if (count > 28) count = 28;
        require(ak820_macro_write(offset, count, data + offset), "contiguous upload accepted");
        offset += count;
    }
}

static void parser_tests(void) {
    uint8_t grammar[80], changed[116], zeros[28] = {0};
    uint8_t invalid[][4] = {{1,0,9,9}, {1,8,9,9}, {1,255,9,9}, {1,1,0,9},
                            {1,4,0,9}, {1,4,9,0}, {1,5,0,9}, {1,7,9,0}};
    unsigned size = 0, opcode, split, i;
    unsigned long before;
    grammar[size++] = 'a';
    for (opcode = 1; opcode <= 7; ++opcode) {
        grammar[size++] = 1;
        grammar[size++] = opcode;
        grammar[size++] = 255;
        if (opcode >= 4) grammar[size++] = 255;
    }
    memset(grammar + size, 0, 16);
    size += 16;
    for (split = 1; split < size; ++split) {
        fixture();
        require(ak820_macro_write(0, split, grammar), "grammar prefix accepted");
        require(!ak820_macro_ready(), "incomplete grammar disabled");
        require(ak820_macro_write(split, size - split, grammar + split), "split operands and terminators accepted");
        require(ak820_macro_ready() && !memcmp(flash_image + MACRO_BASE, grammar, size), "complete grammar published");
        require(ak820_macro_length() == size, "committed logical length hides stale tail");
        require(flash_image[MACRO_BASE + 80] == 'O', "old physical tail need not be erased");
    }
    for (i = 0; i < sizeof(invalid) / sizeof(invalid[0]); ++i) {
        fixture();
        require(!ak820_macro_write(0, 4, invalid[i]), "invalid opcode or zero operand rejected");
        require(!operations && ak820_macro_ready(), "invalid first chunk leaves old set intact");
    }
    for (i = 128; i <= 255; ++i) {
        fixture();
        memset(grammar, 0, 17);
        grammar[0] = (uint8_t)i;
        require(!ak820_macro_write(0, 17, grammar), "non-ASCII plain text rejected");
        require(!operations && ak820_macro_ready(), "unsupported text leaves old macros intact");
    }
    fixture();
    memset(grammar, 0, 17); grammar[0] = 127;
    require(ak820_macro_write(0, 17, grammar) && ak820_macro_ready(), "last supported ASCII byte accepted");
    fixture();
    memset(grammar, 0, 16); grammar[16] = 'X';
    require(!ak820_macro_write(0, 17, grammar) && !operations, "nonzero data after16 terminators rejected");
    require(!ak820_macro_write(0, 0, zeros), "empty chunk rejected");
    require(!ak820_macro_write(65535, 2, zeros), "wrapped offset rejected");
    require(!ak820_macro_write(MACRO_SIZE - 1, 2, zeros), "overrun rejected before mutation");
    require(!ak820_macro_write(28, 1, zeros), "missing offset0 rejected");
    require(ak820_macro_write(0, 15, zeros), "15 empty macros accepted as incomplete");
    require(!ak820_macro_ready(), "15 terminators not committed");
    before = operations;
    require(!ak820_macro_write(16, 1, zeros) && operations == before, "gap rejected without mutation");
    require(ak820_macro_write(0, 15, zeros) && operations == before, "duplicate first chunk does not restart");
    eeprom_driver_init();
    require(ak820_nvm_ok() && !ak820_macro_ready(), "busy survives reboot");
    require(!ak820_macro_write(15, 1, zeros), "RAM coverage is not inferred from old EEPROM after reboot");
    require(ak820_macro_write(0, 16, zeros) && ak820_macro_ready(), "restart from0 completes");
    before = operations;
    require(ak820_macro_write(0, 16, zeros) && operations == before, "completed single-packet retry is idempotent");
    require(ak820_macro_write(16, 28, zeros) && operations == before, "contiguous zero padding needs no rewrite");
    zeros[0] = 3;
    require(!ak820_macro_write(44, 1, zeros), "later nonzero trailing chunk rejected");
    zeros[0] = 0;

    fixture();
    memset(changed, 'a', 100); memset(changed + 100, 0, 16);
    require(ak820_macro_write(0, 28, changed), "long first chunk");
    require(ak820_macro_write(28, 28, changed + 28), "long second chunk");
    before = operations;
    require(ak820_macro_write(0, 28, changed) && operations == before, "old matching first chunk does not rewind coverage");
    changed[30] = 'b';
    require(ak820_macro_write(28, 28, changed + 28), "changed retransmission validates received prefix");
    require(ak820_macro_write(56, 28, changed + 56), "rewound upload continues");
    require(ak820_macro_write(84, 28, changed + 84), "remaining macro terminators");
    require(ak820_macro_write(112, 4, changed + 112) && ak820_macro_ready(), "rewound stream completes");
    before = operations;
    require(ak820_macro_write(112, 4, changed + 112) && operations == before, "last packet retry is idempotent");
    /* New edit with an unchanged first packet still starts a busy generation. */
    require(ak820_macro_write(0, 28, changed) && !ak820_macro_ready(), "new matching prefix begins new upload after commit");
    require(ak820_macro_reset() && ak820_macro_ready() && ak820_macro_length() == 16, "explicit reset publishes16 empty macros");
    for (i = 0; i < 16; ++i) require(!flash_image[MACRO_BASE + i], "reset clears only logical stream");
    require(flash_image[MACRO_BASE + 30] == 'b', "reset hides stale physical tail");

    fixture();
    flash_image[BUSY_ADDRESS + 1] = 0xff; flash_image[BUSY_ADDRESS + 2] = 0xff;
    eeprom_driver_init();
    require(!ak820_macro_ready() && !ak820_macro_length(), "out-of-range durable length disables macros");
    flash_image[BUSY_ADDRESS + 1] = 0; flash_image[BUSY_ADDRESS + 2] = 0;
    eeprom_driver_init();
    require(!ak820_macro_ready(), "length too small for16 macros disables execution");

    fixture();
    memset(expected, 'Z', MACRO_SIZE - 16); memset(expected + MACRO_SIZE - 16, 0, 16);
    write_chunks(expected, MACRO_SIZE);
    require(ak820_macro_ready() && !memcmp(flash_image + MACRO_BASE, expected, MACRO_SIZE), "all macro bytes usable without reserved last byte");
}

int main(void) {
    unsigned long max_operations, cut;
    volatile unsigned long cases = 0;
    unsigned order;
    parser_tests();
    memset(new_stream, 'N', 32);
    new_stream[32] = 1; new_stream[33] = 5; new_stream[34] = 3; new_stream[35] = 0x52;
    memset(new_stream + 36, 0, 16);
    memset(expected, 0, sizeof(expected));
    memcpy(expected, new_stream, sizeof(new_stream));
    fixture();
    write_chunks(new_stream, sizeof(new_stream));
    max_operations = operations;
    require(ak820_macro_ready(), "uninterrupted upload completes");

    for (order = 0; order < 2; ++order) {
        erase_order = order;
        for (cut = 1; cut <= max_operations; ++cut) {
            memcpy(flash_image, initial, sizeof(flash_image));
            inject = false; eeprom_driver_init();
            operations = 0; cut_at = cut; inject = true;
            if (!setjmp(power_loss)) write_chunks(new_stream, sizeof(new_stream));
            inject = false; eeprom_driver_init();
            require(ak820_nvm_ok(), "journal recovery after interrupted macro upload");
            if (ak820_macro_ready()) {
                uint16_t length = ak820_macro_length();
                require((length == 126 && !memcmp(flash_image + MACRO_BASE, initial + MACRO_BASE, length)) ||
                        (length == sizeof(new_stream) && !memcmp(flash_image + MACRO_BASE, expected, length)),
                        "enabled stream is exactly old or complete new, never a partial upload");
            } else {
                require(flash_image[BUSY_ADDRESS] == 1, "interrupted partial stream remains durably disabled");
            }
            require(!memcmp(flash_image, initial, AK820_NVM_BASE), "code and loader untouched");
            ++cases;
        }
    }
    printf("PASS: Vial6 grammar/split/bounds/retry/restart/full-capacity checks; %lu upload power cuts across2 erase orders\n", cases);
    return 0;
}
