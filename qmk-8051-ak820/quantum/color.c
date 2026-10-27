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

#if defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
/* SDCC large-model ABI: input is in DPTR; the remaining arguments are
 * XDATA parameter slots. Read all three input bytes before writing output,
 * so in-place conversion is supported. R0-R7, A, B and DPTR are caller-saved.
 * The selected region needs only one ramp (q for odd regions, t for even).
 * Native MUL keeps the exact high-byte arithmetic of the portable version.
 */
void hsv_to_rgb_into(const HSV __xdata *input, bool use_cie, RGB __xdata *output) __naked {
    input; use_cie; output;
    __asm
        movx a,@dptr
        mov r7,a
        inc dptr
        movx a,@dptr
        mov r6,a
        inc dptr
        movx a,@dptr
        mov r5,a
    __endasm;
#ifdef USE_CIE1931_CURVE
    __asm
        mov dptr,#_hsv_to_rgb_into_PARM_2
        movx a,@dptr
        jz 01001$
        mov a,r5
    __endasm;
#    if !defined(AK820_FULL_CIE)
    __asm
        rr a
        rr a
        rr a
        anl a,#0x1f
    __endasm;
#    endif
    __asm
        mov dptr,#_CIE1931_CURVE
        movc a,@a+dptr
        mov r5,a
01001$:
    __endasm;
#endif
    __asm
        mov a,r6
        jnz 01002$
        mov ar2,r5
        mov ar3,r5
        ljmp 01010$
01002$:
        ; region = (6*h + 1 + high(6*h)) >> 8
        mov a,r7
        mov b,#6
        mul ab
        add a,#1
        add a,b
        mov a,b
        addc a,#0
        mov r4,a
        ; remainder = (2*h - 85*region)*3, modulo 256
        mov b,#85
        mul ab
        mov r3,a
        mov a,r7
        add a,r7
        clr c
        subb a,r3
        mov b,#3
        mul ab
        mov r3,a
        ; p = high(v*(255-s))
        mov a,r6
        cpl a
        mov b,r5
        mul ab
        mov r2,b
        ; odd regions use remainder; even regions use its complement
        mov a,r4
        jb acc.0,01003$
        mov a,r3
        cpl a
        mov r3,a
01003$:
        mov a,r3
        mov b,r6
        mul ab
        mov a,b
        cpl a
        mov b,r5
        mul ab
        mov r3,b
        ; Permute (v, ramp, p) to RGB using swaps.
        mov a,r4
        jz 01010$
        cjne a,#6,01004$
        sjmp 01010$
01004$:
        dec a
        jz 01011$
        dec a
        jz 01012$
        dec a
        jz 01013$
        dec a
        jz 01014$
        ; region 5: (v,p,q)
        mov a,r2
        xch a,r3
        mov r2,a
        sjmp 01010$
01011$: ; region 1: (q,v,p)
        mov a,r5
        xch a,r3
        mov r5,a
        sjmp 01010$
01012$: ; region 2: (p,v,t)
        mov a,r5
        xch a,r3
        xch a,r2
        mov r5,a
        sjmp 01010$
01013$: ; region 3: (p,q,v)
        mov a,r5
        xch a,r2
        mov r5,a
        sjmp 01010$
01014$: ; region 4: (t,p,v)
        mov a,r5
        xch a,r2
        xch a,r3
        mov r5,a
01010$:
        ; R5 = red, R3 = green, R2 = blue
        mov dptr,#_hsv_to_rgb_into_PARM_3
        movx a,@dptr
        mov r0,a
        inc dptr
        movx a,@dptr
        mov dph,a
        mov dpl,r0
    __endasm;
#    if WS2812_BYTE_ORDER == WS2812_BYTE_ORDER_GRB
    __asm
        mov a,r3
        movx @dptr,a
        inc dptr
        mov a,r5
        movx @dptr,a
        inc dptr
        mov a,r2
    __endasm;
#    elif WS2812_BYTE_ORDER == WS2812_BYTE_ORDER_RGB
    __asm
        mov a,r5
        movx @dptr,a
        inc dptr
        mov a,r3
        movx @dptr,a
        inc dptr
        mov a,r2
    __endasm;
#    else
    __asm
        mov a,r2
        movx @dptr,a
        inc dptr
        mov a,r3
        movx @dptr,a
        inc dptr
        mov a,r5
    __endasm;
#    endif
    __asm
        movx @dptr,a
        ret
    __endasm;
}
#else
static uint8_t mulhi8(uint8_t x, uint8_t y) {
    return ((uint16_t)x * y) >> 8;
}

#if defined(AK820_BOARD)
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

#endif /* portable conversion */

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
