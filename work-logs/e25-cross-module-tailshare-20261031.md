# E25 — cross-module exact RET-tail sharing (2026-10-31)

## Summary
Experiment E25 adds an optional assembler-tree pass `util/ak820_tailshare_xmod.py`
(enabled by `--tail-share-xmod`, requires `--tail-share`) that replaces
byte-identical, RET-terminated instruction suffixes occurring in several
modules with an `ljmp` to one retained, `.globl`-exported copy. No added call
frame, no extra stack bytes, no source changes.

## Controlled A/B (isolated copy /home/agent/ak820-code-exp-25, readonly mounts,
snapshot source-unchanged evidence in .build/e25-*-meta/)
- Baseline (exact replica of combined-main recipe, profile main): stage-2
  strict interval failed `0xc700..0xc754` — reproduces the primary ledger.
- Candidate (same + `--tail-share-xmod`): stage-2 strict interval PASSED,
  `highest_address 0xc6b9` (margin 71 bytes under 0xc700).
- Pass self-verification: 26 groups, estimated 118 bytes, per-module object
  CSEG deltas verified exactly 118 bytes total.
- b1 (code-end 0xe000) endpoint: baseline 0xc922 -> candidate 0xc8ae.
- IHX: e25-xmod-b1 sha256 e31e504cededa885c3119d021f372f1c5cdb3010d33d3fbbe55dfd07a9fdcfbb;
  e25-xmod-b2 sha256 d2f20cb9f3762dc7c18170e6fbf7af83f0668f2fb41bb79a5f6a846586d371bd.

## Safety rules of the pass
- Key = exact opcode+operand spelling + byte size per instruction (same as
  ak820_tailshare eligibility, including SAFE_OPS, no control SFR/aliased
  direct RAM, hardware/IRQ modules excluded, no local numeric labels).
- Operand symbols must be defined in exactly one module and `.globl`-exported
  there; same-spelled statics (ambiguous) are excluded; registers/immediates
  allowed; 771 shared global symbols, 2 ambiguous excluded.
- A replaced source span must contain only the covered instructions and
  comments — any other text (labels, directives) rejects the site.
- One retained copy per suffix (lowest module), `ljmp` (3 bytes) elsewhere.
- Per-module object CSEG size check after re-assembly; build aborts on any
  mismatch. Report keeps `linked_saved_bytes: null`, `hardware_validated: false`.
- Canonical compiler-input contract is refused when the flag is on
  (`not args.tail_share_xmod` added to the contract condition), so a candidate
  build cannot claim the verified canonical contract.

## Notes
- Linked endpoint gain (0xc754 -> 0xc6b9) exceeds the object-level 118 bytes
  because the later short-call relaxation sees a different tree; ledger entry
  records both, no summed claims.
- Replaced source spans may swallow interleaved comment lines (the span rule
  rejects only non-comment text such as labels or directives inside a range);
  removing comments is semantically inert.
- No source files were modified; the pass rewrites only a separate assembler
  tree inside the build directory.
