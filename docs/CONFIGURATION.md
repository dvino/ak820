Русский перевод: [Настройка клавиатуры](ru/CONFIGURATION.md).

# Configure the keyboard

Use a compatible Vial client with this firmware. Close the OEM configurator
before connecting. The old `AK820-Vial-v2` OEM adapter uses a different protocol
and is not the configuration interface for this QMK/Vial port.

## Keys and layers

Select a key in Vial's keyboard picture and choose what it should do. There are
six layers, numbered 0–5. A transparent key uses the action from a lower active
layer. `KC_NO` does nothing. When you edit an upper layer, leave a key that can
switch to another layer. You can set a different action for each direction of
the encoder on every layer. Pressing the encoder acts like pressing a regular
key.

Supported actions include standard keys and modifiers, media/system controls,
MO/TO/TG/DF/LM, Caps Word, Repeat, Alt Repeat, Grave Escape and Tri Layer. Lower/Upper use
layers 1/2 and activate layer 3 together. In the bundled legacy release,
ordinary MO(1)/MO(2) do not activate Tri Layer. The compact development profile
derives Adjust whenever both configured input layers are active, including
MO, toggle and default-layer state. Each momentary hold retains its own owner.

Vial may show unsupported actions. The bundled legacy release sends only the
tap key for Mod-Tap and Layer-Tap. Development source adds the compact hold
behavior described in [Tap and hold](TAP-HOLD.md); see [Status](STATUS.md)
for its approval and test state. One Shot, Mouse Keys, Tap Dance, Combos and
Key Overrides remain unsupported. Importing a layout does not add them.

## Macros and persistence

There are 16 macro slots with 8192 bytes of shared space. Create macros in
Vial's macro editor. For every key press in a macro, include a matching release.
The keyboard plays the macro itself; no desktop app needs to stay open. Before
replacing firmware, export your Vial layout so you can restore it later. That
export is separate from the personal ROM recovery image made during installation.

## Unlock and lighting

To unlock Vial, hold the physical Escape and left Control keys together for
three seconds. This also releases any keys the firmware thinks are still held.
Lock Vial again when you finish configuring the keyboard.

Lighting includes solid color, breathing, color cycle, horizontal cycle,
VialRGB Direct and the RC6 candidate's Solid Reactive Simple (Vial effect 31).
Each key press lights that key's LED and starts its own fade. The light fades
out even while you keep holding the key; releasing it does not shorten the fade.
When no keys are pressed, all LEDs are black. The effect fades at each key; it
does not send a ripple or wave across the keyboard.

The reactive speed setting selects a fade time: 0–63 means 2048 ms,
64–127 means 1024 ms, 128–191 means 512 ms, and 192–255 means 256 ms. The
firmware updates the fade every 16 ms. Changing the lighting mode, turning off
the LEDs, suspending the keyboard or reloading settings clears the previous
presses. The owner reports that reactive lighting works normally on the installed
candidate. This is a device observation, not a new automated test or an exact
comparison with the OEM effect.

Direct per-LED colors are kept in temporary memory and are lost when the
keyboard restarts. Global lighting settings are saved. The smaller brightness
curve can round the displayed brightness slightly, but it leaves the saved and
transmitted HSV color values unchanged. See the [memory budget](RESOURCE-BUDGET.md)
and [status](STATUS.md) for the measured limits and test results. A lighting
option appearing in Vial does not by itself mean the firmware supports it.
