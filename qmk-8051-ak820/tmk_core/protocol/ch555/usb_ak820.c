#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* SDCC 4.6: keep loop expressions local to reduce AK820 CODE. */
#pragma noinvariant
#endif

/* SPDX-License-Identifier: GPL-2.0-or-later
 * AK820/VS11K28A USB device transport. The original loader calls this service
 * through its register-saving IRQ wrapper, so USB_DeviceInterrupt returns RET.
 * All control work is private to that service; QMK and NVM run only in main.
 */
#ifdef AK820_USB_HOST_TEST
#    include "ak820_usb_test_shim.h"
#else
#    include "usb_device.h"
#    include "usb_ak820.h"
#    include "report.h"
#    include "raw_hid.h"
#    include "wait.h"
#    include "hal.h"
#endif
#include "via.h"
#include "vial.h"
#include "vialrgb.h"
#include "keyboards/ajazz/ak820/ak820_nvm.h"

#ifndef AK820_USB_HOST_TEST
#    define EP_RESPONSE(ep) (*((volatile uint8_t __xdata *)(0x2200u + (ep))))
#    define EP_LENGTH(ep) (*((volatile uint8_t __xdata *)(0x2208u + (ep))))
#    define ACK_TRANSFER() (D0_STATUS = 0)
#    define ACK_RESET() (USB_IF = bUX_IF_BUS_RST)
#    define ACK_SUSPEND() (USB_IF = bUX_IF_SUSPEND)
#    define ACK_ALL() (USB_IF = 0xff)
#    define READ_CODE(address) (*((const uint8_t __code *)(address)))
#endif

extern volatile uint8_t keyboard_protocol;
extern volatile uint8_t keyboard_idle;
extern bool ak820_nvm_ok(void);
extern void ak820_nvm_begin(void);
extern void ak820_nvm_flush(void);
extern void ak820_nvm_end(void);

volatile UINT8 D0SetupReqCode;
volatile UINT16 D0SetupLen;
volatile PUINT8 pD0Descr; /* retained ABI; descriptor transfers use code pointers */
volatile UINT8 D0UsbConfig;
volatile UINT8 USB_EnumStatus;
volatile UINT8 USB_SleepStatus;
volatile UINT8 MCU_Sleep_Operate;
volatile UINT8 KB_USB_UpStatus;
volatile UINT8 KB_USB_SetReport;
volatile __xdata uint8_t ak820_boot_stage;
volatile __xdata uint8_t ak820_main_heartbeat;

enum { RAW_IDLE, RAW_RX, RAW_READY, RAW_WORK, RAW_TX_ACTIVE, RAW_TX_WAIT,
       RAW_DRAINED, RAW_CANCELLED };
enum { CTRL_IDLE, CTRL_DATA_IN, CTRL_STATUS_OUT, CTRL_STATUS_IN, CTRL_DATA_OUT };
enum { OUTPUT_NONE, OUTPUT_RAW, OUTPUT_LED, OUTPUT_SHARED_LED };

static volatile __xdata uint8_t raw_state;
static __xdata uint8_t raw_buffer[RAW_EPSIZE];
static bool raw_reply_without_nvm; /* main only; classified before handler edits */
static volatile __xdata uint8_t keyboard_reset;
/* Keep each report independently: EP2 multiplexes several report IDs. */
#define SNAPSHOT_KEYBOARD 0
#define SNAPSHOT_NKRO 8
#define SNAPSHOT_MOUSE (SNAPSHOT_NKRO + SHARED_EPSIZE)
#ifdef MOUSE_ENABLE
#    define SNAPSHOT_MOUSE_LENGTH sizeof(report_mouse_t)
#else
#    define SNAPSHOT_MOUSE_LENGTH 0
#endif
#define SNAPSHOT_SYSTEM (SNAPSHOT_MOUSE + SNAPSHOT_MOUSE_LENGTH)
#define SNAPSHOT_CONSUMER (SNAPSHOT_SYSTEM + sizeof(report_extra_t))
#define SNAPSHOT_SIZE (SNAPSHOT_CONSUMER + sizeof(report_extra_t))
static __xdata uint8_t input_snapshot[SNAPSHOT_SIZE];
static const __code uint8_t shared_offsets[] = {0,0,SNAPSHOT_MOUSE,SNAPSHOT_SYSTEM,SNAPSHOT_CONSUMER,0,SNAPSHOT_NKRO};
static const __code uint8_t shared_lengths[] = {0,0,SNAPSHOT_MOUSE_LENGTH,sizeof(report_extra_t),sizeof(report_extra_t),0,SHARED_EPSIZE};
static __xdata uint8_t control_phase;
static __xdata uint8_t output_kind;
static __xdata uint8_t output_report_id;
static __xdata uint8_t control_zlp;
static const uint8_t __code *control_pointer;

