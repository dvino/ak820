/* SPDX-License-Identifier: GPL-2.0-or-later
 * QMK host glue for the AK820 three-IN-endpoint transport.
 */
#include "report.h"
#include "host.h"
#include "host_driver.h"
#include "keyboard.h"
#include "action.h"
#include "usb_device.h"
#include "usb_ak820.h"
#include "usb_device_state.h"
#include "keycode_config.h"
#include "raw_hid.h"
#include "timer.h"
#include "ak820_board.h"
#include "ak820_nvm.h"
#ifdef RGB_MATRIX_ENABLE
#    include "rgb_matrix.h"
#endif

volatile uint8_t keyboard_idle;
volatile uint8_t keyboard_protocol = 1;

/* Main owns the latest desired keyboard report. USB's separate snapshots
 * remain the last accepted reports for GET_REPORT. A timed-out release must
 * stay pending even though the QMK change detector has already seen it. */
static report_keyboard_t last_keyboard_report;
static uint16_t last_keyboard_time;
enum { PENDING_KEYBOARD = 1, PENDING_SYSTEM = 2, PENDING_CONSUMER = 4 };
static uint8_t pending_reports;

static uint8_t keyboard_leds(void) {
    return KB_USB_SetReport;
}

static void send_keyboard(report_keyboard_t *report) {
    uint8_t endpoint = KEYBOARD_IN_EPNUM;
    uint8_t length = KEYBOARD_REPORT_SIZE;
#ifdef NKRO_ENABLE
    if (keyboard_protocol && keymap_config.nkro) {
        endpoint = SHARED_IN_EPNUM;
        length = sizeof(struct nkro_report);
    }
#endif
    last_keyboard_report = *report;
    pending_reports |= PENDING_KEYBOARD;
    if (ak820_usb_send(endpoint, (const uint8_t __xdata *)&last_keyboard_report, length)) {
        pending_reports &= (uint8_t)~PENDING_KEYBOARD;
        last_keyboard_time = timer_read();
    }
}

static void send_mouse(report_mouse_t *report) {
#ifdef MOUSE_ENABLE
    ak820_usb_send(MOUSE_IN_EPNUM, (const uint8_t __xdata *)report, sizeof(report_mouse_t));
#else
    (void)report;
#endif
}

static void send_extra(report_extra_t *report) {
#ifdef EXTRAKEY_ENABLE
    uint8_t pending = report->report_id == REPORT_ID_SYSTEM ? PENDING_SYSTEM : PENDING_CONSUMER;
    if (ak820_usb_send(SHARED_IN_EPNUM, (const uint8_t __xdata *)report, sizeof(report_extra_t))) {
        pending_reports &= (uint8_t)~pending;
    } else {
        pending_reports |= pending;
    }
#else
    (void)report;
#endif
}

/* This port has one transport. Direct entry points keep report dispatch out of
 * mutable RAM callback tables; the generic driver still marks initialization. */
uint8_t ak820_host_keyboard_leds(void) { return keyboard_leds(); }
void ak820_host_send_keyboard(report_keyboard_t *report) { send_keyboard(report); }
void ak820_host_send_mouse(report_mouse_t *report) { send_mouse(report); }
void ak820_host_send_extra(report_extra_t *report) { send_extra(report); }

host_driver_t ch555_usb_stack_driver = {keyboard_leds, send_keyboard, send_mouse, send_extra};

void raw_hid_send(uint8_t *data, uint8_t length) {
    ak820_usb_raw_send(data, length);
}

void protocol_setup(void) {
    ak820_clock_init();
    usb_device_state_init();
}

void protocol_pre_init(void) {
    ak820_boot_stage = 1;
    /* VIA may reset many individual EEPROM bytes during keyboard_init. */
    ak820_nvm_begin();
    USB_Device_Init();
}

void protocol_post_init(void) {
    ak820_nvm_end();
    host_set_driver(&ch555_usb_stack_driver);
    ak820_boot_stage = 2;
}

