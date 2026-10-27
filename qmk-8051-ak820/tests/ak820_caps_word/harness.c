/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdio.h>
#ifdef TEST_ACTION_TAPPING
#    undef NO_ACTION_TAPPING
#endif
#include "action.h"
#include "caps_word.h"
#include "quantum_keycodes.h"

/* The keyboard uses QMK's default generic tapping term in this host fixture. */
#ifndef GET_TAPPING_TERM
#    define GET_TAPPING_TERM(keycode, record) 200
#endif

static uint16_t now;
static uint8_t mods, owned_mods, weak_mods;
static unsigned reports;
static int8_t repeat_count;
bool ak820_macro_primitive;
uint16_t timer_read(void) { return now; }
uint8_t get_mods(void) { return mods | owned_mods; }
int8_t get_repeat_key_count(void) { return repeat_count; }
void clear_mods(void) { mods = 0; }
void clear_weak_mods(void) { weak_mods = 0; }
void add_weak_mods(uint8_t value) { weak_mods |= value; }
void del_weak_mods(uint8_t value) { weak_mods &= ~value; }
void unregister_weak_mods(uint8_t value) { del_weak_mods(value); ++reports; }
void send_keyboard_report(void) { ++reports; }
bool caps_word_press_user(uint16_t keycode);
void caps_word_shift_task(void);

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

static bool physical_event(uint16_t keycode, bool pressed, uint16_t time, uint8_t row, uint8_t col) {
    keyrecord_t record = {0};
    now = time;
    record.event.pressed = pressed;
    record.event.time = time;
    record.event.key.row = row;
    record.event.key.col = col;
    return process_caps_word(keycode, &record);
}

static void cancel_shift_candidate(void) {
    physical_event(KC_A, true, now, 0, 0);
    caps_word_off(); clear_weak_mods(); mods = 0;
}

