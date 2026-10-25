# Whole-program compression

The target is one `maximal` image with all 14 optional modules and every base
function. OS indicators, six layers, sixteen saved Vial macros with an
8192-byte store, eight two-key Combos, eight Tap Dance and eight Key Override
entries, both encoder directions and NKRO remain enabled.
The [plan](MAXIMUM-FUNCTIONALITY-PLAN.md) defines the fixed behavior and limits.

## Current image: 26b

`.build/resume26b-state-bytes` uses **44,747 occupied CODE bytes**. The main
window still overflows by **4,394 bytes**, so this is an oversized diagnostic,
not an installable firmware image. The physical windows remain
`[0x28a0,0x3000)` and `[0x3027,0xc700)`. Loader, NVM and macro storage remain
reserved. LED DMA has its separate fixed area.

| Measurement | Current value |
| --- | ---: |
| Low / main occupied CODE | 1,741 / 43,006 bytes |
| Highest main address | `0xd829` |
| Main-window overflow | 4,394 bytes |
| Ordinary XRAM + flash stage | 2,943 + 64 = 3,007 / 3,072 bytes |
| Available stack | 167 bytes |
| Main / USB / timer / LED bounds | 103 / 5 / 2 / 2 bytes |
| Unresolved paths from those roots | 0 |
| CRT main-entry frame | 2 bytes |
| Conditional total with all distinct IRQ sources | 165 bytes |
| Margin in that model | 2 bytes |

The total is `103 + 2 + 3 × 17 + 5 + 2 + 2`. It depends on the documented bank,
stack, OEM wrapper and distinct-source interrupt assumptions. The complete
hardware startup, routing and non-reentry contract is still open. A conditional
fit does not qualify the full firmware.

IHX SHA256:
`47400365dfe8e7e56fd46a548938ca8c9024467ca13120f506cb7213e9f7ef10`.
[The machine ledger](maximal-current.json) and
[retained verification](../audits/maximal-continuation-20261025/README.md)
record the exact inputs, images, commands and review closure.

## Measured continuation from image 22

The published source baseline `09330ab` was rebuilt with pinned SDCC 4.6.0.
Its IHX reproduces the handoff byte for byte:
`576fd31f4ccbe85f722cf0837c688aee69c5a517694f5d8828bdc0a8d3067fe8`.
A fresh reviewed IRQ context was generated from a retained bootstrap build;
the unavailable external overlay package was not reconstructed or assumed.

| Image | Occupied CODE | Physical XRAM | Stack capacity | Change |
| --- | ---: | ---: | ---: | --- |
| 22, reproduced | 45,461 | 2,976 | 156 | Read kernel on; overlay off |
| 22, same-source read option off | 45,499 | 2,980 | 156 | Original C block reader remains |
| 24 | 45,173 | 2,961 | 167 | Combo GET, fixed LED packet, NVM updater |
| 25 | 45,056 | 2,961 | 167 | Bounded redundant DPTR restore removal |
| 26b, current | 44,747 | 3,007 | 167 | One masked byte per tapping source |

The read option alone saves 38 CODE and four XRAM bytes on identical sources.
The complete continuation saves **714 CODE bytes** against image 22, spends
31 additional XRAM bytes, and increases stack capacity by 11 bytes. These are
linked totals. The separate historical overlay image 21c had 169 stack bytes;
that number does not belong to any current image. Overlay remains off.

The initial image 26 build stopped on an empty staging-directory collision.
No firmware result is attributed to it. A fresh build directory produced 26b
without bypassing a check. Earlier intermediate and failed attempts remain
separate in the retained evidence.

## Changes

- **Combo GET:** the target parser saves the requested index, clears the reply
  record, and passes its XDATA packet storage directly to the existing getter.
  Invalid-index replies remain zero filled. SET and its request echo, firewall,
  marker/version injection and durable writer are unchanged.
- **LED packets:** the target helper uses the public setter's fixed 32-byte
  contract, rejects a nonzero high index byte and oversized count, then walks
  typed HSV storage. Bounds, tail clipping and the brightness clamp remain.
  Other targets retain the previous helper.
- **NVM update:** default-off `--nvm-update-block-asm` selects a separate
  translation unit. Each scalar read precedes its source read. The first
  mismatch tail-calls the existing writer with the original source, all three
  generic-address bytes and original 16-bit length. Equal/empty requests do
  not write. The comparison preserves R0/R1; the unchanged C tailwriter may
  clobber them under its normal ABI. See [the kernel contract](NVM-UPDATE-KERNEL.md).
