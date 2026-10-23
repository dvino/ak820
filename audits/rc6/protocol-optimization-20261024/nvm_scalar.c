#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include "eeprom_driver.h"
#include "ak820_nvm.h"
#ifdef CANDIDATE
#    define BLOCK_READ ak820_eeprom_read_block_xdata
#    define BLOCK_WRITE ak820_eeprom_write_block_xdata
#    define BLOCK_UPDATE ak820_eeprom_update_block_xdata
#else
#    define BLOCK_READ eeprom_read_block
#    define BLOCK_WRITE eeprom_write_block
#    define BLOCK_UPDATE eeprom_update_block
#endif
static uint8_t flash_image[65536];
static uint64_t hash=UINT64_C(1469598103934665603);
static void add(uint8_t value) { hash=(hash^value)*UINT64_C(1099511628211); }
uint8_t ak820_flash_read(uint16_t address) { add(0x52); add(address);add(address>>8);return flash_image[address]; }
bool ak820_flash_erase(uint16_t address) { add(0x45);add(address);add(address>>8);memset(flash_image+address,0,64);return true; }
bool ak820_flash_program(uint16_t address,uint8_t value) { add(0x50);add(address);add(address>>8);add(value);flash_image[address]|=value;return true; }
bool ak820_flash_program_page(uint16_t address,const uint8_t *data) {for(uint8_t i=0;i<64;++i)if(!ak820_flash_program(address+i,data[i]))return false;return true;}
static void reads(void) {
    for(uint32_t offset=0;offset<65536;++offset) {
        add(eeprom_read_byte((const uint8_t *)(uintptr_t)offset));
        uint16_t word=eeprom_read_word((const uint16_t *)(uintptr_t)offset);add(word);add(word>>8);
        uint32_t dword=eeprom_read_dword((const uint32_t *)(uintptr_t)offset);for(uint8_t i=0;i<4;++i)add(dword>>(i*8));
    }
}
int main(void) {
    for(unsigned offset=0;offset<AK820_NVM_SIZE;++offset)flash_image[AK820_NVM_BASE+offset]=(uint8_t)(offset*37+offset/64);
    eeprom_driver_init(); reads();
    uint8_t data[64];memset(data,0x9b,64);
    ak820_nvm_begin();BLOCK_WRITE(data,(void *)(uintptr_t)(63*64),64);reads();
    uint8_t status[7];ak820_nvm_diagnostic(status);for(unsigned i=0;i<7;++i)add(status[i]);
    ak820_nvm_end();reads();
    static const uint16_t offsets[]={0,1,63,64,AK820_NVM_SIZE-1,AK820_NVM_SIZE,65535};
    static const uint8_t sizes[]={0,1,2,64,70};
    uint8_t block[70];
    for(unsigned a=0;a<sizeof(offsets)/sizeof(offsets[0]);++a)for(unsigned b=0;b<sizeof(sizes);++b) {
        eeprom_driver_init();
        memset(block,0xa7,sizeof(block));
        BLOCK_READ(block,(const void *)(uintptr_t)offsets[a],sizes[b]);
        for(unsigned i=0;i<sizeof(block);++i)add(block[i]);
        BLOCK_UPDATE(block,(void *)(uintptr_t)offsets[a],sizes[b]);
        ak820_nvm_diagnostic(status);for(unsigned i=0;i<7;++i)add(status[i]);
        eeprom_driver_init();
        memset(block,0x6c,sizeof(block));
        BLOCK_WRITE(block,(void *)(uintptr_t)offsets[a],sizes[b]);
        ak820_nvm_diagnostic(status);for(unsigned i=0;i<7;++i)add(status[i]);
    }
    for(unsigned i=0;i<65536;++i)add(flash_image[i]);
    printf("%016llx\n",(unsigned long long)hash);
}
