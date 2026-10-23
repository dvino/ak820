// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <stdbool.h>
#include <stdint.h>

#define AK820_NVM_BASE 0xC700u
#define AK820_NVM_SIZE 0x2800u
#define AK820_NVM_END (AK820_NVM_BASE + AK820_NVM_SIZE)
#define AK820_JOURNAL_DATA 0xEF00u
#define AK820_JOURNAL_HEADER 0xEF40u
#define AK820_NVM_WRITE_END 0xEF80u
#define AK820_FLASH_PAGE 64u

#ifdef __SDCC_mcs51
#    define AK820_XDATA __xdata
#else
#    define AK820_XDATA
#endif

/* FD01 status v1. These values describe the first latched storage failure;
 * reading diagnostics never clears it or commits dirty cached data. */
enum {
    AK820_NVM_FAULT_NONE,
    AK820_NVM_FAULT_RECOVERY_PAGE,
    AK820_NVM_FAULT_RECOVERY_CRC,
    AK820_NVM_FAULT_RECOVERY_WRITE,
    AK820_NVM_FAULT_RECOVERY_CLEANUP,
    AK820_NVM_FAULT_HEADER_ERASE,
    AK820_NVM_FAULT_HEADER_ZERO,
    AK820_NVM_FAULT_JOURNAL_WRITE,
    AK820_NVM_FAULT_METADATA_PROGRAM,
    AK820_NVM_FAULT_METADATA_READBACK,
    AK820_NVM_FAULT_COMMIT_PROGRAM,
    AK820_NVM_FAULT_COMMIT_READBACK,
    AK820_NVM_FAULT_TARGET_WRITE,
    AK820_NVM_FAULT_CLEANUP,
    AK820_NVM_FAULT_WRITE_RANGE,
    AK820_NVM_FAULT_BATCH_OVERFLOW,
    AK820_NVM_FAULT_SCHEMA,
};

/* Last attempted in-range IAP: valid, operation, before, after, addr lo/hi.
 * The controller status is sampled, not synthesized. A failed precondition
 * leaves before == after and performs no ROM_CTRL write. */
extern uint8_t AK820_XDATA ak820_flash_diagnostic[6];
void ak820_nvm_diagnostic(uint8_t AK820_XDATA *out);

bool ak820_nvm_ok(void);
/* Block further writes when VIA sees an incompatible schema. Preserve NVM
 * for explicit offline migration; never silently regenerate keymaps/macros. */
void ak820_nvm_schema_fault(void);
void ak820_nvm_begin(void);
void ak820_nvm_flush(void);
void ak820_nvm_end(void);
uint8_t ak820_flash_read(uint16_t address);
bool ak820_flash_erase(uint16_t address);
bool ak820_flash_program(uint16_t address, uint8_t value);
#ifdef __SDCC
bool ak820_flash_program_page(uint16_t address, const uint8_t __xdata *data);
#else
bool ak820_flash_program_page(uint16_t address, const uint8_t *data);
#endif

