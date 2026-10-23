# External dependency plan

2026-10-23. Dependency implementation and verification for
`ajazz/ak820:vial`. No files were removed or changed under `lib/lufa/`; no
firmware build, USB access or release edit was performed.

## What the current tree contains

`qmk-8051-ak820/` is the project's maintained QMK-based source tree. It came
from the `vuhuycan/qmk-8051` archive at commit
`43efac45bff7a793719b050614a5dc5b80307e5f` (recorded archive SHA256
`b8f3d7215f4ab290257dc103145f55fe6e423d40730ab352697c30eceafc4df3`). The
source provenance file says AK820 port changes are included and no Git
checkout metadata is present. The AK820 keyboard, CH555 USB path, platform
code, build scripts, and test helpers contain project-maintained changes. This
tree must not be replaced at build time by the unmodified upstream archive.
The pinned archive is a base for provenance, not a substitute for the current
source.

There is no complete checked-in patch series or recursive current-source hash
manifest that reconstructs every change on top of that archive. The RC6 build
report has SHA256 values for its 465 recorded inputs, but that is not a hash of
every file in the trimmed source tree. Therefore an exact clean patch from the
upstream archive is not yet available. Before moving this maintained fork out
of the AK820 checkout, save a recursive source manifest, compare it to the
pinned base archive, and record the changes as reviewed commits or a patch
series in the separately maintained fork. Do not treat a matching build-input
manifest as proof that all source files match.

`lib/lufa/` is third-party source, with its source pin recorded as `qmk/lufa` commit
`549b97320d515bfca2f95c145a67bd13be968faa` and archive SHA256
`01a62a2258dc4fe574290ce5ccc3f947d4e101141a228cc927ae28e58a7bec23` in
`util/ak820-source-provenance.json`. The source tree itself is ordinary files,
not a Git submodule. I fetched and verified the pinned codeload archive against
that SHA256. The twelve LUFA headers and license recorded below match the
archive byte for byte. The complete current directory does not: it has 22
local-only files under the unpacked Android host-app output directory and is
missing the upstream `AndroidHostApp.zip`. No common file path differs in
content. The installer therefore refuses to replace or merge the current
directory. Its default offline check passes because the build's required
headers and license match. The current tree cannot be called an exact copy of
the pinned archive. The local-only files are under
`Demos/Host/ClassDriver/AndroidAccessoryHost/AndroidHostApp/AndroidHostApp-unpacked/`:
`.classpath`, `AndroidManifest.xml`, `bin/AndroidManifest.xml`,
`bin/LUFA_AOA_Test.apk`, `bin/classes.dex`, `bin/jarlist.cache`,
`bin/resources.ap_`, `gen/com/example/lufa_aoa_test/BuildConfig.java`,
`gen/com/example/lufa_aoa_test/R.java`, `libs/android-support-v4.jar`,
`project.properties`, `res/layout/activity_main.xml`, `res/menu/main.xml`,
`res/values-sw600dp/dimens.xml`, `res/values-sw720dp-land/dimens.xml`,
`res/values-v11/styles.xml`, `res/values-v14/styles.xml`,
`res/values/dimens.xml`, `res/values/strings.xml`, `res/values/styles.xml`,
`res/xml/accessory_filter.xml`, and
`src/com/example/lufa_aoa_test/MainActivity.java`. The archive-only path is
`Demos/Host/ClassDriver/AndroidAccessoryHost/AndroidHostApp/AndroidHostApp.zip`.

The saved RC6 build reads twelve LUFA headers. It does not compile LUFA's AVR
USB stack: the board uses the maintained CH555 USB implementation. One
additional compatibility header under
`tmk_core/protocol/ch555/lufa_utils/` includes those LUFA declarations and
belongs to the maintained fork, so it should remain with that source.

The four files in `lib/ch555/` carry WCH copyright notices. The provenance
file does not identify a separate WCH repository or archive; it only places
them inside the pinned `qmk-8051` source archive. Keep these notices. Until a
separate vendor source and license are verified, retain their source with the
maintained fork and record their individual hashes in its source manifest.
Do not claim that the qmk-8051 archive proves the original WCH source version.

The current upstream `.gitmodules` lists ChibiOS, V-USB, printf, Pico SDK,
LVGL, and `sdcc_MCS51_rm`, although those paths are absent after the source
trim. LUFA and CH555 are not declared submodules. These stale declarations
must be removed or replaced with the actual dependency manifest before a clean
checkout can use submodule initialization as its setup instructions.

