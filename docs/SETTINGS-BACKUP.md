Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

The source installer can save supported settings to a private local folder, restore them, or carry them through one supported firmware update. This is a host-only feature: it uses existing Vial commands and does not add a backup protocol to firmware.

## Supported firmware

Four exact SDCC 4.6 images are recognized by the settings profile:

- Legacy RC6 IHX: `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`;
  permanent CODE SHA256: `6ff7b1653925da7dc12bdb6f7ef5fc1dc4319c5b931def50c68b9cf45c4054d7`.
- Pointer candidate IHX: `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`;
  permanent CODE SHA256: `119c907421d45154b0e6c16fb176ec2c1a51c1fec9627e341599d5b0cc8dca52`.
- Compact tap-hold candidate IHX: `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`;
  its permanent CODE SHA256 is `7e6b90f51a99ac335c0cb910fffc85f1d1705e7159a12de46f8e492807c36d40`.
- C/W source candidate IHX: `45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`;
  its permanent CODE SHA256 is `cc5af6cc86724103fbc3e2c1815bf7a2235edc0ed85a932fd3e993cd6b4f7931`.

Same-image restores and forward transitions in the listed order are supported
by the host model. Downgrades and unknown images are rejected. All four profiles
use schema `0x082002` and the same UID, keycode and NVM capacities. The compact
tap-hold candidate changes the 200 ms hold behavior and macro-owned primitive
semantics; Caps Word behavior is described in [Mod-Tap and Layer-Tap](TAP-HOLD.md).
The C/W source candidate follows the compact tap-hold profile and retains those
settings capacities. Its exact OEM-based image was packed locally from an
isolated source candidate. It is now released and installed as `v0.6.0-alpha.1`.
The live transition from the legacy profile verified settings restoration;
see [Status](STATUS.md) for the post-restart open failure and separate guarded restore.
The earlier three programs remain public CI artifacts.
Sharing a schema alone never grants compatibility: the actual CODE hash and
manifest must match one of the exact profile identities. The target snapshot
must match the selected target before physical unlock or setters.

The four-profile transition model is an in-memory host test. It does not
qualify CPU behavior, a complete release artifact or behavior on a keyboard.

The checked-in installer bundle and CI package selection are separate from
this profile allowlist; see the [CI policy](CI.md) for package selection.
The legacy-to-alpha transition has been checked on a keyboard; the other
profile transitions remain host-model checks. Unsupported firmware or settings stop the operation before erase;
arbitrary build migration is not supported.

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

The earlier settings-only run passed eight offline suites (222 tests, two skips); its [run record](../audits/rc6/host-settings-offline-20261023.json) is historical evidence. The current full qualification record is in [status](STATUS.md) and [CI](CI.md). The four-profile transition test is an in-memory host model; it does not qualify CPU behavior or a built artifact. Alpha release CI passed. The downloaded image was installed once and checked through live readback. The update stopped after restart with an open error; a separately guarded restore then verified the saved settings. See [Status](STATUS.md) for that result and the manual smoke checks. Power-loss behavior remains untested. CI has built the native Windows packages and passed Tk startup checks; visible dialogs and interactive behavior remain untested.
