// SPDX-License-Identifier: GPL-2.0-or-later
#include "ch555.h"
#include "ak820_nvm.h"

void mcu_reset(void) {
    EA = 0;
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    GLOBAL_CFG |= 0x10;
    while (1) { }
}

void bootloader_jump(void) {
    // Stock loader chooses application solely by AA5533CC at27C0. The
    // unchanged loader is entered by clearing that marker and a soft reset.
    uint8_t saved_ie = IE;
    const __code uint8_t *marker = (const __code uint8_t *)0x27C0;
    // Flush is best effort: a settings fault must not block requested recovery.
    // The marker erase/readback below independently gates the loader reset.
    ak820_nvm_flush();
    EA = 0;
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    GLOBAL_CFG |= 0x08;
    ROM_ADDR_L = 0xC0;
    ROM_ADDR_H = 0x27;
    ROM_BUF_MOD = 0x80;
    ROM_DAT_BUF = 0;
    if (ROM_STATUS & 0x40) ROM_CTRL = 0xA6;
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    GLOBAL_CFG &= (uint8_t)~0x08;
    SAFE_MOD = 0;
    // A rejected erase must not masquerade as a successful loader transition.
    if (marker[0] || marker[1] || marker[2] || marker[3]) {
        IE = saved_ie;
        return;
    }
    mcu_reset();
}
