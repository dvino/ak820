/* SPDX-License-Identifier: GPL-2.0-or-later
 * Production USB + verbatim backend/host bodies; hardware/timer/QMK hooks are
 * fixtures. The linked CPU runner separately checks the actual SDCC ABI. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_usb_test_shim.h"
#include "host_driver.h"
#include "usb_device_state.h"

volatile uint8_t test_mmio[0x2300];
uint8_t test_rom[0x10000];
volatile uint8_t EA = 1, IE_USB;
bool vial_unlocked, vial_unlock_in_progress;
uint8_t ak820_flash_diagnostic[6];
enum usb_device_state usb_device_state;
struct { bool nkro; } keymap_config;
static const host_driver_t *driver;
static uint16_t last_system_usage, last_consumer_usage, test_clock;
static unsigned waits_us, waits_ms;

uint16_t timer_read(void) { return test_clock; }
uint16_t timer_elapsed(uint16_t start) { return test_clock - start; }
void wait_us(uint16_t value) { (void)value; ++waits_us; }
void wait_ms(uint16_t value) { (void)value; ++waits_ms; }
void host_set_driver(const host_driver_t *value) { driver = value; }
void ak820_clock_init(void) {}
void ak820_update_indicators(void) {}
void usb_device_state_init(void) { usb_device_state = USB_DEVICE_STATE_INIT; }
void usb_device_state_set_configuration(bool configured, uint8_t number) {
    (void)number; usb_device_state = configured ? USB_DEVICE_STATE_CONFIGURED : USB_DEVICE_STATE_INIT;
}
void usb_device_state_set_suspend(bool configured, uint8_t number) {
    (void)configured; (void)number; usb_device_state = USB_DEVICE_STATE_SUSPEND;
}
void usb_device_state_set_resume(bool configured, uint8_t number) {
    usb_device_state_set_configuration(configured, number);
}
bool ak820_nvm_ok(void) { return true; }
void ak820_nvm_begin(void) {}
void ak820_nvm_flush(void) {}
void ak820_nvm_end(void) {}
void ak820_nvm_diagnostic(uint8_t *out) { memset(out, 0, 7); }
void raw_hid_receive(uint8_t *data, uint8_t length) { (void)data; (void)length; }
void test_ack_transfer(void) { USB_IF &= (uint8_t)~bUX_IF_D0_TRANS; }
void test_ack_all(void) { USB_IF = 0; }
uint8_t test_read_code(uint16_t address) { return test_rom[address]; }
void clear_keyboard(void);
uint16_t host_last_system_usage(void);
uint16_t host_last_consumer_usage(void);

#include "usb_ak820.c"
#include "backend.inc"
#include "host-extra.inc"

void clear_keyboard(void) {
    report_keyboard_t report;
    memset(&report, 0, sizeof(report));
    send_keyboard(&report);
    host_system_send(0);
    host_consumer_send(0);
}

static void initialize(void) {
    memset((void *)test_mmio, 0, sizeof(test_mmio));
    memset(&last_keyboard_report, 0, sizeof(last_keyboard_report));
    pending_reports = last_keyboard_time = test_clock = 0;
    last_system_usage = last_consumer_usage = 0;
    keymap_config.nkro = false;
    EA = 1;
    USB_Device_Init();
    USB_EnumStatus = D0UsbConfig = 1;
    driver = &ch555_usb_stack_driver;
    waits_us = waits_ms = 0;
}

static void complete(uint8_t endpoint) {
    EP_RESPONSE(endpoint) = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
}

static void assert_no_wait_post(void) {
    waits_us = waits_ms = 0;
    protocol_post_task();
    assert(!waits_us && !waits_ms);
}

static void keyboard_latest(void) {
    report_keyboard_t report;
    initialize();
    memset(&report, 0, sizeof(report));
    report.raw[2] = 4;
    send_keyboard(&report);
    assert(!pending_reports && input_snapshot[2] == 4);
    report.raw[2] = 0;
    send_keyboard(&report);
    assert(waits_us == 250 && (pending_reports & PENDING_KEYBOARD));
    assert(last_keyboard_report.raw[2] == 0 && input_snapshot[2] == 4);
    for (unsigned i = 0; i < 10; ++i) assert_no_wait_post();
    report.raw[2] = 5;
    send_keyboard(&report);
    complete(1);
    assert_no_wait_post();
    assert(!pending_reports && input_snapshot[2] == 5 && test_mmio[0x1042] == 5);
}

static void independent_shared(void) {
    initialize();
    host_system_send(0x81);
    host_consumer_send(0xE9);
    host_system_send(0);
    host_consumer_send(0);
    assert(pending_reports == (PENDING_SYSTEM | PENDING_CONSUMER));
    assert_no_wait_post();
    complete(2);
    assert_no_wait_post();
    assert(test_mmio[0x1080] == REPORT_ID_SYSTEM && test_mmio[0x1081] == 0);
    assert(pending_reports == PENDING_CONSUMER);
    complete(2);
    assert_no_wait_post();
    assert(test_mmio[0x1080] == REPORT_ID_CONSUMER && test_mmio[0x1081] == 0);
    assert(!pending_reports);
}

static void retry_guards(void) {
    uint8_t report[64] = {0};
    unsigned checks = 0;
    for (unsigned ea = 0; ea <= 1; ++ea) {
        for (unsigned state = 0; state < 7; ++state) {
            for (unsigned endpoint = 0; endpoint < 5; ++endpoint) {
                initialize();
                EA = ea;
                report[0] = REPORT_ID_CONSUMER;
                if (state == 1) USB_EnumStatus = 0;
                if (state == 2) USB_SleepStatus = 2;
                if (state == 3) USB_SleepStatus = 3;
                if (state == 4) keyboard_reset = 1;
                if (state == 5 && endpoint) EP_RESPONSE(endpoint) = UEP_X_RES_ACK;
                if (state == 6 && endpoint) EP_RESPONSE(endpoint) = UEP_X_RES_STALL;
                bool sent = ak820_usb_try_send(endpoint, report, endpoint == 1 ? 8 : 3);
                bool expected = state == 0 && (endpoint == 1 || endpoint == 2);
                assert(sent == expected && EA == ea && !waits_us && !waits_ms);
                ++checks;
            }
        }
    }
    /* Ready invalid packets still go through the existing length/ID guards. */
    for (unsigned length = 0; length <= 65; ++length) {
        initialize();
        report[0] = REPORT_ID_CONSUMER;
        bool sent = ak820_usb_try_send(2, report, length);
        assert(sent == (length == 3) && EA == 1 && !waits_us && !waits_ms);
        ++checks;
    }
    printf("retry guards: %u state/endpoint/length cases PASS\n", checks);
}

