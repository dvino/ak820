#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

/* SPDX-License-Identifier: GPL-2.0-or-later
 * Compact QMK RGB Matrix API for the AK820 8051 target.
 * Effects: solid, breathing, cycle-all, cycle-left-right, and Vial direct.
 * Configuration deliberately retains QMK's eight-byte EEPROM representation.
 * Render at most eight LEDs per task so USB/keyboard tasks remain cooperative.
 */
#include "rgb_matrix.h"
#include "eeprom.h"
#include "eeconfig.h"
#include "timer.h"
#include "vialrgb.h"
#include "ak820_board.h"
#include "ak820_nvm.h"
#include "led_tables.h"
#include <string.h>

rgb_config_t rgb_matrix_config;
extern HSV g_direct_mode_colors[RGB_MATRIX_LED_COUNT];

#if defined(__SDCC_mcs51)
#    define AK820_FLAG __bit
#else
#    define AK820_FLAG bool
#endif

static AK820_FLAG suspended;
static AK820_FLAG dirty;
static AK820_FLAG rendering;
static uint16_t changed_at;
static uint16_t frame_at;
static uint16_t phase;
static uint8_t led_index;
static uint8_t frame_mode;
static uint8_t frame_hue;
static uint8_t frame_sat;
static uint8_t frame_val;
static uint8_t frame_flags;
static uint8_t frame_phase;
/* Ages use 16-ms ticks: at most 4080 ms, refreshed independently per LED.
 * A press restarts the fade; releases never extinguish another held key. */
static uint8_t reactive_age[RGB_MATRIX_LED_COUNT];
static uint16_t reactive_at;

static void clear_reactive(void) {
    memset(reactive_age, 0, sizeof(reactive_age));
    reactive_at = timer_read();
}

static void age_reactive(void) {
    uint16_t ticks = timer_elapsed(reactive_at) >> 4;
    uint8_t i, decay;
    if (!ticks) return;
    reactive_at += ticks << 4;
    /* Every age is one byte, so larger tick counts have the same zero result. */
    decay = ticks > 255 ? 255 : (uint8_t)ticks;
    for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
        reactive_age[i] = decay >= reactive_age[i] ? 0 : reactive_age[i] - decay;
    }
}

static uint8_t add_sat(uint8_t x, uint8_t y) {
    return x > (uint8_t)(255 - y) ? 255 : x + y;
}

static uint8_t sub_sat(uint8_t x, uint8_t y) {
    return x < y ? 0 : x - y;
}

static void mark_dirty(void) {
    dirty = true;
    changed_at = timer_read();
}

void eeconfig_update_rgb_matrix(void) {
    /* The trailing bytes are part of the stable QMK EEPROM ABI. */
    uint8_t *raw = (uint8_t *)&rgb_matrix_config;
    raw[6] = raw[7] = 0;
    ak820_eeprom_update_block_xdata(&rgb_matrix_config, EECONFIG_RGB_MATRIX, sizeof(rgb_matrix_config));
    dirty = false;
}

void eeconfig_update_rgb_matrix_default(void) {
    memset(&rgb_matrix_config, 0, sizeof(rgb_matrix_config));
    rgb_matrix_config.enable = 1;
    rgb_matrix_config.mode = RGB_MATRIX_DEFAULT_MODE;
    rgb_matrix_config.hsv.h = 0;
    rgb_matrix_config.hsv.s = 255;
    rgb_matrix_config.hsv.v = RGB_MATRIX_DEFAULT_VAL;
    rgb_matrix_config.speed = RGB_MATRIX_DEFAULT_SPD;
    rgb_matrix_config.flags = LED_FLAG_ALL;
    eeconfig_update_rgb_matrix();
}

void rgb_matrix_reload_from_eeprom(void) {
    ak820_eeprom_read_block_xdata(&rgb_matrix_config, EECONFIG_RGB_MATRIX, sizeof(rgb_matrix_config));
    if (!rgb_matrix_config.mode || rgb_matrix_config.mode >= RGB_MATRIX_EFFECT_MAX || rgb_matrix_config.enable > 1) {
        eeconfig_update_rgb_matrix_default();
    }
    if (rgb_matrix_config.hsv.v > RGB_MATRIX_MAXIMUM_BRIGHTNESS) {
        rgb_matrix_config.hsv.v = RGB_MATRIX_MAXIMUM_BRIGHTNESS;
    }
    dirty = false;
    rendering = false;
    clear_reactive();
}

