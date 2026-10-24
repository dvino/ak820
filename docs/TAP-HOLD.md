Русский перевод: [Mod-Tap and Layer-Tap](ru/TAP-HOLD.md).

# Mod-Tap and Layer-Tap

Mod-Tap and Layer-Tap let one key do two jobs. A quick press sends a regular
key. Holding the key activates a modifier or a layer. Choose one of these
actions in Vial's key selector, then set the tap key and modifier or layer.
Layer-Tap supports layers 0–5.

For example, assign Ctrl-Tap-Escape to a key: a quick press sends Escape, and
holding it activates Ctrl. Assign Layer-Tap-Space with layer 1 to another key:
a quick press sends Space, and holding it activates layer 1. Set the actions
for the desired layer in Vial. Keep a way to return to layer 0 when editing
other layers.

The default decision window is 200 ms; QMK Settings can change it from 1 to
1000 ms. Releasing the key before the selected time sends one tap. Holding it
until that time activates the hold. Pressing another key before then
also activates the hold first, so a rolling press that overlaps the next key
acts as a chord. Releasing another key alone does not activate the hold. Each
new press starts a fresh decision; a second press does not repeat the tap key
or lock the modifier/layer on.

The encoder's clockwise and counterclockwise actions are assigned separately
in Vial. Rotating it while a tap-or-hold decision is waiting activates that
key's hold first, then processes the encoder action.

Each physical key keeps its own held action. Releasing one Ctrl-Tap key leaves
Ctrl active if another such key or the physical Ctrl key is still held. A
Layer-Tap hold likewise remains active until that key is released. Changing
the persistent layer does not cancel a Layer-Tap key that is still held.

Caps Word treats a tap as an ordinary key. A Shift hold through Mod-Tap keeps
Caps Word active; an ordinary Shift press turns it off. A Ctrl hold through
Mod-Tap turns Caps Word off when the next ordinary key is pressed while Ctrl
is still held. A Layer-Tap hold alone does not turn Caps Word off.

Macros use their own tap, down and up commands; they do not wait 200 ms for a
physical tap-or-hold decision. A Mod-Tap or Layer-Tap action used in a macro
sends its tap key. These actions are intended for physical keys.

For current installation and verification details, see [Status](STATUS.md).
