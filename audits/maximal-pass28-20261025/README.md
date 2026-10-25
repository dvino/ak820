# Pass 28: keymap buffer check

This package records one source change to the keymap buffer setter and its
offline checks. All 14 optional modules, base functions and storage limits
remain fixed. The maximal image is diagnostic and not installable. No device,
installer, package or release action was performed.

| Build | CODE | Physical XRAM | Conditional stack | Main overflow |
| --- | ---: | ---: | ---: | ---: |
| Retained 27 maximal | 44,699 | 3,007 | recorded in pass 27 | 4,346 |
| Current 28 maximal | 44,638 | 3,007 | 165 / 167 | 4,285 |
| Retained 27 work | 37,470 | 2,554 | recorded in pass 27 | 0 |
| Current 28 work | 37,392 | 2,554 | 160 / 171 | 0 |

The current maximal saves 61 CODE bytes; work saves 78. Measurements come from
retained build reports, MEM files, linked stack reports and map files. The
collector validates all report artifacts and current source/toolchain inputs.
For retained pass 27 only, the differing `quantum/dynamic_keymap.c` must match
Git blob `eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e:qmk-8051-ak820/quantum/dynamic_keymap.c`.
No other historical-source fallback is accepted. These are retained pass 27
builds, not newly reproduced baselines. The entire pass 27 audit stays unchanged.

## Repeatable verification

From the repository root:

```sh
python3 audits/maximal-pass28-20261025/collect.py \
  --output audits/maximal-pass28-20261025/measurements.json \
  --current-output docs/maximal-current.json
python3 tests/ak820_keymap_firewall/run.py
python3 tests/ak820_keymap_firewall/linked.py \
  --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume28-keymap-firewall" \
  --output /tmp/ak820-pass28-linked
```

The collector does not build firmware or access a device. It verifies the
retained files in place and writes only the requested JSON outputs, plus a
discarded temporary postlink report. It checks exact images, maps, listings,
startup evidence, host evidence hash fields, Git oracle identity and the linked
setter's immutable inputs. Large CPU logs stay outside the repository.

The refreshed forced local-GCC host suite passes 6,849,504 differential cases
with ASan/UBSan, detects
three mutants and rejects QK_BOOT alias drift. `host-regression.jsonl` uses a
single evidence object with named hash fields. Its injected EEPROM-read mock
returns `0xff` and sets a sticky flag; this does not prove write-fault handling
or durable backend behavior.

`keymap-linked.json` is the byte-identical compact result from
`/home/danil/ChatGPT/ak820-pass28-research-20261025/linked-firewall/results.json`.
Its immutable-input hashes identify the exact runner, linked image, map, build
report, source, oracle, harness and support tools. The external README records
the offline Docker command and pinned container identity. The reviewed runner is
also retained byte for byte at `tests/ak820_keymap_firewall/linked.py`; the
collector verifies equality with the original external runner. The runner checks
600 actual linked setter cases, all occupied CODE before/after, input guards,
cache flags and bytes, returned SP and stack canaries. It includes partial
pairs, unchanged writes and 88 early rejections. Only CRT to main entry runs
before calls. IRQs are disabled; one cache page with batch depth one supplies
accepted requests. Only pre-existing sticky failures are tested in this CPU
run. New read faults, dirty cross-page transitions, durable storage, flash
operations, interrupts and whole-firmware behavior are not qualified.

The first two external attempts failed parsing the final CODE dump and retain
`pass=false`; they are not PASS evidence. The earlier successful 600-case run
remains in external `attempt3-success/`. The current result adds unique
build-source and QK_BOOT alias checks and preserves all 44,638 occupied CODE
bytes. Its external logs and runner remain pinned by the compact result.

## Stack and context scope

`maximal-context.json`, `work-context.json`, `source-context-review.md` and
`work-context-review.md` are byte-identical copies from pass 27. They are prior
certificates and reviews, not newly generated pass 28 approvals. The collector
checks those certificates against the actual compiler ASM in each current
`obj_ajazz_ak820_vial` tree, toolchain, fixed map sources and absolute provenance
paths. It reruns the postlink binding audit against the actual pass 28 image,
map and listings, comparing the result with the retained build report.
Relocation requires preserving or explicitly re-establishing those original
paths and hashes; silently rewriting provenance would invalidate this check.

Main/USB/timer/LED bounds are 103/5/2/2 for maximal and 98/5/2/2 for work,
with no unresolved paths. CRT adds two bytes; three distinct wrappers reserve
17 bytes each. The conditional totals are 165/167 and 160/171. These checks
retain their valid-memory, bank, wrapper, IRQ routing and non-reentry assumptions.
They do not close OEM startup or hardware contracts.

`linked-checks.json` passes 629 RGB, 576 Combo GET and 48 cache-only updater
cases, 15 distinct-source IRQ orders and 256 LED selectors. All 4,285 occupied
CODE bytes at or above c700 remain unchanged in 20 sessions. `work-irq.json`
retains every occupied CODE byte in 17 sessions. `startup.json` and
`work-startup.json` cover CRT only to main entry. `read-hook.json` is a finite
machine-code register-preservation/no-storage-write proof with its stated
assumptions; it does not prove writer behavior or backend correctness.

`prototype-review.md` is the independent prototype review, retained unchanged.
`source-cpu-review.md` accepts the production change and linked setter proof,
and records a host-runner argument-quoting finding. The runner was corrected
and the forced local-GCC sanitizer suite passed again. `final-review.md` records
the independent CLEAN decision and closes that finding after a separate real
rerun. It covers the frozen offline packet; its listed ledger hashes identify
the snapshot before this review was integrated. This metadata-only integration
adds the exact review and regenerates the evidence ledgers. Final consistency
recheck remains separate. Prior context reviews do not approve the new source
change.

The open gates remain CODE fit, complete OEM startup/IRQ and bank contracts,
the opaque writer, full configured functional regressions and physical
validation. Neither control build replaces the release or enables installation.