/* These functions are reachable only from the interrupt service. Giving them
 * private storage prevents SDCC overlay allocation across main/IRQ calls. No
 * memcpy, generic-pointer helper or QMK function is called from this path. */
#pragma save
#pragma nooverlay

static void raw_abort(void) {
    if (raw_state == RAW_WORK || raw_state == RAW_TX_ACTIVE ||
        raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED)
        raw_state = RAW_CANCELLED;
    else
        raw_state = RAW_IDLE;
    output_kind = OUTPUT_NONE;
}

static void raw_complete(void) {
    if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_DRAINED;
    else if (raw_state == RAW_TX_WAIT) raw_state = RAW_IDLE;
}

static void endpoints_reset(void) {
    uint8_t i;
    /* Match native SIE configuration: IN on EP1/2/3, automatic DATA toggles. */
    D0_EP_MOD = bUX_DEV_EN;
    D0_EP1RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
    D0_EP2RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
    D0_EP3RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
    D0_EP1T_L = D0_EP2T_L = D0_EP3T_L = 0;
    for (i = 0; i < SNAPSHOT_SIZE; ++i) input_snapshot[i] = 0;
    input_snapshot[SNAPSHOT_NKRO] = REPORT_ID_NKRO;
#ifdef MOUSE_ENABLE
    input_snapshot[SNAPSHOT_MOUSE] = REPORT_ID_MOUSE;
#endif
    input_snapshot[SNAPSHOT_SYSTEM] = REPORT_ID_SYSTEM;
    input_snapshot[SNAPSHOT_CONSUMER] = REPORT_ID_CONSUMER;
    for (i = 0; i < RAW_EPSIZE; ++i) pUSB_BUF_DEV0[UX_EP3_ADDR + i] = 0;
    raw_abort();
}

static void control_stall(void) {
    if (raw_state == RAW_RX) raw_state = RAW_IDLE;
    output_kind = OUTPUT_NONE;
    control_phase = CTRL_IDLE;
    D0SetupReqCode = 0xff;
    /* STALL persists until the next SETUP; a timed automatic unstall is wrong. */
    D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
}

static void control_next(void) {
    uint8_t i;
    uint8_t length = D0SetupLen > DEF_ENDP0_SIZE ? DEF_ENDP0_SIZE : D0SetupLen;
    for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = *control_pointer++;
    D0SetupLen -= length;
    if (!length) control_zlp = 0;
    D0_EP0T_L = length;
    D0_EP0RES = (D0_EP0RES & (bUEP_T_TOG | bUEP_R_TOG)) | UEP_T_RES_ACK | UEP_R_RES_ACK;
}

/* Interface numbers index this private CODE-only descriptor table. */
typedef struct {
    const uint8_t __code *report;
    const USB_HID_Descriptor_HID_t __code *hid;
} interface_descriptors_t;
static const interface_descriptors_t __code interface_descriptors[TOTAL_INTERFACES] = {
    [KEYBOARD_INTERFACE] = {(const uint8_t __code *)KeyboardReport, &ConfigurationDescriptor.Keyboard_HID},
    [RAW_INTERFACE] = {(const uint8_t __code *)RawReport, &ConfigurationDescriptor.Raw_HID},
#ifdef SHARED_EP_ENABLE
    [SHARED_INTERFACE] = {(const uint8_t __code *)SharedReport, &ConfigurationDescriptor.Shared_HID},
#endif
};

