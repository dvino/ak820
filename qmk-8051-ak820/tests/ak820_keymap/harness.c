/* SPDX-License-Identifier: GPL-2.0-or-later
 * Memory-only flash and peripheral stubs. run.py inserts unchanged production
 * VIA/keymap function bodies; it links the real board NVM and EEPROM backend.
 */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "config.h"
#include "ak820_nvm.h"
#include "ak820_macro.h"
#include "eeprom.h"
#define VIAL_ENABLE
#define __xdata
#define BUILD_ID AK820_NVM_BUILD_ID
#define VIA_EEPROM_MAGIC_ADDR 37
#define DYNAMIC_BUFFER_MEM
#define VIA_PROTOCOL_VERSION 9
#define QK_BOOT 0x7C00
#define KC_NO 0
typedef uint16_t dynamic_buffer_size_t;
typedef uint8_t matrix_row_t;
static uint8_t flash_image[65536];
static unsigned erases, programs, replies;
bool vial_unlocked, vial_unlock_in_progress;
enum { vial_get_keyboard_id = 0, vial_get_size = 1, vial_get_def = 2,
       vial_get_unlock_status = 5, vial_unlock_start = 6, vial_unlock_poll = 7, vial_lock = 8 };
void eeprom_driver_init(void);
uint8_t ak820_flash_read(uint16_t address) { return flash_image[address]; }
bool ak820_flash_erase(uint16_t address) {
    assert(address >= AK820_NVM_BASE && address < AK820_NVM_WRITE_END && !(address & 63));
    memset(flash_image + address, 0, 64);
    ++erases;
    return true;
}
bool ak820_flash_program(uint16_t address, uint8_t value) {
    assert(address >= AK820_NVM_BASE && address < AK820_NVM_WRITE_END);
    assert(!(flash_image[address] & (uint8_t)~value));
    flash_image[address] |= value;
    ++programs;
    return true;
}
bool ak820_flash_program_page(uint16_t address, const uint8_t *data) {
    unsigned i;
    assert(!(address & 63));
    for (i = 0; i != 64; ++i) {
        if (!ak820_flash_program(address + i, data[i])) return false;
    }
    return true;
}
uint32_t timer_read32(void) { return 0; }
uint32_t via_get_layout_options(void) { return 0; }
void via_init_kb(void) {}
void via_set_layout_options_kb(uint32_t value) { (void)value; }
void via_set_layout_options(uint32_t value) { (void)value; }
matrix_row_t matrix_get_row(uint8_t row) { (void)row; return 0; }
void raw_hid_receive_kb(uint8_t *data, uint8_t length) { (void)length; data[0] = 255; }
uint16_t keycode_at_keymap_location_raw(uint8_t layer, uint8_t row, uint8_t col) {
    (void)row; (void)col;
    return layer < 2 ? (uint16_t)(4 + layer) : 1;
}
uint8_t dynamic_keymap_macro_get_count(void) { return 16; }
uint16_t dynamic_keymap_macro_get_buffer_size(void) { return DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE; }
bool dynamic_keymap_macro_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) { return ak820_macro_write(offset, size, data); }
void dynamic_keymap_macro_reset(void) { assert(!"macro reset is outside this test"); }
uint8_t dynamic_keymap_get_layer_count(void) { return DYNAMIC_KEYMAP_LAYER_COUNT; }
void raw_hid_send(uint8_t *data, uint8_t length) {
    (void)data; assert(length == 32);
    ak820_nvm_flush();
    assert(ak820_nvm_ok());
    ++replies;
}
void wait_ms(uint16_t delay) { (void)delay; }
void bootloader_jump(void) { assert(!"a loader operation must never be executed by this test"); }
void vial_handle_cmd(uint8_t *data, uint8_t length) { (void)data; (void)length; }

/* AK820_ACTUAL_SOURCE */

