Русский перевод: [Совместимость функций](ru/FEATURES.md).

# Feature compatibility

This catalog describes implemented functions and limits. The shared base is present in all ten profiles; optional modules follow the [module matrix](MODULE-MATRIX.md). The default is `main`. QMK Settings and One Shot are included in every current profile. Profile support, release approval and physical keyboard validation are separate states; see [Status](STATUS.md) for current results.

## Base features

| Feature | Description | Guide | Limits |
| --- | --- | --- | --- |
| **Six layers** (`six-layers`) | The keymap has six layers, numbered 0–5. | [CONFIGURATION](CONFIGURATION.md#keys-layers-and-encoder) | Layer-Tap supports layers 0–5. |
| **Vial macros** (`sixteen-vial-macros`) | Store and edit 16 keyboard macros in Vial. | [CONFIGURATION](CONFIGURATION.md#macros) | Eight KiB shared macro buffer; each macro must fit the available storage. |
| **Two-key Combos** (`eight-two-key-combos`) | Configure eight two-key combinations that send one key, a modified key or toggle Caps Word. | [COMBOS](COMBOS.md#two-key-combos) | Eight slots; the matching interval defaults to 40 ms and can be changed from 1 to 1000 ms with QMK Settings. Other input and output limits are in the guide. |
| **Compact tap-hold** (`compact-tap-hold`) | A quick press sends the tap key; holding activates its modifier or layer action. The beta.3 source candidate also supports a saved Vial macro on tap and a layer on hold. | [TAP-HOLD](TAP-HOLD.md#mod-tap-and-layer-tap) | Macro-on-tap is for physical matrix keys and requires the new target image; details and limits are listed in the guide. |
| **Encoder mapping** (`encoder-map`) | Assign keyboard actions to the encoder’s clockwise and counter-clockwise turns. | [CONFIGURATION](CONFIGURATION.md#keys-layers-and-encoder) | Uses the existing encoder map; both directions are configurable. |
| **Media keys** (`media-keys`) | Send actions such as volume, playback and track control to the computer. | [CONFIGURATION](CONFIGURATION.md#key-actions) | Limited to consumer actions supported by the firmware and host. |
| **Caps Word** (`caps-word`) | Caps Word keeps Shift active for letters and selected word characters. | [CONFIGURATION](CONFIGURATION.md#caps-word) | This is the board’s compact implementation; see keymap behavior. |
| **Repeat** (`repeat`) | Repeat sends the last eligible key again. | [CONFIGURATION](CONFIGURATION.md#repeat-and-alt-repeat) | Tracks eligible keyboard actions; some special actions are excluded. |
| **Alternate Repeat** (`alternate-repeat`) | Alternate Repeat sends the opposite key for supported key pairs. | [CONFIGURATION](CONFIGURATION.md#repeat-and-alt-repeat) | Only defined opposite-key pairs are supported. |
| **Tri Layer** (`tri-layer`) | Layer 3 activates when both configured layer keys are held. | [CONFIGURATION](CONFIGURATION.md#tri-layer) | Uses the fixed board layer arrangement: layers 1 and 2 activate layer 3. |
| **RGB effects** (`rgb-effects`) | Use the keyboard’s built-in RGB lighting effects. | [CONFIGURATION](CONFIGURATION.md#lighting) | Available effects depend on the existing RGB implementation. |

## Optional modules

| Module | Description | Guide | Limits |
| --- | --- | --- | --- |
| **NKRO reports** (`nkro-reports`) | The keyboard can report multiple simultaneous keys using NKRO. | [CONFIGURATION](CONFIGURATION.md#key-actions) | Report format depends on the selected profile and host support. |
| **Grave Escape** (`grave-escape`) | One key sends Grave or Escape according to the active modifier state. | [CONFIGURATION](CONFIGURATION.md#grave-escape) | Shift or GUI selects Grave by default; QMK Settings can change the flags. |
| **VialRGB Direct** (`vialrgb-direct-ram`) | Read a coherent 82-color HSV8 palette and upload complete frames through the Direct v1 protocol. | [Direct palette](DIRECT.md) | RAM only; does not enable or select RGB mode and does not save to EEPROM. Upload brightness is clamped to 160. |
| **NKRO control** (`nkro-control`) | Switch the keyboard report between 6KRO and NKRO for the current session. | [CONFIGURATION](CONFIGURATION.md#nkro-control) | Volatile; switching clears held keys and pending actions. |
| **One Shot** (`one-shot`) | Tap a modifier key once, then tap a key to apply it to that keystroke. | [CONFIGURATION](CONFIGURATION.md#one-shot) | No One Shot layer, timeout, locking or tap-toggle. Matrix keys and both encoder directions can arm One Shot; virtual or macro OSM uses the existing held-modifier fallback. |
| **Space Cadet** (`space-cadet`) | Shift keys send a parenthesis or Enter when tapped and act as Shift when held. | [CONFIGURATION](CONFIGURATION.md#space-cadet) | Three keys use the compact tap-hold path; they cannot be Combo inputs. |
| **Compact Leader** (`leader`) | Press Leader, then one selector within 300 ms to run a Vial macro. | [COMPACT-LEADER](COMPACT-LEADER.md) | One physical prefix and one basic selector; no dictionary or encoder/virtual prefix. |
| **Compact Mouse Keys** (`mouse-keys`) | Move the pointer, scroll or hold mouse buttons with keyboard keys. | [COMPACT-MOUSE-KEYS](COMPACT-MOUSE-KEYS.md) | Bounded board implementation with fixed cursor/wheel timing; see guide. |
| **Compact Auto Shift** (`auto-shift`) | Holding a supported key past 175 ms sends its shifted form. The beta.3 profile plan includes it in `main` and `typing`. | [COMPACT_AUTOSHIFT](COMPACT_AUTOSHIFT.md) | Only documented physical basic keys; the default threshold is 175 ms and QMK Settings can change it; several QMK actions excluded. |
| **Compact Dynamic Macros** (`dynamic-macros`) | Record and replay two temporary keyboard sequences. | [COMPACT-DYNAMIC-MACROS](COMPACT-DYNAMIC-MACROS.md) | Two RAM slots, up to 16 completed taps each; erased on restart. |
| **GUI lock** (`gui-lock`) | Temporarily suppress or restore GUI modifier output; W pulses while locked. | [GUI-CONTROL](GUI-CONTROL.md) | Available in `game` and `mmo`; off by default; a nonbase active/default layer overrides the pulse. |
| **Ctrl/GUI swap** (`ctrl-gui-swap`) | Swap left and right Ctrl and GUI output mappings for the session. | [GUI-CONTROL](GUI-CONTROL.md) | Volatile; does not enable persistent Magic settings. |
| **OS indicator override** (`os-indicators`) | Select the OS indicator state from a compatible desktop helper. | [INDICATORS](INDICATORS.md) | Volatile lease expires after 3 s; helper is not included and firmware does not detect OS. |
| **Mac/PC mode** (`mac-pc`) | Swap left and right Alt/GUI mappings to match a Mac layout. | [MAC-PC](MAC-PC.md) | Session-only; no host detection, F-row changes or stock Mac layout. |
| **Compact Tap Dance** (`tap-dance`) | Configure eight keys with tap, hold and repeated-tap actions. | [COMPACT-TAP-DANCE](COMPACT-TAP-DANCE.md) | Eight entries; only supported keyboard actions; extension storage schema 03. |
| **Key Overrides** (`key-overrides`) | Replace a key when selected modifiers and layer conditions match. | [COMPACT-KEY-OVERRIDES](COMPACT-KEY-OVERRIDES.md) | Eight rows with bounded trigger/replacement keys; extension storage schema 03. |
| **QMK Settings** (`qmk-settings`) | Change a small set of timing and behavior settings through Vial. | [QMK-SETTINGS](QMK-SETTINGS.md) | Only enumerated QSIDs are supported; extension storage schema 03. |
