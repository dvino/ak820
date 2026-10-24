Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## Current development builds

The integrated source has 17 named profiles and 19 planned matrix variants.
The final matrix is being regenerated. Exact identities and evidence are in
the [stack and interrupt report](../audits/rc6/runtime-stack-20261024/README.md).

| Integrated candidate | CODE bytes | XRAM | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: |
| `full` | 38,924 | 2,607 | 160 / 166 | 6 |
| `full-ctrl-gui` | 39,302 | 2,610 | 164 / 166 | 2 |

Stack bounds include the persistent CRT frame and all three distinct IRQ
sources. Every configured build must establish its own complete bound and
fit its linked stack allocation before other regression suites run. A measured
CPU peak alone cannot substitute for that bound.

XRAM capacity is 3072 bytes, separate from 512 fixed DMA bytes. The CODE
windows are separate; low trailing space cannot be added to main.
`full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require
`--short-calls`. Mouse Keys + Auto Shift + Dynamic Macros remains unsupported;
the previous probe exceeded the main window by 804 bytes even with short
transfers. New source images still need independent release qualification.

## Published image

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

The published alpha.3 `full` image was measured as a complete linked image, including
both CODE windows and RAM. Main-path use is 93 stack bytes, CRT use is 2 bytes,
and the three IRQ paths use 61 bytes together. Total use is 156 of 162 bytes,
leaving 6 bytes. These figures apply only to the exact qualified image; they
do not establish behavior on physical hardware.

These stack figures describe the published alpha.3 image only. They do not
apply to development profiles with changed source. See [Build profiles](BUILD-PROFILES.md)
for their feature sets and the [technical report](../audits/rc6/runtime-stack-20261024/README.md)
for current compact-feature measurements and limits.
