// SPDX-License-Identifier: GPL-2.0-or-later
// Unchanged behavior from dvino/ak820 38ad013, renamed for differential tests.
uint16_t reference_keymap_key_to_keycode(uint8_t layer, keypos_t key) {
    //ac_dprintf("km key to kc: layer: %x\n",layer);
    //layer = 0;
#ifdef VIAL_ENABLE
    /* Disable any keycode processing while unlocking */
    if (vial_unlock_in_progress) {
        return KC_NO;
    }
    if (key.row == VIAL_MATRIX_MAGIC && key.col == VIAL_MATRIX_MAGIC) {
        return g_vial_magic_keycode_override;
    }
#endif
    if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) {
        //ac_dprintf("km key to kc: layer: %x\n",layer);
        return keycode_at_keymap_location(layer, key.row, key.col);
    }
#ifdef ENCODER_MAP_ENABLE
    else if (key.row == KEYLOC_ENCODER_CW && key.col < NUM_ENCODERS) {
        return keycode_at_encodermap_location(layer, key.col, true);
    } else if (key.row == KEYLOC_ENCODER_CCW && key.col < NUM_ENCODERS) {
        return keycode_at_encodermap_location(layer, key.col, false);
    }
#endif // ENCODER_MAP_ENABLE
    return KC_NO;
}
