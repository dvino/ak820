Русский перевод: [Сборка](ru/BUILD.md).

# Build firmware

Build on Linux x86-64 or Ubuntu WSL with Python 3.11+, Make and GCC.
SDCC 4.6 and LUFA are downloaded dependencies, not tracked source.
From the repository root, install the pinned dependencies once:

```sh
python3 tools/install_sdcc46_toolchain.py
python3 tools/install_lufa_dependency.py --fetch
```

Both installers check pinned archive hashes. For offline installation, pass
`--archive /path/to/archive` instead of downloading. The default LUFA command
without options only checks the local dependency. The SDCC installer on Windows
uses Ubuntu WSL. End users should use the published standalone package, which
includes Python and hidapi. For source-based installer use, see the separate
setup below. Create the firmware build environment:

```sh
cd qmk-8051-ak820
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-ak820-build.txt
.venv/bin/python util/build_ak820.py \
  --sdcc-version 4.6.0 \
  --toolchain ../toolchains/sdcc-4.6.0 \
  --qmk-bin .venv/bin/qmk \
  --build-dir .build/local-1
```

For a control build with SDCC 4.4, install it with
`python3 tools/install_sdcc44_toolchain.py` from the repository root, then use
`--sdcc-version 4.4.0 --toolchain ../toolchains/sdcc-4.4.0` in the QMK directory.
Keep each compiler local and out of Git.

Use a fresh build directory. The builder rejects an existing directory and
records the actual compiler dependency closure, source/tool hashes, commands,
CODE/XRAM/IRAM allocation, IHX/MAP/MEM artifacts and `hardware_validated: false`.
Machine paths use forward slashes; validation also accepts legacy Windows
separators while rejecting paths outside the pinned roots and duplicate aliases.

The linked IHX is an application, not a complete image ready to flash. Packing
adds loader-facing entry/callbacks and validates protected regions against
known references. The release builder requires an explicit local
`--oem-reference-dir` containing `stock-full.bin` and `native-installed.bin`;
it uses them for offline validation and never copies them into the release.
During ordinary first installation, the installer creates private comparison
files in the recovery session from the user's complete verified ROM backup, so
no separate reference download is needed.

CODE has two separate windows: `[0x28a0,0x3000)` and `[0x3027,0xc700)`.
Free bytes in these windows are not interchangeable. NVM and macro storage are
not spare executable CODE. Measure linked occupied bytes rather than binary
file length or source size.

## Development profiles

To select any of the eight development profiles, use the [profile
configurator](BUILD-PROFILES.md). It links the complete image, checks resource
placement and runs offline regression gates plus the selected feature suites
against that image. No configured profile is approved for installation or
release: the whole-program stack bound, exact-image interrupt/nesting safety
and installer transition remain open. Packaging stops for every configured
profile.

The build uses the compact instruction outliner with a fixed opcode and module
allowlist. `--no-outline` and `--no-callee-saves` provide comparison builds.
Outlining changes the linked image and is not a runtime feature. Savings from
one image do not predict another profile because shared code and packing
interact. ABI changes require new stack and interrupt evidence. Do not run
build configurations concurrently in one source tree because Make uses shared
generated files. See the [outlining measurements](../audits/rc6/roadmap-max-20261024/outline-speed.md).

Run [offline tests](TESTING.md), then assemble a new release bundle from the
repository root after independent review. The review record must be a JSON file
bound to the exact IHX, MAP, build report and host inputs. The following is a
command template; replace the review and private reference paths with local
files and use a fresh output directory:

```sh
python3 tools/build_release_bundle.py \
  --build-dir qmk-8051-ak820/.build/local-1 \
  --review /path/to/exact-candidate-review.json \
  --oem-reference-dir /path/to/private-oem-references \
  --toolchain toolchains/sdcc-4.6.0 \
  --builder-source qmk-8051-ak820/util/build_ak820.py \
  --output releases/rc6-new
```

`docs/REVIEW.md` indexes review evidence; it is not the exact-build approval
record. Bundle assembly does not authorize device operations. A changed source
or host input invalidates earlier evidence. Integrate the reviewed bundle under
`releases/rc6`, the installer's fixed bundle location, before running installer
verification or packaging either platform.

## Select a published firmware bundle for source use

