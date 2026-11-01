// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only behavioral checks. Compile with the board directory on -I. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_settings.h"
#include "ak820_crc.h"
#include "ak820_leader_timeout.h"
static unsigned writes, clears, schema_faults;
static uint8_t applied_as, applied_language;
void ak820_autoshift_configure(uint8_t flags) { applied_as = flags; }
void ak820_caps_word_configure(uint8_t ru) { applied_language = ru; }
static bool healthy = true, fail_write;
static uint8_t storage[AK820_NVM_SIZE];
bool ak820_nvm_ok(void) { return healthy; }
void ak820_nvm_schema_fault(void) { ++schema_faults; healthy = false; }
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
static void assert_defaults(void) {
    assert(ak820_settings_grave_esc() == 0);
    assert(ak820_settings_combo_term() == 40 && ak820_settings_tapping_term() == 200);
    assert(ak820_settings_caps_delay() == 80 && ak820_settings_tap_code_delay() == 0);
    assert(ak820_settings_autoshift_timeout() == 175 && ak820_settings_autoshift_flags() == 1);
    assert(ak820_settings_caps_word_language() == 1 && ak820_settings_oneshot_timeout() == 0);
#ifdef AK820_COMPACT_LEADER
    assert(ak820_settings_leader_timeout() == AK820_LEADER_TIMEOUT);
#endif
}

static void seed_nondefault_runtime(void) {
    uint8_t value[2] = {1, 0};
    healthy = true;
    assert(!ak820_settings_set(1, value, 1));
    value[0] = 41; assert(!ak820_settings_set(2, value, 2));
    value[0] = 201; assert(!ak820_settings_set(7, value, 2));
    assert(ak820_settings_grave_esc() == 1 && ak820_settings_combo_term() == 41);
    assert(ak820_settings_tapping_term() == 201);
#ifdef AK820_COMPACT_LEADER
    {
        uint16_t timeout = AK820_LEADER_TIMEOUT == 1000 ? 999 : AK820_LEADER_TIMEOUT + 1;
        value[0] = timeout;
        value[1] = timeout >> 8;
    }
    assert(!ak820_settings_set(23, value, 2));
    assert(ak820_settings_leader_timeout() != AK820_LEADER_TIMEOUT);
#endif
}

static void check_invalid_blank_record(uint8_t reference, unsigned mismatch) {
    uint8_t before[sizeof(storage)];
    unsigned writes_before, faults_before;
    size_t i;
    seed_nondefault_runtime();
    writes_before = writes; faults_before = schema_faults;
    memset(storage + AK820_SETTINGS_ADDR, reference, AK820_SETTINGS_SIZE);
    if (mismatch < AK820_SETTINGS_SIZE)
        storage[AK820_SETTINGS_ADDR + mismatch] = reference == 0 ? 0xFF : 0;
    memcpy(before, storage, sizeof(before));
    healthy = true;
    ak820_settings_init();
    assert(schema_faults == faults_before + (mismatch < AK820_SETTINGS_SIZE));
    assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
    assert_defaults();
    assert(!healthy == (mismatch < AK820_SETTINGS_SIZE));
    for (i = 0; i < sizeof(before); ++i) assert(storage[i] == before[i]);
}

