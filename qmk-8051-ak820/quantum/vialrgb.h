/* SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

#include <inttypes.h>
#include <stdbool.h>

#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
#    define VIALRGB_BUFFER __xdata
#else
#    define VIALRGB_BUFFER
#endif

#define VIALRGB_PROTOCOL_VERSION 1

/* Start at 0x40 in order to not conflict with existing "enum via_lighting_value",
   even though they likely wouldn't be enabled together with vialrgb */
enum {
    vialrgb_set_mode = 0x41,
    vialrgb_direct_fastset = 0x42,
    ak820_direct_begin = 0x43,
    ak820_direct_chunk = 0x44,
    ak820_direct_commit = 0x45,
    ak820_direct_abort = 0x46,
};

enum {
    vialrgb_get_info = 0x40,
    vialrgb_get_mode = 0x41,
    vialrgb_get_supported = 0x42,
    vialrgb_get_number_leds = 0x43,
    vialrgb_get_led_info = 0x44,
    ak820_direct_info = 0x45,
    ak820_direct_read = 0x46,
    ak820_direct_status = 0x47,
};

/* AK820 Direct extension v1. The staging array changes from HSV to RGB only
 * after the complete HSV frame has been committed. States 3/4 belong to the
 * LED IRQ: it starts at scan row zero and publishes one row before its native
 * DMA transfer. Neither the host nor the renderer may reuse it until DONE. */
enum {
    AK820_DIRECT_IDLE, AK820_DIRECT_UPLOAD, AK820_DIRECT_RENDER,
    AK820_DIRECT_QUEUED, AK820_DIRECT_PUBLISH, AK820_DIRECT_DONE,
    AK820_DIRECT_CANCELLED,
};
enum {
    AK820_DIRECT_OK, AK820_DIRECT_INVALID, AK820_DIRECT_BUSY,
    AK820_DIRECT_STALE, AK820_DIRECT_INCOMPLETE, AK820_DIRECT_ID,
};
#define AK820_DIRECT_TIMEOUT 1000
#if defined(AK820_BOARD) && !defined(VIALRGB_NO_DIRECT)
extern uint8_t VIALRGB_BUFFER ak820_direct_stage[246];
extern volatile uint8_t VIALRGB_BUFFER ak820_direct_state;
void ak820_direct_tick(void);
void ak820_direct_cancel(void);
bool ak820_direct_request(void);
#endif

void vialrgb_get_value(uint8_t *data, uint8_t length);
void vialrgb_set_value(uint8_t *data, uint8_t length);
void vialrgb_save(uint8_t *data, uint8_t length);

#if defined(VIALRGB_ENABLE) && !defined(RGB_MATRIX_ENABLE)
#error VIALRGB_ENABLE=yes requires RGB_MATRIX_ENABLE=yes
#endif
