/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "send_string.h"
#include "vial.h"
#define DYNAMIC_KEYMAP_MACRO_DELAY 2
static uint8_t memory[UINT16_MAX + 1u];
static uint16_t length;
static uint32_t trace_events[65536], trace_count, expected_count;
static bool compare_events;
static void trace(uint8_t event, uint16_t value) {
    uint32_t encoded = ((uint32_t)event << 16) | value;
    assert(trace_count < sizeof(trace_events) / sizeof(trace_events[0]));
    if (compare_events) {
        assert(trace_count < expected_count && trace_events[trace_count] == encoded);
    } else {
        trace_events[trace_count] = encoded;
    }
    ++trace_count;
}
bool ak820_macro_ready(void) { return true; }
uint16_t ak820_macro_length(void) { return length; }
uint8_t eeprom_read_byte(const uint8_t *ptr) { return memory[(uintptr_t)ptr]; }
void tap_code(uint8_t v) { trace('t', v); }
void register_code(uint8_t v) { trace('d', v); }
void unregister_code(uint8_t v) { trace('u', v); }
void send_char(char v) { trace('c', (uint8_t)v); }
void wait_ms(uint16_t v) { trace('w', v); }
void vial_keycode_tap(uint16_t v) { trace('T', v); }
void vial_keycode_down(uint16_t v) { trace('D', v); }
void vial_keycode_up(uint16_t v) { trace('U', v); }
/* SOURCES */
static void compare(const uint8_t *stream, size_t size, uint8_t slot) {
    assert(size < DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE);
    memset(memory, 0, sizeof(memory));
    memcpy(memory + DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR, stream, size);
    length = size + DYNAMIC_KEYMAP_MACRO_COUNT;
    compare_events = false; trace_count = 0;
    rc4_dynamic_keymap_macro_send(slot);
    expected_count = trace_count;
    compare_events = true; trace_count = 0;
    dynamic_keymap_macro_send(slot);
    assert(expected_count == trace_count);
}
int main(void) {
    uint8_t stream[32];
    unsigned cases = 0;
    for (uint16_t code = 2; code < 128; ++code) {
        stream[0] = code; stream[1] = 0;
        compare(stream, 2, 0); ++cases;
    }
    for (uint8_t op = SS_TAP_CODE; op <= SS_UP_CODE; ++op)
        for (uint16_t code = 1; code <= 255; ++code) {
            stream[0] = SS_QMK_PREFIX; stream[1] = op; stream[2] = code; stream[3] = 0;
            compare(stream, 4, 0); ++cases;
        }
    for (uint8_t op = VIAL_MACRO_EXT_TAP; op <= VIAL_MACRO_EXT_UP; ++op)
        for (uint32_t code = 0; code <= UINT16_MAX; ++code) {
            if (!(code & 255) || !(code >> 8)) continue;
            stream[0] = SS_QMK_PREFIX; stream[1] = op; stream[2] = code; stream[3] = code >> 8; stream[4] = 0;
            compare(stream, 5, 0); ++cases;
        }
    const uint8_t delays[] = {1,2,127,128,254,255};
    for (unsigned i = 0; i < sizeof(delays); ++i)
        for (unsigned j = 0; j < sizeof(delays); ++j) {
            stream[0] = SS_QMK_PREFIX; stream[1] = SS_DELAY_CODE; stream[2] = delays[i]; stream[3] = delays[j]; stream[4] = 'a'; stream[5] = 0;
            compare(stream, 6, 0); ++cases;
        }
    const uint8_t mixed[] = {'A',1,6,0x21,0x52,1,2,0xe0,1,1,4,1,3,0xe0,1,4,2,2,1,7,0x21,0x52,'b',0,'Z'};
    for (uint8_t slot = 0; slot <= DYNAMIC_KEYMAP_MACRO_COUNT; ++slot) { compare(mixed,sizeof(mixed),slot); ++cases; }
    printf("PASS: %u playback cases match RC4 event+delay traces (all binary 8-bit/16-bit operands, ASCII, slot bounds, mixed commands, delay boundaries).\n", cases);
}
