# Compact key processing — 2026-10-24

The isolated `full` build uses **759 fewer CODE bytes** than commit
`38ad0133278463b4662dcb81eecaa17c9cd93b9b`: 40,043 → 39,284. XRAM changes
from 2,637 to 2,631 bytes. The linked stack capacity stays at 162 bytes.
No keymap, macro, Combo, encoder, report or saved-setting capacity is reduced.

These measurements cover only the core changes below. They exclude the
concurrent RGB driver changes, short transfers, Mouse Keys and Auto Shift.
Their combined image needs its own build and verification.

## Linked measurements

All rows use the pinned SDCC 4.6.0, the `full` profile and the same existing
DCE, outlining and callee-save configuration. Values are complete linked
CODE, including the low code window; they are not sums of translation-unit
estimates. [Measurements and hashes](core-compact-20261024/measurements.json)
also record XDATA object placements and the final isolated core source hashes.
Those hashes describe the isolated measurements, before Auto Shift integration;
the current combined source identity is recorded in the integration report.

| Isolated build | Total CODE | Main window | XRAM | Stack capacity |
| --- | ---: | ---: | ---: | ---: |
| `core-baseline`: unmodified `38ad013` | 40,043 | 38,171 | 2,637 | 162 |
| `core-typed`: private record views and transparent-layer check | 39,958 | 38,086 | 2,637 | 162 |
| `core-rgb`: compact RGB key dispatch | 39,849 | 37,977 | 2,637 | 162 |
| `core-qualified`: scalar position/cache path | 39,515 | 37,643 | 2,623 | 162 |
| `core-event01`: shared event argument copy | 39,416 | 37,544 | 2,631 | 162 |
| `core-repeat01`: adjacent Repeat exclusion ranges | 39,284 | 37,412 | 2,631 | 162 |

The final isolated IHX SHA256 is
`69be845a0b33f15375ee79ce65fb866a66881d12d43614f9152eb25996d6a759`.
Stack capacity is a linker allocation figure, not a whole-program stack bound.

## Changes and boundaries

Internal key positions use a 16-bit value, with the row in the high byte and
the column in the low byte. All 65,536 row/column combinations remain
representable. Scalar lookup/cache helpers remove repeated aggregate copies
from the event path. Public QMK functions remain available as wrappers.
Press-time keycodes still determine releases after a live remap. Both encoder
directions, invalid positions, Vial magic positions and unlock suppression
retain their previous behavior.

The layer search checks `KC_TRANSPARENT` directly in the pinned AK820
configuration. The internal lookup calls the retained keymap implementation
directly: it does not honor a separate override of weak
`keymap_key_to_keycode`. No such override exists in the supported build inputs.
`NO_ACTION_LAYER` and `STRICT_LAYER_RELEASE` are outside this configuration.
The original non-AK820 paths remain available.

Private XDATA views preserve the public generic-pointer signatures. The
retained records originate in `action_exec`, Combo's saved record and Repeat's
last/registered records. Vial extended actions enter through `action_exec`.
These objects are in XSEG in the emitted listings. The original eight profiles
differ only in the NKRO, One Shot and Space Cadet switches; those switches add
consumers, not a different record memory space. IRQ paths do not create or pass
these records. New record producers need the same address-space check.

RGB key dispatch uses the contiguous namespace and the existing action table.
Compile-time assertions bind the byte dispatch to the pinned keycodes. The
configured trigger edge, Shift reversal, supported direct modes and consumption
of disabled mode keys remain unchanged.

The event entry shares the aggregate argument setup used by eight matrix,
encoder and Vial call sites. Each caller supplies its own XDATA event. A named
snapshot captures all six bytes before any event callback. The public
`action_exec` body and its by-value contract remain unchanged. The emitted
wrapper tail-jumps into that body; it does not keep an extra return address
through the processing pipeline. The size saving costs eight XRAM bytes and
one additional six-byte copy per event. Device timing has not been measured.

Repeat's rejected layer-control ranges are adjacent. The AK820 path uses one
range when One Shot is enabled and two ranges otherwise. Compile-time
assertions require every original boundary to remain adjacent. Callback
ordering, callback arguments and modifier updates remain unchanged.

## Verification

The [host differential report](core-compact-20261024/host-differential.json)
compares extracted production functions with frozen `38ad013` implementations
under UBSan:

| Check | Cases | Result |
| --- | ---: | --- |
| Row/column, layer byte and unlock state | 33,554,432 | PASS; exact lookup calls and values |
| RGB code, modifier mask and edge, both trigger modes | 67,108,864 | PASS; exact action, return and record state |
| Repeat code, modifier mask, edge and callback result, One Shot off/on | 134,217,728 | PASS; exact callback, modifier update and return |

The final isolated linked image passes
[280 event-copy ABI cases](core-compact-20261024/event-linked.json), including
all event kinds, both edges, wrapping timestamps and a source address whose
high byte is nonzero. The source event remains unchanged. It also passes
[33 linked feature scenarios](core-compact-20261024/features-linked-summary.json),
including recursive Repeat and extended macro actions.

The earlier scalar/RGB stage passed all 13 profile-specific suites and 27 of
28 default offline suites. The remaining RGB host run failed because
LeakSanitizer could not read `/proc/<pid>/task` in the sandbox. The same fixture
passed with `ASAN_OPTIONS=detect_leaks=0`; AddressSanitizer and UBSan stayed
enabled. The [qualification summary](core-compact-20261024/earlier-qualification-summary.json)
preserves that distinction and the
[environment failure](core-compact-20261024/leak-sanitizer-environment.txt).
The default aggregate run is not recorded as passing. The earlier stack
analysis left the foreground root unresolved; it is not release approval.

The reusable checks run from `qmk-8051-ak820`:

```sh
python tests/ak820_core_compact/run.py --output .build/core-host.json
python tests/ak820_core_compact/linked.py \
  --build-dir .build/COMPLETE_IMAGE \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir .build/COMPLETE_IMAGE/core-linked
```

All checks are offline. No physical USB commands, flash operation or device
behavior check forms part of this report. Final integration, exact-image
safety evidence and independent review remain separate requirements.

## Research and rejected probes

The [SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf) describes
address-space-specific pointers and the MCS51 memory models. This supports
specializing private views only after tracing the actual object origins.
A typed view in `process_record` saved raw CODE but added two DSEG bytes;
it was rejected to preserve the stack allocation.

An apparently smaller event wrapper, `action_exec(*event)`, compiled
incorrectly: the emitted code used the first event byte as the source address.
This matches upstream [bug #4054](https://sourceforge.net/p/sdcc/bugs/4054/)
and [proposed patch #516](https://sourceforge.net/p/sdcc/patches/516/).
The compiler was not patched. The retained named snapshot emits correct
copies and is covered by the linked ABI test.

An exact mixed-integer selection of the existing outlining candidates was
also evaluated on an older diagnostic image. It improved the nominal saving
from 3,369 to 3,407 bytes, only 38 bytes. Raising the existing helper cap did
not improve the greedy result. A new SciPy/HiGHS build dependency was rejected;
[the probe summary](core-compact-20261024/rejected-milp.json) retains the result.
The upstream [LLVM machine outliner](https://llvm.org/doxygen/MachineOutliner_8cpp_source.html)
was consulted for candidate selection and overlap handling. None of this probe
is included in the linked savings above.
