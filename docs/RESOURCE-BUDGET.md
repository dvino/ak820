Русский перевод: [Память и число слоёв](ru/RESOURCE-BUDGET.md).

# Memory and layer count

The released and installed `v0.6.0-alpha.2` application uses 40,313 CODE bytes
(38,492 main and 1,821 low), 2,621 XRAM bytes and 160 bytes of allocated stack
capacity. It leaves 120 bytes in the main CODE window and 67 in the low window.
The image hash and source are in [Status](STATUS.md).

| Resource | alpha.2 |
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

Every development profile is measured as a complete linked image, including
both CODE windows, XRAM, internal RAM and allocated stack capacity. The exact
profile measurements and image identities are in the dated
[qualification evidence](../audits/rc6/roadmap-max-20261024/final/README.md).
Probe savings are non-additive and cannot predict another combination.

Allocated stack capacity is a placement result, not a whole-program runtime
bound. Exact-image interrupt and nesting safety also remain unqualified, so no
configured profile is approved for installation or release. The published
alpha.2 image and its figures above are unchanged. See [Build profiles](BUILD-PROFILES.md)
for the eight development options and their limits.
