#include "sdcc_dummy_macros.h"
/*
Copyright 2012-2017 Jun Wako <wakojun@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "keymap_common.h"
#include "keymap_introspection.h"
#include "report.h"
#include "keycode.h"
#include "action_layer.h"
#include "action.h"
#include "debug.h"
#include "keycode_config.h"
#if defined(AK820_BOARD) && !defined(MAGIC_KEYCODE_ENABLE)
/* This profile has no Magic remapping; the external functions are identities. */
#    define keycode_config(keycode) ((uint16_t)(keycode))
#    define mod_config(mods) ((uint8_t)(mods))
#endif

#include "quantum_keycodes.h"

#ifdef ENCODER_MAP_ENABLE
#    include "encoder.h"
#endif

#ifdef BACKLIGHT_ENABLE
#    include "backlight.h"
#endif

#ifdef MIDI_ENABLE
#    include "process_midi.h"
#endif

#ifdef VIAL_ENABLE
#    include "vial.h"
#endif

extern keymap_config_t keymap_config;

#include <inttypes.h>

/* converts key to action */
uint16_t action_for_key(uint8_t layer, keypos_t key) {
    // 16bit keycodes - important
    //ac_dprintf("layer: %x\n",layer);
    uint16_t keycode = keymap_key_to_keycode(layer, key);
    //ac_dprintf("keycode: %x\n",keycode);
    return action_for_keycode(keycode);
}

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
    if (kind < 0x50) return ACTION_KEY(key); /* MT and LT: existing tap-only fallback. */
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

// translates key to keycode
__attribute__((weak)) uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key) {
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
