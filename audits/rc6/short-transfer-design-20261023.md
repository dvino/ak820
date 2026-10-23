# Short calls and jumps: a bounded experiment

Date: 2026-10-23. This report covers ROADMAP P1.3. It is a design and
read-only source/artifact inspection. No assembler, compiler, linker, packer
or device command was run. No saving is measured. The earlier 531 candidates
are not a current opportunity count or a promise of 531 saved bytes.

Update, 2026-10-23: the official SDCC 4.4.0 release source is now retained and inspected in [the relocation source report](short-transfer-relocation-source-20261023.md). Its J11 page check appears to use the instruction site rather than the next PC. Binary boundary fixtures remain required. The source-unavailable statements below describe the earlier investigation; the general REL rewriter and firmware shortening remain unapproved.

The report follows the owner's supplied plain-language instructions and the
write-like-me skill. No retrieved personal writing sample was available or
claimed.

## Decision

Use a separate copy of the final, already outlined ASM as the first prototype
input. Replace one explicit symbolic `lcall` or `ljmp` there, then let the pinned
assembler and linker rebuild every address. Do not delete bytes from IHX or
patch a REL file in place. ASM keeps symbolic local branches, address constants
and tables available to the existing assembler. This reduces the amount of
relocation machinery the prototype must implement; it does not remove the need
to audit all address users or verify the final layout.

A generic REL rewriter is blocked pending the exact SDCC 4.4.0 extension
definitions and implementation. It must not infer the ACALL/AJMP relocation
record from the generic ASxxxx manual or from a newer fork.

## Version and primary evidence

The saved toolchain record is `docs/sdcc44-toolchain-checks.json`. It identifies
SDCC 4.4.0 #14620 and records SHA256 for SDCC, `sdas8051`, `sdld` and `packihx`.
The next experiment must hash the actual executables again and compare the
control's input manifest. A saved record does not certify a different executable.

The pinned distribution includes
`toolchains/sdcc-4.4.0/share/sdcc/doc/sdas/asmlnk.txt`. Sections 3.6.1 through
3.6.8 describe its object format. The inspected baseline
`qmk-8051-ak820/.build/rc6-candidate-erase-20261023/dce/protocol/host.rel`
starts with `XH3`: hexadecimal, most-significant byte first, 24-bit object
addresses. This is an object representation, not a 24-bit hardware CODE claim.
Its header has areas and symbols; `A` supplies area size and flags, `S` supplies
definitions/references, `T` contains an area-relative address and object bytes,
and the following `R` identifies the containing area and relocation entries.
`P` supplies paging records. Empty T records also occur; a parser must preserve
record association rather than assume each T is an instruction.

The manual's R description gives mode, byte index into the preceding T record,
and area/symbol index. It describes ordinary word/byte, symbol/area, PC-relative,
signed/unsigned, page and selected-byte flags. It explicitly directs readers to
`asxxxx.h` or `aslink.h` for ad hoc extension modes. Its printed T example uses
two address bytes even though section 3.6.1 supports XH3. Therefore neither
fixed two-byte T offsets nor an assumed four-byte entry parser is a sufficient
specification for this project's short-transfer extension.

Primary references checked for this report:

