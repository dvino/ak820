# Integration review before profile qualification

## Scope

This package integrates multi-strategy exact outlining, all eight combinations
of the three bounded optional features, compiler-flag identity checks for inline
Space Cadet, exact-image outline integrity, VialRGB and runtime-stack checks,
and combined NKRO/One Shot/Space Cadet cancellation regressions. English and
Russian guides, status and roadmap describe the same implemented scope.

The original feature and protocol changes have their own independent review
closures in [Space Cadet](space-cadet.md), [protocol sizing](protocol-size.md)
and [runtime stack analysis](../runtime-stack-20261024/report.md).

## Prequalification evidence

- All eight fresh profile images pass the configurator's exact compiler,
  source, feature, CODE and RAM checks; [build identities](profile-builds.json).
- The 18 configurator gate tests, 13 outliner tests and 17 stack analyzer tests
  pass. Runtime negative controls reject a different image, MAP, analyzer or
  decoder, forged approval, missing roots and inconsistent exit status.
- The isolated packing image passes 194 helper CPU comparisons across 3,104
  states. All 1,384 replacement sites pass integrity checks; [packing](packing.md).
- The complete combined image passes 79 tapping/input cases, 15 One Shot cases
  and seven NKRO cases. Its tests cover queued, held and consuming One Shot
  state and pending/held Space Cadet cancellation by mode switches. Results
  bind the image in [combined-probe](combined-probe/).
- The combined image's 199 helpers and 1,428 replacements pass structural
  integrity. This check does not execute helper CPU states.
- Its runtime analyzer returns diagnostic status 2: main and LED roots remain
  unresolved; timer and USB callback bounds are two and six bytes respectively.
  These callback figures exclude hardware/OEM entry and do not qualify the
  whole program or interrupt nesting.
- Documentation checks find 41 public documents and no failures.

Full profile regression qualification follows on a frozen source revision.
No preliminary linked build or partial stack result approves a release.

## Findings and closure

The independent code reviewer checked exact rational priorities, the monotone
heap argument, original-strategy fallback, deterministic ties and unchanged
outlining eligibility. No blocking code issue was found. The runtime report
now also binds the decoder source after a review suggestion; its negative
controls pass.

Documentation review corrected three misleading descriptions: the QMK Settings
plan preserves current Combo offsets while adding a new versioned record;
Auto Shift portability requires explicit C switch labels, not letter-case
conversion; and helper CPU coverage is distinct from all-call-site integrity.
User guides describe behavior while detailed test evidence stays in audits.

The final independent review approved this package for the source freeze
commit with no blocking findings. It reran exact configurator inspection on
all eight images, the gate tests and documentation checks, and verified the
retained packing and combined-image report hashes and case counts. Verbatim
compiler reports retain their original whitespace and are checked by hashes.
Final regression and archive acceptance have separate records; release and
device qualification remain open.
