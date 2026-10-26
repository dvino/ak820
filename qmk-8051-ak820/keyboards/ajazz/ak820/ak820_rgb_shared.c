/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Small RGB leaves occupy the reserved application CODE window below 0x3000. */
#ifdef __SDCC_mcs51
#    pragma codeseg AK820LOW
#endif
#include "ak820_board.h"
#include "vialrgb.h"

/* FastLED/QMK's piecewise sine approximation. The target leaf uses the same
 * eight coefficients and integer rounding, without large-model temporaries.
 * It clobbers only caller-saved A, B, DPTR and R5..R7 and uses no stack. */
#if defined(__SDCC_mcs51)
uint8_t ak820_breathing_wave(uint8_t theta) __naked {
    theta;
    __asm
        mov a,dpl
        mov r7,a
        jnb acc.6,00920$
        cpl a
00920$:
        anl a,#0x3f
        mov r6,a
        anl a,#0x0f
        mov r5,a
        mov a,r7
        jnb acc.6,00921$
        inc r5
00921$:
        mov a,r6
        swap a
        anl a,#3
        add a,acc
        mov r6,a
        mov dptr,#00923$
        movc a,@a+dptr
        xch a,r6
        inc a
        movc a,@a+dptr
        mov b,r5
        mul ab
        swap a
        anl a,#0x0f
        mov r5,a
        mov a,b
        swap a
        orl a,r5
        add a,r6
        mov r6,a
        mov a,r7
        mov c,acc.7
        mov a,r6
        jnc 00922$
        cpl a
        inc a
00922$:
        add a,#128
        mov dpl,a
        ret
00923$:
        .db 0,49,49,41
        .db 90,27,117,10
    __endasm;
}
#else
uint8_t ak820_breathing_wave(uint8_t theta) {
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
#endif

#ifndef VIALRGB_NO_DIRECT
void ak820_direct_cancel(void) {
    /* A published palette is retained. Only pending work is cancelled. */
    if (ak820_direct_state && ak820_direct_state < AK820_DIRECT_DONE)
        ak820_direct_state = AK820_DIRECT_CANCELLED;
}

#endif
