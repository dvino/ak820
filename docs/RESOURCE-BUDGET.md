Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The active profile has six layers. Four layers are an analysis option, not an
installed configuration or a silent change to the current profile.

The controlled comparisons below use the pre-layout RC6 image `12260272…e114`.
The final layout adds 20 CODE bytes; current totals are in [status](STATUS.md).
Later erase-path and local optimization changes are separate from this old
comparison. The status page distinguishes their source and built images.

## Four versus six layers

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
