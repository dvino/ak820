#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define AK820_BOARD 1
#define VIAL_ENABLE 1
#define __SDCC_mcs51 1
#define __xdata

enum {
    id_dynamic_keymap_macro_get_buffer = 0x0e,
    id_dynamic_keymap_macro_set_buffer = 0x0f,
    id_dynamic_keymap_get_buffer = 0x12,
    id_dynamic_keymap_set_buffer = 0x13,
};

static struct {
    unsigned calls;
    uint16_t offset;
    uint16_t size;
    uint8_t *data;
    bool macro_set_ok;
} observed;
static bool vial_unlocked = true;
static bool reply_reached;

/* The test harness receives the exact four case bodies from via.c. */

static void dynamic_keymap_macro_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    ++observed.calls; observed.offset = offset; observed.size = size; observed.data = data;
}
static bool dynamic_keymap_macro_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    ++observed.calls; observed.offset = offset; observed.size = size; observed.data = data;
    return observed.macro_set_ok;
}
static void dynamic_keymap_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    ++observed.calls; observed.offset = offset; observed.size = size; observed.data = data;
}
static void dynamic_keymap_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    ++observed.calls; observed.offset = offset; observed.size = size; observed.data = data;
}

/* Return value models whether raw_hid_receive reaches its final reply send.
 * The four dispatch bodies below are extracted verbatim from production. */
static void dispatch(uint8_t packet[32], uint8_t length) {
    uint8_t *command_id = &packet[0];
    uint8_t *command_data = &packet[1];
    reply_reached = false;
    if (length != 32) return;
    switch (packet[0]) {
        /*__CASE_0__*/
        /*__CASE_1__*/
        /*__CASE_2__*/
        /*__CASE_3__*/
        default: break;
    }
    reply_reached = true;
}

static void reset_observed(void) {
    memset(&observed, 0, sizeof(observed));
    observed.macro_set_ok = true;
}
static void request(uint8_t packet[32], uint8_t command, uint16_t offset, uint8_t size) {
    memset(packet, 0, 32);
    packet[0] = command;
    packet[1] = (uint8_t)(offset >> 8);
    packet[2] = (uint8_t)offset;
    packet[3] = size;
    for (unsigned i = 4; i < 32; ++i) packet[i] = (uint8_t)i;
}
static void expect_forwarded(uint8_t command, uint16_t offset, uint8_t size) {
    uint8_t packet[32];
    reset_observed();
    request(packet, command, offset, size);
    dispatch(packet, 32);
    assert(reply_reached == !(command == id_dynamic_keymap_macro_set_buffer && size > 28));
    if (size <= 28) {
        assert(observed.calls == 1);
        assert(observed.offset == offset);
        assert(observed.size == size);
        assert(observed.data == &packet[4]);
    } else {
        assert(observed.calls == 0);
    }
}
int main(void) {
    uint8_t packet[32];
    const uint16_t offsets[] = {0, 0x00ff, 0x0100, 1535, 1536, 0xffff};
    const uint8_t sizes[] = {0, 1, 28, 29};
    const uint8_t commands[] = {
        id_dynamic_keymap_macro_get_buffer, id_dynamic_keymap_macro_set_buffer,
        id_dynamic_keymap_get_buffer, id_dynamic_keymap_set_buffer,
    };
    for (unsigned c = 0; c < sizeof(commands); ++c)
        for (unsigned o = 0; o < sizeof(offsets) / sizeof(offsets[0]); ++o)
            for (unsigned s = 0; s < sizeof(sizes); ++s)
                expect_forwarded(commands[c], offsets[o], sizes[s]);

    /* The production macro setter must withhold its reply on storage failure,
     * and preserve the exact decoded fields and data pointer passed to storage. */
    reset_observed(); request(packet, id_dynamic_keymap_macro_set_buffer, 0xffff, 28);
    observed.macro_set_ok = false;
    dispatch(packet, 32);
    assert(!reply_reached);
    assert(observed.calls == 1 && observed.offset == 0xffff && observed.size == 28);
    assert(observed.data == &packet[4]);

    reset_observed(); request(packet, id_dynamic_keymap_macro_set_buffer, 1535, 29);
    dispatch(packet, 32);
    assert(!reply_reached);
    assert(observed.calls == 0);

    reset_observed(); request(packet, id_dynamic_keymap_macro_get_buffer, 0xffff, 1);
    dispatch(packet, 31);
    assert(!reply_reached);
    assert(observed.calls == 0);

    puts("PASS: four extracted production VIA bulk cases preserve big-endian offsets, size gates, data-pointer forwarding, and macro-set no-reply failures");
    return 0;
}
