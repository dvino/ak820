Русский перевод: [Сохранение настроек](ru/SETTINGS-BACKUP.md).

# Settings backup and restore

Use the Python installer script to save or restore settings. The script checks
the exact firmware image and stops if the saved data is unsupported. Settings
restore does not change the selected profile or save Direct colors to EEPROM.
The selected profile must have its complete, exactly approved release assets.
A mismatched or absent beta.5 profile catalog/approval blocks restore before USB access; an older image is never silently substituted.

## Run the script

Use `tools/installer/ak820.py` from the source tree, or the matching Python
release package for Windows or Linux x86_64. Install the listed Python
dependency first. Windows uses `py -3`; Linux uses `python3`.

```sh
python3 tools/installer/ak820.py --profile main backup --help
python3 tools/installer/ak820.py --profile main restore --help
```

Follow the command prompts and use the local OEM recovery session and backup
paths requested by the script. A settings backup does not replace the OEM
recovery files. Keep backups private and outside source control. See
[installation](INSTALL.md) for downloading, checksum verification and setup.

## What is saved

The durable settings backup contains key and encoder assignments, macros,
supported options and RGB settings. The typed schema 03 format also preserves
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

For beta.5, recognized settings sources are the exact published beta.3, beta.4,
beta.4.1 and beta.5 images; targets must be beta.5 images. This recognition and
offline transition testing do not authorize settings writes: the beta.5 catalog
keeps `settings_writes_authorized` false. Other release sources are unsupported.
Transitions between profiles of the current release must be explicitly listed
and still pass schema, feature and value checks. Keep configuration
software closed during backup; the firmware does not pause while settings are
read. A failed read, timeout or mismatch stops the operation.

The backup format and migration rules are described in
[module storage](MODULE-STORAGE.md). Current release identities and status are
listed in [Status](STATUS.md).
