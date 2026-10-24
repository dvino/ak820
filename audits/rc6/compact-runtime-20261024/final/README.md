# Frozen development matrix

All 16 named profiles passed in 18 build variants from clean commit
`55acbb0f7977d4c7840d49143e9b40a15b1dc3c8`. Each image passed 28 base suites,
273 base unit tests with zero skips, and its 14–24 selected supplemental
suites. Source and test inputs were frozen throughout. No device was opened.

| Build | CODE bytes | Main / low trailing free | XRAM | Stack capacity |
| --- | ---: | ---: | ---: | ---: |
| `standard` | 38,117 | 2,299 / 84 | 2,589 | 162 |
| `nkro` | 38,256 | 2,160 / 84 | 2,594 | 162 |
| `one-shot` | 38,710 | 1,774 / 16 | 2,599 | 162 |
| `nkro-one-shot` | 38,849 | 1,635 / 16 | 2,604 | 162 |
| `space-cadet` | 38,233 | 2,183 / 84 | 2,592 | 166 |
| `nkro-space-cadet` | 38,372 | 2,044 / 84 | 2,597 | 166 |
| `one-shot-space-cadet` | 38,825 | 1,659 / 16 | 2,602 | 166 |
| `full` | 38,964 | 1,520 / 16 | 2,607 | 166 |
| `full --short-calls` | 38,717 | 1,767 / 16 | 2,607 | 166 |
| `full-gui-lock` | 39,199 | 1,285 / 16 | 2,610 | 166 |
| `full-dynamic-macro-gui` | 40,319 | 165 / 16 | 2,696 | 165 |
| `full-mouse-auto-shift-gui --short-calls` | 40,432 | 52 / 16 | 2,657 | 166 |
| `full-auto-shift-dynamic-macro --short-calls` | 40,466 | 18 / 16 | 2,710 | 165 |
| `full-dynamic-macro` | 40,084 | 400 / 16 | 2,693 | 165 |
| `full-mouse` | 39,814 | 670 / 16 | 2,637 | 166 |
| `full-auto-shift` | 39,577 | 907 / 16 | 2,624 | 166 |
| `full-mouse-auto-shift` | 40,427 | 57 / 16 | 2,654 | 166 |
| `full-mouse-auto-shift --short-calls` | 40,203 | 281 / 16 | 2,654 | 166 |

Each directory contains exact IHX, MAP and MEM, build/configuration reports,
base and supplemental results, partial stack analysis, and the complete raw
build with simulator commands and logs in `raw-build.tar.xz`. Its SHA256 is
recorded in `record.json`; all records are combined in [matrix.json](matrix.json).
Absolute scratch paths inside reports preserve provenance. Reproduction uses
fresh directories and generates fresh path-bound reports.

Both CODE windows remain separate. XRAM capacity is 3072 bytes, with another 512
bytes reserved for DMA. Stack capacity is allocated space, not a proven runtime
bound. `_main` remains unresolved in exact-image analysis, so no image has a
whole-program stack/IRQ qualification. All images remain development-only.
The [package-gate result](package-gate.json) confirms that the changed `full`
image is rejected by the existing exact-source release policy.
