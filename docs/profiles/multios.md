Русский перевод: [multios](../ru/profiles/multios.md).

# multios — Multiple operating systems

Modifier switching between host workflows with built-in lighting.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.
- Dynamic Macros: two temporary recordings of up to 16 completed key taps each.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- Key Overrides: eight modifier-dependent key replacements.
- Mac/PC mode: swap Alt and GUI.
- Swap Ctrl and GUI.
- Tap Dance: eight entries for basic or modified key actions on tap and hold.

## Changes from main

Added: Mac/PC mode: swap Alt and GUI; Swap Ctrl and GUI; Tap Dance for basic or modified key actions.

Removed: VialRGB Direct: direct RGB control from a compatible application.

Auto Shift is not included.

## Limits

Tap Dance has eight entries; its outputs cannot be macros, layers, mouse actions or nested special actions.

Key Overrides: eight modifier-dependent replacements.

Leader selects one of 16 saved Vial macros with a prefix and one 1–0 or A–F key.

The two runtime recordings of up to 16 completed key taps are temporary and lost after restart. They are separate from the 16 persistent Vial macros.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

Direct is disabled; built-in RGB effects remain available.

Alt/GUI and Ctrl/GUI swaps last until restart; defaults are PC mode with no Ctrl/GUI swap.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
