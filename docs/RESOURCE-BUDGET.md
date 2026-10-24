Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## Current development builds

All 16 profiles passed 18 build variants from source `55acbb0`. The complete
[matrix](../audits/rc6/compact-runtime-20261024/final/README.md) records exact
hashes, checks and stack allocations for every image.

| Build | CODE bytes | Main / low trailing free | XRAM |
| --- | ---: | ---: | ---: |
| `full` | 38,964 | 1,520 / 16 | 2,607 |
| `full --short-calls` | 38,717 | 1,767 / 16 | 2,607 |
| `full-mouse` | 39,814 | 670 / 16 | 2,637 |
| `full-auto-shift` | 39,577 | 907 / 16 | 2,624 |
| `full-mouse-auto-shift` | 40,427 | 57 / 16 | 2,654 |
| `full-mouse-auto-shift --short-calls` | 40,203 | 281 / 16 | 2,654 |
| `full-gui-lock` | 39,199 | 1,285 / 16 | 2,610 |
| `full-dynamic-macro` | 40,084 | 400 / 16 | 2,693 |
| `full-dynamic-macro-gui` | 40,319 | 165 / 16 | 2,696 |
| `full-mouse-auto-shift-gui --short-calls` | 40,432 | 52 / 16 | 2,657 |
| `full-auto-shift-dynamic-macro --short-calls` | 40,466 | 18 / 16 | 2,710 |

XRAM capacity is 3072 bytes, separate from 512 fixed DMA bytes. These `full`
variants allocate 165–166 stack bytes; that is capacity, not a proven runtime
bound. The CODE windows are separate: low trailing space cannot be added to
main. Mouse Keys + Auto Shift now fits without short transfers.

Adding Dynamic Macros to Mouse Keys + Auto Shift exceeded the main window by 804
bytes even with short transfers; that profile is unsupported.
`full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require
`--short-calls`. Other rows without that suffix are measured without it.
New images remain unqualified for release.

## Historical comparisons

| Resource | published alpha.3 image |
| --- | ---: |
| Main CODE end | `0xc546` |
| CODE windows | `[0x28a0,0x3000)` and `[0x3027,0xc700)` |
| Trailing free bytes | 441 main / 16 low |
| XRAM | 2,637 / 3,072 bytes |
| Initial SP / allocated stack | `0x5d` / 162 bytes |
| Layers / macros / shared macro storage | 6 / 16 / 8,192 bytes |

Allocated stack capacity is not a worst-case runtime bound. Free bytes in the
two CODE windows cannot be exchanged. NVM and macro storage are not executable
CODE.

A historical controlled comparison found that reducing six layers to four
saved zero CODE and zero XRAM, while freeing 520 logical NVM addresses. Those
addresses were not added to macro storage and the encoder base would move,
requiring a schema and migration decision. The project therefore retains six
layers. Details of the old comparison and RGB measurements remain in the dated
[technical study](../audits/rc6/optimization-deep-analysis-20261023.md); they do
not describe the current release image.

The published alpha.3 `full` image was measured as a complete linked image, including
both CODE windows and RAM. Main-path use is 93 stack bytes, CRT use is 2 bytes,
and the three IRQ paths use 61 bytes together. Total use is 156 of 162 bytes,
leaving 6 bytes. These figures apply only to the exact qualified image; they
do not establish behavior on physical hardware.

These stack figures describe the published alpha.3 image only. They do not
apply to development profiles with changed source. See [Build profiles](BUILD-PROFILES.md)
for their feature sets and the [technical report](../audits/rc6/compact-runtime-20261024/README.md)
for current compact-feature measurements and limits.