static void command(uint8_t *packet) {
    ak820_nvm_begin();
    raw_hid_receive(packet, 32);
    ak820_nvm_end();
    assert(ak820_nvm_ok());
}
static void set_one(uint8_t *packet, uint8_t layer, uint8_t row, uint8_t col, uint16_t code) {
    memset(packet, 0, 32);
    packet[0] = id_dynamic_keymap_set_keycode;
    packet[1] = layer; packet[2] = row; packet[3] = col;
    packet[4] = code >> 8; packet[5] = code;
    command(packet);
}
static void set_bulk(uint8_t *packet, uint16_t code) {
    memset(packet, 0, 32);
    packet[0] = id_dynamic_keymap_set_buffer;
    packet[2] = 2; packet[3] = 2; /* offset 2, size 2 */
    packet[4] = code >> 8; packet[5] = code;
    command(packet);
}
int main(void) {
    uint8_t packet[32];
    memset(flash_image, 0, sizeof(flash_image));
    eeprom_driver_init();
    assert(ak820_nvm_ok());
    set_one(packet, 0, 0, 0, 4);
    assert(packet[0] == id_dynamic_keymap_set_keycode && dynamic_keymap_get_keycode(0, 0, 0) == 4);
    unsigned mutations = erases + programs;
    set_one(packet, 0, 0, 0, QK_BOOT);
    assert(packet[0] == id_unhandled);
    assert(dynamic_keymap_get_keycode(0, 0, 0) == 4 && erases + programs == mutations);

    vial_unlocked = 1;
    set_one(packet, 0, 0, 0, QK_BOOT);
    assert(packet[0] == id_dynamic_keymap_set_keycode && dynamic_keymap_get_keycode(0, 0, 0) == QK_BOOT);
    vial_unlocked = 0;
    set_one(packet, 0, 0, 0, 5);
    assert(dynamic_keymap_get_keycode(0, 0, 0) == 5); /* ordinary editing remains available */
    set_bulk(packet, QK_BOOT);
    assert(dynamic_keymap_get_keycode(0, 0, 1) == 0xFFFF);
    vial_unlocked = 1;
    set_bulk(packet, QK_BOOT);
    assert(dynamic_keymap_get_keycode(0, 0, 1) == QK_BOOT);

    mutations = erases + programs;
    set_one(packet, DYNAMIC_KEYMAP_LAYER_COUNT, 0, 0, 6);
    set_one(packet, 0, MATRIX_ROWS, 0, 6);
    set_one(packet, 0, 0, MATRIX_COLS, 6);
    assert(erases + programs == mutations);
    unsigned before = replies;
    raw_hid_receive(packet, 31);
    assert(replies == before && erases + programs == mutations);
    /* Cross a page boundary and the last keymap byte through the production
     * bulk routines. An unchanged block must incur no flash mutations. */
    uint8_t block[28], result[28];
    memset(block, 0x55, sizeof(block));
    dynamic_keymap_set_buffer(62, sizeof(block), block);
    memset(result, 0xA5, sizeof(result));
    dynamic_keymap_get_buffer(62, sizeof(result), result);
    assert(!memcmp(result, block, sizeof(block)));
    mutations = erases + programs;
    dynamic_keymap_set_buffer(62, sizeof(block), block);
    assert(erases + programs == mutations);
    set_one(packet, 5, 15, 7, 0x0405);
    dynamic_keymap_get_buffer(1534, sizeof(result), result);
    assert(result[0] == 4 && result[1] == 5);
    for (unsigned i = 2; i < sizeof(result); ++i) assert(result[i] == 0);
    dynamic_keymap_get_buffer(65535, sizeof(result), result);
    for (unsigned i = 0; i < sizeof(result); ++i) assert(result[i] == 0);
    mutations = erases + programs;
    dynamic_keymap_set_buffer(1535, 2, block);
    dynamic_keymap_set_buffer(65535, 2, block);
    dynamic_keymap_set_buffer(0, 29, block);
    assert(erases + programs == mutations);

    /* No full EEPROM-tail reads: only the committed macro prefix is visible. */
    uint8_t macros[17] = {'X'};
    assert(ak820_macro_write(0, sizeof(macros), macros));
    flash_image[AK820_NVM_BASE + DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + 17] = 0xA5;
    dynamic_keymap_macro_get_buffer(0, sizeof(result), result);
    assert(result[0] == 'X');
    for (unsigned i = 1; i < sizeof(result); ++i) assert(result[i] == 0);
    /* The production reset must cover all six layers with byte-sized indices,
     * use transparent fallback above the two compiled defaults, and relock. */
    vial_unlocked = 0;
    dynamic_keymap_reset();
    assert(!vial_unlocked);
    for (uint8_t layer = 0; layer < 6; ++layer)
        for (uint8_t row = 0; row < 16; ++row)
            for (uint8_t col = 0; col < 8; ++col)
                assert(dynamic_keymap_get_keycode(layer, row, col) == (layer < 2 ? 4 + layer : 1));
    /* The real VIA startup must never replace a legacy/unknown schema with
     * defaults. Read-only EEPROM/FD00 diagnosis remains possible afterwards. */
    static uint8_t saved[65536];
    const uint32_t schemas[] = {BUILD_ID, 0x082001, 0xFFFFFF};
    for (unsigned i = 0; i < sizeof(schemas) / sizeof(schemas[0]); ++i) {
        for (unsigned j = 0; j < 3; ++j)
            flash_image[AK820_NVM_BASE + 37 + j] = schemas[i] >> (8 * j);
        eeprom_driver_init();
        memcpy(saved, flash_image, sizeof(saved));
        mutations = erases + programs;
        via_init();
        assert(ak820_nvm_ok() == (schemas[i] == BUILD_ID));
        uint8_t diagnostic[7];
        ak820_nvm_diagnostic(diagnostic);
        assert(diagnostic[6] == (schemas[i] == BUILD_ID ? 0 : AK820_NVM_FAULT_SCHEMA));
        if (schemas[i] != BUILD_ID) {
            dynamic_keymap_set_keycode(0, 0, 0, 10);
        }
        assert(!memcmp(saved, flash_image, sizeof(saved)) && erases + programs == mutations);
        assert(eeprom_read_byte((const uint8_t *)37) == (uint8_t)schemas[i]);
    }
    puts("PASS: real VIA/NVM: locked boot firewall, six-layer reset, page-crossing bulk reads/writes, unchanged-write wear avoidance, overflow rejection, macro boundary and schema fault without writes.");
    return 0;
}
