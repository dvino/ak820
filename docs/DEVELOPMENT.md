Русский перевод: [Разработка](ru/DEVELOPMENT.md).

# Development

The maintained firmware target is `qmk-8051-ak820/keyboards/ajazz/ak820/`,
using `keymaps/vial`. The QMK tree is trimmed to the AK820 port and required
shared code. The linked report identifies the translation units in each build.

| Area | Source |
| --- | --- |
| Matrix, encoder and OEM hardware glue | `ak820_board.c`, `matrix.c` |
| Startup, flash and settings journal | `ak820_startup.c`, `ak820_flash.c`, `ak820_nvm.c` |
| Macros and RGB | `ak820_macro.c`, `ak820_rgb.c`; C/W outputs in [Indicators](INDICATORS.md) |
| Tap-hold, Repeat and Alt Repeat | `ak820_tapping.c`, `ak820_tapping.h`; behavior in [Tap-hold](TAP-HOLD.md) |
| Two-key Combos | `ak820_combo.c`, `ak820_combo.h`; behavior in [Combos](COMBOS.md) |
| Build and image packing | `qmk-8051-ak820/util/` |
| Installer and installer tests | `tools/installer/` |
| Runtime and CPU regressions | `qmk-8051-ak820/tests/ak820_*` |

Read `AGENTS.md` before editing. Update English and Russian documentation with
changes to behavior, commands, formats, sizes, addresses, APIs or limits. Keep
README and [Status](STATUS.md) current; put future work in [Roadmap](ROADMAP.md).
Regenerate affected machine reports and compare their values with the artifacts.

Every new feature or profile must close exact-image stack and IRQ bounds across
startup, foreground and interrupt paths before other regression suites run. An
unknown bound or overflow fails the build. The [runtime stack guide](RUNTIME-STACK.md)
describes the check and its limits.

Keep source, built application, release package and installed firmware distinct.
Report host/CPU checks, builds and device checks separately. A pass at one level
does not prove another. Do not send device commands during offline checks.
Hardware flashing requires explicit confirmation for each operation.

Before committing, an independent reviewer checks code, documentation and
verification evidence. Resolve disagreements, document closure and repeat
affected checks. Preserve bootloader and protected ROM boundaries, exact-image
checks, consent and recovery data. Do not include private ROM dumps or user
captures.

For source licensing, see [LICENSE](../LICENSE) and [QMK LICENSE](../qmk-8051-ak820/LICENSE).
Upstream files retain their original notices.
