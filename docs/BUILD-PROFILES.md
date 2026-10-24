Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The configurator builds and checks development images. No profile is approved
for installation or release. The build runs offline tests against the exact
linked image, but it does not prove a whole-program stack bound or exact-image
interrupt and nesting safety. The installer transition for a new feature
identity is also not approved. The `package` command therefore always stops.
The remaining work is listed in the [roadmap](ROADMAP.md). Evidence is in the
[profile qualification report](../audits/rc6/configurable-20261024/qualification.md).

## Build a profile

Run commands from the repository root. Select one profile and a fresh build
directory under `qmk-8051-ak820`:

```sh
python tools/configure_firmware.py list
python tools/configure_firmware.py build --profile standard \
  --build-dir qmk-8051-ak820/.build/new \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

Replace `standard` with `nkro` or `one-shot` to select that option. The
alternative `--features` form accepts no value (no optional feature),
`nkro-control`, or `one-shot`. For example, use `--features nkro-control` to
select NKRO. Do not combine the two optional features: that image exceeds the
main CODE window. `--profile` and `--features` are alternative selectors.

`build` creates and links the image, checks both CODE windows and RAM placement,
then runs the offline host and CPU regression suite against that exact image.
It writes `configuration-report.json`, `qualification.json` and
`profile-tests/results.json` in the build directory. The profile tests include
the gate checks and, when selected, the option’s host and linked CPU tests. These checks do not validate a physical keyboard. To inspect an
existing build again, run:

```sh
python tools/configure_firmware.py inspect --build-dir qmk-8051-ak820/.build/new --toolchain toolchains/sdcc-4.6.0
```

`inspect` rechecks the linked resources and image identity. `package` uses the
same build directory and toolchain arguments, then refuses because the release
evidence and installer transition listed above are missing. A successful
development build is not an installable package.

## What each profile contains

All profiles retain six layers, 16 Vial macros, eight two-key Combos, Grave
Escape and NKRO report support. Combo timing remains 40 ms and compact tap-hold
timing remains 200 ms. Runtime QMK Settings are disabled; profile selection is
a separate build-time choice.

| Profile | Optional feature | Behavior and limit |
| --- | --- | --- |
| `standard` | None | Base feature set only. |
| `nkro` | NKRO control (`NK_ON`, `NK_OFF`, `NK_TOGG`) | Selects the report mode until restart. Restart uses the saved/default mode. Switching clears held keys and pending actions; release those keys before pressing them again. No setting is written to flash. |
| `one-shot` | One Shot modifiers (`OSM`) | Tap OSM, then a key: its modifiers apply until that key is released. Several queued modifier sets combine. Holding OSM acts as a normal modifier. While a consuming key remains down, another OSM acts only as a held modifier. Matrix keys and both encoder directions work. OSL, timeout, locking and tap-toggle are absent. Assigning an OSM key in Vial is distinct from injecting a virtual OSM event from Vial or a macro; those injected events are not supported. |

The exact linked image determines resource use. Measure both CODE windows and
RAM from each build report; feature costs are not additive, so a delta from one
profile cannot predict another. The configurator checks allocation limits but
does not claim a qualified runtime stack allowance.

## Implementation inventory

Two of the 11 roadmap candidates have compact implementations. The others
remain deferred. A client control alone does not establish firmware support.

| Candidate | Current status or limit |
| --- | --- |
| One Shot | Implemented only as the bounded modifier behavior described above; layer form and other behaviors are not included. |
| Tap Dance | Deferred; dynamic entries, shared input ownership and full-image cost need qualification. |
| Key Overrides | Deferred; modifier ownership and interactions with Repeat, Caps Word and macros need qualification. |
| Mouse Keys | Deferred; mouse reports, scan timing and full-image cost need qualification. |
| Auto Shift | Deferred; interactions with tap-hold, Combos and Caps Word need qualification. |
| NKRO control | Implemented only as the three report-mode actions described above; this does not enable all Magic actions. |
| QMK Settings in Vial | Disabled at runtime. Upstream setting IDs 1, 2, 7, 8, 18, 19, 20 and 21 are inventory items, not a promise that their controls are accepted. The upstream structure is 36 bytes and changes the dynamic layout around Combo data at `0x658`; versioning, independent typed backup, defaults and migration must be qualified before enabling it. Existing Combo and tap-hold timing stays fixed at 40 ms and 200 ms. |
| Magic | Deferred; modifier swaps and GUI-key control require separate compatibility and persistence review. |
| Leader | Deferred; sequence length, timeout and supported outputs need bounds. |
| Space Cadet | Deferred; tap-hold ownership and cancellation need qualification. |
| Dynamic macros | Deferred; recording RAM and replay behavior need qualification. The existing 16 Vial macro slots remain available. |

### Diagnostic exclusions

Console and Command remain disabled. Offline fault injection is a test facility,
not a selectable firmware feature. Existing read-only FD00/FD01 diagnosis remains
present. The configurator itself never opens USB or sends keyboard commands.
