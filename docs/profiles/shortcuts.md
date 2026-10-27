Русский перевод: [shortcuts](../ru/profiles/shortcuts.md).

# shortcuts — Prepared commands

Prepared persistent commands and modifier overrides.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- Key Overrides: eight modifier-dependent key replacements.
- Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

## Changes from main

Added: Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

Removed: Dynamic Macros: two temporary recordings of up to 16 completed key taps each; VialRGB Direct: direct RGB control from a compatible application.

Auto Shift is not included.

## Limits

Tap Dance: eight entries with four outputs using basic keys or keys with modifiers. Macro, layer and mouse actions are rejected.

Key Overrides: eight modifier-dependent replacements.

Leader selects one of 16 saved Vial macros with a prefix and one 1–0 or A–F key.

Runtime macro recording is absent; the 16 persistent Vial macros remain available.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

Direct is disabled; built-in RGB effects remain available.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
