/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Based on https://github.com/qmk/qmk_firmware/pull/13036 */

#include "vialrgb.h"

#include <inttypes.h>
#include <string.h>
#include "rgb_matrix.h"
#include "vial.h"
#ifdef AK820_BOARD
#    include "ak820_board.h"
#endif

/* Both private AK820 mode enums fit in one byte. Wire mode IDs remain
 * 16-bit, including rejection of unsupported high-byte values. */
#ifdef AK820_BOARD
typedef uint8_t vialrgb_mode_id_t;
#    define READ_MODE_ID(address) pgm_read_byte(address)
#else
typedef uint16_t vialrgb_mode_id_t;
#    define READ_MODE_ID(address) pgm_read_word(address)
#endif

typedef struct {
    vialrgb_mode_id_t vialrgb_id;
    vialrgb_mode_id_t qmk_id;
} vialrgb_supported_mode_t;

#include "vialrgb_effects.inc"

#ifdef AK820_BOARD
_Static_assert(VIALRGB_EFFECT_PIXEL_FRACTAL <= UINT8_MAX, "VialRGB mode IDs must fit in a byte");
_Static_assert(RGB_MATRIX_EFFECT_MAX <= UINT8_MAX, "QMK mode IDs must fit in a byte");
#endif

#define SUPPORTED_MODES_LENGTH (sizeof(supported_modes)/sizeof(*supported_modes))

#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT
HSV g_direct_mode_colors[RGB_MATRIX_LED_COUNT];
#endif

static void get_supported(uint8_t VIALRGB_BUFFER *args, uint8_t length) {
    /* retrieve supported effects (VialRGB IDs) with ID > gt */
    uint16_t gt = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
    for (uint8_t i = 0; i < length; ++i) args[i] = 0xff;
    for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
        uint16_t id = READ_MODE_ID(&supported_modes[i].vialrgb_id);
        if (id > gt && length >= sizeof(id)) {
            args[0] = id;
            args[1] = id >> 8;
            length -= sizeof(id);
            args += sizeof(id);
        }
    }
}

static uint16_t qmk_id_to_vialrgb_id(uint16_t id) {
    for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
        uint16_t qmk_id = READ_MODE_ID(&supported_modes[i].qmk_id);
        if (qmk_id == id)
            return READ_MODE_ID(&supported_modes[i].vialrgb_id);
    }
    return 0;
}

static uint16_t vialrgb_id_to_qmk_id(uint16_t id) {
    for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
        uint16_t vialrgb_id = READ_MODE_ID(&supported_modes[i].vialrgb_id);
        if (vialrgb_id == id)
            return READ_MODE_ID(&supported_modes[i].qmk_id);
    }
    return 0;
}

static uint16_t get_mode(void) {
    /* Get current mode as vialrgb ID */
    if (!rgb_matrix_is_enabled())
        return VIALRGB_EFFECT_OFF;
    return qmk_id_to_vialrgb_id(rgb_matrix_get_mode());
}

static void set_mode(uint16_t mode) {
    /* Set a mode as vialrgb ID */
    if (mode == VIALRGB_EFFECT_OFF) {
        rgb_matrix_disable_noeeprom();
    } else {
        rgb_matrix_enable_noeeprom();
        rgb_matrix_mode_noeeprom(vialrgb_id_to_qmk_id(mode));
    }
}

#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT
static void get_matrix_pos_for_led(uint16_t led, uint8_t VIALRGB_BUFFER *output) {
#ifdef AK820_BOARD
    uint8_t slot = ak820_rgb_slots[led];
    output[0] = slot >> 3;
    output[1] = slot & 7;
#else
    /* reset initially so if we cannot locate the led, it's considered not part of kb matrix */
    output[0] = output[1] = 0xFF;
    /* this is kinda O(n^2) but what can you do */
    for (uint8_t row = 0; row < MATRIX_ROWS; ++row)
        for (uint8_t col = 0; col < MATRIX_COLS; ++col)
            if (g_led_config.matrix_co[row][col] == led) {
                output[0] = row;
                output[1] = col;
                return;
            }
#endif
}