static void shift_activation(void) {
    /* Physical left+right Shift activates on the second press, while the
     * existing real Shift owner remains intact after Caps Word cleanup. */
    caps_word_off(); clear_weak_mods(); mods = 0;
    physical_event(KC_LSFT, false, 1, 1, 0);
    physical_event(KC_RSFT, false, 2, 1, 1);
    assert(physical_event(KC_LSFT, true, 9, 1, 0));
    owned_mods = MOD_BIT(KC_LSFT);
    assert(physical_event(KC_RSFT, true, 10, 1, 1));
    assert(is_caps_word_on() && get_mods() == MOD_BIT(KC_LSFT));
    owned_mods = MOD_MASK_SHIFT;
    assert(key(KC_A, true) && weak_mods == MOD_BIT(KC_LSFT));
    assert(key(KC_A, false) && is_caps_word_on());
    caps_word_off(); assert(get_mods() == MOD_MASK_SHIFT);
    physical_event(KC_RSFT, false, 12, 1, 1); owned_mods = MOD_BIT(KC_LSFT);
    physical_event(KC_LSFT, false, 13, 1, 0); owned_mods = 0;

    /* Extra real modifiers reject both-shift activation. */
    caps_word_off(); mods = MOD_BIT(KC_LSFT) | MOD_BIT(KC_LCTL);
    physical_event(KC_RSFT, true, 20, 1, 1);
    assert(!is_caps_word_on());
    mods = 0;

    /* A held real opposite Shift contributes to QMK's modifier mask. A macro
     * generated press itself cannot arm or complete the double tap. */
    owned_mods = MOD_BIT(KC_RSFT);
    physical_event(KC_LSFT, true, 30, 1, 2);
    assert(is_caps_word_on()); caps_word_off();
    physical_event(KC_LSFT, false, 31, 1, 2); owned_mods = 0;
    ak820_macro_primitive = true;
    physical_event(KC_LSFT, true, 40, 1, 2);
    ak820_macro_primitive = false;
    physical_event(KC_LSFT, false, 41, 1, 2);
    physical_event(KC_LSFT, true, 42, 1, 2);
    assert(!is_caps_word_on());
    physical_event(KC_LSFT, false, 43, 1, 2); cancel_shift_candidate();

    /* Ordinary Shift remains an ordinary held modifier when no gesture
     * completes. Double-left activation requires press, release, press. */
    assert(physical_event(KC_LSFT, true, 100, 1, 2));
    assert(!is_caps_word_on());
    mods = MOD_BIT(KC_LSFT);
    assert(physical_event(KC_LSFT, false, 110, 1, 2));
    mods = 0;
    assert(physical_event(KC_LSFT, true, 299, 1, 2));
    assert(is_caps_word_on());
    mods = MOD_BIT(KC_LSFT);
    caps_word_off(); assert(mods == MOD_BIT(KC_LSFT));
    mods = 0;

    /* First release is mandatory; 200ms is exclusive and wraps in uint16_t. */
    physical_event(KC_LSFT, true, 400, 1, 2);
    physical_event(KC_LSFT, true, 410, 1, 2);
    assert(!is_caps_word_on()); cancel_shift_candidate();
    physical_event(KC_LSFT, true, 500, 1, 2);
    physical_event(KC_LSFT, false, 510, 1, 2);
    physical_event(KC_LSFT, true, 700, 1, 2);
    assert(!is_caps_word_on());
    physical_event(KC_LSFT, false, 701, 1, 2);
    physical_event(KC_LSFT, true, 702, 1, 2);
    assert(is_caps_word_on()); caps_word_off();
    physical_event(KC_LSFT, false, 703, 1, 2);
    physical_event(KC_LSFT, true, 65500, 1, 2);
    physical_event(KC_LSFT, false, 65510, 1, 2);
    physical_event(KC_LSFT, true, 163, 1, 2);
    assert(is_caps_word_on()); caps_word_off();

    /* Other physical presses and generated/out-of-matrix events cannot
     * complete a pending gesture. A long idle expires the candidate. */
    physical_event(KC_LSFT, true, 1000, 1, 2);
    physical_event(KC_LSFT, false, 1010, 1, 2);
    physical_event(KC_B, true, 1011, 1, 3);
    physical_event(KC_LSFT, true, 1012, 1, 2);
    assert(!is_caps_word_on()); cancel_shift_candidate();
    physical_event(KC_LSFT, true, 2000, 1, 2);
    physical_event(KC_LSFT, false, 2010, 1, 2);
    physical_event(KC_LSFT, true, 2011, MATRIX_ROWS, 2);
    assert(!is_caps_word_on()); cancel_shift_candidate();
    physical_event(KC_LSFT, true, 2500, 1, 2);
    physical_event(KC_LSFT, false, 2510, 1, 2);
    repeat_count = 1;
    physical_event(KC_LSFT, true, 2511, 1, 2);
    repeat_count = 0;
    assert(!is_caps_word_on()); cancel_shift_candidate();
    physical_event(KC_LSFT, true, 3000, 1, 2);
    physical_event(KC_LSFT, false, 3010, 1, 2);
    now = 3200; caps_word_shift_task();
    now = 65500; caps_word_shift_task();
    now = 100; caps_word_shift_task();
    physical_event(KC_LSFT, true, 101, 1, 2);
    assert(!is_caps_word_on()); cancel_shift_candidate();
    puts("PASS: physical both-Shift and double-left-Shift Caps Word gestures, exact deadline, cancellation, held modifiers, and timer wrap/idle.");
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
    shift_activation();
#ifdef AK820_COMPACT_TAPPING
    /* Synthetic macro keycodes cannot change the active language selector. */
    ak820_caps_word_select(AK820_CW_LANG_EN);
    ak820_macro_primitive = true;
    key(AK820_CW_LANG_RU, true);
    assert(!caps_word_ru && !is_caps_word_on());
    ak820_macro_primitive = false;
#endif
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
