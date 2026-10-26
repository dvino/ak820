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
python3 -m venv qmk-8051-ak820/.venv
qmk-8051-ak820/.venv/bin/python -m pip install -r qmk-8051-ak820/requirements-ak820-build.txt
qmk-8051-ak820/.venv/bin/python tools/configure_firmware.py build \
  --profile main \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python \
  --parameter-spills-context /path/to/reviewed-context.json \
  --build-dir qmk-8051-ak820/.build/local-1
```

For a control build with SDCC 4.4, install it with
`python3 tools/install_sdcc44_toolchain.py` from the repository root, then use
`--sdcc-version 4.4.0 --toolchain ../toolchains/sdcc-4.4.0 --profile standard`
in the QMK directory. This explicitly selects a historical control profile;
the current default `main` enables short calls, which require SDCC 4.6.0.
Keep each compiler local and out of Git.

The context path above is a required local input, not a file supplied by the
repository. It must bind this source, pinned tools and protected interrupt
modules; keep its seed evidence unchanged. The [CI producer](../tools/build_ci_profiles.py)
creates fresh per-profile context for the ten-profile build path. A missing or
stale context stops the current build. See [Build profiles](BUILD-PROFILES.md).

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

## Feature profiles

The [profile catalog](profiles/README.md) defines ten fixed compositions with
`main` as default. All ten use schema `0x082003`. The command above selects the
audited pass30 chain: compressed defaults, short calls, NVM read/update and
keymap-word ASM, parameter/register save removal, tail sharing and outlining
with a 400-helper limit. Inspection checks exact flags, sources, pinned tools
and every saved transform proof. Ordinary XRAM is `[0x440,0x1000)`; the preceding
64 bytes remain reserved for flash staging.

The configurator checks placement and the exact-image foreground, startup and
interrupt bounds before full offline regressions. Source profiles and
unmeasured catalog rows do not qualify an image. See the [module matrix](MODULE-MATRIX.md)
and [Status](STATUS.md) for the distinction between source, qualification and
published artifacts. Published beta.1 on 2026-10-25 remains a nine-profile
catalog with standalone installers for its exact `work` image; this description
does not announce beta.2 publication or device validation.

The build uses the compact instruction outliner with a fixed opcode and module
allowlist. `--no-outline` and `--no-callee-saves` provide comparison builds.
Outlining changes the linked image and is not a runtime feature. Savings from
one image do not predict another profile because shared code and packing
interact. ABI changes require new stack and interrupt evidence. Do not run
build configurations concurrently in one source tree because Make uses shared
generated files.

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
  --output dist/local-main-bundle
```

`docs/REVIEW.md` indexes review evidence; it is not the exact-build approval
record. Bundle assembly does not authorize device operations. A changed source
or host input invalidates earlier evidence. Current installer selection uses `tools/installer/profile-catalog.json`. Each
profile needs its complete approved bundle under `releases/beta2/<profile>`,
including its own `approved-release.json`. The all-profile CI assembler writes
these bundles under `dist/ci-firmware/profiles`; packaging stages them at the
selected paths. Missing or mismatched approval blocks packaging.

## Published source releases

For published beta.1, use a clean checkout of its exact tag and follow that
tag's installation instructions. Its `releases/rc6` layout and single `work`
installer are historical. Do not mix that bundle or its approval with current
host code or a different profile. Current source verification requires the
selected profile's complete approved inputs; building alone does not supply them.

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
GitHub Actions prepares all ten profiles through `tools/build_ci_profiles.py`.
The all-profile assembler checks independent policy and exact-image evidence
before writing `dist/ci-firmware/profiles`. Windows and Linux packages must use
those same approved bundles. See [CI and releases](CI.md) for publication gates;
a source change or a local test does not publish a release.
