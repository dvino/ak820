Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## Current development builds

The 2026-10-24 matrix passes offline checks for all eleven profiles and twelve
build variants. The complete measurements and exact image hashes are in the
[technical report](../audits/rc6/compact-next-20261024/README.md).

| Build | CODE bytes | Main / low trailing free | Allocated XRAM |
| --- | ---: | ---: | ---: |
| Published alpha.3 `full` | 40,043 | 441 / 16 | 2,637 |
| Optimized `full` | 39,145 | 1,339 / 16 | 2,638 |
| Optimized `full --short-calls` | 38,907 | 1,577 / 16 | 2,638 |
| `full-mouse` | 40,029 | 455 / 16 | 2,670 |
| `full-auto-shift` | 39,758 | 726 / 16 | 2,655 |
| `full-mouse-auto-shift --short-calls` | 40,403 | 81 / 16 | 2,687 |

XRAM capacity is 3,072 bytes, separate from the fixed 512-byte DMA reservation.
The current `full` variants allocate 163 stack bytes; their maximum runtime
stack use remains unproved. The new combined profile needs `--short-calls`,
which remains off by default. These figures do not transfer alpha.3 release
approval to changed images.

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
for their feature sets and the [technical report](../audits/rc6/compact-next-20261024/README.md)
for current compact-feature measurements and limits.
