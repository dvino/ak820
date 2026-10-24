Русский перевод: [Установка и восстановление](ru/INSTALL.md).

# Installation and recovery

Use these packages only with the wired AJAZZ AK820 that has a VS11K28A
controller and matching PCB revision. V2, Pro and Max are not supported. The
product name and USB ID `320F:505B` alone do not confirm compatibility. Keep a
valid OEM recovery session and a separate settings backup.

## Download and check a release package

Open [Releases](https://github.com/dvino/ak820/releases) and download the
package and matching `.sha256` file for the operating system:

- Windows: `AK820-Windows.zip` and `AK820-Windows.zip.sha256`.
- Linux x86_64: `AK820-Linux-x86_64.tar.gz` and
  `AK820-Linux-x86_64.tar.gz.sha256`.

On Windows, compare the downloaded archive with its checksum in PowerShell:

```powershell
$expected = (Get-Content .\AK820-Windows.zip.sha256 -Raw).Trim().Split()[0]
$actual = (Get-FileHash .\AK820-Windows.zip -Algorithm SHA256).Hash
if ($actual -ne $expected) { throw 'SHA256 mismatch; do not extract this package.' }
```

On Linux, run the checksum command in the folder containing both downloaded
files:

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

## Use the source installer

The native packages above are the normal way to install a release. To run the
source installer or build firmware, follow [Build](BUILD.md). Source tools need
Python 3.10 or newer; firmware builds use Linux or WSL with the pinned toolchain.
