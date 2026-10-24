/* SPDX-License-Identifier: GPL-3.0-only */
#include "ak820_os_indicators.h"
#include "timer.h"
#include "vial.h"

volatile uint8_t ak820_os_indicator_mode;
static uint32_t os_indicator_refreshed;

void ak820_os_indicator_set(uint8_t mode) {
    os_indicator_refreshed = timer_read32();
    ak820_os_indicator_mode = mode;
}

uint8_t ak820_os_indicator_get(void) {
    /* A 16-bit lease can revive after a long macro or foreground stall.
     * Latch expiry, using the existing 32-bit monotonic millisecond clock. */
    if (ak820_os_indicator_mode &&
        (vial_unlock_in_progress || timer_elapsed32(os_indicator_refreshed) >= AK820_OS_INDICATOR_LEASE_MS))
        ak820_os_indicator_mode = AK820_OS_NORMAL;
    return ak820_os_indicator_mode;
}

uint8_t ak820_os_indicator_value(uint8_t normal) {
    uint8_t phase;
    switch (ak820_os_indicator_get()) {
        case AK820_OS_OFF: return 0;
        case AK820_OS_ON: return 255;
        case AK820_OS_BREATHE:
            /* One 4096-ms triangle. Lease refresh never resets its phase. */
            phase = (uint8_t)(timer_read() >> 4);
            if (phase & 0x80) phase = (uint8_t)~phase;
            return (uint8_t)(phase << 1);
        default: return normal;
    }
}