/* Descriptor indexes are checked before the EP0 buffer can be overwritten. */
static uint16_t descriptor_select(uint8_t type, uint8_t index, uint16_t interface) {
    if (type == USB_DESCR_TYP_DEVICE && !index && !interface) {
        control_pointer = (const uint8_t __code *)&DeviceDescriptor;
        return sizeof(DeviceDescriptor);
    }
    if (type == USB_DESCR_TYP_CONFIG && !index && !interface) {
        control_pointer = (const uint8_t __code *)&ConfigurationDescriptor;
        return sizeof(ConfigurationDescriptor);
    }
    if (type == USB_DESCR_TYP_STRING) {
        if (interface != 0 && interface != 0x0409) return 0;
        switch (index) {
            case 0: control_pointer = (const uint8_t __code *)&LanguageString; return LanguageString.Header.Size;
            case 1: control_pointer = (const uint8_t __code *)&ManufacturerString; return ManufacturerString.Header.Size;
            case 2: control_pointer = (const uint8_t __code *)&ProductString; return ProductString.Header.Size;
#ifdef SERIAL_NUMBER
            case 3: control_pointer = (const uint8_t __code *)&SerialNumberString; return SerialNumberString.Header.Size;
#endif
            default: return 0;
        }
    }
    if (index || interface >= TOTAL_INTERFACES) return 0;
    if (type == USB_DESCR_TYP_REPORT || type == USB_DESCR_TYP_HID) {
        const USB_HID_Descriptor_HID_t __code *hid = interface_descriptors[interface].hid;
        if (!hid) return 0;
        if (type == USB_DESCR_TYP_REPORT) {
            control_pointer = interface_descriptors[interface].report;
            return hid->HIDReportLength;
        }
        control_pointer = (const uint8_t __code *)hid;
        return 9;
    }
    return 0;
}

