/* GPL-2.0-or-later: immutable RC4 decoder reference, commit cb9ff6ea. */
uint16_t rc4_action_for_keycode(uint16_t keycode) {
    // keycode remapping
    keycode = keycode_config(keycode);

    action_t action = {.code=0};
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
            action.code = ACTION_KEY(keycode);
            //dprintf("%x\n",action.code);
        }
#ifdef EXTRAKEY_ENABLE
        else if (keycode >= KC_SYSTEM_POWER && keycode <= KC_SYSTEM_WAKE)
            action.code = ACTION_USAGE_SYSTEM(KEYCODE2SYSTEM(keycode));
        else if (keycode >= KC_AUDIO_MUTE && keycode <= KC_LAUNCHPAD)
            action.code = ACTION_USAGE_CONSUMER(KEYCODE2CONSUMER(keycode));
#endif
        else if (keycode >= KC_MS_UP && keycode <= KC_MS_ACCEL2)
            action.code = ACTION_MOUSEKEY(keycode);
        else if (keycode == KC_TRANSPARENT)
            action.code = ACTION_TRANSPARENT;
        else if (keycode >= QK_MODS && keycode <= QK_MODS_MAX)
        // Has a modifier
        // Split it up
#ifdef LEGACY_MAGIC_HANDLING
            action.code = ACTION_MODS_KEY(QK_MODS_GET_MODS(keycode), QK_MODS_GET_BASIC_KEYCODE(keycode)); // adds modifier to key
#else                                                                                                     // LEGACY_MAGIC_HANDLING
            action.code = ACTION_MODS_KEY(mod_config(QK_MODS_GET_MODS(keycode)), keycode_config(QK_MODS_GET_BASIC_KEYCODE(keycode))); // adds modifier to key
#endif                                                                                                    // LEGACY_MAGIC_HANDLING
        else if (keycode >= QK_LAYER_TAP && keycode <= QK_LAYER_TAP_MAX)
