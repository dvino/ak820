/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once

#include <stdbool.h>
#include <stdint.h>

#ifdef RGB_MATRIX_ENABLE
#    include "rgb_matrix_types.h"
#    ifdef __SDCC_mcs51
#        define AK820_RGB_CODE __code
#    else
#        define AK820_RGB_CODE
#    endif
/* Fixed board metadata lives in CODE. The electrical slot is row*8+column,
 * so Vial can derive its matrix coordinates from the same driver table. */
extern const uint8_t AK820_RGB_CODE ak820_rgb_slots[RGB_MATRIX_LED_COUNT];
extern const led_point_t AK820_RGB_CODE ak820_led_points[RGB_MATRIX_LED_COUNT];
#endif

#define AK820_SCAN_ROWS 16
#define AK820_SCAN_COLS 8
#define AK820_LED_DMA_ADDRESS 0x0200
#define AK820_LED_DMA_BYTES 512

/* Called before USB/timer setup. Uses the clock sequence from OEM ROM 2FE2. */
void ak820_clock_init(void);

/* Starts the shared keyboard/RGB multiplexer, after loader callbacks exist. */
void ak820_board_init(void);

/* Loader IRQ11 stub 301E must jump here. Returns with RET, not RETI. */
void ak820_led_irq(void);

/* Copies a completed matrix sweep into rows, returns whether it changed. */
bool ak820_matrix_snapshot(uint8_t *rows);

/* LED electrical index is the same 0..127 slot as row * 8 + column. */
void ak820_set_slot_rgb(uint8_t slot, uint8_t r, uint8_t g, uint8_t b);
void ak820_update_indicators(void);

#ifdef __SDCC_mcs51
extern volatile __xdata __at(AK820_LED_DMA_ADDRESS) uint8_t ak820_led_dma[AK820_LED_DMA_BYTES];
#endif
