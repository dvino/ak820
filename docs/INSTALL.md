Русский перевод: [Установка и восстановление](ru/INSTALL.md).

# Installation and recovery

Use a published complete release with the wired AJAZZ AK820 / VS11K28A. As of 2026-10-24, `v0.6.0-alpha.1` is the latest published and installed version. The planned `v0.6.0-alpha.2` candidate is not published or installable; its Combo backup migration is implemented, with final verification pending. The installer checks the firmware already in the keyboard; the product name and USB ID alone do not identify a supported build. It stops before erasing if the source is unsupported. See [status](STATUS.md) for evidence and device state.

## Package setup

For a Windows release, extract the complete archive and run `AK820/AK820.exe`. Keep all extracted files together. The source installer needs Python 3.10+; Windows firmware builds use WSL, but installing an already built image does not. Offline package verification:

```sh
./AK820.sh verify
```

```powershell
.\AK820.cmd verify
```

Windows CI packages include settings backup, restore and the supported update workflow. Use the complete package from the selected release. The checked-in legacy bundle is older; [Status](STATUS.md) identifies the checked builds. Offline `verify` does not load HID or open USB.

## Use a release firmware bundle with the source installer

Use a clean checkout of the selected release tag. Verify `firmware-bundle.zip`
with its accompanying SHA256 file, then extract it into a folder named
`firmware-bundle`. Copy the contents of
`firmware-bundle/` into `releases/rc6/` and copy its `approved-release.json` to
`tools/installer/approved-release.json`. Run `./AK820.sh verify` before any
device command. This selects the CI-built release rather than the legacy
firmware stored in the source checkout. Keep the full bundle together.

## Linux source setup

Install Python, its venv and development packages, GCC and libudev development
files. On Debian or Ubuntu the build packages include `build-essential`,
`python3-dev`, `python3-venv` and `libudev-dev`. Then run:

```sh
./AK820.sh setup
./AK820.sh udev --install
```

Setup builds pinned hidapi from source with the Linux hidraw backend and
bypasses cached wheels built with another backend. The udev command uses sudo
only to install and apply the device rule; run the installer as the ordinary
desktop user. Neither command resets the keyboard. In a restricted agent
terminal, `no_new_privs` can prevent sudo even when passwordless sudo is
configured; apply the udev command from the ordinary desktop terminal.

## Settings backup and supported update

Read [Settings backup and restore](SETTINGS-BACKUP.md) before running the new commands. They support only the exact reviewed IHX/CODE pairs listed there. Every operation needs a valid OEM recovery session because exact CODE reconstruction uses native bytes not shipped in the repository. Keep the OEM session and settings backup separately.

Before restore or update, confirm the wired VS11K28A hardware revision. Neither the AK820 name nor USB `320F:505B` alone proves compatibility; V2, Pro and Max are unsupported. A mismatched image can leave the keyboard unusable.

The supported commands are:

```sh
./AK820.sh backup --session OEM_DIR --output NEW_DIR
./AK820.sh restore --session OEM_DIR --backup BACKUP_DIR
./AK820.sh update --session OEM_DIR --backup-dir NEW_DIR
```

The equivalent Windows source commands use `AK820.cmd`. Backup reads the keyboard and publishes a new private folder. Restore saves the current target state before writing. The GUI Update action displays the exact update being confirmed. A fresh physical Esc + left Control hold for three seconds confirms it; the installer requests unlock, enters the loader, flashes once and verifies the result. It then requests a second fresh physical hold before restoring and checking settings. Both holds happen inside the installer. No typed `yes`, separate Vial app or manual Bootloader action is part of this workflow. Cancel before erase if the displayed operation is not intended. Errors stop the operation without a retry, blind restore or reset.

In the GUI, choose the OEM session and output or backup folder, then select Backup settings, Restore settings or Update firmware. Before an update, prepare alternate input and stable power. When prompted, make a fresh Esc + left Control hold for three seconds. The installer shows the action being confirmed; cancel before erase if it is not the intended update. After flashing and verification, make a second fresh hold when the installer asks to restore the saved settings.

## OEM recovery

The OEM recovery session contains the original native bytes required to reconstruct and validate the supported firmware. Use a valid session from a supported OEM keyboard; do not use another person's settings backup as a substitute. Keep recovery files private and make a separate copy. ROM captures and diagnostic files may contain personal settings; do not publish them.

For recovery from an already visible loader, use the source command `recover --session OEM_DIR`. Recovery does not restart a running application or retry an erase that failed. If the application is unresponsive and the loader cannot be reached, stop; software recovery has not been established for that condition.

## Existing install paths

The source installer retains the existing `install`, `install --trial` and `recover --session OEM_DIR` workflows. Their behavior and hardware verification state are described in [status](STATUS.md). Do not treat a successful transfer or checksum as proof of physical typing, settings persistence or power-cycle behavior.

Offline checks do not authorize device writes. Each update needs its own confirmation, a fresh backup and an exact image check. Alpha releases are test builds; the release notes and Status distinguish source, package checks and device results.

## Historical alpha.1 stop (2026-10-24)

During installation of `v0.6.0-alpha.1`, `open failed` occurred after restart.
The installer stopped before settings restoration. The cause is not established.
Do not repeat the flash. Preserve the log and backup; first check permissions,
the exact running CODE and healthy storage through read-only diagnosis. Only
after those checks pass may a separate normal settings restore proceed with
a fresh target backup and physical confirmation. See [Status](STATUS.md) for
the recorded operation.
