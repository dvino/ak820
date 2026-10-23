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
uses Ubuntu WSL. The source installer needs Python 3.10+ and its own requirements.
Create the firmware build environment:

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

The default exact instruction outlining and audited callee-save list have
comparison switches `--no-outline` and `--no-callee-saves`. ABI changes require
new stack/interrupt evidence. Build configurations must not run concurrently
in the same source tree because Make uses shared generated files.

Run [offline tests](TESTING.md), obtain independent review, then assemble a
release from the repository root with `tools/build_release_bundle.py --build-dir .build/local-1
--review docs/REVIEW.md --oem-reference-dir /path/to/private-oem-references
--toolchain toolchains/sdcc-4.6.0 --builder-source qmk-8051-ak820/util/build_ak820.py
--output releases/rc6-new`.
The example reference path must point to the user's own local exact pair. The
review must bind the exact IHX, MAP, build report and host inputs. Assembly
does not approve hardware operations. A changed source or host input
invalidates previous evidence. After review, integrate the fresh bundle under
`releases/rc6`, the installer's fixed bundle location, before running installer
verification or Windows packaging.

## Windows installer applications

The current checked output is `dist/AK820-sdcc46-breathing-20261023/`, with complete
`AK820/` and `AK820-cli/` folders. Each needs its full directory; the EXE alone
is insufficient. The apps include Python. Source wrappers require Python 3.10+.

Build command: `tools/build_windows_installer.py --output dist/AK820-sdcc46-breathing-20261023`.
Build and package evidence: `host/runs/20261023-sdcc46-windows.json`.
CLI help, offline verify and GUI self-test passed. The
[independent artifact review](../audits/rc6/sdcc46-release-review-20261023.md)
records the package checks. See [status](STATUS.md) for device results.

Earlier GUI folders and `dist/AK820-RC6-Windows-20261023.zip` are superseded.
Do not use them for this candidate. No current portable ZIP or public download
has been published. The local ZIP is `dist/AK820-sdcc46-breathing-20261023.zip`.
OEM ROMs and personal backups must stay out of app output.
