#include "sdcc_dummy_macros.h"
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* Use the bounded application window below the interrupt-vector table. */
#    pragma codeseg AK820LOW
#endif
// Copyright 2021-2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <stdint.h>
#include "caps_word.h"
#include "timer.h"
#include "action.h"
#include "action_util.h"
#include "quantum_keycodes.h"
#include "modifiers.h"

/** @brief True when Caps Word is active. */
static bool caps_word_active = false;

#if CAPS_WORD_IDLE_TIMEOUT > 0
// Constrain timeout to a sensible range. With 16-bit timers, the longest
// timeout possible is 32768 ms, rounded here to 30000 ms = half a minute.
#    if CAPS_WORD_IDLE_TIMEOUT < 100 || CAPS_WORD_IDLE_TIMEOUT > 30000
#        error "CAPS_WORD_IDLE_TIMEOUT must be between 100 and 30000 ms"
#    endif

/** @brief Deadline for idle timeout. */
static uint16_t idle_timer = 0;

void caps_word_task(void) {
    if (caps_word_active && timer_expired(timer_read(), idle_timer)) {
        caps_word_off();
    }
}

void caps_word_reset_idle_timer(void) {
    idle_timer = timer_read() + CAPS_WORD_IDLE_TIMEOUT;
}
#else
void caps_word_task(void) {}
#endif // CAPS_WORD_IDLE_TIMEOUT > 0

void caps_word_on(void) {
    if (caps_word_active) {
        return;
    }

    clear_mods();
#ifndef NO_ACTION_ONESHOT
    clear_oneshot_mods();
#endif // NO_ACTION_ONESHOT
#if CAPS_WORD_IDLE_TIMEOUT > 0
    caps_word_reset_idle_timer();
#endif // CAPS_WORD_IDLE_TIMEOUT > 0

    caps_word_active = true;
    caps_word_set_user(true);
}

void caps_word_off(void) {
    if (!caps_word_active) {
        return;
    }

#ifdef AK820_COMPACT_TAPPING
    /* Caps Word adds temporary raw Shift. Its cleanup must not consume an
     * encoded action, Repeat or macro primitive's owned weak contribution. */
    del_weak_mods(MOD_MASK_SHIFT);
    send_keyboard_report();
#else
    unregister_weak_mods(MOD_MASK_SHIFT);
#endif
    caps_word_active = false;
    caps_word_set_user(false);
}

void caps_word_toggle(void) {
    if (caps_word_active) {
        caps_word_off();
    } else {
        caps_word_on();
    }
}

bool is_caps_word_on(void) {
    return caps_word_active;
}

__attribute__((weak)) void caps_word_set_user(bool active) {}

/* Keep the default callback with the Caps Word state machine. On AK820 this
 * small module fits in the independently bounded low application window. */
__attribute__((weak)) bool caps_word_press_user(uint16_t keycode) {
    if ((keycode >= KC_A && keycode <= KC_Z) || keycode == KC_MINS) {
        add_weak_mods(MOD_BIT(KC_LSFT));
        return true;
    }
    return (keycode >= KC_1 && keycode <= KC_0) || keycode == KC_BSPC ||
        keycode == KC_DEL || keycode == KC_UNDS;
}
