/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdio.h>
#ifdef TEST_ACTION_TAPPING
#    undef NO_ACTION_TAPPING
#endif
#include "action.h"
#include "caps_word.h"
#include "quantum_keycodes.h"

static uint16_t now;
static uint8_t mods, weak_mods;
static unsigned reports;
uint16_t timer_read(void) { return now; }
uint8_t get_mods(void) { return mods; }
void clear_mods(void) { mods = 0; }
void clear_weak_mods(void) { weak_mods = 0; }
void add_weak_mods(uint8_t value) { weak_mods |= value; }
void unregister_weak_mods(uint8_t value) { weak_mods &= ~value; ++reports; }
void send_keyboard_report(void) { ++reports; }
bool caps_word_press_user(uint16_t keycode);

/* ACTUAL_CAPS_WORD */

static bool key_tap(uint16_t keycode, bool pressed, uint8_t count) {
    keyrecord_t record = {0};
    record.event.pressed = pressed;
#ifndef NO_ACTION_TAPPING
    record.tap.count = count;
#endif
    return process_caps_word(keycode, &record);
}

static bool key(uint16_t keycode, bool pressed) {
    return key_tap(keycode, pressed, 0);
}

#ifdef TEST_ACTION_TAPPING
static void layer_tap_bounds(void) {
    /* All 16 layers and all 256 tap keycodes: holding LT preserves Caps
     * Word; tapping sends the low byte through the actual user callback. */
    for (uint16_t code = QK_LAYER_TAP; code <= QK_LAYER_TAP_MAX; ++code) {
        caps_word_off(); clear_weak_mods(); caps_word_on();
        assert(key_tap(code, true, 0) && is_caps_word_on() && !weak_mods);
        assert(key_tap(code, false, 0) && is_caps_word_on());
        const bool expected_active = caps_word_press_user(code & 0xFF);
        const uint8_t expected_weak = weak_mods;
        caps_word_off(); clear_weak_mods(); caps_word_on();
        assert(key_tap(code, true, 1));
        assert(is_caps_word_on() == expected_active && weak_mods == expected_weak);
        assert(key_tap(code, false, 1));
    }
    /* Adjacent non-LT codes and high quantum codes must not be mistaken
     * for held LT keys, which would silently preserve Caps Word. */
    const uint16_t outside[] = {QK_LAYER_TAP - 1, QK_LAYER_TAP_MAX + 1, 0x5004, QK_REPEAT_KEY, QK_USER, UINT16_MAX};
    for (unsigned i = 0; i < sizeof(outside) / sizeof(outside[0]); ++i) {
        caps_word_off(); clear_weak_mods(); caps_word_on();
        assert(key_tap(outside[i], true, 0) && !is_caps_word_on() && !weak_mods);
    }
    puts("PASS: tapping-enabled Caps Word: 4096 LT hold/tap assignments, release, adjacent/high keycode boundaries.");
}
#endif

int main(void) {
    assert(!is_caps_word_on());
#ifdef TEST_ACTION_TAPPING
    layer_tap_bounds();
#endif
    assert(!key(QK_CAPS_WORD_TOGGLE, true) && is_caps_word_on());
    assert(!key(QK_CAPS_WORD_TOGGLE, false) && is_caps_word_on());
    for (uint16_t code = KC_A; code <= KC_Z; ++code) {
        assert(key(code, true) && is_caps_word_on() && weak_mods == MOD_BIT(KC_LSFT));
        assert(key(code, false) && is_caps_word_on());
    }
    const uint16_t unshifted[] = {KC_1, KC_0, KC_BSPC, KC_DEL, KC_UNDS};
    for (unsigned i = 0; i < sizeof(unshifted) / sizeof(unshifted[0]); ++i) {
        assert(key(unshifted[i], true) && is_caps_word_on() && !weak_mods);
    }
    assert(key(KC_MINS, true) && is_caps_word_on() && weak_mods == MOD_BIT(KC_LSFT));
    const uint16_t layers[] = {MO(5), TO(5), TG(5), TT(5), OSL(5)};
    for (unsigned i = 0; i < sizeof(layers) / sizeof(layers[0]); ++i)
        assert(key(layers[i], true) && is_caps_word_on());
    assert(key(KC_SPACE, true) && !is_caps_word_on() && !weak_mods);

    /* These codes exposed the port's missing upper bound on QK_MOMENTARY. */
    const uint16_t terminators[] = {QK_MOMENTARY_MAX + 1, QK_BOOT, QK_USER, KC_AUDIO_MUTE};
    for (unsigned i = 0; i < sizeof(terminators) / sizeof(terminators[0]); ++i) {
        caps_word_on();
        assert(key(terminators[i], true) && !is_caps_word_on() && !weak_mods);
    }
    caps_word_on(); mods = MOD_BIT(KC_LCTL);
    assert(key(KC_A, true) && !is_caps_word_on());
    caps_word_on(); mods = MOD_BIT(KC_RALT);
    assert(key(KC_A, true) && is_caps_word_on());
    assert(key(KC_RALT, true) && is_caps_word_on());
    assert(!key(QK_CAPS_WORD_TOGGLE, true) && !is_caps_word_on() && !weak_mods);

    now = UINT16_MAX - 20;
    caps_word_on();
    now += CAPS_WORD_IDLE_TIMEOUT - 1; caps_word_task();
    assert(is_caps_word_on());
    now += 1; caps_word_task();
    assert(!is_caps_word_on());
    caps_word_on();
    now += CAPS_WORD_IDLE_TIMEOUT - 1;
    assert(key(KC_A, true)); /* Activity restarts the 5-second idle deadline. */
    now += CAPS_WORD_IDLE_TIMEOUT - 1; caps_word_task();
    assert(is_caps_word_on());
    now += 1; caps_word_task();
    assert(!is_caps_word_on() && !weak_mods && reports > 0);
    puts("PASS: production Caps Word state/handler: toggle press/release, alphabet/numbers/editing, layer bounds, Ctrl/AltGr, timeout/reset/16-bit wrap and weak-mod cleanup.");
    return 0;
}
