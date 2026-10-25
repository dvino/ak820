# Pass 30: default keymaps

The optional `--compress-default-keymap` build flag compresses the two compiled
default layers. It is off by default. All 14 optional modules, base functions
and storage limits remain fixed. No device, installer, package or release action
was performed. The maximal image remains diagnostic and not installable.

| Fresh same-source build | CODE | Physical XRAM | Conditional stack | Main overflow |
| --- | ---: | ---: | ---: | ---: |
| Maximal, option off | 44,601 | 3,007 | recorded in its exact stack report | 4,248 |
| Maximal, option on | 44,400 | 3,010 | 165 / 167 | 4,047 |
| Work, option off | 37,361 | 2,554 | recorded in its exact stack report | 0 |
| Work, option on | 37,170 | 2,557 | 160 / 171 | 0 |

Maximal saves 201 linked CODE bytes; work saves 191. Both use three more physical
XRAM bytes. The option-off IHX files exactly match the respective pass 29 images.
These are fresh current-source control builds, not historical-source substitutes.
The collector verifies all four build artifacts and source/toolchain manifests
in place. The historical pass 29 audit is unchanged.

## Generation and build commands

Use the existing configured build invocation with `--compress-default-keymap`
to enable this opt-in reduction. Keep the other flags, profile, compiler and
feature/storage settings fixed when comparing it with the option-off control.
`build-report.json` records actual commands and logs for each build. Their
absolute build paths and hashes are in `measurements.json`.

The introspection compiler command is wrapped. The current SDCC compiler first
resolves the original 512-byte keymap and `[16,8,2,2,0,1]` metadata. Strict literal
parsing produces 64 class bytes, 114 payload bytes and 32 row offsets. A final
compile uses those 210 bytes and the decoder. The bootstrap ASM is never linked.
The collector independently checks bootstrap data, exact generated include,
final ASM, linked table addresses/bytes, removal of the original allocation,
both compiler dependency closures, compiler/generator identities and command
hashes. The generator is included in the build input manifest. Encoder and LED
data are byte-identical in both paired builds. Six dynamic layers, 16-bit NVM
and wire values and reset behavior remain the source contracts.

From the repository root:

```sh
python3 audits/maximal-pass30-20261025/collect.py \
  --output audits/maximal-pass30-20261025/measurements.json \
  --current-output docs/maximal-current.json
python3 tests/ak820_default_keymap/test_generator.py
```

The collector verifies retained files and writes the requested JSON outputs,
plus discarded temporary postlink reports. It does not build firmware or access
a device. Large artifacts, CPU logs and runners remain at their original
absolute external paths. `external-evidence.json` and the decoder's original
`decoder-linked-SHA256SUMS` bind them. The compact audit alone cannot reproduce
a full build or CPU execution. Reproduction commands for compiler and decoder
checks are in `generation-fix.md`, `host-checks.json` and
`decoder-linked-README.md`. The two rejected extra passes retain their own
commands in `extra-pass1-event.md` and `extra-pass2-protocol.md`.

## Verification

- `host-checks.json` and three logs: seven generator tests and all 16,777,216
  uint8 coordinate triples pass. The actual integrated getter body is checked
  with native ASan/UBSan against current compiler-resolved defaults. Commands,
  immutable offline container identity, current source/tool hashes and native
  compiler identity are retained. This is host execution, not target CPU execution.
- `translation-unit-checks.json`: actual SDCC clean and incremental compile,
  poisoned include replacement, original option-off defaults, unchanged
  encoder/LED bytes, indirect extraction-phase rejection and changed final-only
  generated header rejection. Successful current outputs and the independent
  actual compiler rerun remain at their recorded external paths. Earlier
  intentionally invalidated runs do not qualify the packet.
