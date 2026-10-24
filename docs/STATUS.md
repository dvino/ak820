Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-24. The published and installed release is still
[v0.6.0-alpha.2](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.2).
Its Windows and Linux x86_64 packages are described in [Install](INSTALL.md).
Alpha.3 is being prepared from the `full` profile; publication and native
installer acceptance are pending.

## Alpha.3 source and image

The full candidate includes NKRO control, modifier One Shot and compact Space
Cadet alongside the base functions. Its IHX SHA256 is
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`.
It uses 40,043 CODE bytes, 2,631 XRAM bytes and 162 bytes of allocated stack.
There are 441 trailing main-window bytes and 16 low-window bytes.

Exact-image analysis closes the main and three callback roots. The combined
control-stack allowance is 93 bytes for main, two for CRT entry and 61 for all
three interrupt wrappers and callbacks: 156 bytes, leaving six. The proof uses
bank-0 SDCC calls, valid memory accesses, private guard objects and MCS-51
in-service/RETI semantics; it does not assume two priority levels or prove
physical VS11 timing. See the [release qualification](../audits/rc6/alpha3-release-20261024/review.md)
and [safety manifest](../ci/release-safety.json).

The final candidate passes all 15 distinct-source IRQ orders and all 256 LED
selector values in the CPU model. Startup memory and hostile pre-erase entry
checks pass. Independent checks pass 30 analyzer, six startup and five IRQ
unit tests. Settings checks pass 47 tests; a retained real alpha.2 backup passes
offline preflight for 498 keys, 12 encoder assignments and eight Combo slots.
The safety gate passes 20 tests, and all host tools pass 158 tests.
The complete base recheck passes 28 suites and 273 unit tests without skips.
All 13 supplemental full-profile suites pass on the same unchanged image.
Detailed source hashes, review closure, initial fixture failure and remaining
model limits are in the qualification report.

Only this exact full image satisfies the new packaging gate, independent program
policy and fresh packing receipt. Native CI and downloaded-package acceptance
remain before publication.
The other seven profiles remain development builds. The earlier eight-profile
matrix from source `81cfc96` is [dated evidence](../audits/rc6/roadmap-max-20261024/final/README.md),
not qualification of those profiles after the alpha.3 changes.

The [roadmap archive acceptance](../audits/rc6/roadmap-acceptance-20261024/review.md)
records the imported work. The [roadmap](ROADMAP.md) lists remaining release
work and deferred features. No device commands were issued during alpha.3
preparation.

## Installed firmware

`v0.6.0-alpha.2` is installed from the downloaded Linux release installer.
One flash and one restart completed without an error. Exact CODE and the full
application manifest matched the target after restart. Settings restoration
passed after a separate fresh physical confirmation. A final read-only backup
verified 498 key assignments, 12 encoder assignments, 16 macro slots, eight
saved RGB bytes and eight empty Combo getters. Two typed setters restored the
differences; this is not a write test of every assignment or macro slot.

The [installation report](../audits/rc6/alpha2-release-20261024/device-result.json)
binds the source, installed image and private backup hashes. Settings and OEM
recovery files remain private. General operation was reported as apparently
working; individual physical key, encoder and Combo cases were not separately
confirmed. Power-cycle retention, power-loss behavior, nonempty Combo writes
and manual Windows/Linux GUI acceptance remain untested.
