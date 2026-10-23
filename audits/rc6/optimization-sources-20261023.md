# SDCC code-space research, 2026-10-23

This bounded search supports ROADMAP P1/P2. It adds experiment ideas and
version checks, not measured savings. No build, firmware change or device
operation was performed for this report. Preserve six layers and sixteen
macros. Use the current linked baseline selected by the lead; SPACE-OPTIONS
describes an earlier image and must not supply the new control's hash or size.

The report follows the supplied plain-language instructions and the
write-like-me skill. No personal writing retrieval was available or claimed.

## Primary references and their limits

All links below were checked on 2026-10-23. They are upstream documentation,
maintainer issue records or an instruction reference, rather than benchmark
claims from third parties.

| Reference | Question answered | Revision and applicability |
| --- | --- | --- |
| [SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf), sections 3.3, 3.5.1, 3.13 and 4.1.5 | Which memory-space, optimizer and ABI controls exist? | The retrieved cover says **4.6.4**, while retaining date 2024-01-29 and revision 14650. The `.io` URL returns the same cover. This is not an immutable 4.4.0 manual. Check each proposed control against the pinned executable and its bundled documentation before use. |
| [SDCC release history](https://sdcc.sourceforge.net/previous.php) | What belongs to the compiler releases? | Records 4.4.0 on 2024-01-29 and 4.5.0 on 2025-01-28. It does not establish a CODE benefit or VS11K28A compatibility. Keep 4.4.0 pinned. |
| [8051 instruction reference](https://www.keil.com/support/man/docs/is51/is51_instructions.asp) and [opcode table](https://www.keil.com/support/man/docs/is51/is51_opcodes.asp?bhcp=1) | What is the exact short-transfer condition and encoding cost? | ACALL/AJMP are two bytes, LCALL/LJMP three. The 2-KiB page is determined from the first byte after the short instruction. This supports encoding checks, not VS11K28A oscillator timing. |
| [ASxxxx/ASlink documentation](https://shop-pdp.net/ashtml/asmlnk.htm) | Where should relocation format and linker behavior be investigated? | Upstream assembler documentation; not proof that the SDCC-bundled fork has identical relocation behavior. Read the pinned assembler/linker source or bundled manual before writing a relocation pass. |
| [SDCC bug 3711](https://sourceforge.net/p/sdcc/bugs/3711/) | Can a smaller bit parameter create an ABI failure? | Maintainer reproduced an MCS51 4.4.0 failure for calling a reentrant function with a bit parameter; fixed in r14692 after release. Do not introduce this shape as a size shortcut. |
| [SDCC bug 3712](https://sourceforge.net/p/sdcc/bugs/3712/) | Are later bit/reentrant fixes sufficient for all parameter combinations? | Related medium-model bit plus long-long parameter problem was fixed in r16058 in 2026. Different model/shape from this build; a warning about applicability, not evidence the current firmware is affected. |
| [SDCC patch 504](https://sourceforge.net/p/sdcc/patches/504/) | Is newer MCS51 peephole work safe to transplant? | Open patch set against trunk r16673, created 2026-07-03, updated 2026-08-26. Includes accumulator/carry guards, non-carry PSW tracking, tail/retrack infrastructure and a proposed fixed-register-bank control. Its author reports trunk regressions and a project corpus, while requesting review. Neither release support in 4.4.0 nor target correctness is established. |

The manual documents generic-pointer memory tags and more efficient typed
access, caller-save defaults and a project-wide callee-saves list. It documents
size/speed and selected optimization controls. It also explicitly excludes
MCS51 from `--max-allocs-per-node`; raising that setting is not a supported
MCS51 size experiment. These statements remain subject to the version check
above. [Manual](https://sdcc.sourceforge.net/doc/sdccman.pdf).

## Controlled experiments to consider

These are local research proposals. The source locations identify inputs to
inspect; no candidate is accepted until the fresh relocated image proves it.

| Candidate and local input | Hypothesis and expected effects | Smallest useful probe and stop rule |
| --- | --- | --- |
| Typed-pointer boundary: generic helper calls in the fresh linked inventory | A private XDATA-only or CODE-only operation may avoid generic dispatch and tag setup. CODE may fall; RAM and stack may move; no intended NVM change. | Pick one helper with proven single-space callers. Change its declaration, definition and every caller together. Compare complete image and traces for zero/one/max length, boundary addresses and returned pointer/value. Stop if any caller requires another space, the ABI cannot be proved, or linked gain is nonpositive. |
| Shared protocol tail: repeated reply construction or error return in reachable handlers | Common emitted work may be shared. Added parameter marshalling or generic pointers can erase the gain. A shared tail can change timing and stack. | Choose repeated emitted instructions with the same state effects. Compare an explicit typed helper with the current code, including malformed lengths, unsupported commands and all return paths. Stop on changed reply bytes, side effects, clobbers or no linked gain. Do not weaken validation or NVM failure stops. |
| Callee-save extension: `util/build_ak820.py`, `AK820_CALLEE_SAVES` | One additional frequently called small function might reduce repeated caller spills. Its own prologue and children can cost more. | Keep the current list intact and add one audited C function per isolated control, with the same ABI list in every translation unit. Inspect all callers, children, return registers and IRQ nesting. Record worst relevant stack path. Reject unproved assembly/library boundaries and any net loss. |
| Inlining boundary: current call graph and size listing | A single-call wrapper might shrink when inlined; a repeated inline body might shrink when outlined. Both can change register pressure. | Compare only one wrapper/body family and inspect final caller and callee bytes. Preserve function-pointer use, reentrancy and observable access order. Stop on spill growth, timing-contract loss or nonpositive total gain. Do not assume `inline` means the compiler emitted an inline body. |
| Scoped optimizer control: spill-heavy functions identified in relocated assembly | Disabling one transformation may shorten spill-heavy output even though it removes an optimization. Execution may slow. | First verify pinned support, then test one function with a balanced pragma scope for `nogcse`, `noinvariant` or `noinduction`. Inspect spill slots and loop accesses; compare finite-domain output and linked traces. Reject changed volatile/MMIO access, unacceptable cycles, stack growth or no gain. |
| ACALL/AJMP layout prototype: assembler relocation records and final packer map | Eligible transfers can save one encoding byte each before placement effects. This is not a guaranteed whole-image saving. | Use a separate relocation-aware prototype, retaining original bytes and relocation provenance. Recompute targets, symbols, tables and instruction boundaries after every shrink, including page-edge sites. Validate the packed image and protected windows exhaustively. Stop if any address consumer or relocation is not accounted for. A global `--acall-ajmp` switch is not a substitute. |

Each probe needs a clean copy of the same baseline, exact compiler and input
hashes, full linked CODE, both placement windows, XRAM, stack, IHX hash and
relevant regression evidence. Reject a size win that loses a supported
behavior. Host/CPU agreement does not prove USB timing or physical behavior.

## Duplicate and negative findings

- Typed pointers, common tails and callee saves are existing directions, not
  newly discovered wins. The builder already supplies an audited callee list,
  exact instruction outlining and `--opt-code-size` as its extra-flags default.
  Check final recorded compile arguments rather than the platform file alone.
- The previous 57 generic-pointer sites and 531 short-transfer candidates are
  inventories for earlier layouts. They provide neither current ranking nor a
  saving. Existing outlining must be checked before proposing the same tail.
- `--max-allocs-per-node` is excluded by the current manual for this backend.
  No experiment budget should be spent on a Z80-oriented allocator claim.
- Patch 504's `--fixed-regbank` and new tail infrastructure are trunk proposals,
  not verified pinned options. The loader/IRQ boundary makes a register-bank
  shortcut particularly unsuitable without a separate contract. No broad
  peephole import is proposed.
- The attempt to open a guessed 4.4.0 tagged `gen.c` URL failed. No claim about
  that tag's implementation is made. The pinned compiler sources/bundled
  manual remain a necessary follow-up for exact implementation details.
- Patch 500 appeared in the upstream index as an `emit_add_dptr` extraction
  proposal, but its detail page was inaccessible. Treat it as an unread lead,
  not a validated technique or a reason to change pointer arithmetic.
- The existing SDCC 4.5 internal-compiler failure is already recorded in the
  roadmap. Release notes do not overturn it. Compiler replacement remains a
  separate correctness project before size comparison.
- Four layers, smaller macro capacity, compact CIE and packed Direct HSV are
  already covered by SPACE-OPTIONS/ROADMAP. This search adds no new measured
  benefit for them. Keep their separate CODE/RAM/NVM limits.

## Search record

Queries were bounded to upstream references. Useful queries:

```text
site.sdcc.sourceforge.net doc sdccman callee-saves acall ajmp opt-code-size
site.sourceforge.net/p/sdcc/code 4.4.0 mcs51 gen.c tail
site.keil.com support man docs is51 acall ajmp PC 2048
site.sourceforge.net/p/sdcc/bugs mcs51 callee saves 4.4
site.sourceforge.net/p/sdcc/patches "tail" "mcs51"
```

A search for an `R_J11` relocation reference on a third-party mirror did not
produce useful primary evidence and was not used. Search results also exposed
an older manual mirror and general SDCC tutorials; they were not used in place
of upstream references. This is a bounded compiler/ABI/transfer search, not a
claim to cover all optimizations, QMK algorithms or analogous 8051 projects.
