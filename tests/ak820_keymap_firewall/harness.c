#include "fixture.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool vial_unlocked;
#define EEPROM_BYTES (DYNAMIC_KEYMAP_EEPROM_ADDR + MATRIX_ROWS * MATRIX_COLS * DYNAMIC_KEYMAP_LAYER_COUNT * 2u + 2u)
#define MAX_WRITE_BYTES 32u

typedef struct {
    uint8_t packet[40];
    unsigned reads;
    uintptr_t read_addr[2];
    unsigned fault_status;
    unsigned writes;
    uintptr_t write_addr;
    size_t write_len;
    uintptr_t write_pointer;
    uint8_t write_bytes[MAX_WRITE_BYTES];
} result_t;
static result_t state;
static uint8_t eeprom[EEPROM_BYTES];
static unsigned fault_at;

uint8_t eeprom_read_byte(const uint8_t *p) {
    uintptr_t address = (uintptr_t)p;
    if (address >= sizeof eeprom || state.reads >= 2) abort();
    state.read_addr[state.reads++] = address;
    if (state.reads == fault_at) {
        state.fault_status = 1;
        return 0xFF;
    }
    return eeprom[address];
}

void eeprom_update_byte(uint8_t *p, uint8_t value) {
    uintptr_t address = (uintptr_t)p;
    if (state.writes || address >= sizeof eeprom) abort();
    state.writes = 1;
    state.write_addr = address;
    state.write_len = 1;
    state.write_pointer = 0;
    state.write_bytes[0] = value;
}

void ak820_eeprom_write_block_xdata(const void *p, void *dest, size_t size) {
    uintptr_t address = (uintptr_t)dest;
    if (state.writes || size > MAX_WRITE_BYTES || address + size > sizeof eeprom) abort();
    state.writes = 1;
    state.write_addr = address;
    state.write_len = size;
    state.write_pointer = (uintptr_t)p;
    memcpy(state.write_bytes, p, size);
}

#define dynamic_keymap_set_buffer reference
#include "oracle.inc"
#undef dynamic_keymap_set_buffer
#define dynamic_keymap_set_buffer actual
#ifndef CURRENT_INCLUDE
#define CURRENT_INCLUDE "current.inc"
#endif
#include CURRENT_INCLUDE
#undef dynamic_keymap_set_buffer

static unsigned long long cases;
static uint32_t rng = 0x820026B5u;
static uint32_t random32(void) {
    rng ^= rng << 13;
    rng ^= rng >> 17;
    rng ^= rng << 5;
    return rng;
}

static void compare(uint16_t offset, uint16_t size, unsigned pattern, unsigned locked, unsigned fault) {
    result_t initial = {0}, expected;
    memset(initial.packet, 0xA5, sizeof initial.packet);
    for (unsigned i = 0; i < MAX_WRITE_BYTES; ++i) {
        switch (pattern) {
            case 0: initial.packet[4+i] = 0; break;
            case 1: initial.packet[4+i] = 0xFF; break;
            case 2: initial.packet[4+i] = (i & 1) ? 0x00 : (QK_BOOT >> 8); break;
            case 3: initial.packet[4+i] = (i & 1) ? (QK_BOOT >> 8) : 0x00; break;
            case 4: initial.packet[4+i] = (i % 3) ? (QK_BOOT >> 8) : (QK_BOOT & 0xFF); break;
            default: initial.packet[4+i] = (uint8_t)random32(); break;
        }
    }
    vial_unlocked = !locked;
    fault_at = fault;
    state = initial;
    reference(offset, size, state.packet + 4);
    expected = state;
    state = initial;
    actual(offset, size, state.packet + 4);
    if (memcmp(&state, &expected, sizeof state) != 0) {
        fprintf(stderr, "DIFF offset=%u size=%u pattern=%u locked=%u fault=%u\n",
                offset, size, pattern, locked, fault);
        exit(1);
    }
    if (state.packet[0] != 0xA5 || state.packet[1] != 0xA5 || state.packet[2] != 0xA5 ||
        state.packet[3] != 0xA5 || state.packet[36] != 0xA5 || state.packet[37] != 0xA5 ||
        state.packet[38] != 0xA5 || state.packet[39] != 0xA5) {
        fprintf(stderr, "CANARY offset=%u size=%u\n", offset, size);
        exit(1);
    }
    ++cases;
}

int main(void) {
    if (DYNAMIC_KEYMAP_EEPROM_ADDR + MATRIX_ROWS * MATRIX_COLS * DYNAMIC_KEYMAP_LAYER_COUNT * 2u != EEPROM_BYTES - 2u) abort();
    for (unsigned e = 0; e < 3; ++e) {
        for (unsigned i = 0; i < sizeof eeprom; ++i)
            eeprom[i] = e == 0 ? 0 : e == 1 ? (uint8_t)(QK_BOOT >> 8) : (uint8_t)(i * 19u);
        for (unsigned offset = 0; offset < MATRIX_ROWS * MATRIX_COLS * DYNAMIC_KEYMAP_LAYER_COUNT * 2u; ++offset)
            for (unsigned size = 0; size <= 29; ++size)
                for (unsigned locked = 0; locked < 2; ++locked)
                    for (unsigned pattern = 0; pattern < 6; ++pattern)
                        for (unsigned fault = 0; fault <= 2; ++fault)
                            compare((uint16_t)offset, (uint16_t)size, pattern, locked, fault);
    }
    const uint16_t sizes[] = {0,1,2,27,28,29,255,256,257,32767,32768,65535};
    for (unsigned offset = 0; offset <= UINT16_MAX; ++offset)
        for (unsigned si = 0; si < sizeof sizes / sizeof sizes[0]; ++si)
            for (unsigned locked = 0; locked < 2; ++locked)
                compare((uint16_t)offset, sizes[si], 5, locked, offset % 3);
    for (unsigned i = 0; i < 300000; ++i)
        compare((uint16_t)random32(), sizes[random32() % (sizeof sizes / sizeof sizes[0])],
                5, random32() % 2, random32() % 3);
    printf("PASS differential_cases=%llu matrix_offsets=%u matrix_sizes=30 lock_states=2 patterns=6 fault_schedules=3 high16_offsets=65536 high16_sizes=12 random_cases=300000\n",
           cases, (unsigned)(MATRIX_ROWS * MATRIX_COLS * DYNAMIC_KEYMAP_LAYER_COUNT * 2u));
    return 0;
}