void rgb_matrix_init(void) {
    rgb_matrix_driver.init();
    rgb_matrix_reload_from_eeprom();
    frame_at = timer_read() - RGB_MATRIX_LED_FLUSH_LIMIT;
}

void rgb_matrix_set_color(int index, uint8_t r, uint8_t g, uint8_t b) {
    if (index >= 0 && index < RGB_MATRIX_LED_COUNT) rgb_matrix_driver.set_color(index, r, g, b);
}

void rgb_matrix_set_color_all(uint8_t r, uint8_t g, uint8_t b) {
    rgb_matrix_driver.set_color_all(r, g, b);
}

/* FastLED/QMK's piecewise sine approximation, expressed using C only. */
static uint8_t sine8(uint8_t theta) {
    static const uint8_t coefficients[8] = {0, 49, 49, 41, 90, 27, 117, 10};
    uint8_t offset = theta;
    uint8_t section, fraction, value;
    if (theta & 0x40) offset = 255 - offset;
    offset &= 0x3f;
    fraction = offset & 15;
    if (theta & 0x40) ++fraction;
    section = (offset >> 4) * 2;
    value = coefficients[section] + (((uint16_t)coefficients[section + 1] * fraction) >> 4);
    return (theta & 0x80) ? 128 - value : 128 + value;
}

#ifdef USE_CIE1931_CURVE
/* Interpolate once per breathing frame, before HSV conversion. Other effects
 * retain the existing compact curve. Runtime brightness is clamped to 160,
 * below the compact table's irregular final interval. No extra table or
 * per-LED state is needed. */
static uint8_t breathing_cie(uint8_t value) {
#ifdef AK820_FULL_CIE
    return pgm_read_byte(&CIE1931_CURVE[value]);
#else
    uint8_t index = value >> 3;
    uint8_t low = pgm_read_byte(&CIE1931_CURVE[index]);
    if (index == 31) return low;
    uint8_t delta = pgm_read_byte(&CIE1931_CURVE[index + 1]) - low;
    uint8_t fraction = value & 7;
    uint8_t product = (uint8_t)(delta * fraction);
    return low + (product >> 3);
#endif
}
#endif

