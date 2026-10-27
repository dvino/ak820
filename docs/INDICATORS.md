Русский перевод: [Индикаторы C, W и OS](ru/INDICATORS.md).

# C, W and OS indicators

The keyboard has three separate indicators:

- **C** follows the Caps Lock state reported by the computer. Caps Word does not turn it on.
- **W** lights when any layer above layer 0 is active, including a held, toggled or default layer. When no such layer is active, GUI lock makes W pulse through a 2000 ms brightness cycle. This port uses W for layers.
- **OS** belongs to the optional Mac/PC and host-layout modules below. These modules do not change C or W.

The indicators work independently of key lighting. They are dark before USB configuration and during suspend. An active or default layer above 0 overrides the GUI-lock pulse and lights W steadily. The pulse is available only in `game` and `mmo`, where GUI lock is supported; the default lock state is off. C and OS remain independent. See [GUI controls](GUI-CONTROL.md).

## Mac/PC module

In the curated `system` package, OS is on in Mac mode and off in PC mode. The module swaps Alt and GUI on each side. Assign `AG_SWAP`, `AG_NORM` or `AG_TOGG` in Vial; see [Mac/PC mode](MAC-PC.md). The mode is temporary and defaults to PC after a restart. The saved keymap and F-row are unchanged.

## Host-layout module

Select the OS indicator state from a compatible desktop helper.

In the curated packages that include OS indicator control, a compatible desktop
helper can select OS off, on or slow breathing. The firmware generates the four-second breathing cycle. The helper sends the selected state and refreshes it at least once per second; it does not stream animation frames.

An explicit release, an unknown layout reported by the helper, or three seconds without a refresh restores normal OS behavior. USB reset, reconfiguration, suspend and Vial unlock also cancel the override. A query does not refresh the timeout. The firmware never determines the system layout itself.

In the curated `system` package, normal OS behavior follows the current Mac/PC
mode. A mode change during a helper override takes effect when the override ends.
In packages without Mac/PC, normal OS behavior is off.

These are separate modules included only by the package combinations listed in
[Build profiles](BUILD-PROFILES.md). They keep their state in RAM and do not
change saved settings. The desktop helper itself is still planned; Vial alone does not send its layout updates. See the [protocol contract](../web/docs/OS-INDICATOR-PROTOCOL.md) and [Status](STATUS.md) for implementation and verification scope.
