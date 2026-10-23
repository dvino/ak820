/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "ak820_usb_test_shim.h"
/* Include the actual implementation, to inspect its state at interrupt edges. */
#include "../../tmk_core/protocol/ch555/usb_ak820.c"

volatile uint8_t test_mmio[0x2300];
uint8_t test_rom[0x10000];
volatile uint8_t EA = 1, IE_USB;
volatile uint8_t keyboard_protocol, keyboard_idle;
static unsigned received, begins, flushes, ends;
static bool nvm_good = true;
bool vial_unlocked, vial_unlock_in_progress;
uint8_t ak820_flash_diagnostic[6];
static uint8_t nvm_diagnostic_bytes[7];
static unsigned callback_mode;
static bool setup_pending, reset_during_read;
static uint8_t queued_setup[8];
static unsigned ack_count, code_reads;
static struct {
    uint8_t status, address, request, phase, raw, ep3;
} ack_events[4];

void wait_ms(uint16_t value) { (void)value; }
void wait_us(uint16_t value) { (void)value; }
bool ak820_nvm_ok(void) { return nvm_good; }
void ak820_nvm_begin(void) { ++begins; }
void ak820_nvm_flush(void) { ++flushes; }
void ak820_nvm_end(void) { ++ends; }
void ak820_nvm_diagnostic(uint8_t *out) { memcpy(out, nvm_diagnostic_bytes, 7); }

/* CH555DS1 section 16.3: SETUP preserves RX_LEN/token/endpoint/toggle. If a
 * completion is pending, the first ACK retires it and the second retires SETUP.
 * The fixture exposes queued SETUP bytes after the earlier completion's ACK;
 * this models buffer ownership, not the controller's internal FIFO timing. */
void test_ack_transfer(void) {
    assert(ack_count < sizeof(ack_events) / sizeof(ack_events[0]));
    ack_events[ack_count].status = D0_STATUS;
    ack_events[ack_count].address = D0_ADDR;
    ack_events[ack_count].request = D0SetupReqCode;
    ack_events[ack_count].phase = control_phase;
    ack_events[ack_count].raw = raw_state;
    ack_events[ack_count++].ep3 = D0_EP3RES;
    if (setup_pending && (D0_STATUS & MASK_UXS_TOKEN) != UXS_TOKEN_FREE) {
        memcpy((void *)pD0_EP0_BUF,queued_setup,sizeof(queued_setup));
        D0_STATUS = (D0_STATUS & ~MASK_UXS_TOKEN) | UXS_TOKEN_FREE;
    } else {
        setup_pending = false;
        D0_STATUS = (D0_STATUS & ~(MASK_UXS_TOKEN | bUXS_SETUP_ACT)) | UXS_TOKEN_FREE;
        USB_IF &= ~bUX_IF_D0_TRANS;
    }
}

void test_ack_all(void) {
    setup_pending = false;
    D0_STATUS = UXS_TOKEN_FREE;
    USB_IF = 0;
}

static void service_irq(void) {
    ack_count = 0;
    USB_DeviceInterrupt();
    assert(!(USB_IF & (bUX_IF_D0_TRANS | bUX_IF_BUS_RST | bUX_IF_SUSPEND)));
}

static void queue_setup(uint8_t type, uint8_t request, uint16_t value, uint16_t index, uint16_t length) {
    const uint8_t p[8] = {type,request,value,value >> 8,index,index >> 8,length,length >> 8};
    assert(!setup_pending);
    memcpy(queued_setup,p,sizeof(p));
    setup_pending = true;
    if ((D0_STATUS & MASK_UXS_TOKEN) == UXS_TOKEN_FREE) memcpy((void *)pD0_EP0_BUF,p,sizeof(p));
    D0_STATUS |= bUXS_SETUP_ACT;
    USB_IF |= bUX_IF_D0_TRANS;
}

static void setup(uint8_t type, uint8_t request, uint16_t value, uint16_t index, uint16_t length) {
    queue_setup(type,request,value,index,length);
    service_irq();
    assert(ack_count == 1);
}

