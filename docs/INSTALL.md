Русский перевод: [Установка](ru/INSTALL.md).

# Installation

Beta.4.1 provides Python source packages for Windows and Linux x86_64. The
packages contain the installer scripts and all ten approved firmware profiles.
They do not contain a GUI application. Python 3.10 or newer is required; use
the `python` command on Windows and `python3` on Linux.

Use the installer only with a wired AJAZZ AK820 with the supported VS11K28A
controller and PCB revision. V2, Pro and Max are not supported. The model name
and USB ID `320F:505B` alone do not confirm compatibility.

## Download and check the package

Download the matching archive and `.sha256` file from the
[beta.4.1 release page](https://github.com/dvino/ak820/releases/tag/v0.6.0-beta.4.1):

- Windows: `AK820-Windows.zip` and `AK820-Windows.zip.sha256`.
- Linux x86_64: `AK820-Linux-x86_64.tar.gz` and its `.sha256` file.

On Windows, compare the archive and checksum in PowerShell:

```powershell
$expected = (Get-Content .\AK820-Windows.zip.sha256 -Raw).Trim().Split()[0]
$actual = (Get-FileHash .\AK820-Windows.zip -Algorithm SHA256).Hash
if ($actual -ne $expected) { throw 'SHA256 mismatch; do not extract this package.' }
```

On Linux, run this command in the folder containing both downloaded files:

```sh
sha256sum -c AK820-Linux-x86_64.tar.gz.sha256
```

If the checksum does not match, do not extract or run the archive. Download
both files again.

## Windows

Install Python 3.10 or newer and make sure the `python` command is available.
Extract the complete ZIP, open the `AK820-Python` folder, and set up the local
Python environment:

```powershell
cd AK820-Python
.\AK820.cmd setup
.\AK820.cmd verify
```

The `AK820.cmd` script uses this local environment automatically. For example,
run `.\AK820.cmd diagnose` to list matching USB interfaces without opening them.

## Linux

Install Python 3.10 or newer, `python3-venv`, a C compiler, Python development
headers and `libudev` development files. On Debian or Ubuntu, these packages
are `python3`, `python3-venv`, `python3-dev`, `build-essential` and
`libudev-dev`.

Extract the archive, enter `AK820-Python`, and create the local environment:

```sh
tar -xzf AK820-Linux-x86_64.tar.gz
cd AK820-Python
./AK820.sh setup
./AK820.sh verify
```

The installer needs ordinary user access to the keyboard. If access is denied,
run `./AK820.sh udev --install` from a desktop terminal, then sign out and back
in if the system does not apply the new group access. Do not run the installer
with `sudo`.

## Prepare and install

`verify` checks the downloaded profile files and release approval without
accessing USB. To inspect a profile, add `--profile` before the command, for
example `./AK820.sh --profile game verify` on Linux or
`.\AK820.cmd --profile game verify` on Windows. The default profile is `main`;
the ten profiles and their differences are listed in
[`profiles/README.md`](profiles/README.md).

Before an installation, close the OEM configurator, connect one supported
keyboard, prepare alternate input and stable power, and read
[Settings backup and restore](SETTINGS-BACKUP.md). The `prepare` command
creates a local installation plan without writing to the keyboard. The
`install` command starts from OEM firmware, checks the live device, makes a
fresh OEM recovery copy and shows the exact image. It requires typed `yes`
before writing, then verifies the installed image and checks typing after restart.
Keep the complete session directory, including `permanent-session`, in a
private backup. Stop on an error; do not retry, reset or restore blindly.

To update an existing supported QMK/Vial installation, use
`update --session OEM_DIR --backup-dir NEW_BACKUP_DIR`. Keep the original OEM
recovery session and choose a new backup directory. The script saves current
settings and checks their transfer before requesting a fresh three-second
hold of Esc + left Control. It requests a second physical confirmation before
restoring settings after the update.

## OEM recovery

For a supported recovery, use `recover --session OEM_DIR` only when the
keyboard is already in its loader. For a settings restore, use the saved
settings session and the `restore` command described in
[Settings backup and restore](SETTINGS-BACKUP.md). Restore only after the
installer confirms that the selected source and target images are compatible.

## Companion catalog

The beta.4.1 firmware catalog is also available as `AK820-Beta4.1-Catalog.zip`.
It contains firmware and companion-integration data, not a desktop
application. Companion integration is planned separately.
