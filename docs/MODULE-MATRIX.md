Русский перевод: [Матрица модулей](ru/MODULE-MATRIX.md).

# Module matrix

The firmware is modular because all implemented functions do not fit in controller memory at once. Ten fixed profiles exchange selected `main` features for others. Every profile includes QMK Settings.

[Choose a profile](profiles/README.md). [Feature limits](FEATURES.md). [Qualification and release state](STATUS.md).

| Module | `main` | `game` | `mmo` | `typing` | `code` | `pointer` | `onehand` | `creative` | `shortcuts` | `multios` |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| auto-shift | — | — | — | ✓ | — | — | — | — | — | — |
| ctrl-gui-swap | — | — | — | — | — | — | — | — | — | ✓ |
| dynamic-macros | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| grave-escape | — | — | — | — | ✓ | — | — | — | — | — |
| gui-lock | — | ✓ | ✓ | — | — | — | — | — | — | — |
| key-overrides | ✓ | ✓ | — | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| leader | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| mac-pc | — | — | — | — | — | — | — | — | — | ✓ |
| mouse-keys | — | — | — | — | — | ✓ | ✓ | — | — | — |
| nkro | — | ✓ | ✓ | — | — | — | — | — | — | — |
| nkro-control | — | ✓ | ✓ | — | — | — | — | — | — | — |
| one-shot | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| os-indicators | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| qmk-settings | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| space-cadet | — | — | — | ✓ | ✓ | — | — | — | — | — |
| tap-dance | — | — | ✓ | — | — | — | ✓ | ✓ | ✓ | — |
| vialrgb-direct | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — |

Every profile also includes six layers, 16 persistent Vial macros with a shared 8192-byte buffer, eight two-key Combos, Mod-Tap/Layer-Tap, encoder mapping, media keys, Caps Word, Repeat/Alt Repeat, Tri Layer and built-in RGB effects. Without Direct, global mode, color, brightness and speed remain available; per-LED host frames require Direct.

Module sizes are not additive: each complete image is checked after all optimizations. Previous measurements of the nine-profile catalog do not apply to these compositions. Status records exact release sizes and proof.
