Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The configurator lists 24 named development profiles. The `full` feature set
matches published alpha.3. Each new module profile retains `full` and adds its
named module alone; the three modules are not combined. Other profiles add compact Mouse Keys, Auto Shift,
GUI controls, modifier swaps, Dynamic Macros, Leader or OS indicators in the
supported combinations below. These source profiles require their own exact
image qualification. Every configured build proves whole-image foreground,
startup and interrupt stack bounds before its regression suites; unknown bounds
or overflow fail the build. See [Status](STATUS.md) for current verification.

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
listed by the configurator are valid. The three new module profiles require `--short-calls`. Two earlier profiles also require it, as shown below. For example:

```sh
python tools/configure_firmware.py build --features nkro-control one-shot \
  --build-dir qmk-8051-ak820/.build/nkro-one-shot \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`full-mouse-auto-shift-gui`, `full-auto-shift-dynamic-macro`, `full-tap-dance`,
`full-key-overrides` and `full-qmk-settings` require `--short-calls`, which is
off by default. Earlier short-call qualification variants also exist for `full`
and `full-mouse-auto-shift`. Use a fresh build directory:

```sh
python tools/configure_firmware.py build --profile full-mouse-auto-shift-gui \
  --short-calls \
  --build-dir qmk-8051-ak820/.build/full-input \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`--profile` and `--features` are alternative selectors. `build` links the
image, checks both CODE windows and RAM placement, then proves stack and
interrupt bounds for the exact image before running standard regression gates
and the selected feature's host and linked-CPU suites. An unknown required
bound or stack overflow fails the build. It records the configuration,
qualification and profile suite results in the build directory. These offline
checks do not validate a physical keyboard or establish release safety.

To inspect a completed build again, run:

```sh
python tools/configure_firmware.py inspect --build-dir qmk-8051-ak820/.build/new --toolchain toolchains/sdcc-4.6.0
```

`inspect` rechecks resource placement and image identity. To rerun the runtime
proof for an existing build, use:

```sh
python tools/configure_firmware.py check-runtime \
  --build-dir qmk-8051-ak820/.build/new \
  --toolchain toolchains/sdcc-4.6.0
```

See [Runtime stack check](RUNTIME-STACK.md) for scope and assumptions.
Packaging is restricted
to the exact published alpha.3 image and its pinned inputs. A profile name such as
`full` does not authorize a changed source image. Current development profiles
are not release-qualified.

## Profiles

All profiles retain the base feature set: six layers, 16 Vial macros with an
8192-byte buffer, eight two-key Combos at the fixed `0x658` offset, compact tap-hold, encoder mapping, media keys, NKRO report
support, Caps Word, Repeat and Alt Repeat, Grave Escape, Tri Layer, RGB effects
and VialRGB Direct in RAM. Default Combo timing is 40 ms and default compact
tap-hold timing is 200 ms. `full-qmk-settings` changes these through QSIDs 2 and 7.
Runtime QMK Settings are available only in `full-qmk-settings` and remain a
source-only development feature. Only the three new module profiles use schema
`0x082003`; the legacy `0x082002` format is unchanged. Optional modules are
build-time choices.

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
| `full-leader` | `nkro-control`, `one-shot`, `space-cadet`, compact Leader |
| `full-mouse` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys |
| `full-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, compact Auto Shift |
| `full-mouse-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys and Auto Shift |
| `full-gui-lock` | `nkro-control`, `one-shot`, `space-cadet`, GUI controls |
| `full-ctrl-gui` | `nkro-control`, `one-shot`, `space-cadet`, GUI controls, left/right Ctrl↔GUI swap |
| `full-os-indicators` | base `full` features and volatile FD02 OS indicator control |
| `full-mac-pc` | base `full` features and volatile left/right Alt/GUI swap |
| `full-mac-pc-os-indicators` | `full-mac-pc` plus volatile FD02 OS indicator control |
| `full-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, compact Dynamic Macros |
| `full-dynamic-macro-gui` | `nkro-control`, `one-shot`, `space-cadet`, compact Dynamic Macros and GUI controls |
| `full-mouse-auto-shift-gui` | `nkro-control`, `one-shot`, `space-cadet`, compact Mouse Keys, Auto Shift and GUI controls |
| `full-auto-shift-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, compact Auto Shift and Dynamic Macros |
| `full-tap-dance` | `full` plus compact Tap Dance |
| `full-key-overrides` | `full` plus compact Key Overrides |
| `full-qmk-settings` | `full` plus typed QMK Settings |

`full-leader` selects an existing Vial macro with a physical `QK_LEAD` prefix
and one basic selector within 300 ms. `1`–`9`, `0`, `A`–`F` map to slots
0–15. Macro contents remain editable in Vial. Encoder and virtual prefixes,
longer sequences and a configurable dictionary are absent. See [Leader](COMPACT-LEADER.md).

`full-ctrl-gui` adds `CG_SWAP`, `CG_NORM` and `CG_TOGG`. They swap both left
and right Ctrl/GUI output mappings and reset on reboot. Mapping happens before
GUI lock; modifier owners remain intact. The mapping is volatile and does not
enable persistent Magic settings. See [GUI controls](GUI-CONTROL.md).

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
include the full upstream Space Cadet engine. Tested feature edge cases and limits are
recorded in the historical [compact-feature matrix](../audits/rc6/compact-runtime-20261024/final/README.md). The earlier exact-image runtime baseline is documented in the [runtime stack report](../audits/rc6/leader-next-20261024/final/README.md); it does not qualify these changed profiles.

The exact linked image determines resource use. Measure each profile from its
build report; feature costs are not additive. For the exact published alpha.3 `full` image, release evidence bounds main-path
stack use at 93 bytes, CRT at 2 bytes and all three IRQ paths at 61 bytes. Total
use is 156 of 162 bytes, with 6 bytes remaining. These figures do not qualify
changed source profiles. See the earlier [runtime baseline](../audits/rc6/leader-next-20261024/final/README.md), current [qualification scope and results](../audits/rc6/web-firmware-20261024/runtime-all/README.md), and [Status](STATUS.md).

## Remaining limits

The three compact modules are available only in their named development profiles. They are not release-approved. Each profile adds its own module to `full`; the three modules are not combined in one profile. Their exact behavior, rejected inputs, storage and protocol limits are documented in [Tap Dance](COMPACT-TAP-DANCE.md), [Key Overrides](COMPACT-KEY-OVERRIDES.md), [QMK Settings](QMK-SETTINGS.md) and [module storage](MODULE-STORAGE.md).

Magic support remains limited to volatile GUI controls and volatile Ctrl/GUI or Alt/GUI mapping in selected profiles. Caps variants and persistent Magic settings are outside the current module contract. See [GUI controls](GUI-CONTROL.md) and [Mac/PC mode](MAC-PC.md). Console and Command remain disabled.
