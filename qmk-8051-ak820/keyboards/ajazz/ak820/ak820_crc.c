// SPDX-License-Identifier: GPL-2.0-or-later
#include "ak820_crc.h"

#if defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
/* SDCC mcs51 default register bank 0, non-reentrant ABI: pointer in DPTR,
 * length in the compiler-allocated XDATA parameter slot, result in DPTR. R2-R7,
 * ACC and arithmetic PSW flags are caller-saved scratch (also clobbered by C).
 * R0/R1/B are untouched. No calls or additional stack bytes. */
uint16_t ak820_crc16(const uint8_t AK820_XDATA *data, uint8_t length) __naked {
    data; length;
    __asm
        mov r6,dpl
        mov r7,dph
        mov dptr,#_ak820_crc16_PARM_2
        movx a,@dptr
        mov r2,a
        mov dpl,r6
        mov dph,r7
        mov r4,#0xff
        mov r5,#0xff
        mov a,r2
        jz 00004$
00001$:
        movx a,@dptr
        inc dptr
        xrl a,r5
        mov r5,a
        mov r3,#8
00002$:
        mov a,r4
        add a,acc
        mov r4,a
        mov a,r5
        rlc a
        mov r5,a
        jnc 00003$
        mov a,r4
        xrl a,#0x21
        mov r4,a
        mov a,r5
        xrl a,#0x10
        mov r5,a
00003$:
        djnz r3,00002$
        djnz r2,00001$
00004$:
        mov dpl,r4
        mov dph,r5
        ret
    __endasm;
}
#else
uint16_t ak820_crc16(const uint8_t AK820_XDATA *data, uint8_t length) {
    uint8_t hi = 0xffu, lo = 0xffu;
    while (length--) {
        uint8_t bit;
        hi ^= *data++;
        for (bit = 0; bit != 8; ++bit) {
            uint8_t carry = hi & 0x80u;
            hi = (uint8_t)((hi << 1) | (lo >> 7));
            lo <<= 1;
            if (carry) {
                hi ^= 0x10u;
                lo ^= 0x21u;
            }
        }
    }
    return ((uint16_t)hi << 8) | lo;
}

#endif
