# Faster outlining, 2026-10-24

The outliner now enumerates instruction sequences once and refreshes cached
candidates only when they reach the front of a priority queue. The selection
rules, allowed instructions, two-byte stack cost per helper call and helper limit are
unchanged.

The previous implementation searched every sequence again after each chosen
helper. On the unchanged `48ce5fa` standard build, selection took 30.500 seconds
before this change and 0.398 seconds afterwards. Including parsing, the stage
took 30.766 and 0.667 seconds. These are single local elapsed-time measurements,
not a full-build benchmark. See [measurements](outline-benchmark.json).

All 155 selected helpers, their bodies, replacement locations and order match
the previous result. A fresh full link reproduced the application SHA256
`004bf2cbda40f9c90ab92e0ee6b6a29bc2098e39d5ee8bc6d0da5df638f2565a`
and 39,814 CODE bytes. The firmware behavior and memory use are unchanged.

## Checks and review

The 13 outliner tests pass. The new test compares cached selection with an
independent exhaustive implementation across 100 deterministic inputs, varying
repeated sequences, overlaps, helper limits and minimum savings.

An independent reviewer approved the code, tests, documentation and evidence. The
review checked that equal sequences have equal interval lengths, so removing
used intervals cannot increase the maximum number of disjoint occurrences.
This makes each cached score an upper bound. The queue refresh preserves the
previous savings, size and key tie order. All raw matches remain available,
including overlaps that become usable after an earlier selection.

No device was opened. This change supplies no new stack, interrupt or physical
behavior qualification. The existing release restrictions remain in force.
