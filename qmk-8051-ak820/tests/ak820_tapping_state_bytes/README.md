# One byte per tapping source

This bounded experiment replaces the private five-bit packed array with one
masked byte per source. All five independent flags remain available together.
The setter still masks every input with 31. Source numbering, accepted calls,
cancellation, pending decisions, modifier/layer ownership and One Shot logic
are unchanged. Both encoder directions retain separate source IDs 128 and 129.
No public ABI or persistent storage format changes.

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping_state_bytes/run.py
python3 qmk-8051-ak820/tests/ak820_tapping/run.py --oneshot --space-cadet --output /tmp/tapping-bytes-host.json
python3 qmk-8051-ak820/tests/ak820_tapping_state_bytes/measure.py --build-dir /path/to/resume24-fixed-led --sdcc /path/to/sdcc-4.6.0/bin/sdcc
```

`packed_oracle.c` preserves the original accessors verbatim. The focused host
fixture extracts the production accessors and compares every read with that
oracle and a separate logical byte model. It writes all 256 setter values at
every source for 32 nonuniform surrounding patterns. Every write checks all
130 sources, including adjacent and unrelated canaries. Another 100000
interleaved writes exercise flag combinations, cancellation transitions,
One Shot flag pairs, read/modify/write and masked arbitrary input. UBSan and
array-bounds instrumentation run in the host compiler. The test performs
151444930 source comparisons over 1164960 writes, plus the initial reads.
Only IDs 0 through 129 are valid: NONE (255) and other invalid IDs are excluded
by existing callers. Neither representation supports invalid accessor IDs.
The byte getter relies on zero initialization and writes through the masked
setter. The private array has no other production writer and its address does
not escape. Arbitrary memory corruption is outside this equivalence claim.

## Size evidence

`size-results.json` records the maximal pass24 preprocessed input hash, exact
SDCC binary hash, relevant saved compiler flags and object areas. Only the
real tapping translation unit is compiled. Preprocessor line directives are
removed, and only the array/accessor region is substituted for the candidate.
No firmware image is linked or built by this experiment.

| Object area | Packed | Byte | Change |
|---|---:|---:|---:|
| CSEG | 2064 | 1768 | -296 |
| DSEG | 0 | 0 | 0 |
| OSEG | 4 | 0 | -4 |
| XSEG | 114 | 160 | +46 |

The array grows from 82 to 130 bytes (+48); two fewer accessor parameter/spill
bytes reduce the raw TU XSEG increase to 46. Object OSEG is overlay storage,
so its change does not establish final linked internal-RAM savings. Applied
to 111 remaining XRAM bytes, the conservative array-only estimate leaves 63.
The 296-byte object CODE reduction precedes the build's assembly transforms,
short calls, dead-code elimination, placement and stack analysis. Only a new
linked image can establish its final CODE/XRAM and stack bound.

The earlier rejected five-plane representation mentioned in
`docs/MAXIMUM-FUNCTIONALITY-STATUS.md` is a different experiment. It did not
measure this direct byte representation.

## Behavior evidence and limits

`state-results.json` records the exhaustive comparison and input hashes.
`host-results.json` records the existing production host pipeline with both
One Shot and Space Cadet enabled, including 156 retained-QMK differential
traces. These host tests cover existing ownership, cancellation, timing and
encoder cases; they do not prove hardware timing or interrupt behavior.

The first `--negative-controls` run found a stale textual matcher: the
`lost-release` mutation still expected direct array access. The matcher now
uses `source_state_get(id)`, as the production source does. A fresh run passed
the positive host and 156 QMK traces, and rejected all 13 deliberately broken
variants. The fixture change affects only its mutation target.
Independent component review and the bounded exact-image 26b checks are
recorded in the [current audit](../../../audits/maximal-continuation-20261025/README.md).
Whole-firmware and hardware qualification remain open. These component results
do not by themselves qualify a full build or device behavior.
