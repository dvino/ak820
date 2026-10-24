# Compact input features and further size reduction

This work starts at upstream `38ad0133278463b4662dcb81eecaa17c9cd93b9b`.
The published and installed alpha.3 image is unchanged. All images discussed
here are offline development builds; no physical device commands were issued.

## Scope

The source preserves six layers, sixteen Vial macros, eight two-key Combos,
compact tap-hold, encoder maps, media keys, NKRO reports, Caps Word, Repeat,
Alternate Repeat, Grave Escape, Tri Layer, RGB effects and RAM-only VialRGB
Direct. The NVM schema remains `0x082002`, with Combo storage at offset `0x658`.

The work adds compact Mouse Keys and compact Auto Shift. Their user-visible
behavior and limits are described in [Mouse Keys](../../../docs/COMPACT-MOUSE-KEYS.md)
and [Auto Shift](../../../docs/COMPACT_AUTOSHIFT.md). New images must establish
their own resource, stack and interrupt evidence; alpha.3 approval does not
transfer to them.

## Verification boundary

Host C tests and exact linked uCsim C52 scenarios use supplied peripheral state.
They do not establish physical USB, flash, timing, DMA or interrupt overlap.
Ordinary key regressions explicitly send `AS_OFF` through the production key
path when Auto Shift is compiled. Dedicated Auto Shift scenarios retain its
actual enabled power-on default. Both modes are recorded in fixture results.

AddressSanitizer and UndefinedBehaviorSanitizer run with
`ASAN_OPTIONS=detect_leaks=0`: LeakSanitizer cannot inspect process task state
in this execution environment. Leak detection is not claimed.

## Implementation

The core changes specialize only the pinned AK820 path. Internal positions use
a 16-bit row/column value instead of repeated structure arguments. Private
XDATA views avoid generic-pointer access helpers where every actual producer
has been checked in the emitted assembly. Public QMK entry points remain
available. The configured RGB namespace is dispatched by its low byte after
checking the high byte. Repeat's adjacent layer-control exclusions use one
interval with One Shot enabled and two otherwise, with compile-time boundary
checks.

Eight matrix, encoder and Vial call sites share the event argument setup. A
named six-byte snapshot avoids an observed SDCC extra-dereference defect. The
wrapper tail-jumps into the unchanged public `action_exec` body. The size
saving costs eight XRAM bytes and an additional six-byte copy per event;
physical scan timing has not been measured.

The compact RGB implementation calls its fixed board driver directly. The
signed public LED-index check remains before conversion to an eight-bit index,
and the board entry still checks its bounds. The existing interrupt mask around
live DMA writes is unchanged. The removed indirect table had no selectable
alternative driver in this build.

These source changes reduce the old `full` feature set from 40,043 to 39,145
occupied CODE bytes, a saving of 898 bytes before optional short transfers.
Individual isolated savings are not additive because outlining and compiler
allocation depend on the complete image. See the
[core measurements](../core-compact-20261024.md) for the isolated steps and
their tradeoffs.

### Compact Mouse Keys

Cursor directions, five buttons, vertical and horizontal scrolling share the
existing HID endpoint. Cursor movement uses eight report units per axis every
20 ms; scrolling uses one unit every 80 ms. A new direction attempts immediate
movement. Opposing directions cancel; diagonals are not normalized. Operating
system pointer scaling remains outside the firmware.

There is no relative-motion queue or catch-up burst. Busy endpoints discard
movement; the latest desired button state is retried until accepted, including
release and clear. Acceleration keys and buttons six through eight remain
unsupported. No new persistent record is introduced.

### Compact Auto Shift

The engine starts enabled and owns one physical basic key at a time. A release
before 175 ms emits an ordinary tap; reaching the threshold adds an owned left
Shift and holds the original key until release. Another press before the
threshold first emits the pending key without Shift. Existing modifier and
One Shot state bypasses the delay. Caps Word and Repeat see the emitted key;
Repeat retains the automatically added Shift.

The scope is direct physical letters, digits and the documented punctuation
ranges. Combo inputs, including failed Combo fallback, Combo outputs, tap-hold
outputs, encoders, macros and generated Repeat actions bypass Auto Shift.
There is one deferred owner, and Shift affects the entire keyboard report while
that owner remains held. `AS_ON`, `AS_OFF` and `AS_TOGG` change only the session.
Changing a mapping does not change the pending press's release keycode.

### Optional short transfers

`--short-calls` is off by default. It reassembles a conservative set of foreground
`LCALL`/`LJMP` sites as `ACALL`/`AJMP`, then links and decodes their actual final
targets. The 2 KiB page is calculated from PC + 2. Invalid sites are permanently
returned to long instructions. Every iteration starts from immutable
post-outline input; the final link uses the original CODE and XRAM bounds.
Diagnostic wide links cannot become accepted firmware.

