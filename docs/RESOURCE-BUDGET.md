Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## Current development builds

Integrated resource probes preserve the original memory windows and all base
features. Final frozen-profile qualification is pending; the exact probe
artifacts are in the [technical report](../audits/rc6/compact-runtime-20261024/README.md).

| Build | CODE bytes | Main / low trailing free | Allocated XRAM |
| --- | ---: | ---: | ---: |
| Published alpha.3 `full` | 40,043 | 441 / 16 | 2,637 |
| `full-mouse-auto-shift` | 40,427 | 57 / 16 | 2,654 |
| `full-dynamic-macro-gui` | 40,319 | 165 / 16 | 2,696 |
| `full-mouse-auto-shift-gui --short-calls` | 40,432 | 52 / 16 | 2,657 |

XRAM capacity is 3072 bytes, separate from 512 fixed DMA bytes. These images
allocate 165–166 stack bytes; that capacity is not a runtime stack bound.
The Mouse Keys + Auto Shift combination now fits without short transfers.
Adding Dynamic Macros to that combination exceeded the main window by 804
bytes even with short transfers and is not a supported profile. New builds
remain unqualified for release.

## Historical comparisons

| Resource | historical alpha.2 image |
| --- | ---: |
| Main CODE end | `0xc687` |
| CODE windows | `[0x28a0,0x3000)` and `[0x3027,0xc700)` |
| Trailing free bytes | 120 main / 67 low |
| XRAM | 2,621 / 3,072 bytes |
| Initial SP / allocated stack | `0x5f` / 160 bytes |
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
