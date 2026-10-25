# Whole-program compression

The development target is one `maximal` image containing all 14 optional modules
and all existing base functions. OS indicators, six layers, sixteen saved Vial
macros, the 8192-byte macro store, eight Combos, eight Tap Dance entries and eight
Key Overrides remain part of the target. The nine release profiles remain the
control. The implementation plan is [here](MAXIMUM-FUNCTIONALITY-PLAN.md).

## Measurements

All builds use pinned SDCC 4.6.0. Oversized diagnostic builds measure the complete
feature union; they are not device images and are excluded from installation.
CODE windows, DMA, loader and persistent-storage boundaries remain fixed.

| Candidate | Occupied CODE | Physical XRAM use | State |
| --- | ---: | ---: | --- |
| Original full union, original short calls | 48261 | 3230 / 3072 | CODE and RAM overflow |
| Experiment 1 | 48430 | 3117 / 3072 | Oversized diagnostic |
| Experiment 2 | 48326 | 3127 / 3072 | Oversized diagnostic |
| Experiment 3 | 48004 | 3020 / 3072 | RAM fits; main CODE exceeds limit by 7651 bytes |
| Experiment 6 | 47837 | 3020 / 3072 | Shared VIA buffer parsing; main overflow 7484 bytes |
| Rebuild 5 | 48004 | 3020 / 3072 | Same layout; corrected native packet alignment |
| Experiment 4, rejected | 48095 | 3029 / 3072 | More CODE and smaller stack capacity |
| Experiment 8b | 46965 | 3005 / 3072 | Direct actions and byte predicates in EP0; main overflow 6612 |
| Experiment 9 | 46758 | 3005 / 3072 | Opt-in tail sharing; main overflow 6405 |
| Rebuild 10 | 46758 | 3005 / 3072 | Same image bytes; unique artifact manifest |
| Experiment 11 | 46659 | 3000 / 3072 | Register-preserving NVM reads |
| Experiment 12 | 46570 | 3000 / 3072 | Opt-in register-save trimming |
| Experiment 13 | 46536 | 3000 / 3072 | Helper cap 400 |
| Experiment 14 | 46496 | 2998 / 3072 | Register-preserving settings word reads |
| Experiment 15 | 46438 | 2997 / 3072 | Typed HSV input |
| Experiment 16 | 46156 | 2997 / 3072 | More foreground modules in exact outlining |
| Experiment 17 | 46132 | 2989 / 3072 | Event snapshot in registers |
| Experiment 18, diagnostic only | 45888 | 2980 / 3072 | Shared read/write selector; foreground overestimate 129 |
| Experiment 19 | 45881 | 2980 / 3072 | Separate read/write paths, shared address helper |
| Experiment 20, historical | 45499 | 2980 / 3072 | Opt-in private parameter-copy removal; before IRAM overlay |
| Experiment 21c | 45499 | 2980 / 3072 | IRAM overlay: 20 private bytes from four owners share seven bytes |
| Experiment 22, current diagnostic | 45461 | 2976 / 3072 | Separate read-block kernel; IRAM overlay disabled |

Experiment 3 reserves 64 bytes at XRAM 0x400 for the aligned flash stage and
allocates 2956 ordinary bytes from 0x440. Both areas count toward 3072. Separate
compiler allocation metadata proves the fixed stage extent without adding debug
labels to optimizer input.

The current linked image is recorded in [maximal-current.json](maximal-current.json).
Experiment 22 allocates 2912 ordinary XRAM bytes plus the 64-byte flash stage:
2976 of 3072. Foreground/USB/timer/LED bounds are 103/5/2/2, with no unresolved
paths from these roots. The conditional combined stack estimate is 165 against
156 available. IRAM overlay is disabled in this image; experiment 21c separately
measured 169 available bytes. Combining the read kernel and shared IRAM requires
a fresh context and linked proof. Main CODE still exceeds its boundary by 5108
bytes. Full configured regressions remain blocked by CODE and the incomplete
OEM startup/IRQ contract.

## Prepared changes and evidence

The branch contains an exact guarded split-ROM-switch recognizer with 33 focused
analyzer tests, broader foreground short calls with 20 tests, source-state and
Tap Dance map packing, typed settings operations, shared CRC, shared TD/KO
storage, and direct target-only packet adapters. CRC machine code occupies 52
bytes compared with 160 for the C candidate in experiment 1. Its emitted 8051
harness passed 1024 differential buffer cases, ABI and canary checks; the native
reference passed 16777216 state-byte transitions and 25600 random buffers.