The combined profile's 40,642-byte preimage becomes 40,403 bytes: 239 shortened
transfers, with 12 of the initial 251 candidates restored after relocation.
The final main window has 81 trailing bytes and the low window has 16. Those
windows are separate; their free bytes cannot be treated as one contiguous pool.

The proof checks exact source edits, final listing/IHX instruction bytes,
unchanged instruction opcode and width, fixed operand bytes, all represented
direct and relative edges, and uniform movement of computed-jump or PC-relative
sections. NoICE symbols resolve names that ASlink truncates in MAP files.
Hardware modules, outline helpers and replacements, inline color assembly,
computed-dispatch functions and complex or literal transfer targets are
excluded from selection. The [short-call report](../short-calls-20261024.md)
describes the scope and independent review findings.

## Final measurements

All eleven named profiles pass offline qualification. `full` is also checked
with `--short-calls`, giving twelve exact final variants. Each passes 28 base
suites and 273 unit tests without skips. Supplemental counts differ by feature;
One Shot's host run also covers Space Cadet when both are selected.

| Profile | Short calls | CODE | Main trailing free | Low trailing free | Allocated XRAM | Stack capacity | Supplemental suites |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `standard` | no | 38,297 | 2,119 | 84 | 2,620 | 159 | 14 |
| `nkro` | no | 38,436 | 1,980 | 84 | 2,625 | 159 | 16 |
| `one-shot` | no | 38,889 | 1,595 | 16 | 2,630 | 159 | 16 |
| `nkro-one-shot` | no | 39,028 | 1,456 | 16 | 2,635 | 159 | 18 |
| `space-cadet` | no | 38,415 | 2,001 | 84 | 2,623 | 163 | 15 |
| `nkro-space-cadet` | no | 38,554 | 1,862 | 84 | 2,628 | 163 | 17 |
| `one-shot-space-cadet` | no | 39,006 | 1,478 | 16 | 2,633 | 163 | 16 |
| `full` | no | 39,145 | 1,339 | 16 | 2,638 | 163 | 18 |
| `full` | yes | 38,907 | 1,577 | 16 | 2,638 | 163 | 18 |
| `full-mouse` | no | 40,029 | 455 | 16 | 2,670 | 163 | 20 |
| `full-auto-shift` | no | 39,758 | 726 | 16 | 2,655 | 163 | 20 |
| `full-mouse-auto-shift` | yes | 40,403 | 81 | 16 | 2,687 | 163 | 22 |

XRAM capacity is 3,072 bytes; the fixed 512-byte DMA reservation is separate.
Stack capacity is allocation, not a runtime bound. CODE free columns show the
trailing space of each window; five internal alignment bytes in the main
window are not included. The windows cannot be combined.

Against alpha.3's 40,043 CODE bytes, the same `full` functions use 39,145 bytes
with the default build and 38,907 with short calls: savings of 898 and 1,136
bytes. Adding both new functions yields 40,403 bytes, only 360 bytes more than
alpha.3, with 2,687 allocated XRAM bytes and 163 bytes of stack capacity.
The combined image's IHX SHA256 is
`8873ebe29cea93673f44fa5c20adf8f5c372a73c70f1151da32b7c67671aad85`.
All twelve exact identities and report hashes are in [matrix.json](matrix.json).

## Offline qualification

The final matrix uses the pinned SDCC 4.6.0 compiler and its C52 simulator.
Builds run sequentially inside each of three independent worktrees. The test
runner and all firmware/tool/test sources are frozen for the final runs.
The final per-image measurements and exact identities are in [matrix.json](matrix.json).

Every profile must pass the unchanged 28-suite base qualification contract.
Supplemental suites bind the selected features and include short-call unit
controls even when the transform is off. The supplemental contract rejects a
missing, duplicate, failed, skipped or empty short-call unit run. The old CI
authorization and exact release-safety pins remain unchanged.

Core host differentials compare 33,554,432 position/layer/unlock cases,
67,108,864 RGB cases across both trigger modes, and 134,217,728 Repeat cases
with One Shot on and off. These are exhaustive comparisons of the relevant
extracted functions, not that many independent whole-firmware scenarios.
Each complete image also exercises 280 event-copy ABI cases. The new Mouse
suite has 21 linked scenarios. Auto Shift has 25 scenarios, plus two simultaneous
Mouse/Auto Shift scenarios when both features are compiled.

The exact emitted suites cover matrix/Fn behavior, macro recursion, RGB and
DMA index bounds, and suspend/resume. The transport suite covers busy endpoint
release retry, latest pending state, configuration, reset and suspend guards.
Existing suites continue to exercise remapping, both encoder directions,
Combos, tap-hold, One Shot, Space Cadet, NKRO, VialRGB and guarded-erase faults.

### Corrections retained during integration

The first simultaneous movement test used physical position `(1,4)`, which the
matrix mask excludes. It was corrected to the populated `(6,4)` position;
all 27 Auto Shift scenarios then passed on the unchanged combined image.

