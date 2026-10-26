Русский перевод: [pointer](../ru/profiles/pointer.md).

# pointer — Pointer control

Keyboard pointer control with macros and Leader retained.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.
- Dynamic Macros: two temporary recordings of up to 16 completed key taps each.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- Key Overrides: eight modifier-dependent key replacements.
- Mouse Keys: pointer movement, scrolling and mouse buttons.

## Changes from main

Added: Mouse Keys: pointer movement, scrolling and mouse buttons.

Removed: VialRGB Direct: direct RGB control from a compatible application.

Auto Shift is not included.

## Limits

Key Overrides: eight modifier-dependent replacements.

Leader selects one of 16 saved Vial macros with a prefix and one 1–0 or A–F key.

The two runtime recordings of up to 16 completed key taps are temporary and lost after restart. They are separate from the 16 persistent Vial macros.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

Direct is disabled; built-in RGB effects remain available.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
