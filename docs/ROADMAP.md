Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

NKRO control, modifier One Shot and Space Cadet are available in the `full`
profile. Development profiles add compact Mouse Keys and Auto Shift individually and
together. These new profiles are source development builds;
they do not inherit the published alpha.3 qualification.
Their behavior and limits are listed in [Build profiles](BUILD-PROFILES.md).
The published and installed alpha.3 image is the exact full image described in
[Status](STATUS.md). Source changes since that release, including feature-profile
changes, are development work and are not approved for packaging or installation.

## Deferred features

The initial inventory contains 11 candidates. Five have bounded development
implementations; six remain deferred. A Vial control or keycode is
not evidence that a feature is enabled.

| Candidate | Open work |
| --- | --- |
| Tap Dance | The upstream probe has callback ABI blockers and moves fixed Combo storage; a compact implementation must preserve the Combo layout. |
| Key Overrides | The upstream probe has callback ABI blockers; modifier ownership and interactions with Repeat, Caps Word and macros remain open. |
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
CPU suites against the exact image. The exact published alpha.3 image has reviewed stack, interrupt and
settings-transition evidence. Source changes since that image need their own
evidence before packaging. Model tests do not establish physical behavior.

## Further code-size analysis

Review code reachable in each selected build: action and event handling, USB,
descriptors, Vial, macros, lighting, settings and build-time transforms. Compare
proposals against the complete current image, including interactions with
optional modules. Preserve behavior, interrupt safety, ABI and storage checks.
Keep rejected experiments out of production builds and retain their evidence
in technical reports. Do not reduce layers, macro capacity or existing
functionality to make a new option appear to fit. Storage changes need their own
backup and migration plan.

## Later releases

The alpha.3 release is published and installed. Compact Mouse Keys and Auto Shift
are available in development source profiles only, separately and together; the current changed profiles
have no release qualification. Any later release needs a fresh exact-image
review, platform builds, package acceptance and separate device authorization.
See [Status](STATUS.md) for the published image and current development source.

## Other open work

Physical Combo timing, nonempty Combo writes, cold-start retention, power-loss
behavior and manual Windows/Linux GUI acceptance remain open. VialRGB Direct
remains RAM-only. Persistent palettes are outside this stage until their
storage and migration design is separately agreed.
