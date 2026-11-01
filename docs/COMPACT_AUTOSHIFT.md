Русский перевод: [Компактный Auto Shift](ru/COMPACT_AUTOSHIFT.md).

# Compact Auto Shift

Auto Shift lets you type a shifted character without holding Shift: tap A for
`a`, or hold it for at least 175 ms for `A`, with a typical English computer
layout. The computer's layout determines the actual character.

In published beta.5 this feature is included only in the `main` and `typing`
profiles (a profile is a set of firmware features, not a layer). Mapping a key
in Vial cannot add it to another profile. The current source is separate and not
release-qualified; see [Status](STATUS.md). Fresh or reset settings enable Auto
Shift for all supported categories with a 175 ms hold interval; saved settings
can differ.

## Using Vial

Open your keyboard in Vial. You can assign `AS_ON`, `AS_OFF` or `AS_TOGG` to a
physical key to turn Auto Shift on, off or switch it until restart; the selected
categories remain unchanged. These mappings require a settings write.

QMK Settings entry 3 stores whether Auto Shift starts enabled and which categories
are excluded. Its value adds the desired flags: enabled 1, exclude punctuation
4, digits 8, letters 16. Default 1 means enabled with no exclusions; for example,
9 enables it but excludes digits. A successful change applies immediately and
persists after restart. Entry 4 sets the interval from 1 to 1000 ms. `AS_UP`,
`AS_DOWN` and `AS_RPT` are not supported.

**Before changing anything:** the published beta.5 catalog does not authorize
settings writes. Compatibility alone does not authorize them. On affected
firmware, avoid standard Vial QMK Settings Save and Reset until the client and
exact image are confirmed compatible: saving an unrelated value can change the
Caps Word language. See [QMK Settings](QMK-SETTINGS.md) and
[backup and restore](SETTINGS-BACKUP.md) for details and recovery limits.

## Keys and timing

The engine accepts direct physical basic keys: A–Z, 1–0, Minus through Slash
(including the non-US hash key), and the non-US backslash key. It does not delay
Space, Enter, Tab, Backspace, navigation keys, function keys or modifiers.
The host keyboard layout determines the printed characters.

A release before the configured interval sends an ordinary press and release. At
the interval or later,
the engine holds the key with left Shift until its physical release. The host
can repeat that held shifted key. A different press before the threshold sends
the pending key without adding Shift, before processing the new key. Its
physical release still releases the original key.

Only one key can be processed by Auto Shift at a time. Other keys work
immediately while it remains down, but cannot start another Auto Shift decision.
The added Shift affects other keys pressed while that key is held. Releasing it
removes its added Shift, but a physical Shift or another held modifier remains.

Existing modifiers bypass the delay. These include held Shift, Ctrl, Alt and
GUI (Windows or Command), and a One Shot modifier waiting for the next key. A real Shift press
that interrupts a pending key is processed after the pending ordinary press.
Caps Word still processes the emitted key. Repeat and Alternate Repeat remember
the automatically added Shift.

## Other actions

In the firmware source in this tree, failed Combo inputs bypass Auto Shift.
Routing them through Auto Shift is deferred after a candidate main image overflowed
its CODE window by 156 bytes; this deferral has not been shown to fit. Successful
Combo outputs bypass Auto Shift by default. An experimental,
non-catalog source build can define `AK820_COMBO_AUTOSHIFT` with compact Combo,
Auto Shift and tapping enabled. For an eligible successful output, timing starts
when the second input completes the pair; the first input release ends the output.
Disabled or filtered Auto Shift, active modifiers, a busy owner and ineligible
outputs retain the immediate Combo path. This is a compile-time opt-in, not a
persistent setting or profile-builder option. Standard profile names and build
metadata alone do not identify an image built with this define. The opt-in has
host tests only and still needs exact-image stack, interrupt and regression
qualification; it is not a published catalog profile.

Mod-Tap, Layer-Tap and Space Cadet taps also bypass Auto Shift. Encoder actions,
macros and generated Repeat actions are immediate.

The key action selected when pressed is retained through release. Changing a mapping or layer
while the key is pending or held cannot change its eventual release. Clearing
the keyboard, starting Vial unlock or switching the NKRO mode cancels the owner;
subsequent ticks and releases cannot revive it. `AS_OFF` prevents new decisions
and preserves an already emitted key until its physical release. An interrupted
pending key is resolved before the physical control key changes the mode.

This is a bounded board feature. It does not enable upstream QMK Auto Shift,
Retro Shift, per-key callbacks or repeat-on-second-tap. The timing and report-wide Shift behavior follow the
relevant concepts in the [QMK Auto Shift documentation](https://docs.qmk.fm/features/auto_shift).


Development status and limits are recorded in the [technical report](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/compact-runtime-20261024/README.md).
