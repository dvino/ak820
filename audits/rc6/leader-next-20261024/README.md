# Compact Leader and report pointers

The continuation adds compact Leader, reduces keyboard-report pointer cost
and fixes clean short-call rebuilds. Firmware and tests are frozen at
`d04290b799b1921a55f020ee3cfe041199fae244`. All 18 named profiles and 20 build
variants pass their exact-image runtime gates and complete offline suites.
The published alpha.3 image, installer policy and installed state are unchanged.

## Changes

- `full-leader` selects one of the 16 existing Vial macros with physical
  `QK_LEAD` followed by `1`–`9`, `0`, or `A`–`F` within 300 ms. Macro data is
  edited in Vial. Prefix/selector ownership, cancellation and idle dispatch
  are bounded. See the [implementation review](leader.md) and
  [user guide](../../../docs/COMPACT-LEADER.md).
- Report helper parameters use their actual XDATA address space on AK820
  SDCC. The `full` image saves 34 CODE bytes and seven XRAM bytes, while its
  complete stack bound remains 160/166. Other targets retain their pointer
  types. See the [optimization review](optimization.md).
- Short-call rebuilds accept real empty directories recreated by the
  diagnostic linker. Existing files, symbolic links and special objects still
  stop the operation. Eighteen focused tests cover the copy behavior.

Six layers, 16 Vial macro slots, 8192 macro bytes, eight two-key Combos, NVM
schema `0x082002` and the loader/recovery path are preserved. Broader Leader
sequences and configurable dictionaries are absent. Tap Dance, Key Overrides,
runtime QMK Settings and the remaining Magic variants remain planned work.

## Verification

The [final matrix](final/README.md) retains measurements, exact image identities
and complete raw builds. Each image passes 28 base suites and 273 unit tests
with zero skips, plus 16–26 supplemental suites. The runtime gate
runs first and closes foreground calls, CRT startup and all enabled IRQs.
All 15 distinct-source interrupt orders and 256 LED selectors pass for every
image. The minimum stack margin across the matrix is 1 byte.

Leader's 26 linked cases cover all selectors, expiry, wrap, preheld releases,
cancellation, a pending first slot, encoder exclusion and real macro output.
A nonempty macro sends Shift+Z while One Shot remains queued for the next
physical key. The extended-macro case checks idle-tail dispatch with a physical
key held across interpreter callbacks.

Initial isolated failures, rejected optimization probes and their corrections
are retained in [probes.json](probes.json). The final matrix uses the normal
sanitizer configuration with no external overrides. The existing bounded
fixture retains its own leak-check exception; that fixture was not changed.
Earlier matrices describe
their earlier frozen source and cannot qualify this source.

## Review and limits

Independent source and candidate-evidence review closed the three Leader
findings described in [leader.md](leader.md): SDCC static-argument overwrite,
buffered Combo ordering and replacement of a pending slot. Report ABI and
short-call behavior also passed independent review.

Final independent review reran the full verifier and passed all 20 records.
All 60 resource-table rows across the matrix and English/Russian budget guides
match the machine records. All 20 delay-ABI reports have seven passing cases;
compiler and simulator hashes match the pinned binaries. No firmware or test
source differs from the freeze. The normal sanitizer wording and relative
documentation links were corrected. No finding remains open for this offline
matrix, documentation and evidence package.

The static proof and CPU fixtures do not establish physical keyboard timing,
USB/flash silicon behavior or power-loss recovery. No device command, release
publication, flash or settings change occurred. The full repository archive
preserves the source, evidence and Git history for continuation.
