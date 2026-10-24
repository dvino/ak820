/* SPDX-License-Identifier: GPL-2.0-or-later
 * Host test substitutes address spaces, MMIO storage and the documented SIE
 * completion/SETUP acknowledgement sequence. Register bits/types and
 * descriptors come from the production headers; electrical timing is not modeled.
 */
#pragma once
#include <stdbool.h>
#include <stdint.h>
#define __code
#define __xdata
#define __data
#define __idata
#define __pdata
#define __bit bool
#define __at(address)
#define __sfr extern volatile uint8_t
#define __sbit extern volatile uint8_t
#define __sfr16 extern volatile uint16_t
#define __sfr32 extern volatile uint32_t
#define __interrupt(number)
#define __reentrant
#include "usb_device.h"
#include "usb_ak820.h"
#include "report.h"

extern volatile uint8_t test_mmio[0x2300];
extern uint8_t test_rom[0x10000];
#undef XBYTE
#define XBYTE test_mmio
#undef pUSB_BUF_DEV0
#define pUSB_BUF_DEV0 (&test_mmio[0x1000])
#define EP_RESPONSE(ep) test_mmio[0x2200u + (ep)]
#define EP_LENGTH(ep) test_mmio[0x2208u + (ep)]
#define ACK_TRANSFER() test_ack_transfer()
#define ACK_RESET() (USB_IF &= ~bUX_IF_BUS_RST)
#define ACK_SUSPEND() (USB_IF &= ~bUX_IF_SUSPEND)
#define ACK_ALL() test_ack_all()
#define READ_CODE(address) test_read_code((uint16_t)(address))
void test_ack_transfer(void);
void test_ack_all(void);
uint8_t test_read_code(uint16_t address);
void wait_ms(uint16_t value);
void wait_us(uint16_t value);
void raw_hid_receive(uint8_t *data, uint8_t length);

#ifdef AK820_OS_INDICATORS
extern uint8_t ak820_led_dma[512];
extern volatile uint8_t IE_PWM_I2C;
typedef uint8_t layer_state_t;
extern layer_state_t layer_state, default_layer_state;
uint32_t timer_read32(void);
#endif
