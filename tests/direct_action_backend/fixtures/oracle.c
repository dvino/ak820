uint16_t action_for_keycode(uint16_t keycode) {
#if defined(AK820_BOARD) && defined(NO_ACTION_TAPPING) && defined(NO_ACTION_ONESHOT) && !defined(NO_ACTION_LAYER) && !defined(MAGIC_KEYCODE_ENABLE) && !defined(LEGACY_MAGIC_HANDLING) && !defined(SWAP_HANDS_ENABLE) && !defined(NO_ACTION_TAPPING_MODTAP_MODS) && !defined(NO_ACTION_TAPPING_TAP_TOGGLE_MO)
    _Static_assert(QK_MODS == 0x0100 && QK_MODS_MAX == 0x1fff &&
                   QK_MOD_TAP == 0x2000 && QK_MOD_TAP_MAX == 0x3fff &&
                   QK_LAYER_TAP == 0x4000 && QK_LAYER_TAP_MAX == 0x4fff &&
                   QK_LAYER_MOD == 0x5000 && QK_LAYER_MOD_MAX == 0x51ff,
                   "AK820 byte dispatch requires the pinned keycode namespaces");
    _Static_assert(QK_TO == 0x5200 && QK_TO_MAX == 0x521f &&
                   QK_MOMENTARY == 0x5220 && QK_MOMENTARY_MAX == 0x523f &&
                   QK_DEF_LAYER == 0x5240 && QK_DEF_LAYER_MAX == 0x525f &&
                   QK_TOGGLE_LAYER == 0x5260 && QK_TOGGLE_LAYER_MAX == 0x527f &&
                   QK_ONE_SHOT_LAYER == 0x5280 && QK_ONE_SHOT_LAYER_MAX == 0x529f &&
                   QK_ONE_SHOT_MOD == 0x52a0 && QK_ONE_SHOT_MOD_MAX == 0x52bf &&
                   QK_LAYER_TAP_TOGGLE == 0x52c0 && QK_LAYER_TAP_TOGGLE_MAX == 0x52df,
                   "AK820 layer dispatch requires 32-code groups in namespace 0x52");
    _Static_assert(ACTION_KEY(0xff) == 0x00ff && ACTION_MODS_KEY(0x1f, 0xff) == 0x1fff &&
                   ACTION_LAYER_MODS(2, 0x10) == 0x9210 &&
                   ACTION_LAYER_GOTO(31) == 0x8de8 &&
                   ACTION_DEFAULT_LAYER_SET(31) == 0x8ce8 &&
                   ACTION_LAYER_TOGGLE(31) == 0x8ae8,
                   "AK820 byte dispatch requires the pinned action encoding");
    /* Dispatch once on the namespace byte. Keep the wire/keymap ABI 16-bit;
     * the active no-tapping profile needs byte operations for classification. */
    uint8_t kind = (uint8_t)(keycode >> 8);
    uint8_t key = (uint8_t)keycode;
    uint8_t mods;
    if (!kind) {
        if ((key >= KC_A && key <= KC_EXSEL) ||
            (key >= KC_LEFT_CTRL && key <= KC_RIGHT_GUI) || key == KC_TRANSPARENT)
            return ACTION_KEY(key);
#ifdef EXTRAKEY_ENABLE
        if (key >= KC_SYSTEM_POWER && key <= KC_SYSTEM_WAKE)
            return ACTION_USAGE_SYSTEM(KEYCODE2SYSTEM(key));
        if (key >= KC_AUDIO_MUTE && key <= KC_LAUNCHPAD)
            return ACTION_USAGE_CONSUMER(KEYCODE2CONSUMER(key));
#endif
        if (key >= KC_MS_UP && key <= KC_MS_ACCEL2) return ACTION_MOUSEKEY(key);
        return ACTION_NO;
    }
    if (kind < 0x20) return keycode; /* Encoded modifier+basic actions. */
    if (kind < 0x50) {
#ifdef AK820_COMPACT_TAPPING
        /* Opaque during layer search, including a transparent tap byte.
         * The compact engine consumes the original 16-bit record. */
        return ACTION_NO;
#else
        return ACTION_KEY(key);
#endif
    }
    if (kind < 0x52) {
        uint8_t layer = ((kind & 1u) << 3) | (key >> 5);
        mods = key & 0x1f;
        if (mods & 0x10) mods <<= 4; /* Discard the 5-bit right-mod marker. */
        return ACTION_LAYER_MODS(layer, mods);
    }
    if (kind != 0x52) return ACTION_NO;
    mods = key & 0x1f;
    switch (key >> 5) {
        case 0: kind = (ACT_LAYER << 4) | (OP_BIT_SET << 2) | ON_PRESS; break;
        case 1: return ACTION_LAYER_MOMENTARY(mods);
        case 2: kind = (ACT_LAYER << 4) | (OP_BIT_SET << 2); break;
        case 3:
        case 6: kind = (ACT_LAYER << 4) | (OP_BIT_XOR << 2) | ON_RELEASE; break;
        case 5: return ACTION_MODS(mods); /* Existing held-mod fallback for OSM. */
        default: return ACTION_NO;
    }
    /* TO, DF, TG and TT share the same bit-position encoding. */
    key = ((key & 0x1c) << 3) | (1u << (key & 3));
    return ((uint16_t)kind << 8) | key;
#else

    // keycode remapping
    keycode = keycode_config(keycode);

    uint8_t  action_layer, mod;

#ifndef __SDCC 
//this seems tobe used for supress unused var warning in gcc. sdcc dont need it
    (void)action_layer;
    (void)mod;
#endif

    //dprintf("action_for_key:keycode %x\n",keycode);
    //switch (keycode) {
        if ( (keycode >= KC_A         && keycode <= KC_EXSEL    ) ||
             (keycode >= KC_LEFT_CTRL && keycode <= KC_RIGHT_GUI) ) {
            //dprint("is normal keycode.");
            return ACTION_KEY(keycode);
            //dprintf("%x\n",action.code);
        }
#ifdef EXTRAKEY_ENABLE
        else if (keycode >= KC_SYSTEM_POWER && keycode <= KC_SYSTEM_WAKE)
            return ACTION_USAGE_SYSTEM(KEYCODE2SYSTEM(keycode));
        else if (keycode >= KC_AUDIO_MUTE && keycode <= KC_LAUNCHPAD)
            return ACTION_USAGE_CONSUMER(KEYCODE2CONSUMER(keycode));
#endif
        else if (keycode >= KC_MS_UP && keycode <= KC_MS_ACCEL2)
            return ACTION_MOUSEKEY(keycode);
        else if (keycode == KC_TRANSPARENT)
            return ACTION_TRANSPARENT;
        else if (keycode >= QK_MODS && keycode <= QK_MODS_MAX)
        // Has a modifier
        // Split it up
#ifdef LEGACY_MAGIC_HANDLING
            return ACTION_MODS_KEY(QK_MODS_GET_MODS(keycode), QK_MODS_GET_BASIC_KEYCODE(keycode)); // adds modifier to key
#else                                                                                                     // LEGACY_MAGIC_HANDLING
            #if defined(AK820_BOARD) && !defined(MAGIC_KEYCODE_ENABLE)
            return keycode;
#else
            return ACTION_MODS_KEY(mod_config(QK_MODS_GET_MODS(keycode)), keycode_config(QK_MODS_GET_BASIC_KEYCODE(keycode)));
#endif
#endif                                                                                                    // LEGACY_MAGIC_HANDLING
        else if (keycode >= QK_LAYER_TAP && keycode <= QK_LAYER_TAP_MAX)
#if !defined(NO_ACTION_LAYER) && !defined(NO_ACTION_TAPPING)
#    ifdef LEGACY_MAGIC_HANDLING
            return ACTION_LAYER_TAP_KEY(QK_LAYER_TAP_GET_LAYER(keycode), QK_LAYER_TAP_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            return ACTION_LAYER_TAP_KEY(QK_LAYER_TAP_GET_LAYER(keycode), keycode_config(QK_LAYER_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#else
            // pass through keycode_config again, since it previously missed it
            // and then only send as ACTION_KEY to bypass most of action.c handling
            return ACTION_KEY(keycode_config(QK_LAYER_TAP_GET_TAP_KEYCODE(keycode)));
#endif
#ifndef NO_ACTION_LAYER
        else if (keycode >= QK_TO && keycode <= QK_TO_MAX) {
            // Layer set "GOTO"
            action_layer = QK_TO_GET_LAYER(keycode);
            return ACTION_LAYER_GOTO(action_layer);
        }
        else if (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) {
            // Momentary action_layer
            action_layer = QK_MOMENTARY_GET_LAYER(keycode);
            return ACTION_LAYER_MOMENTARY(action_layer);
        }
        else if (keycode >= QK_DEF_LAYER && keycode <= QK_DEF_LAYER_MAX) {
            // Set default action_layer
            action_layer = QK_DEF_LAYER_GET_LAYER(keycode);
            return ACTION_DEFAULT_LAYER_SET(action_layer);
        }
        else if (keycode >= QK_TOGGLE_LAYER && keycode <= QK_TOGGLE_LAYER_MAX) {
            // Set toggle
            action_layer = QK_TOGGLE_LAYER_GET_LAYER(keycode);
            return ACTION_LAYER_TOGGLE(action_layer);
        }
#endif
#ifndef NO_ACTION_ONESHOT
        else if (keycode >= QK_ONE_SHOT_LAYER && keycode <= QK_ONE_SHOT_LAYER_MAX) {
            // OSL(action_layer) - One-shot action_layer
            action_layer = QK_ONE_SHOT_LAYER_GET_LAYER(keycode);
            return ACTION_LAYER_ONESHOT(action_layer);
        }
#endif // NO_ACTION_ONESHOT
        else if (keycode >= QK_ONE_SHOT_MOD && keycode <= QK_ONE_SHOT_MOD_MAX) {
            // OSM(mod) - One-shot mod
            mod = mod_config(QK_ONE_SHOT_MOD_GET_MODS(keycode));
#if defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
            return ACTION_MODS(mod);
#else  // defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
            return ACTION_MODS_ONESHOT(mod);
#endif // defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
        }
#ifndef NO_ACTION_LAYER
        else if (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX)
#    ifndef NO_ACTION_TAPPING
            return ACTION_LAYER_TAP_TOGGLE(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#    else // NO_ACTION_TAPPING
#        ifdef NO_ACTION_TAPPING_TAP_TOGGLE_MO
            return ACTION_LAYER_MOMENTARY(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#        else  // NO_ACTION_TAPPING_TAP_TOGGLE_MO
            return ACTION_LAYER_TOGGLE(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#        endif // NO_ACTION_TAPPING_TAP_TOGGLE_MO
#    endif     // NO_ACTION_TAPPING
        else if (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) {
            mod          = mod_config(QK_LAYER_MOD_GET_MODS(keycode));
            action_layer = QK_LAYER_MOD_GET_LAYER(keycode);
            return ACTION_LAYER_MODS(action_layer, (uint8_t)((mod & 0x10) ? mod << 4 : mod));
        }
#endif // NO_ACTION_LAYER
        else if (keycode >= QK_MOD_TAP && keycode <= QK_MOD_TAP_MAX) {
#ifndef NO_ACTION_TAPPING
            mod = mod_config(QK_MOD_TAP_GET_MODS(keycode));
#    ifdef LEGACY_MAGIC_HANDLING
            return ACTION_MODS_TAP_KEY(mod, QK_MOD_TAP_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            return ACTION_MODS_TAP_KEY(mod, keycode_config(QK_MOD_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#else      // NO_ACTION_TAPPING
#    ifdef NO_ACTION_TAPPING_MODTAP_MODS
            // pass through mod_config again, since it previously missed it
            // and then only send as ACTION_KEY to bypass most of action.c handling
            return ACTION_MODS(mod_config(QK_MOD_TAP_GET_MODS(keycode)));
#    else  // NO_ACTION_TAPPING_MODTAP_MODS
           // pass through keycode_config again, since it previously missed it
           // and then only send as ACTION_KEY to bypass most of action.c handling
            return ACTION_KEY(keycode_config(QK_MOD_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // NO_ACTION_TAPPING_MODTAP_MODS
#endif     // NO_ACTION_TAPPING
        }
#ifdef SWAP_HANDS_ENABLE
        else if (keycode >= QK_SWAP_HANDS && keycode <= QK_SWAP_HANDS_MAX) 
#    ifdef LEGACY_MAGIC_HANDLING
            return ACTION(ACT_SWAP_HANDS, QK_SWAP_HANDS_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            return ACTION(ACT_SWAP_HANDS, keycode_config(QK_SWAP_HANDS_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#endif

        else
            return ACTION_NO;
    //}
    //dprintf("action %x\n",action);
#endif
}
void process_action(keyrecord_t AK820_RECORD_MEM *record_argument, action_t action) {
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
    keyrecord_t __xdata *record = (keyrecord_t __xdata *)record_argument;
#else
    keyrecord_t *record = record_argument;
#endif
    bool pressed;
    uint8_t mods;
    pressed = record->event.pressed;
#ifndef NO_ACTION_TAPPING
    uint8_t tap_count;
    tap_count = record->tap.count;
#endif

#ifndef NO_ACTION_ONESHOT
    bool do_release_oneshot = false;
    // notice we only clear the one shot layer if the pressed key is not a modifier.
    if (is_oneshot_layer_active() && pressed &&
        (action.kind.id == ACT_USAGE || !(IS_MODIFIER_KEYCODE(action.key.code)
#    ifndef NO_ACTION_TAPPING
                                          || (tap_count == 0 && (action.kind.id == ACT_LMODS_TAP || action.kind.id == ACT_RMODS_TAP))
#    endif
                                              ))
#    ifdef SWAP_HANDS_ENABLE
        && !(action.kind.id == ACT_SWAP_HANDS && action.swap.code == OP_SH_ONESHOT)
#    endif
        && keymap_config.oneshot_enable) {
        clear_oneshot_layer_state(ONESHOT_OTHER_KEY_PRESSED);
        do_release_oneshot = !is_oneshot_layer_active();
    }
#endif

    switch (action.kind.id) {
        /* Key and Mods */
        case ACT_LMODS:
        case ACT_RMODS: {
            mods = (action.kind.id == ACT_LMODS) ? action.key.mods : action.key.mods << 4;
        ordinary_modifier_action:
            if (pressed) {
                if (mods) {
                    if (IS_MODIFIER_KEYCODE(action.key.code) || action.key.code == KC_NO) {
                        // e.g. LSFT(KC_LEFT_GUI): we don't want the LSFT to be weak as it would make it useless.
                        // This also makes LSFT(KC_LEFT_GUI) behave exactly the same as LGUI(KC_LEFT_SHIFT).
                        // Same applies for some keys like KC_MEH which are declared as MEH(KC_NO).
                        add_owned_mods(mods);
                    } else {
                        add_owned_weak_mods(mods);
                    }
                    send_keyboard_report();
                }
                register_code(action.key.code);
            } else {
                unregister_code(action.key.code);
                if (mods) {
                    if (IS_MODIFIER_KEYCODE(action.key.code) || action.key.code == KC_NO) {
                        del_owned_mods(mods);
                    } else {
                        del_owned_weak_mods(mods);
                    }
                    send_keyboard_report();
                }
            }
        } break;
        case ACT_LMODS_TAP:
        case ACT_RMODS_TAP: {
#ifndef NO_ACTION_TAPPING
            mods = (action.kind.id == ACT_LMODS_TAP) ? action.key.mods : action.key.mods << 4;
            switch (action.layer_tap.code) {
#    ifndef NO_ACTION_ONESHOT
                case MODS_ONESHOT:
                    // Oneshot modifier
                    if (!keymap_config.oneshot_enable) {
                        goto ordinary_modifier_action;
                    } else {
                        if (pressed) {
                            if (tap_count == 0) {
                                // Not a tap, but a hold: register the held mod
                                ac_dprintf("MODS_TAP: Oneshot: 0\n");
                                register_mods(mods);
                            } else if (tap_count == 1) {
                                ac_dprintf("MODS_TAP: Oneshot: start\n");
                                add_oneshot_mods(mods);
                            } else if (QS_oneshot_tap_toggle > 1 && tap_count == QS_oneshot_tap_toggle) {
                                ac_dprintf("MODS_TAP: Toggling oneshot");
                                register_mods(mods);
                                del_oneshot_mods(mods);
                                add_oneshot_locked_mods(mods);
                            }
                        } else {
                            if (tap_count == 0 || (QS_oneshot_tap_toggle > 1 && tap_count == 1 && (mods & get_mods()))) {
                                // Release hold/lock and every modifier variant through one tail.
                                unregister_mods(mods);
                                del_oneshot_mods(mods);
                                del_oneshot_locked_mods(mods);
                            }
                        }
                    }
                    break;
#    endif
                case MODS_TAP_TOGGLE:
                    if (pressed) {
                        if (tap_count <= QS_tapping_toggle) {
                            register_mods(mods);
                        }
                    } else {
                        if (tap_count < QS_tapping_toggle) {
                            unregister_mods(mods);
                        }
                    }
                    break;
                default:
#    ifdef HOLD_ON_OTHER_KEY_PRESS_PER_KEY
                    if (pressed && tap_count > 0 &&
                        get_hold_on_other_key_press(get_event_keycode(record->event, false), record) &&
                        record->tap.interrupted) {
                        record->tap.count = 0;
                        register_mods(mods);
                        break;
                    }
#    endif
                    if (tap_count > 0) {
                        goto ordinary_tap_action;
                    }
                    if (pressed) {
                        register_mods(mods);
                    } else {
#    if defined(RETRO_TAPPING) && defined(DUMMY_MOD_NEUTRALIZER_KEYCODE)
                        if (retro_tapping_counter == 2) {
                            neutralize_flashing_modifiers(get_mods());
                        }
#    endif
                        unregister_mods(mods);
                    }
                    break;
            }
#endif // NO_ACTION_TAPPING
        } break;
#ifdef EXTRAKEY_ENABLE
        /* other HID usage */
        case ACT_USAGE:
#ifdef AK820_COMPACT_TAPPING
            /* The only pipeline caller decodes this frozen record. In the
             * supported profile ACT_USAGE comes only from basic A5..C2;
             * encoded modifiers use register_code instead. Keep the raw
             * action API when a caller has no corresponding basic record. */
            if (record->keycode >= KC_SYSTEM_POWER && record->keycode <= KC_LAUNCHPAD) {
                owned_usage_key((uint8_t)record->keycode, pressed);
                break;
            }
#endif
            switch (action.usage.page) {
                case PAGE_SYSTEM:
                    host_system_send(pressed ? action.usage.code : 0);
                    break;
                case PAGE_CONSUMER:
                    host_consumer_send(pressed ? action.usage.code : 0);
                    break;
            }
            break;
#endif // EXTRAKEY_ENABLE
        /* Mouse key */
        case ACT_MOUSEKEY:
            register_mouse(action.key.code, pressed);
            break;
#ifndef NO_ACTION_LAYER
        case ACT_LAYER: {
            uint8_t on = action.layer_bitop.on;
            /* Both layer banks use the same mask. Keep their separate setters
             * so held-layer ownership and default-layer hooks are preserved. */
            if (on ? (pressed ? (on & ON_PRESS) : (on & ON_RELEASE)) : !pressed) {
                uint8_t shift = action.layer_bitop.part * 4;
                layer_state_t bits = ((layer_state_t)action.layer_bitop.bits) << shift;
                layer_state_t mask = action.layer_bitop.xbit ? ~(((layer_state_t)0xf) << shift) : 0;
                bits |= mask;
                if (!on) {
                    switch (action.layer_bitop.op) {
                        case OP_BIT_AND: default_layer_and(bits); break;
                        case OP_BIT_OR: default_layer_or(bits); break;
                        case OP_BIT_XOR: default_layer_xor(bits); break;
                        case OP_BIT_SET: default_layer_set(bits); break;
                    }
                } else {
                    switch (action.layer_bitop.op) {
                        case OP_BIT_AND: layer_and(bits); break;
                        case OP_BIT_OR: layer_or(bits); break;
                        case OP_BIT_XOR: layer_xor(bits); break;
                        case OP_BIT_SET: layer_state_set(bits); break;
                    }
                }
            }
            break;
        }
        case ACT_LAYER_MODS:
            if (pressed) {
                layer_hold_on(action.layer_mods.layer);
                register_mods(action.layer_mods.mods);
            } else {
                unregister_mods(action.layer_mods.mods);
                layer_hold_off(action.layer_mods.layer);
            }
            break;
        case ACT_LAYER_TAP:
        case ACT_LAYER_TAP_EXT:
            switch (action.layer_tap.code) {
#    ifndef NO_ACTION_TAPPING
                case OP_TAP_TOGGLE:
                    /* tap toggle */
                    if (pressed) {
                        if (tap_count < QS_tapping_toggle) {
                            layer_invert(action.layer_tap.val);
                        }
                    } else {
                        if (tap_count <= QS_tapping_toggle) {
                            layer_invert(action.layer_tap.val);
                        }
                    }
                    break;
#    endif
                case OP_ON_OFF:
                momentary_layer_action:
                    pressed ? layer_hold_on(action.layer_tap.val) : layer_hold_off(action.layer_tap.val);
                    break;
                case OP_OFF_ON:
                    pressed ? layer_off(action.layer_tap.val) : layer_on(action.layer_tap.val);
                    break;
                case OP_SET_CLEAR:
                    pressed ? layer_move(action.layer_tap.val) : layer_clear();
                    break;
#    if !defined(NO_ACTION_ONESHOT) && !defined(NO_ACTION_TAPPING)
                case OP_ONESHOT:
                    // Oneshot modifier
                    if (!keymap_config.oneshot_enable) {
                        goto momentary_layer_action;
                    } else {
if (QS_oneshot_tap_toggle > 1) {
                        do_release_oneshot = false;
                        if (pressed) {
                            if (get_oneshot_layer_state() == ONESHOT_TOGGLED) {
                                reset_oneshot_layer();
                                layer_off(action.layer_tap.val);
                                break;
                            } else if (tap_count < QS_oneshot_tap_toggle) {
                                layer_on(action.layer_tap.val);
                                set_oneshot_layer(action.layer_tap.val, ONESHOT_START);
                            }
                        } else {
                            if (tap_count >= QS_oneshot_tap_toggle) {
                                reset_oneshot_layer();
                                set_oneshot_layer(action.layer_tap.val, ONESHOT_TOGGLED);
                            } else {
                                clear_oneshot_layer_state(ONESHOT_PRESSED);
                            }
                        }
} else {
                        if (pressed) {
                            layer_on(action.layer_tap.val);
                            set_oneshot_layer(action.layer_tap.val, ONESHOT_START);
                        } else {
                            clear_oneshot_layer_state(ONESHOT_PRESSED);
                            if (tap_count > 1) {
                                clear_oneshot_layer_state(ONESHOT_OTHER_KEY_PRESSED);
                            }
                        }
}
                    }
#    else  // NO_ACTION_ONESHOT && NO_ACTION_TAPPING
                    if (pressed) {
                        layer_on(action.layer_tap.val);
                    } else {
                        layer_off(action.layer_tap.val);
                    }
#    endif // !defined(NO_ACTION_ONESHOT) && !defined(NO_ACTION_TAPPING)
                    break;
                default:
#    ifndef NO_ACTION_TAPPING /* tap key */
                    if (tap_count > 0) {
                        goto ordinary_tap_action;
                    }
                    goto momentary_layer_action;
#    else
                    if (pressed) {
                        ac_dprintf("KEYMAP_TAP_KEY: Tap: register_code\n");
                        register_code(action.layer_tap.code);
                    } else {
                        ac_dprintf("KEYMAP_TAP_KEY: Tap: unregister_code\n");
                        if (action.layer_tap.code == KC_CAPS) {
                            wait_ms(TAP_HOLD_CAPS_DELAY);
                        } else {
                            wait_ms(TAP_CODE_DELAY);
                        }
                        unregister_code(action.layer_tap.code);
                    }
#    endif
                    break;
            }
            break;
#endif // NO_ACTION_LAYER

#ifdef SWAP_HANDS_ENABLE
        case ACT_SWAP_HANDS:
            switch (action.swap.code) {
                case OP_SH_TOGGLE:
                    if (pressed) {
                        swap_hands = !swap_hands;
                    }
                    break;
                case OP_SH_ON_OFF:
                    swap_hands = pressed;
                    break;
                case OP_SH_OFF_ON:
                    swap_hands = !pressed;
                    break;
                case OP_SH_ON:
                    if (!pressed) {
                        swap_hands = true;
                    }
                    break;
                case OP_SH_OFF:
                    if (!pressed) {
                        swap_hands = false;
                    }
                    break;
#    ifndef NO_ACTION_ONESHOT
                case OP_SH_ONESHOT:
                    if (pressed) {
                        set_oneshot_swaphands();
                    } else {
                        release_oneshot_swaphands();
                    }
                    break;
#    endif

#    ifndef NO_ACTION_TAPPING
                case OP_SH_TAP_TOGGLE:
                    /* tap toggle */

                    if (pressed) {
                        if (swap_held) {
                            swap_held = false;
                        } else {
                            swap_hands = !swap_hands;
                        }
                    } else {
                        if (tap_count < QS_tapping_toggle) {
                            swap_hands = !swap_hands;
                        }
                    }
                    break;
                default:
                    /* tap key */
                    if (tap_count > 0) {
                        if (swap_held) {
                            swap_hands = !swap_hands; // undo hold set up in _tap_hint
                            swap_held  = false;
                        }
                        if (pressed) {
                            register_code(action.swap.code);
                        } else {
                            qs_wait_ms(QS_tap_code_delay);
                            unregister_code(action.swap.code);
                            *record = (keyrecord_t){}; // hack: reset tap mode
                        }
                    } else {
                        if (swap_held && !pressed) {
                            swap_hands = !swap_hands; // undo hold set up in _tap_hint
                            swap_held  = false;
                        }
                    }
#    endif
            }
#endif
        default:
            break;
    }

#ifndef NO_ACTION_TAPPING
    goto action_complete;
ordinary_tap_action:
    // MT and LT share the same basic tap output, including the release delay.
    if (pressed) {
        register_code(action.key.code);
    } else {
        if (action.key.code == KC_CAPS_LOCK) {
            qs_wait_ms(QS_tap_hold_caps_delay);
        } else {
            qs_wait_ms(QS_tap_code_delay);
        }
        unregister_code(action.key.code);
    }
action_complete:
#endif

#ifndef NO_ACTION_LAYER
    // if this event is a layer action, update the leds
    switch (action.kind.id) {
        case ACT_LAYER:
        case ACT_LAYER_MODS:
#    ifndef NO_ACTION_TAPPING
        case ACT_LAYER_TAP:
        case ACT_LAYER_TAP_EXT:
#    endif
            led_set(host_keyboard_leds());
            break;
        default:
            break;
    }
#endif

#ifndef NO_ACTION_TAPPING
#    if defined(RETRO_TAPPING) || defined(RETRO_TAPPING_PER_KEY) || (defined(AUTO_SHIFT_ENABLE) && defined(RETRO_SHIFT))
    if (!is_tap_action(action)) {
        retro_tapping_counter = 0;
    } else {
        if (pressed) {
            if (tap_count > 0) {
                retro_tapping_counter = 0;
            }
        } else {
            if (tap_count > 0) {
                retro_tapping_counter = 0;
            } else {
                if (
#        ifdef RETRO_TAPPING_PER_KEY
                    get_retro_tapping(get_event_keycode(record->event, false), record) &&
#        endif
                    retro_tapping_counter == 2) {
#        if defined(AUTO_SHIFT_ENABLE) && defined(RETRO_SHIFT)
                    process_auto_shift(action.layer_tap.code, record);
#        else
                    tap_code(action.layer_tap.code);
#        endif
                }
                retro_tapping_counter = 0;
            }
        }
    }
#    endif
#endif

#ifdef SWAP_HANDS_ENABLE
#    ifndef NO_ACTION_ONESHOT
    if (pressed && !(action.kind.id == ACT_SWAP_HANDS && action.swap.code == OP_SH_ONESHOT)) {
        use_oneshot_swaphands();
    }
#    endif
#endif

#ifndef NO_ACTION_ONESHOT
    /* Because we switch layers after a oneshot event, we need to release the
     * key before we leave the layer or no key up event will be generated.
     */
    if (do_release_oneshot && !(get_oneshot_layer_state() & ONESHOT_PRESSED)) {
        record->event.pressed = false;
        layer_on(get_oneshot_layer());
        process_record(record);
        layer_off(get_oneshot_layer());
    }
#endif
}
void backend(keyrecord_t AK820_RECORD_MEM *r,uint16_t keycode) { action_t a; a.code=action_for_keycode(keycode); process_action(r,a); }
