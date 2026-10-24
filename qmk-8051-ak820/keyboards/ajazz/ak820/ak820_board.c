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
        lcall 00010$

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

void ak820_set_slot_rgb(uint8_t slot, uint8_t r, uint8_t g, uint8_t b) {
    uint16_t offset;
    uint8_t irq_enabled;
    if (slot >= AK820_SCAN_ROWS * AK820_SCAN_COLS) {
        return;
    }
    offset = (uint16_t)slot * 4;
    irq_enabled = IE_EX & 0x20;
    IE_PWM_I2C = 0;
    /* Native DD75 copies intensity and3 components unchanged to the DMA
     * buffer. All-zero intensity makes an unused LED slot dark. */
    ak820_led_dma[offset]     = (r | g | b) ? 0xff : 0;
    ak820_led_dma[offset + 1] = r;
    ak820_led_dma[offset + 2] = g;
    ak820_led_dma[offset + 3] = b;
    if (irq_enabled) {
        IE_PWM_I2C = 1;
    }
}

#ifdef RGB_MATRIX_ENABLE
#    include "rgb_matrix.h"

#    ifdef AK820_RGB_SLOT_MAP
const __code uint8_t ak820_rgb_slots[] = AK820_RGB_SLOT_MAP;
typedef char ak820_rgb_slot_map_size_must_match[(sizeof(ak820_rgb_slots) == RGB_MATRIX_LED_COUNT) ? 1 : -1];
#    elif RGB_MATRIX_LED_COUNT != 128
#        error "Provide AK820_RGB_SLOT_MAP for the selected physical LED count"
#    endif

static void ak820_rgb_init(void) {
    /* matrix_init started the shared peripheral before quantum_init. */
}

/* SDCC indirect calls pass all callback arguments on the internal stack. */
static void ak820_rgb_set_color(int index, uint8_t r, uint8_t g, uint8_t b) __reentrant {
    if (index < 0 || index >= RGB_MATRIX_LED_COUNT) {
        return;
    }
#    ifdef AK820_RGB_SLOT_MAP
    ak820_set_slot_rgb(ak820_rgb_slots[index], r, g, b);
#    else
    ak820_set_slot_rgb((uint8_t)index, r, g, b);
#    endif
}

static void ak820_rgb_set_color_all(uint8_t r, uint8_t g, uint8_t b) __reentrant {
    uint8_t i;
    for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
        ak820_rgb_set_color(i, r, g, b);
    }
}

static void ak820_rgb_flush(void) {
    /* Each color is already in the live DMA buffer; no separate bus transfer. */
}

const rgb_matrix_driver_t rgb_matrix_driver = {
    ak820_rgb_init,
    ak820_rgb_set_color,
    ak820_rgb_set_color_all,
    ak820_rgb_flush,
};
#endif
