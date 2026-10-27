/* Copyright 2021
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "sdcc_dummy_macros.h"
#include "send_string.h"

#include <ctype.h>
#include <stdlib.h>

#include "quantum_keycodes.h"
#include "keycode.h"
#include "action.h"
#include "wait.h"

#if defined(AUDIO_ENABLE) && defined(SENDSTRING_BELL)
#    include "audio.h"
#    ifndef BELL_SOUND
#        define BELL_SOUND TERMINAL_SOUND
#    endif
float bell_song[][2] = SONG(BELL_SOUND);
#endif

// clang-format off

#if !defined(AK820_BOARD) || !defined(__SDCC_mcs51)
/* Bit-Packed look-up table to convert an ASCII character to whether
 * [Shift] needs to be sent with the keycode.
 */
__attribute__((weak)) const uint8_t ascii_to_shift_lut[16] PROGMEM = {
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),

    KCLUT_ENTRY(0, 1, 1, 1, 1, 1, 1, 0),
    KCLUT_ENTRY(1, 1, 1, 1, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 1, 0, 1, 0, 1, 1),
    KCLUT_ENTRY(1, 1, 1, 1, 1, 1, 1, 1),
    KCLUT_ENTRY(1, 1, 1, 1, 1, 1, 1, 1),
    KCLUT_ENTRY(1, 1, 1, 1, 1, 1, 1, 1),
    KCLUT_ENTRY(1, 1, 1, 0, 0, 0, 1, 1),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 1, 1, 1, 1, 0)
};

#endif

#if !defined(AK820_BOARD) || !defined(__SDCC_mcs51)
/* Bit-Packed look-up table to convert an ASCII character to whether
 * [AltGr] needs to be sent with the keycode.
 */
__attribute__((weak)) const uint8_t ascii_to_altgr_lut[16] PROGMEM = {
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),

    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0)
};

/* Bit-Packed look-up table to convert an ASCII character to whether
 * [Space] needs to be sent after the keycode
 */
__attribute__((weak)) const uint8_t ascii_to_dead_lut[16] PROGMEM = {
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),

    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0),
    KCLUT_ENTRY(0, 0, 0, 0, 0, 0, 0, 0)
};

#endif

/* Look-up table to convert an ASCII character to a keycode.
 */
#if defined(AK820_BOARD) && defined(__SDCC_mcs51)
/* The fixed AK820 map has no keycode above 0x7f; bit 7 carries Shift. */
__attribute__((weak)) const uint8_t ascii_to_keycode_lut[128] PROGMEM = {
    XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    KC_BSPC, KC_TAB, KC_ENT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    XXXXXXX, XXXXXXX, XXXXXXX, KC_ESC, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    KC_SPC, (KC_1 | 0x80), (KC_QUOT | 0x80), (KC_3 | 0x80), (KC_4 | 0x80), (KC_5 | 0x80), (KC_7 | 0x80), KC_QUOT,
    (KC_9 | 0x80), (KC_0 | 0x80), (KC_8 | 0x80), (KC_EQL | 0x80), KC_COMM, KC_MINS, KC_DOT, KC_SLSH,
    KC_0, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7,
    KC_8, KC_9, (KC_SCLN | 0x80), KC_SCLN, (KC_COMM | 0x80), KC_EQL, (KC_DOT | 0x80), (KC_SLSH | 0x80),
    (KC_2 | 0x80), (KC_A | 0x80), (KC_B | 0x80), (KC_C | 0x80), (KC_D | 0x80), (KC_E | 0x80), (KC_F | 0x80), (KC_G | 0x80),
    (KC_H | 0x80), (KC_I | 0x80), (KC_J | 0x80), (KC_K | 0x80), (KC_L | 0x80), (KC_M | 0x80), (KC_N | 0x80), (KC_O | 0x80),
    (KC_P | 0x80), (KC_Q | 0x80), (KC_R | 0x80), (KC_S | 0x80), (KC_T | 0x80), (KC_U | 0x80), (KC_V | 0x80), (KC_W | 0x80),
    (KC_X | 0x80), (KC_Y | 0x80), (KC_Z | 0x80), KC_LBRC, KC_BSLS, KC_RBRC, (KC_6 | 0x80), (KC_MINS | 0x80),
    KC_GRV, KC_A, KC_B, KC_C, KC_D, KC_E, KC_F, KC_G,
    KC_H, KC_I, KC_J, KC_K, KC_L, KC_M, KC_N, KC_O,
    KC_P, KC_Q, KC_R, KC_S, KC_T, KC_U, KC_V, KC_W,
    KC_X, KC_Y, KC_Z, (KC_LBRC | 0x80), (KC_BSLS | 0x80), (KC_RBRC | 0x80), (KC_GRV | 0x80), KC_DEL,
};
#else
__attribute__((weak)) const uint8_t ascii_to_keycode_lut[128] PROGMEM = {
    // NUL   SOH      STX      ETX      EOT      ENQ      ACK      BEL
    XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    // BS    TAB      LF       VT       FF       CR       SO       SI
    KC_BSPC, KC_TAB,  KC_ENT,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    // DLE   DC1      DC2      DC3      DC4      NAK      SYN      ETB
    XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    // CAN   EM       SUB      ESC      FS       GS       RS       US
    XXXXXXX, XXXXXXX, XXXXXXX, KC_ESC,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,

    //       !        "        #        $        %        &        '
    KC_SPC,  KC_1,    KC_QUOT, KC_3,    KC_4,    KC_5,    KC_7,    KC_QUOT,
    // (     )        *        +        ,        -        .        /
    KC_9,    KC_0,    KC_8,    KC_EQL,  KC_COMM, KC_MINS, KC_DOT,  KC_SLSH,
    // 0     1        2        3        4        5        6        7
    KC_0,    KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,    KC_7,
    // 8     9        :        ;        <        =        >        ?
    KC_8,    KC_9,    KC_SCLN, KC_SCLN, KC_COMM, KC_EQL,  KC_DOT,  KC_SLSH,
    // @     A        B        C        D        E        F        G
    KC_2,    KC_A,    KC_B,    KC_C,    KC_D,    KC_E,    KC_F,    KC_G,
    // H     I        J        K        L        M        N        O
    KC_H,    KC_I,    KC_J,    KC_K,    KC_L,    KC_M,    KC_N,    KC_O,
    // P     Q        R        S        T        U        V        W
    KC_P,    KC_Q,    KC_R,    KC_S,    KC_T,    KC_U,    KC_V,    KC_W,
    // X     Y        Z        [        \        ]        ^        _
    KC_X,    KC_Y,    KC_Z,    KC_LBRC, KC_BSLS, KC_RBRC, KC_6,    KC_MINS,
    // `     a        b        c        d        e        f        g
    KC_GRV,  KC_A,    KC_B,    KC_C,    KC_D,    KC_E,    KC_F,    KC_G,
    // h     i        j        k        l        m        n        o
    KC_H,    KC_I,    KC_J,    KC_K,    KC_L,    KC_M,    KC_N,    KC_O,
    // p     q        r        s        t        u        v        w
    KC_P,    KC_Q,    KC_R,    KC_S,    KC_T,    KC_U,    KC_V,    KC_W,
    // x     y        z        {        |        }        ~        DEL
    KC_X,    KC_Y,    KC_Z,    KC_LBRC, KC_BSLS, KC_RBRC, KC_GRV,  KC_DEL
};
#endif

