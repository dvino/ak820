# Packaging the SDCC 4.6 build

Date: 2026-10-23

The offline bundle assembler now accepts `--toolchain` and
`--builder-source`. Both paths are relative to the repository root and must
resolve to existing files or directories inside it. The defaults remain
`toolchains/sdcc-4.4.0` and `qmk-8051-ak820/util/build_ak820.py`.

The default toolchain still requires the production builder. Another
toolchain path must contain the six exact SDCC 4.6 executable hashes recorded
in `sdcc46-probe-20261023.md`. It also requires the private builder with SHA256
`4094ceba4c883b70355fb6fefa8a219cb18a0847bfbcb623c1e5833feaf276db`.
Supplying a path does not permit an arbitrary compiler or builder.

The assembler compares the compiler, assembler, builder and dead-code tool
hashes with the original build report. It validates the report's source and
toolchain manifest against the selected toolchain. The independent review
must still bind the exact IHX, MAP, report and host files. No report is edited.
The bundle includes the selected builder at `reproduction/build_ak820.py`;
its size and hash appear in the release manifest. The private builder's
location-specific source-root expression still needs the original staging
layout when reproducing the build.

The installer accepts the old exact file set and that same set with only
`reproduction/build_ak820.py` added. Other manifest files remain rejected.
When the builder is present, the installer checks its bytes against the
manifest and its hash against `builder_sha256` in the build report. Existing
bundles without the builder remain accepted under their existing checks.

For the existing candidate, append these options to the normal assembler
command after an independent review has passed:

```text
--toolchain qmk-8051-ak820/.build/rc6-sdcc46-probe-20261023/sdcc-4.6.0
--builder-source qmk-8051-ak820/.build/rc6-sdcc46-probe-20261023/build_ak820_experimental.py
```

Verification: `python -m unittest discover -s tools -p test_build_release_bundle.py`
passed 11 tests. Fixtures cover the default path, selected toolchain, swapped
executables, changed builder, wrong report hashes, source-manifest failure,
outside paths, artifact binding and a host edit during assembly. The tests
do not execute a compiler or access USB. A read-only call to `validate_tools`
also passed against the existing full SDCC 4.6 build report and staged tools.
`python -m unittest discover -s tools/installer -p test_installer.py` passed
48 tests, including old/new bundle loading, an unknown extra file, corrupted
builder bytes and a valid manifest whose builder disagrees with the report.

No bundle was assembled in this work package. No approval file was written,
and no device was opened or flashed. This change prepares offline packaging;
it does not validate installed firmware or physical keyboard behavior.
