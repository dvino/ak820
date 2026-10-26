/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Based on https://github.com/qmk/qmk_firmware/pull/13036 */

#include "vialrgb.h"

#include <inttypes.h>
#include <string.h>
#include "rgb_matrix.h"
#include "vial.h"
#ifdef AK820_BOARD
#    include "ak820_board.h"
#    include "timer.h"
#    ifdef __SDCC_mcs51
extern uint8_t __xdata raw_buffer[VIAL_RAW_EPSIZE];
#    endif
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
#ifdef AK820_BOARD
_Static_assert(RGB_MATRIX_LED_COUNT == 82 && sizeof(HSV) == 3, "Direct v1 palette ABI changed");
uint8_t VIALRGB_BUFFER ak820_direct_stage[246];
volatile uint8_t VIALRGB_BUFFER ak820_direct_state;
static uint32_t direct_generation;
static uint16_t direct_id;
static uint16_t direct_at;
static uint8_t direct_coverage;

void ak820_direct_tick(void) {
    if (ak820_direct_state == AK820_DIRECT_UPLOAD && timer_elapsed(direct_at) >= AK820_DIRECT_TIMEOUT)
        ak820_direct_state = AK820_DIRECT_CANCELLED;
}

static uint8_t direct_flags(void) {
    return (rgb_matrix_is_enabled() ? 1 : 0) |
           (rgb_matrix_get_mode() == RGB_MATRIX_VIALRGB_DIRECT ? 2 : 0) |
           (rgb_matrix_get_suspend_state() ? 4 : 0);
}

extern uint8_t VIALRGB_BUFFER raw_buffer[VIAL_RAW_EPSIZE];
#define DIRECT_ARGS (raw_buffer + 2)

/* Compare only the four wire bytes; generic memcmp brings an unnecessary
 * memory-space dispatcher into these fixed-XDATA packets. */
static bool direct_generation_matches(uint8_t offset) {
    const uint8_t VIALRGB_BUFFER *generation = (const uint8_t VIALRGB_BUFFER *)&direct_generation;
    for (uint8_t i = 0; i < 4; ++i) {
        if (raw_buffer[offset + i] != generation[i]) return false;
    }
    return true;
}

static void direct_get(void) {
    static const uint8_t info[] = {'A', 'D', 1, 3, RGB_MATRIX_LED_COUNT, 1, 1,
        RGB_MATRIX_MAXIMUM_BRIGHTNESS, 7, 8,
        AK820_DIRECT_TIMEOUT & 255, AK820_DIRECT_TIMEOUT >> 8};
    uint8_t VIALRGB_BUFFER *args = DIRECT_ARGS;
    uint8_t cmd = raw_buffer[1];
    uint8_t first = args[4], count = args[5];
    uint8_t status = AK820_DIRECT_OK;
    if (cmd == ak820_direct_info) {
        /* Magic rejects an older image's untouched request. HSV8 and Vial
         * LED indices are independent of the current output being dark. */
        for (uint8_t i = 0; i < sizeof(info); ++i) args[i] = info[i];
    } else {
        if (cmd == ak820_direct_status) {
            args[0] = ak820_direct_state;
            args[1] = direct_coverage;
            args[2] = direct_id;
            args[3] = direct_id >> 8;
            args[8] = direct_flags();
        } else {
            if (!count || count > 7 || first >= RGB_MATRIX_LED_COUNT || count > RGB_MATRIX_LED_COUNT - first)
                status = AK820_DIRECT_INVALID;
            else if (!direct_generation_matches(2)) status = AK820_DIRECT_STALE;
            args[0] = status; args[1] = first; args[2] = count; args[3] = direct_flags();
            if (!status) memcpy(args + 8, &g_direct_mode_colors[first], (uint8_t)(count * 3));
        }
        const uint8_t VIALRGB_BUFFER *generation = (const uint8_t VIALRGB_BUFFER *)&direct_generation;
        for (uint8_t i = 0; i < 4; ++i) args[4 + i] = generation[i];
    }
}