- `decoder-linked.json`: 275 calls per exact image, 550 CPU invocations across
  four shards. All 256 defaults and 19 invalid boundary cases pass, including
  absent default layers 2–5 used by six-layer reset. Return words, stack and
  canaries pass; every occupied CODE byte is preserved before/after each shard.
  Actual emitted ABI, tables, sources, runner, simulator, ASM/RST, map and
  manifests are bound. Encoder and LED bytes match the option-off control.
  Raw layer count is static-only evidence: DCE removed the function from both
  linked images. No call to a nonexistent entry is claimed.
- The 256 valid default lookups add 42,260 instructions and 706,464 generic C52
  ticks in total. Per-call deltas are 14–318 instructions and 276–5,256 ticks.
  This is only the reset/default lookup component. It is not complete reset,
  CH555 timing, an 11 ms comparison or ordinary keypress latency. Dynamic
  keypress reads retain the NVM path. The exploratory decoder attempt is
  excluded from accepted aggregation; the original external manifest retains it.
- `startup.json`, `work-startup.json`, `read-hook.json`: current-image CRT and
  finite reader checks. CRT stops at main entry; main-loop and complete
  NVM/settings initialization are outside their scope. The reader proof covers
  45 reachable instructions and rejects seven mutants.
- `linked-checks.json`: 629 RGB setter cases, 576 Combo GET cases, 48 cache-only
  updater cases, 15 IRQ orders and 256 LED selectors; 4,047 occupied CODE bytes
  at or above `0xc700` are preserved in each of 20 sessions.
- `work-irq.json`: current work-profile bounded IRQ check; all 37,170 occupied
  CODE bytes are preserved in each of 17 sessions. It does not qualify a released
  work image.

`maximal-context.json`, `work-context.json` and their source/work reviews remain
byte-identical to the pass 27 certificates retained through pass 29. Current
protected compiler ASM, tools, provenance and map bindings are revalidated;
actual-image postlink checks run afresh. No new context certificate is claimed.

`prototype-review.md` covers the native prototype. `initial-review.md` preserves
the first two P2 integration findings. `generation-fix.md` records corrections;
`implementation-review.md` independently closes those findings for source and
the actual translation unit. The fresh independent `final-review.md` reports
CLEAN for the frozen implementation, tests, documentation and recorded evidence;
both initial P2 findings are closed. Its 45-file manifest identifies the reviewed
pre-integration tree. The report is copied byte-for-byte; its hashes precede
this metadata-only review closure and JSON evidence-list refresh.

## Exactly two additional passes

`extra-pass1-event.json` records one event-chain candidate. All 12,288 bounded
baseline/candidate traces match and three mutants are rejected. Standalone
component CSEG grows from 565 to 627 bytes; component RAM remains unchanged.
Even ideal removal of its entire 58-byte wrapper leaves four bytes of growth.
This is a component estimate, not a full-image linker result. The candidate
was rejected without integration or a full build. Modeled leaf contracts do
not qualify all fourteen features or full stack/IRQ behavior.

`extra-pass2-protocol.json` records no eligible substantial variant. No patch,
component compile or full build was produced. It authenticates six current
protocol/backend sources and historical image 29 listings. Three specific
repeated loops total 42 instruction bytes; ideal sharing could remove at most
28 of those bytes before added costs. This bound covers those loops only,
not every possible protocol rewrite. No saving is claimed.

The integrated saving is 201 bytes, below the requested approximate 0.5 KiB
checkpoint. Both additional passes are complete; the recorded decision is to
pause after final packet review and handoff. The complete-feature objective
remains incomplete. This is not a claim of a global compression minimum.

## Open gates

The conditional stack totals are 165/167 for maximal and 160/171 for work.
They include CRT entry and all distinct IRQ sources under the recorded bank,
OEM wrapper, routing and non-reentry assumptions. Complete OEM startup/IRQ and
bank contracts, the opaque writer, full configured regressions and physical
validation remain open. Maximal also exceeds main CODE by 4,047 bytes.
Source/artifact checks, host/CPU models and physical behavior are separate
levels of evidence. These checks do not permit installation of this diagnostic
image and do not prove durable storage or hardware behavior.
