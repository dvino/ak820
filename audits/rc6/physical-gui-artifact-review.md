# RC6 physical update GUI artifact review

Date: 2026-10-23. Independent offline review of the standalone Windows GUI
and CLI produced for the physical-confirmation update flow. No firmware build,
USB access, device command, reset, loader transition or flash was performed.

## Result

PASS. The approved RC6 installer manifest SHA256 is
`56095cb4720d6e20ea151c6596d465974169d0e338b54a3cebbefeb817ff4949`, matching
`tools/installer/approved-release.json`. The build result at
`host/runs/rc6-physical-gui-build-result.json` records exit code 0 and zero
USB operations.

The output files are:

| File | Size | SHA256 |
| --- | ---: | --- |
| `dist/rc6-physical-gui-20261023/AK820/AK820.exe` | 1,943,029 | `4110d7065cf9f063d356ef834bbda5d6883fd407c7d1082058ad5c169224cb05` |
| `dist/rc6-physical-gui-20261023/AK820-cli/AK820-cli.exe` | 1,782,602 | `35faf323ae1225857e7cbdf35a60abbb9b0b555fd5eb89267e006e9a7c6ea723` |

I compared each of the 26 allowlisted source files (16 host files, eight
release files, the release manifest and the installer approval) against the
copy inside each output bundle. All 52 size and SHA256 comparisons matched.
The bundles contain no `.bin` files, `stock-full.bin` or
`native-installed.bin`. The included `firmware/application.ihx` is the
approved RC6 application image, not a personal OEM ROM.

The packaged CLI `--help`, `verify` and `update-prepared --help` commands each
returned 0. The GUI `--help` and hidden `--self-test` each returned 0; the
self-test creates and destroys the window without USB access. These checks
confirm command startup and package verification, not the visual layout or
physical keyboard behavior. The GUI source imports the bundled `i18n.py` module;
the source-level RU/EN behavior and localized update progress are covered in
`audits/rc6/physical-update-review.md`.

The separate host reports record the promoted seven-suite base run as PASS in
`host/runs/rc6-physical-gui-base-tests-after-promotion.json`, and the update
review records its installer, packaging and firmware-package test results.
This report independently checked the standalone artifacts and smoke commands;
it did not rerun those suites.

No visual inspection of an interactive window was performed. This review does
not establish device detection, physical Esc + left Control recognition,
loader entry, erase behavior, firmware installation, typing, encoder behavior,
durable settings, or power-loss persistence. The installer must still be
started by an owner who has prepared alternate input and stable power; this
artifact review does not authorize a live update.
