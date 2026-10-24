Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## Current development builds

All 17 profiles and 19 variants pass from frozen source `39b6e22`. The
[final matrix](../audits/rc6/runtime-stack-20261024/final/README.md) records
exact identities, all checks and the raw build for each row.

| Build | CODE bytes | Main / low trailing free | XRAM | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| `standard` | 38,077 | 2,339 / 84 | 2,589 | 161 / 162 | 1 |
| `nkro` | 38,216 | 2,200 / 84 | 2,594 | 161 / 162 | 1 |
| `one-shot` | 38,670 | 1,814 / 16 | 2,599 | 160 / 162 | 2 |
| `nkro-one-shot` | 38,809 | 1,675 / 16 | 2,604 | 160 / 162 | 2 |
| `space-cadet` | 38,193 | 2,223 / 84 | 2,592 | 161 / 166 | 5 |
| `nkro-space-cadet` | 38,332 | 2,084 / 84 | 2,597 | 161 / 166 | 5 |
| `one-shot-space-cadet` | 38,785 | 1,699 / 16 | 2,602 | 160 / 166 | 6 |
| `full` | 38,924 | 1,560 / 16 | 2,607 | 160 / 166 | 6 |
| `full-gui-lock` | 39,159 | 1,325 / 16 | 2,610 | 164 / 166 | 2 |
| `full-ctrl-gui` | 39,302 | 1,182 / 16 | 2,610 | 164 / 166 | 2 |
| `full-dynamic-macro-gui` | 40,279 | 205 / 16 | 2,696 | 164 / 165 | 1 |
| `full-mouse-auto-shift-gui --short-calls` | 40,391 | 93 / 16 | 2,657 | 164 / 166 | 2 |
| `full-auto-shift-dynamic-macro --short-calls` | 40,424 | 60 / 16 | 2,710 | 160 / 165 | 5 |
| `full-dynamic-macro` | 40,044 | 440 / 16 | 2,693 | 160 / 165 | 5 |
| `full-mouse` | 39,774 | 710 / 16 | 2,637 | 160 / 166 | 6 |
| `full-auto-shift` | 39,537 | 947 / 16 | 2,624 | 160 / 166 | 6 |
| `full-mouse-auto-shift` | 40,387 | 97 / 16 | 2,654 | 160 / 166 | 6 |
| `full --short-calls` | 38,676 | 1,808 / 16 | 2,607 | 160 / 166 | 6 |
| `full-mouse-auto-shift --short-calls` | 40,168 | 316 / 16 | 2,654 | 160 / 166 | 6 |

Every stack bound includes the persistent CRT frame and all three distinct IRQ
sources. The minimum margin is one byte. A changed image must pass the complete
bound again; a measured CPU peak alone is insufficient. The figures assume the
[documented runtime premises](RUNTIME-STACK.md).

XRAM capacity is 3072 bytes, separate from 512 fixed DMA bytes. The CODE windows
are separate; low trailing space cannot be added to main.
`full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require
`--short-calls`. Mouse Keys + Auto Shift + Dynamic Macros remains unsupported:
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
