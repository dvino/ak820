Русский перевод: [Индикаторы](ru/INDICATORS.md).

# C and W indicators

The development firmware enables two dedicated indicator outputs:

- **C** follows the host's Caps Lock LED report. Pressing Caps does not change
  the light directly; the host supplies its actual state. Caps Word does not
  turn it on by itself.
- **W** shows that a layer above layer 0 is active. Held, toggled and default
  layers count, including Lower/Upper/Adjust. Returning to layer 0 turns it off.
  It does not show Windows-key lock.

The indicators work independently of the key lighting mode, brightness and
on/off setting. Unconfigured USB and USB suspend make both outputs dark.
The next main-loop task recomputes them after configuration or resume.
No settings are saved for these outputs and Caps keeps its existing mapping.

## Implementation and checks

The selected outputs come from the [OEM data-flow trace](../audits/rc6/oem-indicator-dataflow-review-20261024.md):
slot 71, component 1 for the Caps report bit, and slot 79, component 1 for the
second state output. The development firmware gives that second output the
project's additional-layer meaning. These slots are excluded from the 82-key
RGB map. Other components of those slots are preserved.

The update runs in the main loop. It preserves the previous scan-interrupt
enable bit while writing the two dedicated slots; USB interrupts remain enabled.
It uses no persistent storage. The candidate adds 78 populated CODE bytes and
leaves XRAM unchanged. [Status](STATUS.md) records the exact build and checks.

The linked CPU model checks host LED bits, production layer APIs, default and
Tri Layer paths, USB state fixtures, RGB canaries and interrupt-bit restoration.
A state fixture is not a physical USB reset or a test of visible lights.

The physical C/W connections and visible behavior have not been verified.
This is a source-derived firmware candidate, not evidence of installation.
The checked-in legacy installer firmware does not contain this implementation.
