Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The configurator lists sixteen supported development profiles. The `full`
feature set matches published alpha.3. Other profiles add compact Mouse Keys,
Auto Shift, GUI controls or Dynamic Macros in supported combinations. These
profiles are for development, not release or flashing. They have not inherited alpha.3's
image qualification or hardware evidence. See [Status](STATUS.md) and the
[compact-feature report](../audits/rc6/compact-runtime-20261024/README.md).

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
space-separated list of supported feature names. Only named combinations
listed by the configurator are valid. Two profiles require optional
`--short-calls`, as shown below. For example:

```sh
python tools/configure_firmware.py build --features nkro-control one-shot \
  --build-dir qmk-8051-ak820/.build/nkro-one-shot \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require
`--short-calls`, which remains off by default. Other supported profiles do not
require this option. Use a fresh build directory:

```sh
python tools/configure_firmware.py build --profile full-mouse-auto-shift-gui \
  --short-calls \
  --build-dir qmk-8051-ak820/.build/full-input \
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

`inspect` rechecks resource placement and image identity. Packaging is restricted
to the exact published alpha.3 image and its pinned inputs. A profile name such as
`full` does not authorize a changed source image. Current development profiles
are not release-qualified.

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
| `full-mouse` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys |
| `full-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, compact Auto Shift |
| `full-mouse-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys and Auto Shift |
| `full-gui-lock` | `nkro-control`, `one-shot`, `space-cadet`, GUI controls |
| `full-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, compact Dynamic Macros |
| `full-dynamic-macro-gui` | `nkro-control`, `one-shot`, `space-cadet`, compact Dynamic Macros and GUI controls |
| `full-mouse-auto-shift-gui` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys, Auto Shift and GUI controls |
| `full-auto-shift-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, compact Auto Shift and Dynamic Macros |

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
recorded in the [current matrix](../audits/rc6/compact-runtime-20261024/final/README.md).

The exact linked image determines resource use. Measure each profile from its
build report; feature costs are not additive. For the exact published alpha.3 `full` image, release evidence bounds main-path
stack use at 93 bytes, CRT at 2 bytes and all three IRQ paths at 61 bytes. Total
use is 156 of 162 bytes, with 6 bytes remaining. These figures do not qualify
changed source profiles. See [Status](STATUS.md) for evidence and limits.

## Deferred feature inventory

Six of the 11 original candidates have bounded development implementations:
NKRO control, One Shot, Space Cadet, Mouse Keys, Auto Shift and Dynamic Macros.
Magic is partly implemented through GUI controls. The five entries below
contain remaining work. The `full` profile selects NKRO control, One Shot and
Space Cadet; a Vial control alone does not establish firmware support.

| Deferred candidate | Open work |
| --- | --- |
| Tap Dance | Upstream probe has callback ABI blockers and moves fixed Combo storage; a compact implementation must preserve the Combo layout. |
| Key Overrides | Upstream probe has callback ABI blockers; modifier ownership and interactions with Repeat, Caps Word and macros remain open. |
| QMK Settings in Vial | A new versioned saved record, typed backup and restore, and migration still need implementation. The compatible plan preserves existing Combo offsets; see the [settings plan](../audits/rc6/roadmap-max-20261024/qmk-settings-plan.md). |
| Magic modifier swaps | GUI lock is available separately; modifier swaps and persistent settings remain open. |
| Leader | Bound sequence length, timeout and supported outputs. |

Console and Command remain disabled. Fault injection is a test facility, not a
selectable firmware feature. Existing FD00/FD01 diagnosis is read-only. The
configurator does not open USB or send keyboard commands.
