/* SPDX-License-Identifier: GPL-2.0-or-later
 * AK820 replacement for SDCC 4.4 crtxinit.asm.
 *
 * The generic CRT writes XISEG through MOVX @R0 and assumes that P2 selects
 * its high address byte. That is not a verified VS11K28A contract. Use the
 * same explicit 16-bit DPTR addressing as the OEM XDATA initialiser instead.
 * No P2 writes, short MOVX, dual-DPTR extension or initialized C storage is
 * required. The image entry disables IRQs and normalizes XBUS_AUX first.
 *
 * GSINIT3 is a fall-through CRT section: deliberately no RET. SDCC's GSINIT4
 * then clears XSEG and IRAM, followed by its ordinary GSINIT assignments.
 */
#if !defined(__SDCC_mcs51)
#    error "AK820 startup requires SDCC MCS51"
#endif

#pragma codeseg GSINIT3

void _mcs51_genXINIT(void) __naked {
    __asm
        .globl l_XINIT
        .globl s_XINIT
        .globl s_XISEG

        mov r1, #l_XINIT
        mov a, r1
        orl a, #(l_XINIT >> 8)
        jz 00002$
        mov r2, #((l_XINIT + 255) >> 8)
        mov r3, #s_XINIT
        mov r4, #(s_XINIT >> 8)
        mov r5, #s_XISEG
        mov r6, #(s_XISEG >> 8)
00001$:
        mov dpl, r3
        mov dph, r4
        clr a
        movc a, @a+dptr
        mov r7, a
        inc dptr
        mov r3, dpl
        mov r4, dph
        mov dpl, r5
        mov dph, r6
        mov a, r7
        movx @dptr, a
        inc dptr
        mov r5, dpl
        mov r6, dph
        djnz r1, 00001$
        djnz r2, 00001$
00002$:
    __endasm;
}
