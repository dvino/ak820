Русский перевод: [Сжатие полной прошивки](ru/MAXIMUM-FUNCTIONALITY-STATUS.md).

# Whole-program compression

The target remains one `maximal` image with all 14 optional modules and every
base function. Feature counts and storage limits remain fixed by the
[plan](MAXIMUM-FUNCTIONALITY-PLAN.md). The complete-feature objective remains open.

## Current image: 30

`.build/resume30-default-keymap` uses **44,400 occupied CODE bytes**, saving
**201 bytes** against the fresh same-source option-off control. Main CODE
still overflows by **4,047 bytes**. This diagnostic image is not installable.
The physical CODE windows remain `[0x28a0,0x3000)` and `[0x3027,0xc700)`.
Loader, NVM, macro storage and LED DMA reservations remain.

| Measurement | Current value |
| --- | ---: |
| Low / main occupied CODE | 1,741 / 42,659 bytes |
| Highest main address | `0xd6ce` |
| Ordinary XRAM + flash stage | 2,946 + 64 = 3,010 / 3,072 bytes |
| Stack capacity | 167 bytes |
| Main / USB / timer / LED bounds | 103 / 5 / 2 / 2 bytes |
| Unresolved paths from those roots | 0 |
| Conditional total / margin | 165 / 2 bytes |

The conditional total is `103 + 2 + 3 × 17 + 5 + 2 + 2`. It includes CRT
main entry and all distinct IRQ sources. Bank, OEM wrapper, routing and
non-reentry assumptions remain open; this fit does not qualify the firmware.

IHX SHA256: `e4f1d3f64583da25a189c048a9905213a926ca43ae005652ab98964ccc1d954f`.
The [machine ledger](maximal-current.json) and [pass 30 evidence](../audits/maximal-pass30-20261025/README.md)
bind measurements to source, toolchain, images and bounded checks.

## Default keymaps

The opt-in `--compress-default-keymap` build option compresses the two compiled
default layers. The normal build leaves this option off. The current compiler
resolves all 256 original 16-bit defaults before generating 64 class bytes,
114 payload bytes and 32 row offsets. The final image contains those 210 data
bytes and the decoder; the 512-byte original table is excluded from the link.
The net saving includes decoder code. Physical XRAM grows by three bytes.
Encoder defaults and LED tables remain unchanged. The six-layer dynamic NVM
layout and 16-bit wire values remain unchanged.

Generation records the current compiler, source, generator, commands and both
compiler dependency closures. Final assembly and linked bytes are checked
against the compiler-resolved original. Reserved extraction-phase overrides
and changed final-only generated headers are rejected. The earlier review
findings and their corrections remain distinct from final packet review.

The fresh same-source option-off maximal control uses 44,601 CODE bytes and
has the exact IHX bytes of pass 29. The option-on `work` control uses 37,170
CODE and 2,557 physical XRAM bytes, saving 191 CODE bytes against its fresh
option-off control. Its highest address is `0xba90`, leaving 3,183 trailing
main-window bytes. Its main/USB/timer/LED bounds remain 98/5/2/2; the conditional
total is 160 of 171 stack bytes, leaving 11. These controls do not replace a
released image.

## Verification and limits

Seven generator tests, the actual translation-unit checks and all 16,777,216
uint8 coordinate triples pass; the native getter check uses ASan/UBSan. Exact
linked CPU execution passes 275 calls on each of the enabled and option-off
images: every valid default plus 19 invalid boundary cases. All occupied CODE
bytes remain unchanged. The decoder adds 42,260 instructions across the 256
valid lookups in this generic CPU model. This measures the default lookup
component only, without a claim about complete reset or real milliseconds.
Raw layer count is static evidence because DCE removes its function.
These checks do not prove ordinary keypress latency, durable storage or hardware behavior. Default decoding is on reset/default initialization paths;
ordinary dynamic key reads retain their NVM path.

Actual-image stack, CRT and finite reader checks pass. The pass 27 context
certificates and reviews remain byte-identical; current protected compiler
ASM, tools, map and provenance are revalidated with fresh postlink checks.
Other bounded CPU checks pass 629 RGB setter cases, 576 Combo GET cases,
48 cache-only updater cases, 15 distinct-source IRQ orders and 256 LED selectors.
All 4,047 occupied CODE bytes at or above `0xc700` remain unchanged in 20
sessions. The work IRQ check preserves all 37,170 occupied CODE bytes in 17
sessions. CRT checks stop at main entry. Main-loop and complete NVM/settings
initialization remain outside that proof.

Both NVM assembly kernels and existing compiler reductions remain enabled;
IRAM overlay remains off. Further CODE reduction, complete OEM startup/IRQ
and bank contracts, the opaque writer, full configured regressions and physical
validation remain open. No device, installer, packaging or release action was
performed.

## Two further passes and stopping condition

Both requested additional passes are recorded in the audit. The event-chain
pass tried one candidate. Its 12,288 bounded traces match, and three mutants
are rejected, but standalone component CODE grows from 565 to 627 bytes.
It was rejected without integration or a full build. Even an ideal removal
of its entire 58-byte wrapper would leave four bytes of growth; that estimate
is not a linker result.

The protocol pass found no eligible substantial variant. No patch or compile
was produced. Three specific repeated loops total 42 instruction bytes; their
ideal sharing ceiling is 28 bytes before costs. This bounds those loops only
and says nothing about all possible protocol rewrites.

The integrated saving is 201 bytes, below the requested approximate 0.5 KiB
checkpoint. The recorded decision is to pause after packet review and handoff.
The objective remains incomplete; no global compression minimum is claimed.
