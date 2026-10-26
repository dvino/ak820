#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

/* SPDX-License-Identifier: GPL-2.0-or-later
 *
 * AJAZZ AK820 VS11K28A board driver, reconstructed from the supplied OEM ROM
 * SHA256 03c6bd3351f272c855b9bc736d597170f694b5260b2001d1fc9cbfba8b382994.
 * The keyboard and RGB share pins: scanning is done during the LED controller's
 * blanking interrupt. A conventional QMK row-pin scanner must not run here.
 *
 * Native sources: clock 2FE2, init DC37, IRQ D5CE, DMA E274, selector E29D,
 * encoder EF80/99FC, RGB publication DD75. See the supplied ROM disassembly.
 */
#include "info_config.h"
#include "config.h"
#include "ak820_board.h"
#include "ch555.h"
#if defined(RGB_MATRIX_ENABLE) && !defined(VIALRGB_NO_DIRECT)
#    include "vialrgb.h"
void ak820_direct_publish_row(void) __naked;
#endif

#if !defined(__SDCC_mcs51)
#    error "AK820 board driver requires the SDCC MCS51 target"
#endif

#if defined(F_CPU) && F_CPU != 32000000
#    error "AK820 native LED/keyboard timing requires F_CPU=32000000"
#endif

/* Absolute allocations are not excluded from XSEG by SDCC: the linker must
 * place ordinary XDATA at >=0400 and keep USB FIFO1000..13FF reserved. */
volatile __xdata __at(AK820_LED_DMA_ADDRESS) uint8_t ak820_led_dma[AK820_LED_DMA_BYTES];
volatile __xdata uint8_t ak820_scan_rows[AK820_SCAN_ROWS];
volatile __xdata uint8_t ak820_scan_ready;
volatile __xdata uint8_t ak820_scan_sample;

#ifdef AK820_MATRIX_MASK
static const __code uint8_t ak820_matrix_mask[AK820_SCAN_ROWS] = AK820_MATRIX_MASK;
#endif

void ak820_clock_init(void) __naked {
    __asm
        mov 0xa1, #0x55
        mov 0xa1, #0xaa
        orl 0xb9, #0x80
        anl 0xb9, #0xbf
        mov 0xa1, #0x55
        mov 0xa1, #0xaa
        mov a, 0xb9
        anl a, #0xf8
        orl a, #0x06
        mov 0xb9, a
        clr a
        mov 0xa1, a
        ret
    __endasm;
}

void ak820_board_init(void) {
    uint16_t i;

    IE_PWM_I2C = 0;
    for (i = 0; i < AK820_LED_DMA_BYTES; ++i) {
        ak820_led_dma[i] = 0;
    }
    for (i = 0; i < AK820_SCAN_ROWS; ++i) {
        ak820_scan_rows[i] = 0;
    }
    ak820_scan_ready  = 0;
    ak820_scan_sample = 0;

    /* Native DC82..DC9A. The peripheral overrides common/PWM output modes. */
    P4 = P2 = P1 = P3 = P0 = 0xff;
    P1_MOD_OC = P2_MOD_OC = P4_MOD_OC = P3_MOD_OC = P0_MOD_OC = 0;

    LED_CTRL    = 0x01;
    LED_CYCLE   = 0x30;
    LED_FRAME   = 0x50;
    LED_DMA_H   = AK820_LED_DMA_ADDRESS >> 8;
    LED_DMA_L   = AK820_LED_DMA_ADDRESS & 0xff;
    LED_INT_ADJ = 0;
    LED_PWM_OE  = 0xff;
    LED_COMMON  = 0xff;
    LED_CTRL    = 0xfd;

    /* Native EF80: P7.0 and P7.1 input with pullups, not matrix common pins. */
    P7 = 0x03;

    LED_STATUS |= 0x40;
    IE_PWM_I2C = 1;
    LED_RED_ADJ = LED_GRE_ADJ = LED_BLU_ADJ = 0;
}

/* This is a normal loader callback. The immutable OEM IRQ wrapper saves ACC,
 * B, DPTR, PSW and R0..R7, selects bank0, calls the301E stub and executes RETI.
 * No C helper, static parameters or SDCC library routines run in this ISR.
 *
 * Preserve the native DMA read pattern and the exact key-input settling
 * sequence. The special LED DMA transfer must not be replaced by memcpy:
 * native E274 uses E_DIS + PSW.P and four groups of8 MOVX reads, with NOPs.
 */
