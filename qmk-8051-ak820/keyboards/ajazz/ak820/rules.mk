# SPDX-License-Identifier: GPL-2.0-or-later
AK820_BOARD = yes
CUSTOM_MATRIX = yes
SRC += ak820_oneshot.c ak820_combo.c ak820_tapping.c ak820_board.c ak820_indicators.c matrix.c ak820_crc.c ak820_nvm.c ak820_flash.c ak820_timer.c ak820_boot.c ak820_macro.c ak820_startup.c
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
AK820_COMPACT_AUTOSHIFT ?= no
ifeq ($(AK820_COMPACT_AUTOSHIFT),yes)
    OPT_DEFS += -DAK820_COMPACT_AUTOSHIFT
    SRC += ak820_autoshift.c
endif
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

AK820_COMPACT_SPACE_CADET ?= no
ifeq ($(AK820_COMPACT_SPACE_CADET),yes)
    OPT_DEFS += -DAK820_COMPACT_SPACE_CADET
endif

# Fixed-speed Mouse Keys use the existing HID mouse report and endpoint.
AK820_COMPACT_MOUSEKEY ?= no
ifeq ($(AK820_COMPACT_MOUSEKEY),yes)
    MOUSEKEY_ENABLE = yes
    OPT_DEFS += -DAK820_COMPACT_MOUSEKEY
endif

AK820_COMPACT_DYNAMIC_MACRO ?= no
ifeq ($(AK820_COMPACT_DYNAMIC_MACRO),yes)
    OPT_DEFS += -DAK820_COMPACT_DYNAMIC_MACRO
    SRC += ak820_dynamic_macro.c
endif

# Volatile GUI output controls; no Magic swaps or EEPROM changes.
AK820_COMPACT_GUI_LOCK ?= no
ifeq ($(AK820_COMPACT_GUI_LOCK),yes)
    OPT_DEFS += -DAK820_COMPACT_GUI_LOCK
endif

# Volatile Ctrl/GUI report swap; independent of upstream persistent Magic.
AK820_COMPACT_CTRL_GUI_SWAP ?= no
ifeq ($(AK820_COMPACT_CTRL_GUI_SWAP),yes)
    OPT_DEFS += -DAK820_COMPACT_CTRL_GUI_SWAP
endif

AK820_COMPACT_LEADER ?= no
ifeq ($(AK820_COMPACT_LEADER),yes)
    OPT_DEFS += -DAK820_COMPACT_LEADER
    SRC += ak820_leader.c
endif

# Temporary host layout indication on the separate OS channel.
AK820_OS_INDICATORS ?= no
ifeq ($(AK820_OS_INDICATORS),yes)
    OPT_DEFS += -DAK820_OS_INDICATORS
    SRC += ak820_os_indicators.c
endif

# Session-only Mac/PC modifier mode; the OS indicator follows this mode.
AK820_MAC_PC ?= no
ifeq ($(AK820_MAC_PC),yes)
    OPT_DEFS += -DAK820_MAC_PC
endif

# Schema-3 typed modules preserve all legacy keymap/Combo/macro addresses.
AK820_COMPACT_TAP_DANCE ?= no
ifeq ($(AK820_COMPACT_TAP_DANCE),yes)
    OPT_DEFS += -DAK820_COMPACT_TAP_DANCE
    SRC += ak820_tap_dance.c
endif
AK820_COMPACT_KEY_OVERRIDE ?= no
ifeq ($(AK820_COMPACT_KEY_OVERRIDE),yes)
    OPT_DEFS += -DAK820_COMPACT_KEY_OVERRIDE
    SRC += ak820_key_override.c
endif
AK820_QMK_SETTINGS ?= no
ifeq ($(AK820_QMK_SETTINGS),yes)
    OPT_DEFS += -DAK820_QMK_SETTINGS
    SRC += ak820_settings.c
endif

# Fixed-layout word access; keep the existing C implementation as the control.
AK820_KEYMAP_WORDS_ASM ?= no
ifeq ($(AK820_KEYMAP_WORDS_ASM),yes)
    OPT_DEFS += -DAK820_KEYMAP_WORDS_ASM
    SRC += ak820_keymap_words.c
endif

# Diagnostic read kernel: explicit opt-in, separate translation unit.
AK820_NVM_READ_BLOCK_ASM ?= no
ifeq ($(AK820_NVM_READ_BLOCK_ASM),yes)
    OPT_DEFS += -DAK820_NVM_READ_BLOCK_ASM
    SRC += ak820_nvm_read_block.c
else ifneq ($(AK820_NVM_READ_BLOCK_ASM),no)
    $(error AK820_NVM_READ_BLOCK_ASM must be yes or no)
endif

AK820_NVM_UPDATE_BLOCK_ASM ?= no
ifeq ($(AK820_NVM_UPDATE_BLOCK_ASM),yes)
    OPT_DEFS += -DAK820_NVM_UPDATE_BLOCK_ASM
    SRC += ak820_nvm_update_block.c
else ifneq ($(AK820_NVM_UPDATE_BLOCK_ASM),no)
    $(error AK820_NVM_UPDATE_BLOCK_ASM must be yes or no)
endif
