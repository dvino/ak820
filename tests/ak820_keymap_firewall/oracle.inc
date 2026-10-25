void dynamic_keymap_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
    uint16_t dynamic_keymap_eeprom_size = DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2;
    uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset);
    uint8_t DYNAMIC_BUFFER_MEM *buffer = (uint8_t DYNAMIC_BUFFER_MEM *)data;
#ifndef AK820_BOARD
    uint8_t DYNAMIC_BUFFER_MEM *source = buffer;
#endif
    if (!size) return;
#ifdef AK820_BOARD
    if (size > 28) return;
#endif
    dynamic_buffer_size_t count = size;

#ifdef VIAL_ENABLE
    /* ensure the writes are bounded */
    if (offset >= dynamic_keymap_eeprom_size || dynamic_keymap_eeprom_size - offset < size)
        return;

#ifndef VIAL_INSECURE
    /* Check whether it is trying to send a QK_BOOT keycode; only allow setting these if unlocked */
    if (!vial_unlocked) {
        /* how much of the input array we'll have to check in the loop */
        dynamic_buffer_size_t chk_offset = 0;
        dynamic_buffer_size_t chk_sz = count;

        /* initial byte misaligned -- this means the first keycode will be a combination of existing and new data */
        if (offset % 2 != 0) {
            uint16_t kc = (eeprom_read_byte(target - 1) << 8) | buffer[0];
            if (kc == QK_BOOT)
                buffer[0] = 0xFF;

            /* no longer have to check the first byte */
            chk_offset += 1;
        }

        /* final byte misaligned -- this means the last keycode will be a combination of new and existing data */
        if ((offset + size) % 2 != 0) {
            uint16_t kc = (buffer[count - 1] << 8) | eeprom_read_byte(target + count);
            if (kc == QK_BOOT)
                buffer[count - 1] = 0xFF;

            /* no longer have to check the last byte */
            chk_sz -= 1;
        }

        /* check the entire array, replace any instances of QK_BOOT with invalid keycode 0xFFFF */
        for (dynamic_buffer_size_t i = chk_offset; i < chk_sz; i += 2) {
            uint16_t kc = (buffer[i] << 8) | buffer[i + 1];
            if (kc == QK_BOOT) {
                buffer[i] = 0xFF;
                buffer[i + 1] = 0xFF;
            }
        }
    }
#endif
#endif

#ifdef AK820_BOARD
    /* The board backend compares each byte, batches pages and verifies the
     * durable write. Repeating its comparison through byte wrappers adds no
     * guarantee and is costly on the 8051 generic-pointer ABI. */
    ak820_eeprom_write_block_xdata(buffer, (void *)(uintptr_t)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset), size);
#else
    for (dynamic_buffer_size_t i = 0; i < count; i++) {
        if (offset + i < dynamic_keymap_eeprom_size) {
            eeprom_update_byte(target, *source);
        }
        source++;
        target++;
    }
#endif
}
