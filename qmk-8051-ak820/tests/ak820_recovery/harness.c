/* Recovery regression: production transport + verbatim request handlers.
 * Only hardware, NVM storage and unrelated feature accessors are stubs.
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "keyboards/ajazz/ak820/config.h"
#include "ak820_usb_test_shim.h"
#include "dynamic_keymap.h"
#include "matrix.h"
#include "action_layer.h"
#include "keymap_common.h"
#include "quantum_keycodes.h"
#include "timer.h"
#include "vial_generated_keyboard_definition.h"
#include "tmk_core/protocol/ch555/usb_ak820.c"

volatile uint8_t test_mmio[0x2300];
uint8_t test_rom[65536];
volatile uint8_t EA = 1, IE_USB;
volatile uint8_t keyboard_protocol, keyboard_idle;
static bool nvm_good;
uint8_t ak820_flash_diagnostic[6];
static unsigned begins, flushes, ends, writes, boot_calls, scans, ee_disables;
static uint32_t now;
static matrix_row_t matrix_state[MATRIX_ROWS];
static unsigned requests, replies;

void test_ack_transfer(void) { USB_IF &= ~bUX_IF_D0_TRANS; D0_STATUS = UXS_TOKEN_FREE; }
void test_ack_all(void) { USB_IF = 0; D0_STATUS = UXS_TOKEN_FREE; }
uint8_t test_read_code(uint16_t a) { return test_rom[a]; }
void wait_ms(uint16_t value) { now += value; }
void wait_us(uint16_t value) { (void)value; }
uint16_t timer_read(void) { return now; }
uint32_t timer_read32(void) { return now; }
uint16_t timer_elapsed(uint16_t since) { return now - since; }
uint32_t timer_elapsed32(uint32_t since) { return now - since; }
matrix_row_t matrix_get_row(uint8_t row) { assert(row < MATRIX_ROWS); return matrix_state[row]; }
bool matrix_is_on(uint8_t row, uint8_t col) { return (matrix_get_row(row) & (1u << col)) != 0; }
uint16_t read_source_keycode_cache(keypos_t key) { (void)key; return KC_NO; }
void layer_off(uint8_t layer) { (void)layer; }
void clear_keyboard(void) {}
uint8_t matrix_scan(void) { ++scans; return 0; }
bool ak820_nvm_ok(void) { return nvm_good; }
void ak820_nvm_begin(void) { ++begins; }
void ak820_nvm_flush(void) { ++flushes; }
void ak820_nvm_end(void) { ++ends; }
void ak820_nvm_diagnostic(uint8_t *out) { memset(out, 0, 7); out[0] = !nvm_good; }
void bootloader_jump(void) { ++boot_calls; }
void eeconfig_disable(void) { ++ee_disables; }
void raw_hid_send(uint8_t *data, uint8_t length) { ak820_usb_raw_send(data, length); }
uint32_t via_get_layout_options(void) { return 0; }
void via_set_layout_options(uint32_t value) { (void)value; ++writes; }
uint8_t dynamic_keymap_get_layer_count(void) { return 6; }
uint16_t dynamic_keymap_get_keycode(uint8_t l, uint8_t r, uint8_t c) { (void)l; (void)r; (void)c; return 4; }
void dynamic_keymap_set_keycode(uint8_t l, uint8_t r, uint8_t c, uint16_t k) { (void)l; (void)r; (void)c; (void)k; ++writes; }
void dynamic_keymap_reset(void) { ++writes; }
void dynamic_keymap_get_buffer(uint16_t o, uint16_t n, uint8_t *p) { (void)o; memset(p, 0, n); }
void dynamic_keymap_set_buffer(uint16_t o, uint16_t n, uint8_t *p) { (void)o; (void)n; (void)p; ++writes; }
uint8_t dynamic_keymap_macro_get_count(void) { return 16; }
uint16_t dynamic_keymap_macro_get_buffer_size(void) { return 8192; }
void dynamic_keymap_macro_get_buffer(uint16_t o, uint16_t n, uint8_t *p) { (void)o; memset(p, 0, n); }
bool dynamic_keymap_macro_set_buffer(uint16_t o, uint16_t n, uint8_t *p) { (void)o; (void)n; (void)p; ++writes; return nvm_good; }
void dynamic_keymap_macro_reset(void) { ++writes; }
/* Storage only is stubbed; encoder address calculation/get/set are extracted
 * production bodies alongside the real VIA/Vial request handlers. */
