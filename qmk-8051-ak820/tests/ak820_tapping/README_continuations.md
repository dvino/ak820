# Host continuation diagnostic

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/continuations.py
```

Requires Python 3 and a host C compiler with UBSan (`CC`, default `cc`). No
firmware build or device access occurs. Temporary executables are created beside
this fixture and removed on exit. Nothing in production is modified.

## Configuration and extraction

`config.h` enables compact tapping and Combo and disables upstream tapping.
`rules.mk` enables Repeat; compact Auto Shift and Tap Dance are opt-in there.
`util/ak820_profiles.py` enables both Auto Shift and Tap Dance in `typing`.
This diagnostic enables that pair alongside the existing tapping host fixture's
feature subset. It is **not** a full typing-profile build: Leader, One Shot,
Dynamic Macro recording, Key Overrides and other profile components are omitted.
No complete nesting claim for any catalog image follows.

The runner reuses the extraction recipe in `run.py` without executing its CLI.
It combines actual action, preprocessing, quantum, board resolver/cache, owners,
Repeat, macro interpreter and Vial function bodies with actual compact Combo,
Auto Shift and Tap Dance bodies. The VIA macro callback is also extracted, and
VIA processing is enabled. `harness.c` supplies the map, EEPROM, timer, USB/report
and empty user hooks. The Tap Dance settings reader returns one in-memory entry.
Thus hardware, persistence and user callbacks are adapters, not production tests.

Only the action and process-record function definitions are renamed to install
host wrappers. Calls, including nested production calls, go through those
wrappers. Per-invocation event snapshots are compared after callbacks return.
Depth watchdog 16 is a test runaway limit, **not a proposed firmware capacity**.
Host automatic locals do not model SDCC static/overlay storage or its adapter.

## Observed routes

The exercised production paths are:

- Physical macro -> VIA playback -> extended Vial event -> action/preprocessing
  -> Repeat -> process-record -> same macro. Physical admission remembers the
  macro before playback; the interpreter's `sending` guard rejects its recursive
  playback. The initial ordinary key is not repeated. Observed action depth 2,
  process-record depth 3, with no added ordinary-key reports.
- Physical Repeat -> repeated macro -> extended Vial event -> action ->
  process-record -> tri-layer output. Observed depths are again 2 and 3.
- A generated action runs Combo tick before admission, flushing a pending Combo
  record through process-record. `first` is cleared before that dispatch.
- Generated input interrupts a pending Tap Dance through the admission hooks;
  `td_wait` is cleared before dispatch and `ak820_td_invoking` guards finishing.
  Its validator permits only ordinary/modded keyboard outputs, not macros.
- Generated input flushes pending Auto Shift through `ak820_autoshift_before`.
  `as_state` changes before dispatch; eligible outputs are ordinary keycodes.

These explain why the three extra callback engines do not establish arbitrary
macro recursion in these traces. They are not an exhaustive enabled-route proof.

## Assertions and controls

The cases assert real pending states, output owners, release cleanup, event
sentinels and measured nesting. Actual board-cache tests cover a held mapping
change and upper-layer lookup followed by layer deactivation before release.

Test-only injection rejects nested action entry at a selected depth and clears
the keyboard, or cancels a nested process-record call. These exercise host cleanup
and macro/Repeat unwinding, **not a production reject mechanism**. There is no PH
queue, so queue overflow and its physical-release suppression are not tested.
The diagnostic also asserts that a fresh owner acquisition after cleanup remains
possible: it documents the missing quarantine, not a cancellation-safety pass.

A separately compiled semantic mutant replaces Repeat's copied identity with
KC_NO. Compilation must succeed; execution must fail an assertion. Compiler
errors do not count as a negative control.

No PH implementation, noncommitting preprocessing scheme, full source-lifecycle
pairing, SDCC ABI/overlay protection, linked memory/stack/IRQ bound, USB timing or
hardware behavior is qualified here. The existing reference fixtures remain the
separate QMK semantic observations.