void protocol_pre_task(void) {
    /* User hooks and report generation must stay out of the USB interrupt. */
    enum usb_device_state next = (USB_SleepStatus & 2) ? USB_DEVICE_STATE_SUSPEND :
        (D0UsbConfig ? USB_DEVICE_STATE_CONFIGURED : USB_DEVICE_STATE_INIT);
    if (next != usb_device_state) {
        if (next == USB_DEVICE_STATE_SUSPEND) usb_device_state_set_suspend(D0UsbConfig != 0, D0UsbConfig);
        else if (usb_device_state == USB_DEVICE_STATE_SUSPEND) usb_device_state_set_resume(D0UsbConfig != 0, D0UsbConfig);
        else usb_device_state_set_configuration(D0UsbConfig != 0, D0UsbConfig);
#if defined(RGB_MATRIX_ENABLE) && (defined(RGB_MATRIX_SLEEP) || defined(RGB_DISABLE_WHEN_USB_SUSPENDED))
        // Generic USB state hooks do not run the compact RGB sleep handler.
        // Keep LED clearing and resume work in the main loop, outside the ISR.
        rgb_matrix_set_suspend_state(next == USB_DEVICE_STATE_SUSPEND);
#endif
    }
    if (ak820_usb_take_keyboard_reset()) {
        pending_reports = 0;
        memset(&last_keyboard_report, 0, sizeof(last_keyboard_report));
        last_keyboard_time = timer_read();
        clear_keyboard();
    }
}

void protocol_post_task(void) {
    uint8_t endpoint = KEYBOARD_IN_EPNUM;
    uint8_t length = KEYBOARD_REPORT_SIZE;
    ak820_boot_stage = 3;
    ++ak820_main_heartbeat;
    ak820_usb_raw_task();
#ifdef NKRO_ENABLE
    if (keyboard_protocol && keymap_config.nkro) {
        endpoint = SHARED_IN_EPNUM;
        length = sizeof(struct nkro_report);
    }
#endif
    /* At most one attempt per available endpoint per task. A busy/suspended
     * endpoint is skipped, so retry work cannot add the send timeout again.
     * HID idle uses four-ms units; NKRO needs retries but no idle resends. */
    if (((pending_reports & PENDING_KEYBOARD) ||
         (keyboard_idle && (!keyboard_protocol || !keymap_config.nkro) &&
          timer_elapsed(last_keyboard_time) >= (uint16_t)keyboard_idle * 4u)) &&
        ak820_usb_try_send(endpoint, (const uint8_t __xdata *)&last_keyboard_report, length)) {
        pending_reports &= (uint8_t)~PENDING_KEYBOARD;
        last_keyboard_time = timer_read();
    }
#ifdef EXTRAKEY_ENABLE
    if (pending_reports & (PENDING_SYSTEM | PENDING_CONSUMER)) {
        /* Core stores each latest requested usage before invoking send_extra.
         * Keep independent pending bits: the two IDs share EP2 but a consumer
         * update must not overwrite an outstanding system release. */
        report_extra_t report;
        uint8_t pending;
        if (pending_reports & PENDING_SYSTEM) {
            pending = PENDING_SYSTEM;
            report.report_id = REPORT_ID_SYSTEM;
            report.usage = host_last_system_usage();
        } else {
            pending = PENDING_CONSUMER;
            report.report_id = REPORT_ID_CONSUMER;
            report.usage = host_last_consumer_usage();
        }
        if (ak820_usb_try_send(SHARED_IN_EPNUM, (const uint8_t __xdata *)&report, sizeof(report))) {
            pending_reports &= (uint8_t)~pending;
        }
    }
#endif
    /* LED output state is maintained by SET_REPORT; active-layer state
     * includes held, toggled, momentary and default layers. The indicators
     * are forced dark until USB is configured and awake. */
    ak820_update_indicators();
}