static uint8_t encoder_eeprom[EEPROM_SIZE];
uint8_t eeprom_read_byte(const uint8_t *p) {
    uintptr_t address = (uintptr_t)p;
    assert(address < sizeof(encoder_eeprom));
    return encoder_eeprom[address];
}
void eeprom_update_byte(uint8_t *p, uint8_t value) {
    uintptr_t address = (uintptr_t)p;
    assert(address < sizeof(encoder_eeprom));
    ++writes;
    if (nvm_good) encoder_eeprom[address] = value;
}
void vialrgb_get_value(uint8_t *data, uint8_t length) { (void)length; data[2] = 1; }
void vialrgb_set_value(uint8_t *data, uint8_t length) { (void)data; (void)length; ++writes; }
void vialrgb_save(uint8_t *data, uint8_t length) { (void)data; (void)length; ++writes; }

#include "recovery-handler-fragments.inc"

/* Inject at the existing completed-Raw handoff; SIE dispatch is separately
 * exercised by tests/ak820_usb. Replies use the real endpoint publisher. */
static bool packet_request(const uint8_t packet[32], uint8_t *response) {
    assert(raw_state == RAW_IDLE);
    memcpy(raw_buffer, packet, sizeof(raw_buffer));
    raw_state = RAW_READY;
    ++requests;
    ak820_usb_raw_task();
    assert(!raw_reply_without_nvm);
    bool replied = raw_state == RAW_TX_WAIT;
    if (replied) {
        ++replies;
        assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_ACK && D0_EP3T_L == 32);
        memcpy(response, (const void *)(pUSB_BUF_DEV0 + UX_EP3_ADDR), 32);
        D0_STATUS = UXS_TOKEN_IN | 3; USB_IF |= bUX_IF_D0_TRANS;
        USB_DeviceInterrupt();
    } else {
        assert(raw_state == RAW_IDLE);
        assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK);
    }
    assert(raw_state == RAW_IDLE);
    return replied;
}

static bool request(uint8_t command, uint8_t sub, uint8_t arg, uint8_t *response) {
    uint8_t packet[32] = {command, sub, arg};
    return packet_request(packet, response);
}

static void test_encoder_write_packets(void) {
    uint8_t response[32], packet[32], snapshot[EEPROM_SIZE];
    vial_unlocked = vial_unlock_in_progress = false;
    nvm_good = true;
    memset(encoder_eeprom, 0xa5, sizeof(encoder_eeprom));
    for (unsigned layer=0; layer<DYNAMIC_KEYMAP_LAYER_COUNT; ++layer) {
        for (unsigned direction=0; direction<2; ++direction) {
            uint16_t code = 0x0404 + layer*16 + direction;
            memset(packet,0,sizeof(packet));
            packet[0]=0xfe; packet[1]=4; packet[2]=layer; packet[3]=0;
            packet[4]=direction; packet[5]=code>>8; packet[6]=code;
            assert(packet_request(packet,response));
            assert(!memcmp(packet,response,32)); /* Standard Vial echo ACK. */
            uint16_t address=0x640+layer*4+(direction?0:2);
            assert(encoder_eeprom[address]==(code>>8) && encoder_eeprom[address+1]==(code&255));
            packet[1]=3;
            assert(packet_request(packet,response));
            assert(response[direction*2]==(code>>8) && response[direction*2+1]==(code&255));
        }
    }
    memcpy(snapshot,encoder_eeprom,sizeof(snapshot));
    nvm_good=false; /* Latched storage fault: reads remain available. */
    for (unsigned layer=0; layer<DYNAMIC_KEYMAP_LAYER_COUNT; ++layer) {
        for (unsigned direction=0; direction<2; ++direction) {
            memset(packet,0,sizeof(packet));
            packet[0]=0xfe; packet[1]=4; packet[2]=layer; packet[4]=direction;
            packet[5]=0x12; packet[6]=0x34;
            assert(!packet_request(packet,response)); /* No false success. */
            assert(!memcmp(snapshot,encoder_eeprom,sizeof(snapshot)));
            packet[1]=3;
            assert(packet_request(packet,response));
            uint16_t code=0x0404+layer*16+direction;
            assert(response[direction*2]==(code>>8) && response[direction*2+1]==(code&255));
        }
    }
    for(unsigned address=0;address<sizeof(snapshot);++address)
        if(address<0x640 || address>=0x658) assert(snapshot[address]==0xa5);
    puts("PASS: exact web FE04/FE03 packets, 6 layers x 2 directions: persisted big-endian bytes/echo/readback; latched fault rejects writes without false ACK, preserves whole storage and allows reads.");
}

