# CI release time, 2026-10-26

## Measured bottleneck

[GitHub run 40268741259](https://github.com/dvino/ak820/actions/runs/40268741259)
at source `4a1fcff046da09071700b730b1db5982ce427deb` took 84 minutes 6 seconds.
The ten profiles already ran in parallel. The longest build/qualification command
was `multios`, 58 minutes 6 seconds. The serial assembly command then took
20 minutes 43 seconds. See [baseline timings](baseline-timings.json).

Each supplemental suite called `inspect()` before and after execution. Every
call replayed the entire pass30 transform chain, including compiler metadata
capture. Assembly performed three more inspections per profile. Setup and
artifact transfer accounted for seconds rather than most of this delay.

## Changes

- Reuse a successful pass30 replay only while the complete input snapshot is
  identical. Rehash contents and directory membership on every inspection;
  do not rely on timestamps. Include compiler/source/checker inputs, generated
  dependencies, external bootstrap provenance, cwd and environment.
- Keep this cache in memory. Unsupported snapshots use the original validator.
  Failures and changed-during-replay inputs cannot create successful entries.
  All other inspection, runtime, test-log and release-policy gates remain live.
- Run the first assembly inspections in up to four spawned workers. Transfer
  only each requested successful entry to the parent. The original assembler
  then checks current snapshots before reuse. Worker errors stop assembly.
- Compute each absolute-XDATA artifact path once per object. Profiling found
  182,279 repeated path conversions in one inspection; the path, duplicate,
  byte-hash, size and allocation checks are unchanged.
- Upload existing ZIP/gzip archives without a second compression pass. Record
  total and test-only elapsed time for each supplemental suite.

The parallel wrapper leaves `build_ci_release.py` and the installer host
manifest unchanged. Firmware sources, compiler flags, exact program identities,
packing results and OEM-dependent receipts are unchanged.

## Local timing

[The benchmark](inspection-benchmark.json) used two independently built
`multios` directories on the same Linux host. Its cold inspection took 22.974 s;
the next inspection returned an identical result in 2.454 s. Two cold worker
inspections took 24.273 s together. Subsequent parent inspections took 4.347 s
and performed zero additional pass30 replays. These timings measure the local
validator and process transfer, not a complete GitHub release.

The final fresh `multios` build and qualification completed successfully in
424.183 seconds (7 minutes 4 seconds), including the bootstrap, exact-image
stack checks, 28 base suites and 37 supplemental suites. The base suites ran
331 unit tests with zero skips. Shared host discovery separately passed 281
tests; overlapping test executions are not distinct tests. The emitted IHX is
still `d8467f3cdd50bf6a4bca14ab1c4c05804f7bdd9a1d55a4ef589e4fdc51fa62c0`,
with 39,682 CODE bytes and a 160/171-byte whole-program stack bound. See
[local verification](local-verification.json), [build timing](build-timing.json),
[base qualification](qualification.json), [supplemental results](profile-tests.json)
and [runtime summary](runtime-summary.json).

The final build kept sanitizers enabled. An earlier sandboxed attempt stopped
because LeakSanitizer could not inspect `/proc`; it was not counted as a pass.
An intermediate run was stopped to apply the measured XDATA-path optimization.
The final successful run had the process access needed by LeakSanitizer.

The GitHub and local timings use different hosts. The local result must not be
reported as a measured 84-minute-to-7-minute end-to-end release improvement.
A full ten-profile GitHub run and native Windows/Linux package builds have not
been rerun here. The first CI run after import must still qualify all ten
profiles and pass both native package jobs. Existing qualification-reuse rules
reject reuse across these Python source changes. No device commands were sent.