An initial runner entry looked for a nonexistent short-call `run.py`. Replacing
it with discovery exposed the existing exact 28-suite CI contract, which
correctly rejected a 29th base suite. The final integration restores the base
runner byte-for-byte and requires the new tests in each profile's supplemental
plan. Empty and skipped supplemental runs have negative controls. The final
runs start after those corrections; earlier stopped or failed aggregate runs
are not counted as passes.

## Research not incorporated

An exact mixed-integer selection over the existing outlining candidates improved
nominal savings by only 38 bytes. A new SciPy/HiGHS build dependency was not added.
Raising the helper cap did not improve the greedy result. Moving selected RGB
state into scarce internal RAM could save CODE but would reduce the stack
allocation, so it was not included. Broader tail merging remains unqualified.

The direct expression `action_exec(*event)` produced incorrect SDCC output
matching [bug #4054](https://sourceforge.net/p/sdcc/bugs/4054/) and
[patch #516](https://sourceforge.net/p/sdcc/patches/516/). The compiler was not
patched; the explicit snapshot is covered by the exact linked ABI checks.

The global SDCC `--acall-ajmp` option is unsuitable for this multi-page image.
The [SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf),
[Keil's linker optimization description](https://www.keil.com/support/docs/2297.htm)
and its [page-boundary warning](https://www.keil.com/support/docs/178.htm)
informed the conservative per-site relinking design. The
[QMK Mouse Keys](https://docs.qmk.fm/features/mouse_keys) and
[Auto Shift](https://docs.qmk.fm/features/auto_shift) documentation guided the
explicitly limited feature scope; these board engines do not implement every
upstream option.

## Development limits and next work

All current images remain development artifacts. The linked stack capacity is
an allocation, not a proved maximum runtime use. The analyzer leaves the
foreground path unresolved: its RGB callback recognizer covers the former
16-bit guard sequence, while the compact implementation uses a different
guarded byte dispatch. The callback roots are analyzed separately. No symbol
whitelist or old alpha.3 stack allowance is substituted for a new proof.

Release work still requires reviewed foreground and interrupt/nesting evidence
for the exact new image, its installer/settings transition and device acceptance.
The existing package gate continues to reject the changed images. No new
release tag, public package, device write, reset or bootloader command is part
of this work. The published and installed alpha.3 state is unchanged.

Tap Dance, Key Overrides, runtime QMK Settings, the remaining Magic actions,
Leader and Dynamic Macros remain in the roadmap. Their storage and event
ownership requirements are not hidden by enabling Vial controls without an
implementation.

## Retained evidence

Each `final/<variant>/` directory contains the exact configuration, build,
qualification, supplemental, runtime-stack and image reports. `raw-build.tar.gz`
retains every regular file from that completed build, including compiler output,
original and final ASM, listings, linker trials, simulator scripts and raw logs.
Its `files.json` records each original byte count, SHA256 and executable mode.
The visible report copies remain byte-for-byte identical to the raw members.
Original absolute scratch paths inside reports are provenance, not commands to
run in a different checkout.

The [frozen source snapshot](frozen-sources.json) binds the current repository
files used by the compiler or tests. The twelve external LUFA headers and the
pinned compiler remain build dependencies, as described in the build guide;
this Git archive does not vendor the toolchain or Python environment.

The [isolated experiment copies](isolated-shortcalls/files.json) retain the
short-call handoff reports, failed aggregate logs and invalid-position traces.
They remain historical failures, separate from the twelve passing final runs.
The final combined raw archive retains a complete new short-transfer proof.

[Review closure](review.md) records independent source/evidence review and
resolved findings. The [package rejection](package-rejection.json) confirms
that the unchanged release gate refuses the new combined profile; no package
or device operation was performed by that check.

From the repository root, check all retained file bytes, the complete raw
archives, report copies and current repository-source hashes with:

```sh
python3 audits/rc6/compact-next-20261024/verify_evidence.py
```

`SHA256SUMS` covers the evidence files and this verifier. The verification
result is excluded from its own checksum set. This integrity check performs
no build, firmware execution or device access. To rerun the actual tests,
make a fresh build using the command below; do not rewrite historical paths
inside saved reports and claim a new qualification.

## Reproduce

Install the pinned dependencies as described in [Build](../../../docs/BUILD.md).
From the repository root, use a fresh output directory:

```sh
ASAN_OPTIONS=detect_leaks=0 qmk-8051-ak820/.venv/bin/python tools/configure_firmware.py build \
  --profile full-mouse-auto-shift --short-calls \
  --build-dir qmk-8051-ak820/.build/full-input \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

The sanitizer setting above is specific to the documented execution environment.
On a host where LeakSanitizer works, it may be omitted. `full-mouse` and
`full-auto-shift` fit without `--short-calls`; the current combined profile
requires it. The two features do not change the saved-settings schema.
