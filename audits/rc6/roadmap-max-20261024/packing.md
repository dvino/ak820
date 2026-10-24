# More compact exact outlining

The builder now tries eight fixed selection strategies and keeps the greatest
nominal byte saving. The original greedy strategy remains one candidate. Ties
prefer fewer replacement sites, then fewer helpers. This is a bounded search,
not a claim that the result is the smallest possible program.

## Complete-image comparison

The comparison uses the unchanged firmware from `48ce5fa`; only the outliner
differs. It precedes the protocol and Space Cadet source changes.

| Result | Original selection | New selection |
| --- | ---: | ---: |
| Complete application CODE | 39,814 | 39,146 |
| Main-window CODE | 38,010 | 37,342 |
| Low-window CODE | 1,804 | 1,804 |
| Helpers | 155 | 194 |
| Replacement sites | 1,608 | 1,384 |
| Nominal saving from unoutlined input | 2,575 | 3,243 |

The full linked image saves **668 bytes** and uses 224 fewer helper call sites.
XRAM remains 2,612 bytes; the allocated stack remains 160 bytes. Allocation is
not a worst-case runtime bound. Exact hashes are in
[the comparison](packing/comparison.json); the accepted image, MAP, MEM, build
report and complete selection manifest are retained in [packing](packing/).
Combined source optimizations must be measured again: their costs need not add
to this isolated result.

## Selection and safety scope

Each strategy ranks a positive candidate by an exact rational score:
`saving^4 * body_bytes^body_power / sites^site_power`. Negative body powers go
in the denominator. The fixed exponent pairs are `(0,0)`, `(4,2)`, `(2,2)`,
`(0,2)`, `(-1,4)`, `(-2,4)`, `(-3,4)` and `(-4,4)`. Scores do not use floating
point. The chosen strategy and all eight measured objectives are recorded in
the [manifest](packing/outlining.json).

For a fixed exact sequence, removing occupied intervals cannot increase its
maximum count of disjoint matches. With `saving = (body_bytes - 3) * sites -
body_bytes - 1` and the fixed site exponents at most four, each positive score
increases with the match count. A cached priority is therefore an upper bound;
the heap refreshes a candidate before selecting it. This retains overlaps that
can become usable after another selection.

The instruction whitelist, module/function scope, CSEG restriction, 200-helper
cap and 40-instruction maximum are unchanged. Helpers contain no calls and
cannot nest. A helper call still adds two live stack bytes. Experiments with
larger helper/span limits did not improve the best measured result. Broader
direct-memory and low-section transformations were not retained.

## Verification

All 13 outliner unit tests pass. The independent exhaustive reference rebuilds
candidate windows after each selection. Across 100 deterministic inputs and
all eight strategies, its selected bodies, locations and order match the
cached implementation: 800 differential comparisons.

The linked CPU differential test passed all **194 helpers in 3,104 state
cases**. It compares all 32 register-bank IRAM bytes, SP, DPTR, PSW, A, B and
the full XRAM state against the original straight-line instructions. The two
return-address stack cells are outside the compared IRAM range. A separate
integrity phase checks all 1,384 replacements, input hashes, helper bodies,
relocation immediates and call counts. [CPU results](packing/cpu.json) bind the exact image and manifest and
retain per-helper log hashes.

Every final profile runs the same exact-image integrity check and its base and
feature-specific CPU regressions. The complete helper state sweep above is for
the isolated packing image, not a claim that every final profile has run that
same sweep. Integrity checks alone execute no CPU instructions.

No device was opened. Neither these checks nor fewer static call sites prove
physical timing, interrupt latency, USB transfers, DMA behavior or the global
stack bound. Release packaging remains blocked.

## Independent review

Independent code review checked the monotone-score argument, exact ordering,
unchanged eligibility and helper limits, original-strategy fallback, and unit
test agreement. Full documentation and evidence review is recorded with the
integration package before its commit.
