// SPDX-License-Identifier: GPL-2.0-or-later
#include "ak820_settings.h"
#include "ak820_crc.h"
#ifdef AK820_COMPACT_AUTOSHIFT
void ak820_autoshift_configure(uint8_t flags);
#endif
#ifdef CAPS_WORD_ENABLE
void ak820_caps_word_configure(uint8_t ru);
#endif

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
    0x51, 0x53, 0x2, 0xf, 0x7f, 0x0, 0x28, 0x0, 0xc8, 0x0, 0x0, 0x0, 0x50, 0x0, 0xaf, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x8e, 0x61
};
static void defaults(void) {
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) candidate[i] = default_record[i];
}
static uint8_t field_width(uint8_t pos) { return pos == 5 || (pos & 0xFEu) == 16 ? 1 : 2; }
/* The stored record and a typed Set use the same field bounds. */
#ifdef __SDCC_mcs51
#    define SETTINGS_BOOL __bit
#else
#    define SETTINGS_BOOL bool
#endif
static SETTINGS_BOOL field_valid(uint8_t pos, const uint8_t AK820_XDATA *in) {
    uint16_t value;
    if (pos == 5) return !(in[0] & 0xF0u);
    if (pos == 16) return !(in[0] & ~0x1Du);
    if (pos == 17) return in[0] <= 1;
    value = word(in);
    if (pos == 18) return value <= 30000;
    if (pos == 10 || pos == 12) return value <= 100;
    return value && value <= 1000;
}
static SETTINGS_BOOL valid(void) {
    uint8_t i;
    if (candidate[0] != 'Q' || candidate[1] != 'S') return false;
    if (candidate[2] == 1) {
        if (candidate[3] != 11 || candidate[4] != 0x3F) return false;
        for (i = 16; i < 22; ++i) if (candidate[i]) return false;
    } else {
        if (candidate[2] != AK820_SETTINGS_VERSION || candidate[3] != 15 || candidate[4] != AK820_SETTINGS_CAPABILITIES) return false;
        if (candidate[20] || candidate[21]) return false;
    }
    for (i = 5; i < 20; i += field_width(i))
        if (!field_valid(i, candidate + i)) return false;
    return word(candidate + 22) == checksum();
}
/* Controls remain volatile when changed by a key. Explicit settings writes
 * and startup apply the saved selection, after successful validation/storage. */
static void apply_controls(uint8_t id) {
#ifdef AK820_COMPACT_AUTOSHIFT
    if (!id || id == 3) ak820_autoshift_configure(current[16]);
#endif
#ifdef CAPS_WORD_ENABLE
    if (!id || id == 22) ak820_caps_word_configure(current[17]);
#endif
    (void)id;
}
/* A settings change cancels all pending/active owners before persistence.
 * clear_keyboard's board cancellation blocks still-held physical sources.
 * Never publish candidate RAM after a storage fault. No retry or rollback. */
static void publish(void) {
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) current[i] = candidate[i];
}
static int8_t commit(void) {
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
    uint8_t any = 0, all = 0xFF;
    ak820_eeprom_read_block_xdata(candidate, (const void *)AK820_SETTINGS_ADDR, sizeof(candidate));
    if (!valid()) {
        /* Schema migration constructs a valid record. A corrupt or
         * unknown record never silently writes defaults over saved data. */
        for (i = 0; i < sizeof(candidate); ++i) {
            any |= candidate[i];
            all &= candidate[i];
        }
        if (any && all != 0xFF) ak820_nvm_schema_fault();
        defaults();
    }
    /* Upgrade a validated v1 record in RAM. Startup does not write flash;
     * the first changed setting commits the v2 record atomically. */
    if (candidate[2] == 1) {
        candidate[2] = AK820_SETTINGS_VERSION;
        candidate[3] = 15;
        candidate[4] = AK820_SETTINGS_CAPABILITIES;
        candidate[16] = 1;
        seal();
    }
    publish();
    apply_controls(0);
}
#ifdef __SDCC_mcs51
#    define SETTINGS_CODE __code
#else
#    define SETTINGS_CODE
#endif
/* Direct QSID indexing avoids two tables and a linear search per Get/Set.
 * A zero position is unavailable; all actual fields start at byte five. */
