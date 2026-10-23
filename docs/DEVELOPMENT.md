Русский перевод: [Разработка](ru/DEVELOPMENT.md).

# Development

The active port is `qmk-8051-ak820/keyboards/ajazz/ak820/`; its selected keymap
is `keymaps/vial`. The QMK-based tree is trimmed to the maintained AK820 port and required shared code.
Only code reachable by the selected target belongs to the current runtime.

| Area | Location |
| --- | --- |
| Matrix, encoder and OEM hardware glue | `ak820_board.c`, `matrix.c` |
| Startup, flash and settings journal | `ak820_startup.c`, `ak820_flash.c`, `ak820_nvm.c` |
| Macros and RGB | `ak820_macro.c`, `ak820_rgb.c` |
| USB implementation | Follow the active build report for this port's linked USB units; other upstream backends are not active |
| Build, packing, loader tools | `qmk-8051-ak820/util/` |
| Installer and its tests | `tools/installer/` |
| Runtime and CPU regressions | `qmk-8051-ak820/tests/ak820_*` |

Read `AGENTS.md` before edits. Update documentation alongside behavior, command,
format or limit changes. English documents are canonical; update the Russian
translation in the same change. Regenerate affected machine reports and check
their sizes, SHA256, versions and addresses against actual artifacts.

Preserve bootloader and protected ROM boundaries. Do not replace explicit
consent, provenance checks or recovery data with a force option. Do not run
device commands during offline tests. Ask the owner before a hardware flash.

Before proposing a change, run the relevant host tests, build the target and
run linked CPU tests for affected startup/ABI/runtime paths. Document skipped
conditions. Obtain independent review of code, documents and verification
evidence; fix disagreements before committing. Test success at one level does
not establish another level.

For contributions, describe the concrete problem, resulting behavior, test
commands and remaining hardware limitations. Include no personal ROM dumps or
user captures. Source licensing is recorded in [LICENSE](../LICENSE) and
[QMK LICENSE](../qmk-8051-ak820/LICENSE); upstream files keep their original notices.
