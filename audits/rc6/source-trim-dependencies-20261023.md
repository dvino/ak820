# AK820 source dependencies

2026-10-23. Static inspection only. No build, device command or deletion was run
for this report. This is a removal plan for the single supported target
`ajazz/ak820:vial`, with the present feature flags and AK820 tests.

The saved SDCC 4.6 build has 465 input records and 76 artifact records. That list
is useful evidence, but is not a complete list of files needed by the installer,
tests or QMK command startup. Keep the files below before trying a fresh build.

## Keep

- `keyboards/ajazz/ak820/`, including the Vial keymap and definition.
- `builddefs/`, `paths.mk`, `Makefile`, `requirements*.txt`, `setup.cfg`.
- `lib/python/qmk/` and `data/`. QMK imports its listed commands at startup,
  including commands unrelated to this board. The build input collector also
  hashes every QMK Python module and every JSON/HJSON data file.
- `platforms/mcs51/` and the shared files directly inside `platforms/`.
- `platforms/avr/mcu_selection.mk` and
  `platforms/chibios/mcu_selection.mk` if the Make logic stays unchanged.
  `build_keyboard.mk` includes all `platforms/*/mcu_selection.mk`; both files
  are in the saved input list. Removing them changes provenance even if the
  resulting firmware remains identical.
- `lib/ch555/` and the required LUFA headers. The saved build reads twelve
  headers under `lib/lufa/LUFA/`, despite using the custom CH555 USB backend.
  Keep `lib/lufa/` initially, or keep the exact twelve input headers plus the
  LUFA license after checking host-test includes. Do not remove LUFA wholesale.
- `drivers/eeprom/eeprom_driver.c` and `eeprom_driver.h`.
- Shared `tmk_core/protocol/` files and `tmk_core/protocol/ch555/`.
- `quantum/` initially, or its compiler include closure plus test inputs.
  Headers for disabled functions can still be included by shared headers.
- All `tests/ak820*/`. Tests import helpers from other AK820 test directories;
  a directory absent from the default runner can still provide a helper.
- `util/ak820*.py`, `util/build_ak820.py`, `util/build_id.py`,
  `util/vial_generate_definition.py`, `util/pack_ak820.py`,
  `util/check_ak820*.py`, `util/prepare_ak820*.py`, and source provenance.
  Root installer and protocol tools import these directly.
- Existing license files and copyright notices belonging to retained code.

Keep a tracked file inside `layouts/default/`, for example a short README.
`qmk.cli.new.keyboard` calls `Path('layouts/default/').iterdir()` during import.
Removing that directory breaks ordinary generator commands before compilation.
The actual community layouts are not needed: this board has its own LAYOUT and
does not declare community layouts. This requirement can instead be removed by
changing the CLI import or directory check and testing startup separately.

## Safe subtree candidates for this target

These are outside the saved firmware input closure and the current AK820 host
test references. Validate the fresh build and tests after removal; this report
does not claim the trimmed tree has already passed.

- All `keyboards/` content except `ajazz/ak820/` and its ancestor directories.
  The consumed Make list contains no ancestor rules outside this board.
- `users/`; all actual layout definitions under `layouts/`, subject to keeping
  `layouts/default/` as described above.
- `docs/` inside the QMK tree; QMK Doxygen files and upstream example docs.
  This does not refer to this repository's current owner documentation.
- `platforms/arm_atsam/`, `platforms/test/`, and AVR/ChibiOS contents except
  the two MCU selection files described above.
- `lib/arm_atsam/`, `lib/fnv/`, `lib/lib8tion/`, `lib/printf/`, `lib/usbhost/`.
  AK820 uses its compact RGB implementation instead of lib8tion; printing is
  disabled. `print.mk` still adds printf paths, but no printf file appears in
  the compiled closure. Re-enabling printing would require restoring it.
- All `drivers/` subdirectories except `eeprom/`; direct driver files are also
  outside the closure. Keep the two EEPROM files listed above.
- `tmk_core/protocol/arm_atsam/`, `chibios/`, `lufa/`, `usb_hid/`, `vusb/`.
  The separate `lib/lufa/` exception still applies.
- All non-AK820 test directories: `audio`, `autocorrect`, `auto_shift`,
  `basic`, `caps_word`, `combo`, `leader`, `no_tapping`, `repeat_key`, `secure`,
  `tap_dance`, `tap_hold_configurations`, `test_common`, `tri_layer`, `unicode`.
  Current AK820 scripts do not reference their harnesses or `platforms/test`.
- Disabled feature directories under `quantum/`: `audio`, `backlight`,
  `encoder`, `led_matrix`, `midi`, `os_detection`, `painter`, `pointing_device`,
  `rgblight`, `split_common`, `unicode`, `wear_leveling`. None appears in the
  saved closure or AK820 script/source path references. `quantum/encoder.c`
  and `encoder.h` are required and are different from `quantum/encoder/`.
- Upstream editor settings, upstream CI, Docker/Nix/install helpers and unused
  bootloader HEX images. Keep AK820 scripts; ordinary upstream QMK maintenance
  commands are outside the supported workflow after this cut.

The root index has no mode-160000 entries. The QMK `.gitmodules` is inherited
metadata, while LUFA is ordinary tracked source. Remove declarations for absent
libraries rather than presenting them as required dependencies. No current
AK820 builder references `util/sdcc_MCS51_rm`; its old declaration belongs to
the upstream build path. Keep any notices for retained third-party code.

## Checks after trimming

First run QMK startup and generator commands from the QMK root with the pinned
virtual environment. At minimum check `qmk hello`, `qmk list-keyboards`,
`qmk generate-rules-mk -kb ajazz/ak820`, and `qmk generate-config-h -kb
ajazz/ak820`. The keyboard list should contain only the supported board.

Reproduce the SDCC 4.6 build with the saved experimental builder, not the
production builder's SDCC 4.4 version gate. From the QMK root in WSL:

```sh
PYTHONPATH=util .venv/bin/python .build/rc6-sdcc46-probe-20261023/build_ak820_experimental.py \
  --toolchain .build/rc6-sdcc46-probe-20261023/sdcc-4.6.0 \
  --qmk-bin .venv/bin/qmk --build-dir .build/source-trim-sdcc46-20261023
```

Use a fresh output directory. Preserve the original builder and compiler before
moving private build data. A relocated experimental builder needs its source
root expression adjusted explicitly; do not reuse it at an arbitrary path.
Check the resulting IHX SHA256 against
`f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
Compare binary bytes too. Compare the new source manifest and generated flags
after normalizing output paths; document intentionally removed selection files
or generator modules rather than hiding their provenance changes.

Run the repository runner offline, then its host/CPU options in WSL with the
new build selected. Also run retained AK820 suites not called by the default
runner when they cover changed dependencies. In particular preserve and check
USB, recovery, transport, startup, breathing, compiler, definition, IRQ and
emitted-code suites. Inspect each suite's arguments first; do not infer that
the default runner covers every directory.

No result here establishes installed-device behavior. No live update, reset,
bootloader command, USB write or firmware flash is part of this cleanup.
