/* Immutable RC4 cb9ff6ea function bodies; only names prefixed rc4_. */
uint8_t rc4_extract_mod_bits(uint16_t code) {
    //switch (code) {
    //    case QK_MODS ... QK_MODS_MAX:
    //        break;
    //    default:
    //        return 0;
    //}
    if (code >= QK_MODS && code <= QK_MODS_MAX) ;
    else return 0;

    uint8_t mods_to_send = 0;

    if (code & QK_RMODS_MIN) { // Right mod flag is set
        if (code & QK_LCTL) mods_to_send |= MOD_BIT(KC_RIGHT_CTRL);
        if (code & QK_LSFT) mods_to_send |= MOD_BIT(KC_RIGHT_SHIFT);
        if (code & QK_LALT) mods_to_send |= MOD_BIT(KC_RIGHT_ALT);
        if (code & QK_LGUI) mods_to_send |= MOD_BIT(KC_RIGHT_GUI);
    } else {
        if (code & QK_LCTL) mods_to_send |= MOD_BIT(KC_LEFT_CTRL);
        if (code & QK_LSFT) mods_to_send |= MOD_BIT(KC_LEFT_SHIFT);
        if (code & QK_LALT) mods_to_send |= MOD_BIT(KC_LEFT_ALT);
        if (code & QK_LGUI) mods_to_send |= MOD_BIT(KC_LEFT_GUI);
    }

    return mods_to_send;
}

void rc4_do_code16(uint16_t code, void (*f)(uint8_t)) {
    f(rc4_extract_mod_bits(code));
}

__attribute__((weak)) void rc4_register_code16(uint16_t code) {
    if (IS_MODIFIER_KEYCODE(code) || code == KC_NO) {
        rc4_do_code16(code, register_mods);
    } else {
        rc4_do_code16(code, register_weak_mods);
    }
    register_code(code);
}

__attribute__((weak)) void rc4_unregister_code16(uint16_t code) {
    unregister_code(code);
    if (IS_MODIFIER_KEYCODE(code) || code == KC_NO) {
        rc4_do_code16(code, unregister_mods);
    } else {
        rc4_do_code16(code, unregister_weak_mods);
    }
}
