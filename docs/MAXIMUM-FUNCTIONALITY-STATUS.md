Русский перевод: [Сжатие полной прошивки](ru/MAXIMUM-FUNCTIONALITY-STATUS.md).

# Whole-program compression

The target remains one `maximal` image with all 14 optional modules and every
base function. Feature counts and storage limits remain fixed by the
[plan](MAXIMUM-FUNCTIONALITY-PLAN.md).

## Current image: 28

`.build/resume28-keymap-firewall` uses **44,638 occupied CODE bytes**. Main CODE
still overflows by **4,285 bytes**. This diagnostic image is not installable.
The physical CODE windows remain `[0x28a0,0x3000)` and `[0x3027,0xc700)`.
Loader, NVM, macro storage and LED DMA reservations remain.

| Measurement | Current value |
| --- | ---: |
| Low / main occupied CODE | 1,741 / 42,897 bytes |
| Highest main address | `0xd7bc` |
| Ordinary XRAM + flash stage | 2,943 + 64 = 3,007 / 3,072 bytes |
| Stack capacity | 167 bytes |
| Main / USB / timer / LED bounds | 103 / 5 / 2 / 2 bytes |
| Unresolved paths from those roots | 0 |
| Conditional total / margin | 165 / 2 bytes |

The conditional total is `103 + 2 + 3 × 17 + 5 + 2 + 2`. It includes CRT
main entry and all distinct IRQ sources. Bank, OEM wrapper, routing and
non-reentry assumptions remain open; this fit does not qualify the firmware.

IHX SHA256: `87467a0fdae46f4e222de6968b6e1cb48d155bfca77f81363acb947a37e17d1b`.
The [machine ledger](maximal-current.json) and [pass 28 evidence](../audits/maximal-pass28-20261025/README.md)
bind measurements to source, toolchain, images and bounded checks.

## Change and checks

The keymap buffer setter scans affected keycode pairs directly when checking
locked boot-key writes, including partial pairs. It preserves read order,
rejection before writing, accepted data and persistent formats. The maximal
image saves **61 linked CODE bytes** against retained pass 27, with unchanged
XRAM and stack capacity. Its differing historical `dynamic_keymap.c` is checked
against the full recorded Git commit; the other inputs are checked in place.
The [pass 27 evidence](../audits/maximal-pass27-20261025/README.md) remains unchanged.

The host differential suite passes 6,849,504 cases with ASan/UBSan and rejects
three mutants and alias drift. Its read-fault mock returns `0xff` and sets a
sticky flag; it does not model write faults or durable backend behavior.
The exact linked setter passes 600 CPU cases covering partial boundaries,
unchanged cache writes, lock and cache flags, and 88 early rejections. All
44,638 occupied CODE bytes remain unchanged. These calls use one cache page;
new read faults, dirty cross-page transitions, flash effects and IRQs are
outside this setter check.

Actual-image stack, CRT and finite reader checks pass. The pass 27 context
certificates and their reviews are retained byte for byte. Their protected
compiler ASM, tools, map and provenance are revalidated, and the actual pass 28
postlink bindings are checked again; no new context certificate is claimed.
The other bounded CPU checks pass 629 RGB setter cases, 576 Combo GET cases,
48 cache-only updater cases, 15 distinct-source IRQ orders and 256 LED selectors.
All 4,285 occupied bytes at or above `0xc700` remain unchanged in 20 sessions.
CRT executes only to main entry; main-loop and NVM/settings initialization
remain outside these checks.

The current-source `work` control uses 37,392 CODE and 2,554 physical XRAM
bytes, saving 78 CODE bytes against retained pass 27 work. Its highest address
is `0xbb6e`, leaving 2,961 trailing main-window bytes. Main/USB/timer/LED bounds
are 98/5/2/2; the conditional total is 160 of 171 stack bytes, leaving 11.
Its bounded IRQ CPU check preserves all occupied CODE in 17 sessions. This
control build does not replace the released image.

Both NVM assembly kernels and existing compiler reductions remain enabled;
IRAM overlay remains off. Further CODE reduction, complete OEM startup/IRQ
and bank contracts, the opaque writer, full configured regressions and physical
validation remain open. The complete-feature objective remains open. No device,
installer, packaging or release action was performed.
