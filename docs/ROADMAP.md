Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The first configurable development profiles are implemented: `standard`,
`nkro` and `one-shot`. See [Build profiles](BUILD-PROFILES.md) for behavior,
commands and limits. No profile is approved for installation or release while
the whole-program stack bound, exact-image interrupt/nesting proof and installer
transition remain open. Current release and installation results belong in
[Status](STATUS.md). The broader stage remains open for the work below.

## Compact optional features

The initial inventory and two bounded implementations are complete. One Shot
modifiers and NKRO control are available in separate development profiles;
their tested scope is documented in [Build profiles](BUILD-PROFILES.md). The
remaining candidates below are still deferred. A setting shown by Vial is not
proof that a module is included.

| Candidate | First implementation scope | Memory and compatibility |
| --- | --- | --- |
| One Shot | Limited modifier combinations in the `one-shot` development profile; layers and other behaviors are excluded. | Profile regression tests run offline; release safety proof remains open. |
| Tap Dance | A small, fixed set of tap/hold patterns | Measure; check the shared input pipeline, tap-hold and Combos. |
| Key Overrides | Replace a key when specified modifiers are active | Measure; check modifier ownership, Repeat, Caps Word and macros. |
| Mouse Keys | Basic pointer, button and wheel actions | Measure; check USB reports, scan timing and encoder actions. |
| Auto Shift | Choose Shift from press duration | Measure; check interaction with tap-hold, Combos and Caps Word. |
| NKRO control | `NK_ON`, `NK_OFF` and `NK_TOGG` in the `nkro` development profile; volatile only. | Profile regression tests run offline; saved settings and other Magic actions are not included. |
| QMK Settings in Vial | Change supported timing and behavior options without rebuilding | Start with a compact subset; connect each option to its actual handler and measure CODE, RAM and saved-data costs. |
| Magic | Selected modifier swaps and GUI-key control | Review separately from NKRO; check keycode configuration, persistence and existing modifier owners. |
| Leader | Short sequences that trigger actions | Bound sequence length, timeout and supported results. |
| Space Cadet | A modifier while held, a parenthesis when tapped | Check compact tap-hold ownership and cancellation. |
| Dynamic macros | Record and replay key sequences on the keyboard | Distinguish from the existing 16 Vial macros; bound the recording buffer and check RAM and replay behavior. |

The profile inventory separates runtime settings from build switches and user
features from deliberately excluded diagnostics; see [Build profiles](BUILD-PROFILES.md).

The deferred entries are candidates, not promised build options. Their byte
costs and allowed combinations are not yet measured. The order of implementation
should follow usefulness, complete-image cost and interaction complexity.

## QMK Settings and existing compact functions

`QMK_SETTINGS = no` in alpha.2 and all current development profiles. The existing Vial keymap, macro and lighting
settings do not imply QMK Settings support. Inventory the upstream settings:
tap-hold timing and policy, Combo timing, Grave Escape overrides, tap delays,
One Shot, Auto Shift, Mouse Keys and Magic options. Offer only settings consumed
by enabled handlers; a visible control must change actual behavior.

The current compact tap-hold and Combo engines use fixed timing and reduced
behavior. Assess configurable timing and additional behaviors separately from
enabling their upstream engines. List which upstream behaviors remain absent.

The upstream QMK Settings structure occupies 36 bytes before other dynamic
feature data. The current Combo base is fixed by a compile-time assertion.
Enabling the flag alone is therefore insufficient: design the saved layout,
versioning, defaults, reset, backup and migration together, then measure the
whole image. The 36 bytes are a structure size, not a total feature cost.

## Compatibility and memory table

For each module and supported combination, record dependencies, conflicts,
saved-format changes and the exact build settings. Measure the complete linked
image with the pinned compiler; shared code, dead-code removal and outlining
make individual size deltas non-additive.

Track both CODE windows separately, along with XRAM, internal RAM and stack
requirements. The current alpha.2 has 120 trailing main-window bytes and 67
low-window bytes; these are different regions. Its 160-byte allocated stack
capacity is not a proven runtime allowance. See [Memory](RESOURCE-BUDGET.md).
Do not count reserved loader, settings or journal space as free code memory.
Unknown costs or unchecked combinations must stay marked as unknown.

## Build configurator

The configurator accepts only the three implemented development profiles and
rejects the combined NKRO plus One Shot image. Each build links within the real
memory windows and runs offline regression tests on its exact image. It does
not approve profiles for packaging: a reviewed whole-program stack bound,
exact-image interrupt/nesting proof and installer transition are missing.
Estimates alone must never permit an oversized firmware image.

Development results contain the selected options, source commit, toolchain,
resource report and exact firmware identity. Both CODE windows, XRAM, internal
RAM and protected addresses are checked. Runtime stack margin remains
unqualified; therefore packaging stops without producing an approved package.
Expand the allowed combinations only as evidence becomes available.

## Further code-size analysis

Review all code reachable by the selected firmware: action and event handling,
USB, descriptors, Vial, macros, lighting, settings and build-time transforms.
Look for duplicated work, unnecessary generic pointers, avoidable data copies,
representation costs and shared helpers. Compare each proposal with the exact
current build, including interactions with optional modules.

Preserve behavior, interrupt safety, ABI and storage checks. Keep rejected
experiments out of the production build and retain their evidence in technical
reports. Do not reduce layers, macro capacity or existing functionality to make
a new option appear to fit. A layout or storage-format change needs its own
migration and backup plan.

## Completion of this stage

- Document each implemented option, its limits and complete-image resource cost.
- Publish the compatibility table and profiles after release qualification.
- Keep the configurator closed to packaging until stack, IRQ and installer proofs pass.
- Run relevant host and linked CPU regressions for every development profile;
  test interactions rather than just isolated modules.
- Bind packages, settings backup compatibility and update checks to the exact
  selected image. A different feature set is not interchangeable merely
  because it shares a settings schema.
- Keep device acceptance separate from models. Default tests remain offline or
  read-only; every hardware flash needs separate confirmation.

## Other open work

Physical Combo timing, nonempty Combo writes, cold-start retention, power-loss
behavior and manual Windows/Linux GUI acceptance remain open.
VialRGB Direct remains RAM-only. Persistent palettes are outside this
stage until their storage and migration design is separately agreed.
