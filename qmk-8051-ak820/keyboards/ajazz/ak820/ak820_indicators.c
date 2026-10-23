/* SPDX-License-Identifier: GPL-3.0-only */
#pragma codeseg AK820LOW

#include "ak820_board.h"
#include "action_layer.h"
#include "usb_device.h"

/* OEM-derived candidates: host Caps bit 1 uses slot 71; any non-base layer
 * uses slot 79. These slots are reserved outside the QMK RGB map. */
void ak820_update_indicators(void) {
    register uint8_t caps = 0;
    register uint8_t layer = 0;
    __bit irq_enabled = IE_PWM_I2C;

    if (D0UsbConfig && !(USB_SleepStatus & 2)) {
        caps = (uint8_t)(0u - ((KB_USB_SetReport >> 1) & 1));
        if ((layer_state | default_layer_state) & (layer_state_t)~1) layer = 0xff;
    }
    IE_PWM_I2C = 0;
    /* Only intensity and component 1 are owned by each dedicated slot. */
    ak820_led_dma[0x11c] = caps;
    ak820_led_dma[0x11d] = caps;
    ak820_led_dma[0x13c] = layer;
    ak820_led_dma[0x13d] = layer;
    IE_PWM_I2C = irq_enabled;
}
