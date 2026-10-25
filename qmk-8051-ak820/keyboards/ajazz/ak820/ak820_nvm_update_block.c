// SPDX-License-Identifier: GPL-2.0-or-later
/* Separate TU: caller-scratch R2-R7, A, B, DPTR and arithmetic flags.
 * Bank zero, fixed XDATA parameter slots; no recursion or IRQ reentry.
 * Two private stack bytes retain original buf. Scalar call adds its return
 * frame and its own stack; mismatch tail-dispatches after removing private bytes.
 * Each scalar read precedes its source read. Address arithmetic wraps at 16 bits.
 * Original generic tag and length are copied unchanged only on first mismatch.
 * Equal/empty requests never enter the writer or flush. */
#if defined(AK820_NVM_UPDATE_BLOCK_ASM)
#if !defined(AK820_BOARD) || !defined(__SDCC_mcs51) || !defined(__SDCC_MODEL_LARGE)
#error AK820 update kernel requires the AK820 MCS51 large model
#endif
#if defined(__SDCC_STACK_AUTO) || defined(__SDCC_USE_XSTACK) || defined(SDCC_PARMS_IN_BANK1) || defined(__SDCC_PARMS_IN_BANK1) || defined(__SDCC_ALL_CALLEE_SAVES)
#error AK820 update kernel requires fixed XDATA parameters and caller-clobbered registers
#endif
#if !defined(__SDCCCALL) || __SDCCCALL != 0
#error AK820 update kernel requires calling convention zero
#endif
#if !defined(AK820_READ_HOOK_PRESERVES_RN) || AK820_READ_HOOK_PRESERVES_RN != 1
#error AK820 update kernel requires the build-owned bank-zero scalar preservation assertion
#endif
#include "ak820_nvm.h"
_Static_assert(sizeof(void *) == 3 && sizeof(void __xdata *) == 2 && sizeof(size_t) == 2 && sizeof(uint16_t) == 2, "pinned large-model pointer and size ABI");
_Static_assert(AK820_NVM_SIZE == 0x2800u && AK820_NVM_BASE == 0xc700u && AK820_FLASH_PAGE == 64u, "fixed scalar layout");
void ak820_eeprom_update_block_xdata(const void AK820_XDATA *buf, void *addr, size_t len) __naked {
    buf; addr; len;
    __asm
        push dpl
        push dph
        mov r4,dpl
        mov r5,dph
        mov dptr,#_ak820_eeprom_update_block_xdata_PARM_2
        movx a,@dptr
        mov r2,a
        inc dptr
        movx a,@dptr
        mov r3,a
        mov dptr,#_ak820_eeprom_update_block_xdata_PARM_3
        movx a,@dptr
        mov r6,a
        inc dptr
        movx a,@dptr
        mov r7,a
00001$:
        mov a,r6
        orl a,r7
        jz 00005$
        mov dpl,r2
        mov dph,r3
        mov b,#0
        lcall _eeprom_read_byte
        mov b,dpl
        mov dpl,r4
        mov dph,r5
        movx a,@dptr
        cjne a,b,00006$
        inc r4
        cjne r4,#0,00002$
        inc r5
00002$:
        inc r2
        cjne r2,#0,00003$
        inc r3
00003$:
        mov a,r6
        jnz 00004$
        dec r7
00004$:
        dec r6
        sjmp 00001$
00005$:
        pop dph
        pop dpl
        ret
00006$:
        mov dptr,#(_ak820_eeprom_update_block_xdata_PARM_2+0)
        movx a,@dptr
        mov dptr,#(_ak820_eeprom_write_block_xdata_PARM_2+0)
        movx @dptr,a
        mov dptr,#(_ak820_eeprom_update_block_xdata_PARM_2+1)
        movx a,@dptr
        mov dptr,#(_ak820_eeprom_write_block_xdata_PARM_2+1)
        movx @dptr,a
        mov dptr,#(_ak820_eeprom_update_block_xdata_PARM_2+2)
        movx a,@dptr
        mov dptr,#(_ak820_eeprom_write_block_xdata_PARM_2+2)
        movx @dptr,a
        mov dptr,#(_ak820_eeprom_update_block_xdata_PARM_3+0)
        movx a,@dptr
        mov dptr,#(_ak820_eeprom_write_block_xdata_PARM_3+0)
        movx @dptr,a
        mov dptr,#(_ak820_eeprom_update_block_xdata_PARM_3+1)
        movx a,@dptr
        mov dptr,#(_ak820_eeprom_write_block_xdata_PARM_3+1)
        movx @dptr,a
        pop dph
        pop dpl
        ljmp _ak820_eeprom_write_block_xdata
    __endasm;
}
#endif
