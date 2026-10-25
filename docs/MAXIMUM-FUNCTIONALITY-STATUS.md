Русский перевод: [Сжатие полной прошивки](ru/MAXIMUM-FUNCTIONALITY-STATUS.md).

# Whole-program compression

The target remains one `maximal` image with all 14 optional modules and every
base function. Feature counts and storage limits remain fixed by the
[plan](MAXIMUM-FUNCTIONALITY-PLAN.md).

## Current image: 29

`.build/resume29-getter-bounds` uses **44,601 occupied CODE bytes**. Main CODE
still overflows by **4,248 bytes**. This diagnostic image is not installable.
The physical CODE windows remain `[0x28a0,0x3000)` and `[0x3027,0xc700)`.
Loader, NVM, macro storage and LED DMA reservations remain.

| Measurement | Current value |
| --- | ---: |
| Low / main occupied CODE | 1,741 / 42,860 bytes |
| Highest main address | `0xd797` |
| Ordinary XRAM + flash stage | 2,943 + 64 = 3,007 / 3,072 bytes |
| Stack capacity | 167 bytes |
| Main / USB / timer / LED bounds | 103 / 5 / 2 / 2 bytes |
| Unresolved paths from those roots | 0 |
| Conditional total / margin | 165 / 2 bytes |

The conditional total is `103 + 2 + 3 × 17 + 5 + 2 + 2`. It includes CRT
main entry and all distinct IRQ sources. Bank, OEM wrapper, routing and
non-reentry assumptions remain open; this fit does not qualify the firmware.

IHX SHA256: `693fdcd928f2d84b32e19b858cdd6cce29b46d01ea5694403788da08bf3969f9`.
The [machine ledger](maximal-current.json) and [pass 29 evidence](../audits/maximal-pass29-20261025/README.md)
bind measurements to source, toolchain, images and bounded checks.

## Change and checks

The two location getters forward AK820 calls directly to the existing keymap
and encoder readers. Those readers already check the bounds. Other boards
keep the wrapper checks. The maximal image saves **37 linked CODE bytes**
against retained pass 28, with unchanged XRAM and stack capacity. Only the
historical `dynamic_keymap.c` differs; it is checked against the full recorded
Git commit. Other dependencies are checked in place. The
[pass 28 evidence](../audits/maximal-pass28-20261025/README.md) remains unchanged.

The host differential suite passes 134,217,728 comparisons across four
variants: AK820 generic C, translated current AK820 assembly, non-AK820 C and
an alternate generic geometry. All byte inputs, return values, EEPROM read
counts and ordered addresses are compared. Three mutants are rejected.
ASan/UBSan additionally passes the 33,554,432-case AK820 generic variant.
Translated assembly on the host is distinct from target CPU execution.

The exact linked getters pass 2,431 CPU cases, including every valid matrix
location, every direction byte for each valid encoder layer and invalid
boundaries. Reads, returns, cache state, stack and canaries are checked; all
44,601 occupied CODE bytes remain unchanged. The calls use one primed cache
page at a time. New read faults, dirty cross-page transitions, flash effects
and IRQs are outside this getter check. The historical pass 28 setter check
is retained evidence for that image; it is not a fresh pass 29 setter test.

Actual-image stack, CRT and finite reader checks pass. The pass 27 context
certificates and reviews remain byte-identical; protected compiler ASM, tools,
map and provenance are revalidated, with fresh pass 29 postlink checks.
Other bounded CPU checks pass 629 RGB setter cases, 576 Combo GET cases,
48 cache-only updater cases, 15 distinct-source IRQ orders and 256 LED selectors.
All 4,248 occupied bytes at or above `0xc700` remain unchanged in 20 sessions.
CRT executes only to main entry; main-loop and NVM/settings initialization
remain outside these checks.

The current-source `work` control uses 37,361 CODE and 2,554 physical XRAM
bytes, saving 31 CODE bytes against retained pass 28 work. Its highest address
is `0xbb4f`, leaving 2,992 trailing main-window bytes. Main/USB/timer/LED bounds
are 98/5/2/2; the conditional total is 160 of 171 stack bytes, leaving 11.
Its bounded IRQ CPU check preserves all occupied CODE in 17 sessions. This
control build does not replace the released image.

Both NVM assembly kernels and existing compiler reductions remain enabled;
IRAM overlay remains off. Further CODE reduction, complete OEM startup/IRQ
and bank contracts, the opaque writer, full configured regressions and physical
validation remain open. The complete-feature objective remains open. No device,
installer, packaging or release action was performed.
