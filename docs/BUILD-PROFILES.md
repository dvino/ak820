Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The configurator builds and checks development images. All eight combinations
of the three implemented optional features can be selected. No configured
profile is approved for installation or release. Packaging remains blocked
until a whole-program stack bound, exact-image interrupt and nesting safety,
and the installer transition are qualified. See the [roadmap](ROADMAP.md) and
[qualification report](../audits/rc6/roadmap-max-20261024/final/README.md).

## Build a profile

Run commands from the repository root. Use one profile and a fresh build
directory under `qmk-8051-ak820`:

```sh
python tools/configure_firmware.py list
python tools/configure_firmware.py build --profile standard \
  --build-dir qmk-8051-ak820/.build/new \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

Choose any listed profile. The alternative `--features` selector accepts a
space-separated subset of `nkro-control`, `one-shot` and `space-cadet`; omit
values to select the standard feature set. For example:

```sh
python tools/configure_firmware.py build --features nkro-control one-shot \
  --build-dir qmk-8051-ak820/.build/nkro-one-shot \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`--profile` and `--features` are alternative selectors. `build` links the
image, checks both CODE windows and RAM placement, then runs the standard
regression gates and the selected feature's host and linked-CPU suites against
the exact image. It records the configuration, qualification and profile
suite results in the build directory. These offline checks do not validate a
physical keyboard or establish release safety.

To inspect a completed build again, run:

```sh
python tools/configure_firmware.py inspect --build-dir qmk-8051-ak820/.build/new --toolchain toolchains/sdcc-4.6.0
```

`inspect` rechecks resource placement and image identity. `package` always
stops: no configured profile is approved for release, regardless of a
successful development build.

## Profiles

All profiles retain the base feature set: six layers, 16 Vial macros, eight
two-key Combos, compact tap-hold, encoder mapping, media keys, NKRO report
support, Caps Word, Repeat and Alt Repeat, Grave Escape, Tri Layer, RGB effects
and VialRGB Direct in RAM. Combo timing remains 40 ms; compact tap-hold remains
200 ms. Runtime QMK Settings are disabled. Optional features are build-time
choices.

| Profile | Optional features |
| --- | --- |
| `standard` | None |
| `nkro` | `nkro-control` |
| `one-shot` | `one-shot` |
| `nkro-one-shot` | `nkro-control`, `one-shot` |
| `space-cadet` | `space-cadet` |
| `nkro-space-cadet` | `nkro-control`, `space-cadet` |
| `one-shot-space-cadet` | `one-shot`, `space-cadet` |
| `full` | `nkro-control`, `one-shot`, `space-cadet` |

NKRO control provides `NK_ON`, `NK_OFF` and `NK_TOGG`. The selected report mode
lasts until restart; restart uses the saved/default mode. Switching clears
held keys and pending actions, so release held keys before pressing them again.
No setting is written to flash. This does not enable other Magic actions.

One Shot supports modifier combinations. Tap OSM, then a key: its modifiers
apply until that key is released. Several queued modifier sets combine. Holding
OSM acts as a normal modifier. While a consuming key remains down, another OSM
acts only as a held modifier. Matrix keys and both encoder directions are
supported. Layer One Shot, timeout, locking and tap-toggle are absent. Assigning
an OSM key in Vial is supported; injecting a virtual OSM event from Vial or a
macro is not.

Space Cadet maps `SC_LSPO` to left Shift while held and Shift + `9` (`(`) when
tapped; `SC_RSPC` maps to right Shift while held and Shift + `0` (`)`) when
tapped; `SC_SENT` maps to right Shift while held and Enter when tapped. These
keys use the existing compact tap-hold path and its modifier ownership. Space
Cadet keycodes cannot be used as Combo inputs. The implementation does not
include the full upstream Space Cadet engine. Tested edge cases and limits are
recorded in the [Space Cadet report](../audits/rc6/roadmap-max-20261024/space-cadet.md).

The exact linked image determines resource use. Measure each profile from its
build report; feature costs are not additive. The configurator checks resource
placement but does not establish a qualified runtime stack allowance.

## Deferred feature inventory

Three of the 11 candidates have bounded implementations in development
profiles. The other eight remain deferred. A client control alone does not
establish firmware support.

| Deferred candidate | Open work |
| --- | --- |
| Tap Dance | Upstream probe has callback ABI blockers and moves fixed Combo storage; a compact implementation must preserve the Combo layout. |
| Key Overrides | Upstream probe has callback ABI blockers; modifier ownership and interactions with Repeat, Caps Word and macros remain open. |
| Mouse Keys | The upstream probe exceeds the main CODE window by 1,381 bytes; a smaller scope and scan-time review are needed. |
| Auto Shift | Needs explicit C `case` labels instead of GNU case ranges; the upstream probe exceeds the main CODE window by 2,081 bytes. |
| QMK Settings in Vial | A new versioned saved record, typed backup and restore, and migration still need implementation. The compatible plan preserves existing Combo offsets; see the [settings plan](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md). |
| Magic | Modifier swaps and GUI control need separate compatibility and persistence review. |
| Leader | Bound sequence length, timeout and supported outputs. |
| Dynamic macros | Bound recording RAM and qualify replay; existing Vial macros remain available. |

Console and Command remain disabled. Fault injection is a test facility, not a
selectable firmware feature. Existing FD00/FD01 diagnosis is read-only. The
configurator does not open USB or send keyboard commands.

Probe details are in the [feature report](../audits/rc6/roadmap-max-20261024/feature-probes.md).
