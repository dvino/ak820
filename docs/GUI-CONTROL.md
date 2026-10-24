Русский перевод: [Клавиши Win/GUI](ru/GUI-CONTROL.md).

# GUI controls

The development feature `gui-lock` adds three keycodes that can be assigned
in Vial. `full-gui-lock` includes them with the `full` features. The separate
`full-ctrl-gui` profile also adds Ctrl/GUI swapping. These are source-only
development profiles, not part of published alpha.3.

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
the selected GUI mask. GUI lock does not enable other Magic actions or
persistent QMK Settings.

## Ctrl/GUI swap

The `full-ctrl-gui` profile adds three Vial keycodes:

| Keycode | Action |
| --- | --- |
| `CG_SWAP` (`0x701b`) | Swap left Ctrl with left GUI and right Ctrl with right GUI. |
| `CG_NORM` (`0x701c`) | Restore the normal mapping. |
| `CG_TOGG` (`0x701d`) | Toggle between normal and swapped mappings. |

The mapping is applied to output before GUI lock filters GUI bits. Internal
modifier owners are preserved, so changing the mapping does not discard held
modifiers. The selection lasts until reboot and is not saved. It does not add
persistent Magic settings.
