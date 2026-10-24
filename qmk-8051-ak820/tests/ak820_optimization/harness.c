/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "action_layer.h"
#include "keymap_common.h"
#include "quantum_keycodes.h"
#include "report.h"
#define VIAL_MATRIX_MAGIC 240
bool disable_action_cache;
uint16_t keycode_config(uint16_t keycode) { return keycode; }
uint8_t mod_config(uint8_t mods) { return mods; }
bool vial_unlock_in_progress;
uint16_t g_vial_magic_keycode_override;
static uint16_t test_map[1u << MAX_LAYER_BITS][MATRIX_ROWS][MATRIX_COLS];
static uint16_t encoder_map[1u << MAX_LAYER_BITS][NUM_ENCODERS][2];
uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key) {
    if (vial_unlock_in_progress) return KC_NO;
    if (key.row == VIAL_MATRIX_MAGIC && key.col == VIAL_MATRIX_MAGIC) return g_vial_magic_keycode_override;
    assert(layer < (1u << MAX_LAYER_BITS));
    if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) return test_map[layer][key.row][key.col];
    if ((key.row == KEYLOC_ENCODER_CW || key.row == KEYLOC_ENCODER_CCW) && key.col < NUM_ENCODERS)
        return encoder_map[layer][key.col][key.row == KEYLOC_ENCODER_CW];
    return KC_NO;
}
uint16_t ak820_keycode_at(uint8_t layer, uint16_t position) {
    keypos_t key={.row=position>>8,.col=position};
    return keymap_key_to_keycode(layer,key);
}
uint16_t action_for_key(uint8_t layer, keypos_t key) { return action_for_keycode(keymap_key_to_keycode(layer, key)); }

/* PRODUCTION */

