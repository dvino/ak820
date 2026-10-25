/* Copyright 2017 Jason Williams
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

#include "color.h"
#include "led_tables.h"
#include "progmem.h"
#include "util.h"

#if defined(AK820_BOARD) && !defined(AK820_FULL_CIE)
#    define CIE_INDEX(v) ((v) >> 3)
#else
#    define CIE_INDEX(v) (v)
#endif

/* Exact 8x8 unsigned product high byte. SDCC widens explicit uint16_t
 * products to its __mulint ABI, so use the native 8051 instruction here. */
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
static uint8_t mulhi8(uint8_t x, uint8_t y) __naked {
    x; y;
    __asm
        mov b,dpl
        mov dptr,#_mulhi8_PARM_2
        movx a,@dptr
        mul ab
        mov dpl,b
        ret
    __endasm;
}
#else
static uint8_t mulhi8(uint8_t x, uint8_t y) {
    return ((uint16_t)x * y) >> 8;
}
#endif

#if defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
/* Capture each needed HSV component before conversion or output writes. */
void hsv_to_rgb_into(const HSV __xdata *input, bool use_cie, RGB __xdata *output) {
#elif defined(AK820_BOARD)
void hsv_to_rgb_into(HSV hsv, bool use_cie, RGB __xdata *output) {
#else
RGB hsv_to_rgb_impl(HSV hsv, bool use_cie) {
#endif
    RGB      rgb;
    uint8_t  region, remainder, p, q, t;
#if defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
    uint8_t h;
    uint8_t s = input->s, v = input->v;
#else
    uint8_t h;
    uint8_t s = hsv.s, v = hsv.v;
#endif

    if (s == 0) {
#ifdef USE_CIE1931_CURVE
        if (use_cie) {
            rgb.r = rgb.g = rgb.b = pgm_read_byte(&CIE1931_CURVE[CIE_INDEX(v)]);
        } else {
            rgb.r = v;
            rgb.g = v;
            rgb.b = v;
        }
#else
        rgb.r = v;
        rgb.g = v;
        rgb.b = v;
#endif
#ifdef AK820_BOARD
        *output = rgb;
        return;
#else
        return rgb;
#endif
    }

#if defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
    h = input->h;
#else
    h = hsv.h;
#endif
#ifdef USE_CIE1931_CURVE
    if (use_cie) {
        v = pgm_read_byte(&CIE1931_CURVE[CIE_INDEX(v)]);
    }
#endif

    uint16_t scaled = (uint16_t)h * 6;
    region = (scaled + 1 + (scaled >> 8)) >> 8;
    remainder = (h * 2 - region * 85) * 3;

    p = mulhi8(v, 255 - s);
    q = mulhi8(v, 255 - mulhi8(s, remainder));
    t = mulhi8(v, 255 - mulhi8(s, 255 - remainder));

    switch (region) {
        case 6:
        case 0:
            rgb.r = v;
            rgb.g = t;
            rgb.b = p;
            break;
        case 1:
            rgb.r = q;
            rgb.g = v;
            rgb.b = p;
            break;
        case 2:
            rgb.r = p;
            rgb.g = v;
            rgb.b = t;
            break;
        case 3:
            rgb.r = p;
            rgb.g = q;
            rgb.b = v;
            break;
        case 4:
            rgb.r = t;
            rgb.g = p;
            rgb.b = v;
            break;
        default:
            rgb.r = v;
            rgb.g = p;
            rgb.b = q;
            break;
    }

#ifdef AK820_BOARD
    *output = rgb;
#else
    return rgb;
#endif
}

#ifdef AK820_BOARD
/* Keep QMK's public aggregate API for other users. AK820's renderer uses the
 * typed output directly, avoiding SDCC's three-byte generic return pointer. */
RGB hsv_to_rgb_impl(HSV hsv, bool use_cie) {
    RGB rgb;
#if defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
    hsv_to_rgb_into(&hsv, use_cie, &rgb);
#else
    hsv_to_rgb_into(hsv, use_cie, &rgb);
#endif
    return rgb;
}
#endif

RGB hsv_to_rgb(HSV hsv) {
    // SDCC's MCS51 aggregate-return forwarding omits the caller's result copy
    // for "return hsv_to_rgb_impl(...)". Return a named value instead.
    RGB rgb;
#ifdef USE_CIE1931_CURVE
    rgb = hsv_to_rgb_impl(hsv, true);
#else
    rgb = hsv_to_rgb_impl(hsv, false);
#endif
    return rgb;
}

RGB hsv_to_rgb_nocie(HSV hsv) {
    RGB rgb;
    rgb = hsv_to_rgb_impl(hsv, false);
    return rgb;
}

#ifdef RGBW
void convert_rgb_to_rgbw(LED_TYPE *led) {
    // Determine lowest value in all three colors, put that into
    // the white channel and then shift all colors by that amount
    led->w = MIN(led->r, MIN(led->g, led->b));
    led->r -= led->w;
    led->g -= led->w;
    led->b -= led->w;
}
#endif