// clang-format on

#if defined(AK820_BOARD) && !defined(__SDCC_mcs51)
// One-bit masks avoid three variable-count shift loops in send_char.
static const uint8_t ascii_bit_mask_lut[8] PROGMEM = {1, 2, 4, 8, 16, 32, 64, 128};
#endif

// Note: we bit-pack in "reverse" order to optimize loading
#ifdef AK820_BOARD
/* AK820's macro parser rejects non-ASCII; current pos expressions are uint8_t. */
#    define PGM_LOADBIT(mem, pos) ((pgm_read_byte(&((mem)[((uint8_t)(pos)) >> 3])) >> ((pos) & 7)) & 0x01)
#else
#    define PGM_LOADBIT(mem, pos) ((pgm_read_byte(&((mem)[(pos) / 8])) >> ((pos) % 8)) & 0x01)
#endif

void send_string(const char *string) {
    send_string_with_delay(string, 0);
}

void send_string_with_delay(const char *string, uint8_t interval) {
    while (1) {
        char ascii_code = *string;
        if (!ascii_code) break;
        if (ascii_code == SS_QMK_PREFIX) {
            ascii_code = *(++string);
            if (ascii_code == SS_TAP_CODE) {
                // tap
                uint8_t keycode = *(++string);
                tap_code(keycode);
            } else if (ascii_code == SS_DOWN_CODE) {
                // down
                uint8_t keycode = *(++string);
                register_code(keycode);
            } else if (ascii_code == SS_UP_CODE) {
                // up
                uint8_t keycode = *(++string);
                unregister_code(keycode);
            } else if (ascii_code == SS_DELAY_CODE) {
                // delay
                int     ms      = 0;
                uint8_t keycode = *(++string);
                while (isdigit(keycode)) {
                    ms *= 10;
                    ms += keycode - '0';
                    keycode = *(++string);
                }
                while (ms--)
                    wait_ms(1);
            }
        } else {
            send_char(ascii_code);
        }
        ++string;
        // interval
        {
            uint8_t ms = interval;
            while (ms--)
                wait_ms(1);
        }
    }
}

