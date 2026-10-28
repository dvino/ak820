Русский перевод: [Настройка клавиатуры](ru/CONFIGURATION.md).

# Configure the keyboard

Use a compatible Vial client with this firmware. Close the OEM configurator
before connecting. The old `AK820-Vial-v2` OEM adapter uses a different protocol
and is not the configuration interface for this QMK/Vial firmware.

The current catalog contains ten curated profiles and defaults to `main`.
All ten include modifier One Shot. NKRO control is available in `game` and
`mmo`; limited Space Cadet actions are available in `typing` and `code`.
See [Build profiles](BUILD-PROFILES.md).

Select a key in Vial's keyboard picture and choose an action. Vial sends keymap
and lighting changes to the keyboard as you make them. Export the layout when
you want a separate backup; it is different from the ROM recovery copy made by
the installer. See [Settings backup and restore](SETTINGS-BACKUP.md).

## Keys, layers and encoder

The keymap has six layers, numbered 0–5.
Assign keyboard actions to the encoder’s clockwise and counter-clockwise turns.

The keyboard has six editable layers, numbered 0–5. A transparent key (`KC_TRNS`)
uses the action on the next lower active layer. `KC_NO` blocks the key and sends
nothing. Keep a working layer-switch key on any layer you use, or you may have
no convenient way back.

Layer actions have different effects:

| Action | Effect |
| --- | --- |
| `MO(n)` | Hold to activate layer *n*; release removes this hold. |
| `TG(n)` | Toggle layer *n*; another hold or default layer can keep it active. |
| `TO(n)` | Make layer *n* the only toggled layer; held layers remain active. |
| `DF(n)` | Set layer *n* as the default layer. |
| `LM(n, mods)` | Hold for layer *n* and selected modifiers; release removes this hold. |
| `TT(n)` | Toggle layer *n* on each press in this firmware. |

Layer holds are independent: releasing one key or using `TO`/`TG` does not
cancel another held key. Default layers still apply.

For example, assign `MO(1)` to a thumb key on layer 0, then put navigation keys
on layer 1 and leave the rest transparent. Hold the thumb key to use navigation;
release it to return to layer 0. `TT(n)` is a toggle here, not the usual tap/hold
layer action: this firmware disables QMK tap timing.

### Tri Layer

Layer 3 activates when both configured layer keys are held.

Assign `TL_LOWR` and `TL_UPPR` to two keys. They hold layers 1 and 2; when both
are held, the firmware also activates layer 3. Releasing either key removes
its layer and derived layer 3. For example, place configuration actions on
layer 3 and use the two keys together to reach it. The lower and upper target
layers are fixed to 1 and 2 in this build.

Each of the encoder's clockwise and counterclockwise actions can be set
separately on each layer. For example, layer 0 can use volume down/up while
layer 1 uses previous/next track. Pressing the encoder's push switch is an
ordinary key and can be assigned separately on each layer.

## Key actions

Send actions such as volume, playback and track control to the computer.
The keyboard can report multiple simultaneous keys using NKRO.

Standard keyboard keys and modifiers send ordinary key presses. Consumer and
system actions send media controls such as volume, play/pause or next track,
and system controls such as sleep. The host must support the corresponding HID
control for it to have an effect.

The `game` and `mmo` profiles support both six-key rollover (6KRO) and NKRO reports. Assign
`NK_ON`, `NK_OFF` or `NK_TOGG` to switch the report mode until restart; after
restart, the saved/default mode is used. Switching clears held keys and pending
actions. No setting is written to flash. In 6KRO mode, holding more than six
distinct ordinary keys replaces all six key slots with the HID ErrorRollOver
signal. Two sources that produce the same keycode count as one key.

## Caps Word

Caps Word keeps Shift active for letters and selected word characters.

Assign `CW_TOGG` to a key to turn Caps Word on or off. It makes letters uppercase.
Holding both left and right Shift activates Caps Word when the second Shift is
pressed. A quick double press of left Shift also activates it when the second
press begins less than 200 ms after the first press, with left Shift released
between presses. Holding one Shift, waiting too long, pressing another key or
clearing/unlocking the mode cancels the double-press sequence. These gestures
are available in all ten profiles. Macro events, Repeat and non-matrix inputs
do not trigger them.
Digits, Backspace, Delete and underscore continue the mode; minus is sent as
underscore. Other ordinary keys that are not letters or listed word characters
end it. The mode also ends after five seconds without a key press. For example, type `user_name7` with
Caps Word on, then press Space to turn the mode off as the next word begins.

