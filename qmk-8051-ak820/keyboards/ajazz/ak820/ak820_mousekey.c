/* SPDX-License-Identifier: GPL-2.0-or-later
 * Fixed-speed Mouse Keys for the AK820's nonblocking shared HID endpoint.
 */
#ifdef AK820_MOUSEKEY_HOST_TEST
#    include "mousekey_test.h"
#else
#    include "mousekey.h"
#    include "keycodes.h"
#    include "timer.h"
#    include "usb_device.h"
#    include "usb_ak820.h"
#endif

static uint8_t directions;
static uint8_t immediate;
static uint8_t buttons;
static uint8_t accepted_buttons;
static uint16_t cursor_time;
static uint16_t wheel_time;
static report_mouse_t mouse_report;

/* Direction bits follow the four cursor and four wheel keycodes. */
static uint8_t direction_bit(uint8_t code) {
    if (code >= KC_MS_UP && code <= KC_MS_RIGHT) return (uint8_t)(1u << (code - KC_MS_UP));
    if (code >= KC_MS_WH_UP && code <= KC_MS_WH_RIGHT) return (uint8_t)(0x10u << (code - KC_MS_WH_UP));
    return 0;
}

void mousekey_on(uint8_t code) {
    uint8_t bit = direction_bit(code);
    if (bit && !(directions & bit)) {
        immediate |= bit;
        directions |= bit;
        if (bit & 0x0f) cursor_time = timer_read();
        else wheel_time = timer_read();
    } else if (code >= KC_MS_BTN1 && code <= KC_MS_BTN5) {
        buttons |= (uint8_t)(1u << (code - KC_MS_BTN1));
    }
}

void mousekey_off(uint8_t code) {
    uint8_t bit = direction_bit(code);
    directions &= (uint8_t)~bit;
    immediate &= (uint8_t)~bit;
    if (code >= KC_MS_BTN1 && code <= KC_MS_BTN5) buttons &= (uint8_t)~(1u << (code - KC_MS_BTN1));
}

/* Opposing held directions cancel even when only one was newly pressed. */
static int8_t axis(uint8_t selected, uint8_t negative, uint8_t positive) {
    if ((directions & (negative | positive)) == (negative | positive)) return 0;
    if (selected & negative) return -1;
    if (selected & positive) return 1;
    return 0;
}

void mousekey_send(void) {
    uint8_t selected = immediate;
    immediate = 0; /* Relative movement never accumulates behind a busy endpoint. */
#ifdef MOUSE_SHARED_EP
    mouse_report.report_id = REPORT_ID_MOUSE;
#endif
    mouse_report.buttons = buttons;
    mouse_report.x = axis(selected, 4, 8) * 8;
    mouse_report.y = axis(selected, 1, 2) * 8;
    mouse_report.v = axis(selected, 0x20, 0x10);
    mouse_report.h = axis(selected, 0x40, 0x80);
    if (!(mouse_report.x || mouse_report.y || mouse_report.v || mouse_report.h || buttons != accepted_buttons)) return;
    if (ak820_usb_try_send(MOUSE_IN_EPNUM, (const uint8_t __xdata *)&mouse_report, sizeof(mouse_report))) accepted_buttons = buttons;
}

void mousekey_task(void) {
    uint16_t now = timer_read();
    if ((uint16_t)(now - cursor_time) >= 20) {
        cursor_time = now;
        immediate |= directions & 0x0f;
    }
    if ((uint16_t)(now - wheel_time) >= 80) {
        wheel_time = now;
        immediate |= directions & 0xf0;
    }
    mousekey_send();
}

void mousekey_clear(void) {
    directions = 0;
    immediate = 0;
    buttons = 0;
    /* Keep accepted_buttons until a zero-button report is accepted. */
}
