/* SPDX-License-Identifier: GPL-2.0-or-later */
#define AK820_MOUSEKEY_HOST_TEST
#include "../../keyboards/ajazz/ak820/ak820_mousekey.c"
#include <assert.h>
static uint16_t now;
static bool ready = true;
static unsigned sent;
static report_mouse_t last;
uint16_t timer_read(void) { return now; }
bool ak820_usb_try_send(uint8_t ep, const uint8_t *p, uint8_t n) {
    assert(ep == 2 && n == sizeof(last));
    if (!ready) return false;
    last = *(const report_mouse_t *)p; ++sent; return true;
}
static void tick(uint16_t t) { now = t; mousekey_task(); }
int main(void) {
    now = 65530; mousekey_on(0xd0); mousekey_send();
    assert(sent == 1 && last.x == AK820_MOUSE_CURSOR_STEP);
    tick((uint16_t)(65530u + AK820_MOUSE_CURSOR_PERIOD - 1)); assert(sent == 1);
    tick((uint16_t)(65530u + AK820_MOUSE_CURSOR_PERIOD)); assert(sent == 2);
    ready = false; tick((uint16_t)(65530u + 2u * AK820_MOUSE_CURSOR_PERIOD));
    ready = true; tick((uint16_t)(65530u + 2u * AK820_MOUSE_CURSOR_PERIOD)); assert(sent == 2);
    mousekey_off(0xd0); now = 1000; mousekey_on(0xd9); mousekey_send();
    assert(last.v == AK820_MOUSE_WHEEL_STEP); sent = 0;
    tick((uint16_t)(1000u + AK820_MOUSE_WHEEL_PERIOD - 1)); assert(sent == 0);
    tick((uint16_t)(1000u + AK820_MOUSE_WHEEL_PERIOD)); assert(sent == 1);
    mousekey_off(0xd9); mousekey_on(0xda); mousekey_send();
    assert(last.v == -AK820_MOUSE_WHEEL_STEP);
    mousekey_off(0xda); mousekey_on(0xdb); mousekey_send();
    assert(last.h == -AK820_MOUSE_WHEEL_STEP);
    mousekey_off(0xdb); mousekey_on(0xcf); mousekey_send();
    assert(last.x == -AK820_MOUSE_CURSOR_STEP);
    mousekey_clear(); now = 2000; mousekey_on(0xd0); mousekey_on(0xd9); mousekey_send();
    tick((uint16_t)(2000u + (AK820_MOUSE_CURSOR_PERIOD < AK820_MOUSE_WHEEL_PERIOD ?
                            AK820_MOUSE_CURSOR_PERIOD : AK820_MOUSE_WHEEL_PERIOD)));
    assert(last.x == (AK820_MOUSE_CURSOR_PERIOD <= AK820_MOUSE_WHEEL_PERIOD ? AK820_MOUSE_CURSOR_STEP : 0));
    assert(last.v == (AK820_MOUSE_WHEEL_PERIOD <= AK820_MOUSE_CURSOR_PERIOD ? AK820_MOUSE_WHEEL_STEP : 0));
    return 0;
}
