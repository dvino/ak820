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

The `web-dev` branch adds [requirements](../web/docs/REQUIREMENTS.md) and an
[implementation plan](../web/docs/PLAN.md). Entropy is the first shared
native/Wasm candidate to test; Pipette is the fallback. No configurator code
has been imported, built or deployed. The plans were merged into the accepted
firmware baseline. Firmware now provides the OS-helper protocol and an offline
catalog generator; the desktop helper and platform layout detection remain
planned. See the [work report](../audits/rc6/web-firmware-20261024/README.md).

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

All **24 named profiles and 26 linked variants** pass fresh whole-image stack
and interrupt checks. Every image closes foreground calls, CRT startup and
all USB, timer and LED interrupt roots, including all 15 distinct-source IRQ
orders and 256 LED selector values. No required path is unknown.

Three profiles independently add [Tap Dance](COMPACT-TAP-DANCE.md),
[Key Overrides](COMPACT-KEY-OVERRIDES.md) and
[runtime QMK Settings](QMK-SETTINGS.md) to `full`. Each retains six layers,
16 Vial macro slots, 8192 macro bytes and eight Combo slots. These extensions
are separate profile choices; there is no named all-three combination.

| Profile | CODE bytes | XRAM bytes | Stack bound/capacity | Margin | Supplemental suites |
| --- | ---: | ---: | ---: | ---: | ---: |
| `full` | 38,447 | 2,555 | 162/167 | 5 | 21 |
| `full-tap-dance --short-calls` | 40,173 | 2,795 | 166/166 | 0 | 23 |
| `full-key-overrides --short-calls` | 40,464 | 2,734 | 162/162 | 0 | 23 |
| `full-qmk-settings --short-calls` | 40,075 | 2,640 | 162/166 | 4 | 23 |

Each of these four exact images passes **28 base suites and 276 unit tests
without skips**. All 90 supplemental suites pass. Ordinary ASan, UBSan and
LeakSanitizer settings remain enabled. The other 22 variants have fresh
runtime proofs; their full functional regressions were not repeated.
Tap Dance and Key Overrides have no calculated stack margin. Key Overrides
has 20 trailing bytes in the main CODE window. Any change needs a new proof.

The three extension profiles use schema `0x082003`; the other profiles retain
`0x082002`. Typed commands, backup preflight and explicit migration preserve
the existing keymap, encoder, Combo and macro regions. Stored extension data
and enabled controls are separate. See [module storage](MODULE-STORAGE.md).

Firmware inputs are frozen at `ac48c65`. Full qualification uses `147508e`;
the two follow-up commits change host/CPU fixtures and audit records only.
Complete raw builds for the four full regressions, runtime witnesses for all
26 variants and exact hashes are in the [final matrix](../audits/rc6/module-completion-20261024/final/README.md).
The [development catalog](../audits/rc6/module-completion-20261024/final/capability-catalog.json)
contains those four fully checked images, their enabled controls and storage
contracts. The [desktop handoff](../web/docs/FIRMWARE-HANDOFF.md) defines the
next application work.

The earlier [21-profile matrix](../audits/rc6/web-firmware-20261024/runtime-all/README.md)
and [Leader matrix](../audits/rc6/leader-next-20261024/final/README.md) describe
their own source only. Review and fixture corrections are in the
[module work report](../audits/rc6/module-completion-20261024/README.md).
No device command or physical test was performed for this work. The published
and installed alpha.3 image is unchanged; new images have no release or
installer-transition approval.

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
