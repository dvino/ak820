Русский перевод: [README на русском](docs/ru/README.md).

# QMK and Vial for AJAZZ AK820

![AJAZZ AK820 QMK / Vial firmware banner](docs/images/banner.webp)

This project brings QMK and Vial to the **wired AJAZZ AK820 with a VS11K28A / CH555-like 8051 controller**, USB `320F:505B`. AK820 V2, Pro and Max use different hardware and are not supported.

Set up keys, layers, the encoder and macros in Vial. After that, the keyboard works without a desktop app running in the background. The port keeps the keyboard's original loader and stores settings in the keyboard.

## Hardware Compatibility

| Model | Microcontroller | Support |
| --- | --- | --- |
| AJAZZ AK820 (wired) | VS11K28A | Supported |
| AJAZZ AK820 V2 | Different platform | No |
| AJAZZ AK820 Pro | Different platform | No |
| AJAZZ AK820 Max | Different platform | No |

USB VID:PID `320F:505B` is an additional identifying sign, not a compatibility guarantee. The AK820 name alone is not enough either. Check the controller and PCB revision against the photos below before installing firmware.

Keep the original recovery files and read [stock firmware recovery](docs/INSTALL.md#oem-recovery).

<a href="docs/images/pcb-markings.webp"><img src="docs/images/pcb-markings.webp" alt="PCB markings: SG-8976 VS11K28A RGB, Ver:01" width="320"></a>

<details>
<summary>PCB and controller photos</summary>

![PCB](docs/images/pcb.webp)

![VS11K28A](docs/images/controller.webp)

</details>

## Features

- Six editable layers, with separate clockwise and counterclockwise encoder actions on each layer.
- Standard keys, modifiers, media and system controls. The default report supports six distinct ordinary keys at once.
- Sixteen macro slots with 8192 bytes of shared storage; macros play on the keyboard without a desktop app running.
- **Caps Word** types a word in uppercase without holding Shift.
- **Repeat** repeats the last remembered key and modifiers; **Alt Repeat** uses its paired alternate, such as the opposite arrow.
- **Grave Escape** combines Escape and the Grave key on one key, selected by held modifiers.
- **Tri Layer** activates layer 3 while layers 1 and 2 are both active.
- Eight configurable [two-key Combos](docs/COMBOS.md): for example, J + K sends Escape or F + D sends Ctrl+C when pressed within 40 ms.
- [Mod-Tap and Layer-Tap](docs/TAP-HOLD.md): tap for a key, hold for a modifier or layer.
- 82 RGB LEDs with solid color, breathing, color cycles, VialRGB Direct and a separate fade on each pressed key.
- [C/W indicators](docs/INDICATORS.md): C follows Caps Lock; W shows an active additional layer.
- Saved keymaps, macros and global lighting, physical Vial unlock, and [settings backup and restore](docs/SETTINGS-BACKUP.md), including all eight Combo slots.

See [Configuration](docs/CONFIGURATION.md) for assignment examples and limits.
One Shot, Mouse Keys, Tap Dance, Key Overrides, Auto Shift and a user-facing
NKRO mode switch are not supported.

## Disclaimer

The source code, firmware and tools are provided **“as is”, without warranties**
of any kind. Use, modification, flashing and recovery are performed at the
user's own risk. The user is responsible for checking hardware compatibility,
keeping backups and any resulting damage, an unusable device or loss of data.

To the extent permitted by applicable law, the authors and contributors are
not liable for damage or losses caused by using or being unable to use this
project. See sections 15–17 of the [LICENSE](LICENSE).

## Get started

> Install only on the supported wired hardware revision. A mismatched image can leave the keyboard unusable; a matching USB ID does not make another revision safe.

Download the Windows or Linux package from [Releases](https://github.com/dvino/ak820/releases), then follow the [installation and recovery guide](docs/INSTALL.md).

Read [Settings backup](docs/SETTINGS-BACKUP.md) for backup, restore and update
instructions.

Use [Configuration](docs/CONFIGURATION.md) to remap keys, layers, macros and lighting in Vial. To build from source, see [Build](docs/BUILD.md); firmware builds use Linux/WSL, Python 3.11+ and the pinned SDCC 4.6.0 toolchain.

## Documentation and contributions

[Documentation](docs/INDEX.md) · [CI and releases](docs/CI.md) · [Build](docs/BUILD.md) · [Development](docs/DEVELOPMENT.md) · [Testing](docs/TESTING.md) · [Contributing](CONTRIBUTING.md)

English documentation is authoritative; Russian documents are translations. Preserve license notices when reusing the port. Original project code and contributions are GPL-3.0-only; third-party components retain their own licenses. See [licensing](docs/LICENSING.md) and the root [LICENSE](LICENSE).
