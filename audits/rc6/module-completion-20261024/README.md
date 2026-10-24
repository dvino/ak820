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

Current exact-image runtime bounds: full 162/167, Tap Dance 166/166,
Key Overrides 162/162, QMK Settings 162/166 bytes. Startup and all three
IRQ sources are included. No unknown path is accepted. Full regressions and
the complete profile matrix are in progress at this source checkpoint.

The first base run retained three failures: LeakSanitizer could not inspect
process threads in the restricted environment; the retained host tapping
oracle lacked its empty address-space qualifier; the Combo fixture expected
zero optional Vial tables. RGB passes with ordinary sanitizer settings
outside that process restriction. No sanitizer check was disabled for
acceptance. Further linked fixture work initializes runtime settings and
checks the actual outgoing report when Key Overrides projects it.

No USB, reset, loader or flash command was issued. Static and host/CPU-model
results do not establish physical USB timing, durable flash or power-loss
behavior. Release and installer-transition approval remain separate.
