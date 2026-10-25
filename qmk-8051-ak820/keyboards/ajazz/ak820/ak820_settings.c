// SPDX-License-Identifier: GPL-2.0-or-later
#include "ak820_settings.h"
#include "ak820_crc.h"

/* Keep the record on one 64-byte journal page. No generic QMK Settings struct
 * or callback table is used; enabling that implementation moves Combo data. */
_Static_assert((AK820_SETTINGS_ADDR & 63u) + AK820_SETTINGS_SIZE <= 64u, "settings page crossing");
_Static_assert(AK820_SETTINGS_ADDR == 0x6A8u, "settings ABI address");
static uint8_t AK820_XDATA current[AK820_SETTINGS_SIZE];
static uint8_t AK820_XDATA candidate[AK820_SETTINGS_SIZE];
extern void clear_keyboard(void);

#if defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
/* XDATA pointer in DPTR, little-endian word returned in DPTR. R0-R7
 * remain unchanged; only A/B/DPTR and accumulator parity are scratch. */
static uint16_t word(const uint8_t AK820_XDATA *p) __naked {
    p;
    __asm
        movx a,@dptr
        mov b,a
        inc dptr
        movx a,@dptr
        mov dph,a
        mov dpl,b
        ret
    __endasm;
}
#else
static uint16_t word(const uint8_t AK820_XDATA *p) {
    return (uint16_t)p[0] | ((uint16_t)p[1] << 8);
}
#endif
static void put_word(uint8_t AK820_XDATA *p, uint16_t v) { p[0] = v; p[1] = v >> 8; }
static uint16_t checksum(void) { return ak820_crc16(candidate, 22); }
static void seal(void) { put_word(candidate + 22, checksum()); }
#ifdef __SDCC_mcs51
static const __code uint8_t default_record[AK820_SETTINGS_SIZE] = {
#else
static const uint8_t default_record[AK820_SETTINGS_SIZE] = {
#endif
    0x51, 0x53, 0x1, 0xb, 0x3f, 0x0, 0x28, 0x0, 0xc8, 0x0, 0x0, 0x0, 0x50, 0x0, 0xaf, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x7b, 0xc9
};
static void defaults(void) {
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) candidate[i] = default_record[i];
}
static bool valid(void) {
    uint8_t i;
    uint16_t value;
    if (candidate[0] != 'Q' || candidate[1] != 'S' || candidate[2] != AK820_SETTINGS_VERSION || candidate[3] != 11 || candidate[4] != AK820_SETTINGS_CAPABILITIES) return false;
    if (candidate[5] & 0xF0u) return false;
    for (i = 6; i <= 14; i += 2) {
        value = word(candidate + i);
        if (i == 10 || i == 12) { if (value > 100) return false; }
        else if (!value || value > 1000) return false;
    }
    for (i = 16; i < 22; ++i) if (candidate[i]) return false;
    return word(candidate + 22) == checksum();
}
/* A settings change cancels all pending/active owners before persistence.
 * clear_keyboard's board cancellation blocks still-held physical sources.
 * Never publish candidate RAM after a storage fault. No retry or rollback. */
static void publish(void) {
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) current[i] = candidate[i];
}
static int commit(void) {
    uint8_t i;
    if (!ak820_nvm_ok()) return -1;
    for (i = 0; i < AK820_SETTINGS_SIZE; ++i) if (current[i] != candidate[i]) break;
    if (i == AK820_SETTINGS_SIZE) return 0;
    clear_keyboard();
    ak820_nvm_begin();
    ak820_eeprom_update_block_xdata(candidate, (void *)AK820_SETTINGS_ADDR, sizeof(candidate));
    ak820_nvm_end();
    if (!ak820_nvm_ok()) return -1;
    publish();
    return 0;
}
void ak820_settings_init(void) {
    uint8_t i;
    bool blank_zero = true, blank_erased = true;
    ak820_eeprom_read_block_xdata(candidate, (const void *)AK820_SETTINGS_ADDR, sizeof(candidate));
    if (!valid()) {
        /* Schema migration constructs a valid record. A corrupt or
         * unknown record never silently writes defaults over saved data. */
        for (i = 0; i < sizeof(candidate); ++i) {
            if (candidate[i]) blank_zero = false;
            if (candidate[i] != 0xFF) blank_erased = false;
        }
        if (!blank_zero && !blank_erased) ak820_nvm_schema_fault();
        defaults();
    }
    publish();
}
#ifdef __SDCC_mcs51
#    define SETTINGS_CODE __code
#else
#    define SETTINGS_CODE
#endif
static const SETTINGS_CODE uint8_t ids[] = {1, 2,
#ifdef AK820_COMPACT_AUTOSHIFT
    4,
#endif
    7, 18, 19};
static const SETTINGS_CODE uint8_t positions[] = {5, 6,
#ifdef AK820_COMPACT_AUTOSHIFT
    14,
#endif
    8, 10, 12};
static uint8_t offset(uint8_t id) {
    for (uint8_t i = 0; i < sizeof(ids); ++i) if (ids[i] == id) return positions[i];
    return 0;
}
void ak820_settings_query(uint16_t greater_than, uint8_t AK820_XDATA *buffer, uint8_t size) {
    uint8_t i, used = 0;
    for (i = 0; i < size; ++i) buffer[i] = 0xFF;
    if (greater_than >= 19) return;
    for (i = 0; i < sizeof(ids) && used + 2 <= size; ++i) {
        if (ids[i] > (uint8_t)greater_than) { buffer[used++] = ids[i]; buffer[used++] = 0; }
    }
}
int ak820_settings_get(uint16_t id, uint8_t AK820_XDATA *buffer, uint8_t capacity) {
    uint8_t AK820_XDATA *out = buffer;
    uint8_t pos, width = id == 1 ? 1 : 2;
    if (id > 255) return -1;
    pos = offset((uint8_t)id);
    if (!pos || capacity < width) return -1;
    out[0] = current[pos];
    if (width == 2) out[1] = current[pos + 1];
    return 0;
}
int ak820_settings_set(uint16_t id, const uint8_t AK820_XDATA *buffer, uint8_t capacity) {
    const uint8_t AK820_XDATA *in = buffer;
    uint8_t pos, width = id == 1 ? 1 : 2;
    if (id > 255) return -1;
    pos = offset((uint8_t)id);
    if (!pos || capacity < width || !ak820_nvm_ok()) return -1;
    /* current is validated at initialization and every published change keeps
     * its schema intact. Check only this incoming field before sealing once. */
    if (pos == 5) {
        if (in[0] & 0xF0u) return -1;
    } else {
        uint16_t value = word(in);
        if (pos == 10 || pos == 12) { if (value > 100) return -1; }
        else if (!value || value > 1000) return -1;
    }
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) candidate[i] = current[i];
    candidate[pos] = in[0];
    if (width == 2) candidate[pos + 1] = in[1];
    seal();
    return commit();
}
int ak820_settings_reset(void) { defaults(); return commit(); }
uint8_t ak820_settings_grave_esc(void) { return current[5]; }
uint16_t ak820_settings_combo_term(void) { return word(current + 6); }
uint16_t ak820_settings_tapping_term(void) { return word(current + 8); }
uint16_t ak820_settings_tap_code_delay(void) { return word(current + 10); }
uint16_t ak820_settings_caps_delay(void) { return word(current + 12); }
uint16_t ak820_settings_autoshift_timeout(void) { return word(current + 14); }
