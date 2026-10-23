Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The current profile keeps six layers, sixteen macros and 8192 bytes of shared macro storage. Four layers remain a controlled comparison, not a release setting. The private XDATA journal-header pointer is in source; its offline build is a development candidate and has not been promoted or installed. The exact settings-backup pin remains the stable release image.

## Current measured builds

The current source candidate is `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`. The stable release image remains `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.

| Image | CODE total | Main CODE window | Low CODE window | XRAM | Initial SP / allocated stack capacity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Source candidate | 38,069 (36,261 main + 1,808 low) | 36,261 / 38,617 occupied; 2,356 addresses without IHX data | 1,808 / 1,888 occupied; 80 addresses without IHX data | 2,066 / 3,072 occupied; 1,006 free | 0x62 / 157 bytes |
| Stable release | 38,100 (36,292 main + 1,808 low) | 36,292 / 38,617 occupied; 2,325 addresses without IHX data | 1,808 / 1,888 occupied; 80 addresses without IHX data | 2,067 / 3,072 occupied; 1,005 free | 0x62 / 157 bytes |

Window unoccupied counts are address counts, not a guarantee of usable contiguous space. Five addresses, `0x302a..0x302e`, remain reserved in HOME and are included in the unoccupied main-window count; they are not free CODE. Stack capacity is the linker allocation limit, not proof that every runtime path uses at most that many bytes. The pointer change saves 31 CODE bytes and one XRAM byte versus the stable image. The rejected delay-expression probe added three CODE bytes and is not adopted. The build and bounded offline review are recorded in the [review](../audits/rc6/bounded-optimization-20261023.md) and [JSON report](../audits/rc6/bounded-optimization-20261023.json); retained evidence is in [its evidence directory](../audits/rc6/bounded-evidence-20261023/). The candidate has not been installed or promoted. See [Status](STATUS.md) for qualification state.

## Four versus six layers

This controlled comparison uses the pre-layout RC6 baseline `12260272…e114`.
It is separate from the current builds in the table above.

Each matrix layer uses `16 × 8 × 2 = 256` bytes in emulated EEPROM. Each encoder
layer uses `1 × 2 × 2 = 4` bytes. Removing two layers therefore frees **520 bytes
of logical NVM addresses**. The macro base remains fixed at `0x800`; the NVM
region remains `0x2800` bytes and the page cache remains 64 bytes. Without a new
layout, those 520 bytes become a larger unused gap, not extra CODE or macros.

The compiled default keymap and encoder map already contain only two layers.
Changing six to four does not remove two compiled default tables. Layer state
already uses eight bits. An isolated four-layer build measured **39,262 CODE
bytes and 2,071 XRAM bytes**, exactly the same as six layers: **zero saving**
in either resource. Only the logical NVM gap changes.

The encoder EEPROM base would move from `0x640` to `0x440`. Keeping the old
schema ID with that change would interpret layer-4 keymap bytes as encoder
assignments. A four-layer release needs explicit migration and a schema change,
or a deliberate fixed-address compatibility design. Tri Layer still fits
layers 0–3, but existing assignments to layers 4/5 need a migration policy.

Recommendation: retain six layers for this release. A significant space gain
requires redesigning storage or reducing a genuinely large runtime feature;
removing two layers alone does not provide that gain.

## RGB precision

The full-versus-compact CIE comparison below also uses the pre-layout RC6
baseline `12260272…e114`; it is a historical controlled comparison, separate
from the current builds above.

Masking color bytes without changing representation does not save space.
The candidate compact CIE curve replaces 256 entries with 32 and keeps wire
and EEPROM HSV values unchanged. Its gross table saving is 224 CODE bytes;
the linked control measured **216 CODE bytes saved** (39,478 full CIE versus
39,262 compact, identical runtime features). Across the renderer's value range
0–160, the tested maximum channel deviation is 8/255, with values 0, 80 and
160 exact. Per-key fade adds 82 age bytes plus a 2-byte timestamp in RAM.

Packing Direct HSV into two bytes could save 82 RAM bytes but adds conversion
code and color loss. That option has not been enabled.

The local Breathing change interpolates between the same 32 table entries once
per frame. It adds no new curve table and leaves the other effects' conversion
unchanged. All 161 supported curve inputs have at most one unit of error against
the full curve in the CPU model. Host tests at brightness 160 show 69 output
levels instead of 20 and a maximum step of 2 instead of 8 at phase step 1.
These are offline results, not a visible-smoothness or hardware-timing test.
