Русский перевод: [game](../ru/profiles/game.md).

# game — Games

Games with NKRO, GUI lock and Direct.

The [shared functions](README.md#shared-functions) are included.

## Profile modules

- One Shot modifiers.
- Dynamic Macros: two temporary recordings of up to 16 completed key taps each.
- Host-controlled OS indicator.
- QMK Settings: supported timing parameters.
- Key Overrides: eight modifier-dependent key replacements.
- VialRGB Direct: direct RGB control from a compatible application.
- NKRO keyboard reports.
- NKRO on/off controls.
- GUI lock: block Win/Command keys.

## Changes from main

Added: NKRO keyboard reports; NKRO on/off controls; GUI lock: block Win/Command keys.

Removed: Leader: a prefix followed by one 1–0 or A–F key selects one of 16 saved Vial macros.

## Limits

Key Overrides: eight modifier-dependent replacements.

The two runtime recordings of up to 16 completed key taps are temporary and lost after restart. They are separate from the 16 persistent Vial macros.

OS uses a host-refreshed indicator lease; the firmware does not detect the OS or layout.

[Full module limits](README.md#module-limits) · [Choose a profile](README.md) · [Installation](../INSTALL.md)
