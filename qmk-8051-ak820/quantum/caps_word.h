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

#pragma once

#include <stdbool.h>
#include <stdint.h>

#ifdef AK820_BOARD
#define AK820_CW_LANG_EN 0x7E00
#define AK820_CW_LANG_RU 0x7E01
#define AK820_CW_LANG_TOGGLE 0x7E02
/* Shared by the low-window state machine and main-window selector handler. */
#ifdef __SDCC_mcs51
extern __bit caps_word_ru;
#else
extern bool caps_word_ru;
#endif
void ak820_caps_word_configure(uint8_t ru);
void ak820_caps_word_select(uint16_t keycode);
#endif

#ifndef CAPS_WORD_IDLE_TIMEOUT
#    define CAPS_WORD_IDLE_TIMEOUT 5000 // Default timeout of 5 seconds.
#endif

#if defined(AK820_COMPACT_TAPPING) && defined(DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD)
void caps_word_shift_task(void);
void caps_word_shift_cancel(void);
#endif

/** @brief Matrix scan task for Caps Word feature */
void caps_word_task(void);

#if CAPS_WORD_IDLE_TIMEOUT > 0
/** @brief Resets timer for Caps Word idle timeout. */
void caps_word_reset_idle_timer(void);
#endif

/** @brief Activates Caps Word. */
void caps_word_on(void);

/** @brief Deactivates Caps Word. */
void caps_word_off(void);

/** @brief Toggles Caps Word. */
void caps_word_toggle(void);

/** @brief Gets whether currently active. */
bool is_caps_word_on(void);

/**
 * @brief Caps Word set callback.
 *
 * @param active True if Caps Word is active, false otherwise
 */
void caps_word_set_user(bool active);