- **DPTR restore:** the existing guarded parameter pass can remove a restore
  immediately followed by a full DPTR overwrite. Only a bare C symbol or fixed
  16-bit immediate is accepted; labels, directives and expressions reject the
  enhancement. Equivalence is reached after the unchanged overwrite. Review
  found the original operand grammar accepted location-dependent expressions;
  that grammar was narrowed and the new rejection cases pass.
- **Tapping state:** all five independent tap-hold/One Shot flags now use one
  masked byte per source. The array grows from 82 to 130 bytes; fewer parameter
  bytes make the linked XRAM increase 46. The complete image saves 309 CODE
  bytes against 25. Ownership, cancellation, source IDs and encoder handling
  are unchanged. The stale lost-release test mutation was updated to use the
  existing accessor; all 13 deliberately broken variants are rejected.

Both NVM kernel options, private parameter trimming, register-save trimming,
short calls, tail sharing and the 400-helper cap are enabled in 26b. The new
NVM updater and compiler passes remain opt-in. No feature registry, persistent
format, installer image or release qualification record was changed.

## Verification and limits

Component checks passed within their stated scope:

| Component | Evidence |
| --- | --- |
| Combo adapter | 32,768 cases in each native and target-alignment host model; SDCC alignment check |
| LED helper/setter | Index/count grid, high-byte rejection, value edges and all packet lengths under ASan/UBSan |
| NVM updater | 3,169 paired SDCC/s51 cases with scalar/writer mocks; maximum-length first mismatch |
| DPTR enhancement | 15 host tests; 1,024 CPU state pairs / 2,048 executions; 40 admitted sites |
| Tapping byte state | 1,164,960 writes and 151,444,930 source comparisons; 156 retained-QMK traces; 13 negative controls |

The exact 26b image passed a separate bounded CPU suite: 629 public RGB setter
cases, 576 public Combo GET cases, 48 NVM updater/real-writer cache cases,
15 ordered distinct-source IRQ nests and all 256 LED selector values.
The configured target brightness clamp is 160. All eight valid Combo records
fit in their primed 64-byte cache pages. Dirty page crossings that require
flash are excluded, and physical erase/program entries are protected by stop
breakpoints. No such entry was reached.

CRT ran only to main entry. NVM/settings initialization and the main loop did
not run. All 4,394 occupied CODE bytes at or above `0xc700` remained unchanged
in all 20 simulator sessions. This avoids the ordinary fixture's flash seeding,
which would overwrite executable bytes in an oversized image.

Fresh linked inventory, application stack and CRT checks pass. A newly authored
finite reader check covers 45 reachable instructions, two additional stack
bytes and seven rejected effect mutations. It proves conditional R0–R7
preservation for the actual reader, not read values or the opaque writer.
The complete 65,535-byte equal updater traversal, source-pointer wrap and
physical flash behavior are not dynamically qualified by these fixtures.

The current-source `work` control uses 37,545 CODE bytes and 2,554 physical
XRAM bytes. Its highest address is `0xbc07`, leaving 2,808 trailing main-window
bytes. Fresh main/CRT/IRQ bounds give 160 of 171 stack bytes. It passed all 15
IRQ orders and 256 selector values with all 37,545 CODE bytes unchanged in
17 sessions. These legal resources qualify only this bounded control check;
they do not qualify `maximal` or replace the released work image.
Full configured regressions remain blocked by illegal maximal CODE placement
and the incomplete OEM startup/IRQ, bank and opaque-writer contracts. No device
writes, reset, bootloader transition, flashing or installer replacement occurred.

## Deferred measurements

A scratch-only direct-DATA outliner screen reproduced the current selection,
then found 131 extra nominal bytes with the old helpers fixed, or 171 with
reselection. Adding ordinary BIT access raises those estimates to 133/175;
OSEG adds nothing. Private relocation, allocation, lifetime and IRQ proofs are
still missing, so production eligibility was not broadened.

Replacing the Tap Dance nibble map with bytes saves 66 raw object CODE bytes
but consumes 64 XRAM bytes. That would use almost all remaining RAM before a
linked measurement. It remains a separate lower-priority candidate.
Earlier rejected five-plane state, rule-bytecode, medium-model and compiler
switch experiments remain recorded in Git history and
[optimization research](OPTIMIZATION-RESEARCH.md). No screen proves a global
minimum. The next work is further code reduction and closure of the exact
startup/IRQ contract; the complete-feature objective is not yet met.
