// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only behavioral checks. Compile with the board directory on -I. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_settings.h"
static unsigned writes, clears;
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
    uint8_t out[16], v[2], good[AK820_SETTINGS_SIZE];
    unsigned i;
    memset(storage, 0xA5, sizeof(storage));
    memset(storage + AK820_SETTINGS_ADDR, 0, AK820_SETTINGS_SIZE);
    ak820_settings_init();
    assert(healthy && !writes && ak820_settings_combo_term() == 40);
    assert(ak820_settings_tapping_term() == 200 && ak820_settings_caps_delay() == 80);
    assert(ak820_settings_tap_code_delay() == 0 && ak820_settings_autoshift_timeout() == 175);
    ak820_settings_query(1, out, sizeof(out));
#ifdef AK820_COMPACT_AUTOSHIFT
    assert(out[0] == 2 && out[2] == 4 && out[4] == 7 && out[6] == 18 && out[8] == 19 && out[10] == 255);
#else
    assert(out[0] == 2 && out[2] == 7 && out[4] == 18 && out[6] == 19 && out[8] == 255);
    assert(ak820_settings_get(4, out, sizeof(out)) == -1);
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
    v[0] = 40; assert(!ak820_settings_set(2, v, 2) && !writes && !clears);
    v[0] = 55; assert(!ak820_settings_set(2, v, 2) && writes == 1 && clears == 1);
    assert(storage[AK820_SETTINGS_ADDR - 1] == 0xA5 && storage[AK820_SETTINGS_ADDR + AK820_SETTINGS_SIZE] == 0xA5);
    ak820_settings_init(); assert(ak820_settings_combo_term() == 55 && healthy);
    /* Exhaust incoming values; accepted fields must pass startup validation.
     * Invalid values must not cancel owners or enter persistence. */
    {
        static const uint8_t ids[] = {1, 2, 7, 18, 19,
#ifdef AK820_COMPACT_AUTOSHIFT
            4,
#endif
        };
        unsigned field;
        for (field = 0; field < sizeof(ids); ++field) {
            unsigned long value;
            for (value = 0; value <= 65535; ++value) {
                unsigned before_writes = writes, before_clears = clears;
                bool accepted = ids[field] == 1 ? (value & 255) < 16 :
                    (ids[field] == 18 || ids[field] == 19) ? value <= 100 :
                    value >= 1 && value <= 1000;
                v[0] = value; v[1] = value >> 8;
                assert(ak820_settings_set(ids[field], v, 2) == (accepted ? 0 : -1));
                if (!accepted) {
                    assert(writes == before_writes && clears == before_clears);
                } else {
                    assert(!ak820_settings_get(ids[field], out, sizeof(out)));
                    assert(out[0] == v[0] && (ids[field] == 1 || out[1] == v[1]));
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
    puts("AK820 settings host model PASS");
}
