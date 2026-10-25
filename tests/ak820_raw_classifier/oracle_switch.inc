static bool raw_request_is_nonpersistent(void) {
    switch (raw_buffer[0]) {
        case id_get_protocol_version:
        case id_dynamic_keymap_get_keycode:
        case id_dynamic_keymap_macro_get_count:
        case id_dynamic_keymap_macro_get_buffer_size:
        case id_dynamic_keymap_macro_get_buffer:
        case id_dynamic_keymap_get_layer_count:
        case id_dynamic_keymap_get_buffer:
        case id_bootloader_jump:
            return true;
        case id_get_keyboard_value:
            switch (raw_buffer[1]) {
                case id_uptime:
                case id_layout_options:
                case id_switch_matrix_state:
                case id_firmware_version:
                    return true;
                default: return false;
            }
        case id_lighting_get_value:
            switch (raw_buffer[1]) {
                case vialrgb_get_info:
                case vialrgb_get_mode:
                case vialrgb_get_supported:
                case vialrgb_get_number_leds:
                case vialrgb_get_led_info:
                    return true;
                default: return false;
            }
        case id_vial_prefix:
            switch (raw_buffer[1]) {
                case vial_get_keyboard_id:
                case vial_get_size:
                case vial_get_def:
                case vial_get_encoder:
                case vial_get_unlock_status:
                case vial_unlock_start:
                case vial_unlock_poll:
                case vial_lock:
                case vial_qmk_settings_query:
                case vial_qmk_settings_get:
                    return true;
                case vial_dynamic_entry_op:
                    switch (raw_buffer[2]) {
                        case dynamic_vial_get_number_of_entries:
                        case dynamic_vial_tap_dance_get:
                        case dynamic_vial_combo_get:
                        case dynamic_vial_key_override_get:
                            return true;
                        default: return false;
                    }
                default: return false;
            }
        default: return false;
    }
}
