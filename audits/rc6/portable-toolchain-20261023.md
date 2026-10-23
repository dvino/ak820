# Portable compiler setup

Date: 2026-10-23

## Local setup

The repository no longer needs to carry the SDCC executables as source files.
The pinned installers place them under the ignored repository-local
`toolchains/` directory. Neither installer changes the system `PATH` or
system compiler. The 4.4 installer now targets `toolchains/sdcc-4.4.0`; the
new 4.6 installer targets `toolchains/sdcc-4.6.0`.

On Windows, the 4.6 installer downloads the archive over HTTPS from SourceForge
or accepts a local archive with `--archive`, then uses the WSL distribution
named `Ubuntu` to extract and check the Linux executables. On Linux it runs the
same checked extraction directly. The archive must be exactly 23,853,152 bytes
with SHA256
`f6b929c62ed3082a26087885e0f1f9bf41878602ef1f57e40b11b4a01bf4f366`. The
installer checks archive paths before writing files, checks six executable
hashes, asks SDCC to report its version, and writes an installation receipt.
An existing unreceipted target is left alone and causes setup to stop.

Use the downloaded installer on a connected machine with:

```text
python tools/install_sdcc46_toolchain.py
```

To bootstrap from the already staged archive without network access:

```text
python tools/install_sdcc46_toolchain.py --archive qmk-8051-ak820/.build/rc6-sdcc46-probe-20261023/sdcc-4.6.0-amd64-unknown-linux2.5.tar.bz2
```

The repository's production builder now defaults to SDCC 4.6.0. Its
`--sdcc-version` option accepts only `4.4.0` or `4.6.0`; the selected version
must match the compiler output. Pass the local compiler path explicitly when
building:

```text
python qmk-8051-ak820/util/build_ak820.py --sdcc-version 4.6.0 --toolchain toolchains/sdcc-4.6.0
```

For the 4.4.0 comparison build, use
`--sdcc-version 4.4.0 --toolchain toolchains/sdcc-4.4.0`.

## Verification

The offline 4.6 install completed from the archive already staged in the QMK
probe directory. It installed at
`toolchains/sdcc-4.6.0` with SDCC 4.6.0 #16555 (Linux). The receipt records
4,399 validated archive members and 278,045,275 uncompressed bytes. The six
executable hashes matched the release pins in
`tools/build_release_bundle.py`. No system compiler was modified. This was a
toolchain installation and version check, not a firmware build or device test.

The synthetic offline installer suite passed 8 tests. It covers local archive
bootstrap and repeat installation, archive size and hash mismatch, duplicate
members, traversal and unsafe links, and the SourceForge redirect allowlist.
The builder selection suite passed 3 tests. It checks both allowed versions,
rejects cross-version selection, and checks the CLI's 4.6.0 default. These
tests did not build firmware or access USB.

The 4.4 setup script was not rerun after its target path changed. The
pre-existing `toolchains/sdcc-4.4.0` files on this PC predate its new local
installation receipt; the installer intentionally refuses to replace such a
directory. A clean machine can install it to the empty local target. Existing
4.4 build evidence remains tied to the compiler hashes and commands recorded
in the earlier audits.

## Remaining portability work

The Windows installer currently assumes an Ubuntu WSL distribution is
available under that exact name. The archive is Linux amd64, so another
platform needs a Linux or compatible WSL environment. QMK's Python environment
and other host build tools still need their own setup instructions.

Release packaging accepts the existing pinned private SDCC 4.6 builder and
the current production builder at its exact repository path. The selected
build report must still match the builder and compiler hashes, its source
manifest must validate, and the independent review must bind the build and
host files. A focused test covers production-builder acceptance and rejects a
changed report hash. No release bundle was assembled or changed here.

The packaged `reproduction/build_ak820.py` also computes its source root from
`Path(__file__).resolve().parents[2]`. That location changes when the builder
is placed in a release bundle, so the packaged script cannot be invoked in
place as a general reproduction command. Before claiming portable release
reproduction, add an explicit source-root option to the production builder,
bind that version in the release manifest, and test it against the extracted
release source tree.

No release bundle was assembled or repacked. No device was opened or flashed.
