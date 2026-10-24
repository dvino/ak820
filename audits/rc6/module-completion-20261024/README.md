# Firmware module completion

Input is the full Git archive `ak820-web-os-macpc-20261024.tar.zst`,
415,002,680 bytes. Work starts from `e3ad29c`, retaining the accepted source,
release evidence and history. Published and installed alpha.3 is unchanged.

## Scope

Three independent development profiles add compact Tap Dance, compact Key
Overrides and runtime QMK Settings. Each retains the full base, six layers,
16 macro slots, 8192 macro bytes and eight Combos. Schema03 reserves separate
page-contained extension records without moving the existing regions.
Legacy profiles retain schema02. No all-extension combination is offered.

Host commands validate typed fields, exact image/profile capability, replies,
getters and full durable NVM neighbors. Backups preserve inactive stored data
and reject an impossible restoration before any write. Migration to schema03
is explicit; downgrade to schema02 is rejected. The catalog exposes stored and
enabled capabilities separately and requires complete exact-image evidence.

The desktop contract is in [the handoff](../../../web/docs/FIRMWARE-HANDOFF.md).
This work does not implement the desktop application or extend the installer
release allowlist.

## Source and review

[Independent review and finding closure](review.md) records source decisions.
Failed size probes and earlier focused linked results are retained under
`probes/`; they are diagnostic evidence, not final qualification.

## Final qualification

All 24 named profiles and 26 linked variants pass fresh runtime checks. Four
exact images pass 28 base suites and 276 unit tests without skips each, plus
90 supplemental suites. The [final matrix](final/README.md) retains complete
raw builds for those four images and all compiler/runtime witnesses for the
other 22. Each image passes all 15 distinct-source IRQ orders and 256 LED
selector values. Unknown foreground paths are not accepted.

Current bounds: full 162/167, Tap Dance 166/166, Key Overrides 162/162 and
QMK Settings 162/166 bytes. The two zero-margin profiles require a new proof
for every change. The main CODE window has only 20 trailing bytes in KO.

Firmware inputs remain `ac48c65`. Full qualification uses `147508e`, with only
host/CPU fixture and audit follow-ups. Every compiler input is independently
bound to the frozen Git blobs; original build/qualification metadata is
preserved. Other profiles receive runtime-only requalification in this change.
The generated development catalog contains exactly the four full-regression
images and retains false release, write and flashing permission fields.

The first base run retained three failures: LeakSanitizer could not inspect
process threads in the restricted environment; the retained host tapping
oracle lacked its empty address-space qualifier; the Combo fixture expected
zero optional Vial tables. RGB passes with ordinary sanitizer settings
outside that process restriction. No sanitizer check was disabled for
acceptance. The corrected shared fixtures initialize runtime settings and check the actual
outgoing report, including its callback pointer, when Key Overrides projects it.
The normal full run also retained an initial restricted-environment LSan failure;
its complete escalated rerun passed with unchanged sanitizer options.

No USB, reset, loader or flash command was issued. Static and host/CPU-model
results do not establish physical USB timing, durable flash or power-loss
behavior. Release and installer-transition approval remain separate.
