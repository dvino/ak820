Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-25. [v0.6.0-beta.1](https://github.com/dvino/ak820/releases/tag/v0.6.0-beta.1)
is published. Its standalone Windows and Linux x86_64 installers install `work`.
The release also includes the nine-profile compatibility matrix, exact-image
capabilities, bilingual descriptions, SHA256 files and English/Russian installation guides.
Only `work` is approved for installation; the other eight profiles remain candidates.

All three [native CI jobs](https://github.com/dvino/ak820/actions/runs/40137874411)
passed for source `bef20f8`. Downloaded public files match all 16 published asset
hashes. Both GUI/CLI payloads match the same approved firmware bundle; Linux
CLI help and offline verification also pass locally. See the
[publication record](../audits/rc6/beta1-release-20261025/publication.json),
[download checks](../audits/rc6/beta1-release-20261025/published-assets-check.json)
and [independent package review](../audits/rc6/beta1-release-20261025/native-review.md).
The duplicate dev and tag runs were cancelled after selecting the successful
same-source main run; neither cancellation is a failed firmware test.

## Work beta

The exact IHX SHA256 is
`652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880`.
Permanent packed CODE SHA256 is
`a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10`.
The image uses 40,386 CODE bytes and 2,676 XRAM bytes, with 22 trailing bytes
in the main window and 92 in the low window. The control-stack bound is
99 foreground + 2 entry + 61 interrupt bytes: 162 of 165, leaving three.

The source installer uses an independently assembled retained `work` bundle.
Published native packages contain the CI rebuild of the same exact IHX.
The fresh CI run passed 28 base suites, 291 unit tests without skips and all
30 profile suites. Local qualification reused the passed base results and
repeated all 30 profile suites after two release-asset tools changed during
the initial phase. The initial source-change stop and all logs are retained.
See [acceptance](../audits/rc6/beta1-release-20261025/acceptance.md) and
[current qualification](../audits/rc6/beta1-release-20261025/current-work-qualification.json).

Offline packing and a retained alpha.2 backup preflight passed. Host models
cover alpha.3-to-work settings transfer, both encoder directions and downgrade
rejection. No beta device operation was performed. Physical USB timing, LED DMA,
real flash faults, power-loss behavior, retention after power cycling and manual
GUI workflows remain untested. The [release safety manifest](../ci/release-safety.json)
binds the exact stack, startup, interrupt and settings-transition evidence.

## Firmware catalog

The desktop catalog contains nine curated profiles. `work` is the default and
adds Leader, Dynamic Macros and companion-controlled OS indication to the
common functions. Mac/PC, Mouse Keys and Auto Shift are not enabled in `work`.
All 14 existing optional modules are covered across the catalog.  The [module matrix](MODULE-MATRIX.md) contains exact feature
membership and linked sizes; [build profiles](BUILD-PROFILES.md) explains each
package.

At source freeze `7125bee`, all nine exact images passed linked memory inspection, foreground/startup/interrupt
stack proof and full offline qualification. Each passes 28 base suites with
286 unit tests and zero skips, plus 26–33 profile suites. Across the catalog
this is 252 base and 255 supplemental suite executions; repeated shared tests
are not counted as distinct tests. Runtime proof precedes the regressions for
each image. The [verification summary](../audits/rc6/beta-catalog-20261024/summary.json)
and [technical report](../audits/rc6/beta-catalog-20261024/README.md) bind the
actual images, measurements, logs and review closure.

`work` uses 40,386 CODE and 2,676 XRAM bytes; 22 main-window and 92 low-window
bytes remain. Its control-stack bound is 162 of 165 bytes, leaving three.
`tap-dance` is 166 of 166 and `key-overrides` is 162 of 162: both pass the
current bound with zero margin. Any code change requires a new exact-image
check; these results do not establish physical timing or power-loss behavior.
Results from the older 24-profile/26-variant matrix do not qualify these images.

The common feature counts remain six layers, 16 Vial macro slots, 8192 shared
macro bytes and eight two-key Combo slots. `tap-dance`, `key-overrides` and
`settings` use schema `0x082003`; the other six use `0x082002`. Stored extension
capacity does not enable an absent module. See [module storage](MODULE-STORAGE.md).

The repository `web/` JSON files preserve the original candidate snapshots.
Use the release's [firmware-matrix.json](https://github.com/dvino/ak820/releases/download/v0.6.0-beta.1/firmware-matrix.json)
for installation status and the reviewed packed `work` settings identity.
Only the `work` row is promoted. Other cross-image settings transfers remain
blocked unless the trusted catalog explicitly lists the exact source/target pair.
See the [firmware handoff](../web/docs/FIRMWARE-HANDOFF.md) for capability and help-link contracts.

## Last recorded installation

The last recorded installation is [alpha.3](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.3), dated 2026-10-24.
Its IHX is `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`.
Beta.1 was not installed in this work.

Alpha.3 was installed with the CLI from the downloaded published Linux archive.
One loader transition, one flash and one restart completed successfully. Exact
CODE and the full application manifest matched the released target after restart.
A second fresh physical confirmation authorized restoring settings. Restoration
verified 498 keys, 12 encoder assignments, 16 macro slots, eight saved RGB bytes
and the eight Combo slots; ten typed setters were used. Full durable NVM readback
passed. Typing was reported working after the update.

The first confirmation attempt timed out before loader entry or erase. It stopped
without retry; a new attempt was explicitly authorized. Fresh backups, update
and restore confirmations and private evidence hashes are recorded in the
[device result](../audits/rc6/alpha3-release-20261024/device-result.json).
OEM recovery images, settings and device captures remain private.

Individual physical NKRO, One Shot, Space Cadet and encoder cases, power-cycle
retention, power-loss behavior and manual GUI acceptance were not tested.

## AK Configurator

Configurator source is maintained in the separate [dvino/ak-configurator](https://github.com/dvino/ak-configurator) repository. The local source was imported there; it has not yet been adapted for AK820. This repository contains no AK820-adapted configurator build, device test or deployment. See its [requirements](https://github.com/dvino/ak-configurator/blob/main/docs/REQUIREMENTS.md), [plan](https://github.com/dvino/ak-configurator/blob/main/docs/PLAN.md) and [migration review](https://github.com/dvino/ak-configurator/blob/main/docs/REVIEW.md). Local documentation checks and independent review cover both migration diffs; they do not qualify the application or firmware.