static const SETTINGS_CODE uint8_t positions[23] = {0, 5, 6,
#ifdef AK820_COMPACT_AUTOSHIFT
    16, 14,
#else
    0, 0,
#endif
    0,
#ifdef AK820_COMPACT_ONESHOT
    18,
#else
    0,
#endif
    8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 12, 0, 0, 17};
#ifdef __SDCC_mcs51
/* Vial admits only its fixed 32-byte raw packet before reaching these calls.
 * Keep its wire offsets here so pointer/capacity argument setup disappears. */
extern __xdata uint8_t raw_buffer[32];
void ak820_settings_query_packet(void) {
    uint16_t greater_than = word(raw_buffer + 2);
#    define buffer raw_buffer
#    define size 32u
#else
void ak820_settings_query(uint16_t greater_than, uint8_t AK820_XDATA *buffer, uint8_t size) {
#endif
    uint8_t i, used = 0;
    for (i = 0; i < size; ++i) buffer[i] = 0xFF;
    if (greater_than >= 22) return;
    for (i = (uint8_t)greater_than + 1; i < sizeof(positions)
#ifndef __SDCC_mcs51
         && used + 2 <= size
#endif
         ; ++i) {
        if (positions[i]) { buffer[used++] = i; buffer[used++] = 0; }
    }
}
#ifdef __SDCC_mcs51
#    undef buffer
#    undef size
int ak820_settings_get_packet(void) {
    uint16_t id = word(raw_buffer + 2);
#    define buffer (raw_buffer + 1)
#    define capacity 31u
#else
int ak820_settings_get(uint16_t id, uint8_t AK820_XDATA *buffer, uint8_t capacity) {
#endif
    uint8_t AK820_XDATA *out = buffer;
    uint8_t pos, width;
    if (id >= sizeof(positions)) return -1;
    pos = positions[(uint8_t)id];
    width = field_width(pos);
    if (!pos || capacity < width) return -1;
    out[0] = current[pos];
    if (width == 2) out[1] = current[pos + 1];
    return 0;
}
#ifdef __SDCC_mcs51
#    undef buffer
#    undef capacity
int ak820_settings_set_packet(void) {
    uint16_t id = word(raw_buffer + 2);
#    define buffer (raw_buffer + 4)
#    define capacity 28u
#else
int ak820_settings_set(uint16_t id, const uint8_t AK820_XDATA *buffer, uint8_t capacity) {
#endif
    const uint8_t AK820_XDATA *in = buffer;
    uint8_t pos, width;
    if (id >= sizeof(positions)) return -1;
    pos = positions[(uint8_t)id];
    width = field_width(pos);
    if (!pos || capacity < width || !ak820_nvm_ok()) return -1;
    /* current is validated at initialization and every published change keeps
     * its schema intact. Check only this incoming field before sealing once. */
    if (!field_valid(pos, in)) return -1;
    for (uint8_t i = 0; i < AK820_SETTINGS_SIZE; ++i) candidate[i] = current[i];
    candidate[pos] = in[0];
    if (width == 2) candidate[pos + 1] = in[1];
    seal();
    if (commit()) return -1;
    apply_controls((uint8_t)id);
    return 0;
}
#ifdef __SDCC_mcs51
#    undef buffer
#    undef capacity
#endif
int ak820_settings_reset(void) {
    defaults();
    if (commit()) return -1;
    apply_controls(0);
    return 0;
}
uint8_t ak820_settings_grave_esc(void) { return current[5]; }
uint16_t ak820_settings_combo_term(void) { return word(current + 6); }
uint16_t ak820_settings_tapping_term(void) { return word(current + 8); }
uint16_t ak820_settings_tap_code_delay(void) { return word(current + 10); }
uint16_t ak820_settings_caps_delay(void) { return word(current + 12); }
uint16_t ak820_settings_autoshift_timeout(void) { return word(current + 14); }
uint8_t ak820_settings_autoshift_flags(void) { return current[16]; }
uint8_t ak820_settings_caps_word_language(void) { return current[17]; }
uint16_t ak820_settings_oneshot_timeout(void) { return word(current + 18); }