static void queue_in(uint8_t ep) {
    assert(!(USB_IF & bUX_IF_D0_TRANS));
    if (ep && (EP_RESPONSE(ep) & bUEP_X_AUTO_TOG)) EP_RESPONSE(ep) ^= bUEP_X_TOG;
    D0_STATUS = UXS_TOKEN_IN | ep;
    USB_IF |= bUX_IF_D0_TRANS;
}

static void in(uint8_t ep) {
    queue_in(ep);
    service_irq();
    assert(ack_count == 1);
}

static void queue_out(const uint8_t *data, uint8_t length, bool toggle_ok) {
    assert(!(USB_IF & bUX_IF_D0_TRANS));
    if (length) memcpy((void *)pD0_EP0_BUF,data,length);
    D0_RX_LEN = length;
    D0_STATUS = UXS_TOKEN_OUT | (toggle_ok ? bUXS_TOG_OK : 0);
    USB_IF |= bUX_IF_D0_TRANS;
}

static void out(const uint8_t *data, uint8_t length, bool toggle_ok) {
    queue_out(data,length,toggle_ok);
    service_irq();
    assert(ack_count == 1);
}

static void reset(void) {
    USB_IF |= bUX_IF_BUS_RST;
    service_irq();
    assert(!USB_EnumStatus && !D0UsbConfig && !D0_ADDR);
}

uint8_t test_read_code(uint16_t address) {
    ++code_reads;
    if (reset_during_read) {
        reset_during_read = false;
        reset();
        assert(raw_state == RAW_CANCELLED);
    }
    return test_rom[address];
}

static void fresh(void) {
    memset((void *)test_mmio,0,sizeof(test_mmio));
    callback_mode = received = begins = flushes = ends = code_reads = 0;
    reset_during_read = false;
    nvm_good = true;
    EA = 1;
    USB_Device_Init();
    assert(IE_USB && USB_CTRL == bUX_DP_PU_EN && D0_EP_MOD == 1 && USB_IF == 0);
    reset();
}

static void configure(void) {
    setup(0,USB_SET_ADDRESS,5,0,0);
    assert(D0_ADDR == 0 && D0_EP0T_L == 0);
    in(0);
    assert(D0_ADDR == 5);
    setup(0,USB_SET_CONFIGURATION,1,0,0);
    assert(USB_EnumStatus && D0UsbConfig == 1);
    in(0);
    for (uint8_t ep = 1; ep <= 3; ++ep) assert(EP_RESPONSE(ep) == (bUEP_X_AUTO_TOG | UEP_X_RES_NAK));
}

static size_t get_descriptor(uint8_t type, uint8_t index, uint16_t iface, uint16_t max_length, uint8_t *destination) {
    size_t count = 0;
    setup(type == USB_DESCR_TYP_HID || type == USB_DESCR_TYP_REPORT ? 0x81 : 0x80,
          USB_GET_DESCRIPTOR,(uint16_t)type << 8 | index,iface,max_length);
    assert((D0_EP0RES & MASK_UEP_T_RES) != UEP_T_RES_STALL);
    while (control_phase == CTRL_DATA_IN) {
        assert(D0_EP0T_L <= 64);
        memcpy(destination + count,(const void *)pD0_EP0_BUF,D0_EP0T_L);
        count += D0_EP0T_L;
        in(0);
    }
    assert(control_phase == CTRL_STATUS_OUT);
    out(NULL,0,true);
    assert(control_phase == CTRL_IDLE);
    return count;
}

static void raw_request(const uint8_t data[32]) {
    setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
    assert(raw_state == RAW_RX && control_phase == CTRL_DATA_OUT);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_NAK);
    out(data,32,true);
    assert(raw_state == RAW_READY && control_phase == CTRL_STATUS_IN);
    in(0);
}

