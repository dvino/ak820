// SPDX-License-Identifier: GPL-2.0-or-later
// Unchanged behavior from dvino/ak820 38ad013, renamed for differential tests.
bool reference_process_rgb(const uint16_t keycode, const keyrecord_t *record) {
    // need to trigger on key-up for edge-case issue
#ifndef RGB_TRIGGER_ON_KEYDOWN
    if (!record->event.pressed) {
#else
    if (record->event.pressed) {
#endif
#if (defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)) || (defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES))
        uint8_t shifted = get_mods() & MOD_MASK_SHIFT;
#endif
#if defined(AK820_BOARD) && defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES) && !defined(RGBLIGHT_ENABLE)
        if (keycode >= RGB_MODE_FORWARD && keycode <= RGB_SPD) {
            uint8_t action = (uint8_t)(keycode - RGB_MODE_FORWARD);
            if (shifted) action ^= 1;
            reference_rgb_actions[action]();
            return false;
        }
#endif
        switch (keycode) {
            case RGB_TOG:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                rgblight_toggle();
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                rgb_matrix_toggle();
#endif
                return false;
#if !(defined(AK820_BOARD) && defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES) && !defined(RGBLIGHT_ENABLE))
            case RGB_MODE_FORWARD:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_step, rgblight_step_reverse);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_step, rgb_matrix_step_reverse);
#endif
                return false;
            case RGB_MODE_REVERSE:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_step_reverse, rgblight_step);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_step_reverse, rgb_matrix_step);
#endif
                return false;
            case RGB_HUI:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_increase_hue, rgblight_decrease_hue);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_increase_hue, rgb_matrix_decrease_hue);
#endif
                return false;
            case RGB_HUD:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_decrease_hue, rgblight_increase_hue);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_decrease_hue, rgb_matrix_increase_hue);
#endif
                return false;
            case RGB_SAI:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_increase_sat, rgblight_decrease_sat);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_increase_sat, rgb_matrix_decrease_sat);
#endif
                return false;
            case RGB_SAD:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_decrease_sat, rgblight_increase_sat);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_decrease_sat, rgb_matrix_increase_sat);
#endif
                return false;
            case RGB_VAI:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_increase_val, rgblight_decrease_val);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_increase_val, rgb_matrix_decrease_val);
#endif
                return false;
            case RGB_VAD:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_decrease_val, rgblight_increase_val);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_decrease_val, rgb_matrix_increase_val);
#endif
                return false;
            case RGB_SPI:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_increase_speed, rgblight_decrease_speed);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_increase_speed, rgb_matrix_decrease_speed);
#endif
                return false;
            case RGB_SPD:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgblight_decrease_speed, rgblight_increase_speed);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                handleKeycodeRGB(shifted, rgb_matrix_decrease_speed, rgb_matrix_increase_speed);
#endif
                return false;
#endif
            case RGB_MODE_PLAIN:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES)
                rgblight_mode(RGBLIGHT_MODE_STATIC_LIGHT);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES)
                rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR);
#endif
                return false;
            case RGB_MODE_BREATHE:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_BREATHING)
                handleKeycodeRGBMode(RGBLIGHT_MODE_BREATHING, RGBLIGHT_MODE_BREATHING_end);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES) && defined(ENABLE_RGB_MATRIX_BREATHING)
                rgb_matrix_mode(RGB_MATRIX_BREATHING);
#endif
                return false;
            case RGB_MODE_RAINBOW:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_RAINBOW_MOOD)
                handleKeycodeRGBMode(RGBLIGHT_MODE_RAINBOW_MOOD, RGBLIGHT_MODE_RAINBOW_MOOD_end);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES) && defined(ENABLE_RGB_MATRIX_CYCLE_LEFT_RIGHT)
                rgb_matrix_mode(RGB_MATRIX_CYCLE_LEFT_RIGHT);
#endif
                return false;
            case RGB_MODE_SWIRL:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_RAINBOW_SWIRL)
                handleKeycodeRGBMode(RGBLIGHT_MODE_RAINBOW_SWIRL, RGBLIGHT_MODE_RAINBOW_SWIRL_end);
#endif
#if defined(RGB_MATRIX_ENABLE) && !defined(RGB_MATRIX_DISABLE_KEYCODES) && defined(ENABLE_RGB_MATRIX_CYCLE_PINWHEEL)
                rgb_matrix_mode(RGB_MATRIX_CYCLE_PINWHEEL);
#endif
                return false;
            case RGB_MODE_SNAKE:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_SNAKE)
                handleKeycodeRGBMode(RGBLIGHT_MODE_SNAKE, RGBLIGHT_MODE_SNAKE_end);
#endif
                return false;
            case RGB_MODE_KNIGHT:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_KNIGHT)
                handleKeycodeRGBMode(RGBLIGHT_MODE_KNIGHT, RGBLIGHT_MODE_KNIGHT_end);
#endif
                return false;
            case RGB_MODE_XMAS:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_CHRISTMAS)
                rgblight_mode(RGBLIGHT_MODE_CHRISTMAS);
#endif
                return false;
            case RGB_MODE_GRADIENT:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_STATIC_GRADIENT)
                handleKeycodeRGBMode(RGBLIGHT_MODE_STATIC_GRADIENT, RGBLIGHT_MODE_STATIC_GRADIENT_end);
#endif
                return false;
            case RGB_MODE_RGBTEST:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_RGB_TEST)
                rgblight_mode(RGBLIGHT_MODE_RGB_TEST);
#endif
                return false;
            case RGB_MODE_TWINKLE:
#if defined(RGBLIGHT_ENABLE) && !defined(RGBLIGHT_DISABLE_KEYCODES) && defined(RGBLIGHT_EFFECT_TWINKLE)
                handleKeycodeRGBMode(RGBLIGHT_MODE_TWINKLE, RGBLIGHT_MODE_TWINKLE_end);
#endif
                return false;
        }
    }

    return true;
}
