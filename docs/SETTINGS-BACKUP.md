Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

The installer can save supported settings to a private folder, restore
them, or carry them through a supported firmware update. It uses existing Vial
commands; the firmware does not need a separate backup protocol.

## Supported firmware and migration

The installer accepts five exact reviewed image profiles. Their IHX and CODE
hashes are listed in the [profile record](../audits/rc6/alpha2-release-20261024/settings-profiles.json);
[Status](STATUS.md) identifies the current release and installed image.
It checks both the application and firmware already in the keyboard before
writing. Same-build restore and approved forward migrations are supported;
downgrades and unknown builds are rejected.

Older firmware has no Combo settings, so its backup has no Combo section. A
Combo-enabled backup records all eight slots, including empty ones. A malformed
or unsupported Combo version stops backup or restore before settings are
written. An older backup can be restored to Combo-enabled firmware only when
all eight target slots are empty; the restore leaves them empty. Restoring a
Combo-enabled backup applies all eight saved slots, so an empty slot clears the
matching target slot. Firmware without Combo support rejects a backup that
contains Combos. See [Combo behavior](COMBOS.md) for supported entries.

## Commands

Run the source installer as `AK820.sh` on Linux or `AK820.cmd` on Windows:

```sh
./AK820.sh backup --session OEM_DIR --output NEW_DIR
./AK820.sh restore --session OEM_DIR --backup BACKUP_DIR
./AK820.sh update --session OEM_DIR --backup-dir NEW_DIR
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
firmware also saves all eight Combo slots. The installer checks the saved files
before completing the backup.

Connect only one supported keyboard. Its Vial identifier identifies the model,
not a unique unit. Reads do not freeze the firmware: keep configuration tools
closed and do not change settings during a backup. Repeated reads check for
changes but cannot guarantee an atomic snapshot. A mismatch stops the operation.

The backup does not include the Direct RGB palette, temporary lighting state,
animation position, held keys or a running macro's position. One Shot, Mouse
Keys, Tap Dance and Key Overrides are unsupported. Restore stops before writing
when a value cannot be reproduced with supported settings commands.

Exact image identities and current validation results are recorded in
[Status](STATUS.md).
