# Remaining feature probes

Offline builds on 2026-10-24 leave Mouse Keys, Auto Shift, Tap Dance and Key
Overrides deferred. No firmware was packaged or sent to a device.

## Complete-image results

The matched source is `16222db8753cfec83cec55c7a728530e1b261c06`, with the
experimental exact-sequence outliner copied from the parallel size work.
Its SHA256 is recorded in [the measurements](feature-probes.json). That
outliner is a probe dependency under separate review; these results do not
approve it. Each probe starts from the standard profile and changes one board
feature flag. It keeps existing features and the real CODE windows:
`0x28a0..0x2fff` and `0x3027..0xc6ff`.

| Probe | Linked image bytes | Change from matched baseline | Bytes outside CODE windows | Result |
| --- | ---: | ---: | ---: | --- |
| Matched standard baseline | 39,115 | 0 | 0 | Builder accepts the memory windows. |
| Upstream Mouse Keys | 41,797 | +2,682 | 1,381 | Builder rejects `0xc700..0xcc64`. |
| Upstream Auto Shift | Unknown | Unknown | Unknown | SDCC rejects three case ranges. |
| Auto Shift with temporary explicit cases | 42,497 | +3,382 | 2,081 | Builder rejects `0xc700..0xcf20`. |
| Upstream Vial Tap Dance | Unknown | Unknown | Unknown | Callback assignments fail compilation. |
| Upstream Vial Key Overrides | Unknown | Unknown | Unknown | Pointer assignment and initializer fail compilation. |

Counts use actual bytes present in the complete linked Intel HEX image.
They are not source-size estimates. The rejected images are probe evidence,
not installable firmware. Linker ROM totals also include five unoccupied
alignment bytes; the JSON retains the linker memory summaries separately.
Costs are specific to this baseline and outliner, and are not additive.

## Why each candidate remains deferred

**Mouse Keys:** enabling `MOUSEKEY_ENABLE` compiles and links, but exceeds the
main CODE window. A smaller implementation or further sound savings are
needed before a profile can be considered. USB mouse reports, scan timing,
encoder actions and physical behavior were not tested.

**Auto Shift:** enabling `AUTO_SHIFT_ENABLE` fails in
`quantum/process_keycode/process_auto_shift.c` at lines 74, 77 and 84: SDCC
reports that case-range expressions require C2y. A second, probe-only build
expands the same alpha, numeric and symbol ranges into explicit numeric cases
and retains the separate non-US backslash case. That build links but exceeds
the main CODE window by 2,081 bytes. The portability edit was restored; no
Auto Shift implementation was added. A bounded design must also address
interaction with compact tap-hold, Combos and Caps Word.

**Tap Dance:** `TAP_DANCE_ENABLE=yes` selects Vial's upstream dynamic engine.
SDCC rejects the callback assignments in `quantum/vial.c:602..604` because
function-pointer argument storage types differ. No complete image exists, so
CODE and RAM costs remain unknown. Independently, adding Tap Dance storage
moves the existing Combo base: `quantum/dynamic_keymap.c:129` requires the base
to remain `0x658`. The assertion was not bypassed. A compatible saved layout,
versioning, backup and migration plan is needed along with an ABI-safe port.
A small fixed Tap Dance design would require a separate, defined scope.

**Key Overrides:** `KEY_OVERRIDE_ENABLE=yes` selects Vial's upstream dynamic
engine. SDCC rejects `quantum/vial.c:723` with an indirection-type mismatch
and the zero initializer at line 682 with illegal-address and nonconstant
initializer errors. No complete image exists, so CODE and RAM costs remain
unknown. An ABI-safe port and saved-layout review must precede measurement;
modifier ownership, Repeat, Caps Word and macros need interaction tests.

## Reproduction and limits

Each build used SDCC 4.6.0, the QMK virtual environment and a fresh directory:

```sh
python util/build_ak820.py \
  --toolchain /workspace/scratch/426029716a36/ak820/toolchains/sdcc-4.6.0 \
  --qmk-bin /workspace/scratch/664bab7a0eb4/ak820/qmk-8051-ak820/.venv/bin/qmk \
  --build-dir .build/probe-NAME
```

The respective board flag is changed only during its isolated build. For the
portable Auto Shift probe, each range in `get_auto_shifted_key` is replaced
by its exact cases: alpha `0x04..0x1d`, numeric `0x1e..0x27`, symbols
`0x2d..0x38`, followed by `KC_NONUS_BACKSLASH`. The ordinary flag-only probe
retains the original source.

[Measurements](feature-probes.json) include exact image hashes, allocation
summaries and compile errors. [Log excerpts](feature-probe-logs/) retain the
builder outcome for each probe. Temporary feature flags, Auto Shift edits
and the copied outliner were restored after measurement. These offline
probes establish build blockers and image costs only. They do not prove
runtime stack bounds, interrupt safety, feature behavior or hardware
compatibility. No release or installation approval follows from the baseline
passing the builder.

## Independent review

An independent review checked source agreement, recomputed IHX/MAP/MEM hashes,
parsed every complete image to confirm occupied CODE bytes and overflow ranges,
and compared compiler errors with the retained logs. The review approved this
audit-only package with no blocking findings. The baseline distinction and
nonadditive costs were checked explicitly; no runtime or release approval was
granted.
