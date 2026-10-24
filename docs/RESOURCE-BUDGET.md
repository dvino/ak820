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

Any future feature or profile must be measured in a complete linked build,
including both CODE windows, XRAM and stack. Probe savings are non-additive.
Final development profile measurements and exact image hashes are recorded in
the [qualification report](../audits/rc6/configurable-20261024/qualification.md).
The standard profile saves 499 CODE bytes and nine XRAM bytes against alpha.2,
with 602 trailing main bytes, 84 low bytes and 160 allocated stack bytes.
No profile has a proven
whole-program stack bound or exact-image interrupt/nesting proof, so allocated
stack capacity remains a placement result, not a qualified runtime allowance.
The published alpha.2 image and its numbers above are unchanged. See
[Build profiles](BUILD-PROFILES.md) for the development options and restrictions.
