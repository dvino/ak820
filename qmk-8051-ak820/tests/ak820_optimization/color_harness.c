/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdio.h>
#include "color.h"
#define PROGMEM
#define pgm_read_byte(p) (*(const uint8_t *)(p))
/* TABLE */
/* ACTUAL */
/* REFERENCE */
int main(void) {
    for (unsigned cie = 0; cie < 2; ++cie)
        for (unsigned h = 0; h <= UINT8_MAX; ++h)
            for (unsigned s = 0; s <= UINT8_MAX; ++s)
                for (unsigned v = 0; v <= UINT8_MAX; ++v) {
                    HSV hsv = {.h = h, .s = s, .v = v};
                    RGB a = hsv_to_rgb_impl(hsv, cie), b = rc4_hsv_to_rgb_impl(hsv, cie);
                    if (a.r != b.r || a.g != b.g || a.b != b.b) {
                        fprintf(stderr, "HSV mismatch %u,%u,%u cie%u: %u,%u,%u != %u,%u,%u\n", h,s,v,cie,a.r,a.g,a.b,b.r,b.g,b.b);
                        return 1;
                    }
                }
    puts("PASS: all 16777216 HSV colors, with and without CIE (33554432 cases), exactly match RC4.");
}