Packet adapters passed 516096 differential cases in an alignment-one target
model and 516096 in the native fallback. SDCC separately confirmed the actual
record types have alignment one. This is not full firmware CPU execution.
Settings, storage, macro power-cut and packing checks are targeted host tests;
they do not establish physical behavior or full combined-feature regression.

Typed logical keycode reads and a single lookup per press were measured in
experiment 4. The candidate added 91 CODE bytes, retained foreground bound 103
and reduced stack capacity to 150. Both transformations were reverted. Protocol
and event dispatch restructuring remain in scope. No feature removal is
accepted as compression. Work is incomplete until a legal complete image passes
all relevant proofs, regressions and independent review.

## Rejected or deferred candidates

- Scanning Tap Dance slots instead of retaining the map loses newest-slot
  selection with same-source reentrant dances.
- A five-plane tapping representation used more RAM and code in the measured
  image; the five-bit representation was retained.
- Nibble packing the upstream origin-layer cache produced no target saving:
  that cache is absent from the compact Key Override image.
- Direct-DATA outlining is deferred until relocation and nonvolatile-object
  metadata can prove its safety. Prelink offsets are not final DATA addresses.

Experiment 20 saves 2762 CODE bytes and 250 XRAM bytes against the original
full-union control. These are complete-image totals, not sums of isolated
function estimates. Protocol restructuring, real-engine rule bytecode and
compiler tail sharing were evaluated separately. Real Leader/KO domain bytecode
added 130 CODE bytes; narrower tables added 101. Both were rejected. Tail sharing
first saved 191 bytes in an older standalone object experiment. The conservative
pass saved 147 object bytes in experiment 9; after linking and short-call
placement that complete image was 207 bytes smaller than 8b. Experiment 20
records 163 object bytes removed by its tail-sharing pass. The
pass is experimental and opt-in; no extra return frame is added.

Experiment 6 merges buffer-command parsing and 32-bit reply formatting without
adding a helper frame. A native ASan/UBSan oracle comparison passed 524288
packets: all command IDs and buffer size bytes, randomized other bytes, unlock
and write-failure states. Native/native-target ABI differences remain outside
this check. Independent source review found no correctness issue; its test
coverage wording finding was corrected.

Experiment 7 duplicated the scalar NVM read fast path inside the register-saving
wrapper. It passed 67108864 native value/read-count cases but added 47 CODE bytes
without lowering foreground stack 103 or increasing stack capacity 154. It was
reverted.

Experiment 8b directly dispatches retained keycode actions under a strict board
configuration guard, keeping the raw action API and other configurations. It
also uses byte predicates and three cached BIT values in USB setup. Together
they reduce complete-image CODE by 872 and XRAM by 15 bytes. Direct-action native
comparison passed 524288 ordered traces; USB fixture and 131072 differential IRQ
traces passed. The scalar USB predicates separately passed all 65536 words in
emitted SDCC/s51 code. These are component checks, not full-image CPU execution.
The first build exposed a missing forward declaration for register_mouse; the
correct declaration was added and 8b compiled. The current-source native action
comparison was rerun successfully after that correction.

Independent source review found no code blocker in action, USB or tail sharing.
The stale action-source hash finding was resolved by rerunning the current source
and recording image identities separately. Actual BIT allocation/IRQ ownership,
all-stack qualification, full regressions and combined code/docs final review
remain required. Internet-derived candidates and applicability checks are recorded
in [optimization research](OPTIMIZATION-RESEARCH.md).

The first tail-share manifest repeated final ASM entries also retained by short
calls. Rebuild 10 records each resolved artifact once. Its 556 artifact records
have unique paths and matching hashes; strict linked inventory now passes. The
linked IHX bytes match experiment 9. This repairs evidence bookkeeping, not
firmware behavior.

No device commands, flashing, installer replacement or publication occurred.

## Register and argument experiments

NVM scalar reads now use a target-only naked implementation preserving R0–R7.
The public generic-address entry tail-dispatches to it. Range, cache/fault reads
and CODE reads remain unchanged; native builds keep the C body. The source has
two private DPTR stack bytes on cache hits; outlining may insert additional
helper frames, counted by exact-image analysis. This saves 99 linked CODE and
five XRAM bytes versus rebuild 10 and lowers foreground bound from 105 to 103.
The emitted component passed 82688 cases per scalar entry and 216 compiled C
block-reader calls, including IDATA/XDATA outputs and canaries.

The experimental `--trim-register-saves` pass proves finite local CFGs,
transitive clobbers and balanced private frames from assembled instructions.
It rejects unknown effects, bank writes, stack aliases, indirect IRAM and unknown
or recursive calls. Seven current sites remove 22 save/restore pairs: 88 object
bytes, 89 complete-image bytes after placement. A real CPU fixture checks
registers, return values, a branch and a private frame; 14 focused tests include
real assembler adversaries. Independent source review found no blocker. Relocated
symbol identity still relies on the fresh assembler and retained relocation
records; no stronger claim is made.

