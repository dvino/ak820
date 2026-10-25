/* Pre-experiment VIA parser snapshot for differential native checks. */
void raw_hid_receive(uint8_t *packet, uint8_t length) {
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    /* The AK820 USB transport owns this fixed XDATA packet buffer. */
    uint8_t __xdata *data = (uint8_t __xdata *)packet;
    uint8_t __xdata *command_id = &data[0];
    uint8_t __xdata *command_data = &data[1];
#else
    uint8_t *data = packet;
    uint8_t *command_id = &data[0];
    uint8_t *command_data = &data[1];
#endif
#ifdef AK820_BOARD
    if (length != 32) return;
#endif
#ifdef VIAL_ENABLE
    /* When unlock is in progress, we can only react to a subset of commands */
    if (vial_unlock_in_progress) {
        if (data[0] != id_vial_prefix) {
#    ifdef AK820_BOARD
            return;
#    else
            goto skip;
#    endif
        }
        uint8_t cmd = data[1];
        if (cmd != vial_get_keyboard_id && cmd != vial_get_size && cmd != vial_get_def && cmd != vial_get_unlock_status && cmd != vial_unlock_start && cmd != vial_unlock_poll && cmd != vial_lock)
            goto skip;
    }
#endif

    switch (*command_id) {
        case id_get_protocol_version: {
            command_data[0] = VIA_PROTOCOL_VERSION >> 8;
            command_data[1] = VIA_PROTOCOL_VERSION & 0xFF;
            break;
        }
        case id_get_keyboard_value: {
            switch (command_data[0]) {
                case id_uptime: {
                    uint32_t value  = timer_read32();
                    command_data[1] = (value >> 24) & 0xFF;
                    command_data[2] = (value >> 16) & 0xFF;
                    command_data[3] = (value >> 8) & 0xFF;
                    command_data[4] = value & 0xFF;
                    break;
                }
                case id_layout_options: {
                    uint32_t value  = via_get_layout_options();
                    command_data[1] = (value >> 24) & 0xFF;
                    command_data[2] = (value >> 16) & 0xFF;
                    command_data[3] = (value >> 8) & 0xFF;
                    command_data[4] = value & 0xFF;
                    break;
                }
                case id_switch_matrix_state: {
#ifdef VIAL_ENABLE
                    /* Disable wannabe keylogger unless unlocked */
                    if (!vial_unlocked)
                        goto skip;
#endif

#if (((MATRIX_COLS + 7) / 8) * MATRIX_ROWS <= 28)
                    uint8_t i = 1;
                    for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
                        matrix_row_t value = matrix_get_row(row);
#    if (MATRIX_COLS > 24)
                        command_data[i++] = (value >> 24) & 0xFF;
#    endif
#    if (MATRIX_COLS > 16)
                        command_data[i++] = (value >> 16) & 0xFF;
#    endif
#    if (MATRIX_COLS > 8)
                        command_data[i++] = (value >> 8) & 0xFF;
#    endif
                        command_data[i++] = value & 0xFF;
                    }
#endif
                    break;
                }
                default: {
                    raw_hid_receive_kb(data, length);
                    break;
                }
            }
            break;
        }
        case id_set_keyboard_value: {
            switch (command_data[0]) {
                case id_layout_options: {
                    uint32_t value = ((uint32_t)command_data[1] << 24) | ((uint32_t)command_data[2] << 16) | ((uint32_t)command_data[3] << 8) | (uint32_t)command_data[4];
                    via_set_layout_options(value);
                    break;
                }
                default: {
                    raw_hid_receive_kb(data, length);
                    break;
                }
            }
            break;
        }
        case id_dynamic_keymap_get_keycode: {
            uint16_t keycode = dynamic_keymap_get_keycode(command_data[0], command_data[1], command_data[2]);
            command_data[3]  = keycode >> 8;
            command_data[4]  = keycode & 0xFF;
            break;
        }
        case id_dynamic_keymap_set_keycode: {
#if defined(VIAL_ENABLE) && !defined(VIAL_INSECURE)
            /* Apply the existing Vial boot-key restriction to the one-key
             * route too. Reject visibly and preserve the previous mapping. */
            if (!vial_unlocked && command_data[3] == (QK_BOOT >> 8) && command_data[4] == (QK_BOOT & 0xFF)) {
                *command_id = id_unhandled;
                break;
            }
#endif
            dynamic_keymap_set_keycode(command_data[0], command_data[1], command_data[2], (command_data[3] << 8) | command_data[4]);
            break;
        }
        case id_dynamic_keymap_reset: {
            dynamic_keymap_reset();
            break;
        }
        case id_lighting_set_value: {
#if defined(VIA_QMK_BACKLIGHT_ENABLE)
            via_qmk_backlight_set_value(command_data);
#endif
#if defined(VIA_QMK_RGBLIGHT_ENABLE)
            via_qmk_rgblight_set_value(command_data);
#endif
#if defined(VIALRGB_ENABLE)
            vialrgb_set_value(data, length);
#endif
#if defined(VIA_QMK_RGB_MATRIX_ENABLE)
            via_qmk_rgb_matrix_set_value(command_data);
#endif
#if defined(VIA_CUSTOM_LIGHTING_ENABLE)
            raw_hid_receive_kb(data, length);
#endif
#if !defined(VIA_QMK_BACKLIGHT_ENABLE) && !defined(VIA_QMK_RGBLIGHT_ENABLE) && !defined(VIALRGB_ENABLE) && !defined(VIA_CUSTOM_LIGHTING_ENABLE) && !defined(VIA_QMK_RGB_MATRIX_ENABLE)
            // Return the unhandled state
            *command_id = id_unhandled;
#endif
            break;
        }
        case id_lighting_get_value: {
#if defined(VIA_QMK_BACKLIGHT_ENABLE)
            via_qmk_backlight_get_value(command_data);
#endif
#if defined(VIA_QMK_RGBLIGHT_ENABLE)
            via_qmk_rgblight_get_value(command_data);
#endif
#if defined(VIALRGB_ENABLE)
            vialrgb_get_value(data, length);
#endif
#if defined(VIA_QMK_RGB_MATRIX_ENABLE)
            via_qmk_rgb_matrix_get_value(command_data);
#endif
#if defined(VIA_CUSTOM_LIGHTING_ENABLE)
            raw_hid_receive_kb(data, length);
#endif
#if !defined(VIA_QMK_BACKLIGHT_ENABLE) && !defined(VIA_QMK_RGBLIGHT_ENABLE) && !defined(VIALRGB_ENABLE) && !defined(VIA_CUSTOM_LIGHTING_ENABLE) && !defined(VIA_QMK_RGB_MATRIX_ENABLE)
            // Return the unhandled state
            *command_id = id_unhandled;
#endif
            break;
        }
        case id_lighting_save: {
#if defined(VIA_QMK_BACKLIGHT_ENABLE)
            eeconfig_update_backlight_current();
#endif
#if defined(VIA_QMK_RGBLIGHT_ENABLE)
            eeconfig_update_rgblight_current();
#endif
#if defined(VIALRGB_ENABLE)
            vialrgb_save(data, length);
#endif
#if defined(VIA_QMK_RGB_MATRIX_ENABLE)
            eeconfig_update_rgb_matrix();
#endif
#if defined(VIA_CUSTOM_LIGHTING_ENABLE)
            raw_hid_receive_kb(data, length);
#endif
#if !defined(VIA_QMK_BACKLIGHT_ENABLE) && !defined(VIA_QMK_RGBLIGHT_ENABLE) && !defined(VIALRGB_ENABLE) && !defined(VIA_CUSTOM_LIGHTING_ENABLE) && !defined(VIA_QMK_RGB_MATRIX_ENABLE)
            // Return the unhandled state
            *command_id = id_unhandled;
#endif
            break;
        }
#ifdef VIA_EEPROM_ALLOW_RESET
        case id_eeprom_reset: {
            via_eeprom_set_valid(false);
            eeconfig_init_via();
            break;
        }
#endif
        case id_dynamic_keymap_macro_get_count: {
            command_data[0] = dynamic_keymap_macro_get_count();
            break;
        }
        case id_dynamic_keymap_macro_get_buffer_size: {
            uint16_t size   = dynamic_keymap_macro_get_buffer_size();
            command_data[0] = size >> 8;
            command_data[1] = size & 0xFF;
            break;
        }
        case id_dynamic_keymap_macro_get_buffer: {
            uint16_t offset = (command_data[0] << 8) | command_data[1];
            uint16_t size   = command_data[2]; // size <= 28
            if (size <= 28)
                dynamic_keymap_macro_get_buffer(offset, size, &command_data[3]);
            break;
        }
        case id_dynamic_keymap_macro_set_buffer: {
#ifdef VIAL_ENABLE
            /* Until keyboard is unlocked, don't allow changing macros */
            if (!vial_unlocked) {
#    ifdef AK820_BOARD
                return;
#    else
                goto skip;
#    endif
            }
#endif
            uint16_t offset = (command_data[0] << 8) | command_data[1];
            uint16_t size   = command_data[2]; // size <= 28
#ifdef AK820_BOARD
            // No echoed success for malformed, incomplete-range or failed
            // writes. The USB task releases the request for the host retry.
            if (size > 28 || size > length - 4 || !dynamic_keymap_macro_set_buffer(offset, size, &command_data[3])) return;
#else
            if (size <= 28)
                dynamic_keymap_macro_set_buffer(offset, size, &command_data[3]);
#endif
            break;
        }
        case id_dynamic_keymap_macro_reset: {
#if defined(AK820_BOARD) && defined(VIAL_ENABLE)
            if (!vial_unlocked) return;
#endif
            dynamic_keymap_macro_reset();
            break;
        }
        case id_dynamic_keymap_get_layer_count: {
            command_data[0] = dynamic_keymap_get_layer_count();
            break;
        }
        case id_dynamic_keymap_get_buffer: {
            uint16_t offset = (command_data[0] << 8) | command_data[1];
            uint16_t size   = command_data[2]; // size <= 28
            if (size <= 28)
                dynamic_keymap_get_buffer(offset, size, &command_data[3]);
            break;
        }
        case id_dynamic_keymap_set_buffer: {
            uint16_t offset = (command_data[0] << 8) | command_data[1];
            uint16_t size   = command_data[2]; // size <= 28
            if (size <= 28)
                dynamic_keymap_set_buffer(offset, size, &command_data[3]);
            break;
        }
#if defined(VIAL_ENABLE) && !defined(VIAL_INSECURE)
        /* As VIA removed bootloader jump entirely, we shall only keep it for secure builds */
        case id_bootloader_jump: {
            /* Until keyboard is unlocked, don't allow jumping to bootloader */
            if (!vial_unlocked)
                goto skip;
            // Need to send data back before the jump
            // Informs host that the command is handled
            raw_hid_send(data, length);
            // Give host time to read it
            wait_ms(100);
            bootloader_jump();
            break;
        }
#endif
#ifdef VIAL_ENABLE
        case id_vial_prefix: {
            vial_handle_cmd(data, length);
            break;
        }
#endif
        default: {
            // The command ID is not known let the keyboard implement it
            raw_hid_receive_kb(data, length);
            break;
        }
    }
#ifdef VIAL_ENABLE
skip:
#endif
    // Return the same buffer, optionally with values changed
    // (i.e. returning state to the host, or the unhandled state).
    raw_hid_send(data, length);
}
