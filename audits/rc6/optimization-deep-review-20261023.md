# Review of the deeper optimization research

Date: 2026-10-23. Independent review of the analysis, local inventory and
SDCC release-source research. The reviewer did not write those reports or
their inventory. No compiler, linker, USB command, reset or flash ran during
this review. Existing unrelated working-tree changes were left alone.

## Result

The research reports pass this review. No substantive finding remains in
the reviewed analysis. This approves the evidence and proposed experiment
boundaries; it does not approve a compiler change or a firmware update.
The separate 4.6 full-build experiment is outside this verdict until its
own complete evidence is reviewed.

The owner subsequently made testing and release of the current 4.6 fixes
the immediate priority; the other optimization ideas remain future work.
The final English/Russian ROADMAP and SPACE-OPTIONS consistency reread is
complete. Their ranked probes, unknown gains, short-call blocker and
conditional compiler backport agree with the research. Release qualification
still needs a separate review.

The reread found stale text saying the 4.6 build had no linked size, dangling
references to a removed comparison, an obsolete priority sentence and an
ambiguous label for 38,100 CODE bytes. The authors removed the stale text and
references, stated the current priority and labeled the size as build-report
CODE. A final targeted reread confirmed those corrections. ROADMAP explicitly
records the separate 38,105-byte map occupancy and leaves reconciliation to
the release audit. No document finding remains open in this review.

## Evidence checked

- Read `optimization-deep-analysis-20261023.md`,
  `optimization-deep-local-20261023.md` and its JSON,
  `optimization-deep-sdcc-research-20261023.md`, plus the short-transfer
  source and failed-fixture records.
- Recomputed hashes of all 64 final RST files, the IHX and all inspected
  source files recorded by the local inventory: no mismatch. Its IHX hash
  is `4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
  The reported 39,144 CODE, 2,067 XRAM and 1,361 free CODE bytes agree
  across the reports. Stack allocation capacity is correctly distinguished
  from a measured global stack bound.
- Checked the inventory script's instruction-row filter and grouping.
  The JSON sums to 36,359 instruction bytes in 436 nonempty label groups,
  with 1,302 direct transfer sites. Its 49 generic-pointer sites split into
  34 gets, 13 puts and two comparisons; other reported counts are 45 memcpy,
  seven integer multiplies and five indirect-call helper sites. The report
  correctly excludes data, absent library bodies and execution frequency.
  These counts are not complete C-function sizes or a complete call graph.
- Inspected the linked NVM header path at RST lines 546–671: it saves a
  three-byte generic pointer, performs the three described generic loads
  and receives the local XDATA header at `0x0529` with tag zero. Inspected
  the macro-delay path at lines 2816–2835: parameter setup, five pushes,
  multiply call at `0x87E7` and matching pops are present. These support
  bounded experiments, not an assumed linked saving.
- Recomputed all source-comparison record hashes against the retained
  4.4.0 and 4.6.0 release trees: no mismatch. The 4.6 archive hash matches
  `5fd6a93e5997ce01756868fe35e441095cfb637894a80c262514a634094973b6`.
  An independent `git diff --no-index --numstat` confirms six changed
  MCS51 files with 323 inserted and 109 deleted lines. Those totals use
  Git's diff algorithm and say nothing about emitted firmware size.
- Read representative release-source changes and option handling:
  `optimizeReturn()` accepts the default zero setting; explicit no-return
  optimization and debug handling can disable it. MCS51 is explicitly
  excluded from lospre. The new 186.f/303 rules, volatile guards and the
  changed return/parameter paths support the research report's caution
  about copying rules or adopting a compiler. The checked library-source
  equality claims match the retained hashes.

## Acceptance limits checked

Already integrated savings are identified as baseline costs. The separate
controls are not added together as a new total; the 288-byte combined saving
and 203-byte installed-candidate comparison use their stated whole-image
controls. Existing compact CIE, feature switches, DCE and outlining are not
offered again as fresh savings.

Every proposed local or compiler-rule experiment has unknown benefit until
a full controlled link. Public pointer ABI, callback roots, six layers,
sixteen macros, error behavior, both CODE windows and stack effects remain
part of acceptance. Unsupported architecture/flag suggestions are rejected
or explicitly require a separate contract.

The short-transfer account correctly says six of 42 fixtures ran before
the invalid absolute-destination case crashed the linker and produced an
empty IHX. The remaining 36 cases and the actual page-boundary mismatch are
unproved. No valid-input crash, 42-case pass or firmware saving is inferred.
Short transfers remain blocked from integration.

Source inspection, linked build results and host/CPU comparisons remain
separate from physical timing, USB interaction, durable storage, power-loss
behavior and installed firmware. No device operation follows from this review.
