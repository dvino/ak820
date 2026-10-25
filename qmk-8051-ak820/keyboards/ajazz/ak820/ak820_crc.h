// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <stdint.h>
#include "ak820_nvm.h"

/* CRC-16/CCITT-FALSE: poly 0x1021, init 0xffff, no reflection/xorout.
 * Buffers are XDATA on mcs51; length is 0..255 bytes. Foreground only:
 * SDCC may overlay parameters/locals. No callbacks or recursive/ISR calls.
 * SDCC large model uses a naked bank-0 implementation: R2-R7/ACC/DPTR and arithmetic PSW flags are
 * clobbered, DPTR returns CRC. No additional stack use beyond return address.
 * Native builds retain the C reference implementation. */
uint16_t ak820_crc16(const uint8_t AK820_XDATA *data, uint8_t length);
