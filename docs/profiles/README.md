Русский перевод: [Профили](../ru/profiles/README.md).

# Firmware profiles

All functions do not fit in the controller memory at once. The firmware therefore uses modules: each profile selects the functions available in one image. `main` is the default. Other profiles exchange some of its modules for functions suited to a particular task.

Choosing a profile changes the firmware. Switching a layer in Vial cannot add an absent module. The Windows and Linux installer offers profile selection; installation requires a verified and approved exact image. The AK Configurator companion is still in development. See [installation](../INSTALL.md) for the steps and [Status](../STATUS.md) for release availability.

| Profile | Purpose |
| --- | --- |
| [main](main.md) | Universal reference configuration. |
| [game](game.md) | Games with NKRO, GUI lock and Direct. |
| [mmo](mmo.md) | Multi-action game bindings; Tap Dance replaces Key Overrides. |
| [typing](typing.md) | Text entry with Auto Shift and Space Cadet. |
| [code](code.md) | Manual-shift coding with Space Cadet and Grave Escape. |
| [pointer](pointer.md) | Keyboard pointer control with macros and Leader retained. |
| [onehand](onehand.md) | Reduced-reach pointer and basic tap/hold bindings. |
| [creative](creative.md) | Application shortcut keys with Direct and runtime recording. |
| [shortcuts](shortcuts.md) | Prepared persistent commands and modifier overrides. |
| [multios](multios.md) | Modifier switching between host workflows with built-in lighting. |

## Shared functions

All ten profiles provide:

- Six editable layers and encoder actions for each layer.
- 16 saved Vial macros and eight two-key Combos.
- Mod-Tap and Layer-Tap, One Shot, Caps Word, Repeat and Alt Repeat, Tri Layer.
- Media and system keys, built-in RGB effects.
- QMK Settings for supported timing parameters.
- C (Caps Lock) and W (active layer above zero) indicators, and host control of OS.

The [feature catalog](../FEATURES.md) describes configuration and limits. NKRO, Grave Escape, Space Cadet and Direct depend on the selected profile.

## Module limits

Tap Dance has eight entries. Its four outputs accept a basic keyboard key, a modifier, or a key with encoded modifiers; layers, macros, mouse actions and nested special actions are unsupported. Key Overrides has eight replacements. Leader selects one of the 16 saved Vial macros.

The two Dynamic Macro recordings hold up to 16 completed key taps each in RAM and are lost after restart. These recordings are separate from the 16 Vial macros saved in keyboard storage.

The OS indicator does not detect the operating system or layout. A compatible host helper selects its state and refreshes a lease; three seconds without refresh restores normal indicator behavior. In `multios`, that behavior follows the temporary Mac/PC mode; in the other profiles, OS is off.

[Tap Dance](../COMPACT-TAP-DANCE.md) · [Key Overrides](../COMPACT-KEY-OVERRIDES.md) · [Leader](../COMPACT-LEADER.md) · [Dynamic Macros](../COMPACT-DYNAMIC-MACROS.md) · [Indicators](../INDICATORS.md)
