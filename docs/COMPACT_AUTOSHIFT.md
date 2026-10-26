Русский перевод: [Компактный Auto Shift](ru/COMPACT_AUTOSHIFT.md).

# Compact Auto Shift

Holding a supported key past 175 ms sends its shifted form.

The beta.3 profile plan includes this engine in `main` and `typing`. It starts
enabled and uses a fixed 175 ms hold threshold. `AS_ON`, `AS_OFF` and `AS_TOGG`
change the current session without writing settings. `AS_UP`, `AS_DOWN` and
`AS_RPT` are not supported.

## Keys and timing

The engine accepts direct physical basic keys: A–Z, 1–0, Minus through Slash
(including the non-US hash key), and the non-US backslash key. It does not delay
Space, Enter, Tab, Backspace, navigation keys, function keys or modifiers.
The host keyboard layout determines the printed characters.

A release before 175 ms sends an ordinary press and release. At 175 ms or later,
the engine holds the key with left Shift until its physical release. The host
can repeat that held shifted key. A different press before the threshold sends
the pending key without adding Shift, before processing the new key. Its
physical release still releases the original key.

There is one owner. Other keys work immediately while it remains down;
they cannot start another Auto Shift decision. Shift applies to the whole
keyboard report, so another key pressed while an automatically shifted key is
held also sees Shift. Releasing the owner removes only its own Shift reference.
A physical Shift key or another modifier owner remains held.

Existing modifiers bypass the delay. This includes held Shift, Ctrl, Alt and
GUI, encoded modifier owners and queued One Shot modifiers. A real Shift press
that interrupts a pending key is processed after the pending ordinary press.
Caps Word still processes the emitted key. Repeat and Alternate Repeat remember
the automatically added Shift.

## Other actions

Combo input fallback and Combo outputs use their existing pipeline and bypass
Auto Shift. A key configured as a Combo input therefore does not gain Auto Shift
when that Combo fails. Mod-Tap, Layer-Tap and Space Cadet taps also bypass it.
Encoder actions, macros and generated Repeat actions are immediate.

The press-time keycode is retained through release. Changing a mapping or layer
while the key is pending or held cannot change its eventual release. Clearing
the keyboard, starting Vial unlock or switching the NKRO mode cancels the owner;
subsequent ticks and releases cannot revive it. `AS_OFF` prevents new decisions
and preserves an already emitted key until its physical release. An interrupted
pending key is resolved before the physical control key changes the mode.

This is a bounded board feature. It does not enable upstream QMK Auto Shift,
Retro Shift, per-key callbacks, repeat-on-second-tap, adjustable timing or
persistent settings. The timing and report-wide Shift behavior follow the
relevant concepts in the [QMK Auto Shift documentation](https://docs.qmk.fm/features/auto_shift).


Development status and limits are recorded in the [technical report](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/compact-runtime-20261024/README.md).
