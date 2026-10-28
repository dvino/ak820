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

The firmware provides six editable layers, per-layer encoder actions, 16 saved
Vial macros, eight two-key Combos, media and system keys, Caps Word, Repeat and
Alt Repeat, Tri Layer, Mod-Tap and Layer-Tap, and built-in RGB effects. The **C**
indicator follows Caps Lock or Caps Word; **W** shows an active layer above layer 0.

The current source also supports selectable Caps Word rules, session controls
for Combos, saved Auto Shift and One Shot settings, and a saved macro on tap
with a layer on hold for physical keys. See [Tap and hold](docs/TAP-HOLD.md)
for the new action; packaged release availability is listed in [Status](docs/STATUS.md).
Caps Word can also start by holding both Shift keys, or with a quick double
press of left Shift; the [configuration guide](docs/CONFIGURATION.md#caps-word) describes it.

VialRGB Direct supports coherent palette snapshots and complete-frame updates
through its versioned protocol. Its 82 HSV8 colors remain in RAM. The W indicator
uses a slow pulse while GUI lock is active; another active or default layer above
0 takes priority and lights W steadily. See [Direct](docs/DIRECT.md) and
[indicators](docs/INDICATORS.md).

All functions do not fit in the controller memory at once. Ten modular
[profiles](docs/profiles/README.md) select different sets of functions. The default
`main` adds One Shot, Leader, two temporary macro recordings, eight Key Overrides,
Auto Shift, QMK Settings, host control of the OS indicator and VialRGB Direct.
GUI lock remains in `game` and `mmo`, not `main`. Other profiles provide NKRO,
Tap Dance, Space Cadet, Grave Escape,
Mouse Keys or modifier swaps by exchanging selected modules.

The beta.4 release is published with Python installation scripts for Windows
and Linux x86_64. Standalone GUI installers are not planned. The beta.4.1
catalog update is being prepared so the separate [AK Configurator](https://github.com/dvino/ak-configurator)
can install the exact beta.4 images for an owner-run device test. This catalog
change does not claim hardware validation or authorize settings writes. See
[Status](docs/STATUS.md) for release and hardware limits, and the
[feature catalog](docs/FEATURES.md) for function details.

## Disclaimer

The source code, firmware and tools are provided **“as is”, without warranties**
of any kind. Use, modification, flashing and recovery are performed at the
user's own risk. The user is responsible for checking hardware compatibility,
keeping backups and any resulting damage, an unusable device or loss of data.

To the extent permitted by applicable law, the authors and contributors are
not liable for damage or losses caused by using or being unable to use this
project. See sections 15–17 of the [LICENSE](https://github.com/dvino/ak820/blob/main/LICENSE).

## Get started

> Install only on the supported wired hardware revision. A mismatched image can leave the keyboard unusable; a matching USB ID does not make another revision safe.

Download the Windows or Linux package from [Releases](https://github.com/dvino/ak820/releases), then follow the [installation and recovery guide](docs/INSTALL.md).

Read [Settings backup](docs/SETTINGS-BACKUP.md) for backup, restore and update
instructions.

Use [Configuration](docs/CONFIGURATION.md) to remap keys, layers, macros and lighting in Vial. To build from source, see [Build](https://github.com/dvino/ak820/blob/main/docs/BUILD.md); firmware builds use Linux/WSL, Python 3.11+ and the pinned SDCC 4.6.0 toolchain. Every development profile build requires the [stack and interrupt check](https://github.com/dvino/ak820/blob/main/docs/RUNTIME-STACK.md) before its other regression checks.

## Documentation and contributions

The whole-program development target is described in the [compression plan](https://github.com/dvino/ak820/blob/main/docs/MAXIMUM-FUNCTIONALITY-PLAN.md). Current results and remaining limits are in [compression status](https://github.com/dvino/ak820/blob/main/docs/MAXIMUM-FUNCTIONALITY-STATUS.md).

[Documentation](https://github.com/dvino/ak820/blob/main/docs/INDEX.md) · [AK Configurator](https://github.com/dvino/ak-configurator) · [CI and releases](https://github.com/dvino/ak820/blob/main/docs/CI.md) · [Build](https://github.com/dvino/ak820/blob/main/docs/BUILD.md) · [Development](https://github.com/dvino/ak820/blob/main/docs/DEVELOPMENT.md) · [Testing](https://github.com/dvino/ak820/blob/main/docs/TESTING.md) · [Contributing](https://github.com/dvino/ak820/blob/main/CONTRIBUTING.md)

The companion application is maintained in [AK Configurator](https://github.com/dvino/ak-configurator). The [firmware handoff](https://github.com/dvino/ak820/blob/main/web/docs/FIRMWARE-HANDOFF.md) describes its firmware contracts.

English documentation is authoritative; Russian documents are translations. Preserve license notices when reusing the port. Original project code and contributions are GPL-3.0-only; third-party components retain their own licenses. See [licensing](https://github.com/dvino/ak820/blob/main/docs/LICENSING.md) and the root [LICENSE](https://github.com/dvino/ak820/blob/main/LICENSE).