static void control_setup(void) {
    uint8_t type = pD0_SETUP_REQ->bRequestType;
    uint16_t value = pD0_SETUP_REQ->wValueL | ((uint16_t)pD0_SETUP_REQ->wValueH << 8);
    uint16_t index = pD0_SETUP_REQ->wIndexL | ((uint16_t)pD0_SETUP_REQ->wIndexH << 8);
    uint16_t length;
    /* These predicates use this SETUP packet only. No branch tests them after
     * changing D0SetupLen, and this service is not reentrant. */
    __bit valid_interface = index < TOTAL_INTERFACES;
    __bit zero_index = !index;
    __bit zero_value = !value;
    __bit zero_length;
    uint8_t endpoint;
    uint8_t i;
    uint8_t offset = 0;
    uint8_t report_id;
    if (raw_state == RAW_RX) raw_state = RAW_IDLE; /* abort only unfinished OUT */
    output_kind = OUTPUT_NONE;
    control_phase = CTRL_IDLE;
    control_zlp = 0;
    D0SetupReqCode = pD0_SETUP_REQ->bRequest;
    D0SetupLen = pD0_SETUP_REQ->wLengthL | ((uint16_t)pD0_SETUP_REQ->wLengthH << 8);
    zero_length = !D0SetupLen;
    D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
    D0_EP0T_L = 0;

    /* Dispatch the request byte once; recipient, direction and every field
     * remain checked in the request-specific predicates below. */
    switch (D0SetupReqCode) {
        case USB_GET_DESCRIPTOR:
            if (type == 0x80 || type == 0x81) {
                if (((value >> 8) == USB_DESCR_TYP_HID || (value >> 8) == USB_DESCR_TYP_REPORT) != (type == 0x81)) {
                    control_stall(); return;
                }
                length = descriptor_select(value >> 8, value, index);
                if (!length) { control_stall(); return; }
                control_zlp = length < D0SetupLen && !(length & (DEF_ENDP0_SIZE - 1));
                if (D0SetupLen > length) D0SetupLen = length;
                control_phase = D0SetupLen ? CTRL_DATA_IN : CTRL_STATUS_OUT;
                if (D0SetupLen) control_next();
                return;
            } else { control_stall(); return; }
        case USB_SET_ADDRESS:
            if (type == 0x00 && zero_index && zero_length && value <= 127) {
                D0SetupLen = value; /* applied after status-IN ACK */
                control_phase = CTRL_STATUS_IN;
            } else { control_stall(); return; }
            break;
        case USB_SET_CONFIGURATION: /* HID_SET_REPORT has the same request byte. */
            if (type == 0x00 && zero_index && zero_length && value <= 1) {
                endpoints_reset();
                D0UsbConfig = value;
                USB_EnumStatus = value != 0;
                keyboard_reset = 1;
                control_phase = CTRL_STATUS_IN;
            } else if (type == 0x21 && D0UsbConfig) {
                if (index == RAW_INTERFACE && value == 0x0200 && D0SetupLen == RAW_EPSIZE && raw_state == RAW_IDLE) {
                    raw_state = RAW_RX;
                    output_kind = OUTPUT_RAW;
                } else if (index == KEYBOARD_INTERFACE && value == 0x0200 && D0SetupLen == 1) {
                    output_kind = OUTPUT_LED;
#if defined(NKRO_ENABLE) && defined(SHARED_EP_ENABLE)
                } else if (index == SHARED_INTERFACE && value == (0x0200 | REPORT_ID_NKRO) && D0SetupLen == 2) {
                    output_kind = OUTPUT_SHARED_LED;
                    output_report_id = REPORT_ID_NKRO;
#endif
                } else { control_stall(); return; }
                control_phase = CTRL_DATA_OUT;
                return; /* OUT data must arrive before status-IN becomes ACK */
            } else { control_stall(); return; }
            break;
        case USB_GET_CONFIGURATION:
            if (type == 0x80 && zero_index && zero_value && D0SetupLen == 1) {
                pD0_EP0_BUF[0] = D0UsbConfig;
                D0_EP0T_L = 1;
                control_phase = CTRL_STATUS_OUT;
            } else { control_stall(); return; }
            break;
        case USB_GET_INTERFACE: /* DEF_USB_SET_IDLE has the same request byte. */
            if (type == 0x81 && valid_interface && zero_value && D0SetupLen == 1 && D0UsbConfig) {
                pD0_EP0_BUF[0] = 0;
                D0_EP0T_L = 1;
                control_phase = CTRL_STATUS_OUT;
            } else if (valid_interface && D0UsbConfig && type == 0x21 && zero_length) {
                if (index == KEYBOARD_INTERFACE) keyboard_idle = value >> 8;
                control_phase = CTRL_STATUS_IN;
            } else { control_stall(); return; }
            break;
        case USB_SET_INTERFACE: /* DEF_USB_SET_PROTOCOL has the same request byte. */
            if (type == 0x01 && valid_interface && zero_value && zero_length && D0UsbConfig) {
                control_phase = CTRL_STATUS_IN;
            } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0x21 && zero_length && value <= 1) {
                keyboard_protocol = value;
                keyboard_reset = 1;
                control_phase = CTRL_STATUS_IN;
            } else { control_stall(); return; }
            break;
        case USB_GET_STATUS:
            if (zero_value && D0SetupLen == 2 &&
                ((type == 0x80 && zero_index) || (type == 0x81 && valid_interface && D0UsbConfig) ||
                 (type == 0x82 && D0UsbConfig && (index == 0 || index == 0x80 || (index >= 0x81 && index <= 0x83))))) {
                endpoint = index & 7;
                pD0_EP0_BUF[0] = type == 0x80 ? ((USB_SleepStatus & 1) << 1) :
                    ((type == 0x82 && endpoint && (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_STALL) ? 1 : 0);
                pD0_EP0_BUF[1] = 0;
                D0_EP0T_L = 2;
                control_phase = CTRL_STATUS_OUT;
            } else { control_stall(); return; }
            break;
        case USB_CLEAR_FEATURE: /* HID_GET_REPORT has the same request byte. */
        case USB_SET_FEATURE: /* DEF_USB_GET_PROTOCOL has the same request byte. */
            if (zero_length && D0UsbConfig) {
                if (type == 0x00 && value == 1 && zero_index) {
                    if (D0SetupReqCode == USB_SET_FEATURE) USB_SleepStatus |= 1;
                    else USB_SleepStatus &= ~1;
                } else if (type == 0x02 && zero_value && index >= 0x81 && index <= 0x83) {
                    endpoint = index & 7;
                    /* Clearing HALT restarts DATA0 and discards any undelivered packet. */
                    EP_RESPONSE(endpoint) = bUEP_X_AUTO_TOG | (D0SetupReqCode == USB_SET_FEATURE ? UEP_X_RES_STALL : UEP_X_RES_NAK);
                    if (endpoint == RAW_IN_EPNUM) raw_complete();
                } else { control_stall(); return; }
                control_phase = CTRL_STATUS_IN;
            } else if (type == 0xa1 && D0SetupReqCode == HID_GET_REPORT && D0UsbConfig && D0SetupLen) {
                report_id = value;
                if ((value >> 8) == 1 && index == KEYBOARD_INTERFACE && !report_id) {
                    length = KEYBOARD_EPSIZE;
                    offset = SNAPSHOT_KEYBOARD;
                } else if ((value >> 8) == 1 && index == SHARED_INTERFACE &&
                           report_id < sizeof(shared_lengths) && shared_lengths[report_id]) {
                    length = shared_lengths[report_id];
                    offset = shared_offsets[report_id];
                } else if ((value >> 8) == 1 && index == RAW_INTERFACE && !report_id) {
                    length = D0SetupLen < RAW_EPSIZE ? D0SetupLen : RAW_EPSIZE;
                    for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = pUSB_BUF_DEV0[UX_EP3_ADDR + i];
                    length = 0; /* data already copied */
                } else if (value == 0x0200 && index == KEYBOARD_INTERFACE) {
                    pD0_EP0_BUF[0] = KB_USB_SetReport;
                    length = 0;
                    D0SetupLen = 1;
                } else if (value == (0x0200 | REPORT_ID_NKRO) && index == SHARED_INTERFACE) {
                    pD0_EP0_BUF[0] = REPORT_ID_NKRO;
                    pD0_EP0_BUF[1] = KB_USB_SetReport;
                    length = 0;
                    if (D0SetupLen > 2) D0SetupLen = 2;
                } else if (value == 0x0300 && index == RAW_INTERFACE) {
                    /* Read-only EP0 Feature report, independent of Raw HID main-loop
                     * dispatch and EP3. Never flush NVM or change raw_state here. */
                    pD0_EP0_BUF[0] = 'A';
                    pD0_EP0_BUF[1] = 'K';
                    pD0_EP0_BUF[2] = 'B';
                    pD0_EP0_BUF[3] = 'T';
                    pD0_EP0_BUF[4] = 1;
                    pD0_EP0_BUF[5] = ak820_boot_stage;
                    pD0_EP0_BUF[6] = ak820_main_heartbeat;
                    pD0_EP0_BUF[7] = (USB_EnumStatus ? 1 : 0) | (USB_SleepStatus & 2);
                    length = 0;
                    if (D0SetupLen > 8) D0SetupLen = 8;
                } else { control_stall(); return; }
                if (length) {
                    if (D0SetupLen > length) D0SetupLen = length;
                    for (i = 0; i < D0SetupLen; ++i) pD0_EP0_BUF[i] = input_snapshot[offset + i];
                } else if (index == RAW_INTERFACE && D0SetupLen > RAW_EPSIZE) D0SetupLen = RAW_EPSIZE;
                D0_EP0T_L = D0SetupLen;
                control_phase = CTRL_STATUS_OUT;
            } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0xa1 && D0SetupReqCode == DEF_USB_GET_PROTOCOL && zero_value && D0SetupLen == 1) {
                pD0_EP0_BUF[0] = keyboard_protocol;
                D0_EP0T_L = 1;
                control_phase = CTRL_STATUS_OUT;
            } else { control_stall(); return; }
            break;
        case DEF_USB_GET_IDLE:
            if (valid_interface && D0UsbConfig && type == 0xa1 && !(value >> 8) && D0SetupLen == 1) {
                pD0_EP0_BUF[0] = index == KEYBOARD_INTERFACE ? keyboard_idle : 0;
                D0_EP0T_L = 1;
                control_phase = CTRL_STATUS_OUT;
            } else { control_stall(); return; }
            break;
        default: control_stall(); return;
    }
    D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
}

