// SPDX-License-Identifier: GPL-2.0-or-later
/* Fixed-layout AK820 key/encoder EEPROM access. Keep this in a separate TU:
 * SDCC does not infer the register clobbers inside these naked definitions. */
#if defined(AK820_KEYMAP_WORDS_ASM) && defined(AK820_BOARD) && defined(__SDCC_mcs51) && defined(__SDCC_MODEL_LARGE)
#if defined(__SDCC_STACK_AUTO) || defined(__SDCC_USE_XSTACK)
#    error AK820 word access requires fixed XDATA parameter slots, without automatic or external stack parameters
#endif
#if defined(SDCC_PARMS_IN_BANK1) || defined(__SDCC_PARMS_IN_BANK1)
#    error AK820 word access requires default large-model parameter passing, not bank-one parameters
#endif
#if defined(__SDCC_ALL_CALLEE_SAVES)
#    error AK820 word access APIs require caller-clobbered registers
#endif
#if !defined(__SDCCCALL) || __SDCCCALL != 0
#    error AK820 word access requires the pinned MCS51 calling convention zero
#endif
#include "dynamic_keymap.h"
#include "eeprom.h"
#include "encoder.h"

#ifndef ENCODER_MAP_ENABLE
#    error AK820 keymap word kernel requires encoder maps
#endif
_Static_assert(DYNAMIC_KEYMAP_LAYER_COUNT == 6 && MATRIX_ROWS == 16 && MATRIX_COLS == 8,
               "AK820 keymap coordinate layout");
_Static_assert(NUM_ENCODERS == 1, "AK820 encoder coordinate layout");
_Static_assert(DYNAMIC_KEYMAP_EEPROM_ADDR == 0x0040u, "AK820 keymap base");
_Static_assert(DYNAMIC_KEYMAP_EEPROM_ADDR + DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2u == 0x0640u,
               "AK820 encoder base");
_Static_assert(sizeof(uint8_t) == 1 && sizeof(uint16_t) == 2 && sizeof(bool) == 1 && sizeof(void *) == 3,
               "SDCC large-model word ABI");

/* Bank-zero ABI: R2/R3 hold the logical EEPROM address and R5/R6 hold the
 * word across native hooks. Both hooks must preserve every R0..R7 register.
 * The audited builder emits the ABI macro only when both hooks are in its
 * common callee-saves list and none of these four public APIs is in that list.
 * The naked scalar read independently preserves every R register. The C update
 * wrapper preserves used registers and saves all registers across unlisted
 * children. A/B/DPTR/arithmetic flags remain scratch.
 *
 * No XDATA frame or mutable working context exists. The inspected NVM hook
 * closure and selected IRQ roots cannot reenter keymap access. Mock nested
 * entry is nevertheless safe when the hook's callee-saves ABI protects the
 * outer register context. Exact object/image clobber and stack checks remain
 * required; this macro is a build-owned assertion, not a user feature switch.
 */