The helper cap 400 saves another 34 linked bytes, without changing instruction
eligibility or allowing nested helpers. The settings word reader preserves all
R registers and avoids a parameter spill; it saves 40 linked CODE and two XRAM
bytes. Its emitted helper passed 65536 values and 327680 actual C getter calls.
Independent review found no ABI defect; the native fallback and host validation
model remain unchanged. CRC comments now correctly list all arithmetic PSW flags
as scratch. These changes do not qualify the oversized image for runtime tests.

## Color input

Experiment 15 passes a typed XDATA HSV pointer to the private target conversion
entry. Direct mode reads its existing array entry without an aggregate copy;
generated effects use their existing local color. Public aggregate color APIs
and other configurations remain available. Grayscale conversion still avoids
reading hue. OS indication, CIE, effects and output order are unchanged.

The complete image saves 58 CODE bytes and one XRAM byte against experiment 14.
Strict linked inventory passes. Exact application roots remain 103/5/2/2 with
no unresolved transfer, but the combined stack estimate still exceeds capacity
by 11 bytes and startup/IRQ wrapper qualification remains open.

Native ASan/UBSan comparison passed all 33554432 HSV/CIE combinations for both
core and public wrapper, in native and pointer models. The actual RGB harness
and full-CIE/no-CIE/non-board comparisons passed. Emitted SDCC/s51 callers
passed 4480 samples through typed and aggregate APIs with canaries. These are
component checks; the target renderer, DMA timing and complete image were not
executed. Independent source review found an unnecessary grayscale hue read;
that read was moved past the grayscale return and all component checks rerun.
The frozen experiment and scripts are retained in the external private evidence
directory under `ak820-rgb-pointer`.

## Foreground outlining coverage

Experiment 16 admits the remaining foreground Auto Shift, Dynamic Macro,
Leader, saved-macro, One Shot, OS waveform and indicator modules to the existing
exact outliner. Instruction eligibility is unchanged: no branches, calls, stack,
SFR, indirect IRAM or PC-relative loads enter a helper. USB/timer/LED callbacks
remain excluded. USB lifecycle code clears the OS mode byte directly and does
not call the waveform helpers. Indicator behavior remains unchanged.

The full image saves 282 CODE bytes against experiment 15 with unchanged RAM
and application stack bounds. There are 219 helpers and 1672 replacement sites.
All helper instructions and immediate relocations match the original input
after following actual stack-neutral tail jumps; every LCALL/ACALL replacement
was checked against final addresses. Strict linked inventory passes.

The older integrity checker expected each helper to remain contiguous and each
call to remain long. Tail sharing and short-call relaxation invalidate that
representation, so the checker now follows actual LJMP/AJMP/SJMP chains and
checks ACALL page boundaries. Calls, changed instructions, cycles and missing
bytes fail. Six adversarial byte fixtures pass alongside the 13 outliner gate
tests. This checks transformation integrity, not CPU execution, interrupt
latency, startup wrappers or physical behavior. Independent review remains
required before committing this packet.

## Event snapshot

Experiment 17 replaces the target large-model event adapter's two aggregate
copies with six register loads followed by six stores into the existing
`action_exec` parameter. All input bytes are read before any store, preserving
overlap. The public aggregate API and C fallback remain. The tail jump adds
no frame; current wrapper callers are in other translation units. A future
internal caller must revisit SDCC naked-function clobber inference.

The full image saves 24 CODE bytes and eight XRAM bytes against experiment 16.
Strict linked inventory passes; application stack roots remain 103/5/2/2 with
no unresolved transfer. The source hash differs from experiment 16; each build
keeps its own input identities. Resource and full qualification gates remain.

The actual adapter bodies, real headers and pinned compiler flags passed 65535
patterned XDATA snapshots and 2816 overlapping-parameter cases in s51. The
reference is the previous C adapter. The initial overlap fixture let the oracle
change candidate input; it was corrected to freeze expected output and restore
input before the second call, then rerun. Mock action bodies capture parameters;
these checks do not execute the real action engines, nested callbacks or IRQs.
Independent review found no present semantic or ABI blocker under the pinned
large-model/static-parameter/bank-zero contract. Exact-image runtime acceptance
is still absent. The external packet is `ak820-action-event`.

## Catalog control on the current source