static void control_out(void) {
    uint8_t i;
    if (!(D0_STATUS & bUXS_TOG_OK)) return; /* duplicate OUT is not a new request */
    if (control_phase == CTRL_STATUS_OUT && D0_RX_LEN == 0) {
        control_phase = CTRL_IDLE;
        D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
        return;
    }
    if (control_phase != CTRL_DATA_OUT || D0_RX_LEN != D0SetupLen) { control_stall(); return; }
    if (output_kind == OUTPUT_RAW && raw_state == RAW_RX) {
        for (i = 0; i < RAW_EPSIZE; ++i) raw_buffer[i] = pD0_EP0_BUF[i];
        raw_state = RAW_READY; /* publish only after the entire packet is copied */
    } else if (output_kind == OUTPUT_LED) {
        KB_USB_SetReport = pD0_EP0_BUF[0];
    } else if (output_kind == OUTPUT_SHARED_LED && pD0_EP0_BUF[0] == output_report_id) {
        KB_USB_SetReport = pD0_EP0_BUF[1];
    } else { control_stall(); return; }
    output_kind = OUTPUT_NONE;
    D0SetupLen = 0;
    control_phase = CTRL_STATUS_IN;
    D0_EP0T_L = 0;
    D0_EP0RES = bUEP_T_TOG | UEP_R_RES_NAK | UEP_T_RES_ACK;
}