void send_char(char ascii_code) {
#if defined(AUDIO_ENABLE) && defined(SENDSTRING_BELL)
    if (ascii_code == '\a') { // BEL
        PLAY_SONG(bell_song);
        return;
    }
#endif

#ifdef AK820_BOARD
    uint8_t ascii_index = (uint8_t)ascii_code;
#    if defined(__SDCC_mcs51)
    uint8_t encoded_keycode = pgm_read_byte(&ascii_to_keycode_lut[ascii_index]);
    uint8_t keycode         = encoded_keycode & 0x7F;
    bool    is_shifted      = (encoded_keycode & 0x80) != 0;
    bool    is_altgred      = false;
    bool    is_dead         = false;
#    else
    uint8_t bit_mask    = pgm_read_byte(&ascii_bit_mask_lut[ascii_index & 7]);
    uint8_t bit_index   = ascii_index >> 3;
    uint8_t keycode     = pgm_read_byte(&ascii_to_keycode_lut[ascii_index]);
    bool    is_shifted  = (pgm_read_byte(&ascii_to_shift_lut[bit_index]) & bit_mask) != 0;
    bool    is_altgred  = (pgm_read_byte(&ascii_to_altgr_lut[bit_index]) & bit_mask) != 0;
    bool    is_dead     = (pgm_read_byte(&ascii_to_dead_lut[bit_index]) & bit_mask) != 0;
#    endif
#else
    uint8_t keycode    = pgm_read_byte(&ascii_to_keycode_lut[(uint8_t)ascii_code]);
    bool    is_shifted = PGM_LOADBIT(ascii_to_shift_lut, (uint8_t)ascii_code);
    bool    is_altgred = PGM_LOADBIT(ascii_to_altgr_lut, (uint8_t)ascii_code);
    bool    is_dead    = PGM_LOADBIT(ascii_to_dead_lut, (uint8_t)ascii_code);
#endif

    if (is_shifted) {
        register_code(KC_LEFT_SHIFT);
    }
    if (is_altgred) {
        register_code(KC_RIGHT_ALT);
    }
    tap_code(keycode);
    if (is_altgred) {
        unregister_code(KC_RIGHT_ALT);
    }
    if (is_shifted) {
        unregister_code(KC_LEFT_SHIFT);
    }
    if (is_dead) {
        tap_code(KC_SPACE);
    }
}

void send_dword(uint32_t number) {
    send_word(number >> 16);
    send_word(number & 0xFFFFUL);
}

void send_word(uint16_t number) {
    send_byte(number >> 8);
    send_byte(number & 0xFF);
}

void send_byte(uint8_t number) {
    send_nibble(number >> 4);
    send_nibble(number & 0xF);
}

void send_nibble(uint8_t number) {
    //switch (number & 0xF) {
    //    case 0 ... 9:
    //        send_char(number + '0');
    //        break;
    //    case 10 ... 15:
    //        send_char(number - 10 + 'a');
    //        break;
    //}
    uint8_t number_4b = number & 0xf;
    if (number_4b < 10)
            send_char(number + '0');
    else if (number_4b >= 10 && number_4b <= 15)
            send_char(number - 10 + 'a');
}

void tap_random_base64(void) {
#if defined(__AVR_ATmega32U4__)
    uint8_t key = (TCNT0 + TCNT1 + TCNT3 + TCNT4) % 64;
#else
    uint8_t key = rand() % 64;
#endif
    //switch (key) {
        //if (key >= 0 && key <= 25)
        if      (key <= 25) // the >= 0 check seems stupid
            send_char(key + 'A');
        else if (key >= 26 && key <= 51)
            send_char(key - 26 + 'a');
        else if (key == 52)
            send_char('0');
        else if (key >= 53 && key <= 61)
            send_char(key - 53 + '1');
        else if (key == 62)
            send_char('+');
        else if (key == 63)
            send_char('/');
    //}
}

#if defined(__AVR__)
void send_string_P(const char *string) {
    send_string_with_delay_P(string, 0);
}

void send_string_with_delay_P(const char *string, uint8_t interval) {
    while (1) {
        char ascii_code = pgm_read_byte(string);
        if (!ascii_code) break;
        if (ascii_code == SS_QMK_PREFIX) {
            ascii_code = pgm_read_byte(++string);
            if (ascii_code == SS_TAP_CODE) {
                // tap
                uint8_t keycode = pgm_read_byte(++string);
                tap_code(keycode);
            } else if (ascii_code == SS_DOWN_CODE) {
                // down
                uint8_t keycode = pgm_read_byte(++string);
                register_code(keycode);
            } else if (ascii_code == SS_UP_CODE) {
                // up
                uint8_t keycode = pgm_read_byte(++string);
                unregister_code(keycode);
            } else if (ascii_code == SS_DELAY_CODE) {
                // delay
                int     ms      = 0;
                uint8_t keycode = pgm_read_byte(++string);
                while (isdigit(keycode)) {
                    ms *= 10;
                    ms += keycode - '0';
                    keycode = pgm_read_byte(++string);
                }
                while (ms--)
                    wait_ms(1);
            }
        } else {
            send_char(ascii_code);
        }
        ++string;
        // interval
        {
            uint8_t ms = interval;
            while (ms--)
                wait_ms(1);
        }
    }
}
#endif
