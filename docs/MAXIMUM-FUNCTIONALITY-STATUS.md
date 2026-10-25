# Whole-program compression

The target remains one `maximal` image with all 14 optional modules and every
base function. Feature counts and storage limits remain fixed by the
[plan](MAXIMUM-FUNCTIONALITY-PLAN.md).

## Current image: 27

`.build/resume27-classifier` uses **44,699 occupied CODE bytes**. Main CODE
still overflows by **4,346 bytes**. This is an oversized diagnostic image;
it is not installable. The physical CODE windows remain `[0x28a0,0x3000)` and
`[0x3027,0xc700)`. Loader, NVM, macro storage and LED DMA reservations remain.

| Measurement | Current value |
| --- | ---: |
| Low / main occupied CODE | 1,741 / 42,958 bytes |
| Highest main address | `0xd7f9` |
| Ordinary XRAM + flash stage | 2,943 + 64 = 3,007 / 3,072 bytes |
| Stack capacity | 167 bytes |
| Main / USB / timer / LED bounds | 103 / 5 / 2 / 2 bytes |
| Unresolved paths from those roots | 0 |
| Conditional total / margin | 165 / 2 bytes |

The conditional total is `103 + 2 + 3 × 17 + 5 + 2 + 2`. It includes CRT
main entry and all distinct IRQ sources. Bank, OEM wrapper, routing and
non-reentry assumptions remain open; this fit does not qualify the firmware.

IHX SHA256: `96b7e63eba3e30b2d598b0f52e19b23c7a07ff5363194f87d565d359ab5da7f3`.
The [machine ledger](maximal-current.json) and [pass 27 evidence](../audits/maximal-pass27-20261025/README.md)
bind measurements to source, toolchain, images and reviewed contexts.

## Change and checks

The USB raw-command classifier now uses bounded direct tests in place of
nested switches. Allowed commands, setter rejection, packet handling and
persistent formats remain unchanged. All 16,777,216 three-byte prefixes agree
with the retained switch oracle; both admission mutants are rejected.

Baseline 26b was reproduced byte for byte from its recorded inputs. Its IHX
is `47400365dfe8e7e56fd46a548938ca8c9024467ca13120f506cb7213e9f7ef10`.
The new maximal image saves **48 linked CODE bytes**, with no XRAM or stack
capacity change. Differing historical baseline source is checked against Git
`cfd05a0`; it is not presented as current source. Previous continuation evidence
remains [historical](../audits/maximal-continuation-20261025/README.md).

Fresh linked stack, CRT and finite reader checks pass for the exact image.
The bounded CPU suite passes 629 RGB setter cases, 576 Combo GET cases,
48 cache-only updater cases, 15 distinct-source IRQ orders and 256 LED
selectors. All 4,346 occupied bytes at or above `0xc700` remain unchanged in
20 sessions. CRT executes only to main entry. Main-loop and NVM/settings
initialization, physical flash operations and the full configured regressions
are outside these checks.

The current-source `work` control uses 37,470 CODE and 2,554 physical XRAM
bytes: 75 fewer CODE bytes than the archived work control. Its highest address
is `0xbbbc`, leaving 2,883 trailing main-window bytes. Main/USB/timer/LED bounds
are 98/5/2/2; the conditional total is 160 of 171 stack bytes, leaving 11.
Its fresh bounded IRQ CPU check passes all 15 orders and 256 selectors with
all occupied CODE unchanged. It is a control build, not a replacement release.

Both NVM assembly kernels and the existing compiler reductions remain enabled;
IRAM overlay remains off. The next gates are further CODE reduction, complete
OEM startup/IRQ and bank contracts, the opaque writer, full configured
regressions and physical validation. The complete-feature objective remains
open. No device writes, packaging, installer or release changes were made.
