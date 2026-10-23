Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

The source installer can save supported settings to a private local folder, restore them, or carry them through one supported firmware update. This is a host-only feature: it uses existing Vial commands and does not add a backup protocol to firmware.

## Supported firmware

Two exact SDCC 4.6 images are recognized:

- Legacy RC6 IHX: `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
- Pointer candidate IHX: `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`.

Same-image restores and the explicit legacy-to-candidate transition are
supported by host models. Downgrades and unknown images are rejected. Both
images use schema `0x082002`, the same Vial definition and protocol. Sharing a
schema alone never grants compatibility: the actual CODE hash and manifest
must match one of the exact reviewed image identities. The target snapshot
must match the selected target before physical unlock or setters.

The checked-in installer bundle still selects the legacy image. CI packages
select the freshly reproduced candidate under the [CI policy](CI.md).
The transition has not been performed on a keyboard. Unsupported firmware
or settings stop the operation before erase; arbitrary build migration is
not supported.

Every command takes `--session OEM_DIR`. This is required because the installer reconstructs the exact CODE image using the original native bytes from a valid OEM recovery session; those bytes are not shipped in the repository. Existing valid OEM recovery data may be used. The update image is regenerated from the approved bundle. A settings backup is not a substitute for the OEM recovery session.

## Commands

Run these through `AK820.sh` on Linux or `AK820.cmd` on Windows with the source installer:

```sh
./AK820.sh backup --session OEM_DIR --output NEW_DIR
./AK820.sh restore --session OEM_DIR --backup BACKUP_DIR
./AK820.sh update --session OEM_DIR --backup-dir NEW_DIR
```

Use the corresponding `AK820.cmd` commands on Windows. Quote paths containing spaces. `backup` only reads the keyboard. Its destination must be new; a completed backup is never overwritten. Keep the result private and local. It includes the full ROM, settings, saved NVM and read log, so do not publish or commit it.

`restore` validates the backup and target, saves a fresh target backup, then restores through supported Vial setters and verifies the values by reading them back. `update` validates the current source and settings, creates a new settings backup, flashes one exact image, then requests a fresh physical unlock and restores/verifies settings after restart. The installer asks for a second physical unlock after restart. An error, timeout or readback mismatch stops the workflow; there is no blind retry, rollback or reset.

The GUI provides matching backup, restore and update controls. For write operations, a modal asks for a fresh physical Esc + left Control hold for three seconds. The new paths do not ask for typed `yes`. Cancellation before erase stops the operation.

## What is saved

A checked backup stores 498 physical key assignments across six layers, 12 encoder assignments, all 16 macro slots with the published length preserved, layout options, saved RGB settings and exposed RGB RAM values. Macro data is sent in safe chunks; its published length and padding are preserved. A hash manifest records each file. The backup is written privately to a temporary directory, checked from disk and then published as a complete new directory.

The settings export is not a complete snapshot of every live firmware value. Direct RGB palette values cannot be read. Hidden current RGB mode and flags, transient RAM state, animation phase, held keys and macro execution position are not captured. Saved RGB bytes and exposed RAM values are recorded separately.

Restore is blocked before any erase or setting write when a keycode is unknown or when required core NVM data, RGB flags or padding cannot be reproduced with available setters. Direct palette mode is also blocked. A failed compatibility check requires stopping and resolving the settings or target explicitly; the tool does not silently discard those values.

## Offline verification

The earlier settings-only run passed eight offline suites (222 tests, two skips); its [run record](../audits/rc6/host-settings-offline-20261023.json) is historical evidence. The current full qualification passes 23 suites with 257 unit tests and zero skips; see [status](STATUS.md) and [CI](CI.md). Read-only diagnosis passed on the installed legacy firmware. Settings writes, an update, candidate firmware behavior and power-loss behavior were not tested on the device. The existing Windows executables predate this feature; a new native Windows build and GUI check remain pending.
