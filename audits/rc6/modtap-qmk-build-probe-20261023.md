# QMK tap engine size probe

Date: 2026-10-23. The isolated build tested whether the retained QMK tapping
engine can be enabled within the AK820 application CODE window. The build
failed the existing size limit. No source change was made in the primary
checkout, and no device operation was performed.

## Probe setup

The disposable worktree is `/tmp/ak820-modtap-qmk-probe`, branch
`codex/modtap-qmk-probe`, based on primary `7f7aa478e82d747141a409786b7c309cc465174d`.
Only the probe copy of `qmk-8051-ak820/keyboards/ajazz/ak820/config.h` changed:

```diff
-#define NO_ACTION_TAPPING
#define TAPPING_TERM 200
#define QUICK_TAP_TERM 0
```

`HOLD_ON_OTHER_KEY_PRESS` and `NO_ACTION_ONESHOT` remain defined; no other
feature flag or keymap changed. The pinned LUFA files were copied from the
primary checkout and passed the lock-file check. The existing QMK virtual
environment was used by absolute path. No dependency version changed.

From the worktree's `qmk-8051-ak820` directory, the build command was:

```sh
python3 util/build_ak820.py \
  --toolchain /home/danil/Documents/git/ak820/toolchains/sdcc-4.6.0 \
  --qmk-bin /home/danil/Documents/git/ak820/qmk-8051-ak820/.venv/bin/qmk \
  --build-dir .build/modtap-qmk-probe-20261023b
```

The toolchain reports SDCC 4.6.0 #16555. Its SHA256 is
`3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`; the
assembler SHA256 is
`2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877`.
The builder retained its normal `--opt-code-size`, exact outlining, audited
callee-save list and address windows. No expanded ceiling or feature removal
was used.

## Result

The link completed, but the builder rejected the image with:

```text
ValueError: Linked code outside permitted interval: 0xc700..0xcc0d
```

The candidate memory report records 41,719 bytes in ROM/EPROM/FLASH from
`0x28A0` through `0xCC0D`: 1,808 bytes in the low window and 39,911 bytes in
the main window. The permitted windows remain `0x28A0..0x2FFF` and
`0x3027..0xC6FF`; the main-window occupancy therefore exceeds its ceiling by
1,294 bytes. This is 3,650 bytes above the baseline's 36,261-byte main-window
occupancy. The candidate crosses the ceiling, so it is not a build success or
an installable artifact.

| Resource | Baseline | QMK tapping opt-in | Change |
| --- | ---: | ---: | ---: |
| Reported linked CODE | 38,069 bytes | 41,719-byte mapped span | +3,650 bytes by window occupancy |
| Main CODE window | 36,261 bytes | 39,911 bytes | +3,650 bytes |
| Low CODE window | 1,808 bytes | 1,808 bytes | 0 bytes |
| XRAM | 2,066 bytes | 2,238 bytes | +172 bytes |
| Initial SP | `0x62` | `0x62` | unchanged |
| Allocated stack capacity | 157 bytes | 157 bytes | unchanged |

The baseline is the exact artifact in
`qmk-8051-ak820/.build/goal-baseline-20261023/build-report.json`, with IHX
SHA256 `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`.
That report records SDCC 4.6.0 #16555, 38,069 CODE bytes, 36,261 main-window
bytes, 1,808 low-window bytes, and an XRAM span of 2,066 bytes. The candidate
IHX SHA256 is
`5dab28c60a85c805cc7de4a52179d25a5eb42f7184fe5c2db37e2f16247ed558`;
its map SHA256 is
`ada9a283813047bc7f682ceeaf4babd754236c61b5cc67bb260841e67957e5c3`, and its
memory report SHA256 is
`86dec0bbc53b3651c90a86aa0465fbe30a5062773d0b6fe559cfb80efe4f9941`.

The full compiler log, linked map, memory report and IHX are retained in
`/tmp/ak820-modtap-qmk-probe/qmk-8051-ak820/.build/modtap-qmk-probe-20261023b/`.
The report and map were generated before the builder rejected the size; a
successful `build-report.json` was not produced. The IHX is a failed probe
artifact and must not be packaged or installed. Allocated stack capacity is
not a measured worst-case stack bound.

## Scope

This measures the linked cost of removing `NO_ACTION_TAPPING` while keeping
the requested flags. Removing that flag also disables the compact byte
decoder guard in `keymap_common.c` and selects the generic decoder, which
emits real Mod-Tap and Layer-Tap actions. This therefore measures decoder
and engine enrollment together. It does not prove working runtime behavior
or that all newly compiled tapping paths
are safe for this port. With tapping enabled, the `OP_TAP_TOGGLE` layer-tap
case guarded by `NO_ACTION_TAPPING` becomes available; `NO_ACTION_ONESHOT`
remains set, so the One Shot action continues through its existing momentary
layer fallback. No runtime, host/CPU, physical-device or installation test
was run. Existing release sources, the installed image and keyboard behavior
were not changed or validated by this probe.

Unique failed-build evidence was also preserved outside Git under
`/home/danil/Documents/ak820-private-backup-20261023/optimization-probes/qmk-modtap`.

Independent review, 2026-10-23: review_modtap_contract checked the artifact
hashes, memory figures and source guards. The initial tap-only decoder claim
was corrected: this opt-in includes the generic decoder. The report is
approved as a negative size probe, not as runtime support or an update image.
