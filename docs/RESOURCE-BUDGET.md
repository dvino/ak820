Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed image remains `v0.6.0-alpha.3`. Its identity and
release evidence are in [Status](STATUS.md). Current source is development work.

## Current development profiles

All 24 named profiles and 26 variants pass exact-image foreground, startup and
all enabled interrupt checks. Firmware inputs are frozen at `ac48c65`; the
full-regression fixtures are frozen at `147508e`. Complete identities and
qualification scopes are in the [final matrix](../audits/rc6/module-completion-20261024/final/README.md).

| Build | CODE bytes | Main / low trailing free | XRAM | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| `full` | 38447 | 2037 / 16 | 2555 | 162 / 167 | 5 |
| `full-auto-shift` | 39055 | 1429 / 16 | 2572 | 162 / 166 | 4 |
| `full-auto-shift-dynamic-macro-short` | 39902 | 582 / 16 | 2658 | 162 / 165 | 3 |
| `full-ctrl-gui` | 38745 | 1739 / 16 | 2558 | 162 / 166 | 4 |
| `full-dynamic-macro` | 39500 | 984 / 16 | 2641 | 162 / 165 | 3 |
| `full-dynamic-macro-gui` | 39649 | 835 / 16 | 2644 | 162 / 165 | 3 |
| `full-gui-lock` | 38602 | 1882 / 16 | 2558 | 162 / 166 | 4 |
| `full-key-overrides-short` | 40464 | 20 / 16 | 2734 | 162 / 162 | 0 |
| `full-leader` | 39117 | 1367 / 16 | 2582 | 162 / 163 | 1 |
| `full-mac-pc` | 38654 | 1754 / 92 | 2558 | 162 / 166 | 4 |
| `full-mac-pc-os-indicators` | 39091 | 1317 / 92 | 2567 | 162 / 166 | 4 |
| `full-mouse` | 39297 | 1187 / 16 | 2585 | 162 / 167 | 5 |
| `full-mouse-auto-shift` | 39905 | 579 / 16 | 2602 | 162 / 166 | 4 |
| `full-mouse-auto-shift-gui-short` | 39818 | 666 / 16 | 2605 | 162 / 166 | 4 |
| `full-mouse-auto-shift-short` | 39683 | 801 / 16 | 2602 | 162 / 166 | 4 |
| `full-os-indicators` | 38899 | 1509 / 92 | 2564 | 162 / 167 | 5 |
| `full-qmk-settings-short` | 40075 | 409 / 16 | 2640 | 162 / 166 | 4 |
| `full-short` | 38220 | 2264 / 16 | 2555 | 162 / 167 | 5 |
| `full-tap-dance-short` | 40173 | 311 / 16 | 2795 | 166 / 166 | 0 |
| `nkro` | 37766 | 2650 / 84 | 2542 | 156 / 163 | 7 |
| `nkro-one-shot` | 38327 | 2157 / 16 | 2552 | 162 / 163 | 1 |
| `nkro-space-cadet` | 37878 | 2538 / 84 | 2545 | 156 / 167 | 11 |
| `one-shot` | 38188 | 2296 / 16 | 2547 | 162 / 163 | 1 |
| `one-shot-space-cadet` | 38308 | 2176 / 16 | 2550 | 162 / 167 | 5 |
| `space-cadet` | 37739 | 2677 / 84 | 2540 | 156 / 167 | 11 |
| `standard` | 37627 | 2789 / 84 | 2537 | 156 / 163 | 7 |

A `-short` suffix denotes verified short calls. The three extension profiles,
`full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require that
option. The additional `full-short` and `full-mouse-auto-shift-short` rows show
both forms of those profiles.

The minimum stack margin is zero for Tap Dance and Key Overrides. Their
bounds include the persistent CRT frame and all three distinct IRQ sources.
Every changed image must pass again; a peak observed in CPU tests is not an
upper bound. See [runtime premises](RUNTIME-STACK.md). The previous measurements
at `1187d4c` remain in their [technical matrix](../audits/rc6/web-firmware-20261024/runtime-all/README.md).

XRAM capacity is 3072 bytes, separate from 512 fixed DMA bytes. CODE windows
are separate; low trailing space cannot be added to main. No all-extension
profile or Mouse Keys + Auto Shift + Dynamic Macros combination is offered.
New development images have no release approval.

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
for the accepted compact-feature baseline measurements and limits.

## Fixed Vial callbacks

The AK820 SDCC target uses the empty default keyboard/user record callbacks.
Their calls, argument copies and unused post-processing lookup are omitted.
Other targets and native host fixtures retain their callback paths. Adding a
custom callback requires enabling that path deliberately and repeating whole-image
CODE, stack and regression checks; the SDCC port does not provide weak overrides.
