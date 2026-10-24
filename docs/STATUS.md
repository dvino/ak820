Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-25. [v0.6.0-alpha.3](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.3)
is published and installed. The release contains standalone Windows and Linux
x86_64 installers, SHA256 files, the firmware bundle and separate English and
Russian installation instructions. All three [native CI jobs](https://github.com/dvino/ak820/actions/runs/40076916540)
passed for source `b17d7c8`. Downloaded public packages pass checksum, exact-image,
GUI/CLI input and offline CLI verification; see the [publication record](../audits/rc6/alpha3-release-20261024/publication.json)
and [asset checks](../audits/rc6/alpha3-release-20261024/published-assets-check.json).
The duplicate tag run was cancelled after publication from that successful main
run; it was not a failed firmware or installer test.

## Companion-design beta

`v0.6.0-beta.1` is being prepared as the nine-profile firmware baseline for companion design. The work source bundle is approved; native Windows/Linux package acceptance and publication are pending. The beta release is the first installable firmware baseline for the companion and includes standalone Windows and Linux x86_64 installers with SHA256 files and bilingual installation instructions. The installers target the exact `work` image (`652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880`, 40,386 CODE bytes, 2,676 XRAM bytes; stack bound 162/165). The other eight profiles remain catalog candidates and are not included in the installers. Beta firmware has not been tested on hardware. The installed alpha.3 firmware remains unchanged. The [acceptance record](../audits/rc6/beta1-release-20261025/acceptance.md) records the source integration, exact assets and independent review.

## Alpha.3 source and image

The full image includes NKRO control, modifier One Shot and compact Space
Cadet alongside the base functions. Its IHX SHA256 is
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`.
It uses 40,043 CODE bytes, 2,637 allocated XRAM bytes and 162 bytes of allocated stack.
There are 441 trailing main-window bytes and 16 low-window bytes.

Exact-image analysis closes the main and three callback roots. The combined
control-stack allowance is 93 bytes for main, two for CRT entry and 61 for all
three interrupt wrappers and callbacks: 156 bytes, leaving six. The proof uses
bank-0 SDCC calls, valid memory accesses, private guard objects and MCS-51
in-service/RETI semantics; it does not assume two priority levels or prove
physical VS11 timing. See the [release qualification](../audits/rc6/alpha3-release-20261024/review.md)
and [alpha.3 safety manifest](https://github.com/dvino/ak820/blob/v0.6.0-alpha.3/ci/release-safety.json).

The released image passes all 15 distinct-source IRQ orders and all 256 LED
selector values in the CPU model. Startup memory and hostile pre-erase entry
checks pass. Independent checks pass 30 analyzer, six startup and five IRQ
unit tests. Settings checks pass 47 tests; a retained real alpha.2 backup passes
offline preflight for 498 keys, 12 encoder assignments and eight Combo slots.
The safety gate passes 20 tests, and all host tools pass 158 tests.
The complete base recheck passes 28 suites and 273 unit tests without skips.
All 13 supplemental full-profile suites pass on the same unchanged image.
Detailed source hashes, review closure, initial fixture failure and remaining
model limits are in the qualification report.

The alpha.3 full image satisfied its packaging gate, independent program policy and packing receipt. That evidence applies only to alpha.3. Beta profile qualification is recorded below; it does not include physical device validation.

## Current development source

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

The machine catalog and bilingual popup descriptions are prepared for desktop
integration. Exact packed settings identities require the validated local OEM
reference during packaging. Cross-image restore is disabled unless the trusted
catalog explicitly lists that exact source/target pair. The candidate catalog and ZIP record exact linked images; beta release approval and installer evidence are recorded in the beta acceptance record.
The [desktop handoff](../web/docs/FIRMWARE-HANDOFF.md) describes these contracts.

The previous [module completion evidence](../audits/rc6/module-completion-20261024/final/README.md)
remains tied to its recorded inputs. No device commands or physical tests have been performed for the new catalog. Installed alpha.3 remains unchanged.

## Installed firmware

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
