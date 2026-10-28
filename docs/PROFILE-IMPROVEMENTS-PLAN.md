Русский перевод: [План развития профилей](ru/PROFILE-IMPROVEMENTS-PLAN.md).

# Plan: profile improvements and custom firmware builds

This is a discussion plan, not a claim that proposed features are implemented or that firmware is ready to install. The measurements below were supplied by the owner as provisional figures for particular built images; they may change with the sources. Space in separate CODE windows is not interchangeable. The cost of modules and settings can only be determined after linking the specific combination. This document does not authorize changes to the current optimization work or flashing a device.

## Common foundation

All ten profiles contain six layers, encoder actions, 16 persistent Vial macros, eight two-key Combos, Mod-Tap/Layer-Tap, One Shot, Caps Word, Repeat/Alt Repeat, Tri Layer, basic lighting and the supported QMK Settings. A profile is a firmware composition, not a switchable layer. Actions configurable in Vial do not add a module that is absent from the firmware. See the [module matrix](MODULE-MATRIX.md) and [profile descriptions](profiles/README.md).

Compare current contents against `qmk-8051-ak820/util/ak820_profiles.py`, not just the descriptions or an older build. “Maximize” means maximizing usefulness for the profile's purpose while preserving existing features, not promising that every module will fit.

## Candidates for each profile

Free bytes in the table are main CODE / low CODE / XRAM. CODE headroom is window size minus occupied bytes, not necessarily trailing space or capacity where new code can be placed; XRAM headroom is ordinary external RAM capacity minus its used size. The [measurement record](../work-logs/profile-headroom-20261028/measurements.md) identifies the measured images, source manifests and method. Candidate order reflects usefulness, not proven size; each addition requires separate measurement and interaction tests. Do not remove existing features to make room without a separate owner decision.

| Profile | Current purpose and notable features | Headroom, bytes | First things to investigate |
| --- | --- | --- | --- |
| `main` | General-purpose, including Auto Shift, Leader, Key Overrides, temporary macros and Direct. | 170 / 5 / 154 | Settings and improvements to existing features below. Do not plan Tap Dance: previous attempts to fit it have been made and substantial optimization headroom is not expected. |
| `game` | Gaming: NKRO for simultaneous key presses, Win lock and Direct; no Leader or Auto Shift. | 210 / 5 / 81 | Small improvements to gaming controls and their indications; evaluate useful settings without affecting latency or key release. Do not assume large modules will fit. |
| `mmo` | Games with multiple actions: NKRO, Win lock, Tap Dance and Direct; no Leader or Key Overrides. | 371 / 5 / 80 | Improvements to existing Tap Dance and its limits if justified by a gaming scenario; separately check cost and interactions. Do not promise to restore Key Overrides. |
| `typing` | Text entry: Auto Shift and Space Cadet, a Shift key with an additional action on a short press; Leader and Key Overrides, no Direct. | 1853 / 28 / 661 | First evaluate Tap Dance to reduce movement and/or NKRO, then typing-comfort settings and Combo + Auto Shift. Do not assume the combination fits without a build. |
| `code` | Programming: Space Cadet and Grave Escape, which selects Escape or Grave based on a modifier; Leader and Key Overrides, no Direct. | 2217 / 28 / 672 | Evaluate Tap Dance for editor shortcuts, then NKRO and useful small settings; account for the fact that current Tap Dance does not emit macros or layers. |
| `pointer` | Keyboard-controlled pointer: Mouse Keys, Leader and Key Overrides; no Direct. | 1766 / 28 / 653 | Mouse Keys speed and convenience settings; evaluate Tap Dance and NKRO without degrading mouse-button holds or accessibility of control. |
| `onehand` | One-handed use: Mouse Keys, Tap Dance and Leader; no Key Overrides or Direct. | 1914 / 28 / 628 | Investigate One Shot and timing for reduced movement range, Mouse Keys settings, then possible Key Overrides; preserve one-handed usability. |
| `creative` | Application shortcuts, Direct, Leader, temporary macros and Tap Dance; no Key Overrides. | 820 / 5 / 147 | Check whether useful Tap Dance improvements or Key Overrides fit; separately investigate NKRO. Distinguish persistent macros from temporary macros. |
| `shortcuts` | Prepared commands: Leader, Key Overrides and Tap Dance; no temporary macros or Direct. | 1988 / 28 / 611 | Evaluate adding temporary macros and NKRO, and improving Leader. Check usefulness and the complete combination together. |
| `multios` | Switches Ctrl/GUI and Alt/GUI keys for different OSes; Leader and Key Overrides, no Direct. Switching applies to the current session; the OS is not detected automatically. | 2302 / 28 / 679 | Evaluate Tap Dance and NKRO, then switching convenience and clear mode indication without promising automatic OS detection. |

For each candidate, first clarify the user scenario and existing limitations, then build a control and candidate with the same toolchain. Keep a change only when it is useful, has acceptable latency, works correctly with other modules and leaves sufficient headroom. A module's absence from a profile does not by itself make adding it useful.

