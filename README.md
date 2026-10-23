Русский перевод: [README на русском](docs/ru/README.md).

# QMK and Vial for AJAZZ AK820

This project brings QMK and Vial to the **wired AJAZZ AK820 with a VS11K28A / CH555-like 8051 controller**, USB `320F:505B`. AK820 V2, Pro and Max use different hardware and are not supported.

Set up keys, layers, the encoder and macros in Vial. After that, the keyboard works without a desktop app running in the background. The port keeps the keyboard's original loader and stores settings in the keyboard.

## Features

- Six layers, with separate clockwise and counterclockwise encoder actions on each layer.
- Standard keys, modifiers, media and system controls, plus NKRO (sending more than six keys at once).
- Sixteen macro slots with 8192 bytes of shared storage.
- Caps Word, Repeat, Alt Repeat, Grave Escape and Tri Layer.
- 82 RGB LEDs with solid color, breathing, color cycles, VialRGB Direct and a fade on the pressed key.
- Persistent keymaps, macros and global lighting; physical Vial unlock.
- A source installer for supported firmware updates. Tap-hold, One Shot, Mouse Keys, Tap Dance, Combos and Key Overrides are not supported by this profile.

## Get started

Start with the [installation and recovery guide](docs/INSTALL.md) before using the installer.

For the source installer, Python 3.10+ is required. Verify the complete bundle offline:

```sh
# Linux
./AK820.sh verify
```

```powershell
# Windows
.\AK820.cmd verify
```

Use [Configuration](docs/CONFIGURATION.md) to remap keys, layers, macros and lighting in Vial. Firmware builds use Linux/WSL, Python 3.11+ and the pinned SDCC 4.6.0 toolchain.

## Documentation and contributions

[Documentation](docs/INDEX.md) · [Build](docs/BUILD.md) · [Development](docs/DEVELOPMENT.md) · [Testing](docs/TESTING.md) · [Contributing](CONTRIBUTING.md)

English documentation is authoritative; Russian documents are translations. Preserve license notices when reusing the port. Original project code and contributions are GPL-3.0-only; third-party components retain their own licenses. See [licensing](docs/LICENSING.md) and the root [LICENSE](LICENSE).
