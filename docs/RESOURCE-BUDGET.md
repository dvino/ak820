Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The published and installed `v0.6.0-alpha.2` image remains unchanged. The
alpha.3 `full` candidate uses 40,043 CODE bytes and is source-qualified; it has
not been published or installed. See [Status](STATUS.md) for exact image identity.

| Resource | alpha.2 published |
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

The alpha.3 full candidate is measured as a complete linked image, including
both CODE windows and RAM. Main-path use is 93 stack bytes, CRT use is 2 bytes,
and the three IRQ paths use 61 bytes together. Total use is 156 of 162 bytes,
leaving 6 bytes. These figures apply only to the exact qualified image; they
do not establish behavior on physical hardware.

The published alpha.2 image and its figures above are unchanged. The full
candidate has source proof and independent policy review, but publication waits
for native CI. No device behavior is claimed. See [Build profiles](BUILD-PROFILES.md)
for the eight options and their limits.