A source checkout retains an older `releases/rc6` bundle. Building the firmware
or running `setup` does not replace it. To use the source installer for a
published release, start with a clean checkout of that release tag and download
`firmware-bundle.zip` plus its SHA256 file from the same release. Check the
checksum before extraction, using the method in [Install](INSTALL.md) with the
firmware bundle's filenames.

Extract the ZIP into a new `firmware-bundle` directory. Its `firmware`, `reports`
and other files are directly inside that directory. Copy its full contents into
`releases/rc6`, then copy `firmware-bundle/approved-release.json` to
`tools/installer/approved-release.json`. Keep the bundle complete; do not mix
files from different releases. Run the source launcher's `verify` below before
using any device command. The approved manifest checks the selected files
against that exact release and host source.

## Source installer setup

Run the commands in this section from the repository root.

This Python environment is separate from the QMK firmware build environment
above. The source launcher needs Python 3.10 or newer. On Ubuntu/Debian install
its system dependencies, then let the launcher create `.venv-ak820-installer`
and install the pinned `hidapi==0.15.0` requirement:

```sh
sudo apt-get install build-essential python3-dev python3-venv python3-tk libudev-dev
./AK820.sh setup
./AK820.sh udev --install
./AK820.sh verify
.venv-ak820-installer/bin/python tools/installer/gui.py
```

The udev command installs the project's device-access rule and reloads udev.
For source use on Windows, install Python 3.10 or newer, then run from
PowerShell in the repository root:

```powershell
.\AK820.cmd setup
.\AK820.cmd verify
.\.venv-ak820-installer\Scripts\python.exe tools\installer\gui.py
```

These commands prepare and start the installer interface; `verify` checks the
release files offline. They do not flash a keyboard. Standalone Windows and
Linux packages are preferred for end users and need no Python setup.

## Native Linux installer

Build the standalone package on Ubuntu 22.04 x86_64 with Python 3.12,
`python3-dev`, `python3-tk`, `libudev-dev`, `libusb-1.0-0-dev`,
`build-essential`, `xvfb` and `xauth`. Install the pinned requirements with the
hidraw backend, then run the packaging regression and builder from the
repository root:

```sh
HIDAPI_WITH_HIDRAW=1 HIDAPI_WITH_LIBUSB=0 \
  python3 -m pip install --no-binary=hidapi -r tools/installer/requirements-build-linux.txt
python3 -B -m unittest discover -s tools -p test_build_linux_installer.py
python3 tools/build_linux_installer.py --output dist/AK820-Linux-x86_64
(cd dist && sha256sum AK820-Linux-x86_64.tar.gz > AK820-Linux-x86_64.tar.gz.sha256)
```

The builder refuses an existing output or work directory. It creates GUI and CLI
applications, verifies their approved inputs, checks frozen hidraw, CLI help,
offline verification and Tk startup under Xvfb, then writes the tarball. These
smokes do not open USB or check live keyboard behavior. See [CI and releases](CI.md)
for how the release workflow supplies fresh firmware and publishes artifacts.

## Windows installer applications

For a new Windows package, build from the reviewed release on native Windows
using Python 3.12 and the pinned PyInstaller 6.16.0 requirements:

```powershell
py -3.12 -m venv .venv-windows-installer
.venv-windows-installer\Scripts\python -m pip install -r tools\installer\requirements-build-windows.txt
.venv-windows-installer\Scripts\python tools\test_build_windows_installer.py
.venv-windows-installer\Scripts\python tools\build_windows_installer.py --output dist\AK820-Windows
```

The command refuses to replace an existing output directory or ZIP. It builds
both applications, checks every approved input's SHA256 inside each full
PyInstaller directory, runs CLI help and offline release verification, then
creates and destroys the Tk interface with `--self-test`. That last check is a
native Tk UI smoke, not an interactive usability check. The output contains
`AK820/`, `AK820-cli/`, `AK820.cmd`, `build-provenance.json`, and
`smoke-report.json`; the sibling `dist/AK820-Windows.zip` contains those full
paths. Review both JSON reports and the ZIP before distribution. The build does
not enumerate USB, test a physical keyboard or flash firmware. OEM references,
personal backups, and runtime sessions are excluded.
GitHub Actions builds and checks every branch push and pull request. Version tags publish the reviewed Windows and Linux packages after the firmware,
Windows and Linux checks pass. Both packages use firmware built by the same Linux
CI run. Tags on commits in main publish the firmware bundle, Windows ZIP and
Linux tarball. See
[CI and releases](CI.md) for triggers, artifacts and the reproducible-build policy.
