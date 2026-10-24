Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image is `v0.6.0-alpha.3`. Its exact identity and
release evidence are recorded in [Status](STATUS.md). All current development
profiles have source changes beyond that image and are not release-qualified.

## New Mac/PC and OS profiles

The configurator now lists 21 named profiles. Clean-source measurements for `full`
and the three new module combinations remain pending; their scope is in the
[new matrix](../audits/rc6/web-firmware-20261024/final/README.md).
Other profiles retain the accepted measurements below at their frozen source;
those measurements do not qualify changed source.

## Accepted Leader baseline

All 18 profiles and 20 variants pass from frozen source `d04290b`. The
[final matrix](../audits/rc6/leader-next-20261024/final/README.md) records
exact identities, all checks and the raw build for each row.

| Build | CODE bytes | Main / low trailing free | XRAM | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| `standard` | 38,044 | 2,372 / 84 | 2,582 | 161 / 162 | 1 |
| `nkro` | 38,183 | 2,233 / 84 | 2,587 | 161 / 162 | 1 |
| `one-shot` | 38,637 | 1,847 / 16 | 2,592 | 160 / 162 | 2 |
| `nkro-one-shot` | 38,776 | 1,708 / 16 | 2,597 | 160 / 162 | 2 |
| `space-cadet` | 38,159 | 2,257 / 84 | 2,585 | 161 / 166 | 5 |
| `nkro-space-cadet` | 38,298 | 2,118 / 84 | 2,590 | 161 / 166 | 5 |
| `one-shot-space-cadet` | 38,751 | 1,733 / 16 | 2,595 | 160 / 166 | 6 |
| `full` | 38,890 | 1,594 / 16 | 2,600 | 160 / 166 | 6 |
| `full-leader` | 39,606 | 878 / 16 | 2,627 | 160 / 162 | 2 |
| `full-gui-lock` | 39,125 | 1,359 / 16 | 2,603 | 164 / 166 | 2 |
| `full-ctrl-gui` | 39,268 | 1,216 / 16 | 2,603 | 164 / 166 | 2 |
| `full-dynamic-macro-gui` | 40,247 | 237 / 16 | 2,689 | 164 / 165 | 1 |
| `full-mouse-auto-shift-gui --short-calls` | 40,359 | 125 / 16 | 2,650 | 164 / 166 | 2 |
| `full-auto-shift-dynamic-macro --short-calls` | 40,391 | 93 / 16 | 2,703 | 160 / 165 | 5 |
| `full-dynamic-macro` | 40,012 | 472 / 16 | 2,686 | 160 / 165 | 5 |
| `full-mouse` | 39,740 | 744 / 16 | 2,630 | 160 / 166 | 6 |
| `full-auto-shift` | 39,503 | 981 / 16 | 2,617 | 160 / 166 | 6 |
| `full-mouse-auto-shift` | 40,353 | 131 / 16 | 2,647 | 160 / 166 | 6 |
| `full --short-calls` | 38,643 | 1,841 / 16 | 2,600 | 160 / 166 | 6 |
| `full-mouse-auto-shift --short-calls` | 40,132 | 352 / 16 | 2,647 | 160 / 166 | 6 |

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
for their feature sets and the [technical report](../audits/rc6/leader-next-20261024/README.md)
for current compact-feature measurements and limits.
