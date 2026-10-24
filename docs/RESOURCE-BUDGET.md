Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published `v0.6.0-alpha.3` image remains unchanged. Its release identity and
installed-device state are recorded in [Status](STATUS.md). Current source has
nine curated profile packages. Their exact feature sets and per-image CODE,
XRAM and stack measurements belong in the [module matrix](MODULE-MATRIX.md);
resource use cannot be estimated by adding the cost of individual modules.
Qualification state for the current source is also in [Status](STATUS.md).

## Published alpha.3 image

| Resource | Published image |
| --- | ---: |
| Main CODE end | `0xc546` |
| CODE windows | `[0x28a0,0x3000)` and `[0x3027,0xc700)` |
| Trailing free bytes | 441 main / 16 low |
| XRAM | 2,637 / 3,072 bytes |
| Initial SP / allocated stack | `0x5d` / 162 bytes |
| Layers / macro slots / shared macro buffer | 6 / 16 / 8,192 bytes |

The published image was measured as a complete linked build across both CODE
windows and RAM. Its main-path stack use is 93 bytes, CRT use is 2 bytes, and
all three IRQ paths use 61 bytes together. Total use is 156 of 162 bytes,
leaving 6 bytes. These figures apply only to the exact published image; they do
not qualify a changed source build or prove physical behavior.

Allocated stack capacity is not a runtime bound. Free bytes in the two CODE
windows cannot be exchanged. XRAM capacity is 3,072 bytes, separate from 512
fixed DMA bytes. NVM and macro storage are not executable CODE.

## Fixed Vial callbacks

The AK820 SDCC target uses the empty default keyboard and user record callbacks.
Their calls, argument copies and unused post-processing lookup are omitted.
Other targets and native host fixtures retain their callback paths. Adding a
custom callback requires enabling that path deliberately and repeating whole-
image CODE, stack and regression checks; this SDCC port does not provide weak
overrides.