static void control_in(void) {
    if (control_phase == CTRL_DATA_IN) {
        if (D0SetupLen || control_zlp) {
            D0_EP0RES ^= bUEP_T_TOG;
            control_next();
            return;
        }
        control_phase = CTRL_STATUS_OUT;
    } else if (control_phase == CTRL_STATUS_IN) {
        if (D0SetupReqCode == USB_SET_ADDRESS) D0_ADDR = D0SetupLen;
        control_phase = CTRL_IDLE;
    }
    D0_EP0RES = bUEP_R_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
}

void USB_DeviceInterrupt(void) {
    uint8_t status;
    uint8_t endpoint;
    do {
        /* Reset wins over stale endpoint completion flags. */
        if (USB_IF & bUX_IF_BUS_RST) {
            endpoints_reset();
            D0_ADDR = 0;
            D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
            KB_USB_SetReport = 0;
            keyboard_protocol = 1;
            keyboard_idle = 0;
            keyboard_reset = 1;
            D0SetupReqCode = 0xff;
            D0SetupLen = 0;
            control_phase = CTRL_IDLE;
            D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
            ACK_TRANSFER();
            ACK_RESET();
        } else if (USB_IF & bUX_IF_D0_TRANS) {
            status = D0_STATUS;
            endpoint = status & MASK_UXS_ENDP;
            /* SETUP preserves RX_LEN and any pending IN/OUT completion. Retire
             * that completion first; its ACK leaves SETUP pending with token
             * FREE for the next iteration. SETUP_ACT itself guarantees 8 bytes. */
            if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_OUT && !endpoint) {
                control_out();
            } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_IN) {
                if (!endpoint) control_in();
                else if (endpoint <= 3) {
                    EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_NAK;
                    if (endpoint == RAW_IN_EPNUM) raw_complete();
                }
            } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_FREE && (status & bUXS_SETUP_ACT)) {
                control_setup();
            }
            ACK_TRANSFER();
        } else if (USB_IF & bUX_IF_SUSPEND) {
            if (USB_IF & bUX_SUSPEND) USB_SleepStatus |= 2;
            else {
                USB_SleepStatus &= ~2;
                keyboard_reset = 1;
            }
            ACK_SUSPEND();
        }
    } while (USB_IF & (bUX_IF_BUS_RST | bUX_IF_D0_TRANS | bUX_IF_SUSPEND));
}
#pragma restore