## Settings and feature interactions

1. Configurable Leader timeout. Retain the current 300 ms default; determine the range after studying the implementation and interfaces. Check its representation in Vial and AK Configurator, identifier and storage compatibility.
2. Auto Shift can already be disabled persistently through QSID 3 and temporarily through `AS_OFF`/`AS_TOGG`; it is enabled by default in `main` and `typing`. Determine how to make disabling it clear and convenient in the interface and documentation; do not add a duplicate setting. Changing the default requires a separate owner decision.
3. Consider allowing Caps Word activation gestures (both Shifts and double left Shift) to be disabled while retaining the assignable `CW_TOGG` action and user Combos. The owner prefers double Shift; check gesture and Combo interactions before changing behavior. This is a candidate, not a confirmed low-cost feature.
4. Double left Shift currently uses `GET_TAPPING_TERM`, not an independent interval; existing QSID 7 changes the general tap/hold time. Investigate the need for an independent interval and its cost without presenting duplicate functionality as an existing setting.
5. Investigate passing through an unsuitable ordinary key after Leader instead of consuming it. A behavior change or toggle requires a separate decision; digits and A–F remain selectors.
6. Investigate Combo + Auto Shift: currently, when a Combo input does not form a combination, it bypasses Auto Shift. Evaluate a solution without breaking timing, press/release ownership, successful Combo handling, modifiers or memory limits. Do not promise it will fit.
7. For `pointer`/`onehand`, evaluate genuinely useful pointer and scrolling speed parameters; for other profiles, add settings only for confirmed scenarios. Study Mod-Tap modes for rapid overlapping presses separately: changing the logic is riskier than adjusting ordinary timing.

The existing QMK Settings record is versioned, CRC-checked and requires reserved bytes to be zero. A new persistent parameter needs compatibility with the immediately preceding version, safe migration without losing user settings, NVM error handling, range checks, interface verification and exact-image measurement. Do not use an unsupported QSID without checking the protocol and client.

## Custom firmware builder

Goal: a novice can choose desired capabilities, understand trade-offs and build a custom configuration. Provide an accessible interactive mode with clear questions and a non-interactive CLI for automation; a TUI is acceptable if it genuinely simplifies choice but is not a required dependency. Offer a starting profile, explain names in plain language and explicitly show what is already enabled.

Starting point: `tools/configure_firmware.py` already builds and checks known profiles without USB access, while `ak820_profiles.select()` currently accepts only predefined combinations; `CONFLICTS` is currently empty, which does not prove there are no conflicts. Reuse existing tools and qualification rather than presenting an arbitrary selection as a supported profile. Check the availability of the pinned SDCC and dependencies on target operating systems; do not promise platform support before testing.

Builder plan:

1. Create one testable catalog of capabilities, dependencies, limitations and interactions based on code and tests: what is absent, required, incompatible, works only with limitations (such as Combo + Auto Shift), or remains unverified. Show the reason and remedies; do not label unknown combinations compatible. Check module combinations and the actual supported actions, not just names.
2. Provide interactive selection and a CLI with the same validation, safe defaults, cancellation, clear errors and a review of selected capabilities, without requiring terminal expertise. Do not perform USB operations during selection or building.
3. Build selected combinations from explicitly specified switches using the pinned toolchain and a separate output directory. Check both physical CODE windows, XRAM, IRAM and stack; estimates do not replace linking. On overflow, report the specific region and measured excess and let the user remove modules manually; never remove them automatically.
4. Run exact-image startup, foreground and all permitted IRQ checks plus relevant regression and interaction tests before presenting a result as qualified. If a check is unknown or not run, clearly say the image is unqualified; do not equate a successful build with safe firmware installation.
5. Record composition, source and tool versions, image hashes and test results. Design capability identification and settings/backup transitions for arbitrary compositions; current catalogs and identity checks accept known configurations. Do not weaken installer, backup or NVM checks.
6. Provide plain-language instructions that distinguish building from installation. Do not flash automatically; prepare a recovery path and backup. Flashing, entering the bootloader and USB writes require separate authorization and existing exact-image checks. Current installer policy does not automatically authorize an arbitrary image.
7. Test empty and invalid input, cancellation, unknown or duplicate modules, incompatibilities, missing tools, overflow in each region, interrupted builds, paths with spaces, reruns and corrupt outputs; do not overwrite others' data. Add tests for both interfaces and message quality.

## Order and completion criteria

First document and confirm profile priorities and user scenarios; then measure candidates separately and in selected combinations. Investigate the Leader setting and Combo + Auto Shift improvement first in `main`, without changing anyone else's active work in parallel. For every final image record identity, both CODE windows, XRAM, IRAM/stack, exact-image verification results and tests. Update related Russian and English descriptions and the capability catalog along with implementation. Independent review is required before committing. Do not infer physical behavior or device flashing safety from offline tests.