void ak820_led_irq(void) __naked {
    __asm
        inc 0xa6
        mov a, 0xa6
        anl a, #0x0f
        mov r6, a
        jnz 00001$
        mov 0xa6, #0x10
        mov 0xc7, #0x02
        mov 0xc6, #0x00
00001$:
#if defined(RGB_MATRIX_ENABLE) && !defined(VIALRGB_NO_DIRECT)
        lcall _ak820_direct_publish_row
#endif
        lcall 00010$
#if defined(RGB_MATRIX_ENABLE) && !defined(VIALRGB_NO_DIRECT)
        ; Release staging only after the last row's native transfer.
        cjne r6, #0x0f, 00003$
        mov dptr, #_ak820_direct_state
        movx a, @dptr
        cjne a, #4, 00003$
        mov a, #5
        movx @dptr, a
00003$:
#endif

        ; Native D5ED..D617, only the sample XRAM address is relocated.
        mov 0xc1, #0xff
        mov 0xc2, #0xff
        nop
        nop
        mov dptr, #0x21d1
        movx a, @dptr
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        mov dptr, #_ak820_scan_sample
        mov a, 0xc0
        movx @dptr, a
        clr a
        mov 0xc2, a
        mov 0xc1, a
        mov 0xa7, #0xff
        mov 0xb0, #0xff
        mov 0x80, #0xff

        mov dptr, #_ak820_scan_sample
        movx a, @dptr
        cpl a
        mov r5, a
        mov dptr, #_ak820_scan_rows
        mov a, dpl
        add a, r6
        mov dpl, a
        clr a
        addc a, dph
        mov dph, a
        mov a, r5
        movx @dptr, a
        cjne r6, #0x0f, 00002$
        mov dptr, #_ak820_scan_ready
        mov a, #1
        movx @dptr, a
00002$:
        ret

        ; Native E274..E29D: the32 MOVX operations feed the peripheral DMA.
00010$:
        setb 0xae
        setb 0xd0
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        nop
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        nop
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        nop
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        movx a, @dptr
        clr 0xae

        ; Native E29D..E2E0, with the jump table relocated locally.
        mov a, 0xa6
        jbc 0xe4, 00011$
        anl a, #1
        inc a
        cpl a
        dec a
        anl 0xf1, a
        ret
00011$:
        ; The selector has sixteen entries even if the peripheral sets high bits.
        anl a, #0x0f
        mov r7, a
        add a, r7
        add a, r7
        mov dptr, #00012$
        jmp @a+dptr
00012$:
        clr 0x80
        ret
        clr 0x81
        ret
        clr 0x82
        ret
        clr 0x83
        ret
        clr 0x84
        ret
        clr 0x85
        ret
        clr 0x86
        ret
        clr 0x87
        ret
        clr 0xb0
        ret
        clr 0xb1
        ret
        clr 0xb2
        ret
        clr 0xb3
        ret
        clr 0xb4
        ret
        clr 0xb5
        ret
        clr 0xb6
        ret
        clr 0xb7
        ret
    __endasm;
}

#if defined(RGB_MATRIX_ENABLE) && !defined(VIALRGB_NO_DIRECT)
/* Inverse of AK820_RGB_SLOT_MAP, checked by linked tests. 255 means an
 * unmapped slot, including the independent C/W/OS indicators. */
static const __code uint8_t ak820_rgb_led_for_slot[128] = {
    0,14,29,44,58,72,255,255,1,15,30,45,255,73,255,255,
    2,16,31,46,59,74,255,255,3,17,32,47,60,255,255,255,
    4,18,33,48,61,255,255,255,5,19,34,49,62,75,255,255,
    6,20,35,50,63,255,255,255,7,21,36,51,64,255,255,255,
    8,22,37,52,65,255,255,255,9,23,38,53,66,76,255,255,
    10,24,39,54,67,77,255,255,11,25,40,55,68,78,255,255,
    12,26,41,255,255,255,255,255,255,27,42,56,69,79,255,255,
    255,255,13,57,70,80,255,255,255,28,43,71,255,81,255,255
};

/* r6 is the current native scan row. All scratch registers are already
 * preserved by the immutable OEM wrapper. There is no C call or static
 * parameter in this path, and the native 32-MOVX block is unchanged. */
void ak820_direct_publish_row(void) __naked {
    __asm
        mov dptr, #_ak820_direct_state
        movx a, @dptr
        cjne a, #3, 00901$
        mov a, r6
        jnz 00909$
        mov a, #4
        movx @dptr, a
00901$:
        cjne a, #4, 00909$
        mov a, r6
        rl a
        rl a
        rl a
        mov r5, a
        mov r7, #8
00902$:
        mov dptr, #_ak820_rgb_led_for_slot
        mov a, r5
        movc a, @a+dptr
        cjne a, #0xff, 00903$
        sjmp 00908$
00903$:
        mov b, #3
        mul ab
        add a, #<(_ak820_direct_stage)
        mov dpl, a
        clr a
        addc a, #>(_ak820_direct_stage)
        mov dph, a
        movx a, @dptr
        mov r2, a
        inc dptr
        movx a, @dptr
        mov r3, a
        inc dptr
        movx a, @dptr
        mov r4, a
        mov a, r5
        mov b, #4
        mul ab
        mov dpl, a
        mov a, b
        add a, #2
        mov dph, a
        mov a, r2
        orl a, r3
        orl a, r4
        jz 00904$
        mov a, #0xff
00904$:
        movx @dptr, a
        inc dptr
        mov a, r2
        movx @dptr, a
        inc dptr
        mov a, r3
        movx @dptr, a
        inc dptr
        mov a, r4
        movx @dptr, a
00908$:
        inc r5
        djnz r7, 00902$
00909$:
        ret
    __endasm;
}
#endif

