Русский перевод: [Проверки](ru/TESTING.md).

# Testing

Keep four kinds of evidence separate: source review, build/integrity checks,
host/CPU execution, and physical keyboard behavior. None substitutes for another.

## Offline checks

From the repository root:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools/installer -p 'test_*.py' -v
python -B -m unittest discover -s tools -p 'test_build_release_bundle.py' -v
python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_package -p 'test_*.py' -v
```

The combined runner records each command, exit code and log hash under
`host/runs/`; use `--host` on Linux/WSL and optionally `--build-dir` for linked
CPU suites. It sends no device commands and never runs a flash test.

Host C runners require GCC/Clang on Linux/WSL. From `qmk-8051-ak820/`, use
`python tests/ak820_usb/run.py`, `python tests/ak820_keymap/run.py`,
`python tests/ak820_caps_word/run.py` and `python tests/ak820_macro_guard/run.py`.
Use the current [status](STATUS.md) and machine reports for additional regressions.
Real SDCC checks need `AK820_SDCC_BIN` pointing at the pinned toolchain's `bin`.

The checked Windows apps are in `dist/AK820-sdcc46-breathing-20261023/`.
Build log: `host/runs/20261023-sdcc46-windows.json`. CLI help, offline verify,
update help and GUI self-test passed. The
[independent artifact review](../audits/rc6/physical-gui-artifact-review.md)
records the checks of all 26 bound files per app. These are packaging checks;
separate live results are in [status](STATUS.md). Earlier GUI folders and the
old portable ZIP are superseded.

Linked CPU runners accept the new build directory and pinned `s51`, for example:

```sh
python tests/ak820_features/run.py --build-dir .build/local-1 \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 --output-dir .build/local-1-features
python tests/ak820_irq/run.py --build-dir .build/local-1 \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --stock-rom /path/to/private-oem-references/stock-full.bin \
  --output-dir .build/local-1-irq --main-sample-bytes 80
```

The stock ROM argument must point to the owner's local OEM archive; release
reference images are no longer stored in this checkout. These fixtures are
used only by offline CPU tests and must not be added to release output.

CPU fixtures execute linked instructions with modeled peripheral operations.
They do not emulate VS11K28A USB/flash silicon or prove every stack path safe.
Use a new output directory and match the image hash before reusing a report.

## Automatic checks without physical input

The current test work needs no key presses, knob rotation, cable reconnect or
manual unlock. Start with the offline runner:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools -p 'test_ak820_device_tests.py' -v
python tools/ak820_device_tests.py
```

The last command prints a plan. It must not open HID or write a setting in its
default mode. The combined runner includes its offline regressions. With a
completed Linux build, `--host --build-dir qmk-8051-ak820/.build/local-1`
also runs host and linked CPU checks; those still send no device commands.
Add --iap-fault-profile guarded-erase for the candidate with erase readback.
The default legacy-iap profile is for the earlier image; selecting a profile
does not identify or validate the image by itself.

| Area | Automatic check | What it does not prove |
| --- | --- | --- |
| Keys and layers | Read all 83 physical matrix slots on all six layers; compare protocol values with saved bytes. Opt-in write tests change a representative key on each layer and restore it. | Physical switch wiring, scan timing or typing from every key |
| Encoder | Read both directions on six layers; opt-in tests change and restore each direction. One hardware encoder has 12 assignment slots in total. | Rotation signals, detents or encoder push input |
| Macros | Check 16 slots, the 8192-byte protocol view and saved length metadata. Macro writes are reported as SKIP; tests never start unlock or execute a macro. | Macro upload round trips and triggering a macro from a physical key |
| RGB | Read capabilities, 82 LED records and settings; opt-in tests change and restore RAM settings while proving saved bytes stay unchanged. | Durable RGB save (SKIP), LED appearance, color accuracy or reactive light from a real press |
| Input features | Existing host/CPU cases cover report handling, Caps Word, Repeat/Alt Repeat, Grave Escape, Tri Layer and macro processing where implemented. | Physical input and electrical USB behavior |
| Storage failures | Test missing ACK, getter-only changes, bad durable readback, changed neighboring bytes and failed restoration. | Every possible controller failure or power-loss timing |

Live protocol checks are intended for later post-flash runs. Setting writes
need explicit authorization and opt-in arguments; a read-only run does not
grant it. Before every write, the runner must require a healthy stable snapshot.
After a change it must verify the reply, getter, exact saved bytes and unchanged
neighbors before trying one restoration. On a timeout or mismatch it stops and
saves the evidence. It never resets, retries, starts a bootloader or restores
blindly. Reports must list failures and skipped checks rather than call all
functions tested.

For a future read-only run after flashing, use Python with `hidapi` installed
and the matching personal session. The release is checked against its approval
before HID is opened:

```sh
python tools/ak820_device_tests.py --run --release-dir releases/rc6 \
  --session /path/to/personal-session --output host/runs/post-flash-1
```

Use a new output directory. To include the reversible mapping and RGB RAM
checks, add **both** `--allow-settings-write --owner-authorized`, only after
authorization for those changes. The plan, individual PASS/FAIL/SKIP results,
snapshots and request trace stay in the private output folder. These commands
never flash the keyboard or ask for physical actions.

The installed RC6 failed its encoder write at `target_write` despite a successful
cold boot. Keep that case in the offline regressions. During this test work no
new live commands or firmware writes are being run on that faulted keyboard.

## Physical acceptance checklist

Only start after the owner confirms the flash and has alternate input ready.
Keep cable and power stable while writing. Preserve the personal recovery folder.

1. Verify progressing boot status and type ordinary text, modifiers and media keys.
2. Test every physical key, encoder press and both directions; check release of chords.
3. Remap keys/layers/encoder, save a macro and global lighting, then restart.
4. Disconnect power and reconnect twice. Confirm the permanent application starts
   and retained settings work; a trial must instead follow its documented loader path.
5. Check reactive LEDs: idle black, correct key, chords, re-hit, fade, brightness
   and mode switches. Inspect actual appearance; a numerical model cannot do this.
6. Test Vial unlock/lock and Bootloader recovery using the personal session.

Record the exact image SHA256, device variant, OS, steps and results. A failed
step is a failure even when the loader checksum or another test passed.
