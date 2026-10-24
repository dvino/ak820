Русский перевод: [О проекте и документация](../../../../docs/ru/README.md).

# AJAZZ AK820 / VS11K28A

QMK/Vial port for the wired AJAZZ AK820, USB `320F:505B`. V2, Pro and Max
are different hardware. The selected keymap is `vial`.

Use the repository's [README](../../../../README.md),
[build guide](../../../../docs/BUILD.md),
[configuration guide](../../../../docs/CONFIGURATION.md) and
[current status](../../../../docs/STATUS.md).

This directory contains active matrix, hardware, RGB, NVM and startup sources.
Do not flash a linked IHX directly: the packer preserves OEM loader/tail
boundaries and generates a personal update/recovery session. Device writes
require explicit owner confirmation.