static void check_invalid_nonblank_record(uint8_t first) {
    uint8_t before[sizeof(storage)];
    unsigned writes_before, faults_before;
    seed_nondefault_runtime();
    writes_before = writes; faults_before = schema_faults;
    memset(storage + AK820_SETTINGS_ADDR, 0, AK820_SETTINGS_SIZE);
    storage[AK820_SETTINGS_ADDR] = first;
    memcpy(before, storage, sizeof(before));
    healthy = true;
    ak820_settings_init();
    assert(schema_faults == faults_before + 1 && !healthy);
    assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
    assert_defaults();
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
    /* Blank records are quiet; any single-byte mismatch is classified once. */
    for (i = 0; i < AK820_SETTINGS_SIZE; ++i) {
        check_invalid_blank_record(0, i);
        check_invalid_blank_record(0xFF, i);
    }
    check_invalid_blank_record(0, AK820_SETTINGS_SIZE);
    check_invalid_blank_record(0xFF, AK820_SETTINGS_SIZE);
    check_invalid_nonblank_record(1);
    check_invalid_nonblank_record(0xFE);
    /* Reinitializing a malformed record classifies it once per init. */
    {
        uint8_t before[sizeof(storage)];
        unsigned faults_before, writes_before;
        seed_nondefault_runtime();
        storage[AK820_SETTINGS_ADDR] = 1;
        memcpy(before, storage, sizeof(before));
        faults_before = schema_faults; writes_before = writes;
        healthy = true;
        ak820_settings_init();
        assert(schema_faults == faults_before + 1 && !healthy);
        assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
        assert_defaults();
        seed_nondefault_runtime();
        storage[AK820_SETTINGS_ADDR] = 1;
        memcpy(before, storage, sizeof(before));
        writes_before = writes;
        healthy = true;
        ak820_settings_init();
        assert(schema_faults == faults_before + 2 && !healthy);
        assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
        assert_defaults();
        seed_nondefault_runtime();
        memset(storage + AK820_SETTINGS_ADDR, 0, AK820_SETTINGS_SIZE);
        memcpy(before, storage, sizeof(before));
        writes_before = writes;
        healthy = true;
        ak820_settings_init();
        assert(schema_faults == faults_before + 2 && healthy);
        assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
        assert_defaults();
    }
    /* Consecutive malformed init calls must each classify the unchanged record. */
    {
        uint8_t before[sizeof(storage)];
        unsigned faults_before, writes_before;
        seed_nondefault_runtime();
        storage[AK820_SETTINGS_ADDR] = 1;
        memcpy(before, storage, sizeof(before));
        faults_before = schema_faults; writes_before = writes;
        healthy = true;
        ak820_settings_init();
        assert(schema_faults == faults_before + 1 && !healthy);
        assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
        assert_defaults();
        healthy = true;
        ak820_settings_init();
        assert(schema_faults == faults_before + 2 && !healthy);
        assert(writes == writes_before && !memcmp(storage, before, sizeof(before)));
        assert_defaults();
        healthy = true;
    }
    /* Isolate fixture seeding from the legacy counter assertions below. */
    writes = clears = 0;
    ak820_settings_query(1, out, sizeof(out));
    {
        static const uint8_t expected[] = {2,
#ifdef AK820_COMPACT_AUTOSHIFT
            3, 4,
#endif
#ifdef AK820_COMPACT_ONESHOT
            6,
#endif
            7, 18, 19, 22,
#ifdef AK820_COMPACT_LEADER
            23,
#endif
        };
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
    /* Exercise every advertised field at each short-buffer boundary. */
    {
        static const uint8_t ids[] = {1, 2, 7, 18, 19, 22,
#ifdef AK820_COMPACT_AUTOSHIFT
            3, 4,
#endif
#ifdef AK820_COMPACT_ONESHOT
            6,
#endif
#ifdef AK820_COMPACT_LEADER
            23,
#endif
        };
        unsigned field;
        uint8_t cap;
        for (field = 0; field < sizeof(ids); ++field) {
            uint8_t width = ids[field] == 1 || ids[field] == 3 || ids[field] == 22 ? 1 : 2;
            assert(!ak820_settings_get(ids[field], v, sizeof(v)));
            for (cap = 0; cap <= 2; ++cap) {
                memset(out, 0xA5, sizeof(out));
                assert(ak820_settings_get(ids[field], out, cap) == (cap < width ? -1 : 0));
                if (cap < width) {
                    for (i = 0; i < sizeof(out); ++i) assert(out[i] == 0xA5);
                } else {
                    assert(out[0] == v[0] && (width == 1 || out[1] == v[1]));
                    for (i = width; i < sizeof(out); ++i) assert(out[i] == 0xA5);
                }
                assert(ak820_settings_set(ids[field], v, cap) == (cap < width ? -1 : 0));
                assert(!writes && !clears && healthy);
            }
        }
    }
    assert(ak820_settings_get(2, out, 1) == -1);
    assert(ak820_settings_get(257, out, 2) == -1);
    assert(ak820_settings_set(257, out, 2) == -1);
    /* Every out-of-range ID must leave both output and persistent state alone. */
    {
        unsigned long id;
        size_t cap;
        v[0] = 1; v[1] = 0;
        for (id = 24; id <= 65535; ++id) {
            for (cap = 0; cap <= 2; ++cap) {
                memset(out, 0xA5, sizeof(out));
                assert(ak820_settings_get((uint16_t)id, out, cap) == -1);
                for (i = 0; i < sizeof(out); ++i) assert(out[i] == 0xA5);
                assert(ak820_settings_set((uint16_t)id, v, cap) == -1);
                assert(!writes && !clears && healthy);
            }
        }
    }
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
    /* A valid CRC must not hide an invalid value in any stored field. */
    {
        static const struct { uint8_t pos, low, high; } invalid[] = {
            {5, 0x10, 0}, {6, 0, 0}, {8, 0, 0}, {10, 101, 0},
            {12, 101, 0}, {14, 0, 0}, {16, 2, 0}, {17, 2, 0},
            {18, 0x31, 0x75}, {20, 0xe9, 3}
        };
        unsigned field;
        for (field = 0; field < sizeof(invalid) / sizeof(invalid[0]); ++field) {
            uint16_t crc;
            memcpy(storage + AK820_SETTINGS_ADDR, good, sizeof(good));
            storage[AK820_SETTINGS_ADDR + invalid[field].pos] = invalid[field].low;
            if (invalid[field].pos != 5 && invalid[field].pos != 16 && invalid[field].pos != 17)
                storage[AK820_SETTINGS_ADDR + invalid[field].pos + 1] = invalid[field].high;
            crc = ak820_crc16(storage + AK820_SETTINGS_ADDR, 22);
            storage[AK820_SETTINGS_ADDR + 22] = crc;
            storage[AK820_SETTINGS_ADDR + 23] = crc >> 8;
            healthy = true;
            ak820_settings_init();
            assert(!healthy);
        }
    }
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
    /* Validate old persisted records before upgrading in RAM. A read or
     * unchanged write never touches old bytes. */
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
        assert(storage[AK820_SETTINGS_ADDR + 2] == 3 && applied_language == 1);
        ak820_settings_init(); assert(healthy && applied_language == 1);
        /* Reserved legacy bytes with a valid CRC are not a future record. */
        memcpy(good, legacy, sizeof(good)); good[16] = 1;
        unsigned crc = ak820_crc16(good, 22); good[22] = crc; good[23] = crc >> 8;
        memcpy(storage + AK820_SETTINGS_ADDR, good, sizeof(good));
        healthy = true; ak820_settings_init(); assert(!healthy && applied_language == 1);
    }
#ifdef AK820_COMPACT_LEADER
    {
        unsigned before;
        uint8_t legacy_v2[AK820_SETTINGS_SIZE];
        memset(storage + AK820_SETTINGS_ADDR, 0, AK820_SETTINGS_SIZE);
        healthy = true; ak820_settings_init();
        assert(ak820_settings_leader_timeout() == AK820_LEADER_TIMEOUT);
        v[0] = 0; v[1] = 0; before = writes;
        assert(ak820_settings_set(23, v, 2) == -1 && writes == before);
        v[0] = 0xe9; v[1] = 3;
        assert(ak820_settings_set(23, v, 2) == -1 && writes == before);
        v[0] = 0xe8;
        assert(ak820_settings_set(23, v, 1) == -1 && writes == before);
        assert(!ak820_settings_set(23, v, 2) && ak820_settings_leader_timeout() == 1000);
        fail_write = true; v[0] = 1; v[1] = 0;
        assert(ak820_settings_set(23, v, 2) == -1 && ak820_settings_leader_timeout() == 1000);
        fail_write = false; healthy = true; ak820_settings_init();
        assert(ak820_settings_leader_timeout() == 1000);
        assert(!ak820_settings_reset() && ak820_settings_leader_timeout() == AK820_LEADER_TIMEOUT);
        memcpy(legacy_v2, storage + AK820_SETTINGS_ADDR, sizeof(legacy_v2));
        legacy_v2[2] = 2; legacy_v2[3] = 15; legacy_v2[4] = 127;
        legacy_v2[20] = legacy_v2[21] = 0;
        i = ak820_crc16(legacy_v2, 22); legacy_v2[22] = i; legacy_v2[23] = i >> 8;
        memcpy(storage + AK820_SETTINGS_ADDR, legacy_v2, sizeof(legacy_v2));
        before = writes; ak820_settings_init();
        assert(healthy && writes == before && ak820_settings_leader_timeout() == AK820_LEADER_TIMEOUT);
        assert(!memcmp(storage + AK820_SETTINGS_ADDR, legacy_v2, sizeof(legacy_v2)));
        v[0] = 1; v[1] = 0;
        assert(!ak820_settings_set(23, v, 2));
        assert(storage[AK820_SETTINGS_ADDR + 2] == 3 && ak820_settings_leader_timeout() == 1);
        assert(!memcmp(storage + AK820_SETTINGS_ADDR + 5, legacy_v2 + 5, 15));
    }
#else
    assert(ak820_settings_get(23, out, sizeof(out)) == -1);
    v[0] = 1; v[1] = 0;
    assert(ak820_settings_set(23, v, 2) == -1);
#endif
    puts("AK820 settings host model PASS");
}
