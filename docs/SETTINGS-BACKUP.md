Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

The installer saves supported settings to a private folder, restores them, or
carries them through a supported firmware update. It uses existing Vial
commands; the firmware has no separate backup protocol.

## Supported firmware and migration

The current beta.2 installer profiles are `main`, `game`, `mmo`, `typing`,
`code`, `pointer`, `onehand`, `creative`, `shortcuts` and `multios`. The exact
profile images and approved transitions are listed in [Status](STATUS.md).
The installer checks the application and firmware before writing. It accepts
same-image restore and only exact whitelisted forward transitions. Downgrades,
unknown images and unlisted profile-to-profile transitions are rejected.

The offline transition set includes alpha.2, alpha.3 and beta.1 `work` as
sources to each of the ten beta.2 profiles, plus the reviewed transitions
between beta.2 profiles. It does not promise that every saved value exists or
can be reproduced by every target profile. Unsupported keycodes, inactive
Tap Dance or Key Override entries, unavailable QMK Settings, or Direct RGB
values that cannot be reproduced stop restore before the first settings write.

Older firmware has no Combo settings, so its backup has no Combo section. A
Combo-enabled backup records all eight slots, including empty ones. A malformed
or unsupported Combo version stops backup or restore before settings are
written. An older backup can be restored to Combo-enabled firmware only when
all eight target slots are empty; they remain empty. A Combo-enabled backup
applies all eight saved slots, so an empty slot clears the matching target
slot. Firmware without Combo support rejects a backup that contains Combos.
See [Combo behavior](COMBOS.md) for supported entries.

Caps Word Combos and macro-on-tap Layer-Tap keycodes require a target image that supports them. The installer
checks the exact source and target images before preparing an update. Earlier
beta.2 images remain recognized as migration sources; they do not gain these
actions. A Caps Word Combo or macro-on-tap Layer-Tap keycode cannot be restored
to an image that lacks its support.

## Commands

Run the source installer as `AK820.sh` on Linux or `AK820.cmd` on Windows.
Select an exact profile with `--profile`; the default is `main`:

```sh
./AK820.sh --profile main backup --session OEM_DIR --output NEW_DIR
./AK820.sh --profile main restore --session OEM_DIR --backup BACKUP_DIR
./AK820.sh --profile main update --session OEM_DIR --backup-dir NEW_DIR
```

Each command needs a valid OEM recovery session. The installer uses it to
reconstruct and check the exact firmware image. A settings backup cannot
replace this session.

`backup` reads the keyboard and creates a new private folder; it never replaces
an existing backup. The folder includes ROM and diagnostic data as well as
settings, so keep it private and outside Git. `restore` first backs up the
current device, then writes supported values and checks them by reading them
back.

In the GUI, choose the OEM session and backup folder, then select Backup,
Restore or Update. Before Update, prepare alternate input and stable power. A
fresh physical Esc + left Control hold for three seconds confirms the displayed
update. After flashing and checking the image, the installer requests a second
fresh hold before restoring settings. Both holds happen inside the installer.
No typed `yes`, separate Vial app or manual Bootloader action is needed. Cancel
before erase if the displayed update is wrong. On an error, timeout or bad
readback, stop; do not retry or restore blindly.

## Saved settings and limits

A backup includes 498 key assignments across six layers, 12 encoder
assignments, 16 macros, layout options and supported RGB settings. Combo-enabled
firmware also saves all eight Combo slots. Beta.2 schema `0x082003` backups
use typed format `ak820-settings-backup-2` and include the complete extension
tables and QMK Settings data, including stored tables for modules inactive in
the selected profile. Saving those tables does not activate the modules during
restore. Legacy backups use `ak820-settings-backup-1`; they can initialize a
beta.2 target's extension storage only when its tables are empty and settings
are at defaults. The installer checks saved files before completing a backup.

Connect only one supported keyboard. Its Vial identifier identifies the
model, not a unique unit. Reads do not freeze the firmware: keep configuration
tools closed and do not change settings during a backup. Repeated reads check
for changes but cannot guarantee an atomic snapshot. A mismatch stops the
operation.

The backup does not include the Direct RGB palette, temporary lighting state,
animation position, held keys or a running macro's position. Restore stops
before writing when a saved value cannot be reproduced with supported settings
commands.

Exact image identities and current validation results are recorded in
[Status](STATUS.md). The typed storage layout and migration rules are in
[Module storage](MODULE-STORAGE.md).
