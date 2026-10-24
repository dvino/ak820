# SPDX-License-Identifier: GPL-2.0-or-later
AK820_BOARD = yes
CUSTOM_MATRIX = yes
SRC += ak820_oneshot.c ak820_combo.c ak820_tapping.c ak820_board.c ak820_indicators.c matrix.c ak820_nvm.c ak820_flash.c ak820_timer.c ak820_boot.c ak820_macro.c ak820_startup.c
EEPROM_DRIVER = custom
ENCODER_ENABLE = yes
ENCODER_MAP_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = no
NKRO_ENABLE = yes
CONSOLE_ENABLE = no
COMMAND_ENABLE = no
MAGIC_ENABLE = no
CAPS_WORD_ENABLE = yes
REPEAT_KEY_ENABLE = yes
GRAVE_ESC_ENABLE = yes
TRI_LAYER_ENABLE = yes
SPACE_CADET_ENABLE = no
LEADER_ENABLE = no
DYNAMIC_MACRO_ENABLE = no
TAP_DANCE_ENABLE = no
COMBO_ENABLE = no
KEY_OVERRIDE_ENABLE = no
AUTO_SHIFT_ENABLE = no
QMK_SETTINGS = no
RGB_MATRIX_ENABLE = yes
RGB_MATRIX_DRIVER = custom
VIALRGB_ENABLE = yes

# Compact user controls are opt-in and do not enable the Magic engine.
AK820_NKRO_CONTROL ?= no
ifeq ($(AK820_NKRO_CONTROL),yes)
    OPT_DEFS += -DAK820_NKRO_CONTROL
endif

AK820_COMPACT_ONESHOT ?= no
ifeq ($(AK820_COMPACT_ONESHOT),yes)
    OPT_DEFS += -DAK820_COMPACT_ONESHOT
endif
