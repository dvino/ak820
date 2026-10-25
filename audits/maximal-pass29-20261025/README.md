# Pass 29: location getters

AK820 location getters forward to existing readers, which already check bounds.
Other boards retain the wrapper checks. All 14 optional modules, base functions
and storage limits remain fixed. No device, installer, package or release action
was performed. The maximal image remains diagnostic and not installable.

| Build | CODE | Physical XRAM | Conditional stack | Main overflow |
| --- | ---: | ---: | ---: | ---: |
| Retained 28 maximal | 44,638 | 3,007 | recorded in pass 28 | 4,285 |
| Current 29 maximal | 44,601 | 3,007 | 165 / 167 | 4,248 |
| Retained 28 work | 37,392 | 2,554 | recorded in pass 28 | 0 |
| Current 29 work | 37,361 | 2,554 | 160 / 171 | 0 |

The current maximal saves 37 CODE bytes; work saves 31. The collector derives
measurements from retained build reports, MEM files, linked stack reports and
maps. It validates every reported artifact and source/toolchain input. Only
retained pass 28 `quantum/dynamic_keymap.c` may differ from the current tree;
it must match Git blob
`6c2cdc0452b664e37cd32a30b31e3e5f800c49cc:qmk-8051-ak820/quantum/dynamic_keymap.c`.
All other dependencies must match in place. These are retained baseline builds,
not newly reproduced builds. The historical pass 28 audit remains unchanged.

## Verification

From the repository root:

```sh
python3 audits/maximal-pass29-20261025/collect.py \
  --output audits/maximal-pass29-20261025/measurements.json \
  --current-output docs/maximal-current.json
python3 tests/ak820_getter_bounds/run.py
```

The collector verifies retained files and writes the requested JSON outputs,
plus a discarded temporary postlink report. It does not build firmware or
access a device. Full build artifacts, simulator runners and large logs remain
in the external workspace paths recorded in the evidence. The compact audit
alone cannot reproduce a build or CPU execution. The host runner executes the
source comparison offline; its output and exact runner/source/compiler
identities are retained in `host-regression.jsonl`.

`maximal-context.json`, `work-context.json` and their source/work reviews are
byte-identical to the retained pass 27 certificates copied through pass 28.
The collector checks current protected compiler ASM, tools, provenance and map
bindings and reruns the current image's postlink audit. It does not claim a
new certificate was generated.

## Evidence and limits

- `host-regression.jsonl`: 134,217,728 comparisons across AK820 generic C,
  translated current AK820 assembly, non-AK820 C and alternate geometry.
  Returns, read counts and ordered EEPROM addresses are compared for every
  byte tuple. Three mutants are rejected. ASan/UBSan covers the additional
  33,554,432-case AK820 generic run. A host assembly translation is not target
  CPU execution. The final suite also passes forced local GCC dispatch inside
  the pinned offline container; `host-execution-context.json` records that outer
  image and compiler identity. The runner correctly reports its own container
  field as null for this local dispatch.
- `getter-linked.json`: 2,431 exact linked getter CPU cases across eight shards.
  Actual-image ABI, source, map, emitted ASM, runner and simulator identities
  are checked. `getter-linked-SHA256SUMS` binds 102 retained external files,
  including every shard report, raw log and the earlier failed attempts. The
  installed `tests/ak820_getter_bounds/linked.py` matches the executed runner
  byte for byte. The external aggregate stays at its original absolute path;
  the test README explains the reproduction commands and paths.
  All 768 valid matrix locations, 1,536 valid encoder raw-byte cases and 127
  invalid boundary samples exercise return values and ordered reads. Cache bytes/flags, stack, canaries
  and the complete occupied CODE image must remain unchanged. Raw traces
  confirm B=0 and the ordered DPTR value at all 4,608 reader entries. Each call uses
  one primed cache page. Flash and write stopguards are active. This does not
  cover new read faults, dirty cross-page transitions, IRQs or durable storage.
- `startup.json`, `work-startup.json`, `read-hook.json`: current-image CRT and
  finite reader checks. CRT stops at main entry. Main-loop and NVM/settings
  initialization remain outside their scope.
- `linked-checks.json`: 629 RGB setter cases, 576 Combo GET cases, 48 cache-only
  updater cases, 15 IRQ orders and 256 LED selectors; 4,248 occupied CODE bytes
  at or above `0xc700` are preserved in each of 20 sessions.
- `work-irq.json`: current work-profile bounded IRQ check; all 37,361 occupied
  CODE bytes are preserved in each of 17 sessions. It does not qualify the
  released work image.
- `prototype-report.md` and `prototype-review.md`: exact retained prototype
  material. Its clean review covers the proposed getter integration, not the
  complete final pass 29 packet.

`initial-review.md` preserves the historical open finding in local host-runner
dispatch. The one-condition correction passed the final forced-local run.
The fresh independent `final-review.md` closes P2 and reports CLEAN for the
corrected source, tests, documentation and verification packet. That report
retains its original pre-integration manifest; it is copied without changes.

The pass 28 setter's 600-case CPU result remains evidence for its historical
image. It is not a new pass 29 whole-image setter result.

The conditional stack totals are 165/167 for maximal and 160/171 for work.
They include CRT entry and all distinct IRQ sources under the recorded bank,
OEM wrapper, routing and non-reentry assumptions. Complete OEM startup/IRQ and
bank contracts, the opaque writer, full configured regressions and physical
validation remain open. Maximal also exceeds main CODE by 4,248 bytes.
Source and artifact checks, host/CPU models and physical behavior are separate
levels of evidence. None of these checks proves hardware behavior or permits
installation of the diagnostic image.
