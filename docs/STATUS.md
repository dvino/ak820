Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-24. [v0.6.0-alpha.3](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.3)
is published and installed. The release contains standalone Windows and Linux
x86_64 installers, SHA256 files, the firmware bundle and separate English and
Russian installation instructions. All three [native CI jobs](https://github.com/dvino/ak820/actions/runs/40076916540)
passed for source `b17d7c8`. Downloaded public packages pass checksum, exact-image,
GUI/CLI input and offline CLI verification; see the [publication record](../audits/rc6/alpha3-release-20261024/publication.json)
and [asset checks](../audits/rc6/alpha3-release-20261024/published-assets-check.json).
The duplicate tag run was cancelled after publication from that successful main
run; it was not a failed firmware or installer test.

## Web and desktop configurator

The configurator has [requirements](../web/docs/REQUIREMENTS.md), an
[implementation plan](../web/docs/PLAN.md) and a
[firmware handoff](../web/docs/FIRMWARE-HANDOFF.md). Entropy is the first shared
native/Wasm candidate to test; Pipette is the fallback. No configurator code
has been imported, built or deployed. Firmware supplies the OS-helper protocol,
profile catalogs and bilingual feature descriptions. The desktop helper and
platform layout detection remain planned.

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
and [safety manifest](../ci/release-safety.json).

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

Only the exact alpha.3 full image satisfies the packaging gate, independent
program policy and packing receipt. Other profiles and changed source are for
development. The current development matrix is recorded below. Offline qualification did
not access a device; installation results are recorded separately.

## Current development source

The desktop catalog contains nine curated profiles. `work` is the default and
adds Leader, Dynamic Macros and companion-controlled OS indication to the
common functions. Mac/PC, Mouse Keys and Auto Shift are not enabled in `work`.
All 14 existing optional modules are covered across the catalog. No new module
was added. The [module matrix](MODULE-MATRIX.md) contains exact feature
membership and linked sizes; [build profiles](BUILD-PROFILES.md) explains each
package.

All nine exact images pass linked memory inspection, foreground/startup/interrupt
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
catalog explicitly lists that exact source/target pair. The candidate catalog
and ZIP do not approve installation or replace the published alpha.3 bundle.
The [desktop handoff](../web/docs/FIRMWARE-HANDOFF.md) describes these contracts.

The previous [module completion evidence](../audits/rc6/module-completion-20261024/final/README.md)
remains tied to its recorded inputs. No device commands or physical tests have
been performed for the new catalog. Published and installed alpha.3 remains
unchanged.

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