static void reset_and_suspend(void) {
    report_keyboard_t report;
    initialize();
    memset(&report, 0, sizeof(report));
    report.raw[2] = 4;
    send_keyboard(&report);
    report.raw[2] = 5;
    send_keyboard(&report);
    complete(1);
    USB_SleepStatus = 2;
    assert_no_wait_post();
    assert(test_mmio[0x1042] == 4 && (pending_reports & PENDING_KEYBOARD));
    USB_SleepStatus = 0;
    keyboard_reset = 1;
    assert_no_wait_post();
    assert((EP_RESPONSE(1) & MASK_UEP_X_RES) == UEP_X_RES_NAK);
    protocol_pre_task();
    assert_no_wait_post();
    assert(last_keyboard_report.raw[2] == 0 && test_mmio[0x1042] == 0);
    assert(!(pending_reports & PENDING_KEYBOARD));
}

static void fixed_dispatch_and_startup(void) {
    host_driver_t empty_driver = {0};
    initialize();
    driver = NULL;
    host_system_send(0x81);
    assert(!pending_reports && last_system_usage == 0x81);
    assert(EP_RESPONSE(SHARED_IN_EPNUM) != (bUEP_X_AUTO_TOG | UEP_X_RES_ACK));
    /* The fixed AK820 transport uses the driver only as an initialized marker.
     * A nonnull empty callback table must still reach its direct transport. */
    driver = &empty_driver;
    host_system_send(0x82);
    assert(test_mmio[0x1080] == REPORT_ID_SYSTEM && test_mmio[0x1081] == 0x82);
    assert(!pending_reports);
}

int main(void) {
    fixed_dispatch_and_startup();
    keyboard_latest();
    independent_shared();
    retry_guards();
    reset_and_suspend();
    puts("production backend + USB: ownership, no-wait retry, reset/suspend PASS");
    return 0;
}
