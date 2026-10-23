// Copyright 2026 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

/*******************************************************************************
  88888888888 888      d8b                .d888 d8b 888               d8b
      888     888      Y8P               d88P"  Y8P 888               Y8P
      888     888                        888        888
      888     88888b.  888 .d8888b       888888 888 888  .d88b.       888 .d8888b
      888     888 "88b 888 88K           888    888 888 d8P  Y8b      888 88K
      888     888  888 888 "Y8888b.      888    888 888 88888888      888 "Y8888b.
      888     888  888 888      X88      888    888 888 Y8b.          888      X88
      888     888  888 888  88888P'      888    888 888  "Y8888       888  88888P'
                                                        888                 888
                                                        888                 888
                                                        888                 888
     .d88b.   .d88b.  88888b.   .d88b.  888d888 8888b.  888888 .d88b.   .d88888
    d88P"88b d8P  Y8b 888 "88b d8P  Y8b 888P"      "88b 888   d8P  Y8b d88" 888
    888  888 88888888 888  888 88888888 888    .d888888 888   88888888 888  888
    Y88b 888 Y8b.     888  888 Y8b.     888    888  888 Y88b. Y8b.     Y88b 888
     "Y88888  "Y8888  888  888  "Y8888  888    "Y888888  "Y888 "Y8888   "Y88888
         888
    Y8b d88P
     "Y88P"
*******************************************************************************/

#pragma once

#ifndef BOOTMAGIC_LITE_COLUMN
#    define BOOTMAGIC_LITE_COLUMN 0
#endif // BOOTMAGIC_LITE_COLUMN

#ifndef BOOTMAGIC_LITE_ROW
#    define BOOTMAGIC_LITE_ROW 0
#endif // BOOTMAGIC_LITE_ROW

#ifndef DYNAMIC_KEYMAP_EEPROM_MAX_ADDR
#    define DYNAMIC_KEYMAP_EEPROM_MAX_ADDR 10239
#endif // DYNAMIC_KEYMAP_EEPROM_MAX_ADDR

#ifndef DYNAMIC_KEYMAP_LAYER_COUNT
#    define DYNAMIC_KEYMAP_LAYER_COUNT 6
#endif // DYNAMIC_KEYMAP_LAYER_COUNT

#ifndef DEBOUNCE
#    define DEBOUNCE 5
#endif // DEBOUNCE

#ifndef RGB_MATRIX_MAXIMUM_BRIGHTNESS
#    define RGB_MATRIX_MAXIMUM_BRIGHTNESS 160
#endif // RGB_MATRIX_MAXIMUM_BRIGHTNESS

#ifndef DEVICE_VER
#    define DEVICE_VER 0x0100
#endif // DEVICE_VER

#ifndef MANUFACTURER
#    define MANUFACTURER "AJAZZ"
#endif // MANUFACTURER

#ifndef PRODUCT
#    define PRODUCT "AK820 wired RGB (VS11K28A)"
#endif // PRODUCT

#ifndef PRODUCT_ID
#    define PRODUCT_ID 0x505B
#endif // PRODUCT_ID

#ifndef VENDOR_ID
#    define VENDOR_ID 0x320F
#endif // VENDOR_ID

#ifndef MATRIX_COLS
#    define MATRIX_COLS 8
#endif // MATRIX_COLS

#ifndef MATRIX_ROWS
#    define MATRIX_ROWS 16
#endif // MATRIX_ROWS

#ifndef ENCODERS_PAD_A
#    define ENCODERS_PAD_A { PORT7_1 }
#endif // ENCODERS_PAD_A

#ifndef ENCODERS_PAD_B
#    define ENCODERS_PAD_B { PORT7_0 }
#endif // ENCODERS_PAD_B

#ifndef ENCODER_RESOLUTION
#    define ENCODER_RESOLUTION 2
#endif // ENCODER_RESOLUTION
