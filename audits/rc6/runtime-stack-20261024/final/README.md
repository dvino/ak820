# Final stack and interrupt qualification

All **17 named profiles and 19 variants** pass from clean frozen firmware and
test source `39b6e227dd72302b9945cb73531f0b2493028591`. Builds ran in three
separate checkouts. Each variant closed its exact foreground, CRT and IRQ bound
before running 28 base suites and 273 base unit tests without skips, followed
by its required feature suites. Sanitizer checks were enabled without override.

The matrix includes the two profiles requiring short calls and two additional
short-call builds of `full` and `full-mouse-auto-shift`. The machine-readable
[summary](summary.json) includes image and record hashes. Every row links its
complete record, reports, image, map, memory allocation and raw build archive.

| Variant | CODE | Free main / low | XRAM | Main | CRT | IRQ | Bound / capacity | Margin | Feature suites |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [standard](standard/record.json) | 38,077 | 2339 / 84 | 2,589 | 98 | 2 | 61 | 161 / 162 | 1 | 16 |
| [nkro](nkro/record.json) | 38,216 | 2200 / 84 | 2,594 | 98 | 2 | 61 | 161 / 162 | 1 | 18 |
| [one-shot](one-shot/record.json) | 38,670 | 1814 / 16 | 2,599 | 97 | 2 | 61 | 160 / 162 | 2 | 18 |
| [nkro-one-shot](nkro-one-shot/record.json) | 38,809 | 1675 / 16 | 2,604 | 97 | 2 | 61 | 160 / 162 | 2 | 20 |
| [space-cadet](space-cadet/record.json) | 38,193 | 2223 / 84 | 2,592 | 98 | 2 | 61 | 161 / 166 | 5 | 17 |
| [nkro-space-cadet](nkro-space-cadet/record.json) | 38,332 | 2084 / 84 | 2,597 | 98 | 2 | 61 | 161 / 166 | 5 | 19 |
| [one-shot-space-cadet](one-shot-space-cadet/record.json) | 38,785 | 1699 / 16 | 2,602 | 97 | 2 | 61 | 160 / 166 | 6 | 18 |
| [full](full/record.json) | 38,924 | 1560 / 16 | 2,607 | 97 | 2 | 61 | 160 / 166 | 6 | 20 |
| [full-gui-lock](full-gui-lock/record.json) | 39,159 | 1325 / 16 | 2,610 | 101 | 2 | 61 | 164 / 166 | 2 | 22 |
| [full-ctrl-gui](full-ctrl-gui/record.json) | 39,302 | 1182 / 16 | 2,610 | 101 | 2 | 61 | 164 / 166 | 2 | 25 |
| [full-dynamic-macro-gui](full-dynamic-macro-gui/record.json) | 40,279 | 205 / 16 | 2,696 | 101 | 2 | 61 | 164 / 165 | 1 | 24 |
| [full-mouse-auto-shift-gui --short-calls](full-mouse-auto-shift-gui-short/record.json) | 40,391 | 93 / 16 | 2,657 | 101 | 2 | 61 | 164 / 166 | 2 | 26 |
| [full-auto-shift-dynamic-macro --short-calls](full-auto-shift-dynamic-macro-short/record.json) | 40,424 | 60 / 16 | 2,710 | 97 | 2 | 61 | 160 / 165 | 5 | 24 |
| [full-dynamic-macro](full-dynamic-macro/record.json) | 40,044 | 440 / 16 | 2,693 | 97 | 2 | 61 | 160 / 165 | 5 | 22 |
| [full-mouse](full-mouse/record.json) | 39,774 | 710 / 16 | 2,637 | 97 | 2 | 61 | 160 / 166 | 6 | 22 |
| [full-auto-shift](full-auto-shift/record.json) | 39,537 | 947 / 16 | 2,624 | 97 | 2 | 61 | 160 / 166 | 6 | 22 |
| [full-mouse-auto-shift](full-mouse-auto-shift/record.json) | 40,387 | 97 / 16 | 2,654 | 97 | 2 | 61 | 160 / 166 | 6 | 24 |
| [full --short-calls](full-short/record.json) | 38,676 | 1808 / 16 | 2,607 | 97 | 2 | 61 | 160 / 166 | 6 | 20 |
| [full-mouse-auto-shift --short-calls](full-mouse-auto-shift-short/record.json) | 40,168 | 316 / 16 | 2,654 | 97 | 2 | 61 | 160 / 166 | 6 | 24 |

The minimum stack margin is **1 byte**. This is a conservative complete
control-stack allowance under the stated premises, not an observed maximum.
The combined calculation includes all three distinct interrupt sources; every
image also passes all 15 ordered nonempty IRQ nests and 256 LED selector values.
Seven linked delay cases verify register preservation and stack balance.
The new Ctrl/GUI profile additionally passes its exhaustive host/feature-flag
checks and all eight linked interaction cases.

Across the matrix, 532 base suite runs and
5187 base unit-test executions pass, plus
401 supplemental suite runs. Repeated tests across images
are executions, not distinct test cases. Each profile's exact suite plan and
source/log hashes are retained.

## Recheck retained evidence

Run from the repository root:

```sh
python3 audits/rc6/runtime-stack-20261024/verify_matrix.py
```

The independent validator checks frozen Git blobs, exact image/report/log hashes,
required suites and all raw archive contents. To repeat compilation and CPU
execution, use [Build profiles](../../../../docs/BUILD-PROFILES.md) with fresh
build directories. The pinned compiler and simulator are identified in each
build and runtime report.

## Scope

The bound begins at CRT entry with IE and IE_EX zero, valid memory accesses,
bank-0 SDCC calls and MCS-51 in-service/RETI semantics. It does not establish
physical VS11 timing, USB behavior or pre-CRT trial erase. Source and reports
remain development evidence: release approval and hardware validation are
false, and no physical device commands were sent. The published alpha.3 image,
release safety policy and settings schema remain unchanged.

See the parent [technical report](../README.md) for the six former capacity
failures, delay correction, independent review and finding closure.
