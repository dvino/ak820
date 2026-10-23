// SPDX-License-Identifier: GPL-2.0-or-later
// Register sequence derived from the supplied AK820 ROM (erase at E650),
// and CH555 register definitions. Erased flash reads 00, programming sets bits.
#include "ch555.h"
#include "ak820_nvm.h"

uint8_t AK820_XDATA ak820_flash_diagnostic[6];

/* A 64-byte block program requires a 64-byte aligned XRAM buffer. The
 * over-allocation keeps this reservation inside the ordinary linker-managed
 * XRAM area without borrowing the loader, USB, LED DMA or stack memory. */
static __xdata uint8_t block_storage[2 * AK820_FLASH_PAGE - 1];
static uint8_t __xdata *block_data;

/* SDCC passes the first __xdata pointer in DPTR. Keep that value intact for
 * both the parameter-validity check and the IAP opcode, matching OEM 1230..
 * 123D. Ordinary C temporaries use DPTR for XRAM. Return before:after in the
 * uint16_t ABI (DPH:DPL) only after the flash operation or rejected check. */
static uint16_t program_block(const uint8_t __xdata *data) __naked {
    data;
    __asm
        mov a, _ROM_CTRL
        mov b, a
        jnb acc.6, 00001$
        mov _ROM_CTRL, #0x9a
        mov a, _ROM_CTRL
00001$:
        mov dpl, a
        mov dph, b
        ret
    __endasm;
}

/* Keep the erase status check and opcode in registers, like OEM 16CA..
 * 16D2, without compiler-generated XRAM accesses in that sequence. This
 * removes an ordering difference; it does not establish a DPTR requirement
 * for A6. As in program_block(), A/B/DPTR are scratch, DPH:DPL returns
 * before:after, and no register-bank register or interrupt state is changed. */
static uint16_t erase_page(void) __naked {
    __asm
        mov a, _ROM_CTRL
        mov b, a
        jnb acc.6, 00002$
        mov _ROM_CTRL, #0xa6
        mov a, _ROM_CTRL
00002$:
        mov dpl, a
        mov dph, b
        ret
    __endasm;
}

uint8_t ak820_flash_read(uint16_t address) {
    return *((const __code uint8_t *)address);
}

static bool flash_operation(uint16_t address, uint8_t value, uint8_t operation) {
    uint8_t previous_ie, before, status;
    if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END) return false;
    ak820_flash_diagnostic[0] = 1;
    ak820_flash_diagnostic[1] = operation ? operation : 0x9A;
    ak820_flash_diagnostic[4] = (uint8_t)address;
    ak820_flash_diagnostic[5] = (uint8_t)(address >> 8);
    previous_ie = IE;
    EA = 0;
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    GLOBAL_CFG |= 0x08;  // CODE_WE
    ROM_ADDR_L = (uint8_t)address;
    ROM_ADDR_H = (uint8_t)(address >> 8);
    /* operation==0 is private to this function and selects one full block.
     * It is never written as an opcode to ROM_CTRL. */
    ROM_BUF_MOD = operation ? 0x80 : AK820_FLASH_PAGE - 1;
    ROM_DAT_BUF = value;
    if (operation) {
        uint16_t states = erase_page();
        before = (uint8_t)(states >> 8);
        status = (uint8_t)states;
    } else {
        uint16_t states = program_block(block_data);
        before = (uint8_t)(states >> 8);
        status = (uint8_t)states;
    }
    ak820_flash_diagnostic[2] = before;
    ak820_flash_diagnostic[3] = status;
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    GLOBAL_CFG &= (uint8_t)~0x08;
    SAFE_MOD = 0;
    IE = previous_ie;
    return (before & 0x40) && !(status & 0x02);
}

bool ak820_flash_erase(uint16_t address) {
    uint8_t i;
    if (address & (AK820_FLASH_PAGE - 1)) return false;
    if (!flash_operation(address, 0, 0xA6)) return false;
    /* Status success alone does not prove erase. Stop before programming if
     * any CODE byte remains set, retaining A6 as the last IAP diagnostic. */
    for (i = 0; i != AK820_FLASH_PAGE; ++i) {
        if (ak820_flash_read(address + i) != 0) return false;
    }
    return true;
}

bool ak820_flash_program(uint16_t address, uint8_t value) {
    uint8_t i;
    uint8_t offset;
    uint16_t page;
    if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END) return false;
    offset = address & (AK820_FLASH_PAGE - 1);
    page = address & ~(AK820_FLASH_PAGE - 1);
    block_data = (uint8_t __xdata *)(((uint16_t)block_storage + AK820_FLASH_PAGE - 1) & ~(AK820_FLASH_PAGE - 1));
    /* The single-byte ROM_BUF_MOD=0x80 path has no OEM-backed programming
     * contract. Stage the complete current page and preserve every existing
     * bit, then use the same aligned-DPTR block path as program_page(). This
     * also preserves neighbours if the controller replaces its whole block.
     * Journal metadata is still verified before the separate commit call. */
    for (i = 0; i != AK820_FLASH_PAGE; ++i) block_data[i] = ak820_flash_read(page + i);
    block_data[offset] |= value;
    return flash_operation(page, 0, 0);
}

bool ak820_flash_program_page(uint16_t address, const uint8_t __xdata *data) {
    uint8_t i;
    if (address & (AK820_FLASH_PAGE - 1)) return false;
    block_data = (uint8_t __xdata *)(((uint16_t)block_storage + AK820_FLASH_PAGE - 1) & ~(AK820_FLASH_PAGE - 1));
    for (i = 0; i != AK820_FLASH_PAGE; ++i) block_data[i] = data[i];
    return flash_operation(address, 0, 0);
}
