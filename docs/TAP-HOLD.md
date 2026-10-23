Русский перевод: [Mod-Tap и Layer-Tap](ru/TAP-HOLD.md).

# Mod-Tap and Layer-Tap

Mod-Tap and Layer-Tap assign two actions to one key. The short press sends a
tap key. A hold activates a modifier or layer. These actions can be useful for
placing a modifier or layer switch under a frequently used key.

## Current support

The bundled legacy firmware sends the tap key for Mod-Tap and Layer-Tap;
it does not activate the hold action. Vial may still show these actions.
Selecting one does not add hold support.

Development source implements compact tap-hold. The behavior below describes
that development profile. Package approval, test results and installation state
are recorded separately in [Status](STATUS.md).

## Candidate behavior

In the compact development profile, a press stays undecided for 200 ms. Releasing it before 200 ms, with no other key pressed in between,
sends one tap. Holding it for 200 ms activates its modifier or layer. Pressing
another key first also activates the hold before the new key is resolved. This
makes a quick chord choose the hold; a rolling sequence that overlaps the next
press also chooses the hold. Releasing another key by itself does not choose
the hold.

For example, Ctrl-Tap-Escape sends Escape when tapped briefly. Holding that key
activates Ctrl. A Layer-Tap-Space key sends Space when tapped briefly and
activates its selected layer when held. The tap key and layer can be changed
through Vial in that profile. Caps Lock and its default
assignment are not part of this change.

After a tap completes, the next press starts a new decision. A held second
press activates the hold action; it does not repeat the tap key. There is no
double-tap lock. A tap of a modifier sends a temporary modifier press and
release.

Each held action keeps its own effect. For example, releasing one Ctrl-Tap
hold does not release Ctrl while another Ctrl-Tap or a physical Ctrl key is
still held. Momentary layer holds work the same way. Turning a layer on or
changing the persistent layer with TG or TO does not cancel a key that is still
holding that layer. Lower and Upper activate Adjust together; an explicit
Adjust assignment remains active when either one is released.

Other key releases are handled as they happen while a tap is undecided. For
example, Shift down, Mod-Tap down, Shift up, Mod-Tap up sends the tap without
Shift. This release timing is intentional; QMK's general tapping engine may
hold the Shift release until it has decided the tap.

The encoder's clockwise and counterclockwise actions each produce a tap when
their press and release complete before a timeout or another press. Pressing
the encoder while a Mod-Tap or Layer-Tap is undecided commits that earlier key
to its hold before resolving the encoder action. During Vial unlock, held keys
are released and suppressed until they are released physically and pressed
again.

## Caps Word

A short tap passes through Caps Word as an ordinary key. A Mod-Tap modifier
hold or Layer-Tap layer hold changes its held state directly and does not by
itself stop Caps Word. Thus a Shift hold through Mod-Tap keeps the mode active,
while an ordinary Shift press stops it. A Ctrl hold through Mod-Tap stops Caps
Word when the next ordinary key press is processed with Ctrl still held.

## Macros

Macro DOWN and UP commands change the macro's own held state. Repeated DOWN
is idempotent; UP cannot release a physical key, a tap-hold action or Repeat.
A DOWN in one macro can still be released by an UP in another. TAP and text
use temporary presses without consuming retained macro holds. Explicit state
clearing also clears macro holds and stops remaining playback.

Extended macro Mod-Tap and Layer-Tap commands use their basic tap key. Macro
TAP, DOWN and UP already specify the action; they do not start a timed physical
tap-hold decision. Encoded modifier commands set or clear their macro modifier
bits. These are script-state commands, not independent physical key owners.

## Limits

The candidate keeps six layers, 16 macro slots and 8192 bytes of macro storage.
It does not change the saved layout format, UID or NVM layout. Layer-Tap
targets are limited to layers 0–5. The tap field is one byte, so it cannot hold
a macro, an RGB action or another extended action.

The USB boot-keyboard report has six slots for distinct ordinary keys. With six
different keys already held, an additional key may appear as ErrorRollOver
until a slot is free. The firmware must retain the held keys and report them
when they fit again. NKRO reports can represent more distinct keys. If two
sources hold the same key, releasing one source does not release the other.

This candidate's source behavior has not been shown to match physical key
timing, USB scheduling or encoder hardware. A source change or host/CPU test
does not establish those results. See [Testing](TESTING.md) and [Status](STATUS.md)
for evidence and release state.