## Inputs required by the saved RC6 firmware build

The RC6 build report records 465 inputs. It contains 12 files under
`lib/lufa/`, one LUFA compatibility header in the maintained CH555 path, four
`lib/ch555/` files, 96 QMK Python files, 94 data files, one pinned build
requirements file, and 29 SDCC 4.6 toolchain files. The 96 Python and 94 data
records are the build-input collector's conservative QMK source/data set;
they do not mean every command module or data file is imported by the AK820
firmware itself. QMK startup and generator commands use this source tree too,
so trim it further only with their own import tests.

The LUFA files in the saved build closure are:

| File | SHA256 in RC6 build report |
| --- | --- |
| `lib/lufa/LUFA/Common/Architectures.h` | `20cd56152f9b5ab052462a5cbf00e99d49688d709dd19dd93b217ae26c3994b3` |
| `lib/lufa/LUFA/Common/Common.h` | `096187c481661ae61a599605eebeb9c2086d76726cea4494531634aa504a42c4` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/AudioClassCommon.h` | `2471292efc68b86a5c12f78cafbe72bfbd9db98aebd5d9cdddc656c9d85530b8` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/CDCClassCommon.h` | `8af709ba99b2b5d54d3448922e609fb376aef1572e22d5ef0fa7107248e69673` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/HIDClassCommon.h` | `93984216c27929687eb00349c708c516a1e21c9aaf0bb1a777a53ed403fd5014` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/HIDParser.h` | `332e6447ab18ffc71116a4f6d3232684e0fc59f7b247ed9ce86715892984a62c` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/HIDReportData.h` | `8887facdc7b85b69804aa20709075eb0472ba02d3290e9e45cfa5afe5d92c5e6` |
| `lib/lufa/LUFA/Drivers/USB/Class/Common/MIDIClassCommon.h` | `e95ba0af8ed6f008f35bd8fd46efb041ab45ba658c0590e10b98d330072a5266` |
| `lib/lufa/LUFA/Drivers/USB/Core/Events.h` | `d3b131927c399b52294e2fb8816b7514595bea076e9f43c439e0014507a43cdd` |
| `lib/lufa/LUFA/Drivers/USB/Core/StdDescriptors.h` | `04de70083c58520e5e06a6d61904e7cb096143f3fb43060de2d9a102731b1990` |
| `lib/lufa/LUFA/Drivers/USB/Core/USBController.h` | `bda07947e9551b37df498e5b3bbc461d14d6b6dbe3eeb17e5c4f4f1f52e21875` |
| `lib/lufa/LUFA/Drivers/USB/Core/USBMode.h` | `4bf9d2fdda3592f478fc81a4bd5bab99187c6169aa972f3994c141669d117d5d` |

The LUFA license is `lib/lufa/LUFA/License.txt`, a permissive license with
conditions requiring copyright and permission notices to be retained. If the
complete LUFA tree is removed, fetch only the twelve headers above and this
license for the firmware build. Keep the compatibility header with the
maintained source. Before dropping anything else, search host tests and QMK
startup paths for includes outside the firmware dependency closure.

`lib/ch555/` contains vendor-marked WCH code. The project license guide says
existing third-party notices govern these files; do not apply the root
GPL-3.0-only statement to them. Preserve the WCH notices and the applicable
upstream QMK license files. The exact license grant for the WCH-only files
still needs a verified source or vendor license record.

The Python build requirements are pinned by version in
`requirements-ak820-build.txt`, and the source provenance file records that
file's SHA256 as
`fd5e2d8288a1d99c1775d456898313c788070b70e411bb539b9219aea396d33c`.
They are external packages, not source to copy into this repository. The
requirements file has no per-wheel hashes, so it does not yet identify exact
download bytes. Generate a platform-specific wheel lock with source URL,
version, wheel filename and SHA256 for each package; preserve license and
notice files from the selected wheels in the dependency cache and release
notices. Do not silently resolve newer versions.

The saved build uses SDCC 4.6 from the separate local experimental toolchain.
The source provenance file instead records the regular SDCC 4.4 archive
`sdcc-4.4.0.tar.bz2`, SHA256
`7cb4c96bd774f95e8032746e6808b59f3a8e2b3e7b4c72ac566bb67beeacff80`, plus
compiler and assembler hashes. The SDCC 4.6 probe report is the authority for
the RC6 experimental build; the 4.4 values must not be reported as its
toolchain. Keep both toolchains outside the source checkout and identify the
compiler, assembler, headers, libraries and archive hashes separately in the
lock/report for each build flavor.

## LUFA installer and external-cache mechanism

`qmk-8051-ak820/dependencies/lufa.json` now records the LUFA repository,
immutable revision, archive URL and SHA256, archive root, local destination,
license and hashes of the twelve build headers plus license. The
`tools/install_lufa_dependency.py` command defaults to an offline, read-only
check of those thirteen files. On a clean checkout, `--fetch` downloads the
locked archive; `--archive <file>` uses a supplied archive. Both paths verify
the archive and locked file hashes, reject traversal and links, and only install
when the destination is absent or already byte-for-byte identical to the full
archive. A divergent existing directory is preserved and reported; the tool
does not merge or overwrite it. The archive is fetched to a temporary file and
is not retained in the repository.

I fetched the pinned archive during this work. Its archive SHA256 matched the
lock, and the twelve locked headers plus `LUFA/License.txt` matched the
existing files. The install attempt stopped at the full-tree comparison and
made no changes because of the 23 path differences listed above. The seven
offline installer tests passed, including archive hash mismatch, required-file
hash mismatch, traversal, symlink, repeat install and divergent-target
preservation. No firmware build was run.

Use one checked-in lock manifest for external inputs, but keep downloaded
content outside Git, for example in `%LOCALAPPDATA%\AK820\deps\<name>\<sha>`
or a caller-supplied `AK820_DEPS_CACHE`. Each entry should state the exact
source URL, immutable commit or package version, archive SHA256, archive root
directory, required paths, required file hashes where available, license path
and intended cache destination. Separate source dependencies, Python wheels
and compiler toolchains into distinct entries and build flavors.

The setup command should have two explicit modes. `--fetch` downloads to a
temporary file, checks the archive hash before extraction, checks the required
file hashes, then installs into a new hash-named cache directory. Default and
`--offline` modes only read the cache and fail with the missing dependency,
expected pin and fetch command. Never fetch the current branch or update a
pin automatically. Cache entries are immutable; a changed pin creates a new
directory. The build takes `--deps-cache` (or reads the cache environment
variable) and includes external file paths and hashes in its input report.

For the maintained QMK-derived source, make a separate source repository or
Git submodule that points to the maintained AK820 fork commit. Keep the fork's
Git history and third-party base metadata there. The root project should pin
that commit and the supported board/release configuration. Do not fetch the
unmodified `vuhuycan/qmk-8051` archive in place of this fork. A submodule is
only appropriate after the current tree has been converted to the separate
repository and its history, local changes and release build have been
verified. The current tree has no nested `.git` metadata, so this conversion
cannot be safely inferred from the archive pin alone.

## Removal sequence and checks

1. Save a recursive file/size/SHA256 manifest for the current trimmed QMK
   source and the exact RC6 release inputs. Compare `lib/lufa/` with the pinned
   archive before calling it byte-for-byte unchanged. Save a separate diff or
   patch series for every AK820-maintained change against the QMK base.
2. Create the external dependency lock and cache checker. Include the exact
   LUFA subset above, its license, Python wheels and each supported toolchain.
   Keep CH555 vendor code and compatibility glue with the maintained source
   until their origins and split are evidenced.
3. Move the QMK-derived maintained source to its own pinned repository only
   after confirming complete history/diff recovery. Replace stale `.gitmodules`
   declarations with the actual pin mechanism. Do not prune the QMK source to
   only the 465 firmware input records: QMK CLI startup, generators and test
   helpers need files outside that report.
4. Run cache verification offline from an empty source checkout. Then run QMK
   startup/generator checks, the saved SDCC 4.6 build into a fresh output
   directory, compare the RC6 IHX and binary bytes, and run the offline AK820
   regression suites. If input paths change, update build-input validation to
   accept only the locked external roots and record their hashes.
5. Keep code, dependency documentation, license notices and regenerated
   source/build reports together. Report build results separately from host
   tests and physical keyboard behavior.

This work independently checked the LUFA archive and the thirteen locked
files only. It did not verify Python wheels, the experimental toolchain, or the
complete maintained QMK fork against its base archive. It does not establish
that an externalized checkout builds. No device write, update, reset,
bootloader transition or flash was performed.
