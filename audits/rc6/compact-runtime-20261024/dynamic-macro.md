# Compact Dynamic Macros

This is an offline development feature. No device write, reset or flash is part
of this work. The installed alpha.3 image is unchanged.

## Use

Map `DM_REC1` or `DM_REC2` to start recording into one of two RAM slots. Starting
replaces that slot immediately. `DM_RSTP` stops recording. `DM_PLY1` and
`DM_PLY2` finish a recording, then play the selected slot. Recording and playback
controls pressed during playback are ignored. Power loss clears both slots.

Each slot holds the first sixteen supported key presses. A press becomes a
stored tap when its last keyboard owner releases it. Stopping drops unfinished
presses and keeps completed taps in press order. Reaching capacity ignores new
presses until recording stops; releases still complete existing entries.
Overlapping keys are recorded, but replay turns them into consecutive taps.
No original timing or held-key duration is retained.

The recorded output contains HID keyboard usages `0x04..0x7f` and the effective
modifier bits at each emitted press. This includes ordinary typing, encoded
modifier keys, tap-hold tap outputs, Combo outputs/fallback,
Auto Shift and One Shot results when their physical action reaches the keyboard
handler. Caps Word's emitted Shift is included. Modifier presses alone are not
stored. An already-held duplicate usage does not create another entry; the
entry completes only on a final eligible physical release.

Mouse, media/system usages, usages `0x80` and above, layer/configuration actions,
standalone modifiers, encoder output, Vial macro output, generated Repeat and
Alternate Repeat output, Grave Escape's synthetic output and Space Cadet's synthetic tap output are excluded.
Generated macro controls cannot invoke recording or playback. This is a bounded
completed-tap implementation, not the full upstream Dynamic Macro engine.

Nested Vial macro primitives pause playback to keep their ownership bookkeeping
separate. Playback waits at least 10 ms between press/release phases, with no catch-up
burst. It adds only its own key/modifier references. Physical modifiers combine
with stored modifiers; they are never cleared to force an exact chord. A usage
already owned by another input is skipped because it cannot form a new tap.
A physical owner arriving during playback survives playback's release. Playback
does not update Repeat history or run Caps Word/Auto Shift again.

A pending keyboard report, unconfigured USB, suspend or pending reset blocks the
next playback phase. A busy release is retried by the existing transport before
another tap starts. The new transport queries do not change retry behavior.
Unlock, settings clear, report-mode changes and reset/resume cleanup cancel the
engine through the shared clear path. Completed slots survive that cancellation;
unfinished recording entries are discarded. Suspend prevents publication; resume
cleanup cancels playback before typing resumes.

## Representation and boundaries

Two sixteen-entry arrays share a 64-byte `{usage, modifiers}` buffer. The high
usage bit marks an unfinished press. Two lengths and small playback/recording
state replace full event records. The NVM schema stays `0x082002`, Combo storage
stays at `0x658`, and six layers, sixteen Vial macros and eight Combos remain.
No host GUI or persistent-storage format changes are introduced.

## Verification

Host tests compile the production action, report, tapping, One Shot, Auto Shift,
Repeat and recording code with UBSan. Six negative controls must fail when
incomplete filtering, effective modifiers, transport gating, duplicate-owner
balance, nested-primitive gating or cancellation is removed. Tests cover rolling presses, capacity,
overwrite, both slots, unfinished/preheld keys, Shift ownership in both release
orders, OSM, encoded modifiers, Caps Word, Auto Shift, generated exclusions,
6KRO rollover-hidden ownership, NKRO ownership and timer wrap.

The linked suite executes the exact SDCC image on uCsim C52. It checks storage,
press order, both slots, ownership, effective modifiers, generated controls,
unlock, clear, real busy endpoint down/release retry, unconfigured/reset guards,
and suspend/resume. Peripheral state and endpoint completion are supplied by the
fixture. These checks do not establish physical USB, interrupt overlap or scan
timing. Whole-program stack and exact release approval remain separate gates.

The isolated `full-dynamic-macro` build uses **40,265 CODE bytes**, 2,724 allocated
XRAM bytes and 162 bytes of stack capacity. Against the baseline `full` image,
this adds 1,120 CODE and 86 XRAM bytes. The main window has 219 trailing bytes;
the low window remains separate. The buffer/state alone occupies 74 XRAM bytes;
compiler parameter/local allocations account for the remaining measured delta.

All **26 linked scenarios** pass on that exact image. The largest observed stack
use in these scenarios is 35 bytes; this is a test observation, not a whole-program
bound. Host UBSan tests pass and kill all six mutation controls.

The exact image, input hashes and measurements are in
[`dynamic-macro/measurements.json`](dynamic-macro/measurements.json). The IHX
SHA256 is `99eb56d0a1c32d61f23db3c66f1e316dc0b18f792fa1e29a7012fc7e8328580a`.
The adjacent `host.json`, `linked.json` and `build.json` retain results and build
provenance. `raw-build-linked.tar.gz` retains the complete isolated build and
linked scripts/logs. The archive hash is recorded in `measurements.json`.

The build command, from the QMK directory, was:

```sh
/workspace/scratch/97c35f9846c1/ak820/qmk-8051-ak820/.venv/bin/python util/build_ak820.py \
  --profile full-dynamic-macro --build-dir .build/dm-reviewed \
  --toolchain /workspace/scratch/97c35f9846c1/ak820/toolchains/sdcc-4.6.0 \
  --qmk-bin /workspace/scratch/97c35f9846c1/ak820/qmk-8051-ak820/.venv/bin/qmk
```

An initial `full-auto-shift-dynamic-macro --short-calls` experiment stopped at
the existing strict diagnostic page-marker gate. That failed image is not a
qualified artifact. Auto Shift interaction is covered by the production host
fixture; exact linked Auto Shift interaction awaits a fitting integrated image.

A nested-primitive linked test initially used opcode 5 (extended tap), which
intentionally leaves primitive ownership disabled. The fixture was corrected
to opcodes 6/7 (extended down/up), then both deferred acquisition and due release
were rerun with A and Shift ownership checks. The retained 26-case report is the
passing corrected run.