static uint8_t direct_set(void) {
    uint8_t VIALRGB_BUFFER *args = DIRECT_ARGS;
    uint8_t cmd = raw_buffer[1];
    uint8_t first, count, i, bytes;
    uint8_t VIALRGB_BUFFER *target;
    if (cmd == ak820_direct_begin) {
        if (ak820_direct_state >= AK820_DIRECT_RENDER && ak820_direct_state <= AK820_DIRECT_PUBLISH)
            return AK820_DIRECT_BUSY;
        /* A new BEGIN replaces an unfinished upload. No live color changes. */
        ak820_direct_state = AK820_DIRECT_CANCELLED;
        if (args[0] != 1 || args[1] != RGB_MATRIX_LED_COUNT || !(args[2] | args[3]))
            return AK820_DIRECT_INVALID;
        if (!direct_generation_matches(6)) return AK820_DIRECT_STALE;
        direct_id = (uint16_t)args[2] | ((uint16_t)args[3] << 8);
        direct_coverage = 0;
        direct_at = timer_read();
        ak820_direct_state = AK820_DIRECT_UPLOAD;
        return AK820_DIRECT_OK;
    }
    if (args[0] != (uint8_t)direct_id || args[1] != (uint8_t)(direct_id >> 8)) return AK820_DIRECT_ID;
    if (cmd == ak820_direct_commit && ak820_direct_state >= AK820_DIRECT_RENDER && ak820_direct_state <= AK820_DIRECT_DONE)
        return AK820_DIRECT_OK; /* Idempotent retry, no second publication. */
    if (ak820_direct_state != AK820_DIRECT_UPLOAD) return AK820_DIRECT_BUSY;
    if (cmd == ak820_direct_abort) {
        ak820_direct_state = AK820_DIRECT_CANCELLED;
        return AK820_DIRECT_OK;
    }
    if (cmd == ak820_direct_commit) {
        ak820_direct_state = AK820_DIRECT_CANCELLED;
        if (direct_coverage != RGB_MATRIX_LED_COUNT) return AK820_DIRECT_INCOMPLETE;
        memcpy(g_direct_mode_colors, ak820_direct_stage, sizeof(ak820_direct_stage));
        ++direct_generation;
        /* Commit changes RAM only; do not select Direct, enable RGB or save. */
        ak820_direct_state = direct_flags() == 3 ? AK820_DIRECT_RENDER : AK820_DIRECT_DONE;
        return AK820_DIRECT_OK;
    }
    first = args[2]; count = args[3];
    if (!count || count > 8 || first > direct_coverage || first >= RGB_MATRIX_LED_COUNT ||
        count > RGB_MATRIX_LED_COUNT - first || (first < direct_coverage && count > direct_coverage - first)) {
        ak820_direct_state = AK820_DIRECT_CANCELLED;
        return AK820_DIRECT_INVALID;
    }
    target = ak820_direct_stage + (uint8_t)(first * 3);
    args += 4;
    bytes = count * 3;
    /* Sequential chunks; exact duplicates are harmless. Compare the clamped
     * representation, matching legacy fastset's brightness semantics. */
    for (i = 2; i < bytes; i += 3) {
        if (args[i] > RGB_MATRIX_MAXIMUM_BRIGHTNESS) args[i] = RGB_MATRIX_MAXIMUM_BRIGHTNESS;
    }
    if (first < direct_coverage) {
        for (i = 0; i < bytes; ++i) {
            if (target[i] != args[i]) {
                ak820_direct_state = AK820_DIRECT_CANCELLED;
                return AK820_DIRECT_INVALID;
            }
        }
    } else {
        memcpy(target, args, bytes);
        direct_coverage += count;
    }
    direct_at = timer_read();
    return AK820_DIRECT_OK;
}

bool ak820_direct_request(void) {
    uint8_t cmd = raw_buffer[1];
    ak820_direct_tick();
    if (raw_buffer[0] == 8 && cmd >= ak820_direct_info && cmd <= ak820_direct_status) {
        if (vial_unlock_in_progress) raw_buffer[2] = AK820_DIRECT_BUSY;
        else direct_get();
    } else if (raw_buffer[0] == 7 && cmd >= ak820_direct_begin && cmd <= ak820_direct_abort) {
        raw_buffer[2] = vial_unlock_in_progress ? AK820_DIRECT_BUSY : direct_set();
    } else return false;
    return true;
}
#endif
#endif

