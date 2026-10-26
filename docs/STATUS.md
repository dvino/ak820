Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

## v0.6.0-beta.3 source candidate, 2026-10-26

The source candidate retains Caps Word toggle (`CW_TOGG`) as a two-key Combo
output and adds macro-on-tap, layer-on-hold actions for physical matrix keys.
The beta.3 profile plan puts Auto Shift in `main` and `typing`, and leaves GUI
lock out of `main`. A rejected `game` image with the proposed W pulse exceeded
the CODE limit by 160 bytes. The pulse has been deferred in all profiles.
Host checks for the Combo output, macro keycode handling, settings storage and
protocol have passed. Shared tool preflight passed 283 tests. The current main
image uses 40,398 CODE bytes. Fresh startup, foreground and enabled-interrupt
checks passed with a 160/167-byte stack bound. Main passed 336 unit tests with
no skips and all 34 supplemental profile suites.
All ten local images passed exact-image qualification: 336 unit tests without
skips per image and 32–37 supplemental suites. Offline packing and 230 default
settings plans across 23 source images passed, as did 100 Caps Word Combo plans,
100 macro Layer-Tap plans and the frozen 180-test settings suite. These are
offline checks, not device validation. Source review passed; final generated
policy review remains pending. Rejected earlier candidates do not qualify the release.
Publication is on hold. The published beta.2 release
remains available unchanged. No device writes were performed; installation and
keyboard behavior are untested.

## CI validation time, 2026-10-26

The release workflow reuses successful transform checks while all inputs remain
identical and runs the first assembly inspections in four processes. Every
inspection rehashes the inputs; firmware tests and release checks still run.
See [CI and releases](https://github.com/dvino/ak820/blob/main/docs/CI.md).

A fresh local `multios` build and qualification completed in 7 minutes 4 seconds:
28 base suites, 331 unit tests with no skips, and 37 supplemental suites passed.
The exact IHX remained unchanged; the whole-program stack bound is 160/171 bytes.
Shared host discovery passed 281 tests. A separate inspection benchmark measured
22.974 seconds cold and 2.454 seconds with unchanged inputs. The previous
[GitHub run](https://github.com/dvino/ak820/actions/runs/40268741259) took
84 minutes 6 seconds overall, including 58 minutes 6 seconds for the `multios`
build/qualification command. These are different hosts, not an end-to-end CI
speedup measurement. A new ten-profile GitHub run and native package builds
remain to be run. No device commands were sent. Evidence and review are in
`audits/ci-speed-20261026/`.

## Beta.2: ten profiles

Beta.2 contains ten profiles: `main`, `game`, `mmo`, `typing`, `code`, `pointer`,
`onehand`, `creative`, `shortcuts` and `multios`. `main` is the default. The installer
selects profiles, and each profile has English and Russian instructions. See the
[profile catalog](profiles/README.md) and [module matrix](MODULE-MATRIX.md).

The exact fresh image for each profile passed foreground, startup and every
enabled interrupt stack check before full regression. Each image passed 28
base suites and 331 unit tests with no skips, plus 32–37 supplemental
suites. Across ten images this is 280 base and 335 supplemental suite
executions. Repeated shared tests are not counted as distinct tests. Fresh
builds retained the same IHX bytes as the images used for packing and
settings-transition checks. The [qualification
record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/qualification-final.json)
links image identities and results. The [packing
preflight](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/packing-preflight.json)
records offline package checks; the [transition
preflight](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/transition-preflight.json)
covers 130 offline cases: ten same-profile cases and 120 explicit forward edges. Sources alpha.2, alpha.3 and beta.1 `work` each have a listed path to all ten beta.2 profiles; paths between beta.2 profiles are limited to the reviewed edges. The [alpha.3 correction record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/alpha3-transition-fix.json) binds historical IHX `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18` and CODE `01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d`; it records ten offline alpha.3 restore plans and separate nondefault fixtures. Unsupported or unlisted transitions are rejected. These checks do not validate hardware behavior.

| Profile | CODE bytes | Stack bound |
| --- | ---: | ---: |
| `main` | 39,803 | 160/168 bytes |
| `game` | 40,085 | 160/167 bytes |
| `mmo` | 39,884 | 164/167 bytes |
| `typing` | 39,942 | 160/172 bytes |
| `code` | 39,779 | 160/172 bytes |
| `pointer` | 40,098 | 160/172 bytes |
| `onehand` | 40,077 | 164/172 bytes |
| `creative` | 39,707 | 164/168 bytes |
| `shortcuts` | 40,081 | 164/172 bytes |
| `multios` | 39,682 | 160/171 bytes |

See the [final release review
record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/final-release-review.md)
for review scope and recorded findings. Publication is recorded on the [release page](https://github.com/dvino/ak820/releases/tag/v0.6.0-beta.2). No USB
commands were sent for beta.2. USB timing,
LED DMA, physical flash faults, power loss, retention after power removal and manual
GUI behavior remain untested. Hardware acceptance is unvalidated.

## Previous release: beta.1

[v0.6.0-beta.1](https://github.com/dvino/ak820/releases/tag/v0.6.0-beta.1)
provides Windows and Linux x86_64 installers for the `work` image. Its
checks, catalog and packages apply to beta.1 only. See the [acceptance
record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta1-release-20261025/acceptance.md),
[publication
record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta1-release-20261025/publication.json)
and [download
checks](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta1-release-20261025/published-assets-check.json).

The whole-program compression diagnostic is recorded in [Maximum Functionality
Status](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/docs/MAXIMUM-FUNCTIONALITY-STATUS.md).

## Last recorded installation

The last recorded installation is
[alpha.3](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.3), dated 2026-10-24.
IHX SHA256: `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`. The
exact CODE and application manifest matched after restart. Settings
readback covered 498 keys, 12 encoder assignments, 16 macro slots, eight
RGB bytes and eight Combo slots; full durable NVM readback passed. See the [device
result](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/alpha3-release-20261024/device-result.json).
Beta.1 and beta.2 were not installed during this work. This historical alpha.3 result
does not validate beta.2 hardware behavior.

## AK Configurator

The companion is developed in the separate
[dvino/ak-configurator](https://github.com/dvino/ak-configurator) repository. The
standalone firmware installers in this repository provide profile selection while
the companion is being developed. See the companion
[requirements](https://github.com/dvino/ak-configurator/blob/main/docs/REQUIREMENTS.md)
and [plan](https://github.com/dvino/ak-configurator/blob/main/docs/PLAN.md).
