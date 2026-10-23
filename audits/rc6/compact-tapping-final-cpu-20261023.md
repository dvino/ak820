# Final linked tapping CPU run — 2026-10-23

## First run: failed fixture assumption

The first complete 65-case linked CPU run did not pass. The first 64 cases completed,
and their saved simulator logs match all expected memory snapshots and keyboard
and extra-report traces. The 65th case, `macro-cancel-stops-stream`, exceeded
the runner's 45-second `s51` timeout. It produced no completed simulator log.
The timeout is a failure; this run does not establish the final macro-cancel
case or an overall pass. No retry or fixture change was made.

The suite ran an existing linked SDCC 8051 image in the generic uCsim C52
emulator. It did not build firmware or access USB or a keyboard.

## Command and inputs

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/emitted.py \
  --build-dir qmk-8051-ak820/.build/compact-modtap-send-mask-20261023 \
  --s51 /home/danil/Documents/git/ak820/toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir qmk-8051-ak820/.build/compact-modtap-send-mask-cpu-20261023
```

The output directory contains 64 completed `.log` files and their simulator
scripts. The timed-out case has a simulator script but no completed log or
`results.json`. The completed logs were checked offline against the runner's
expected snapshots and traces; this did not start another simulator process.

## Measurements and limits

All 64 completed cases passed the offline comparison. The highest recorded
stack pointer was 150, from initial SP 101, or 49 bytes exercised against 154
bytes available. Maximum observed event clock count was 225,276 in
`boundary-199-65500`; the two-task full-matrix scan reached 9,622,704 clocks.
The largest completed macro clock sample was 9,275,640 in
`macro-256-down-modifier`. These are emulator instruction-clock counts and
include the offline call trampoline where applicable. They do not establish
physical latency or interrupt-nesting stack use.

The first macro-cancel fixture replaced the simulated `_eeconfig_init` entry
with `RET`, assuming that EE_CLR used it. Later diagnosis showed that this
image instead enters EEPROM-disable and reset; the patched entry was unused.
The timed-out run provides no completed evidence for that case. EEPROM reset,
durable storage, power-fail handling, physical matrix and encoder behavior,
USB, IRQ overlap and physical timing remain untested.

## Artifact identity

| Input | SHA-256 |
|---|---|
| Linked image `ajazz_ak820_vial.ihx` | `24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655` |
| Linked map `ajazz_ak820_vial.map` | `e457bacda3ede08ba62a3f047d6c04deb773742de5137e26f9ffda4b63b8f478` |
| Tapping source `ak820_tapping.c` | `beaa2a96510fcaada9685d3b7fe46346a8bd85c17edecfd7a5126a907dcfa313` |
| CPU runner `emitted.py` | `f33f23b60412427ac03077765b0be8a6a39b588346e8a215fa34627f4de75055` |
| Linked runner support `ak820_emitted/run.py` | `27aa969d76917a0a77bd0d9ef3deb94b74d20c16fca6dabc9979d074ded89eb9` |
| Pinned simulator `s51` | `61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd` |

This result describes only the source and linked artifact named above. It does
not establish which firmware is installed on any keyboard.

## Corrected complete run

The failed assumption was diagnosed and corrected in the CPU fixture only;
see [diagnosis](compact-tapping-macro-cancel-diagnosis-20261023.md) and
[independent hook review](compact-tapping-macro-cancel-hook-review-20261023.md).
The image remains the exact IHX above. A fresh complete run with output in
`.build/compact-modtap-send-mask-cpu-final-20261023` passed **all 65 cases**.
Retained machine report: [65-case result](compact-tapping-final-cpu-20261023.json).
Runner SHA256: `a7c27ad81a158c4703ab55a56b3dddd6478a9508e9bab028174be32e96aa7e03`.

The corrected cancellation case redirects one simulated macro DOWN call through
a guarded register-preserving hook. It calls the original `register_code`, then
the real `clear_keyboard`, and resumes the actual interpreter. All eight memory
checks, five keyboard sends and two consumer callbacks match. The next macro
command is not executed. This proves the cancellation primitive under that
injection; it does not execute or validate EEPROM/reset behavior.

Across the complete run, peak SP is 150 from initial 101: 49 bytes exercised
against 154 bytes allocated. The hook case peaks at SP 136 including its
register saves. IRQ overlap remains unmodelled. Earlier 64-case timing samples
remain emulator evidence; no instruction-clock count establishes physical
latency. No device operation was performed.

## Latest image after Grave Escape ownership correction

A broader qualification run later found a separate Grave Escape source defect.
The earlier 65-case pass above remains valid for its named scope/image but did
not cover that interaction. The corrected latest IHX is
`d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`.
A fresh complete 65-case run passed on that image, retained as
[latest CPU result](compact-tapping-grave-fixed-cpu-20261024.json).
Initial SP is 98, peak SP 147: 49 tested bytes against capacity 157.
Separate linked suites also passed 33 feature cases, 10 unlock cases and 16
Tri Layer cases. Their source/fixture corrections are reviewed in
`compact-tapping-gesc-fix-review-20261023.md`. Complete 26-suite qualification
and final artifact approval remain separate. No device operation occurred.