#if !defined(NO_ACTION_LAYER) && !defined(NO_ACTION_TAPPING)
#    ifdef LEGACY_MAGIC_HANDLING
            action.code = ACTION_LAYER_TAP_KEY(QK_LAYER_TAP_GET_LAYER(keycode), QK_LAYER_TAP_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            action.code = ACTION_LAYER_TAP_KEY(QK_LAYER_TAP_GET_LAYER(keycode), keycode_config(QK_LAYER_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#else
            // pass through keycode_config again, since it previously missed it
            // and then only send as ACTION_KEY to bypass most of action.c handling
            action.code = ACTION_KEY(keycode_config(QK_LAYER_TAP_GET_TAP_KEYCODE(keycode)));
#endif
#ifndef NO_ACTION_LAYER
        else if (keycode >= QK_TO && keycode <= QK_TO_MAX) {
            // Layer set "GOTO"
            action_layer = QK_TO_GET_LAYER(keycode);
            action.code  = ACTION_LAYER_GOTO(action_layer);
        }
        else if (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) {
            // Momentary action_layer
            action_layer = QK_MOMENTARY_GET_LAYER(keycode);
            action.code  = ACTION_LAYER_MOMENTARY(action_layer);
        }
        else if (keycode >= QK_DEF_LAYER && keycode <= QK_DEF_LAYER_MAX) {
            // Set default action_layer
            action_layer = QK_DEF_LAYER_GET_LAYER(keycode);
            action.code  = ACTION_DEFAULT_LAYER_SET(action_layer);
        }
        else if (keycode >= QK_TOGGLE_LAYER && keycode <= QK_TOGGLE_LAYER_MAX) {
            // Set toggle
            action_layer = QK_TOGGLE_LAYER_GET_LAYER(keycode);
            action.code  = ACTION_LAYER_TOGGLE(action_layer);
        }
#endif
#ifndef NO_ACTION_ONESHOT
        else if (keycode >= QK_ONE_SHOT_LAYER && keycode <= QK_ONE_SHOT_LAYER_MAX) {
            // OSL(action_layer) - One-shot action_layer
            action_layer = QK_ONE_SHOT_LAYER_GET_LAYER(keycode);
            action.code  = ACTION_LAYER_ONESHOT(action_layer);
        }
#endif // NO_ACTION_ONESHOT
        else if (keycode >= QK_ONE_SHOT_MOD && keycode <= QK_ONE_SHOT_MOD_MAX) {
            // OSM(mod) - One-shot mod
            mod = mod_config(QK_ONE_SHOT_MOD_GET_MODS(keycode));
#if defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
            action.code = ACTION_MODS(mod);
#else  // defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
            action.code = ACTION_MODS_ONESHOT(mod);
#endif // defined(NO_ACTION_TAPPING) || defined(NO_ACTION_ONESHOT)
        }
#ifndef NO_ACTION_LAYER
        else if (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX)
#    ifndef NO_ACTION_TAPPING
            action.code = ACTION_LAYER_TAP_TOGGLE(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#    else // NO_ACTION_TAPPING
#        ifdef NO_ACTION_TAPPING_TAP_TOGGLE_MO
            action.code = ACTION_LAYER_MOMENTARY(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#        else  // NO_ACTION_TAPPING_TAP_TOGGLE_MO
            action.code = ACTION_LAYER_TOGGLE(QK_LAYER_TAP_TOGGLE_GET_LAYER(keycode));
#        endif // NO_ACTION_TAPPING_TAP_TOGGLE_MO
#    endif     // NO_ACTION_TAPPING
        else if (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) {
            mod          = mod_config(QK_LAYER_MOD_GET_MODS(keycode));
            action_layer = QK_LAYER_MOD_GET_LAYER(keycode);
            action.code  = ACTION_LAYER_MODS(action_layer, (mod & 0x10) ? mod << 4 : mod);
        }
#endif // NO_ACTION_LAYER
        else if (keycode >= QK_MOD_TAP && keycode <= QK_MOD_TAP_MAX) {
#ifndef NO_ACTION_TAPPING
            mod = mod_config(QK_MOD_TAP_GET_MODS(keycode));
#    ifdef LEGACY_MAGIC_HANDLING
            action.code = ACTION_MODS_TAP_KEY(mod, QK_MOD_TAP_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            action.code = ACTION_MODS_TAP_KEY(mod, keycode_config(QK_MOD_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#else      // NO_ACTION_TAPPING
#    ifdef NO_ACTION_TAPPING_MODTAP_MODS
            // pass through mod_config again, since it previously missed it
            // and then only send as ACTION_KEY to bypass most of action.c handling
            action.code = ACTION_MODS(mod_config(QK_MOD_TAP_GET_MODS(keycode)));
#    else  // NO_ACTION_TAPPING_MODTAP_MODS
           // pass through keycode_config again, since it previously missed it
           // and then only send as ACTION_KEY to bypass most of action.c handling
            action.code = ACTION_KEY(keycode_config(QK_MOD_TAP_GET_TAP_KEYCODE(keycode)));
#    endif // NO_ACTION_TAPPING_MODTAP_MODS
#endif     // NO_ACTION_TAPPING
        }
#ifdef SWAP_HANDS_ENABLE
        else if (keycode >= QK_SWAP_HANDS && keycode <= QK_SWAP_HANDS_MAX) 
#    ifdef LEGACY_MAGIC_HANDLING
            action.code = ACTION(ACT_SWAP_HANDS, QK_SWAP_HANDS_GET_TAP_KEYCODE(keycode));
#    else  // LEGACY_MAGIC_HANDLING
            action.code = ACTION(ACT_SWAP_HANDS, keycode_config(QK_SWAP_HANDS_GET_TAP_KEYCODE(keycode)));
#    endif // LEGACY_MAGIC_HANDLING
#endif

        else
            action.code = ACTION_NO;
    //}
    //dprintf("action %x\n",action);
    return action.code;
}