void raw_hid_receive(uint8_t *data, uint8_t length) {
    assert(length == 32 && raw_state == RAW_WORK && begins == ends + 1);
    ++received;
    if (callback_mode == 1) {
        /* A second host command while main owns the first must not overwrite it. */
        setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
        assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL && raw_state == RAW_WORK);
    }
    if (callback_mode == 2) {
        reset();
        assert(raw_state == RAW_CANCELLED);
    }
    for (uint8_t i = 0; i < 32; ++i) data[i] ^= 0xa5;
    if (callback_mode == 4) data[0] = id_get_protocol_version; /* write response looks like a read */
    if (callback_mode == 5) memset(data,0xff,32); /* read response loses all request bytes */
    ak820_usb_raw_send(data,length);
    if (callback_mode == 3) {
        assert(raw_state == RAW_TX_ACTIVE);
        in(3);
        assert(raw_state == RAW_DRAINED);
        setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
        assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL && raw_state == RAW_DRAINED);
    }
}

static void test_setup_registers_and_order(void) {
    const uint8_t stale_lengths[] = {0,1,2,32,255};
    uint8_t packet[32];
    for (uint8_t i = 0; i < sizeof(packet); ++i) packet[i] = i + 1;
    for (size_t i = 0; i < sizeof(stale_lengths); ++i) {
        fresh();
        D0_RX_LEN = stale_lengths[i];
        setup(0x80,USB_GET_DESCRIPTOR,0x0100,0,64);
        assert(D0_RX_LEN == stale_lengths[i]);
        assert(D0SetupReqCode == USB_GET_DESCRIPTOR && D0_EP0T_L == 18);
        assert(control_phase == CTRL_DATA_IN && (D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_ACK);
    }

    fresh();
    setup(0,USB_SET_ADDRESS,42,0,0);
    queue_in(0);
    queue_setup(0x80,USB_GET_DESCRIPTOR,0x0100,0,64);
    service_irq();
    assert(ack_count == 2 && D0_ADDR == 42 && D0_EP0T_L == 18);
    assert(ack_events[0].address == 42 && ack_events[0].request == USB_SET_ADDRESS);
    assert(ack_events[0].phase == CTRL_IDLE);
    assert(ack_events[1].request == USB_GET_DESCRIPTOR && ack_events[1].phase == CTRL_DATA_IN);
    assert((ack_events[1].status & MASK_UXS_TOKEN) == UXS_TOKEN_FREE);

    in(0); /* descriptor data, then its status OUT plus the next SETUP */
    queue_out(NULL,0,true);
    queue_setup(0x80,USB_GET_CONFIGURATION,0,0,1);
    service_irq();
    assert(ack_count == 2 && D0_RX_LEN == 0);
    assert(ack_events[0].phase == CTRL_IDLE && ack_events[0].request == USB_GET_DESCRIPTOR);
    assert(ack_events[1].phase == CTRL_STATUS_OUT && ack_events[1].request == USB_GET_CONFIGURATION);

    fresh(); configure(); raw_request(packet); ak820_usb_raw_task();
    assert(raw_state == RAW_TX_WAIT);
    queue_in(3);
    queue_setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
    service_irq();
    assert(ack_count == 2 && ack_events[0].raw == RAW_IDLE && ack_events[1].raw == RAW_RX);
    assert((ack_events[0].ep3 & MASK_UEP_X_RES) == UEP_X_RES_NAK);
    assert(control_phase == CTRL_DATA_OUT);

    queue_out(packet,32,true);
    queue_setup(0x80,USB_GET_CONFIGURATION,0,0,1);
    service_irq();
    assert(ack_count == 2 && D0_RX_LEN == 32 && raw_state == RAW_READY);
    assert(ack_events[0].raw == RAW_READY && ack_events[0].phase == CTRL_STATUS_IN);
    assert(ack_events[1].request == USB_GET_CONFIGURATION);
    assert(!memcmp(raw_buffer,packet,sizeof(packet)));

    fresh(); configure();
    setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
    setup(0x80,USB_GET_DESCRIPTOR,0x0100,0,64); /* abort unfinished OUT */
    assert(raw_state == RAW_IDLE && control_phase == CTRL_DATA_IN);

    fresh(); configure(); raw_request(packet); ak820_usb_raw_task();
    queue_in(3);
    reset(); /* reset takes priority over a stale completion */
    assert(ack_count == 1 && ack_events[0].raw == RAW_IDLE && ack_events[0].request == 0xff);
}

static void expect_string(uint8_t index, const char *text) {
    uint8_t actual[256];
    size_t length = strlen(text);
    size_t count = get_descriptor(USB_DESCR_TYP_STRING,index,0x0409,255,actual);
    assert(count == 2 + 2 * length && actual[0] == count && actual[1] == USB_DESCR_TYP_STRING);
    for (size_t i = 0; i < length; ++i) {
        assert(actual[2 + 2 * i] == (uint8_t)text[i] && actual[3 + 2 * i] == 0);
    }
}

static void test_descriptors(void) {
    uint8_t actual[512];
    fresh();
    assert(sizeof(DeviceDescriptor) == 18 && sizeof(ConfigurationDescriptor) == 84);
    assert(DeviceDescriptor.Endpoint0Size == 64 && ConfigurationDescriptor.Config.TotalInterfaces == 3);
    assert(ConfigurationDescriptor.Raw_Interface.InterfaceNumber == 1 && ConfigurationDescriptor.Raw_Interface.TotalEndpoints == 1);
    assert(ConfigurationDescriptor.Raw_INEndpoint.EndpointAddress == 0x83 && ConfigurationDescriptor.Raw_INEndpoint.EndpointSize == 32);
    assert(get_descriptor(USB_DESCR_TYP_DEVICE,0,0,8,actual) == 8);
    assert(!memcmp(actual,&DeviceDescriptor,8));
    assert(get_descriptor(USB_DESCR_TYP_CONFIG,0,0,65535,actual) == sizeof(ConfigurationDescriptor));
    assert(!memcmp(actual,&ConfigurationDescriptor,sizeof(ConfigurationDescriptor)));
    assert(get_descriptor(USB_DESCR_TYP_REPORT,0,RAW_INTERFACE,255,actual) == RawReport_size);
    assert(!memcmp(actual,RawReport,RawReport_size));
    assert(get_descriptor(USB_DESCR_TYP_REPORT,0,SHARED_INTERFACE,65535,actual) == ConfigurationDescriptor.Shared_HID.HIDReportLength);
    assert(!memcmp(actual,SharedReport,ConfigurationDescriptor.Shared_HID.HIDReportLength));
    assert(get_descriptor(USB_DESCR_TYP_STRING,0,0,255,actual) == 4);
    assert(!memcmp(actual,"\x04\x03\x09\x04",4));
    expect_string(1,MANUFACTURER);
    expect_string(2,PRODUCT);
    expect_string(3,SERIAL_NUMBER);
    setup(0x80,USB_GET_DESCRIPTOR,0x0309,0x0409,255);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
    setup(0x81,USB_GET_DESCRIPTOR,0x2200,255,255);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
}

static void test_hid_control(void) {
    uint8_t led = 5;
    fresh(); configure();
    setup(0x21,HID_SET_PROTOCOL,0,KEYBOARD_INTERFACE,0);
    assert(keyboard_protocol == 0); in(0);
    setup(0xa1,HID_GET_PROTOCOL,0,KEYBOARD_INTERFACE,1);
    assert(D0_EP0T_L == 1 && pD0_EP0_BUF[0] == 0); in(0); out(NULL,0,true);
    setup(0x21,HID_SET_IDLE,0x1200,KEYBOARD_INTERFACE,0);
    assert(keyboard_idle == 0x12); in(0);
    setup(0x21,HID_SET_REPORT,0x0200,KEYBOARD_INTERFACE,1);
    out(&led,1,false); assert(KB_USB_SetReport == 0);
    out(&led,1,true); assert(KB_USB_SetReport == 5); in(0);
    uint8_t shared[2] = {REPORT_ID_NKRO,2};
    setup(0x21,HID_SET_REPORT,0x0200 | REPORT_ID_NKRO,SHARED_INTERFACE,2);
    out(shared,2,true); assert(KB_USB_SetReport == 2); in(0);
    uint8_t keyboard[8] = {1,0,4,0,0,0,0,0};
    assert(ak820_usb_send(1,keyboard,8)); in(1);
    setup(0xa1,HID_GET_REPORT,0x0100,KEYBOARD_INTERFACE,64);
    assert(D0_EP0T_L == 8 && !memcmp((const void *)pD0_EP0_BUF,keyboard,8));
    in(0); out(NULL,0,true);
    uint8_t consumer[3] = {REPORT_ID_CONSUMER,0xe9,0};
    uint8_t system[3] = {REPORT_ID_SYSTEM,0x81,0};
    assert(ak820_usb_send(2,consumer,3)); in(2);
    assert(ak820_usb_send(2,system,3)); in(2);
    setup(0xa1,HID_GET_REPORT,0x0100 | REPORT_ID_CONSUMER,SHARED_INTERFACE,64);
    assert(D0_EP0T_L == 3 && !memcmp((const void *)pD0_EP0_BUF,consumer,3));
    in(0); out(NULL,0,true);
    setup(0xa1,HID_GET_REPORT,0x0200 | REPORT_ID_NKRO,SHARED_INTERFACE,64);
    assert(D0_EP0T_L == 2 && pD0_EP0_BUF[0] == REPORT_ID_NKRO && pD0_EP0_BUF[1] == 2);
    in(0); out(NULL,0,true);
#ifdef MOUSE_ENABLE
    uint8_t mouse[sizeof(report_mouse_t)] = {REPORT_ID_MOUSE,1,2,3,0,0};
    assert(ak820_usb_send(2,mouse,sizeof(mouse))); in(2);
    setup(0xa1,HID_GET_REPORT,0x0100 | REPORT_ID_MOUSE,SHARED_INTERFACE,64);
    assert(D0_EP0T_L == sizeof(mouse) && !memcmp((const void *)pD0_EP0_BUF,mouse,sizeof(mouse)));
    in(0); out(NULL,0,true);
#else
    setup(0xa1,HID_GET_REPORT,0x0100 | REPORT_ID_MOUSE,SHARED_INTERFACE,64);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
#endif
    setup(0,USB_SET_CONFIGURATION,0,0,0);
    assert(!USB_EnumStatus && !D0UsbConfig); in(0);
    assert(!ak820_usb_send(1,&led,1));
}

static void test_raw_lifecycle(void) {
    uint8_t packet[32];
    for (uint8_t i = 0; i < 32; ++i) packet[i] = i;
    fresh(); configure(); raw_request(packet);
    assert(received == 0); /* no QMK or flash work runs inside the interrupt */
    ak820_usb_raw_task();
    assert(received == 1 && begins == 1 && flushes == 1 && ends == 1 && raw_state == RAW_TX_WAIT);
    assert(D0_EP3T_L == 32 && (D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_ACK);
    for (uint8_t i = 0; i < 32; ++i) assert(pUSB_BUF_DEV0[UX_EP3_ADDR + i] == (i ^ 0xa5));
    assert(!(D0_EP3RES & bUEP_X_TOG)); /* first data packet must be DATA0 */
    in(3); assert(raw_state == RAW_IDLE && (D0_EP3RES & bUEP_X_TOG));
    for (callback_mode = 1; callback_mode <= 3; ++callback_mode) {
        if (!D0UsbConfig) configure();
        raw_request(packet); ak820_usb_raw_task();
        if (callback_mode == 1) { assert(raw_state == RAW_TX_WAIT); in(3); }
        else assert(raw_state == RAW_IDLE);
    }
    assert(begins == ends);
    fresh(); configure(); raw_request(packet); nvm_good = false;
    ak820_usb_raw_task();
    assert(flushes == 1 && ends == 1 && raw_state == RAW_IDLE);
    assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK && D0_EP3T_L == 0);
    setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,31);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
    setup(0x21,HID_SET_REPORT,0x0200,RAW_INTERFACE,32);
    out(packet,31,true); assert(raw_state == RAW_IDLE && (D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
}

/* Explicit expected wire requests; the loops also cover every unknown byte
 * value at each command/subcommand level. Actual VIA/Vial authorization is
 * outside this transport harness and is not replaced by the reply whitelist. */
static const uint8_t recovery_requests[][3] = {
    {id_get_protocol_version,0,0}, {id_dynamic_keymap_get_keycode,0,0},
    {id_dynamic_keymap_macro_get_count,0,0}, {id_dynamic_keymap_macro_get_buffer_size,0,0},
    {id_dynamic_keymap_macro_get_buffer,0,0}, {id_dynamic_keymap_get_layer_count,0,0},
    {id_dynamic_keymap_get_buffer,0,0}, {id_bootloader_jump,0,0},
    {id_get_keyboard_value,id_uptime,0}, {id_get_keyboard_value,id_layout_options,0},
    {id_get_keyboard_value,id_switch_matrix_state,0}, {id_get_keyboard_value,id_firmware_version,0},
    {id_lighting_get_value,vialrgb_get_info,0}, {id_lighting_get_value,vialrgb_get_mode,0},
    {id_lighting_get_value,vialrgb_get_supported,0}, {id_lighting_get_value,vialrgb_get_number_leds,0},
    {id_lighting_get_value,vialrgb_get_led_info,0},
    {id_vial_prefix,vial_get_keyboard_id,0}, {id_vial_prefix,vial_get_size,0},
    {id_vial_prefix,vial_get_def,0}, {id_vial_prefix,vial_get_encoder,0},
    {id_vial_prefix,vial_get_unlock_status,0}, {id_vial_prefix,vial_unlock_start,0},
    {id_vial_prefix,vial_unlock_poll,0}, {id_vial_prefix,vial_lock,0},
    {id_vial_prefix,vial_qmk_settings_query,0}, {id_vial_prefix,vial_qmk_settings_get,0},
    {id_vial_prefix,vial_dynamic_entry_op,dynamic_vial_get_number_of_entries},
    {id_vial_prefix,vial_dynamic_entry_op,dynamic_vial_tap_dance_get},
    {id_vial_prefix,vial_dynamic_entry_op,dynamic_vial_combo_get},
    {id_vial_prefix,vial_dynamic_entry_op,dynamic_vial_key_override_get},
};

static void faulted_request(const uint8_t packet[32], bool allowed, unsigned mode) {
    fresh(); configure(); nvm_good = false; callback_mode = mode;
    raw_request(packet); ak820_usb_raw_task();
    assert(received == 1 && begins == 1 && flushes == 1 && ends == 1);
    assert(raw_state == (allowed ? RAW_TX_WAIT : RAW_IDLE));
    assert((D0_EP3RES & MASK_UEP_X_RES) == (allowed ? UEP_X_RES_ACK : UEP_X_RES_NAK));
    assert(!raw_reply_without_nvm);
    if (allowed) {
        assert(D0_EP3T_L == 32 && pUSB_BUF_DEV0[UX_EP3_ADDR] == (mode == 5 ? 0xff : id_get_protocol_version));
        in(3); assert(raw_state == RAW_IDLE);
    }
}

static void test_recovery_reply_policy(void) {
    uint8_t packet[32] = {0};
    for (unsigned group = 0; group < 5; ++group) {
        for (unsigned value = 0; value < 256; ++value) {
            packet[0] = group == 0 ? value : group == 3 ? id_get_keyboard_value : group == 4 ? id_lighting_get_value : id_vial_prefix;
            packet[1] = group == 0 ? 0 : group == 2 ? vial_dynamic_entry_op : value;
            packet[2] = group == 2 ? value : 0;
            if (group == 0 && value == 0xfd) continue; /* separate FD00 tests */
            bool allowed = false;
            for (size_t i = 0; i < sizeof(recovery_requests) / sizeof(recovery_requests[0]); ++i)
                if (!memcmp(packet,recovery_requests[i],3)) allowed = true;
            faulted_request(packet,allowed,4);
        }
    }
    for (size_t i = 0; i < sizeof(recovery_requests) / sizeof(recovery_requests[0]); ++i) {
        memcpy(packet,recovery_requests[i],3);
        faulted_request(packet,true,5);
    }

    /* A reset cancels an otherwise allowed reply, and the exemption cannot
     * leak into a later settings write. An early IN drain retains ownership. */
    fresh(); configure(); nvm_good = false; callback_mode = 2;
    packet[0] = id_vial_prefix; packet[1] = vial_unlock_poll; packet[2] = 0;
    raw_request(packet); ak820_usb_raw_task();
    assert(raw_state == RAW_IDLE && !USB_EnumStatus && !raw_reply_without_nvm);
    assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK);
    configure(); callback_mode = 4;
    packet[0] = id_dynamic_keymap_set_keycode;
    raw_request(packet); ak820_usb_raw_task();
    assert(raw_state == RAW_IDLE && (D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK);
    callback_mode = 3; packet[0] = id_get_protocol_version;
    raw_request(packet); ak820_usb_raw_task();
    assert(raw_state == RAW_IDLE && !raw_reply_without_nvm);
}

static void test_halt_reset_and_diagnostics(void) {
    uint8_t packet[32] = {0};
    const struct { uint16_t address; uint8_t count; bool valid; } cases[] = {
        {0xffe5,27,true}, {0xffff,1,true}, {0xffff,0,true},
        {0xffff,2,false}, {0x0000,28,false}
    };
    fresh(); configure();
    setup(2,USB_SET_FEATURE,0,0x81,0); in(0);
    assert((D0_EP1RES & MASK_UEP_X_RES) == UEP_X_RES_STALL && !ak820_usb_send(1,packet,8));
    setup(2,USB_CLEAR_FEATURE,0,0x81,0); in(0);
    assert(D0_EP1RES == (bUEP_X_AUTO_TOG | UEP_X_RES_NAK) && ak820_usb_send(1,packet,8));
    reset(); assert(raw_state == RAW_IDLE && KB_USB_SetReport == 0 && keyboard_protocol == 1 && keyboard_idle == 0);

    for (uint32_t i = 0; i < 65536; ++i) test_rom[i] = i ^ (i >> 8);
    for (unsigned fault = 0; fault < 2; ++fault) {
        fresh(); configure(); nvm_good = !fault;
        for (size_t c = 0; c < sizeof(cases) / sizeof(cases[0]); ++c) {
            packet[0] = 0xfd; packet[1] = 0;
            packet[2] = cases[c].address >> 8; packet[3] = cases[c].address;
            packet[4] = cases[c].count;
            code_reads = 0;
            raw_request(packet); ak820_usb_raw_task();
            assert(received == 0 && begins == 0 && flushes == 0 && ends == 0);
            assert(raw_state == RAW_TX_WAIT && D0_EP3T_L == 32);
            assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_ACK);
            assert(pUSB_BUF_DEV0[UX_EP3_ADDR] == 0xfd);
            assert(pUSB_BUF_DEV0[UX_EP3_ADDR + 1] == (cases[c].valid ? 0 : 0xff));
            uint8_t count = cases[c].valid ? cases[c].count : 0;
            assert(code_reads == count && pUSB_BUF_DEV0[UX_EP3_ADDR + 4] == count);
            for (uint8_t i = 0; i < 27; ++i)
                assert(pUSB_BUF_DEV0[UX_EP3_ADDR + 5 + i] == (i < count ? test_rom[cases[c].address + i] : 0));
            in(3); assert(raw_state == RAW_IDLE);
        }
        /* FD01 must not route through NVM, even with a dirty/faulted cache or
         * while Vial unlock blocks ordinary commands. Repeated reads preserve
         * the complete snapshot and publish only the new diagnostic reply. */
        packet[1] = 1;
        const uint8_t nv[] = {fault, 1, 1, 7, 2, 0, 12};
        const uint8_t iap[] = {1, 0x9a, 0x40, 0x42, 0x80, 0xc7};
        memcpy(nvm_diagnostic_bytes, nv, sizeof(nv));
        memcpy(ak820_flash_diagnostic, iap, sizeof(iap));
        vial_unlocked = 0; vial_unlock_in_progress = 1;
        for (unsigned repeat = 0; repeat < 2; ++repeat) {
            raw_request(packet); ak820_usb_raw_task();
            assert(!received && !begins && !flushes && !ends);
            assert(raw_state == RAW_TX_WAIT && D0_EP3T_L == 32);
            assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_ACK);
            const volatile uint8_t *response = pUSB_BUF_DEV0 + UX_EP3_ADDR;
            assert(response[0] == 0xfd && response[1] == 1 && response[2] == 1 && response[3] == 0xa8);
            assert(!memcmp((const void *)(response + 4), nv, sizeof(nv)));
            assert(!memcmp((const void *)(response + 11), iap, sizeof(iap)));
            assert(response[17] == 0 && response[18] == 1 && response[19] == 1 && response[20] == 0 && response[21] == RAW_WORK);
            for (uint8_t i = 22; i < 32; ++i) assert(response[i] == 0);
            assert(!memcmp(nvm_diagnostic_bytes, nv, sizeof(nv)) && !memcmp(ak820_flash_diagnostic, iap, sizeof(iap)));
            in(3); assert(raw_state == RAW_IDLE);
        }
        vial_unlock_in_progress = 0;
        /* Unknown FD subcommands retain the existing fail-closed behavior. */
        packet[1] = 2;
        raw_request(packet); ak820_usb_raw_task();
        assert(received == 1 && begins == 1 && flushes == 1 && ends == 1);
        assert(raw_state == (fault ? RAW_IDLE : RAW_TX_WAIT));
        assert((D0_EP3RES & MASK_UEP_X_RES) == (fault ? UEP_X_RES_NAK : UEP_X_RES_ACK));
    }

    fresh(); configure(); nvm_good = false;
    packet[1] = 0; packet[4] = 1;
    raw_request(packet); reset_during_read = true; ak820_usb_raw_task();
    assert(code_reads == 1 && raw_state == RAW_IDLE && !USB_EnumStatus);
    assert(!received && !begins && !flushes && !ends && (D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK);
}

static void test_boot_feature(void) {
    fresh(); configure();
    nvm_good = false;
    /* Main can be stalled with a pending Raw request. EP0 diagnostics must
     * still finish without dispatching it or touching NVM/EP3 ownership. */
    raw_state = RAW_WORK;
    for (uint8_t stage = 1; stage <= 3; ++stage) {
        ak820_boot_stage = stage;
        ak820_main_heartbeat = (uint8_t)(stage * 83);
        USB_SleepStatus = stage == 2 ? 2 : 0;
        const uint8_t expected[] = {'A','K','B','T',1,stage,(uint8_t)(stage * 83),stage == 2 ? 3 : 1};
        const uint8_t lengths[] = {1,8,64};
        for (uint8_t i = 0; i < sizeof(lengths); ++i) {
            setup(0xa1,HID_GET_REPORT,0x0300,RAW_INTERFACE,lengths[i]);
            assert(D0_EP0T_L == (lengths[i] < 8 ? lengths[i] : 8));
            assert(!memcmp((const void *)pD0_EP0_BUF,expected,D0_EP0T_L));
            assert(raw_state == RAW_WORK && !received && !begins && !flushes && !ends);
            assert((D0_EP3RES & MASK_UEP_X_RES) == UEP_X_RES_NAK);
            in(0); out(NULL,0,true);
        }
    }
    /* A Feature SET_REPORT, unknown ID or other interface cannot write the
     * diagnostic state. Read-only is enforced by the actual controller. */
    setup(0x21,HID_SET_REPORT,0x0300,RAW_INTERFACE,8);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
    setup(0xa1,HID_GET_REPORT,0x0301,RAW_INTERFACE,8);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
    setup(0xa1,HID_GET_REPORT,0x0300,KEYBOARD_INTERFACE,8);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
    assert(ak820_boot_stage == 3 && ak820_main_heartbeat == 249 && raw_state == RAW_WORK);
    reset();
    setup(0xa1,HID_GET_REPORT,0x0300,RAW_INTERFACE,8);
    assert((D0_EP0RES & MASK_UEP_T_RES) == UEP_T_RES_STALL);
}

int main(void) {
    test_setup_registers_and_order();
    test_descriptors();
    test_hid_control();
    test_raw_lifecycle();
    test_recovery_reply_policy();
    test_halt_reset_and_diagnostics();
    test_boot_feature();
    puts("PASS: production AK820 USB/descriptor sources: stale RX_LEN, ordered two-ACK SETUP, UTF-16 strings, EP0 segmentation, HID control, Raw32 ownership/reset, original-request recovery whitelist, persistence gate, read-only FD00/FD01 and EP0 AKBT diagnostics");
}