void rgb_matrix_task(void) {
    uint8_t end;
    HSV hsv;
    RGB rgb;
    age_reactive();
    if (dirty && timer_elapsed(changed_at) >= 1000) eeconfig_update_rgb_matrix();
    if (!rendering) {
        if (timer_elapsed(frame_at) < RGB_MATRIX_LED_FLUSH_LIMIT) return;
        frame_at = timer_read();
        phase += (uint16_t)rgb_matrix_config.speed + 32;
        frame_phase = phase >> 8;
        frame_mode = suspended || !rgb_matrix_config.enable ? RGB_MATRIX_NONE : rgb_matrix_config.mode;
        frame_hue = rgb_matrix_config.hsv.h;
        frame_sat = rgb_matrix_config.hsv.s;
        frame_val = rgb_matrix_config.hsv.v;
        frame_flags = rgb_matrix_config.flags;
        if (frame_mode == RGB_MATRIX_BREATHING) {
            frame_val = ((uint16_t)frame_val * sine8(frame_phase - 64)) >> 8;
#ifdef USE_CIE1931_CURVE
            frame_val = breathing_cie(frame_val);
#endif
        }
        led_index = 0;
        rendering = true;
    }
    end = led_index + 8;
    if (end > RGB_MATRIX_LED_COUNT) end = RGB_MATRIX_LED_COUNT;
    while (led_index < end) {
        if (!frame_mode || !(LED_FLAG_KEYLIGHT & frame_flags)) {
            rgb_matrix_set_color(led_index, 0, 0, 0);
        } else {
            if (frame_mode == RGB_MATRIX_VIALRGB_DIRECT) {
                hsv = g_direct_mode_colors[led_index];
            } else {
                hsv.h = frame_hue;
                hsv.s = frame_sat;
                hsv.v = frame_val;
                if (frame_mode == RGB_MATRIX_CYCLE_ALL) hsv.h += frame_phase;
                if (frame_mode == RGB_MATRIX_CYCLE_LEFT_RIGHT) hsv.h += ak820_led_points[led_index].x - frame_phase;
                if (frame_mode == RGB_MATRIX_SOLID_REACTIVE_SIMPLE) {
                    /* Four speed bands select 2048/1024/512/256 ms. */
                    uint8_t shift = 7 - (rgb_matrix_config.speed >> 6);
                    uint8_t duration = 1 << shift;
                    uint8_t age = reactive_age[led_index];
                    hsv.v = age >= duration ? frame_val : ((uint16_t)frame_val * age) >> shift;
                }
            }
            /* This model-large local is XDATA. Pass a two-byte typed output
             * pointer instead of SDCC's generic aggregate-return pointer. */
#ifdef USE_CIE1931_CURVE
            hsv_to_rgb_into(hsv, frame_mode != RGB_MATRIX_BREATHING, &rgb);
#else
            hsv_to_rgb_into(hsv, false, &rgb);
#endif
            rgb_matrix_set_color(led_index, rgb.r, rgb.g, rgb.b);
        }
        ++led_index;
    }
    if (led_index == RGB_MATRIX_LED_COUNT) {
        rgb_matrix_driver.flush();
        rendering = false;
    }
}

void process_rgb_matrix(uint8_t row, uint8_t col, bool pressed) {
    uint8_t i, slot;
    if (!pressed || suspended || !rgb_matrix_config.enable ||
        rgb_matrix_config.mode != RGB_MATRIX_SOLID_REACTIVE_SIMPLE || row >= MATRIX_ROWS || col >= MATRIX_COLS) return;
    age_reactive();
    slot = row * MATRIX_COLS + col;
    for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
        if (ak820_rgb_slots[i] == slot) {
            reactive_age[i] = 128 >> (rgb_matrix_config.speed >> 6);
            return;
        }
    }
}

void rgb_matrix_set_suspend_state(bool state) {
    suspended = state;
    rendering = false;
    clear_reactive();
    if (state) {
        rgb_matrix_set_color_all(0, 0, 0);
        rgb_matrix_driver.flush();
    }
}

bool rgb_matrix_get_suspend_state(void) { return suspended; }
uint8_t rgb_matrix_is_enabled(void) { return rgb_matrix_config.enable; }
uint8_t rgb_matrix_get_mode(void) { return rgb_matrix_config.mode; }
HSV rgb_matrix_get_hsv(void) { return rgb_matrix_config.hsv; }
uint8_t rgb_matrix_get_hue(void) { return rgb_matrix_config.hsv.h; }
uint8_t rgb_matrix_get_sat(void) { return rgb_matrix_config.hsv.s; }
uint8_t rgb_matrix_get_val(void) { return rgb_matrix_config.hsv.v; }
uint8_t rgb_matrix_get_speed(void) { return rgb_matrix_config.speed; }
led_flags_t rgb_matrix_get_flags(void) { return rgb_matrix_config.flags; }

