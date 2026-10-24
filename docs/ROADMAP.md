Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

NKRO control, modifier One Shot and Space Cadet are available in the `full`
profile. Development profiles add compact Mouse Keys, Auto Shift, GUI controls, volatile Ctrl/GUI swaps,
Dynamic Macros and Leader in supported combinations. The configurator
provides eighteen named profiles; the qualified matrix covers twenty variants: the named
profiles plus `full` and `full-mouse-auto-shift` with `--short-calls`. These profiles are source development builds; they do not inherit the published alpha.3 qualification.
Their behavior and limits are listed in [Build profiles](BUILD-PROFILES.md).
The published and installed alpha.3 image is the exact full image described in
[Status](STATUS.md). Source changes since that release, including feature-profile
changes, are development work and are not approved for packaging or installation.

## Deferred features

The initial inventory contains 11 candidates. Bounded implementations now
cover NKRO control, One Shot, Space Cadet, Mouse Keys, Auto Shift, GUI lock and
Dynamic Macros and Leader. A Vial control or keycode alone does not show that a feature is
enabled.

| Candidate | Open work |
| --- | --- |
| Tap Dance | The upstream probe has callback ABI blockers and moves fixed Combo storage; a compact implementation must preserve the Combo layout. |
| Key Overrides | The upstream probe has callback ABI blockers; modifier ownership and interactions with Repeat, Caps Word and macros remain open. |
| QMK Settings in Vial | A new versioned saved record, typed backup and restore, and migration still need implementation. The compatible plan preserves existing Combo offsets; see the [settings plan](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md). |
| Other Magic changes | Ctrl/GUI swap is available in `full-ctrl-gui`; other modifier swaps, including Alt/Caps variants, and persistent settings remain open. |

The available implementations are intentionally limited. NKRO control
adds only `NK_ON`, `NK_OFF` and `NK_TOGG`; One Shot handles modifier combinations
without layer form, timeout or locking; Space Cadet handles `SC_LSPO`, `SC_RSPC`
and `SC_SENT` through compact tap-hold. See [Build profiles](BUILD-PROFILES.md)
for exact behavior and tested interactions.
GUI lock controls are described in [GUI controls](GUI-CONTROL.md). Compact
Dynamic Macros provide two volatile slots of 16 completed taps; see the
[user guide](COMPACT-DYNAMIC-MACROS.md) for exclusions and playback behavior.
Compact [Leader](COMPACT-LEADER.md) selects one of the 16 existing Vial macros
with `QK_LEAD` followed by a single selector within 300 ms. Longer sequences
and a configurable sequence dictionary are not implemented.

## Runtime settings and saved data

`QMK_SETTINGS = no` in alpha.3 and configured development profiles. Vial
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
[Resource budget](RESOURCE-BUDGET.md), the historical [compact-feature matrix](../audits/rc6/compact-runtime-20261024/final/README.md), and the current exact-image [runtime stack report](../audits/rc6/leader-next-20261024/final/README.md).

Every new source profile or image must pass exact-image stack and IRQ proof
before other regression gates; unknown bounds or overflow fail the build.
`check-runtime` reruns the proof on an existing build. Regression gates and
profile-specific host and linked CPU suites then run against the exact image.
The exact published alpha.3 image has reviewed stack, interrupt and
settings-transition evidence. Source code, linked-image CPU results and the
actual installed or released alpha.3 are separate facts. Source changes need their own stack and IRQ
evidence before other regressions and any release review. Model tests do not
establish physical behavior.

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

The alpha.3 release is published and installed. Compact Mouse Keys, Auto Shift, GUI controls, volatile Ctrl/GUI swaps,
Dynamic Macros and Leader are available in development source profiles only. Changed
profiles have no release qualification. Any later release needs a fresh exact-image
review, platform builds, package acceptance and separate device authorization.
See [Status](STATUS.md) for the published image and current development source.

## Other open work

Physical Combo timing, nonempty Combo writes, cold-start retention, power-loss
behavior and manual Windows/Linux GUI acceptance remain open. VialRGB Direct
remains RAM-only. Persistent palettes are outside this stage until their
storage and migration design is separately agreed.
