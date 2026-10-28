/* SPDX-License-Identifier: GPL-3.0-only */
#if !defined(AK820_OS_INDICATORS) && !defined(AK820_MAC_PC)
#    pragma codeseg AK820LOW
#endif

#ifdef AK820_USB_HOST_TEST
#    include "ak820_usb_test_shim.h"
#else
#    include "ak820_board.h"
#    include "action_layer.h"
#    include "action_util.h"
#    include "timer.h"
#    include "usb_device.h"
#endif
#include "caps_word.h"
#ifdef AK820_OS_INDICATORS
#    include "ak820_os_indicators.h"
#endif
#ifdef AK820_MAC_PC
#    include "ak820_mac_pc.h"
#endif
#ifdef AK820_COMPACT_GUI_LOCK
static __data uint16_t gui_pulse_last;
static __data uint16_t gui_pulse_phase;
static __bit gui_pulse_started;
static void gui_pulse_reset(void) {
    gui_pulse_started = 0;
    gui_pulse_phase = 0;
}
#endif

#ifdef AK820_COMPACT_GUI_LOCK
#if defined(__SDCC_mcs51)
/* phase / 125 leaves r < 125. For every such r, floor(16*r/125)
 * equals floor(131*r/1024), so one 8-bit multiply completes the fraction.
 * Keep all R registers intact: callers may retain indicator values there. */
static uint8_t gui_pulse_angle(uint16_t phase) __naked {
    phase;
    __asm
        mov b, #192
00001$:
        mov a, dpl
        clr c
        subb a, #125
        mov dpl, a
        mov a, dph
        subb a, #0
        jc 00002$
        mov dph, a
        mov a, b
        add a, #16
        mov b, a
        sjmp 00001$
00002$:
        mov a, dpl
        add a, #125
        mov dph, b
        mov b, #131
        mul ab
        mov a, b
        rr a
        rr a
        anl a, #0x3f
        add a, dph
        mov dpl, a
        ret
    __endasm;
}
#else
static uint8_t gui_pulse_angle(uint16_t phase) {
    return (uint8_t)(192u + ((phase << 4) / 125u));
}
#endif
static uint8_t gui_pulse_value(void) {
    uint16_t now = timer_read();
    if (!gui_pulse_started) {
        gui_pulse_started = 1;
        gui_pulse_last = now;
    } else {
        uint16_t elapsed = (uint16_t)(now - gui_pulse_last);
        gui_pulse_last = now;
        while (elapsed >= 2000u) elapsed = (uint16_t)(elapsed - 2000u);
        gui_pulse_phase = (uint16_t)(gui_pulse_phase + elapsed);
        if (gui_pulse_phase >= 2000u) gui_pulse_phase = (uint16_t)(gui_pulse_phase - 2000u);
    }
    /* The phase accumulator stays in [0,1999]. Sine runs one full cycle from
     * its trough at phase 192 through its crest and back over two seconds. */
    return ak820_breathing_wave(gui_pulse_angle(gui_pulse_phase));
}
#endif

/* OEM-derived channels: C uses slot 71 component 1; W uses slot 79
 * component 1. OS uses slot 79 component 3, sharing only slot intensity.
 * Dedicated slots remain outside the ordinary QMK RGB map. */
void ak820_update_indicators(void) {
    register uint8_t caps = 0;
    register uint8_t layer = 0;
#if defined(AK820_OS_INDICATORS) || defined(AK820_MAC_PC)
    register uint8_t os = 0;
#endif
    __bit irq_enabled = IE_PWM_I2C;

    if (D0UsbConfig && !(USB_SleepStatus & 2)) {
        /* C reflects host Caps Lock OR local Caps Word; neither changes the USB LED report. */
        caps = (uint8_t)(0u - (((KB_USB_SetReport >> 1) & 1u) | (uint8_t)is_caps_word_on()));
        if ((layer_state | default_layer_state) & (layer_state_t)~1) {
            layer = 0xff;
#ifdef AK820_COMPACT_GUI_LOCK
            gui_pulse_reset();
#endif
        }
#ifdef AK820_COMPACT_GUI_LOCK
        else if (ak820_gui_lock_is_active()) {
            layer = gui_pulse_value();
        }
        else {
            gui_pulse_reset();
        }
#endif
#ifdef AK820_MAC_PC
        if (ak820_mac_mode) os = 0xff;
#endif
#ifdef AK820_OS_INDICATORS
        os = ak820_os_indicator_value(os);
#endif
    }
#ifdef AK820_COMPACT_GUI_LOCK
    else {
        gui_pulse_reset();
    }
#endif
    IE_PWM_I2C = 0;
    /* W and OS have independent component bytes. Their shared intensity is
     * full whenever either channel is active, so OS cannot dim or hide W. */
    ak820_led_dma[0x11c] = caps;
    ak820_led_dma[0x11d] = caps;
#if defined(AK820_OS_INDICATORS) || defined(AK820_MAC_PC)
    ak820_led_dma[0x13c] = (layer | os) ? 0xff : 0;
    ak820_led_dma[0x13f] = os;
#else
    ak820_led_dma[0x13c] = layer;
#endif
    ak820_led_dma[0x13d] = layer;
    IE_PWM_I2C = irq_enabled;
}
