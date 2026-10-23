# SDCC research for the next size experiments

Date: 2026-10-23. This report reads upstream release sources and the current
build evidence. It does not report a new firmware optimization. No compiler,
assembler, linker or USB command ran for this work. The separate full 4.6.0
experiment belongs to the lead and its report must supply its result.

The control supplied for this work is SDCC 4.4.0, 39,144 CODE bytes, 2,067
XRAM bytes and 152 bytes of available stack allocation. Free CODE is 1,361
bytes: 1,332 in the main window and 29 in the low window. These are allocation
figures, not measured worst-case stack use or installed-device validation.
Six layers and sixteen macros remain requirements.

The supplied plain-language guidance and writing-style skill were applied.
No personal writing retrieval was available or claimed.

## Sources that can actually answer the version question

The [official release page](https://sdcc.sourceforge.net/) dates 4.6.0 to
2026-06-22. Its code-generation improvement claim names the Z80-related ports.
It does not promise a smaller MCS51 image. The current online manual changes
with development, so this investigation used the actual 4.4.0 and 4.6.0 source
packages for implementation checks.

The already retained 4.4.0 archive is identified in
`short-transfer-relocation-source-20261023.md`. For 4.6.0 the
[official directory](https://sourceforge.net/projects/sdcc/files/sdcc/4.6.0/)
lists `sdcc-src-4.6.0.tar.bz2`, dated 2026-06-22. Download succeeded through
`https://pilotfiber.dl.sourceforge.net/project/sdcc/sdcc/4.6.0/sdcc-src-4.6.0.tar.bz2`.
The archive has 26,552,471 bytes and SHA256
`5fd6a93e5997ce01756868fe35e441095cfb637894a80c262514a634094973b6`.
This identifies the downloaded bytes; no publisher signature was checked.

The archive, extraction, per-file hashes and unified source diffs are private
under `.build/rc6-deep-sdcc-research-20261023/` at repository root.
`source-comparison.json` records the compared files. Source paths and line
numbers below refer to those extracted releases, not a guessed Git tag.

## What changed in the MCS51 backend

The directory comparison changes six files, with 323 inserted and 109 deleted
lines. This is a source diff count, not a firmware size prediction.

* `ralloc.c` changes a dump-stage name from `_2` to `_3`. There is no new MCS51
  register allocator in that file. `rtrack.c` is unchanged.
* `gen.c` changes noreturn calls to jumps and skips their register-save and
  cleanup paths; fixes parameter receive and stack-frame details; handles a
  two-register swap; adjusts operand release and comparison generation; and
  changes some complement and Boolean-bitfield paths. The substantial common
  compiler changes outside this directory also matter, so this small diff
  cannot certify ABI or semantic equivalence.
* `peeph.def` adds rule 186.f for one byte-table CODE-address sequence and rule
  303 to forward an accumulator value without an intermediate dead location.
  Rule 302 restarts matching after deleting a dead move. Short branch rules
  are reordered. Other edits add volatile guards and correct operands.
* `main.c` adds restartable atomic support and assembler option metadata, and
  handles negated bit operands in read/write tracking. This is not a general
  target-specific dual-DPTR optimization.

The 4.6.0 ChangeLog attributes MCS51 peephole fixes on 2026-04-01 to part of
patch 493. Its online detail page was inaccessible during this investigation;
the release-source diff above is the evidence, not a claim to have reviewed
every proposed patch. A complete compiler comparison must also account for
shared optimizer and library code and the project's post-compiler outlining.

## Flags: useful controls and dead ends

| Control | Exact implementation evidence and decision |
| --- | --- |
| `--opt-code-size` | Already supplied by `util/build_ak820.py`; current saved flags contain an earlier `--opt-code-speed` and a later `--opt-code-size`. Do not count enabling size optimization as new work. The exact recorded arguments are authoritative. |
| `--peep-return` | Already enabled by default. In both releases `SDCCpeeph.c:503`, `optimizeReturn()` accepts `peepReturn >= 0`. In 4.4 `SDCCmain.c:1393-1409`, only explicit `--no-peep-return` or `--debug` disables it; explicit `--peep-return` sets 1. Current flags have `-g`, not `--debug`. Do not infer GCC's `-g` semantics or claim a new win from adding the already-default flag. |
| `--peep-file FILE` | A real extension point: 4.4 `SDCCpeeph.c:3959-3975` reads built-in rules first and then the extra file. It does not replace built-ins unless combined with `--no-peep`. Keep built-ins; record the extra file hash. Import one independently proved rule, not a trunk rule collection. |
| `--peep-asm` | `SDCCgen.c:206,290` removes the inline-assembly exclusion from matching; the peephole loop otherwise skips `isInline` lines. This exposes hand-written IRQ/startup/flash code to assumptions intended for compiler output. No global experiment is recommended. First inventory inline blocks and their live flags, MMIO order and clobbers. |
| `--max-allocs-per-node N` | Shared graph algorithms reference it, but MCS51 has zero registers in the tree-decomposition allocator description. Both 4.4 `SDCCopt.c:3305` and 4.6 `SDCCopt.c:3949` explicitly exclude MCS51 from lospre because added temporaries caused a size regression. Raising N is not a supported MCS51 allocator improvement; `--nolospre` also cannot disable a pass this backend never runs. |
| `--callee-saves LIST` | Already applied to eleven audited functions in every translation unit. Add only one C function whose callers, children and register use can be checked together. `--all-callee-saves` changes every boundary, including libraries and assembly, and is not a safe shorthand for the existing method. |
| `__using(n)` / register banks | The builder documents bank 0 at the application C boundary. Another bank consumes internal RAM and affects IRQ/loader and direct `arN` accesses. The proposed `--fixed-regbank` is post-release patch 504, absent from the two release option tables; it is not a supported flag to add. |
| `--parms-in-bank1` | Removed in development version 4.3.6, as the release manual's compatibility section records. It is absent from 4.4's MCS51 option table. Old tutorials are inapplicable, especially with warning 117 disabled in the current flags. |
| `--stack-auto`, `--xstack` | Real ABI and allocation changes, not isolated size flags. MCS51 `main.c` selects separate small/medium/large/huge library families and stack variants. Existing assembly, interrupt paths, library parameters and placement must all agree. Do not try a partial conversion while claiming unchanged stack or compatibility. |
| `--model-small/medium/huge` | Small moves default objects toward scarce internal RAM; medium uses paged external memory; huge introduces banked calls. Current large model and fixed loader contract cannot be changed by a one-flag size probe. Prefer explicit memory-space types for a private object/helper whose addresses are known. |
| DPTR and generic pointers | The MCS51 release option table offers no dual-DPTR selector. DS390/DS400 options and STC251 forks are different targets. `--xram-movc` changes the instruction used to read XRAM; it requires a hardware memory mapping contract, not merely an 8051-compatible core. Generic-pointer tags remain `00/40/60/80` for XDATA/near/PDATA/CODE in both port descriptions. A typed private pointer can remove dispatch, but does not justify changing public QMK/Vial interfaces. |

## Runtime libraries and a compiler correctness gate

The current link map includes `___memcpy`, `_memset`, `__gptrput`, `__mulint`
and `__gptrget`. The corresponding upstream sources `__memcpy.c`, `_memset.c`,
`_gptrput.c`, `_mulint.c` and `_gptrget.c` are byte-identical between 4.4.0 and
4.6.0. Replacing these with the newer source has no demonstrated algorithmic
benefit. Their compiled output can still differ. `mcs51/gptr_cmp.asm` changes
where DPL is pushed and popped so the null-pointer early path avoids that work;
it does not remove the instructions from the function. Use the exact model's
library and inspect the map's extracted members; never mix compiler and library
ABIs merely to obtain a smaller image.

[Accepted patch 513](https://sourceforge.net/p/sdcc/patches/513/) is a more
important adoption check than release marketing. Applied in r16814 on
2026-08-26, after 4.6.0 #16555, it fixes materializing a carry Boolean through a
pointer. Both downloaded release `gen.c` files still contain at line 1125
`aop->size = sym->ruonly ? 1 : 0;`; the accepted fix also considers
`POINTER_SET(ic)`. [Bug 3845](https://sourceforge.net/p/sdcc/bugs/3845/)
supplies a Boolean struct-member reproducer. This does not establish that the
current firmware triggers it, and the original report used other flags.
It does require targeted emitted-code and CPU checks before treating either
release as correct for newly changed Boolean pointer/member stores. A successful
full compile does not test this property. No compiler patch was applied here.

The lead also identified [bug 4066](https://sourceforge.net/p/sdcc/bugs/4066/?limit=25),
fixed by patch 514 in r16836 on 2026-08-30. A peephole can shorten jump-table
entries and a later rule can widen some again, breaking the table stride.
The reported reduced trigger uses speed optimization and `--nosidechannels`;
current saved flags end in size optimization and no `nosidechannels` occurrence
was found in the inspected quantum, MCS51 platform or board source directories.
That is an applicability negative, not proof that every table is correct.
Check every emitted table's index stride, entries and targets in any compiler
or peephole experiment.

## Narrow experiments worth retaining

1. Finish the isolated 4.6.0 comparison already running. Compare source and
   input hashes, warnings, final retained functions and library members, both
   placement windows, XRAM and stack paths. A delta in a translation-unit ASM
   file is insufficient because outlining and placement can reverse it. Add
   Boolean pointer-store tests for true and false, bit/reentrant parameter
   shapes and existing firmware CPU regressions. Stop on an unexplained
   warning, ABI difference, semantic mismatch or nonpositive linked benefit.
   Compiler adoption remains separate from accepting a size result.
2. If 4.6.0 is unsuitable, inventory current retained 4.4 ASM for the exact
   186.f byte-CODE-table sequence and the accumulator-forwarding shape of 303.
   Read all liveness and volatile conditions against the 4.4 matcher before
   copying one rule into a private `--peep-file`. Test boundary indexes, carry
   inputs, aliasing and live output registers. Prefer 186.f first because it
   describes a bounded address sequence rather than a broad dead-store rule.
   First count valid sites; no count or whole-image saving was measured here.
3. [Patch 491](https://sourceforge.net/p/sdcc/patches/491/) gives a concrete
   source-shape lead: pointer postincrement can expose DPTR increment, while
   a later subtraction can undo the saving. Search current retained loops for
   repeated pointer-register/DPTR copies. Compare one bounded CODE-string or
   XDATA-buffer loop with an explicit typed, postincrement form. Check zero
   length, first terminator, maximum length and address boundaries; never
   remove bounds or allow an extra MMIO read. The upstream proposed carry and
   loop-hoisting rules remain proposals; copying them without live-register
   proof is not justified.
4. For a shared generic helper, rank current linked call sites by repeated tag
   setup and dispatch. Specialize one private CODE-to-XDATA or XDATA-to-XDATA
   operation only when every caller's space is proved. Keep the generic helper
   if other spaces still need it. Count added specialized body and wrappers
   against saved call-site work. Stop if overlap/return-pointer semantics,
   IRQ reentrancy or a pointer-space assumption is unclear.

Concrete source starting points are the CODE lookup in
`quantum/send_string/send_string.c:210` for rule 186.f, and the bounded packet
fill in `quantum/vial.c:120` for comparing indexed with typed-pointer loop
forms. The packet fill and parser already have XDATA specialization; that is
existing work, not a new pointer conversion. The string parsers call other
functions inside their loops, so they cannot simply keep DPTR live across those
calls. First use their emitted assembly to determine whether a narrower leaf
loop exists. Several generic `memcpy` sites in Vial belong to optional feature
branches; source search alone does not prove they survive the current build.

All four proposals have **unknown benefit** until measured in the complete
image. Acceptance needs positive linked CODE saving, legal placement,
preserved six layers/sixteen macros, no unexplained RAM/stack change, matching
protocol and CPU results, and independent review. CPU agreement cannot prove
USB timing, physical inputs, durable flash behavior or installed firmware.

## Research record and deliberately excluded leads

All web checks were made on 2026-10-23. Queries included:

```text
SDCC 4.6.0 release notes mcs51
SDCC manual peep-return max-allocs-per-node mcs51 callee-saves
site.sourceforge.net/p/sdcc "peep-return" mcs51
site.sourceforge.net/p/sdcc "peep-asm" bug
site.sourceforge.net/p/sdcc "callee-saves" mcs51 bug
site.sourceforge.net/p/sdcc "mcs51" "dptr" optimization
site.sourceforge.net/p/sdcc "mcs51" "parms-in-bank1"
site.sourceforge.net/p/sdcc/patches/493 "mcs51"
site.sourceforge.net/p/sdcc/bugs/3804
```

The official source archive replaced the previously unsuccessful guessed-tag
lookup. [Patch 504](https://sourceforge.net/p/sdcc/patches/504/) remains open;
its tail/retrack/liveness changes target trunk r16673 and were deliberately
held until after release. Corpus rule-hit totals are not CODE savings or
AK820 validation. [Patch 466](https://sourceforge.net/p/sdcc/patches/466/)
likewise proposes broad liveness/read-write changes and is not an isolated
production-rule source. Patch 500's detail page and bug 3804 were inaccessible;
their titles or snippets were not promoted to verified optimizations.

[Bug 3903](https://sourceforge.net/p/sdcc/bugs/3903/) concerns huge-model
function-pointer comparison. It explains why moving to a different memory
model needs tests; it does not establish a defect in this large-model image.
Third-party tutorials, packaging pages, mirrors and STC251 fork advertising
were not used to infer supported MCS51 flags or likely savings.

The short-transfer investigation is not repeated as a new win. Its current
fixture run stopped at a linker crash, and the boundary mismatch remains
unmeasured. Neither a global `--acall-ajmp` flag nor a silent linker can close
that prerequisite. See `short-transfer-fixtures-20261023.md` before scheduling
any firmware shortening experiment.
