# Successful Combo initialized-record reference

Run the focused host checks from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/ph_combo_reference.py
python3 qmk-8051-ak820/tests/ak820_tapping/ph_layer_reference.py
```

No production source is modified. Both fixtures enter through the shared
`initialized_physical_record` host adapter, not retained `action_exec`.
The adapter aggregate-initializes the entire record with its physical event;
omitted tap fields and, for Combo, explicit keycode are zero. It preserves the
retained dispatch gate `IS_NOEVENT(record.event) ||
pre_process_record_quantum(&record)` before calling actual retained tapping.
Physical Combo members therefore pass through genuine retained preprocessing
and `process_combo`; successful output and synthetic release still traverse
retained Combo and tapping functions. Engine-managed replays are not zeroed.

This boundary represents fresh unresolved physical input. Retained non-board
`action_exec` does not establish initialized tapping state in this configuration;
it is no longer extracted. The prior diagnostic's inherited count 51 was an
invalid host observation, not reference semantics or a possible production
four-bit tap count. The host tap structure has a full-byte count. UBSan does not
prove ordinary stack initialization; the aggregate initializer establishes it.

## Checked traces

The Combo fixture configures A+B -> C while LT(1, Esc) is pending. Immediately
after the LT press, it asserts zero count, no interruption, pressed LT identity,
zero layer state and no final callback. Both member-release orders must produce
exactly these final callback rows (event time, dispatch time, column, pressed,
keycode, action, tap count, layer state):

```text
F 10 80 2 1 4129 a129 0 2
F 30 80 0 1 0006 0006 0 2
F 80 80 0 0 0006 0006 0 2
F 90 90 2 0 4129 a129 0 0
```

No physical chord member reaches final callbacks and overflow is rejected.
A separately compiled and successfully executed direct-dispatch mutant replaces
the buffered Combo output's tapping call with the final callback. Its first
callback must specifically be `F 30 71 0 1 0006 0006 0 0`: Combo dispatch before
LT hold, on layer zero. Compilation failure or arbitrary output difference is
not accepted as the semantic negative control.

The layer fixture revalidates PH lookup refresh, release-cache lookup after
layer-off, and transparent fallback using the same initialized boundary. The PH
trace now checks the complete callback sequence, initial pending state and no
overflow; existing compiled no-PH, no-refresh, release-cache and transparency
controls remain in place. Earlier passes through uninitialized `action_exec`
are superseded by these adapter-scoped checks.

## Adaptations and limits

- Includes and `#pragma once` are stripped from extracted Combo source/header.
- `MAKE_COMBOEVENT` is expression-valued: the repository factory expands to a
  declaration and cannot be used in the retained release initializer.
- Timer, program-memory access and layer-map functions are host adapters.
- Final callbacks decode generated keycodes and model ordinary LT layer changes;
  they do not execute `process_action`, final quantum processing or real HID.
- Unused-parameter warnings are disabled for retained default weak callbacks;
  other warnings remain errors and UBSan remains enabled.

These tests establish only the tested initialized-record ordering and lookup
boundaries. They do not qualify unchanged `action_exec`, all Combo settings,
Quick Tap, cancellation, overflow behavior, reentrancy, transaction quarantine,
compact-candidate equivalence, SDCC ABI, a linked image, stack/IRQ bounds,
installed firmware or hardware behavior. No PH production implementation is
provided. Independent review remains required.
