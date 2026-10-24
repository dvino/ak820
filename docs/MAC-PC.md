Русский перевод: [Режим Mac/PC](ru/MAC-PC.md).

# Mac/PC mode

The optional `AK820_MAC_PC` module switches the left and right Alt/GUI
modifiers together. PC mode leaves them unchanged. Mac mode exchanges Alt
with GUI on each side; GUI is the Command key on macOS.

Assign these existing QMK keycodes in Vial:

| Keycode | Hex value | Action on press |
| --- | --- | --- |
| `AG_SWAP` | `0x7014` | Select Mac mode |
| `AG_NORM` | `0x7015` | Select PC mode |
| `AG_TOGG` | `0x7016` | Switch between Mac and PC |

The mode starts in PC after a restart and lasts only for the current session.
It does not write settings or change the saved keymap. Releasing a mode key
does not switch modes again. A held modifier changes its output immediately,
then releases normally. The mapping applies to physical keys, One Shot,
Mod-Tap and macro modifiers in both 6KRO and NKRO reports.

This is a compact modifier switch. It does not recreate the stock Mac layout,
change F-row or media keys, detect the host OS, or configure the computer.
The separate left-only and right-only Alt/GUI magic keycodes are outside this
module. Use the three commands above.

If Ctrl/GUI swap or GUI lock is also enabled, the order is Mac Alt/GUI swap,
then Ctrl/GUI swap, then GUI lock. The lock therefore blocks GUI output after
the selected swaps. Clearing held keys, changing rollover mode, and suspend
cleanup retain the selected Mac/PC mode; a firmware restart returns to PC.

The build profiles are `full-mac-pc` and `full-mac-pc-os-indicators`.
The latter also enables the [host override of OS](INDICATORS.md). Indicator behavior
and the available profiles are documented separately from the mode controls.
