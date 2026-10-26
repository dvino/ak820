Русский перевод: [Установка и восстановление](ru/INSTALL.md).

# Installation and recovery

These instructions describe beta.2 packages; publication status is recorded in [Status](STATUS.md).

Use these packages only with a wired AJAZZ AK820 that has a VS11K28A
controller and matching PCB revision. V2, Pro and Max are not supported. The
product name and USB ID `320F:505B` alone do not confirm compatibility. The
first installation creates an OEM recovery session. Keep it and later settings
backups in separate private copies.

Offline English and Russian guides are included under `AK820/_internal/docs/` and `AK820/_internal/docs/ru/` in each native package. Start with `profiles/README.md` in the chosen language.

## Choose a profile

The installer offers ten firmware profiles. `main` is selected by default.
Choose a profile before starting an operation; the installer shows its purpose
and changes from `main`. The choice stays fixed while package checks,
preparation, confirmation and installation are in progress. Choosing a profile
alone does not write to the keyboard.

| Profile | What it adds or changes |
| --- | --- |
| `main` | Key Overrides, Leader macro shortcuts, temporary Dynamic Macros and VialRGB Direct control. |
| `game` | Adds NKRO reports and controls and GUI lock; keeps Key Overrides, Dynamic Macros and Direct lighting; removes Leader. |
| `mmo` | Adds NKRO, GUI lock and eight Tap Dance entries instead of Key Overrides; keeps Dynamic Macros and Direct lighting; removes Leader. |
| `typing` | Adds Auto Shift and Space Cadet; keeps Key Overrides, Leader and Dynamic Macros; removes Direct lighting. |
| `code` | Adds Space Cadet and Grave Escape; keeps Key Overrides, Leader and Dynamic Macros; removes Direct lighting. |
| `pointer` | Adds Mouse Keys for pointer movement, scrolling and buttons; keeps Key Overrides, Leader and Dynamic Macros; removes Direct lighting. |
| `onehand` | Adds Mouse Keys and Tap Dance; keeps Leader and Dynamic Macros; removes Key Overrides and Direct lighting. |
| `creative` | Adds Tap Dance; keeps Leader, Dynamic Macros and Direct lighting; removes Key Overrides. |
| `shortcuts` | Adds Tap Dance; keeps Key Overrides and Leader; removes Dynamic Macros and Direct lighting. |
| `multios` | Adds Mac/PC Alt/GUI mode and Ctrl/GUI swap; keeps Key Overrides, Leader and Dynamic Macros; removes Direct lighting. |

All profiles include six layers, 16 saved Vial macros, eight Combos, QMK
Settings for supported timing parameters, One Shot, common tap/hold and media
functions, built-in RGB effects and host-controlled OS indication. `main` also
includes Key Overrides and VialRGB Direct control. Direct is needed for
per-LED control by a compatible application; built-in lighting remains
available in every profile. See the [profile descriptions](profiles/README.md)
for details and limits.

To change the installed profile, prepare an update to the selected target with
a settings backup. The installer checks settings compatibility for the exact
source and target images and stops before writing if the transition is not
supported. In the CLI, select a profile with `--profile`, for example
`AK820-cli --profile game verify`. `verify` checks package files without
accessing the keyboard.

## Download and check a package