`work-control-17` rebuilds the existing work feature selection with the same
source and optimization switches as experiment 17, within physical CODE
windows. It uses 38874 occupied CODE bytes and 2472 ordinary XRAM bytes plus
the 64-byte flash stage. Main's highest address is 0xc138. Application roots
are 98/5/2/2, without unresolved transfers; the conservative startup/three-IRQ
estimate is 160 against 157 available stack bytes. This control therefore
does not qualify for runtime or full configured regressions. Its legal CODE
placement does not replace the complete fourteen-module target. Existing
installer/catalog artifacts and installed firmware remain unchanged.

## Shared keymap word kernel, diagnostic experiment 18

The opt-in `AK820_KEYMAP_WORDS_ASM=yes` option supplies the four key/encoder
get/set APIs from a separate target-only assembly translation unit. Both
coordinate-helper APIs remain in source; ordinary DCE removes unused bodies.
Geometry and ABI guards preserve the six-layer/16-row/8-column/one-encoder
layout and EEPROM addresses. Native byte order, invalid-input results and
backend failure handling are unchanged in the component comparison.

The kernel relies on the existing audited EEPROM hooks preserving R0-R7.
The builder emits a guarded ABI assertion only with both hooks in its common
callee-saves list and rejects incompatible public-API/stack/bank conventions.
Independent review checked the actual hook objects and found no blocker to
a diagnostic integration. The no-frame kernel passed 5760 exact ordered-I/O
comparisons; seven actual EEPROM/NVM/CRC cases passed all-register canaries
with hardware flash calls mocked. Neither check qualifies flash persistence
or reentry into the real non-reentrant backend.

The complete experimental image occupies 45888 CODE bytes and 2916+64=2980
XRAM bytes. Stack capacity rises to 156. Its highest main address is 0xdc9e,
5535 bytes beyond the limit. Strict byte inventory passes. However the current
analyzer reports foreground 129, USB 5, timer 2 and LED 2. The common kernel
contains a read/write selector whose value is not tracked by that analyzer, so
a getter's bound includes the backend write closure. This is an identified
control-flow overapproximation, not a proved runtime stack increase; it cannot
be waived. Experiment 19 replaces that selector with separate read/write entries, as
described below. No target-specific analyzer whitelist was added. Full
qualification remains open.

## Checkpoint 19 and resumed work

Checkpoint 19 separated keymap read/write entries and restored foreground bound
103 without an analyzer exception. Its 5760 ordered I/O comparisons, three ABI
policy tests and exact linked-byte checks passed. A fresh independent review now
accepts the hook register checker within its stated bank, writer-stack and IRQ
assumptions. Those assumptions remain separate from hardware qualification.

## Experiment 20: remove private parameter copies

The default-off `--trim-parameter-spills` pass removes a store/reload sequence
only for an unescaped, nonvolatile compiler-private formal. It requires
`--parameter-spills-context FILE`. Typed metadata and assembly come from the
same retained preprocessed input and compiler invocation. The pass checks
source, ABI, opcodes, reserved memory and the complete application IRQ closures.
A new exact-image audit must pass after linking. Its approval covers that
bounded transformation, not stack capacity or hardware interrupt behavior.

The maximal build selects 82 prefixes and saves 607 bytes in individual objects.
After outlining and short-call placement, the complete image saves **382 CODE
bytes** against 19: 45499 bytes, highest address 0xdb19, main overflow 5146.
XRAM remains 2916+64=2980 and stack capacity 156. Application paths remain
103/5/2/2 without unknown transfers; CRT analysis retains a two-byte main-entry
frame. The conditional combined estimate remains 165, nine bytes above capacity.

All 82 prefixes passed 1312 before/after s51 state comparisons covering every
register bank, full PSW, ABI/canaries and page crossing. Eleven metadata/guard
tests pass and are retained under `tests/ak820_parameter_spills`. Exact linked
integrity checks pass for 211 helpers and 1559 substitutions. Fresh independent
reviews cover the installed pass and positive new-image postlink evidence.
These are component/static results; full configured regressions remain blocked.

A same-source `work` control shrinks from 38874 to 38505 CODE bytes with the
pass enabled, saving 369. XRAM stays 2472+64=2536; paths stay 98/5/2/2 and
capacity stays 157. Its conditional estimate 160 still exceeds capacity.
Both controls remain diagnostic evidence, not replacements for released images.

External evidence is retained under
`ak-configurator-local-artifacts/maximal-optimization-20261025/resume-pass20/`:
`work-comparison.json`, `inventory20.json`, `startup20.json`, `cpu/`, `hooks20/`,
`outline-integrity/` and independent review reports. Image identities and
resource totals are in `maximal-current.json` and the exact build report.

