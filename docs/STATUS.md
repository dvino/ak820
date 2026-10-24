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

The `full-leader` development profile adds compact [Leader](COMPACT-LEADER.md):
a physical `QK_LEAD` prefix followed by one selector within 300 ms runs one of
the 16 existing Vial macros. The selector and prefix are consumed; macro
contents remain editable in Vial. The keymap, macro and Combo storage layout
is unchanged. The configurator now lists 18 profiles and a 20-variant
qualification plan. The combined-source matrix is being regenerated; the
older results below qualify only their stated frozen source.

The development follow-up narrows keyboard report helper arguments to their
actual XDATA memory space. The measured `full` candidate saves 34 CODE bytes
and seven XRAM bytes with the same 160/166 stack bound. Short-call builds also
accept empty listing directories recreated by the diagnostic linker; the
reproduced tight-profile IHX is unchanged. Measurements, rejected experiments
and independent review are in the [optimization report](../audits/rc6/leader-next-20261024/optimization.md).
The earlier matrix below describes its frozen source, not this follow-up.

All **17 named profiles and 19 build variants** pass from clean frozen source
`39b6e22`. Every image closes foreground, startup and all three interrupt paths
before its regression suites. Each passes 28 base suites and 273 base unit
tests without skips, plus 16–26 supplemental suites. The complete bounds fit
all linked stack allocations; the minimum remaining margin is 1 byte.

The analyzer now resolves the compact RGB callback. This exposed six earlier
images whose conservative bound exceeded capacity. Correcting the shared delay
calling convention reduces saved registers without changing the delay loop.
The rebuilt `full` uses 160 of 166 stack bytes; `full-ctrl-gui` uses 164 of 166.

The new `full-ctrl-gui` profile adds volatile left/right Ctrl/GUI swaps alongside
GUI lock. It retains raw modifier ownership and queued One Shot state. Six
layers, 16 Vial macros, 8192 macro bytes, eight Combos and schema `0x082002`
remain unchanged.

Every new feature/profile must pass its own exact-image runtime check before
full regression qualification. All 19 images pass 15 IRQ nest orders, all 256
LED selector values and seven delay ABI cases. These are static and CPU-model
results; the public IRQ fixture does not require a private OEM image.
Measurements and source, image, test and log hashes are in the
[final matrix](../audits/rc6/runtime-stack-20261024/final/README.md).
Findings and independent review are in the
[technical report](../audits/rc6/runtime-stack-20261024/README.md).

The previous compact matrix at source `55acbb0` is historical. Changed source
still requires separate release and installer-transition approval. No physical
test or device command was performed. The published and installed firmware
remains the exact alpha.3 image above.

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
