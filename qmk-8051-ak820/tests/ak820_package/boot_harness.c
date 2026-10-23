// SPDX-License-Identifier: GPL-2.0-or-later
// Minimal target-CPU fixture; never loaded onto a physical device.
#include "ak820_nvm.h"

volatile __xdata __at(0x0400) uint8_t test_nvm_good;
volatile __xdata __at(0x0401) uint8_t test_flush_count;
volatile __xdata __at(0x0402) uint8_t test_persist_count;

void ak820_nvm_flush(void) {
    ++test_flush_count;
    if (test_nvm_good) ++test_persist_count;
}

bool ak820_nvm_ok(void) {
    return test_nvm_good != 0;
}

void test_returned(void) {
    __asm nop __endasm;
}

void bootloader_jump(void);

void main(void) {
    bootloader_jump();
    test_returned();
    while (1) { }
}