int main(void) {
    unsigned opaque_compact_taps = 0;
    for (uint32_t code = 0; code <= UINT16_MAX; ++code) {
        uint16_t actual = action_for_keycode(code), expected = rc4_action_for_keycode(code);
#ifdef AK820_COMPACT_TAPPING
        /* MT/LT payloads are consumed by the compact engine before the
         * ordinary action dispatcher. The decoder contract is opaque ACTION_NO;
         * linked-pipeline tests cover their actual tap/hold behavior. */
        if ((code >= QK_MOD_TAP && code <= QK_MOD_TAP_MAX) ||
            (code >= QK_LAYER_TAP && code <= QK_LAYER_TAP_MAX)) {
            expected = ACTION_NO;
            ++opaque_compact_taps;
        }
#endif
        if (code >= QK_LAYER_MOD && code <= QK_LAYER_MOD_MAX) {
            uint8_t mods = QK_LAYER_MOD_GET_MODS(code);
            if (mods & 0x10) mods = (uint8_t)(mods << 4);
            expected = ACTION_LAYER_MODS(QK_LAYER_MOD_GET_LAYER(code), mods);
        }
        if (actual != expected) {
            fprintf(stderr, "decoder mismatch %04x: %04x != %04x\n", (unsigned)code, actual, expected);
            return 1;
        }
    }
#ifdef AK820_COMPACT_TAPPING
    assert(opaque_compact_taps == (QK_MOD_TAP_MAX - QK_MOD_TAP + 1) +
                                  (QK_LAYER_TAP_MAX - QK_LAYER_TAP + 1));
#endif
    for (unsigned layer = 0; layer < (1u << MAX_LAYER_BITS); ++layer) {
        for (unsigned row = 0; row < MATRIX_ROWS; ++row)
            for (unsigned col = 0; col < MATRIX_COLS; ++col)
                test_map[layer][row][col] = 0x1000 | (layer << 8) | (row * MATRIX_COLS + col);
        for (unsigned encoder = 0; encoder < NUM_ENCODERS; ++encoder) {
            encoder_map[layer][encoder][0] = KC_VOLD;
            encoder_map[layer][encoder][1] = KC_VOLU;
        }
    }
    for (unsigned layer = 0; layer <= UINT8_MAX; ++layer) {
        for (unsigned row = 0; row < MATRIX_ROWS; ++row)
            for (unsigned col = 0; col < MATRIX_COLS; ++col) {
                keypos_t key = {.row = row, .col = col};
                update_source_layers_cache(key, layer);
                unsigned masked = layer & ((1u << MAX_LAYER_BITS) - 1);
#ifdef KEY_OVERRIDE_ENABLE
                assert(read_source_layers_cache(key) == masked);
#endif
                assert(read_source_keycode_cache(key) == test_map[masked][row][col]);
            }
    }
    for (unsigned row = 0; row < MATRIX_ROWS; ++row)
        for (unsigned col = 0; col < MATRIX_COLS; ++col) {
            keypos_t key = {.row = row, .col = col};
            update_source_layers_cache(key, (row + col) % DYNAMIC_KEYMAP_LAYER_COUNT);
        }
    for (unsigned row = 0; row <= UINT8_MAX; ++row)
        for (unsigned col = 0; col <= UINT8_MAX; ++col) {
            if (row < MATRIX_ROWS && col < MATRIX_COLS) continue;
            if ((row == KEYLOC_ENCODER_CW || row == KEYLOC_ENCODER_CCW) && col < NUM_ENCODERS) continue;
            keypos_t key = {.row = row, .col = col};
            update_source_layers_cache(key, 7);
#ifdef KEY_OVERRIDE_ENABLE
            assert(read_source_layers_cache(key) == 0);
#endif
            assert(read_source_keycode_cache(key) == KC_NO);
        }
    for (unsigned row = 0; row < MATRIX_ROWS; ++row)
        for (unsigned col = 0; col < MATRIX_COLS; ++col) {
            keypos_t key = {.row = row, .col = col};
            unsigned layer = (row + col) % DYNAMIC_KEYMAP_LAYER_COUNT;
#ifdef KEY_OVERRIDE_ENABLE
            assert(read_source_layers_cache(key) == layer);
#endif
            assert(read_source_keycode_cache(key) == test_map[layer][row][col]);
        }
    /* A resolved compound key may replace only its keycode, preserving its
     * optional source-layer information and all neighboring slots. */
    for (unsigned row = 0; row < MATRIX_ROWS; ++row)
        for (unsigned col = 0; col < MATRIX_COLS; ++col) {
            keypos_t key = {.row = row, .col = col};
            assert(update_source_keycode_cache(key, 0x4000 | (row * MATRIX_COLS + col)));
#ifdef KEY_OVERRIDE_ENABLE
            assert(read_source_layers_cache(key) == (row + col) % DYNAMIC_KEYMAP_LAYER_COUNT);
#endif
        }
    for (unsigned row = 0; row <= UINT8_MAX; ++row)
        for (unsigned col = 0; col <= UINT8_MAX; ++col) {
            bool valid = (row < MATRIX_ROWS && col < MATRIX_COLS) ||
                         ((row == KEYLOC_ENCODER_CW || row == KEYLOC_ENCODER_CCW) && col < NUM_ENCODERS);
            if (!valid) {
                keypos_t key = {.row = row, .col = col};
                assert(!update_source_keycode_cache(key, UINT16_MAX));
            }
        }
    for (unsigned row = 0; row < MATRIX_ROWS; ++row)
        for (unsigned col = 0; col < MATRIX_COLS; ++col) {
            keypos_t key = {.row = row, .col = col};
            assert(read_source_keycode_cache(key) == (0x4000 | (row * MATRIX_COLS + col)));
        }
    const uint16_t held_codes[] = {KC_A, KC_LSFT, MO(1), LM(2, MOD_LCTL), TG(3), KC_MUTE};
    for (uint8_t layer = 0; layer < DYNAMIC_KEYMAP_LAYER_COUNT; ++layer)
        for (unsigned i = 0; i < sizeof(held_codes) / sizeof(held_codes[0]); ++i) {
            keypos_t key = {.row = 3, .col = 4};
            keyevent_t press = {.key = key, .pressed = true, .time = 1};
            test_map[layer][key.row][key.col] = held_codes[i];
            layer_state = 1u << layer;
            assert(get_event_keycode(press, true) == held_codes[i]);
            assert(store_or_get_action(true, key) == action_for_keycode(held_codes[i]));
            /* Vial writes the occupied slot while the physical key is held. */
            test_map[layer][key.row][key.col] = KC_B;
            layer_state = 1u << ((layer + 1) % DYNAMIC_KEYMAP_LAYER_COUNT);
            press.pressed = false;
            assert(get_event_keycode(press, true) == held_codes[i]);
            assert(store_or_get_action(false, key) == action_for_keycode(held_codes[i]));
            layer_state = 1u << layer;
            press.pressed = true;
            assert(get_event_keycode(press, true) == KC_B);
            assert(store_or_get_action(true, key) == action_for_keycode(KC_B));
        }
    for (uint8_t layer = 0; layer < DYNAMIC_KEYMAP_LAYER_COUNT; ++layer) {
        keypos_t key = {.row = KEYLOC_ENCODER_CW, .col = 0};
        update_source_layers_cache(key, layer);
        encoder_map[layer][0][1] = KC_A;
        assert(read_source_keycode_cache(key) == KC_VOLU);
        key.row = KEYLOC_ENCODER_CCW;
        update_source_layers_cache(key, layer);
#ifdef KEY_OVERRIDE_ENABLE
        assert(read_source_layers_cache(key) == layer);
#endif
        /* CW and CCW use independent source slots, so remapping one direction
         * while the other is cached does not replace its held keycode. */
        assert(read_source_keycode_cache(key) == KC_VOLD);
        update_source_layers_cache(key, layer);
        assert(read_source_keycode_cache(key) == KC_VOLD);
        assert(update_source_keycode_cache(key, KC_ESC));
        key.row = KEYLOC_ENCODER_CW;
        assert(read_source_keycode_cache(key) == KC_VOLU);
#ifdef KEY_OVERRIDE_ENABLE
        assert(read_source_layers_cache(key) == layer);
#endif
    }
    keypos_t magic = {.row = VIAL_MATRIX_MAGIC, .col = VIAL_MATRIX_MAGIC};
    g_vial_magic_keycode_override = KC_X;
    assert(read_source_keycode_cache(magic) == KC_X);
    vial_unlock_in_progress = true;
    assert(read_source_keycode_cache(magic) == KC_NO);
    keypos_t physical = {.row = 3, .col = 4};
    assert(read_source_keycode_cache(physical) == KC_NO);
    vial_unlock_in_progress = false;
    puts("PASS: all 65536 decoder inputs satisfy RC4 ordinary-action semantics, the LM right-mod correction and opaque compact MT/LT decoding; all cache coordinates/layer bytes, live remap A/modifier/MO/LM/toggle/consumer releases, encoder, virtual keys and unlock suppression.");
}
