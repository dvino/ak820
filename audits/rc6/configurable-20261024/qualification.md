# Configurable development builds, 2026-10-24

## Work boundary

Three explicit profiles are implemented: `standard`, `nkro`, and `one-shot`.
They retain all previously enabled features and the saved schema `0x082002`.
This is development work; no profile is approved for release or installation.
The published alpha.2 image and installed-firmware evidence are unchanged.
No USB device was opened, reset or flashed.

All three final profiles passed the complete configurator build flow from clean
commit `5fcbe4aa143ca6c4fd877a8c26a35a8d5aa6cf31`. Source, tests and bilingual
documentation passed independent review before implementation commits. The
final documentation and evidence commit changes no compiled or test source.

## Final complete-image measurements

| Image | Main CODE | Low CODE | Total CODE | Main trailing bytes | Low trailing bytes | XRAM bytes | Initial SP | Stack capacity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Published alpha.2 control | 38,492 | 1,821 | 40,313 | 120 | 67 | 2,621 | `0x5f` | 160 |
| `standard` | 38,010 | 1,804 | 39,814 | 602 | 84 | 2,612 | `0x5f` | 160 |
| `nkro` | 38,162 | 1,804 | 39,966 | 450 | 84 | 2,617 | `0x60` | 159 |
| `one-shot` | 38,607 | 1,872 | 40,479 | 5 | 16 | 2,622 | `0x5f` | 160 |

XRAM capacity is 3,072 bytes. Main and low trailing space are different regions;
small internal holes do not make their space interchangeable. The standard
profile saves 499 CODE bytes and nine XRAM bytes against alpha.2, preserving its
160-byte allocated stack. NKRO adds 152 CODE and five XRAM bytes to standard,
and has one fewer allocated stack byte. One Shot adds 665 CODE and ten XRAM
bytes. These measured complete-image differences do not predict combinations.
No profile has a qualified runtime stack bound or margin.

| Profile | Application IHX SHA256 |
| --- | --- |
| `standard` | `004bf2cbda40f9c90ab92e0ee6b6a29bc2098e39d5ee8bc6d0da5df638f2565a` |
| `nkro` | `b31f3eaef084569a9c48a372edc057dfb45508ba6a29e29dcfb0dda3e737e8a2` |
| `one-shot` | `4784f3063d5fc0a5a30d683816ade5b6d4a6408e8a5e14cb68d3cefab7cc3184` |

The [evidence index](final/profiles.json) binds the original build reports,
configuration reports, application IHX, MAP, MEM, suite reports and retained
logs. Original execution paths remain in those reports as provenance; each
retained file has a relative path, size and SHA256 in the index. Raw simulator
traces and intermediate ASM/RST files are omitted from this compact evidence;
a fresh build regenerates them. The application IHX is not a complete
flashable ROM.

## Final regression results

Each profile passed all 28 required base suites, including 270 unit tests with
zero skips, host input/storage behavior and the eight complete-image CPU suites.
The dedicated profile plan additionally passed:

| Profile | Required additional suites |
| --- | --- |
| `standard` | Configurator gates: 13 tests. |
| `nkro` | 13 gate tests; actual NKRO handler host test; two complete-image NKRO scenarios. |
| `one-shot` | 13 gate tests; production OSM host interactions, 156 differential traces and negative controls; 15 complete-image OSM scenarios. |

Every suite checks unchanged image identity before and after execution. The
optional plan also binds the exact command, logs and test-source snapshot.
All configuration reports retain `offline_tests_passed: true` and
`release_approved: false`. Actual CLI negative checks confirm that packaging
and the combined option stop without producing a package or rejected build
directory; see
[negative gates](final/negative-gates.json).

The complete host tool discovery passes 133 tests. Two test fixtures were
corrected after that wider run: a synthetic historical builder is recognized
only within its concurrent-host-change unit test, and toolchain installer
tests create their working directory in a fresh checkout. Independent review
and focused reruns passed; production release checks were not weakened.
ASan and UBSan remained enabled. Leak detection was disabled because the
container restricts the process interfaces needed by LeakSanitizer.


## Retained optimizations

The [private-state changes](size-source.md) save 279 linked CODE bytes and nine
XRAM bytes. The [expanded foreground outliner](../outline-input-20261024/README.md)
saves a further 220 CODE bytes in its control build. Neither change removes
layers, macros, Combos, Grave Escape or other previously enabled functionality.
The final standard image is byte-identical to the outlined control. Its
39,814 CODE bytes preserve the 499-byte reduction against the original control.
The table above records the final integrated measurements.

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

Final independent reinspection reproduced every profile identity and resource
report, validated both exact suite contracts and their file hashes, and confirmed
that package approval still refuses. The standard, NKRO and One Shot evidence
is approved for offline development qualification within those limits. A
separate final review verified all 178 indexed retained files by size and
SHA256, matched the reports to the documentation, and approved this evidence
and documentation commit without blockers.

These are source, build, host and generic CPU model checks. Physical timing,
actual interrupt routing/nesting, USB operation, flash behavior and device
acceptance are not established by them.
