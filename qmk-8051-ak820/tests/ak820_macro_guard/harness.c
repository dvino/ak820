/* SPDX-License-Identifier: GPL-2.0-or-later
 * Host-only stubs and assertions. run.py inserts the current production
 * decode_keycode(), dynamic_keymap_macro_send(), and the production string
 * walkers at the marker below. Only key-emission endpoints are stubbed.
 */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "send_string_keycodes.h"

#define AK820_BOARD
#define DYNAMIC_KEYMAP_MACRO_COUNT 16
#define DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR ((uintptr_t)stream)
#define DYNAMIC_KEYMAP_MACRO_DELAY 0

static uint8_t stream[128];
static uint16_t stream_length;
static bool ready = true;
static unsigned events, texts, waits;
static char event_kinds[128];
static uint16_t event_codes[128];
static uint8_t text_bytes[128];

void dynamic_keymap_macro_send(uint8_t id);
void send_string(const char *s);
void send_string_with_delay(const char *s, uint8_t delay);
static bool ak820_macro_ready(void) { return ready; }
static uint16_t ak820_macro_length(void) { return stream_length; }
static uint8_t eeprom_read_byte(const uint8_t *p) {
    assert(p >= stream && p < stream + stream_length);
    return *p;
}
static void emit(char kind, uint16_t code) {
    assert(events < sizeof(event_kinds));
    event_kinds[events] = kind;
    event_codes[events++] = code;
}
static void tap_code(uint8_t code) { emit('t', code); }
static void register_code(uint8_t code) { emit('d', code); }
static void unregister_code(uint8_t code) { emit('u', code); }
static void send_char(char c) {
    /* The production sender has 128-entry ASCII lookup tables. */
    assert((uint8_t)c < 128);
    assert(texts < sizeof(text_bytes));
    text_bytes[texts++] = (uint8_t)c;
}
static void wait_ms(uint16_t ms) { waits += ms; }
static void extended(char kind, uint16_t kc) {
    emit(kind, kc);
    if (kc == 0x7701) {
        dynamic_keymap_macro_send(0);
        dynamic_keymap_macro_send(1);
    }
}
static void vial_keycode_tap(uint16_t kc) { extended('T', kc); }
static void vial_keycode_down(uint16_t kc) { extended('D', kc); }
static void vial_keycode_up(uint16_t kc) { extended('U', kc); }

/* AK820_ACTUAL_SOURCE */

int main(void) {
    const uint8_t recursive[] = {1, 5, 1, 0x77, 1, 6, 1, 0x77, 1, 7, 1, 0x77, 'X', 0, 'Y', 0};
    memcpy(stream, recursive, sizeof(recursive));
    stream_length = 30;
    dynamic_keymap_macro_send(0);
    assert(events == 3 && texts == 1);
    dynamic_keymap_macro_send(0);
    assert(events == 6 && texts == 2);
    dynamic_keymap_macro_send(1);
    assert(events == 6 && texts == 3);

    ready = false;
    dynamic_keymap_macro_send(0);
    assert(events == 6);
    ready = true;
    dynamic_keymap_macro_send(16);
    assert(events == 6);
    stream_length = 1;
    stream[0] = 'X';
    dynamic_keymap_macro_send(1);
    assert(events == 6);

    /* Every interpreter early break must release the playback guard. */
    memset(stream, 0, sizeof(stream));
    stream_length = 16;
    dynamic_keymap_macro_send(0);
    stream[0] = 1;
    stream[1] = 0;
    dynamic_keymap_macro_send(0);
    stream[1] = 4;
    stream[2] = 0;
    stream[3] = 1;
    dynamic_keymap_macro_send(0);
    stream[2] = 1;
    stream[3] = 0;
    dynamic_keymap_macro_send(0);
    memset(stream, 0, sizeof(stream));
    stream[0] = 'X';
    dynamic_keymap_macro_send(0);
    assert(texts == 4);

    /* A Vial delay can exceed the signed16-bit range of the target. */
    stream[0] = 1;
    stream[1] = 4;
    stream[2] = 255;
    stream[3] = 255;
    stream[4] = 0;
    dynamic_keymap_macro_send(0);
    assert(waits == 65024);
    memset(stream, 0, sizeof(stream));
    stream[0] = 'Y';
    dynamic_keymap_macro_send(0);
    assert(texts == 5);
    /* Every extended/basic combination must restore the short command's NUL.
     * Use the real string consumer: a stub used to conceal this defect. */
    for (uint8_t ext = 5; ext <= 7; ++ext) {
        for (uint8_t basic = 1; basic <= 3; ++basic) {
            const uint8_t mixed[] = {1, ext, 0x21, 0x52, 1, basic, 4, 0};
            memset(stream, 0, sizeof(stream));
            memcpy(stream, mixed, sizeof(mixed));
            stream_length = sizeof(mixed) + 15;
            events = texts = waits = 0;
            dynamic_keymap_macro_send(0);
            assert(events == 2 && texts == 0 && waits == 0);
            assert(event_codes[0] == 0x5221 && event_codes[1] == 4);
            assert(event_kinds[0] == "TDU"[ext - 5]);
            assert(event_kinds[1] == "tdu"[basic - 1]);
        }
    }

    /* Non-ASCII operands are valid; only unencoded plain text is restricted. */
    const uint8_t operands[] = {1, 2, 0xE0, 1, 3, 0xE0, 0};
    memset(stream, 0, sizeof(stream));
    memcpy(stream, operands, sizeof(operands));
    stream_length = sizeof(operands) + 15;
    events = texts = 0;
    dynamic_keymap_macro_send(0);
    assert(events == 2 && !texts && event_codes[0] == 0xE0 && event_codes[1] == 0xE0);

    /* Older EEPROM streams may predate publication validation. Stop such text
     * before the ASCII sender; the playback guard must permit the next macro. */
    for (unsigned value = 128; value <= 255; ++value) {
        memset(stream, 0, sizeof(stream));
        stream[0] = (uint8_t)value;
        stream_length = 17;
        events = texts = 0;
        dynamic_keymap_macro_send(0);
        assert(!events && !texts);
        stream[0] = 'X';
        dynamic_keymap_macro_send(0);
        assert(texts == 1 && text_bytes[0] == 'X');
    }
    puts("PASS: real macro/string playback, recursive-action guard, mixed extended/basic termination, high-byte operands, legacy non-ASCII rejection, and delay65024.");
    return 0;
}
