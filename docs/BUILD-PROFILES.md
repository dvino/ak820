Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The planned desktop configurator will offer nine ready-made profiles. Choose a profile as a
whole; the application does not combine independent module switches. The
`work` profile is the default. It includes NKRO control, One Shot, Space Cadet,
Leader, Dynamic Macros and OS indicator control. Mouse Keys and Mac/PC mode are
off in `work`; choose `mouse` or `system` when those functions are needed.

The profile list and each profile's enabled modules come from the firmware
registry. Older development profile names remain available through the
low-level CLI to reproduce previous builds; they are not separate choices in
the desktop configurator. No profile contains every optional module.

| Profile | Intended use | Package-specific modules |
| --- | --- | --- |
| `work` | General work; default choice | Leader, Dynamic Macros, OS indicator control |
| `essential` | Core typing controls | OS indicator control |
| `typing` | Typing with held-key Shift behavior | Auto Shift, OS indicator control |
| `mouse` | Keyboard pointer and scroll controls | Mouse Keys, OS indicator control |
| `mouse-typing` | Mouse controls and Auto Shift | Mouse Keys, Auto Shift, GUI lock, OS indicator control |
| `system` | Switch modifier mappings for Windows, Linux or macOS | GUI lock, Ctrl/GUI swap, Mac/PC Alt/GUI swap, OS indicator control |
| `tap-dance` | Configure tap and hold actions per key | Tap Dance |
| `key-overrides` | Replace keys under selected modifiers | Key Overrides |
| `settings` | Change supported timing and behavior values | QMK Settings |

Every package also includes the common NKRO control, modifier One Shot and limited
Space Cadet controls. The shared base features are six layers, 16 Vial macros
with an 8192-byte buffer, eight two-key Combos, compact tap-hold, encoder mapping,
media and system keys, NKRO reports, Caps Word, Repeat and Alt Repeat,
Grave Escape, Tri Layer, RGB effects and VialRGB Direct. The [feature catalog](FEATURES.md)
explains behavior and limits. The [module matrix](MODULE-MATRIX.md) lists
compatibility and measured resource use for all nine profiles.

## Build a profile

Run commands from the repository root. Create a new build directory beneath
`qmk-8051-ak820` for every build. `work` is selected when `--profile` is
omitted; curated profiles automatically use the checked short-call option with
the pinned SDCC 4.6.0 toolchain.

```sh
python tools/configure_firmware.py list
python tools/configure_firmware.py build --profile work \
  --build-dir qmk-8051-ak820/.build/work \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`list` reports the curated `release_profiles` separately from compatibility
profiles retained for previous development builds. `build` links the image,
checks both CODE windows and RAM placement, proves stack and interrupt bounds
for that exact image, then runs its offline regression suites. An unknown
required bound or overflow fails the build. Passing offline checks does not
prove physical keyboard behavior or approve an image for release.

To inspect an existing build:

```sh
python tools/configure_firmware.py inspect --build-dir qmk-8051-ak820/.build/work --toolchain toolchains/sdcc-4.6.0
```

To rerun its runtime proof:

```sh
python tools/configure_firmware.py check-runtime \
  --build-dir qmk-8051-ak820/.build/work \
  --toolchain toolchains/sdcc-4.6.0
```

See [runtime stack check](RUNTIME-STACK.md) for the proof's scope. Current
qualification results and release state are in [Status](STATUS.md). The published `v0.6.0-alpha.3` image is unchanged.
