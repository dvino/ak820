# Full firmware release qualification, 2026-10-24

## Exact candidate

The full profile retains all base functions and enables NKRO control, modifier
One Shot and the three compact Space Cadet actions. The application IHX SHA256
is `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`.
The permanent CODE identity is
`01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d`.
The image uses 40,043 CODE bytes and 2,637 XRAM bytes. Allocated stack is 162
bytes; 441 main-window and 16 low-window trailing bytes remain.

## Stack and interrupts

[Stack analysis](stack.json) closes every requested root: main uses at most
93 control-stack bytes; timer, USB and LED callbacks use 2, 6 and 2. The
[startup check](startup.json) adds a two-byte main-entry allowance. Each actual
OEM wrapper adds 17 bytes. Bounding all three sources simultaneously adds
61 bytes, so the complete allowance is 156 of 162 bytes, leaving six bytes.

This proof uses normal bank-0 SDCC calls, valid memory accesses and private
non-escaped guard objects. The analyzer validates guard statements and emitted
loads/stores, tracks their ownership through calls, and rejects an ancestor
flag being cleared. It does not use a chosen recursion-depth cap. Fixed USB
callbacks now use direct calls; other finite ROM dispatches are checked against
the exact image. The LED selector masks its table index to four bits.

The [IRQ report](../alpha3-irq-20261024/final/results.json) checks exact OEM
wrappers, all 15 distinct-source orders, all 256 selector inputs, priority/source
writes, masked shared initialization and private allocation. The architectural
premise is MCS-51 in-service/RETI behavior; no number of VS11 priority levels is
assumed. The [architecture contract](../alpha3-irq-20261024/architecture-contract.json)
links the primary Intel manual. Actual interrupt routing and electrical timing
are separate from this instruction-level proof. CPU observations at IRQ entry
are scenarios; the static sum covers arbitrary phase overlap.

Independent review closed startup entry-frame omissions, a short-transfer
masking-check bypass, incomplete source escape detection and a stale priority
limit. Their mutations are regression tests. Final independent checks pass
30 analyzer, six startup and five IRQ tests and reproduce the numeric result.
[CRT CPU observations](../alpha3-stack-20261024/final-startup/cpu.json) cover the
complete deterministic CRT and hostile inherited state before the erase helper.

## Settings and packaging

The [transition witness](../alpha3-transition-20261024/transition.json) pins
both target identities and feature permissions. All 47 settings tests pass.
An actual retained alpha.2 backup passes offline preflight for 498 key and
12 encoder assignments and eight Combo slots, without bypassing core checks.
Fresh backups, physical confirmation, cancellation before erase and failure
stops remain. NKRO mode and pending One Shot state are volatile.

Independent transition review found no blocking defect. The safety gate has
20 passing tests for exact identity, source and evidence binding, stack
placement, unresolved paths, overflow and missing qualification. Its independent
review is complete. The committed safety manifest does not replace the separate
program policy, packing receipt, full regression pass or native package checks.

Fresh offline trial and permanent packing succeeds using local private OEM
references. Recovery bytes exactly match the original application region;
images remain private. The public [receipt](../../../ci/packing-receipt.json)
contains hashes and results only. No USB device was opened or written.

The first base run failed only because an old review-binding fixture supplied
non-JSON bytes as a build report. The new safety binding parses the production
JSON format; the fixture now supplies valid JSON. The failed report and all
28 logs remain in `initial-fixture-failure/`. The corrected focused bundle tests
pass 12 tests; all host tools pass 158 tests. A complete recheck is separate.

The complete recheck passes all 28 base suites and 273 unit tests without skips,
then all 13 supplemental full-profile suites. Image identities remain unchanged.
The final runtime analysis returns zero with no unresolved roots. The
configuration's package command verifies the current source-bound base and
supplemental contracts and the safety manifest before granting eligibility.
The image is eligible for the separately reviewed release pipeline; this is
not a device write or a publication result.

## Publication state

The [independent program review](program-review.md) approves this exact source,
image, policy, receipt and offline evidence for commit and CI reproduction.
All findings are closed. The three native jobs in
[main CI](https://github.com/dvino/ak820/actions/runs/40076916540) passed for
`b17d7c8`. The verified assets from that run were published as
[v0.6.0-alpha.3](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.3).
The duplicate tag run was cancelled after publication; it is not a failed test.
[Publication metadata](publication.json) records all eight downloaded assets.
[Public asset checks](published-assets-check.json) verify their checksums,
official installer authorization, both GUI/CLI input sets and native architecture.
The Linux CLI also passed help and offline verification.

The [device result](device-result.json) records one successful installation from
the published Linux package, exact CODE and manifest readback, two fresh physical
confirmations and verified settings restoration. An earlier confirmation timeout
performed no flash and stopped; another attempt was explicitly authorized.
Typing was reported working. Individual physical feature and encoder cases,
USB timing, LED DMA, cold-start retention, electrical flash faults and manual
GUI interaction remain outside the verification performed here.


## Documentation closeout

Independent final review approves the published-state documentation, asset
checker and recorded evidence. STATUS wording findings are closed in both
languages, and the actual linked MEM confirms 2,637 XRAM bytes. Public guides
separate the released image, installation results and untested physical cases.
The downloaded-asset helper passes after the status commit and preserves the
release's exact policy and image bindings. No blocking findings remain.