#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
static void get_supported_fixed(void) {
    /* The validated 32-byte transport always has room for every board mode.
     * Keep the wire threshold 16-bit, including unsupported high bytes. */
    _Static_assert(SUPPORTED_MODES_LENGTH * 2 <= VIAL_RAW_EPSIZE - 2, "VialRGB mode reply capacity changed");
    uint8_t gt = raw_buffer[2], high = raw_buffer[3], out = 2;
    for (uint8_t i = 2; i < VIAL_RAW_EPSIZE; ++i) raw_buffer[i] = 0xff;
    if (high) return;
    for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
        uint8_t id = READ_MODE_ID(&supported_modes[i].vialrgb_id);
        if (id > gt) {
            raw_buffer[out++] = id;
            raw_buffer[out++] = 0;
        }
    }
}
#endif

static void get_supported(uint8_t VIALRGB_BUFFER *args, uint8_t length) {
    /* retrieve supported effects (VialRGB IDs) with ID > gt */
#ifdef AK820_BOARD
    uint8_t gt = args[0];
    bool high = args[1] != 0;
#else
    uint16_t gt = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
#endif
    for (uint8_t i = 0; i < length; ++i) args[i] = 0xff;
#ifdef AK820_BOARD
    if (high) return;
#endif
    for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
        vialrgb_mode_id_t id = READ_MODE_ID(&supported_modes[i].vialrgb_id);
        if (id > gt && length >= 2) {
            args[0] = id;
            args[1] = id >> 8;
            length -= 2;
            args += 2;
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
#ifdef __SDCC_mcs51
    /* The public entry already checked sole-buffer ownership and length. */
    args = raw_buffer + 2;
#endif
    /* The AK820 direct-fastset packet is fixed at VIAL_RAW_EPSIZE. After
     * the two VIA bytes, args[0..29] are always available. */
    _Static_assert(VIAL_RAW_EPSIZE == 32, "AK820 VialRGB fastset packet layout changed");
    _Static_assert(RGB_MATRIX_LED_COUNT <= UINT8_MAX, "AK820 LED index must fit in one byte");
    uint8_t first_index = args[0];
    uint8_t num_leds = args[2];
    if (args[1] || num_leds > (VIAL_RAW_EPSIZE - 5) / 3 || first_index >= RGB_MATRIX_LED_COUNT) return;
    if (num_leds) {
        /* Legacy fastset wins over an uncommitted upload. An accepted atomic
         * publication owns staging until the IRQ finishes, so legacy writes
         * update only the active HSV palette and follow it on the next frame. */
        if (ak820_direct_state == AK820_DIRECT_UPLOAD) ak820_direct_state = AK820_DIRECT_CANCELLED;
        ++direct_generation;
    }
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
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    if ((uint8_t __xdata *)data != raw_buffer) return;
    uint8_t __xdata *args = raw_buffer + 2;
#else
    uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
#endif
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
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
        get_supported_fixed();
#else
        get_supported(args, length - 2);
#endif
        break;
    }
#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT
    case vialrgb_get_number_leds: {
        args[0] = RGB_MATRIX_LED_COUNT & 0xFF;
        args[1] = RGB_MATRIX_LED_COUNT >> 8;
        break;
    }
    case vialrgb_get_led_info: {
#ifdef AK820_BOARD
        uint8_t led = args[0];
        if (args[1] || led >= RGB_MATRIX_LED_COUNT) return;
#else
        uint16_t led = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
        if (led >= RGB_MATRIX_LED_COUNT) return;
#endif
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
#ifdef AK820_BOARD
        uint8_t slot = ak820_rgb_slots[led];
        args[3] = slot >> 3;
        args[4] = slot & 7;
#else
        // position in keyboard matrix (if it's keyboard LED, otherwise 0xFF)
        get_matrix_pos_for_led(led, &args[3]);
#endif
        break;
    }
#endif
    }
}

void vialrgb_set_value(uint8_t *data, uint8_t length) {
    if (length != VIAL_RAW_EPSIZE) return;

    /* data[0] is used by VIA command id */
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    if ((uint8_t __xdata *)data != raw_buffer) return;
    uint8_t __xdata *args = raw_buffer + 2;
#else
    uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
#endif
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
