Русский перевод: [creative](../ru/profiles/creative.md).

# creative — Editing and graphics

Application shortcut keys with Direct and runtime recording.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.
- Dynamic Macros: two temporary recordings of up to 16 completed key taps each.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- VialRGB Direct: direct RGB control from a compatible application.
- Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

## Changes from main

Added: Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

Removed: Key Overrides: eight modifier-dependent key replacements.

## Limits

Tap Dance: eight entries with four outputs using basic keys or keys with modifiers. Macro, layer and mouse actions are rejected.

Leader selects one of 16 saved Vial macros with a prefix and one 1–0 or A–F key.

The two runtime recordings of up to 16 completed key taps are temporary and lost after restart. They are separate from the 16 persistent Vial macros.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
