Русский перевод: [onehand](../ru/profiles/onehand.md).

# onehand — Reduced reach

Reduced-reach pointer and basic tap/hold bindings.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.
- Dynamic Macros: two temporary recordings of up to 16 completed key taps each.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- Mouse Keys: pointer movement, scrolling and mouse buttons.
- Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

## Changes from main

Added: Mouse Keys: pointer movement, scrolling and mouse buttons; Tap Dance: eight entries with tap, hold, double-tap and tap-hold outputs.

Removed: Key Overrides: eight modifier-dependent key replacements; VialRGB Direct: direct RGB control from a compatible application.

Auto Shift is not included.

## Limits

Tap Dance: eight entries with four outputs using basic keys or keys with modifiers. Macro, layer and mouse actions are rejected.

Leader selects one of 16 saved Vial macros with a prefix and one 1–0 or A–F key.

The two runtime recordings of up to 16 completed key taps are temporary and lost after restart. They are separate from the 16 persistent Vial macros.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

Direct is disabled; built-in RGB effects remain available.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
