Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The three implemented optional features—NKRO control, modifier One Shot and
Space Cadet—are available in all eight combinations in development profiles.
Their behavior and limits are listed in [Build profiles](BUILD-PROFILES.md).
The exact full image has reviewed stack, interrupt and settings-transition
proofs and is published as alpha.3. Other profiles remain development work and
need separate qualification before release. Current source, release and device
results belong in [Status](STATUS.md).

## Deferred features

The initial inventory contains 11 candidates. Three have bounded
implementations; the other eight remain deferred. A Vial control or keycode is
not evidence that a feature is enabled.

| Candidate | Open work |
| --- | --- |
| Tap Dance | The upstream probe has callback ABI blockers and moves fixed Combo storage; a compact implementation must preserve the Combo layout. |
| Key Overrides | The upstream probe has callback ABI blockers; modifier ownership and interactions with Repeat, Caps Word and macros remain open. |
| Mouse Keys | The upstream probe exceeds the main CODE window by 1,381 bytes; a smaller scope and scan-time review are needed. |
| Auto Shift | Needs explicit C `case` labels instead of GNU case ranges; the upstream probe exceeds the main CODE window by 2,081 bytes. |
| QMK Settings in Vial | A new versioned saved record, typed backup and restore, and migration still need implementation. The compatible plan preserves existing Combo offsets; see the [settings plan](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md). |
| Magic | Modifier swaps and GUI control need separate compatibility and persistence review. |
| Leader | Bound sequence length, timeout and supported outputs. |
| Dynamic macros | Bound recording RAM and qualify replay behavior; Vial macros remain available. |

Probe details and measured outcomes are in the
[feature report](../audits/rc6/roadmap-max-20261024/feature-probes.md).

The three available implementations are intentionally limited. NKRO control
adds only `NK_ON`, `NK_OFF` and `NK_TOGG`; One Shot handles modifier combinations
without layer form, timeout or locking; Space Cadet handles `SC_LSPO`, `SC_RSPC`
and `SC_SENT` through compact tap-hold. See [Build profiles](BUILD-PROFILES.md)
for exact behavior and tested interactions.

## Runtime settings and saved data

`QMK_SETTINGS = no` in alpha.2 and configured development profiles. Vial
keymap, macro and lighting settings do not imply support for QMK Settings.
Only expose a setting when an enabled handler consumes it and changes behavior.

The upstream QMK Settings structure is 36 bytes before other dynamic feature
data. Enabling the upstream flag alone moves the fixed Combo layout at `0x658`
and is incompatible. The reviewed compatible plan places a versioned record in
the measured 328-byte gap from `0x6a8` to `0x7ef`, preserving existing Combo
offsets. A new versioned saved record and migration still need implementation.
Define defaults, reset, typed backup and restore, then measure the complete linked image. See the
[QMK Settings plan](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md).
The upstream structure size alone is not the feature's total resource cost.

## Resource and compatibility evidence

Every supported feature combination must be measured as a complete linked
image. Track both CODE windows, XRAM, internal RAM and stack placement. Shared
code, dead-code removal and outlining make individual probe costs non-additive.
Do not count loader, settings or journal space as free CODE. See
[Resource budget](RESOURCE-BUDGET.md) and the dated
[qualification evidence](../audits/rc6/roadmap-max-20261024/final/README.md).

Development builds run regression gates and profile-specific host and linked
CPU suites against the exact image. The full image additionally has a
reviewed control-stack and all-source interrupt allowance, under the documented
MCS-51 architectural contract. Other profiles need their own evidence before
packaging. Model tests do not establish physical behavior.

## Further code-size analysis

Review code reachable in each selected build: action and event handling, USB,
descriptors, Vial, macros, lighting, settings and build-time transforms. Compare
proposals against the complete current image, including interactions with
optional modules. Preserve behavior, interrupt safety, ABI and storage checks.
Keep rejected experiments out of production builds and retain their evidence
in technical reports. Do not reduce layers, macro capacity or existing
functionality to make a new option appear to fit. Storage changes need their own
backup and migration plan.

<a id="next-alpha-release"></a>

## Further profiles and releases

The full alpha.3 release is complete; its results are in [Status](STATUS.md).
Future work should qualify each newly selected feature identity separately.
Regenerate stack, interrupt, settings and packing evidence when their inputs
change. Matching schemas or passing isolated tests do not make profiles
interchangeable. Keep Windows/Linux installers, checksums and both installation
languages in subsequent releases. Keep device acceptance separate from models
and default tests offline or read-only. Any hardware write requires separate
confirmation.

## Other open work

Physical Combo timing, nonempty Combo writes, cold-start retention, power-loss
behavior and manual Windows/Linux GUI acceptance remain open. VialRGB Direct
remains RAM-only. Persistent palettes are outside this stage until their
storage and migration design is separately agreed.