void rgb_matrix_toggle_noeeprom(void) { rgb_matrix_config.enable ^= 1; rendering = false; clear_reactive(); }
void rgb_matrix_enable_noeeprom(void) { if (!rgb_matrix_config.enable) clear_reactive(); rgb_matrix_config.enable = 1; rendering = false; }
void rgb_matrix_disable_noeeprom(void) { rgb_matrix_config.enable = 0; rendering = false; clear_reactive(); }
void rgb_matrix_mode_noeeprom(uint8_t mode) {
    if (!mode || mode >= RGB_MATRIX_EFFECT_MAX) return;
    if (mode != rgb_matrix_config.mode) clear_reactive();
    rgb_matrix_config.mode = mode;
    rendering = false;
}
void rgb_matrix_step_noeeprom(void) {
    rgb_matrix_mode_noeeprom(rgb_matrix_config.mode + 1 >= RGB_MATRIX_EFFECT_MAX ? 1 : rgb_matrix_config.mode + 1);
}
void rgb_matrix_step_reverse_noeeprom(void) {
    rgb_matrix_mode_noeeprom(rgb_matrix_config.mode <= 1 ? RGB_MATRIX_EFFECT_MAX - 1 : rgb_matrix_config.mode - 1);
}
void rgb_matrix_sethsv_noeeprom(uint16_t hue, uint8_t sat, uint8_t val) {
    rgb_matrix_config.hsv.h = hue;
    rgb_matrix_config.hsv.s = sat;
    rgb_matrix_config.hsv.v = val > RGB_MATRIX_MAXIMUM_BRIGHTNESS ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
}
void rgb_matrix_set_speed_noeeprom(uint8_t speed) { rgb_matrix_config.speed = speed; }
void rgb_matrix_set_flags_noeeprom(led_flags_t flags) { rgb_matrix_config.flags = flags; }

void rgb_matrix_increase_hue_noeeprom(void) { rgb_matrix_config.hsv.h += 8; }
void rgb_matrix_decrease_hue_noeeprom(void) { rgb_matrix_config.hsv.h -= 8; }
void rgb_matrix_increase_sat_noeeprom(void) { rgb_matrix_config.hsv.s = add_sat(rgb_matrix_config.hsv.s, 16); }
void rgb_matrix_decrease_sat_noeeprom(void) { rgb_matrix_config.hsv.s = sub_sat(rgb_matrix_config.hsv.s, 16); }
void rgb_matrix_increase_val_noeeprom(void) {
    uint8_t val = add_sat(rgb_matrix_config.hsv.v, 16);
    rgb_matrix_config.hsv.v = val > RGB_MATRIX_MAXIMUM_BRIGHTNESS ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
}
void rgb_matrix_decrease_val_noeeprom(void) { rgb_matrix_config.hsv.v = sub_sat(rgb_matrix_config.hsv.v, 16); }
void rgb_matrix_increase_speed_noeeprom(void) { rgb_matrix_config.speed = add_sat(rgb_matrix_config.speed, 16); }
void rgb_matrix_decrease_speed_noeeprom(void) { rgb_matrix_config.speed = sub_sat(rgb_matrix_config.speed, 16); }

#define PERSIST_WRAPPER(name) void name(void) { name##_noeeprom(); mark_dirty(); }
PERSIST_WRAPPER(rgb_matrix_toggle)
PERSIST_WRAPPER(rgb_matrix_enable)
PERSIST_WRAPPER(rgb_matrix_disable)
PERSIST_WRAPPER(rgb_matrix_step)
PERSIST_WRAPPER(rgb_matrix_step_reverse)
PERSIST_WRAPPER(rgb_matrix_increase_hue)
PERSIST_WRAPPER(rgb_matrix_decrease_hue)
PERSIST_WRAPPER(rgb_matrix_increase_sat)
PERSIST_WRAPPER(rgb_matrix_decrease_sat)
PERSIST_WRAPPER(rgb_matrix_increase_val)
PERSIST_WRAPPER(rgb_matrix_decrease_val)
PERSIST_WRAPPER(rgb_matrix_increase_speed)
PERSIST_WRAPPER(rgb_matrix_decrease_speed)
#undef PERSIST_WRAPPER

void rgb_matrix_mode(uint8_t mode) { rgb_matrix_mode_noeeprom(mode); mark_dirty(); }
void rgb_matrix_sethsv(uint16_t hue, uint8_t sat, uint8_t val) { rgb_matrix_sethsv_noeeprom(hue, sat, val); mark_dirty(); }
void rgb_matrix_set_speed(uint8_t speed) { rgb_matrix_set_speed_noeeprom(speed); mark_dirty(); }
void rgb_matrix_set_flags(led_flags_t flags) { rgb_matrix_set_flags_noeeprom(flags); mark_dirty(); }
