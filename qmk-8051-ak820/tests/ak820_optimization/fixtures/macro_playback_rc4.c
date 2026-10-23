/* GPL-2.0-or-later: RC4 macro playback reference, commit cb9ff6ea. */
void rc4_dynamic_keymap_macro_send(uint8_t id) {
#ifdef AK820_BOARD
    /* Extended keycodes can dispatch a macro again through action_exec.
     * SDCC's static interpreter locals cannot support nested playback. */
    static bool sending;
    if (sending) return;
#endif
    if (id >= DYNAMIC_KEYMAP_MACRO_COUNT) {
        return;
    }

#ifdef AK820_BOARD
    // The Vial GUI never writes the upstream last-byte busy marker.
    // AK820 commits only complete validated streams using a separate byte.
    if (!ak820_macro_ready()) return;
    uint8_t *p;
#else
    // Check the last byte of the buffer.
    // If it's not zero, then we are in the middle
    // of buffer writing, possibly an aborted buffer
    // write. So do nothing.
    uint8_t *p = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE - 1);
    if (eeprom_read_byte(p) != 0) {
        return;
    }
#endif

    // Skip N null characters
    // p will then point to the Nth macro
    p         = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR);
#ifdef AK820_BOARD
    uint8_t *end = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + ak820_macro_length());
#else
    uint8_t *end = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE);
#endif
    while (id > 0) {
        // If we are past the end of the buffer, then the buffer
        // contents are garbage, i.e. there were not DYNAMIC_KEYMAP_MACRO_COUNT
        // nulls in the buffer.
        if (p == end) {
            return;
        }
        if (eeprom_read_byte(p) == 0) {
            --id;
        }
        ++p;
    }

#ifdef AK820_BOARD
    /* All preflight returns precede this point; every interpreter exit
     * below reaches the release at the end of the function. */
    sending = true;
#endif
    // Send the macro string one or three chars at a time
    // by making temporary 1 or 3 char strings
    char data[4] = {0, 0, 0, 0};
    // AK820 validates the complete grammar before publication; retain the
    // explicit boundary as a second bound on the main interpreter loop.
    while (p < end) {
        data[0] = eeprom_read_byte(p++);
        data[1] = 0;
        // Stop at the null terminator of this macro string
        if (data[0] == 0) {
            break;
        }
        if (data[0] == SS_QMK_PREFIX) {
            // If the char is magic, process it as indicated by the next character
            // (tap, down, up, delay)
            data[1] = eeprom_read_byte(p++);
            if (data[1] == 0)
                break;
            if (data[1] == SS_TAP_CODE || data[1] == SS_DOWN_CODE || data[1] == SS_UP_CODE) {
                // For tap, down, up, just stuff it into the array and send_string it
                data[2] = eeprom_read_byte(p++);
                /* An earlier extended action used the fourth byte as data. */
                data[3] = 0;
                if (data[2] != 0)
                    send_string(data);
            } else if (data[1] == VIAL_MACRO_EXT_TAP || data[1] == VIAL_MACRO_EXT_DOWN || data[1] == VIAL_MACRO_EXT_UP) {
                data[2] = eeprom_read_byte(p++);
                if (data[2] != 0) {
                    data[3] = eeprom_read_byte(p++);
                    if (data[3] != 0) {
                        uint16_t kc;
                        memcpy(&kc, &data[2], sizeof(kc));
                        kc = decode_keycode(kc);
                        switch (data[1]) {
                        case VIAL_MACRO_EXT_TAP:
                            vial_keycode_tap(kc);
                            break;
                        case VIAL_MACRO_EXT_DOWN:
                            vial_keycode_down(kc);
                            break;
                        case VIAL_MACRO_EXT_UP:
                            vial_keycode_up(kc);
                            break;
                        }
                    }
                }
            } else if (data[1] == SS_DELAY_CODE) {
                // For delay, decode the delay and wait_ms for that amount
                uint8_t d0 = eeprom_read_byte(p++);
                uint8_t d1 = eeprom_read_byte(p++);
                if (d0 == 0 || d1 == 0)
                    break;
                // we cannot use 0 for these, need to subtract 1 and use 255 instead of 256 for delay calculation
                uint16_t ms = (uint16_t)(d0 - 1) + (uint16_t)(d1 - 1) * 255u;
                while (ms--) wait_ms(1);
            }
        } else {
#ifdef AK820_BOARD
            /* Stored streams from older firmware also need the ASCII bound;
             * publication validation alone cannot protect their playback. */
            if ((uint8_t)data[0] >= 128) break;
#endif
            // If the char wasn't magic, just send it
            send_string_with_delay(data, DYNAMIC_KEYMAP_MACRO_DELAY);
        }
    }
#ifdef AK820_BOARD
    sending = false;
#endif
}