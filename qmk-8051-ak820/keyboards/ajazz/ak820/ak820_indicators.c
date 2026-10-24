/* SPDX-License-Identifier: GPL-3.0-only */
#if !defined(AK820_OS_INDICATORS) && !defined(AK820_MAC_PC)
#    pragma codeseg AK820LOW
#endif

#ifdef AK820_USB_HOST_TEST
#    include "ak820_usb_test_shim.h"
#else
#    include "ak820_board.h"
#    include "action_layer.h"
#    include "usb_device.h"
#endif
#ifdef AK820_OS_INDICATORS
#    include "ak820_os_indicators.h"
#endif
#ifdef AK820_MAC_PC
#    include "ak820_mac_pc.h"
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
        caps = (uint8_t)(0u - ((KB_USB_SetReport >> 1) & 1));
        if ((layer_state | default_layer_state) & (layer_state_t)~1) layer = 0xff;
#ifdef AK820_MAC_PC
        if (ak820_mac_mode) os = 0xff;
#endif
#ifdef AK820_OS_INDICATORS
        os = ak820_os_indicator_value(os);
#endif
    }
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
