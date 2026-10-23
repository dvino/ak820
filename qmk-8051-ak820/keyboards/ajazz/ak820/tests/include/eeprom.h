/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once
#include <stdint.h>
#include <stddef.h>

/* Host-only adapters to the actual board EEPROM backend. */
void eeprom_driver_init(void);
void eeprom_read_block(void *data, const void *address, size_t size);
void eeprom_write_block(const void *data, void *address, size_t size);
static inline uint8_t eeprom_read_byte(const uint8_t *address) {
    uint8_t value;
    eeprom_read_block(&value, address, 1);
    return value;
}
static inline void eeprom_update_byte(uint8_t *address, uint8_t value) {
    eeprom_write_block(&value, address, 1);
}
