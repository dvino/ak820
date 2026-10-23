Русский перевод: [Установка и восстановление](ru/INSTALL.md).

# Installation and recovery

Use the complete release with the wired AJAZZ AK820 / VS11K28A. The installer checks the firmware already in the keyboard; the product name and USB ID alone do not identify a supported build. It stops before erasing if the source is unsupported. See [status](STATUS.md) for evidence and device state.

## Package setup

For a Windows release, extract the complete archive and run `AK820/AK820.exe`. Keep all extracted files together. The source installer needs Python 3.10+; Windows firmware builds use WSL, but installing an already built image does not. Offline package verification:

```sh
./AK820.sh verify
```

```powershell
.\AK820.cmd verify
```

The source bundle passed offline `verify` with no HID load or USB access. The currently checked Windows applications predate settings backup/restore; use the source installer for this feature. No updated Windows package is available.

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

Read [Settings backup and restore](SETTINGS-BACKUP.md) before running the new commands. They support only the exact SDCC 4.6 RC6 image identified there. Every operation needs a valid OEM recovery session because exact CODE reconstruction uses native bytes not shipped in the repository. Keep the OEM session and settings backup separately.

The supported commands are:

```sh
./AK820.sh backup --session OEM_DIR --output NEW_DIR
./AK820.sh restore --session OEM_DIR --backup BACKUP_DIR
./AK820.sh update --session OEM_DIR --backup-dir NEW_DIR
```

The equivalent Windows source commands use `AK820.cmd`. Backup reads the keyboard and publishes a new private folder. Restore saves the current target state before writing. Update saves settings, flashes one approved image, then restores and verifies. New write operations use a physical unlock dialog; they do not ask for typed `yes`. A second physical unlock is required after restart for restore. Errors stop the operation without a retry, rollback or reset.

In the GUI, choose the OEM session and output or backup folder, then select Backup settings, Restore settings or Update firmware. For update, prepare a spare keyboard and stable power. When prompted, make a fresh Esc + left Control hold for three seconds. The installer shows the action being confirmed. Cancel before erase if the displayed operation is not intended.

## OEM recovery

The OEM recovery session contains the original native bytes required to reconstruct and validate the supported firmware. Use a valid session from a supported OEM keyboard; do not use another person's settings backup as a substitute. Keep recovery files private and make a separate copy. ROM captures and diagnostic files may contain personal settings; do not publish them.

For recovery from an already visible loader, use the source command `recover --session OEM_DIR`. Recovery does not restart a running application or retry an erase that failed. If the application is unresponsive and the loader cannot be reached, stop; software recovery has not been established for that condition.

## Existing install paths

The source installer retains the existing `install`, `install --trial` and `recover --session OEM_DIR` workflows. Their behavior and hardware verification state are described in [status](STATUS.md). Do not treat a successful transfer or checksum as proof of physical typing, settings persistence or power-cycle behavior.

The current feature work does not authorize or perform live device operations. Physical acceptance and public release remain separate steps; this offline source check does not approve either.