At checkpoint 20, IRAM allocation was recomputed for image 19: four noninterfering foreground
owners have 19 private bytes that could share seven, a potential 12-byte saving.
That proposal passed independent review for component assembly only; no linked
stack improvement had been measured at that stage. The later exact-image result
is recorded under experiment 21c; current image 22 disables that overlay.
Complete OEM entry and VS11K28A interrupt routing/non-reentry evidence remain
open. All fourteen modules remain enabled. No full regressions, device actions,
commit, packaging or publication were performed in this resumed packet.

## Experiment 21c: IRAM overlay diagnostic

The fresh oversized image `.build/maximal-overlay-21c-oversized/ajazz_ak820_vial.ihx`
has SHA256 `b4035dcde630ce8ae43ce8b7cc6b286f5a84b872e48805973d3df0cde46b2dbe`;
its MAP SHA256 is `84d54869ed5d4a789b62028ae59481e2d976236979fd94573798c7e2555824f3`.
The build report identifies builder SHA256
`458e94d9b7f35860237e807190a506553bfd0ea00b28c526e2b35611dae9e86a`.
The image contains all 14 optional modules. CODE remains 45,499 bytes, with a
5,146-byte main-window overflow. XRAM is 2916 ordinary bytes plus a 64-byte
flash stage. The overlay combines 20 private bytes from four foreground function owners
into a seven-byte shared pool, freeing 13 bytes. The owners are
`ak820_eeprom_update_block_xdata` (7 bytes), `fast_set_leds` (4),
`vialrgb_get_value` (4) and `dynamic_keymap_set_buffer` (5); they span three
modules. The exact-image link proof covers 407 ordinary relocations and 17
library operand relocations; the full 118-byte `__memcpy` member was verified
from retained relocatable input.

The exact linked application roots remain 103/5/2/2, with no unresolved path.
The overlay capacity is 169 bytes. The conditional combined estimate is 165,
leaving four bytes only under the separate OEM wrapper, routing and nesting
assumptions. Startup evidence covers the two-byte pre-main control-stack bound
and two-byte main-entry frame, with interrupt enables unchanged until main; it
does not establish the incoming OEM interrupt state. The CPU model passed 15
IRQ orderings and all 256 LED selector values. It uses a fixture and does not
prove foreground owner behavior, hardware timing or device behavior.

Independent review passed bounded diagnostic integration of the exact image.
It checked 2,487 build artifacts, 21 proof inputs, 636 reference artifacts and
22 library-integration files. The explicit inventory selection reports 45,499 occupied bytes and 79 listings;
independent review passed with no blocking findings. Its SHA256 is
`da289ae21cec81dce6d84a206a1bf1fa8b833435e321ed1c67368492a1c8a2fc`. The
inventory utility changed after the firmware build and does not change the linked
image. A separate CPU comparison passed 23 paired cases for the four foreground owners.
It checked cache/LED effects, live-memory canaries, SP and unchanged CODE.
NVM writes stayed in a primed cache; durable flash writes were not exercised.
RGB replies 0x41/0x42 were checked by differential comparison only.
The independent CPU review passed within this component scope.

The image remains diagnostic-only and cannot be installed. The full exact-image
OEM startup/IRQ routing and non-reentry contract, opaque-writer and application
bank gates, complete functional regressions and physical validation remain
open. Full configured regressions are blocked by the CODE overflow and IRQ
contract. No device commands, firmware package, commit or publication occurred.

## Experiment 22: separate read-block kernel

The default-off `--nvm-read-block-asm` option selects a separate 8051 translation
unit for XDATA block reads through the existing scalar EEPROM hook. The C
fallback and public API remain available. The exact integrated sources match
the independently reviewed package. Existing component CPU comparisons cover
82688 cases per scalar entry and 436 block calls; they are component evidence,
not execution of the complete linked image.

The fresh oversized image uses 45461 CODE bytes, 38 fewer than experiment 20,
and 2912 ordinary XRAM bytes, four fewer. A same-source option-off full build
has not been run. Stack bounds remain 103/5/2/2 and capacity 156. Exact startup
and linked inventory checks pass. The actual EEPROM hooks retain their reviewed
conditional R0–R7 preservation; four mutated implementations are rejected.
The conditional writer, bank and IRQ assumptions remain open.

IRAM overlay is disabled: the image-20 allocation certificate cannot admit the
changed generated code. A fresh image-22 context has been prepared externally;
its component path integration, independent review and full relink remain
separate work. No full configured regressions, device actions, package, commit
or publication were performed. The approximate work-volume estimate is 40%; it
does not measure firmware readiness.