New settings default to Russian. Existing saved English (`0`) selections remain
unchanged; to fix premature termination on Russian letters such as `б`, explicitly
set QSID 22 to Russian (`1`) or use keycode `0x7e01`. The English mode remains
available (`0`); the firmware cannot detect or switch the host keyboard layout. Russian rules
add `х`, `ъ`, `ж`, `э`, `б`, `ю` and `ё` on `LBRC`, `RBRC`, `SCLN`, `QUOT`,
`COMM`, `DOT` and `GRV`. These seven key positions act as letters for Caps Word;
their punctuation output still follows the computer's layout. The firmware does
not change that layout. Minus becomes underscore in both rulesets. Changing the language ends active Caps Word only when the
selection differs; it also removes temporary Shift. Re-selecting the current
language preserves the active word and its timer. The language selectors
`0x7e00`, `0x7e01` and `0x7e02` choose English, choose Russian and toggle the
selection for the session; they do not output OS layout changes. The indicator
light mode is not a language indicator. Language selection preserves queued One
Shot modifiers and held-action ownership.

## Repeat and Alt Repeat

Repeat sends the last eligible key again.
Alternate Repeat sends the opposite key for supported key pairs.

Assign `QK_REPEAT_KEY` (the `QK_REP` alias) to repeat the last repeatable key.
The firmware remembers the modifiers held with that key, so pressing `Ctrl+F`
and then Repeat sends `Ctrl+F` again. Layer controls, modifiers by themselves,
Repeat and Alt Repeat do not replace the remembered key.

Assign `QK_ALT_REPEAT_KEY` (`QK_AREP`) for a related action. With no modifier or
only Shift, examples include `J`↔`K`, `H`↔`L`, `W`→`B`, `E`→`B` and `B`→`W`; with Ctrl, Alt or
GUI, examples include `F`↔`B`, `N`↔`P` and `A`↔`E`. Arrows, Home/End,
PageUp/PageDown, Backspace/Delete, brackets, volume and media-track keys also
have opposing pairs. The captured modifiers are applied to the alternate key.
If the last key has no defined alternate, Alt Repeat sends nothing.

## Grave Escape

One key sends Grave or Escape according to the active modifier state.

Assign `QK_GESC` to use one key for Escape and Grave.
It sends Escape normally and Grave while Shift or GUI is held. The key released
is the same one selected when it was pressed. For example, tap it for Escape or
hold Shift and press it to send Shift+Grave. The resulting character depends
on the host keyboard layout. By default Alt and Ctrl do not change this choice.
The `settings` profile can change the Grave Escape override flags through
[QMK Settings](QMK-SETTINGS.md).

## Mod-Tap and Layer-Tap

A quick press sends the tap key; holding activates its modifier or layer action.

A short tap sends the tap key; holding activates its modifier or layer. The
window defaults to 200 ms and QMK Settings can change it from 1 to 1000 ms.
Pressing another key first selects hold. For example, assign Ctrl-Tap-Escape
to a key: tap it for Escape or press it with another key to use Ctrl. See [Tap
and hold](TAP-HOLD.md) for overlap and layer behavior.

## Space Cadet

Shift keys send a parenthesis or Enter when tapped and act as Shift when held.

Assign `SC_LSPO` for left Shift with `(` on tap, `SC_RSPC` for right Shift with
`)` on tap, or `SC_SENT` for right Shift with Enter on tap. Parentheses use
Shift+9 and Shift+0; the resulting characters depend on the host layout. These
actions use the same configurable tap-hold decision as Mod-Tap (200 ms by
default). They are not the full QMK Space Cadet engine. Space Cadet keycodes
cannot be used as Combo inputs. See [Build profiles](BUILD-PROFILES.md) for
tested limits.

### NKRO control

Switch the keyboard report between 6KRO and NKRO for the current session.

Assign `NK_ON`, `NK_OFF` or `NK_TOGG` to a physical key. Switching clears held
keys and pending actions, and the selection is not saved across restart. This
control is present in `game` and `mmo`.

## One Shot

Tap a modifier key once, then tap a key to apply it to that keystroke.

Assign an `OSM(...)` action to a physical matrix key or either encoder direction,
tap and release it, then press a consuming matrix key or turn the encoder. The
queued modifier remains active through the consuming action's release. Several
queued OSM modifier sets combine. If another OSM is pressed while a consuming
action is still held, it acts as a held modifier only and does not queue another
set. Matrix keys and both encoder directions can set or consume One Shot.
Virtually injected OSM events do not arm the One Shot queue. They retain the
ordinary held-modifier fallback: macro down/up holds and releases the modifier;
a macro tap does not leave it queued for the next key. Layer One Shot, locking
and tap-toggle are not supported. QSID 6 sets the saved timeout from 0
to 30000 ms; zero means unlimited. The timer starts or refreshes when an unused
OSM key is released.

