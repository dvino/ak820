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
development. The current matrix is recorded below. Offline qualification did
not access a device; installation results are recorded separately.

## Current development source

All 16 named profiles passed 18 build variants from frozen source `55acbb0`.
Each image passed 28 base suites and 273 base unit tests with zero skips, plus
14–24 supplemental suites for its selected features. These results belong to
the frozen source. Cleanup later changed the configurator test fixture path;
firmware source and retained image bytes are unchanged.

Compact Mouse Keys and Auto Shift are joined by volatile GUI controls and
two temporary Dynamic Macro slots. Six layers, 16 Vial macros, 8192 macro bytes,
eight Combos and schema `0x082002` remain unchanged. The previous eleven-profile
matrix belongs to source `06b8f0f` and is historical.

A whole-program stack bound for these images remains unproved. The normal
package command rejected the changed `full` image because its source differs
from the reviewed release witness. No physical test or device command was
performed in this work. The published and installed firmware remains the exact
alpha.3 image above. Measurements, hashes, raw logs and independent review are
in the [technical report](../audits/rc6/compact-runtime-20261024/README.md).

Integration checks and archive size are recorded in the [acceptance report](../audits/rc6/compact-runtime-20261024/acceptance.md).

Repository cleanup and retained evidence are recorded in the [cleanup report](../audits/rc6/cleanup-20261024.md).

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