#ifdef AK820_BOARD
static void fast_set_leds(uint8_t VIALRGB_BUFFER *args) {
    /* The AK820 direct-fastset packet is fixed at VIAL_RAW_EPSIZE. After
     * the two VIA bytes, args[0..29] are always available. */
    _Static_assert(VIAL_RAW_EPSIZE == 32, "AK820 VialRGB fastset packet layout changed");
    _Static_assert(RGB_MATRIX_LED_COUNT <= UINT8_MAX, "AK820 LED index must fit in one byte");
    uint8_t first_index = args[0];
    uint8_t num_leds = args[2];
    if (args[1] || num_leds > (VIAL_RAW_EPSIZE - 5) / 3 || first_index >= RGB_MATRIX_LED_COUNT) return;
    if (num_leds > RGB_MATRIX_LED_COUNT - first_index) num_leds = RGB_MATRIX_LED_COUNT - first_index;
    HSV VIALRGB_BUFFER *color = &g_direct_mode_colors[first_index];
    args += 3;
    while (num_leds--) {
        color->h = *args++;
        color->s = *args++;
        uint8_t val = *args++;
        color->v = (val > RGB_MATRIX_MAXIMUM_BRIGHTNESS) ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
        ++color;
    }
}
#else
static void fast_set_leds(uint8_t VIALRGB_BUFFER *args, uint8_t length) {
    /* Set multiple leds HSV, first 2 bytes are index of the first led, then number of leds, followed by HSV for the leds */
    /* we have 32-2-2-1=27 total bytes available, so can set up to 9 leds per packet */
    if (length < 3) return;

    uint16_t first_index = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
    uint8_t num_leds = args[2];
    length -= 3;
    args += 3;

    /* length is an unsigned byte; avoid SDCC's signed-division promotion. */
    if ((uint16_t)num_leds * 3u > length || first_index >= RGB_MATRIX_LED_COUNT) return;
    if (num_leds > RGB_MATRIX_LED_COUNT - first_index) num_leds = RGB_MATRIX_LED_COUNT - first_index;

    for (uint8_t i = 0; i < num_leds; ++i) {
        HSV VIALRGB_BUFFER *color = &g_direct_mode_colors[first_index++];
        color->h = *args++;
        color->s = *args++;
        uint8_t val = *args++;
        color->v = (val > RGB_MATRIX_MAXIMUM_BRIGHTNESS) ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
    }
}
#endif
#endif

void vialrgb_get_value(uint8_t *data, uint8_t length) {
    if (length != VIAL_RAW_EPSIZE) return;

    /* data[0] is used by VIA command id */
    uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
    uint8_t cmd = args[-1];
    switch (cmd) {
    case vialrgb_get_info:
        args[0] = VIALRGB_PROTOCOL_VERSION & 0xFF;
        args[1] = VIALRGB_PROTOCOL_VERSION >> 8;
        args[2] = RGB_MATRIX_MAXIMUM_BRIGHTNESS;
        break;
    case vialrgb_get_mode: {
        uint16_t vialrgb_id = get_mode();
        args[0] = vialrgb_id & 0xFF;
        args[1] = vialrgb_id >> 8;
        args[2] = rgb_matrix_get_speed();
        args[3] = rgb_matrix_get_hue();
        args[4] = rgb_matrix_get_sat();
        args[5] = rgb_matrix_get_val();
        break;
    }
    case vialrgb_get_supported: {
        get_supported(args, length - 2);
        break;
    }
#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT
    case vialrgb_get_number_leds: {
        args[0] = RGB_MATRIX_LED_COUNT & 0xFF;
        args[1] = RGB_MATRIX_LED_COUNT >> 8;
        break;
    }
    case vialrgb_get_led_info: {
        uint16_t led = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
        if (led >= RGB_MATRIX_LED_COUNT) return;
#ifdef AK820_BOARD
        args[0] = ak820_led_points[led].x;
        args[1] = ak820_led_points[led].y;
        args[2] = LED_FLAG_KEYLIGHT;
#else
        // x, y
        args[0] = g_led_config.point[led].x;
        args[1] = g_led_config.point[led].y;
        // flags
        args[2] = g_led_config.flags[led];
#endif
        // position in keyboard matrix (if it's keyboard LED, otherwise 0xFF)
        get_matrix_pos_for_led(led, &args[3]);
        break;
    }
#endif
    }
}

void vialrgb_set_value(uint8_t *data, uint8_t length) {
    if (length != VIAL_RAW_EPSIZE) return;

    /* data[0] is used by VIA command id */
    uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
    uint8_t cmd = args[-1];
    switch (cmd) {
    case vialrgb_set_mode: {
        uint16_t vialrgb_id = args[0] | (args[1] << 8);
        set_mode(vialrgb_id);
        rgb_matrix_set_speed_noeeprom(args[2]);
        rgb_matrix_sethsv_noeeprom(args[3], args[4], args[5]);
        break;
    }
#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT
    case vialrgb_direct_fastset: {
#ifdef AK820_BOARD
        fast_set_leds(args);
#else
        fast_set_leds(args, length - 2);
#endif
        break;
    }
#endif
    }
}

void vialrgb_save(uint8_t *data, uint8_t length) {
    (void)data;
    (void)length;

    eeconfig_update_rgb_matrix();
}