Open the [beta.2 release page](https://github.com/dvino/ak820/releases/tag/v0.6.0-beta.2)
and download the package and its matching checksum file:

- Windows installer: [AK820-Windows.zip](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Windows.zip) and [AK820-Windows.zip.sha256](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Windows.zip.sha256).
- Linux x86_64 installer: [AK820-Linux-x86_64.tar.gz](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Linux-x86_64.tar.gz) and [AK820-Linux-x86_64.tar.gz.sha256](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Linux-x86_64.tar.gz.sha256).
- Firmware and companion catalog: [AK820-Beta2-Catalog.zip](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Beta2-Catalog.zip) and [AK820-Beta2-Catalog.zip.sha256](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.2/AK820-Beta2-Catalog.zip.sha256).

On Windows, compare the downloaded archive with its checksum in PowerShell.
For the installer, run:

```powershell
$expected = (Get-Content .\AK820-Windows.zip.sha256 -Raw).Trim().Split()[0]
$actual = (Get-FileHash .\AK820-Windows.zip -Algorithm SHA256).Hash
if ($actual -ne $expected) { throw 'SHA256 mismatch; do not extract this package.' }
```

Use the corresponding `.sha256` filename for the Linux or catalog archive.
On Linux, run the matching command in the folder containing both files, for
example:

```sh
sha256sum -c AK820-Linux-x86_64.tar.gz.sha256
```

If a checksum does not match, do not extract or run the package. Download both
files again.

## Windows

Extract the complete ZIP and keep its folders together. Launch
`AK820-Windows/AK820/AK820.exe`. Python does not need to be installed. The
command-line tool is in `AK820-Windows/AK820-cli/AK820-cli.exe`.

## Linux

The standalone package is for x86_64 Linux with glibc 2.35 or newer, such as
Ubuntu 22.04. It includes Python and Tk. It needs `libudev1`, a desktop display
that supports X11 or XWayland, and normal `udev`/hidraw device access.

After checking the checksum, extract the archive and launch the GUI:

```sh
tar -xzf AK820-Linux-x86_64.tar.gz
cd AK820-Linux-x86_64
./AK820/AK820
```

If the application cannot access the keyboard, install the supplied device
rule from a desktop terminal:

```sh
./AK820-cli/AK820-cli udev --install
```

This command uses `sudo` only to install and apply the rule. Run the GUI as the
ordinary desktop user; do not launch it with `sudo`.

## Firmware and companion catalog

The catalog archive contains firmware images and data for companion
integration; it does not contain a desktop application to launch. Its JSON
files describe profile selection, exact-image capabilities and module help.
The `guide.en` and `guide.ru` paths in module descriptions are relative to the
repository's `web/` directory. Resolve them against
`https://github.com/dvino/ak820/blob/v0.6.0-beta.2/web/`, and include the
linked guides in a companion package for offline help. Read the [firmware
handoff](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/web/docs/FIRMWARE-HANDOFF.md)
before integrating catalog data.

## First installation from OEM firmware

If the keyboard still runs its original OEM firmware, an earlier recovery
session is not required. Close the OEM configurator and connect only one
supported keyboard. Prepare alternate input and stable power.

In the GUI, open **Other actions — OEM installation and recovery** and choose
**Install from OEM**. Confirm reading the complete original ROM. The installer
checks that copy, prepares the update and shows its image before requesting
write confirmation. Follow the installer prompts, including the typing check
after restart. Stop on any error; do not repeat the write blindly.

Keep the complete session folder shown in the log. Its `permanent-session`
subfolder contains `images.json`, `before-full-rom.bin` and `restore-native.bin`;
select that subfolder as the OEM recovery session for future updates and
recovery. These private files are read from the keyboard, not downloaded with
the release. **Save OEM backup** in the same panel saves a recovery session
without installing firmware.

## Back up settings and update firmware

Read [Settings backup and restore](SETTINGS-BACKUP.md) before changing the
firmware. In the GUI, select the OEM recovery session and a new backup folder,
then choose Update. Prepare alternate input and stable power first. The
installer shows the exact update; a fresh physical Esc + left Control hold for
three seconds confirms it. The installer requests unlock, enters the loader,
flashes once and verifies the image. It then asks for a second fresh hold before
restoring and checking the saved settings. Both holds happen inside the
installer. No typed `yes`, separate Vial app or manual Bootloader action is
needed. Cancel before erase if the displayed update is not intended.

On timeout, storage error or bad readback, stop. Do not retry, reset or restore
blindly. See [Settings backup and restore](SETTINGS-BACKUP.md) for what can be
saved and which old backups can be moved to firmware with Combos.

## OEM recovery

The OEM recovery session contains original firmware data needed to reconstruct
and check the supported image. Keep it private and separate from the settings
backup. For recovery from a loader that is already visible, use the supplied
CLI's `recover --session OEM_DIR` command. If the application is unresponsive
and the loader is unavailable, stop and seek help; do not repeat an erase.