bool ak820_matrix_snapshot(uint8_t *rows) {
    uint8_t row;
    uint8_t value;
    uint8_t irq_enabled;
    bool changed = false;

    if (!ak820_scan_ready) {
        return false;
    }
    /* Mask only the scan interrupt during the16-byte snapshot; USB remains
     * responsive. Preserve its previous enable state instead of forcing it. */
    irq_enabled = IE_EX & 0x20;
    IE_PWM_I2C = 0;
    ak820_scan_ready = 0;
    for (row = 0; row < AK820_SCAN_ROWS; ++row) {
        value = ak820_scan_rows[row];
#ifdef AK820_MATRIX_MASK
        value &= ak820_matrix_mask[row];
#endif
        if (rows[row] != value) {
            rows[row] = value;
            changed = true;
        }
    }
    if (irq_enabled) {
        IE_PWM_I2C = 1;
    }
    return changed;
}

void ak820_set_slot_rgb(uint8_t slot, uint8_t r, uint8_t g, uint8_t b) __naked {
    _Static_assert(AK820_SCAN_ROWS * AK820_SCAN_COLS == 128 && AK820_LED_DMA_ADDRESS == 0x0200,
                   "Compact slot writer requires the native 128-slot DMA layout");
    slot; r; g; b;
    /* Large-model ABI: slot in DPL, colors in XDATA parameter slots. Preserve
     * the LED IRQ enable in carry across four MOVX writes; MOV/INC DPTR do not
     * change carry, and other IRQ wrappers restore PSW. No whole-frame mask,
     * calls, static scratch or stack use. Native DD75 intensity is retained. */
    __asm
        mov a,dpl
        jnb acc.7,00930$
        ret
00930$:
        mov r7,a
        mov dptr,#_ak820_set_slot_rgb_PARM_2
        movx a,@dptr
        mov r2,a
        mov dptr,#_ak820_set_slot_rgb_PARM_3
        movx a,@dptr
        mov r3,a
        mov dptr,#_ak820_set_slot_rgb_PARM_4
        movx a,@dptr
        mov r4,a
        mov a,r7
        add a,acc
        add a,acc
        mov dpl,a
        mov a,#2
        addc a,#0
        mov dph,a
        mov a,r2
        orl a,r3
        orl a,r4
        jz 00931$
        mov a,#0xff
00931$:
        mov c,_IE_PWM_I2C
        clr _IE_PWM_I2C
        movx @dptr,a
        inc dptr
        mov a,r2
        movx @dptr,a
        inc dptr
        mov a,r3
        movx @dptr,a
        inc dptr
        mov a,r4
        movx @dptr,a
        mov _IE_PWM_I2C,c
        ret
    __endasm;
}

#ifdef RGB_MATRIX_ENABLE
#    include "rgb_matrix.h"

#    ifdef AK820_RGB_SLOT_MAP
const __code uint8_t ak820_rgb_slots[] = AK820_RGB_SLOT_MAP;
typedef char ak820_rgb_slot_map_size_must_match[(sizeof(ak820_rgb_slots) == RGB_MATRIX_LED_COUNT) ? 1 : -1];
#    elif RGB_MATRIX_LED_COUNT != 128
#        error "Provide AK820_RGB_SLOT_MAP for the selected physical LED count"
#    endif

/* The only board renderer is known at build time. Direct calls avoid the
 * stack-only ABI required by an indirect __reentrant callback. */
void ak820_rgb_set_color(uint8_t index, uint8_t r, uint8_t g, uint8_t b) {
    if (index >= RGB_MATRIX_LED_COUNT) {
        return;
    }
#    ifdef AK820_RGB_SLOT_MAP
    ak820_set_slot_rgb(ak820_rgb_slots[index], r, g, b);
#    else
    ak820_set_slot_rgb((uint8_t)index, r, g, b);
#    endif
}

void ak820_rgb_set_color_all(uint8_t r, uint8_t g, uint8_t b) {
    uint8_t i;
    for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
        ak820_rgb_set_color(i, r, g, b);
    }
}

/* matrix_init starts the shared peripheral before quantum_init. Each color
 * goes straight into the live DMA buffer; no init or flush callback is needed. */
#endif
