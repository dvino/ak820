Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-24. [v0.6.0-alpha.2](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.2)
is published from commit `4772c433057bde5c9ccc4f2f3f904f1dcb326c17`.
It includes eight two-key Combos and settings backup/restore for their eight
slots. Windows and Linux x86_64 installers are available. See [Install](INSTALL.md)
for package selection, checksums and launch commands.

## Source and built image

Development continued from `dev` commit `48ce5fa`. The configurator now offers
all eight combinations of NKRO control, modifier One Shot and compact Space
Cadet. Commands and limits are in [Build profiles](BUILD-PROFILES.md). Published
and installed alpha.2 remains unchanged.

The `ak820-roadmap-20261024-git.tar.gz` handoff was imported through `4f6fffb`.
All 2,071 retained evidence checksums pass. The local full-profile rebuild
reproduces IHX SHA256 `45681603a105334214919be0b8c32fc4ea94e8fc9d5a2003e98d673809d15a78`.
The full recheck passed 28 base suites, 270 unit tests without skips and nine
supplemental suites. The initial documentation-link failure is retained.
Release packaging still refuses the image for the three reasons below; this
acceptance does not publish alpha.3. See the [acceptance record](../audits/rc6/roadmap-acceptance-20261024/review.md)
and [next release plan](ROADMAP.md#next-alpha-release).

All eight profiles pass full linking and exact memory/configuration checks.
The current standard image uses **39,115 CODE and 2,612 XRAM bytes**, saving
699 CODE bytes from the starting development image and 1,198 from alpha.2.
The full profile with all three optional features uses **40,018 CODE and 2,630
XRAM bytes**; it leaves 466 trailing main-window bytes and 16 low-window bytes.
Its 162 allocated stack bytes are capacity, not a runtime bound. Exact profile
sizes and image identities are in the
[development evidence](../audits/rc6/roadmap-max-20261024/final/README.md).
All eight profiles passed complete offline qualification from source `81cfc96`:
28 base suites and 270 unit tests without skips per profile, plus 58 supplemental
suite executions across the matrix. Exact flags, artifacts, commands, logs and
test-source hashes are bound to each result. The initial sanitizer environment
failures and the complete successful reruns are retained in the same report.

The new [packing selection](../audits/rc6/roadmap-max-20261024/packing.md)
saves 668 CODE bytes on an unchanged baseline. All 194 helpers pass 3,104 CPU
state comparisons; integrity checks cover all 1,384 replacement sites.
[Protocol changes](../audits/rc6/roadmap-max-20261024/protocol-size.md) reduce
private representation and descriptor costs without changing wire formats.
[Space Cadet](../audits/rc6/roadmap-max-20261024/space-cadet.md) adds the three
bounded Shift/tap actions. Feature costs are measured in complete images and
must not be added as independent estimates.

The [exact-image stack analyzer](../audits/rc6/runtime-stack-20261024/report.md)
now resolves bounded USB dispatch and constant ROM callback targets, rejects
unproven paths and records unresolved roots. It does not yet establish a bound
for the whole main path or the LED interrupt. A reviewed global stack bound,
exact-image interrupt/nesting proof and installer transition remain missing.
No profile is approved for installation or release; the existing release
workflow and configurator stop before producing a package. No device commands
were sent during this development work.

[Feature probes](../audits/rc6/roadmap-max-20261024/feature-probes.md) identify
size and compiler blockers for Mouse Keys, Auto Shift, Tap Dance and Key
Overrides. The [QMK Settings design](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md)
inventories effective settings and a versioned record in the measured logical
gap after Combo data. It is a proposal; the saved format and runtime settings
remain unchanged.

### Published alpha.2 image

The Combo work was imported from `ak820-combos-20261024-git.zip`, based on
`4b83bb9`, through `d361501`. Release integration adds reviewed settings
preservation and native Linux packaging. The application uses 40,313 CODE
bytes: 38,492 main and 1,821 low. It leaves 120 trailing main-window bytes and
67 low-window bytes. XRAM is 2,621 bytes; initial SP is `0x5f`, with 160 bytes
allocated for the stack. These figures do not prove a worst-case stack bound.

The application IHX SHA256 is
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`.
The IHX is an application, not a complete flashable ROM. The installer builds
the complete update with validated local OEM recovery data.

## Verification

The [tag CI run](https://github.com/dvino/ak820/actions/runs/40060505913)
passed all four jobs. Its firmware qualification passed 28 suites and 270 unit
tests with zero skips. The fresh local qualification before Linux packaging
passed 28 suites and 265 tests; later Linux host changes have separate
[regression evidence](../audits/rc6/alpha2-release-20261024/linux-integration.json).
Host models and linked CPU execution do not establish device behavior.

Native Windows and Ubuntu 22.04/glibc 2.35 builds passed CLI verification and
Tk startup checks. Linux also verified its frozen hidraw backend. The three
downloaded public archives passed checksum, source and packaged-input checks;
see the [asset check](../audits/rc6/alpha2-release-20261024/asset-check.json) and
[independent review](../audits/rc6/alpha2-release-20261024/published-artifact-review.md).
The downloaded Linux CLI also passed local help and offline verification.
GUI startup checks do not establish manual interaction or display scaling.

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
