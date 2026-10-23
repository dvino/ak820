#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

/* Copyright 2019 Nick Brassel (tzarc)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdint.h>
#include <string.h>

#include "eeprom_driver.h"

#if defined(AK820_BOARD) || defined(AK820_NVM_SCALAR_TEST)
#    include "ak820_nvm.h"
#    define EEPROM_LOCAL_READ ak820_eeprom_read_block_xdata
#    define EEPROM_LOCAL_WRITE ak820_eeprom_write_block_xdata
#else
#    define EEPROM_LOCAL_READ eeprom_read_block
#    define EEPROM_LOCAL_WRITE eeprom_write_block
#endif

#if !defined(AK820_BOARD) && !defined(AK820_NVM_SCALAR_TEST)
uint8_t eeprom_read_byte(const uint8_t *addr) {
    uint8_t ret = 0;
    eeprom_read_block(&ret, addr, 1);
    return ret;
}
#endif

uint16_t eeprom_read_word(const uint16_t *addr) {
    uint16_t ret = 0;
    EEPROM_LOCAL_READ(&ret, addr, 2);
    return ret;
}

uint32_t eeprom_read_dword(const uint32_t *addr) {
    uint32_t ret = 0;
    EEPROM_LOCAL_READ(&ret, addr, 4);
    return ret;
}

void eeprom_write_byte(uint8_t *addr, uint8_t value) {
    EEPROM_LOCAL_WRITE(&value, addr, 1);
}

void eeprom_write_word(uint16_t *addr, uint16_t value) {
    EEPROM_LOCAL_WRITE(&value, addr, 2);
}

void eeprom_write_dword(uint32_t *addr, uint32_t value) {
    EEPROM_LOCAL_WRITE(&value, addr, 4);
}

void eeprom_update_block(const void *buf, void *addr, size_t len) {
    const uint8_t *source = (const uint8_t *)buf;
    const uint8_t *target = (const uint8_t *)addr;
    size_t i;
    // The old SDCC adaptation allocated len bytes and never freed them.
    // Compare incrementally and preserve one full block update for backends.
    for (i = 0; i < len; ++i) {
        if (eeprom_read_byte(target + i) != source[i]) {
            eeprom_write_block(buf, addr, len);
            return;
        }
    }
}

void eeprom_update_byte(uint8_t *addr, uint8_t value) {
    uint8_t orig = eeprom_read_byte(addr);
    if (orig != value) {
        eeprom_write_byte(addr, value);
    }
}

void eeprom_update_word(uint16_t *addr, uint16_t value) {
    uint16_t orig = eeprom_read_word(addr);
    if (orig != value) {
        eeprom_write_word(addr, value);
    }
}

void eeprom_update_dword(uint32_t *addr, uint32_t value) {
    uint32_t orig = eeprom_read_dword(addr);
    if (orig != value) {
        eeprom_write_dword(addr, value);
    }
}