int main(void) {
    uint8_t response[32];
    USB_Device_Init(); endpoints_reset(); USB_EnumStatus = D0UsbConfig = 1;
    assert(!nvm_good && !vial_unlocked && !vial_unlock_in_progress);

    assert(request(id_get_protocol_version, 0, 0, response));
    assert(response[1] == 0 && response[2] == VIA_PROTOCOL_VERSION);
    assert(request(id_vial_prefix, vial_get_keyboard_id, 0, response));
    assert(response[0] == VIAL_PROTOCOL_VERSION && response[12] == 1);
    static const uint8_t uid[] = VIAL_KEYBOARD_UID;
    assert(!memcmp(response + 4, uid, sizeof(uid)));
    assert(request(id_dynamic_keymap_get_layer_count, 0, 0, response));
    assert(response[1] == 6);
    assert(request(id_dynamic_keymap_macro_get_buffer_size, 0, 0, response));
    assert(response[1] == 0x20 && response[2] == 0);
    assert(request(id_vial_prefix, vial_dynamic_entry_op, dynamic_vial_get_number_of_entries, response));
    assert(!response[0] && !response[1] && !response[2] && response[31] == 1);
    assert(request(id_vial_prefix, vial_get_size, 0, response));
    uint32_t size = response[0] | (uint32_t)response[1] << 8 | (uint32_t)response[2] << 16 | (uint32_t)response[3] << 24;
    assert(size == sizeof(keyboard_definition));
    for (unsigned page = 0; page < (size + 31) / 32; ++page) {
        assert(page < 256);
        assert(request(id_vial_prefix, vial_get_def, page, response));
        unsigned n = size - page * 32 < 32 ? size - page * 32 : 32;
        assert(!memcmp(response, keyboard_definition + page * 32, n));
    }
    assert(request(id_vial_prefix, vial_get_unlock_status, 0, response));
    assert(!response[0] && !response[1]);
    assert(response[2] == 0 && response[3] == 0 && response[4] == 0 && response[5] == 5);
    assert(request(id_bootloader_jump, 0, 0, response));
    assert(boot_calls == 0); /* Reply exemption does not authorize the jump. */
    matrix_state[0] = 0x21;
    assert(request(id_get_keyboard_value, id_switch_matrix_state, 0, response));
    assert(response[2] == 0); /* Locked matrix read remains blocked by VIA. */

    assert(request(id_vial_prefix, vial_unlock_start, 0, response));
    assert(vial_unlock_in_progress && !vial_unlocked);
    assert(!request(id_bootloader_jump, 0, 0, response));
    assert(boot_calls == 0);
    matrix_state[0] = 0;
    for (unsigned i = 0; i < 55; ++i) {
        now += 101;
        vial_unlock_task();
        assert(request(id_vial_prefix, vial_unlock_poll, 0, response));
        assert(!response[0] && response[1] && response[2] == 30);
    }
    matrix_state[0] = 1;
    now += 101;
    vial_unlock_task();
    assert(request(id_vial_prefix, vial_unlock_poll, 0, response));
    assert(!response[0] && response[2] == 30);
    matrix_state[0] = 0x21;
    /* Polling never advances time or starts a physical hold. */
    for (unsigned i = 0; i < 50; ++i) {
        now += 101;
        assert(request(id_vial_prefix, vial_unlock_poll, 0, response));
        assert(!response[0] && response[1] && response[2] == 30);
    }
    vial_unlock_task();
    now += 2999; vial_unlock_task();
    assert(!vial_unlocked && vial_unlock_counter == 1);
    /* Release and repress between host polls must reset the entire hold. */
    matrix_state[0] = 1; vial_unlock_task();
    matrix_state[0] = 0x21; vial_unlock_task();
    now += 2; vial_unlock_task();
    assert(request(id_vial_prefix, vial_unlock_poll, 0, response));
    assert(!response[0] && response[1] && response[2] == 30);
    /* A lock request cancels an in-progress hold through the real VIA gate. */
    assert(request(id_vial_prefix, vial_lock, 0, response));
    now += 5000; vial_unlock_task();
    assert(!vial_unlocked && !vial_unlock_in_progress);
    assert(request(id_vial_prefix, vial_unlock_start, 0, response));
    now = UINT32_MAX - 2000;
    vial_unlock_task();
    now += 2999; vial_unlock_task();
    assert(!vial_unlocked && vial_unlock_counter == 1);
    now += 1; vial_unlock_task(); /* 32-bit wrap, no host polls during hold. */
    assert(vial_unlocked && !vial_unlock_in_progress && !nvm_good);
    assert(request(id_vial_prefix, vial_get_unlock_status, 0, response));
    assert(response[0] && !response[1]);
    assert(request(id_get_keyboard_value, id_switch_matrix_state, 0, response));
    assert(response[2] == 0x21);
    assert(request(id_bootloader_jump, 0, 0, response));
    assert(boot_calls == 1 && !nvm_good);

    const uint8_t setters[][3] = {
        {id_set_keyboard_value, id_layout_options, 0},
        {id_dynamic_keymap_set_keycode, 0, 0}, {id_dynamic_keymap_reset, 0, 0},
        {id_lighting_set_value, vialrgb_set_mode, 0}, {id_lighting_save, 0, 0},
        {id_eeprom_reset, 0, 0}, {id_dynamic_keymap_macro_set_buffer, 0, 0},
        {id_dynamic_keymap_macro_reset, 0, 0}, {id_dynamic_keymap_set_buffer, 0, 0},
        {id_vial_prefix, vial_set_encoder, 0}, {id_vial_prefix, vial_qmk_settings_set, 0},
        {id_vial_prefix, vial_qmk_settings_reset, 0},
        {id_vial_prefix, vial_dynamic_entry_op, dynamic_vial_tap_dance_set},
        {id_vial_prefix, vial_dynamic_entry_op, dynamic_vial_combo_set},
        {id_vial_prefix, vial_dynamic_entry_op, dynamic_vial_key_override_set},
    };
    for (unsigned i = 0; i < sizeof(setters) / sizeof(setters[0]); ++i)
        assert(!request(setters[i][0], setters[i][1], setters[i][2], response));
    assert(writes >= 9); /* Real dispatch reached the enabled setter stubs. */
    const uint8_t unknown[][3] = {{0x20,0,0},{0xff,0,0},{0xfd,2,0},
        {id_vial_prefix,0xff,0},{id_vial_prefix,vial_dynamic_entry_op,0xff},
        {id_get_keyboard_value,0xff,0},{id_lighting_get_value,0xff,0}};
    for (unsigned i = 0; i < sizeof(unknown) / sizeof(unknown[0]); ++i)
        assert(!request(unknown[i][0], unknown[i][1], unknown[i][2], response));
    assert(request(id_vial_prefix, vial_lock, 0, response));
    assert(!vial_unlocked);
    assert(request(id_bootloader_jump, 0, 0, response));
    assert(boot_calls == 1);

    unsigned old_begins = begins, old_flushes = flushes, old_ends = ends;
    assert(request(0xfd, 0, 0, response));
    assert(begins == old_begins && flushes == old_flushes && ends == old_ends);
    assert(request(0xfd, 1, 0, response));
    assert(response[0] == 0xfd && response[1] == 1 && response[2] == 1 && response[3] == 0xa8);
    assert(response[4] == 1 && !response[17] && !response[18]);
    assert(begins == old_begins && flushes == old_flushes && ends == old_ends);
    assert(begins == ends);

    matrix_state[0] = 0;
    bootmagic_lite();
    assert(boot_calls == 1 && ee_disables == 0 && scans == 2);
    matrix_state[0] = 1;
    bootmagic_lite();
    assert(boot_calls == 2 && ee_disables == 1 && scans == 4);
    assert(!vial_unlocked && !nvm_good);
    test_encoder_write_packets();
    printf("PASS: %u requests, %u replies; real VIA/Vial discovery, scan-driven 3 s unlock with read-only polls, inter-poll release, cancellation and 32-bit wrap; locked boot/matrix gates, faulted boot dispatch, 15 setters and 7 unknowns gated, FD00/FD01 zero-NVM, locked/faulted Esc bootmagic dispatch.\n", requests, replies);
    return 0;
}
