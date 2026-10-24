Русский перевод: [Клавиши Win/GUI](ru/GUI-CONTROL.md).

# GUI controls

The development feature `gui-lock` adds three keycodes that can be assigned
in Vial. The `full-gui-lock` profile includes them with the existing `full`
features. This is an offline development build; it is not a released firmware.

| Keycode | Action |
| --- | --- |
| `GU_OFF` | Suppress the left and right GUI modifier bits in keyboard reports. |
| `GU_ON` | Allow both GUI modifiers again. |
| `GU_TOGG` | Toggle between those states. |

GUI is the Windows key on Windows and usually Super/Meta on Linux. The change
applies on press; releasing the control does not change its state. It lasts
until restart, which enables GUI again. It is not saved to flash.

The three controls preserve queued One Shot modifiers and Repeat history.

Turning GUI off immediately releases its bits in the report while preserving
other keys and modifiers. Physical, encoded, One Shot and generated modifiers
use the same output mask. Their internal owners remain intact. Turning GUI on
while a GUI key remains held exposes that held modifier immediately; release
it first if that is unwanted.

A held GUI key still counts as a modifier inside Auto Shift, so it bypasses
the Auto Shift delay even while GUI output is disabled. Dynamic Macros also
retain the recorded GUI modifier; this filter controls whether it is sent.

A clear, NKRO switch or suspend cleanup releases its ordinary owners and keeps
the selected GUI mask. These controls do not enable modifier swaps, other
Magic actions or persistent QMK Settings.
