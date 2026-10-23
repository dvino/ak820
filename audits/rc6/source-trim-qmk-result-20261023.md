# QMK upstream source trim result

2026-10-23. The upstream QMK source under `qmk-8051-ak820/` was trimmed for
the supported `ajazz/ak820:vial` target. This records file movement and static
tree checks only. No build, test, USB access, firmware update, or release edit
was performed.

## Preserved backup

Moved content is recoverable under:

`C:\Users\vinok\Documents\Codex\AK820-private-backups\source-trim-qmk-20261023-20261023-172735`

The complete final backup inventory, with file sizes and SHA256 values, is:

`C:\Users\vinok\Documents\Codex\AK820-private-backups\source-trim-qmk-inventory-20261023-final.json`

The exact 1,171 moved roots are listed in:

`C:\Users\vinok\Documents\Codex\AK820-private-backups\source-trim-qmk-moved-roots-20261023-final.txt`

It lists 37,397 files totaling 117,779,833 bytes. The initial inventory covered
37,053 files before movement. I compared those hashes with the backup after
movement: there were no missing files or hash differences. While adding the
default-layout files to that inventory, the original manifest was overwritten.
I then generated the complete final inventory from the backup. The final
manifest therefore records the backed-up state; the original per-file
pre-move manifest is no longer available.

## Paths moved

- All 977 foreign board directories directly under `keyboards/`; only
  `keyboards/ajazz/ak820/` remains in the source tree.
- `users/`, `layouts/community/`, and all 86 community layout directories
  below `layouts/default/`. The tracked `layouts/default/readme.md` remains as
  the QMK CLI startup stub.
- `docs/` inside the QMK checkout.
- `platforms/arm_atsam/`, `platforms/test/`, and all AVR and ChibiOS platform
  content except each `mcu_selection.mk`.
- `lib/arm_atsam/`, `lib/fnv/`, `lib/lib8tion/`, `lib/printf/`, and
  `lib/usbhost/`.
- Every `drivers/` directory except `drivers/eeprom/`, plus all five direct
  files in `drivers/`.
- `tmk_core/protocol/arm_atsam/`, `chibios/`, `lufa/`, `usb_hid/`, and
  `vusb/`.
- All 15 non-AK820 test directories.
- `quantum/audio/`, `backlight/`, `encoder/`, `led_matrix/`, `midi/`,
  `os_detection/`, `painter/`, `pointing_device/`, `rgblight/`,
  `split_common/`, `unicode/`, and `wear_leveling/`.

## Retained exceptions checked

The following paths remain present: `keyboards/ajazz/ak820/`, all 23
`tests/ak820*/` directories, `layouts/default/readme.md`, `lib/lufa/`,
`lib/ch555/`, `lib/python/qmk/`, `data/`, `platforms/mcs51/`,
`platforms/avr/mcu_selection.mk`, `platforms/chibios/mcu_selection.mk`, and
both EEPROM driver source and header files. The target board is the only board
root left under `keyboards/`.

## Remaining validation

Run the QMK startup and generator commands, reproduce the saved SDCC 4.6 build
with a fresh output directory, compare the resulting IHX and binary, and run
the offline repository and AK820 host/CPU suites described in
`source-trim-dependencies-20261023.md`. No claim is made here that the trimmed
tree builds or that the installed firmware behaves differently. The owner is
handling a separate update of an existing immutable release; this cleanup did
not alter release files.
