Русский перевод: [Настройка клавиатуры](ru/CONFIGURATION.md).

# Configure the keyboard

Use a compatible Vial client with this firmware. Close the OEM configurator
before connecting. The old `AK820-Vial-v2` OEM adapter uses a different protocol
and is not the configuration interface for this QMK/Vial firmware.

Select a key in Vial's keyboard picture and choose an action. Vial sends keymap
and lighting changes to the keyboard as you make them. Export the layout when
you want a separate backup; it is different from the ROM recovery copy made by
the installer. See [Settings backup and restore](SETTINGS-BACKUP.md).

## Keys, layers and encoder

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

Standard keyboard keys and modifiers send ordinary key presses. Consumer and
system actions send media controls such as volume, play/pause or next track,
and system controls such as sleep. The host must support the corresponding HID
control for it to have an effect.

The default keymap setting uses six-key rollover (6KRO). NKRO reporting code
is present, but this firmware does not provide a supported key to switch modes.
When more than six distinct ordinary keys are held, the 6KRO report replaces
all six key slots with the HID ErrorRollOver signal. Releasing keys until six or
fewer remain clears that signal and reports the surviving keys. Two sources
that produce the same keycode count as one distinct key.

## Caps Word

Assign `CW_TOGG` to a key to turn Caps Word on or off. It makes letters uppercase.
Digits, Backspace, Delete and underscore continue the mode; minus is sent as
underscore. Other ordinary keys, including punctuation, end it. The mode also
ends after five seconds without a key press. For example, type `user_name7` with
Caps Word on, then press Space to turn the mode off as the next word begins.

## Repeat and Alt Repeat

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

Assign `QK_GESC` to use one key for Escape and Grave.
It sends Escape normally and Grave while Shift or GUI is held. The key released
is the same one selected when it was pressed. For example, tap it for Escape or
hold Shift and press it to send Shift+Grave. The resulting character depends
on the host keyboard layout. Alt and Ctrl do not change the
choice in this build.

## Mod-Tap and Layer-Tap

A short tap sends the tap key; holding activates its modifier or layer. The
decision window is 200 ms, and pressing another key first selects hold. For
example, assign Ctrl-Tap-Escape to a key: tap it for Escape or press it with
another key to use Ctrl. See [Tap and hold](TAP-HOLD.md) for overlap and layer
behavior.

## Two-key Combos

The firmware has eight configurable two-key Combo slots. A configured pair
pressed within 40 ms sends one output instead of its two input keys. For
example, set `J` + `K` to `Escape`, or `F` + `D` to `Ctrl+C`. Configure the
pair and output using Vial's Combo controls. See [Two-key Combos](COMBOS.md) for
supported inputs, outputs, timing, and backup behavior.

The first key may be delayed for up to 40 ms while the firmware checks for its
partner. At 40 ms, or when another key/event arrives first, it is sent normally.
Combos accept ordinary keyboard keys as inputs. Their output can be an ordinary
key or a modifier combined with an ordinary key. Modifiers, layer actions,
macros, encoder events and other special actions cannot be Combo inputs.

## Macros

There are 16 macro slots with 8192 bytes of shared storage. Record or edit
macros in Vial's macro editor. A macro runs on the keyboard, so the Vial client
does not need to remain open. For each key press, include a matching release.
Macros can include key taps, held key-down/key-up commands, delays and text.
Text is limited to ASCII bytes; Unicode text is not supported. For example, a
Ctrl+C macro presses Ctrl, presses C, releases C, then releases Ctrl. Include
a release for each key-down that should not remain held. The 8192-byte limit is
shared by all slots, so long scripts leave less space for the others. See [Settings backup and restore](SETTINGS-BACKUP.md)
before replacing firmware or moving a layout.

## Caps and layer indicators

The dedicated **C** indicator follows the host's Caps Lock state. Caps Word
does not turn it on by itself. **W** lights when any layer above layer 0 is
active, including held, toggled or default layers. These indicators work
independently of key lighting. See [C and W indicators](INDICATORS.md).

## Unlocking Vial

To unlock Vial, make a fresh physical hold of Escape and left Control together
for three seconds. This also releases keys the firmware still considers held.
Release both keys after the unlock. Lock Vial again when finished configuring.

## Lighting

Supported modes are solid color, breathing, color cycle, horizontal color
cycle, VialRGB Direct and Solid Reactive Simple. Use Vial's lighting controls
or assign the available RGB keycodes to keys. Brightness, color and speed are
global settings. Direct mode lets you set individual LED colors; those colors
are kept in temporary memory and are lost when the keyboard restarts. The
global lighting settings are saved.

In Solid Reactive Simple, pressing a key lights its LED and starts that LED's
fade. Each press fades independently; holding the key does not keep it lit, and
releasing the key does not shorten the fade. It does not create a wave across
the keyboard. Changing modes, turning lighting off, suspending the keyboard or
reloading settings clears the previous presses. The speed setting selects one
of four fade times: 0–63 is 2048 ms, 64–127 is 1024 ms, 128–191 is 512 ms, and
192–255 is 256 ms. A lighting option displayed by Vial does not by itself
mean that the firmware supports it.

## Limits

This firmware does not support One Shot actions, Mouse Keys, Tap Dance, Key
Overrides or Auto Shift. Other generic QMK/Vial options may also appear in the
client without firmware support. Importing a layout cannot add missing firmware
features. When an action is important, verify that it is included here or in a
linked guide before assigning it.
