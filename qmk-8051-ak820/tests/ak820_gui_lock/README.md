# GUI control linked regressions

`linked.py` runs the exact linked SDCC image on a generic C52 CPU with
simulated matrix, storage and USB endpoint readiness. It does not open USB or
prove physical USB, interrupt timing, flashing or installed firmware behavior.

Run from the repository root with an existing bounded build that includes
`gui-lock`:

```sh
python3 qmk-8051-ak820/tests/ak820_gui_lock/linked.py \
  --build-dir qmk-8051-ak820/.build/PROFILE \
  --s51 toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir /tmp/ak820-gui-regression
```

The output includes `results.json`, the linked image SHA256 and per-case
simulator commands and logs. A failed assertion returns a nonzero exit code.

The full-profile baseline has eleven cases. These cover held left and right
GUI, encoded modifiers, clear and resume cleanup, One Shot, Repeat, NKRO and
a busy endpoint. Optional-feature cases run only when the build report lists
the corresponding feature:

- `dynamic-macros`: records A with physical GUI and Ctrl while GUI is masked.
  The stored tap retains both raw modifiers. GUI controls add no recording
  entries. Replay stays masked until GU_ON reveals the same active tap;
  playback release preserves physical Ctrl and leaves no modifier owner.
- `auto-shift`: keeps Auto Shift enabled at its production default. Held GUI
  still bypasses Auto Shift while masked. Without GUI, A remains deferred at
  174 ms and gains Shift at 175 ms. GUI toggles preserve the active Shift
  owner, and all owners clear on release. Ordinary GUI cases explicitly use
  the production AS_OFF path.

A full-profile image with either optional feature therefore runs twelve
cases; an image with both runs thirteen. These checks observe production
controls and modifier/report state without writing private Dynamic Macro or
Auto Shift state.
