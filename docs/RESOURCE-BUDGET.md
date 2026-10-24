Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published `v0.6.0-alpha.3` release uses the `full` profile. Its linked image
uses 40,043 CODE bytes. See [Status](STATUS.md) for the exact image identity and
device evidence.

| Resource | alpha.3 published |
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

For the published image, the reviewed main-path bound is 93 stack bytes, CRT
use is 2 bytes, and the three IRQ paths use 61 bytes together. Total use is 156
of 162 bytes, leaving 6 bytes. These figures apply only to this linked image.
They do not cover the physical feature cases or power-loss behavior still listed
as untested in [Status](STATUS.md). See [Build profiles](BUILD-PROFILES.md) for
the eight options and their limits.
