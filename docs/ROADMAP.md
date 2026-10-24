Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The next stage is a configurable build with compact optional features and a
further analysis of the active code for size savings. Existing features and
settings must remain usable. Current release and installation results belong
in [Status](STATUS.md).

## Compact optional features

Inventory the functions missing from the installed firmware, then prepare
small implementations that can be enabled independently at build time. Start
with a minimal working version of each feature, with its behavior and limits
written down. A setting shown by Vial is not proof that a module is included.

| Candidate | First implementation scope | Memory and compatibility |
| --- | --- | --- |
| One Shot | A modifier or layer for the next key | Measure; check cancellation, held keys and layer owners. |
| Tap Dance | A small, fixed set of tap/hold patterns | Measure; check the shared input pipeline, tap-hold and Combos. |
| Key Overrides | Replace a key when specified modifiers are active | Measure; check modifier ownership, Repeat, Caps Word and macros. |
| Mouse Keys | Basic pointer, button and wheel actions | Measure; check USB reports, scan timing and encoder actions. |
| Auto Shift | Choose Shift from press duration | Measure; check interaction with tap-hold, Combos and Caps Word. |
| NKRO control | A small user action for the reporting code already present | Measure; check both report modes and saved settings without enabling all Magic actions. |
| Other disabled QMK functions | Review Leader, Space Cadet, dynamic macros and runtime settings separately | Define a bounded scope first; do not enable upstream modules blindly. |

These are candidates, not promised build options. Their byte costs and allowed
combinations are not yet measured. The order of implementation should follow
usefulness, complete-image cost and interaction complexity.

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

Use the measured table as input to a configurator. It should explain available
options, dependencies and conflicts, and reject combinations that have not
been qualified. Show estimates while choosing, but accept a configuration only
after its actual build passes the linker and all resource checks. An estimate
alone must never permit an oversized firmware image.

The result should contain the selected options, source commit, toolchain,
resource report and exact firmware identity. Validate both CODE windows, XRAM,
internal RAM, a justified stack margin and protected addresses. If a limit or
required evidence is missing, stop without producing an approved package.
Keep a small set of tested profiles as the first usable version; expand the
allowed combinations as evidence becomes available.

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

- Document each implemented option, its limits and measured resource cost.
- Publish the compatibility table and tested build profiles.
- Provide a configurator that rejects unknown, incompatible and oversized builds.
- Run relevant host and linked CPU regressions for every supported profile;
  test interactions rather than just isolated modules.
- Bind packages, settings backup compatibility and update checks to the exact
  selected image. A different feature set is not interchangeable merely
  because it shares a settings schema.
- Keep device acceptance separate from models. Default tests remain offline or
  read-only; every hardware flash needs separate confirmation.

## Other open work

Physical Combo timing, nonempty Combo writes, cold-start retention, power-loss
behavior and manual Windows/Linux GUI acceptance remain open. Language
switching on Caps and a Windows language helper require a separate behavior
contract, including cancellation and stale state; language status must remain
in RAM. VialRGB Direct remains RAM-only. Persistent palettes are outside this
stage until their storage and migration design is separately agreed.
