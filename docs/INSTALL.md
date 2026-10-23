Русский перевод: [Установка и восстановление](ru/INSTALL.md).

# Installation and recovery

Use the complete release with the wired AJAZZ AK820 / VS11K28A. The installer
also checks the firmware already in the keyboard: the product name and USB ID
alone are not enough to identify a supported version. It stops before erasing
if the firmware is not supported. See [status](STATUS.md) for the checked build
and what has been tested on a keyboard.

## Before installing

Have another keyboard or the operating system's on-screen keyboard ready. The
AK820 cannot type while it is in its original loader. Close other keyboard
configuration tools. Connect one supported AK820 and leave its cable connected
until installation and checks finish.

Before it resets or erases anything, the installer reads all 65,536 bytes of
the keyboard's ROM and saves an exact recovery copy for you. It carries settings
over only when the new firmware can represent them. If a key assignment cannot
be carried over, or a macro is too large, preparation stops instead of silently
losing that data. A partial read may help diagnose a problem, but it is not a
complete backup.

The installer does not include the manufacturer's ROM images. It compares your
backup with known loader, protected-area and firmware signatures, then makes
private comparison files in your recovery folder. This identifies a supported
firmware version; it does not prove that other keyboards with the same name or
USB ID will work.

The recovery folder belongs to your keyboard. Keep a separate copy. Do not use
another owner's backup and do not commit ROM captures or diagnostic archives
containing personal settings to a public repository.

## Updating the owner's installed RC6 candidate

The GUI's `Обновить прошивку` action is a limited repair workflow
for the exact candidate and personal session checked in this work. It is not
a general updater for other keyboards or images. Its offline review and
standalone build must pass before use; see [status](STATUS.md).

Select the prepared personal session. The GUI reads and saves the current full
ROM, checks it against the recorded fault state, and stops if it differs. It
preserves the durable settings from before the failed encoder probe, including
the original clockwise assignment, and discards that probe's pending journal.
It shows the image hash and asks for explicit consent before writing.

The integrated update workflow passed review and this owner's installation. Click Update,
then hold physical Esc + left Control together for three seconds when asked.
That fresh hold confirms the displayed update. No typed `yes`, `ready`, Vial
app or manual Bootloader action is required. The installer requests unlock,
checks completion, sends one loader transition and waits for the loader.
Cancellation is allowed before erase. If a command or transition fails, it
stops without retry, reset or recovery. After one transfer it checks startup and full
readback. Physical typing and a power cycle are not part of these checks.

The GUI starts in Russian only when the system language is Russian; otherwise
it starts in English. The RU / EN button changes the interface language.

## Source-based command line

Python 3.10+ is needed for the source installer. Windows firmware compilation
uses WSL, but installing an already built image does not.

| Action | Linux | Windows |
| --- | --- | --- |
| Verify files without USB | `./AK820.sh verify` | `.\AK820.cmd verify` |
| Install local host dependencies | `./AK820.sh setup` | `.\AK820.cmd setup` |
| List device state without opening it | `./AK820.sh` | `.\AK820.cmd` |
| Prepare backup and install permanently | `./AK820.sh install` | `.\AK820.cmd install` |
| Explicit one-session trial | `./AK820.sh install --trial` | `.\AK820.cmd install --trial` |
| Recover from an already visible loader | `./AK820.sh recover --session PATH` | `.\AK820.cmd recover --session PATH` |

Put paths with spaces in quotes. During preparation, answer `y` to continue or
press Enter to cancel. Before writing, the installer shows the selected image
and recovery folder, then asks you to type the exact lowercase word `yes`. It
asks for both approvals while the keyboard can still type. If you cancel, it
does not reset or erase the keyboard.

Permanent mode keeps the marker that starts the application. Trial mode clears
that marker during startup, so the next reset or unplug returns to the loader.
Trial is only for a short test. A successful file transfer or checksum alone
does not mean installation worked: the installer also checks that the keyboard
is running, asks you to type, and reads back the application, protected areas
and initial settings.

## Recovery

If the permanent application still responds, unlock Vial and choose its
Bootloader action. This clears the application marker and restarts the keyboard
in its original loader. Simply unplugging a permanent installation does not
start recovery. Run `recover --session PATH` with your own complete recovery
folder. The recovery command does not restart a running application or retry an
erase that failed.

If the application is unresponsive and the loader cannot be reached, stop.
Do not assume a software recovery action will work. Physical recovery access
and cold boot behavior require separate hardware validation.

## Windows application

The Windows GUI and command-line app were built locally as complete folders.
Use all of `dist/AK820-sdcc46-breathing-20261023/AK820/` or
`dist/AK820-sdcc46-breathing-20261023/AK820-cli/`; the EXE by itself is not enough.
These apps do not need Python installed on the target PC. The source version
still needs Python 3.10+. The [status page](STATUS.md) links to the local build
and offline check results. There is no public download yet.
