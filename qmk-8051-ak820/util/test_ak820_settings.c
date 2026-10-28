// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only behavioral checks. Compile with the board directory on -I. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_settings.h"
#include "ak820_crc.h"
static unsigned writes, clears;
static uint8_t applied_as, applied_language;
void ak820_autoshift_configure(uint8_t flags) { applied_as = flags; }
void ak820_caps_word_configure(uint8_t ru) { applied_language = ru; }
static bool healthy = true, fail_write;
static uint8_t storage[AK820_NVM_SIZE];
bool ak820_nvm_ok(void) { return healthy; }
void ak820_nvm_schema_fault(void) { healthy = false; }
void ak820_nvm_begin(void) {}
void ak820_nvm_end(void) {}
void clear_keyboard(void) { ++clears; }
void ak820_eeprom_read_block_xdata(void *out, const void *addr, size_t n) { memcpy(out, storage + (size_t)addr, n); }
void ak820_eeprom_update_block_xdata(const void *in, void *addr, size_t n) {
    assert((size_t)addr == AK820_SETTINGS_ADDR && n == AK820_SETTINGS_SIZE);
    ++writes;
    if (fail_write) { healthy = false; return; }
    memcpy(storage + (size_t)addr, in, n);
}
int main(void) {
    uint8_t out[24], v[2], good[AK820_SETTINGS_SIZE];
    unsigned i;
    memset(storage, 0xA5, sizeof(storage));
    memset(storage + AK820_SETTINGS_ADDR, 0, AK820_SETTINGS_SIZE);
    ak820_settings_init();
    assert(healthy && !writes && ak820_settings_combo_term() == 40);
    assert(ak820_settings_tapping_term() == 200 && ak820_settings_caps_delay() == 80);
    assert(ak820_settings_tap_code_delay() == 0 && ak820_settings_autoshift_timeout() == 175);
    assert(ak820_settings_autoshift_flags() == 1 && ak820_settings_caps_word_language() == 1);
    assert(ak820_settings_oneshot_timeout() == 0 && applied_language == 1);
    ak820_settings_query(1, out, sizeof(out));
    {
        static const uint8_t expected[] = {2,
#ifdef AK820_COMPACT_AUTOSHIFT
            3, 4,
#endif
#ifdef AK820_COMPACT_ONESHOT
            6,
#endif
            7, 18, 19, 22};
        for (i = 0; i < sizeof(expected); ++i) assert(out[i * 2] == expected[i] && out[i * 2 + 1] == 0);
        for (i = sizeof(expected) * 2; i < sizeof(out); ++i) assert(out[i] == 255);
    }
#ifndef AK820_COMPACT_AUTOSHIFT
    assert(ak820_settings_get(3, out, sizeof(out)) == -1);
    assert(ak820_settings_get(4, out, sizeof(out)) == -1);
#else
    assert(applied_as == 1);
#endif
#ifndef AK820_COMPACT_ONESHOT
    assert(ak820_settings_get(6, out, sizeof(out)) == -1);
#endif
    assert(ak820_settings_get(2, out, 1) == -1);
    assert(ak820_settings_get(257, out, 2) == -1);
    assert(ak820_settings_set(257, out, 2) == -1);
    ak820_settings_query(65535, out, sizeof(out));
    for (i = 0; i < sizeof(out); ++i) assert(out[i] == 255);
    ak820_settings_query(0, out, 3);
    assert(out[0] == 1 && out[1] == 0 && out[2] == 255);
    v[0] = 0; v[1] = 0;
    assert(ak820_settings_set(2, v, 2) == -1 && !writes);
    v[0] = 16; assert(ak820_settings_set(1, v, 2) == -1);
    v[0] = 101; assert(ak820_settings_set(18, v, 2) == -1);
    /* A truncated two-byte Set must preserve both storage and runtime state. */
    v[0] = 55; v[1] = 0;
    assert(ak820_settings_set(2, v, 1) == -1);
    assert(!writes && !clears && ak820_settings_combo_term() == 40);
    v[0] = 40; assert(!ak820_settings_set(2, v, 2) && !writes && !clears);
    v[0] = 55; assert(!ak820_settings_set(2, v, 2) && writes == 1 && clears == 1);
    assert(storage[AK820_SETTINGS_ADDR - 1] == 0xA5 && storage[AK820_SETTINGS_ADDR + AK820_SETTINGS_SIZE] == 0xA5);
    ak820_settings_init(); assert(ak820_settings_combo_term() == 55 && healthy);
    /* Exhaust incoming values; accepted fields must pass startup validation.
     * Invalid values must not cancel owners or enter persistence. */
    {
        static const uint8_t ids[] = {1, 2, 7, 18, 19, 22,
#ifdef AK820_COMPACT_AUTOSHIFT
            3, 4,
#endif
#ifdef AK820_COMPACT_ONESHOT
            6,
#endif
        };
        unsigned field;
        for (field = 0; field < sizeof(ids); ++field) {
            unsigned long value;
            for (value = 0; value <= 65535; ++value) {
                unsigned before_writes = writes, before_clears = clears;
                bool accepted = ids[field] == 1 ? (value & 255) < 16 :
                    ids[field] == 3 ? !((value & 255) & ~0x1D) :
                    ids[field] == 22 ? (value & 255) <= 1 :
                    ids[field] == 6 ? value <= 30000 :
                    (ids[field] == 18 || ids[field] == 19) ? value <= 100 :
                    value >= 1 && value <= 1000;
                v[0] = value; v[1] = value >> 8;
                assert(ak820_settings_set(ids[field], v, 2) == (accepted ? 0 : -1));
                if (!accepted) {
                    assert(writes == before_writes && clears == before_clears);
                } else {
                    assert(!ak820_settings_get(ids[field], out, sizeof(out)));
                    assert(out[0] == v[0] && (ids[field] == 1 || ids[field] == 3 || ids[field] == 22 || out[1] == v[1]));
                    ak820_settings_init();
                    assert(healthy);
                }
            }
        }
    }
    v[0] = 55; v[1] = 0;
    assert(!ak820_settings_set(2, v, 2));
    fail_write = true; v[0] = 56;
    assert(ak820_settings_set(2, v, 2) == -1 && ak820_settings_combo_term() == 55);
    assert(ak820_settings_reset() == -1);
    fail_write = false; healthy = true;
    memcpy(good, storage + AK820_SETTINGS_ADDR, sizeof(good));
    /* Every single-byte tear/corruption is rejected as a whole on reboot. */
    for (i = 0; i < sizeof(good); ++i) {
        memcpy(storage + AK820_SETTINGS_ADDR, good, sizeof(good));
        storage[AK820_SETTINGS_ADDR + i] ^= 1;
        healthy = true;
        ak820_settings_init();
        assert(!healthy && ak820_settings_combo_term() == 40);
    }
    memset(storage + AK820_SETTINGS_ADDR, 255, AK820_SETTINGS_SIZE);
    healthy = true; ak820_settings_init();
    assert(healthy && ak820_settings_combo_term() == 40);
    /* Validate old persisted records before upgrading in RAM. The first changed
     * setting emits v2; a read or unchanged write never touches old bytes. */
    {
        static const uint8_t legacy[] = {0x51,0x53,1,11,0x3f,0,40,0,200,0,0,0,80,0,175,0,0,0,0,0,0,0,0x7b,0xc9};
        unsigned before = writes;
        memcpy(storage + AK820_SETTINGS_ADDR, legacy, sizeof(legacy));
        healthy = true; ak820_settings_init();
        assert(healthy && writes == before && ak820_settings_autoshift_flags() == 1);
        assert(applied_language == 0 && ak820_settings_oneshot_timeout() == 0);
        v[0] = 0; v[1] = 0;
        assert(!ak820_settings_set(22, v, 1) && writes == before);
        assert(!memcmp(storage + AK820_SETTINGS_ADDR, legacy, sizeof(legacy)));
        v[0] = 1;
        assert(!ak820_settings_set(22, v, 1) && writes == before + 1);
        assert(storage[AK820_SETTINGS_ADDR + 2] == 2 && applied_language == 1);
        ak820_settings_init(); assert(healthy && applied_language == 1);
        /* Reserved legacy bytes with a valid CRC are not a future record. */
        memcpy(good, legacy, sizeof(good)); good[16] = 1;
        unsigned crc = ak820_crc16(good, 22); good[22] = crc; good[23] = crc >> 8;
        memcpy(storage + AK820_SETTINGS_ADDR, good, sizeof(good));
        healthy = true; ak820_settings_init(); assert(!healthy && applied_language == 1);
    }
    puts("AK820 settings host model PASS");
}