- [SDCC 4.4.0 release announcement](https://sourceforge.net/p/sdcc/mailman/message/58730353/)
  identifies the released source tag as `tags/sdcc-4.4.0-/sdcc`, including the
  trailing hyphen. It establishes the release/tag spelling, not the J11 format.
- [ASxxxx documentation](https://shop-pdp.net/ashtml/asmlnk.htm) is useful
  background. It is not substituted for the bundled fork's extension source.
- [8051 operand reference](https://www.keil.com/support/man/docs/is51/is51_instructions.asp)
  defines addr11 relative to the page of the following instruction.
- [ACALL encoding](https://www.keil.com/support/man/docs/a51/a51_acall.htm)
  gives the two-byte instruction, incremented PC and opcode address bits.

Attempts to read the release-tag `sdas/asxxsrc/asxxxx.h`,
`sdas/linksrc/lkrloc.c` and `sdas/as8051/i51mch.c` through SourceForge's tree/raw
URLs failed in this session. Their paths/content have not been verified. The
next prerequisite is to obtain the official 4.4.0 source archive or a pinned
release revision, record archive/file hashes, locate the actual assembler
encoder and linker relocation dispatch, and follow the J11 definitions through
both. Do not cite guessed paths or HEAD/trunk as verified release source.

## Address users that must be closed

| Address user | Required evidence before a changed image can pass |
| --- | --- |
| REL area sizes, T offsets, R/P entries and symbol definitions | Inventory every linked object, including extracted runtime-library members. Decode every encountered mode using the pinned implementation. Account for addends, selected bytes, index order and object-byte removal. Reject an unknown mode. ASM regeneration is preferred to manual record edits. |
| Global, local and absolute symbols; `.org`, equates and exports | Compare old/new MAP and ASM identities. Classify each absolute value as fixed hardware/window address or layout-dependent CODE address. Include area starts/lengths and linker-generated `s_`/`l_` symbols. Never shift SFR/XRAM constants as if they were CODE. |
| LCALL/LJMP and existing ACALL/AJMP | Match each original symbolic edge to a final decoded target. Check every existing short edge after any layout change, including library edges. A site with no source provenance cannot be rewritten. |
| SJMP, JZ/JNZ, JC/JNC, JB/JNB/JBC, CJNE and DJNZ | Reassemble symbolic targets and check final signed displacement and decoded destination. Reject embedded numeric displacements without an explained fixed target. Check both paths, including a branch spanning the changed instruction. |
| Computed jumps and switch tables | Inspect `jmp @a+dptr`, table entry widths, table base expressions and index scaling. Prove each indirect destination remains an instruction boundary. Reject any unexplained numeric CODE target or inline-data/control-flow ambiguity. |
| CODE/function pointers, XINIT and DPTR constants | Trace `.dw`, `.db` low/high expressions, `mov dptr,#symbol`, split DPL/DPH loads, generic-pointer CODE tags and callback tables. Linker relocation alone cannot repair an unlabelled numeric address. Preserve pointer ABI and table order. |
| Runtime/library transfers and return-address use | Include linked library members and startup. Reject hand-written code that consumes the call return address as inline-data location until its behavior is proved after the one-byte change. |
| Packer callbacks, entry and copied constants | Regenerate from the new MAP/IHX. `pack_ak820.py` reads `_keymaps`, `_encoder_map`, XINIT/XISEG and startup symbols; it emits callback LJMPs for timer, USB and LED from their linked symbols. Keep those roots and verify the actual packed bytes. |
| Protected regions and fixed entry contract | Preserve main `[0x3027,0xC700)` and low `[0x28A0,0x3000)` link windows; packer entry/helpers precede low CODE, callbacks occupy `[0x3000,0x3027)`, and NVM begins at `0xC700`. Re-run overlap, protected-ROM, startup and package validation. Total free bytes do not imply either window fits. |

This is the required consumer inventory, not a claim that every consumer in the
firmware has already been decoded. The existing DCE symbol search and its
external roots are useful inputs; they are not a complete relocation proof.
The builder retains packer-only roots including USB/timer/LED handlers because
their callback edges are absent from application ASM.

## Exact page check and layout procedure

For final short-site address `s` and final target `t`, require
`((s + 2) & 0xF800) == (t & 0xF800)`. ACALL uses opcode
`0x11 | ((t >> 3) & 0xE0)`; AJMP uses `0x01 | ((t >> 3) & 0xE0)`;
the second byte is `t & 0xFF`. Decode those final bytes independently.
LCALL/LJMP are three bytes, so testing the old site's `s+3` page gives the wrong
answer at a boundary. The check must use the new site and new target, not the
original link's addresses. No VS11K28A cycle saving is established here.

Shrinking moves subsequent symbols. Another short edge can then cross a 2-KiB
page boundary, and a candidate that passed on the control can fail after other
changes. Shrink-only eligibility is not monotone. Do not repeatedly apply a
global candidate set until an unproved fixed point appears.

For the first probe, use one candidate and one fresh full link. If it fails
the final page check, discard that candidate without widening it silently.
For a later bounded set, retain an explicit per-site long/short decision,
relink after each accepted addition, and validate all short sites each time.
Reject an addition that invalidates an earlier edge. Record the decision set,
layout hash and iteration limit; detect repeated states if a future relaxer
allows widening. Deterministic termination is required before broad use.

## Smallest reproducible experiment

1. Wait for the lead's canonical build to finish. Freeze its manifest, tool
   hashes, flags, object order, library inputs, ASM/REL/LST/RST, MAP/MEM/IHX and
   source hashes. Keep six layers, sixteen macros and all feature settings.
2. In a new research directory, reproduce the exact control from final outlined
   ASM with the original assembler/link flags and libraries. Its IHX must match
   byte for byte. Do not rerun DCE/outlining on modified input: that would mix
   transformations and can select different helpers.
3. Before firmware edits, make isolated assembly/link fixtures for symbolic
   local and external ACALL/AJMP. Cover positive and negative page cases,
   especially sites `0x07FD`, `0x07FE`, `0x07FF` and targets `0x07FF`, `0x0800`.
   Record diagnostics, final bytes, XH3 R entries and source-backed decoding.
   A linker that silently encodes an out-of-page transfer is a failing fixture,
   not evidence that the program is valid. Include symbol pointers, a branch
   across the site and a table address in the fixture.
4. Select one explicit symbolic transfer with a known target, outside startup,
   IRQ and NVM-sensitive code for the first probe. Record module/area/function,
   ASM line, original REL relocation, old site/target and expected new encoding.
   Change only its mnemonic in the copied ASM. Assemble and relink the full
   image; keep the candidate's complete artifacts and commands.
5. Compare every address user above. Require exactly the intended symbolic edge
   and instruction-kind change; relocated operands elsewhere may change bytes
   but must preserve destinations by symbol identity. Check both windows,
   XRAM/stack, startup, final packer callbacks, hashes and package invariants.
   Compare complete linked/packed size, not nominal opcode bytes.
6. Run the applicable offline feature/ABI/CPU tests, including paths through
   the changed edge. Save limits and skipped paths. Independent review must
   examine implementation, documentation, decoder evidence and the full diff
   before any integration or commit. Hardware behavior and timing remain
   untested; this plan authorizes no live operation.

Stop at a control mismatch, unidentified address consumer, unresolved library
member, unknown relocation mode, linker diagnostic, invalid page/displacement,
wrong decoded target, changed ABI/observable behavior, window overlap, failed
regression or nonpositive complete-image benefit. Preserve the failed artifacts.
Do not restore, reset, retry or perform a device operation to make a probe pass.

## What remains unresolved

The release-specific J11 record layout and linker overflow checks have not
been verified from source. No complete consumer certificate, new eligibility
count, fixture result, current-baseline candidate or saving is produced by
this report. The safe next deliverable is the source-backed relocation fixture
and one isolated ASM experiment, not a global shortening implementation.
