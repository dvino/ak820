Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

**Beta.5 does not authorize settings writes.** Catalog approval, image
recognition and offline migration checks do not authorize restore or settings
transfer. Backup and export for the current candidate's v3 images are also
blocked pending exact-image qualification. The guidance below describes backup
where supported and restore only if writes become authorized.

For a supported image, use the Python installer script to save settings. For a permitted restore, the
script checks the exact firmware image and stops if the saved data is unsupported. Settings
restore does not change the selected profile or save Direct colors to EEPROM.
The selected profile must have its complete, exactly approved release assets.
A mismatched or absent beta.5 profile catalog/approval blocks restore before USB access; an older image is never silently substituted.

During a permitted restore, close other keyboard clients and do not press keys,
reset the keyboard or enter its loader. The open HID handle does not exclude
other clients: a separate raw-HID command can change the loader marker after
an image check. The adapter cannot eliminate that race. A transport failure
stops the operation; do not retry or restore blindly.

## Run the script

Use `tools/installer/ak820.py` from the source tree, or the matching Python
release package for Windows or Linux x86_64. Install the listed Python
dependency first. Windows uses `py -3`; Linux uses `python3`.

```sh
python3 tools/installer/ak820.py --profile main backup --help
python3 tools/installer/ak820.py --profile main restore --help
```

For a supported image, supply paths as arguments: `backup --session OEM_DIR --output BACKUP_DIR`
uses the original private OEM recovery session (`permanent-session` inside
the installation session folder) and a separate settings backup directory. If settings writes become authorized, restore uses
`restore --session OEM_DIR --backup BACKUP_DIR`. These are subcommands of the
script; after package setup, use `AK820.cmd` on Windows or `./AK820.sh` on Linux.
A settings backup does not replace the OEM recovery files. Keep both private
and outside source control. See [installation](INSTALL.md) for setup.

## What is saved

The durable settings backup format covers key and encoder assignments, macros,
supported options and RGB settings; format support does not make v3 export available. The typed schema 03 format also preserves
the supported extension data. Exact image identities and permitted transitions
are checked before restore. Unsupported keycodes, extension entries, settings,
or profile transitions stop restore before its first settings write.

Direct colors are volatile and use a separate `direct-ram.json` sidecar when
the exact image advertises Direct v1 and runtime negotiation succeeds. The
sidecar records the 82 HSV8 entries and their format metadata. The settings
export does not freeze all RAM and NVM state at the same instant.

The separate `restore_direct_palette` API restores this sidecar only after an
explicit write-enabled call, exact-image and runtime-capability checks, and a
fresh palette generation read. It commits the complete frame and verifies the
palette readback. This API does not select Direct mode or save the palette to
EEPROM. Older backups without the sidecar cannot recover Direct colors. See
[Direct palette](DIRECT.md) for the protocol and limits.

The original beta.5 release was published on 2026-10-29. Preserved release
metadata records 16 assets, the release notes, and beta.3, beta.4, beta.4.1
and the original beta.5 images as settings sources with beta.5 targets. Handoff evidence records passing
release CI run `40826926074`, verification of 16 release-file SHA256 values,
and a match between the ten published IHX files and then-qualified local
images. The release is no longer available at its former GitHub page. These
historical checks do not qualify the current candidate or establish physical
behavior. Its catalog keeps `settings_writes_authorized` false. Other release
sources are unsupported. Transitions between profiles of a release must be
explicitly listed and pass schema, feature and value checks. Keep configuration
software closed during backup; firmware does not pause while settings are read.
A failed read, timeout or mismatch stops the operation.

The current local tag `v0.6.0-beta.5` points to commit
`2ab372dab7f084b76b57aa98a9543c249a6d0c30`, tagged 2026-11-01. Do not identify
this candidate with the earlier release: its release page is unavailable, and
the current candidate has not been qualified for release.

The current candidate for possible re-publication is not release-qualified. Its policy
admits only authenticated beta.4.1 profile identities and its own current
profile identities as settings sources; targets are candidate profiles only.
Beta.3 sources are not admitted. Beta.4 and beta.4.1 images have identical
image identities, so they cannot be distinguished by image identity. The v3
exact-image loading and migration gates remain pending. This policy does not
qualify the candidate, authorize settings writes or establish physical restore
behavior.

The backup format and migration rules are described in
[module storage](MODULE-STORAGE.md). Current release identities and status are
listed in [Status](STATUS.md).