#if !defined(AK820_WORD_HOOKS_PRESERVE_RN) || AK820_WORD_HOOKS_PRESERVE_RN != 1
#    error AK820 word access requires the audited register-preserving native hook ABI
#endif
uint16_t dynamic_keymap_get_keycode(uint8_t a,uint8_t b,uint8_t c) __naked {
__asm
mov r2,dpl
mov dptr,#_dynamic_keymap_get_keycode_PARM_2
movx a,@dptr
mov r3,a
mov dptr,#_dynamic_keymap_get_keycode_PARM_3
movx a,@dptr
mov r4,a
mov r0,#0
ljmp _ak820_keymap_word_read
__endasm;
}
void dynamic_keymap_set_keycode(uint8_t a,uint8_t b,uint8_t c,uint16_t key) __naked {
__asm
mov r2,dpl
mov dptr,#_dynamic_keymap_set_keycode_PARM_2
movx a,@dptr
mov r3,a
mov dptr,#_dynamic_keymap_set_keycode_PARM_3
movx a,@dptr
mov r4,a
mov dptr,#_dynamic_keymap_set_keycode_PARM_4
movx a,@dptr
mov r5,a
inc dptr
movx a,@dptr
mov r6,a
mov r0,#0
ljmp _ak820_keymap_word_write
__endasm;
}
uint16_t dynamic_keymap_get_encoder(uint8_t a,uint8_t b,bool c) __naked {
__asm
mov r2,dpl
mov dptr,#_dynamic_keymap_get_encoder_PARM_2
movx a,@dptr
mov r3,a
mov dptr,#_dynamic_keymap_get_encoder_PARM_3
movx a,@dptr
mov r4,a
mov r0,#2
ljmp _ak820_keymap_word_read
__endasm;
}
void dynamic_keymap_set_encoder(uint8_t a,uint8_t b,bool c,uint16_t key) __naked {
__asm
mov r2,dpl
mov dptr,#_dynamic_keymap_set_encoder_PARM_2
movx a,@dptr
mov r3,a
mov dptr,#_dynamic_keymap_set_encoder_PARM_3
movx a,@dptr
mov r4,a
mov dptr,#_dynamic_keymap_set_encoder_PARM_4
movx a,@dptr
mov r5,a
inc dptr
movx a,@dptr
mov r6,a
mov r0,#2
ljmp _ak820_keymap_word_write
__endasm;
}
/* Geometry helper returns C=0 with R2/R3 address, C=1 when invalid.
 * It returns before native I/O; getter control flow cannot reach a writer. */
static void ak820_keymap_word_address(void) __naked {
__asm
 mov a,r0
 anl a,#2
 jnz ak820_word_encoder
 mov a,r2
 clr c
 subb a,#6
 jnc ak820_word_invalid
 mov a,r3
 clr c
 subb a,#16
 jnc ak820_word_invalid
 mov a,r4
 clr c
 subb a,#8
 jnc ak820_word_invalid
 mov a,r3
 swap a
 mov r7,a
 mov a,r4
 add a,acc
 add a,r7
 add a,#0x40
 mov r3,0x02
 mov r2,a
 clr a
 addc a,r3
 mov r3,a
 clr c
 ret
ak820_word_invalid:
 setb c
 ret
ak820_word_encoder:
 mov a,r2
 clr c
 subb a,#6
 jnc ak820_word_invalid
 mov a,r3
 jnz ak820_word_invalid
 mov a,r2
 rl a
 rl a
 mov r2,a
 mov a,r4
 jnz ak820_word_clockwise
 mov a,r2
 add a,#2
 mov r2,a
ak820_word_clockwise:
 mov a,r2
 add a,#0x40
 mov r2,a
 mov r3,#6
 clr c
 ret
__endasm;
}
static void ak820_keymap_word_read(void) __naked {
__asm
 lcall _ak820_keymap_word_address
 jc ak820_word_read_invalid
 mov dpl,r2
 mov dph,r3
 mov b,#0
 lcall _eeprom_read_byte
 mov r6,dpl
 inc r2
 cjne r2,#0,ak820_word_read_second
 inc r3
ak820_word_read_second:
 mov dpl,r2
 mov dph,r3
 mov b,#0
 lcall _eeprom_read_byte
 mov dph,r6
 ret
ak820_word_read_invalid:
 mov dptr,#0
 ret
__endasm;
}
static void ak820_keymap_word_write(void) __naked {
__asm
 lcall _ak820_keymap_word_address
 jc ak820_word_write_invalid
 mov dptr,#_eeprom_update_byte_PARM_2
 mov a,r6
 movx @dptr,a
 mov dpl,r2
 mov dph,r3
 mov b,#0
 lcall _eeprom_update_byte
 inc r2
 cjne r2,#0,ak820_word_write_second
 inc r3
ak820_word_write_second:
 mov dptr,#_eeprom_update_byte_PARM_2
 mov a,r5
 movx @dptr,a
 mov dpl,r2
 mov dph,r3
 mov b,#0
 ljmp _eeprom_update_byte
ak820_word_write_invalid:
 ret
__endasm;
}

#endif
