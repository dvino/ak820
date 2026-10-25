// SPDX-License-Identifier: GPL-2.0-or-later
/* Separate translation unit is mandatory: R2-R7 are caller scratch.
 * The child eeprom_read_byte must preserve R0-R7. No private pushes here.
 * Bank zero is required by the builder/startup contract; exact linked image
 * caller/helper and IRQ stack qualification remains mandatory. */
#if defined(AK820_NVM_READ_BLOCK_ASM)
#if !defined(AK820_BOARD) || !defined(__SDCC_mcs51) || !defined(__SDCC_MODEL_LARGE)
#error AK820 read kernel requires the AK820 MCS51 large model
#endif
#if defined(__SDCC_STACK_AUTO) || defined(__SDCC_USE_XSTACK) || defined(SDCC_PARMS_IN_BANK1) || defined(__SDCC_PARMS_IN_BANK1) || defined(__SDCC_ALL_CALLEE_SAVES)
#error AK820 read kernel requires fixed XDATA parameters and caller-clobbered registers
#endif
#if !defined(__SDCCCALL) || __SDCCCALL != 0
#error AK820 read kernel requires calling convention zero
#endif
#if !defined(AK820_READ_HOOK_PRESERVES_RN) || AK820_READ_HOOK_PRESERVES_RN != 1
#error AK820 read kernel requires the build-owned bank-zero scalar preservation assertion
#endif
#include "ak820_nvm.h"
_Static_assert(sizeof(void *) == 3 && sizeof(void __xdata *) == 2 && sizeof(size_t) == 2 && sizeof(uint16_t) == 2, "pinned large-model pointer and size ABI");
_Static_assert(AK820_NVM_SIZE == 0x2800u && AK820_NVM_BASE == 0xc700u && AK820_FLASH_PAGE == 64u, "fixed scalar layout");
void ak820_eeprom_read_block_xdata(void AK820_XDATA *buf, const void *addr, size_t len) __naked {
    buf; addr; len;
    __asm
        mov r4,dpl
        mov r5,dph
        mov dptr,#_ak820_eeprom_read_block_xdata_PARM_2
        movx a,@dptr
        mov r2,a
        inc dptr
        movx a,@dptr
        mov r3,a
        mov dptr,#_ak820_eeprom_read_block_xdata_PARM_3
        movx a,@dptr
        mov r6,a
        inc dptr
        movx a,@dptr
        mov r7,a
00001$:
        mov a,r6
        orl a,r7
        jz 00005$
        mov a,r6
        jnz 00002$
        dec r7
00002$:
        dec r6
        mov a,r3
        clr c
        subb a,#0x28
        jnc 00003$
        mov dpl,r2
        mov dph,r3
        mov b,#0
        lcall _eeprom_read_byte
        mov a,dpl
        inc r2
        cjne r2,#0,00004$
        inc r3
        sjmp 00004$
00003$:
        clr a
00004$:
        mov dpl,r4
        mov dph,r5
        movx @dptr,a
        inc r4
        cjne r4,#0,00001$
        inc r5
        sjmp 00001$
00005$:
        ret
    __endasm;
}
#endif
