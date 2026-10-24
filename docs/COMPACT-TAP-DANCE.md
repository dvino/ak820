Русский перевод: [Tap Dance](ru/COMPACT-TAP-DANCE.md).

# Compact Tap Dance

The optional AK820 module provides eight Vial Tap Dance entries. Map `TD(0)`
through `TD(7)` to physical keys and set the four actions in Vial. Each action
accepts a keyboard key, a modifier, or a keyboard key with encoded modifiers.
`KC_NO` leaves an action empty. Layers, macros, consumer keys, mouse actions,
nested Tap Dance and other special actions are rejected.

A single tap runs the tap action after the tapping term expires. Holding the
first press runs the hold action; an empty hold action uses the tap action.
Two taps run the double-tap action. Tapping once, then holding the second press,
runs the tap-hold action. An empty double-tap action sends the tap action twice.
An empty tap-hold action sends one tap, then holds the hold action, falling back
to the tap action when needed. Held output ends on the physical source release.

Another key press finishes the waiting dance before that key is processed.
An interrupted first press uses the tap action, even while held. An interrupted
second press uses two single taps; the second output stays down until release
when that press is still held. Releases from keys held before the dance keep
their original action.

The tapping term starts again on the second press. Zero selects 200 ms; explicit
terms range from 1 to 32767 ms. The 16-bit timer handles one wrap. As with other
16-bit timed controls, a waiting decision needs scan ticks before a complete
timer cycle elapses.

Only one dance waits for a decision at a time. Resolved holds from different
entries can overlap. Mapping the same entry to two keys does not create a second
simultaneous owner: the later source is consumed until release. Three or more
presses are split into gestures of at most two presses; arbitrary tap counts
and QMK callbacks are not supported. Encoder pulses and generated actions do
not start dances.

Clearing the keyboard cancels pending dances and drops held output through the
shared ownership reset. Still-held physical sources stay blocked until release.
Configuration writes use that same clear path. An entry is read once when a
new gesture begins, so a gesture uses one consistent configuration.

## Storage and integration

The eight 10-byte `vial_tap_dance_entry_t` values reserve `0x6c0..0x73f`.
Entries 0–5 use offsets `index * 10`; entries 6–7 use offsets
`64 + (index - 6) * 10`. Padding prevents a record update crossing a 64-byte
journal page. The six layers, eight Combos, 16 macro slots and 8192-byte macro
stream retain their existing locations and capacities.

The event `before` hook runs after tapping admission and before key lookup.
The record hook runs after Leader and before Auto Shift. The scan task expires
waiting decisions. The shared clear path calls the cancellation hook. Final
keyboard actions use the existing key and modifier ownership references.

`python3 qmk-8051-ak820/tests/ak820_tap_dance/host.py` runs the production engine in an isolated
host fixture with undefined-behavior checks. It covers all four gestures,
fallback actions, interruption, overlapping holds, duplicate-entry suppression,
timer wrap, cancellation and validation. This test does not prove linked stack
bounds, interactions with every enabled module, persistent storage, USB reports
or physical timing. Exact-image stack and interrupt checks and linked regression
results belong in the build qualification record.