void USB_Device_Init(void) {
    IE_USB = 0;
    USB_CTRL = 0;
    raw_state = RAW_IDLE;
    endpoints_reset();
    D0_ADDR = D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
    KB_USB_SetReport = KB_USB_UpStatus = MCU_Sleep_Operate = 0;
    keyboard_protocol = 1;
    keyboard_idle = 0;
    keyboard_reset = 0;
    control_phase = CTRL_IDLE;
    D0SetupReqCode = 0xff;
    D0SetupLen = 0;
    D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
    HB_ADDR = 0x7f;
    ACK_ALL();
    USB_IE = bUX_IE_SUSPEND | bUX_IE_TRANSFER | bUX_IE_BUS_RST;
    USB_CTRL = bUX_DP_PU_EN;
    IE_USB = 1;
}

void USB_WakeUp_PC(void) {
    uint8_t saved;
    if (USB_SleepStatus != 3) return;
    saved = USB_CTRL;
    USB_CTRL ^= bUX_DP_PU_EN | bUX_DM_PU_EN;
    wait_ms(10);
    USB_CTRL = saved;
}

bool ak820_usb_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length) {
    uint8_t saved_ea;
    uint8_t i;
    uint8_t timeout = 250;
    uint8_t offset = SNAPSHOT_SIZE;
    uint8_t report_id;
    if (endpoint < 1 || endpoint > 3 || length > 64 || !USB_EnumStatus) return false;
    if (endpoint == KEYBOARD_IN_EPNUM) {
        if (length != KEYBOARD_EPSIZE) return false;
        offset = SNAPSHOT_KEYBOARD;
    } else if (endpoint == SHARED_IN_EPNUM) {
        report_id = report[0];
        if (report_id >= sizeof(shared_lengths) || !shared_lengths[report_id] || length != shared_lengths[report_id]) return false;
        offset = shared_offsets[report_id];
    } else if (length != RAW_EPSIZE) return false;
    if (USB_SleepStatus & 2) { USB_WakeUp_PC(); return false; }
    while ((EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_ACK && timeout--) wait_us(40);
    saved_ea = EA;
    EA = 0;
    if (!USB_EnumStatus || (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) != UEP_X_RES_NAK ||
        (endpoint == RAW_IN_EPNUM && raw_state != RAW_WORK)) { EA = saved_ea; return false; }
    for (i = 0; i < length; ++i) {
        pUSB_BUF_DEV0[((uint16_t)endpoint << 6) + i] = report[i];
        if (offset != SNAPSHOT_SIZE) input_snapshot[offset + i] = report[i];
    }
    EP_LENGTH(endpoint) = length;
    if (endpoint == RAW_IN_EPNUM) raw_state = RAW_TX_ACTIVE;
    EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_ACK;
    EA = saved_ea;
    return true;
}

bool ak820_usb_try_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length) {
    uint8_t saved_ea = EA;
    bool sent = false;
    EA = 0;
    /* Keep the ready/reset test and publication atomic. With this NAK checked
     * under EA=0, send cannot enter its busy wait or wake-up delay. Its report
     * copy is bounded by 64 bytes and restores the disabled state on return. */
    if (endpoint >= 1 && endpoint <= 2 && USB_EnumStatus &&
        !(USB_SleepStatus & 2) && !keyboard_reset &&
        (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_NAK) {
        sent = ak820_usb_send(endpoint, report, length);
    }
    EA = saved_ea;
    return sent;
}

/* Permit discovery and the existing physical-unlock recovery flow after an
 * NVM fault. Unknown commands/subcommands and every setter stay fail-closed.
 * This only controls replies; VIA/Vial still enforce command authorization. */
static bool raw_request_is_nonpersistent(void) {
    switch (raw_buffer[0]) {
        case id_get_protocol_version:
        case id_dynamic_keymap_get_keycode:
        case id_dynamic_keymap_macro_get_count:
        case id_dynamic_keymap_macro_get_buffer_size:
        case id_dynamic_keymap_macro_get_buffer:
        case id_dynamic_keymap_get_layer_count:
        case id_dynamic_keymap_get_buffer:
        case id_bootloader_jump:
            return true;
        case id_get_keyboard_value:
            switch (raw_buffer[1]) {
                case id_uptime:
                case id_layout_options:
                case id_switch_matrix_state:
                case id_firmware_version:
                    return true;
                default: return false;
            }
        case id_lighting_get_value:
            switch (raw_buffer[1]) {
                case vialrgb_get_info:
                case vialrgb_get_mode:
                case vialrgb_get_supported:
                case vialrgb_get_number_leds:
                case vialrgb_get_led_info:
                    return true;
                default: return false;
            }
        case id_vial_prefix:
            switch (raw_buffer[1]) {
                case vial_get_keyboard_id:
                case vial_get_size:
                case vial_get_def:
                case vial_get_encoder:
                case vial_get_unlock_status:
                case vial_unlock_start:
                case vial_unlock_poll:
                case vial_lock:
                case vial_qmk_settings_query:
                case vial_qmk_settings_get:
                    return true;
                case vial_dynamic_entry_op:
                    switch (raw_buffer[2]) {
                        case dynamic_vial_get_number_of_entries:
                        case dynamic_vial_tap_dance_get:
                        case dynamic_vial_combo_get:
                        case dynamic_vial_key_override_get:
                            return true;
                        default: return false;
                    }
                default: return false;
            }
        default: return false;
    }
}

void ak820_usb_raw_send(const uint8_t *report, uint8_t length) {
    if (length != RAW_EPSIZE) return;
    ak820_nvm_flush();
    if (raw_reply_without_nvm || ak820_nvm_ok()) ak820_usb_send(RAW_IN_EPNUM, (const uint8_t __xdata *)report, length);
}

void ak820_usb_raw_task(void) {
    uint8_t i;
    uint8_t length;
    uint16_t address;
    uint8_t saved_ea = EA;
    EA = 0;
    if (!USB_EnumStatus || raw_state != RAW_READY) { EA = saved_ea; return; }
    raw_state = RAW_WORK;
    EA = saved_ea;
    if (raw_buffer[0] == 0xfd && raw_buffer[1] == 0) {
        /* Read-only diagnostic extension for full-ROM backup and verification.
         * FD 00 addr_hi addr_lo count, followed by at most 27 code bytes. */
        address = ((uint16_t)raw_buffer[2] << 8) | raw_buffer[3];
        length = raw_buffer[4];
        for (i = 5; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
        if (length > RAW_EPSIZE - 5 || (length && address > 0xffffu - (length - 1))) {
            raw_buffer[1] = 0xff;
            raw_buffer[4] = 0;
        } else {
            for (i = 0; i < length; ++i) raw_buffer[5 + i] = READ_CODE(address + i);
        }
        /* Readback must remain available after an NVM fault, without causing
         * a write/flush. Normal Vial replies retain their persistence gate. */
        ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
    } else if (raw_buffer[0] == 0xfd && raw_buffer[1] == 1) {
        /* FD01 v1: read-only RAM status, deliberately outside NVM batching.
         * Never flush, clear a failure, or acknowledge a previous setter. */
        for (i = 2; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
        raw_buffer[2] = 1;
        raw_buffer[3] = 0xa8;
        ak820_nvm_diagnostic(&raw_buffer[4]);
        for (i = 0; i < 6; ++i) raw_buffer[11 + i] = ak820_flash_diagnostic[i];
        raw_buffer[17] = vial_unlocked;
        raw_buffer[18] = vial_unlock_in_progress;
        raw_buffer[19] = USB_EnumStatus;
        raw_buffer[20] = USB_SleepStatus;
        raw_buffer[21] = raw_state;
        ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
    } else {
        raw_reply_without_nvm = raw_request_is_nonpersistent();
        ak820_nvm_begin();
        raw_hid_receive(raw_buffer, RAW_EPSIZE);
        ak820_nvm_end();
        raw_reply_without_nvm = false;
    }
    saved_ea = EA;
    EA = 0;
    /* Retain the buffer until both main and hardware have finished with it. */
    if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_TX_WAIT;
    else if (raw_state == RAW_WORK || raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED) raw_state = RAW_IDLE;
    EA = saved_ea;
}

bool ak820_usb_take_keyboard_reset(void) {
    uint8_t result;
    uint8_t saved_ea = EA;
    EA = 0;
    result = keyboard_reset;
    keyboard_reset = 0;
    EA = saved_ea;
    return result != 0;
}