## Two-key Combos

Configure eight two-key combinations that send one key or modified key.

`CM_ON`, `CM_OFF` and `CM_TOGG` control Combos for the session from physical
keys; they start enabled after restart. Changing the actual state sends a
buffered key first, then clears held actions across the keyboard. Release held
keys before pressing again. The saved slots do not change.

The firmware has eight configurable two-key Combo slots. A configured pair
pressed within the selected interval sends one output instead of its two input
keys. The interval defaults to 40 ms; QMK Settings can change it from 1 to
1000 ms with the `settings` profile's QMK Settings module. For example, set `J` + `K` to
`Escape`, or `F` + `D` to `Ctrl+C`. Configure the pair and output using Vial's
Combo controls. See [Two-key Combos](COMBOS.md) for supported inputs, outputs,
timing, and backup behavior.

The first key may be delayed for up to the selected interval while the firmware
checks for its partner. At the interval, or when another key/event arrives first,
it is sent normally.
Combos accept ordinary keyboard keys as inputs. Their output can be an ordinary
key or a modifier combined with an ordinary key. Modifiers, layer actions,
macros, encoder events and other special actions cannot be Combo inputs.

## Macros

Store and edit 16 keyboard macros in Vial.

There are 16 macro slots with 8192 bytes of shared storage. Record or edit
macros in Vial's macro editor. A macro runs on the keyboard, so the Vial client
does not need to remain open. For each key press, include a matching release.
Macros can include key taps, held key-down/key-up commands, delays and text.
Text is limited to ASCII bytes; Unicode text is not supported. For example, a
Ctrl+C macro presses Ctrl, presses C, releases C, then releases Ctrl. Include
a release for each key-down that should not remain held. The 8192-byte limit is
shared by all slots, so long scripts leave less space for the others. See [Settings backup and restore](SETTINGS-BACKUP.md)
before replacing firmware or moving a layout.

The current source adds a macro-on-tap, layer-on-hold action for
physical matrix keys. Enter its AK820 keycode in an editor that accepts numeric
values; see [Tap and hold](TAP-HOLD.md#macro-on-tap-layer-on-hold) for the
formula, example and limits. Earlier firmware does not support this action.

## Caps and layer indicators

The dedicated **C** indicator lights when host Caps Lock or local Caps Word is
active. **W** lights when any layer above layer 0 is
active, including held, toggled or default layers. These indicators work
independently of key lighting. See [C, W and OS indicators](INDICATORS.md) and [Mac/PC mode](MAC-PC.md).

## Unlocking Vial

To unlock Vial, make a fresh physical hold of Escape and left Control together
for three seconds. This also releases keys the firmware still considers held.
Release both keys after the unlock. Lock Vial again when finished configuring.

## Lighting

Use the keyboard’s built-in RGB lighting effects.
Adjust supported RGB settings through VialRGB; changes apply in RAM.

Supported modes are solid color, breathing, color cycle, horizontal color
cycle, VialRGB Direct and Solid Reactive Simple. Use Vial's lighting controls
or assign the available RGB keycodes to keys. Brightness, color and speed are
global settings. Direct uses an 82-entry HSV8 palette in RAM. Its protocol can
read a coherent snapshot and apply a complete frame; it does not enable or
select RGB mode, and the palette is lost when the keyboard restarts. See the
[Direct palette guide](DIRECT.md) for host API and restore details. Global
lighting settings are saved separately.

In Solid Reactive Simple, pressing a key lights its LED and starts that LED's
fade. Each press fades independently; holding the key does not keep it lit, and
releasing the key does not shorten the fade. It does not create a wave across
the keyboard. Changing modes, turning lighting off, suspending the keyboard or
reloading settings clears the previous presses. The speed setting selects one
of four fade times: 0–63 is 2048 ms, 64–127 is 1024 ms, 128–191 is 512 ms, and
192–255 is 256 ms. A lighting option displayed by Vial does not by itself
mean that the firmware supports it.

## Limits

The available profiles and their limits are listed in
[Build profiles](BUILD-PROFILES.md). A Vial control alone does not add firmware
support. Before assigning an action, check that it is supported by the installed
firmware.

Development profiles provide separate compact [Tap Dance](COMPACT-TAP-DANCE.md),
[Key Overrides](COMPACT-KEY-OVERRIDES.md) and [QMK Settings](QMK-SETTINGS.md)
modules. Select a supported combination from [Build profiles](BUILD-PROFILES.md).
