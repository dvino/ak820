# RC6 resumed Windows artifact review

Date: 2026-10-23. Independent artifact reviewer; no implementation authorship.
Scope: exact dist/rc6-resume-20261023 Windows output, offline only.

Result: PASS for the checks below; no correctness findings in this bounded artifact review. This is not hardware validation, authorization to flash, or publication approval.

## Exact identities

Approved release manifest SHA256: 2b99a807b6aa3cfc8fda224c9116de246430f7a42ff5a6a37195730a914c1ae6.

| Executable | Bytes | SHA256 |
| --- | ---: | --- |
| AK820/AK820.exe | 1911942 | 58151123457191b4624686799866f682850cb400c8fb2dbdf897d3562e6579b0 |
| AK820-cli/AK820-cli.exe | 1775861 | ef954206c270d7eb8559ab6e75d04f1ff7ac4b7251fd00acd4ba3679006bee11 |

For each application's _internal, independently compared all 25 project files against current promoted inputs: 15 HOST_FILES, eight release payload/review files, release manifest, and exact approval JSON. Both copies matched every byte by SHA256. No unexpected project files existed under packaged releases/, tools/, or qmk-8051-ak820/. The manifest binds the listed payload sizes and SHA256; these are the reviewed release bytes.

## Executable checks

Fresh Python subprocess execution, captured process exit code (not PowerShell stderr classification):

- AK820-cli.exe --help: exit 0.
- AK820-cli.exe verify: exit 0; reported matching release and independent approval, hidapi not loaded, USB not opened.
- AK820.exe --self-test: exit 0, empty stdout/stderr.

These independently reproduce the three successful results in host/runs/rc6-resume-windows-smoke.json. The build log's PowerShell NativeCommandError classification of redirected INFO stderr does not override these executable return codes.

## Private-image exclusion

Scanned every file in this fresh output (1,219 files; 54,505,006 bytes), including executables, for complete exact byte sequences of eight distinct private binary images. Inputs were the external OEM archive manifest's referenced images, evidence/oem-backup/before-full-rom.bin, all six host/runs/20261023-rc6-final-ready/*.bin images, and both read-only encoder/resume ROM captures. All expected private source files existed. No complete private-image bytes occurred in the output. No stock-full/native-installed/before-full-rom/restore-native/readback/rom.bin filenames occurred. No archive or captured bytes were copied into this report.

This establishes exclusion of these full images and unexpected project files; it does not claim that all short OEM-derived sequences are absent. The reviewed runtime intentionally retains its documented 87-byte erase helper. Compression or arbitrary transformed private content was not exhaustively decoded; allowlisted copied project content and exact hashes constrain the packaged inputs.

No USB enumeration, device open, reset, bootloader transition, firmware write, flash, commit, or publication was performed. GUI interactive workflows, physical keyboard behavior, power-loss recovery, and cold boot remain untested by this artifact check. Source/documentation review remains the frozen review in docs/REVIEW.md; root owns subsequent current-state documentation updates.
