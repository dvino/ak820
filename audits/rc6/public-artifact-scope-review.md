# Public snapshot artifact scope

Date: 2026-10-23. This is a bounded local content review. No USB operation,
build, deletion, commit or publication was performed. Only this report was
written. The existing checkout and private Git bundle must retain the original
history and evidence. The recommendations below apply to a future public copy.

## Decision

Exclude the seven unrelated upstream HEX files and all five historical release
directories from the public copy. Keep the current RC6 source, notices and
reviewed release files. This removes eight old IHX files as well as obsolete
instructions, machine paths and OEM disassembly in the same historical releases.
It does not change the RC6 firmware or installer.

This is a distribution scope recommendation, not a legal finding. It does not
claim that every remaining file is cleared for publication. No external license
claims were researched, and this was not a review of every repository file.

## Exact exclusions

Exclude these seven files from the future public snapshot:

```text
qmk-8051-ak820/util/bootloader_at90usb128_1.0.1.hex
qmk-8051-ak820/util/bootloader_at90usb64_1.0.0.hex
qmk-8051-ak820/util/bootloader_atmega16u4_1.0.1.hex
qmk-8051-ak820/util/bootloader_atmega32u4_1.0.0.hex
qmk-8051-ak820/util/bootloader_ps2avrgb_bootloadhid_1.0.1.hex
qmk-8051-ak820/util/pro_micro_ISP_B6_10.hex
qmk-8051-ak820/util/teensy_2.0_ISP_B0.hex
```

Exclude these historical directory trees, rather than editing their old reports
and invalidating the evidence they record:

```text
releases/rc1/
releases/rc2/
releases/rc3/
releases/rc4/
releases/rc5/
```

The eight IHX files covered by those directory exclusions are:

```text
releases/rc1/firmware/application.ihx
releases/rc2/firmware/application.ihx
releases/rc3/firmware/application.ihx
releases/rc4/firmware/application.ihx
releases/rc5/firmware/application.ihx
releases/rc5/reports/controls/rc5-release-no-callee-v2/ajazz_ak820_vial.ihx
releases/rc5/reports/controls/rc5-release-no-outline-v2/ajazz_ak820_vial.ihx
releases/rc5/reports/controls/rc5-repeat-v2/ajazz_ak820_vial.ihx
```

Do not exclude `releases/rc6/firmware/application.ihx`. Do not delete source
licenses or notices as a side effect of filtering binaries. The separate
private-history/OEM exclusions still apply; this list adds to that boundary.

## Source, notices and dependencies

The seven HEX files belong to AVR bootloader or ISP workflows. The local
`qmk-8051-ak820/docs/isp_flashing_guide.md` identifies the four Atmel DFU images
as factory bootloaders and links their upstream archive; it describes the two
ISP images and the PS2AVRGB bootloader. The Japanese guide also links them.
These guides are provenance pointers, not evidence that the exact matching
source and file-specific redistribution notices are present locally.

The source tree has a GPLv2 `LICENSE` and pinned archive provenance in
`util/ak820-source-provenance.json`. Neither establishes a file-specific source
and notice mapping for all seven HEX files. The targeted local search found
no corresponding ArduinoISP source or source/build recipe for those exact
images. Removing unused binaries avoids needing that unresolved mapping for
this snapshot. It does not establish that the files are unlawful to distribute.

The eight old IHX files have AK820 build reports, sources or historical patches
around them. This review did not reproduce each old build or prove complete
corresponding source for each image. Their main reason for exclusion is that
they are historical outputs, not current installer inputs.

Current dependency evidence:

- `util/ak820_release_manifest.py` selects `RELEASE = 'rc6'` and enumerates
  current host inputs; none of the fifteen files is an input there.
- `tools/build_release_bundle.py` takes one checked build and local OEM
  references, then copies its IHX/MAP/MEM into the new bundle. It does not
  consume those historical IHX or AVR HEX files.
- `tools/build_windows_installer.py` uses the current release manifest and an
  explicit file allowlist. It does not copy the entire source tree or old releases.
- `util/ak820_build_inputs.py` records the compiler dependency closure and
  relevant source/tool inputs; unrelated HEX files are not build sources.
- Targeted searches of the current installer, release builder, package tests
  and combined test runner found no old-release input dependency.

## Historical content and current documentation

The old releases contain machine-specific absolute paths. For example,
`releases/rc1/reports/build-report.json` and `firmware/application.map` record
`/workspace/scratch/...`; RC2 records a different scratch root. These are
confirmed machine paths, not proof of an owner's personal identity or secret.

Old releases also contain literal OEM code fragments. Confirmed examples are
`releases/rc2/reports/audit/D/native-disassembly.txt` and
`releases/rc2/reports/audit/D/rc2-emitted/oem-wrapper-disassembly.log`.
Both include addresses, byte values and decoded instructions from native ROM.
Removing only `.bin` or `.ihx` files would leave these textual fragments.
In contrast, the inspected `recovery-handler-fragments.inc` is C source; its
filename alone is not evidence of raw OEM bytes.

Current `docs/BUILD.md` explains that OEM references are local inputs and are
not copied into releases. Current `docs/TESTING.md` uses a placeholder private
reference path. Keep these instructions. Archived RC3 build/install documents
and RC4/5 manifests describe old reference layouts and should remain private
with their releases, rather than appear as current instructions.

## Checks affected and required follow-up

The current installer/package tests and RC6 integrity checks should remain
available after these exclusions. That is a dependency conclusion from source
inspection, not a new test PASS. Repeat the clean-copy offline suites and the
RC6 bound-hash check after filtering; save the new exclusion list with results.
Do not relabel earlier clean-copy results as checks of a newly filtered copy.

One historical test does need special handling:
`qmk-8051-ak820/tests/ak820_startup/run.py` currently requires both
`--legacy-build` and `--stock-rom`. It loads legacy IHX/MAP and compares old
startup behavior with the current build. RC3 is the documented historical
fixture in archived build instructions. The argument is **not optional** in
the present source. Excluding RC3 means this specific historical comparison
cannot run from the public snapshot alone. Keep its original fixture privately
and supply a private path when reproducing it. Making the argument optional
would be a separate source/test change requiring review; this report does not
make that change. Existing archived evidence remains historical evidence.

Old RC1-5 verification scripts, manifests and hash lists will no longer form
self-contained runnable releases in the public copy. Do not advertise those
old bundles as shipped or reproducible from that copy. Keep their complete
versions in the private archive. Review `releases/HASHES.json` and archived
cross-links when assembling the public snapshot so it does not claim excluded
files are present.

No physical acceptance was repeated here. The lead's existing RC6 readback and
typing evidence remains separate; cold boot remains pending. This report
does not authorize publication or a hardware operation.
