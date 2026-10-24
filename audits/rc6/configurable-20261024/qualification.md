# Configurable development builds, 2026-10-24

## Work boundary

Three explicit profiles are implemented: `standard`, `nkro`, and `one-shot`.
They retain all previously enabled features and the saved schema `0x082002`.
This is development work; no profile is approved for release or installation.
The published alpha.2 image and installed-firmware evidence are unchanged.
No USB device was opened, reset or flashed.

The source implementation has passed independent precommit review. Final
integrated builds and exact-image offline qualification are still pending in
this intermediate commit. Results will be added here after those runs finish.

## Retained optimizations

The [private-state changes](size-source.md) save 279 linked CODE bytes and nine
XRAM bytes. The [expanded foreground outliner](../outline-input-20261024/README.md)
saves a further 220 CODE bytes in its control build. Neither change removes
layers, macros, Combos, Grave Escape or other previously enabled functionality.
The measured intermediate default image uses 39,814 CODE bytes against 40,313
in the original control, a 499-byte reduction. Final integrated profile
measurements remain authoritative for the finished source.

The complete outliner differential run checks 155 helpers and 1,608 replacement
sites, using 16 CPU states per helper (2,480 cases). All pass. New selected
foreground sites are disjoint from the conservative closure of three interrupt
roots and 13 reachable functions. This check is not a global stack proof.

Further private flags with an extra 24-byte saving were rejected because they
reduced allocated stack capacity. Small loop/helper changes that added calls or
regressed size were also rejected. The global `--noinvariant` experiment saved
only four bytes against the original control while adding two XRAM bytes; it
is not enabled. The pinned compiler does not support `--max-allocs-per-node`
for this target. The retained compiler and ABI flags remain unchanged.

## Features and combinations

The [profile guide](../../../docs/BUILD-PROFILES.md) lists all 11 candidates,
implemented behavior and remaining scope. The configuration catalog is
`qmk-8051-ak820/util/ak820_profiles.py`. Both optional switches are explicitly
set for every build; inherited Make options cannot silently choose a feature.

The compact NKRO controls change the existing report mode until restart. They
clear input owners before switching and do not write NVM. The One Shot profile
implements bounded OSM modifiers, including matrix and both encoder sources,
held modifiers, queued masks and cancellation. OSL and upstream One Shot
settings are absent. No new saved state or migration is introduced.

[Pre-integration feature measurements](compact-options/SCOPE.md) retain exact
hashes and rejected experiments. The combined NKRO + One Shot image crosses
the main limit through `0xc792`, so it is rejected as an allowed choice. The
larger OSM + OSL experiment also overflows and is absent from active code.
Feature costs are not additive.

Runtime QMK Settings remain disabled. The upstream 36-byte structure precedes
Combo data at the fixed base `0x658`; simply enabling it changes the saved
layout. The existing 16 macro slots and 8,192-byte macro capacity remain
unchanged. Combo and tap-hold timing remain 40 ms and 200 ms. A visible Vial
control alone does not establish an implemented firmware setting.

## Resource and identity gates

The configurator validates occupied bytes separately in low CODE
`[0x28a0,0x3000)` and main CODE `[0x3027,0xc700)`. It checks ordinary XRAM
`[0x400,0x1000)`, the absolute LED DMA buffer at `0x200`, IRAM placement,
stack allocation and the startup DPTR contract. A complete manifest of final
relocated listings is checked against their hashes and the instruction bytes
in the final IHX. This also verifies that only the selected optional handler
is present without changing its firmware linkage.

The report binds the option set, schema, source manifest, compiler, IHX, MAP,
MEM and build report. All 28 existing host/CPU suites remain required. A
separate exact profile contract requires the configurator gate tests and the
chosen option's host and linked suites. Missing, duplicated, modified or
wrong-image evidence is rejected.

`runtime_stack_bound` and `stack_margin` remain null. Static allocation and
sampled simulator peaks do not establish a maximum over all foreground paths,
interrupts and nesting. Consequently `package` always refuses. Both existing
release packagers also reject configured development images. Removing the
configuration field does not bypass the guard: legacy reports need an
explicit recognized historical builder and must lack the new profile source.
No settings/install transition is approved merely from a matching schema.

## Independent review

The [source review](source-review.md) covers the retained size patch. Independent
reviews of compact input and outliner changes found no remaining source blocker.
The last fixes restore the private tapping-source ABI in profiles without OSM
and add cancellation, overlapping modifier, MT/LT, Repeat, Caps Word and Combo
interaction checks. The configurator review closed a removable-configuration
bypass, missing required optional-feature suites, and incomplete relocated
listing coverage. The final focused gate suite passes 13 tests. Temporary host
test fixtures were updated to reach the intended missing-approval branch;
production installer checks were not relaxed.

These are source, build, host and generic CPU model checks. Physical timing,
actual interrupt routing/nesting, USB operation, flash behavior and device
acceptance are not established by them.
