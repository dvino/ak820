# AK820 size optimization regressions

These tests extract the current production functions at execution time and compare
ordinary behavior with immutable RC4 function bodies from commit `cb9ff6ea`.
The decoder also checks the explicit compact MT/LT contract described below.

## Host semantics

From the firmware root:

```sh
python tests/ak820_optimization/run.py --output .build/optimization-host.json
```

A C11 host compiler with AddressSanitizer and UndefinedBehaviorSanitizer is
required. `--test cache`, `--test color`, `--test macro`, and `--test buffers`
select individual suites. `--source-root` can test a separate checkout.

- The action decoder is checked on all 65,536 input keycodes. MT/LT ranges
  return opaque `ACTION_NO`: the compact engine consumes these keycodes before
  ordinary dispatch. All other results match immutable RC4 except 128 LM
  right-modifier cases, which use the corrected specification. The old integer
  promotion leaked a modifier marker into the layer number. The MT/LT range
  count is asserted separately; these decoder checks do not prove tap/hold timing.
- The physical/encoder cache is checked on all coordinate byte combinations and
  all input layer bytes, with and without optional Key Override layer storage.
  Mutable keymaps cover letters, modifiers, MO, LM, TG, and consumer actions
  remapped while held; releases preserve the original keycode and the next press
  uses the replacement. Virtual Vial keys and unlock suppression are checked.
- HSV conversion is compared on all 16,777,216 HSV triples both with and without
  the CIE lookup: 33,554,432 exact RGB comparisons.
- Macro playback compares exact event/delay sequences on 196,019 cases: ASCII,
  every allowed nonzero 8-bit/16-bit operand, delay boundaries, mixed commands,
  and slot bounds. The original send-string parser is included as the reference
  path. This tests decoded playback, not NVM publication validation.
- Keyboard reports cover every byte value, all 65,536 real/weak modifier pairs,
  deterministic random reports, and repeated-report suppression. Debounce uses
  40,000 events across row-count bounds, exact expiry, restarts and timer wrap.

Fixtures are original bodies with only their top-level function names changed;
`debounce_rc4.c` also renames its two shared state variables. Compiler definitions
and mock peripherals match the current AK820 profile. These checks establish C
semantics, not the SDCC calling convention or actual hardware behavior.

## Linked 8051 instructions

Run this on the exact final candidate build, in addition to the existing
`tests/ak820_emitted/run.py` integration checks:

```sh
python tests/ak820_optimization/emitted.py \
  --build-dir .build/CANDIDATE \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51
python tests/ak820_emitted/run.py \
  --build-dir .build/CANDIDATE \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51
```

The first command resolves `_mulhi8` and its parameter from the current linked
map/listing, checks the helper bytes in the IHX, and runs all 65,536 operand pairs
on uCsim C52. Every call verifies sentinel values in R0–R7. This register check is
necessary: a preliminary helper that used R7 passed arithmetic checks but broke
its compiled HSV caller, which retained a live value in that register. The
accepted helper uses A/B/DPTR only.

The second command checks the complete compiled RGB path as well as matrix and
macro behavior. Both reports identify the tested image hash. The simulator
trampoline and scratch addresses exist only in the test process. No USB device
or real flash is accessed, and generic C52 simulation does not validate physical
USB, flash/IAP, DMA, oscillator behavior, timing or IRQ overlap.

## Exact instruction outlining

The builder retains pre-outline assembly/listings in `dce-input`, applies
`util/ak820_outline_audit.py`, and records the selected bodies, owners, call
sites and source hashes in `dce/outlining.json`. `--no-outline` provides a
same-source comparison build. The read-only audit command also accepts an
already outlined build; reapplying the transformation is rejected.

```sh
python tests/ak820_optimization/outline_unit.py
python tests/ak820_optimization/outline.py \
  --build-dir .build/CANDIDATE \
  --input-dce .build/CANDIDATE/dce-input \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --output-dir .build/CANDIDATE/outline-tests
python util/ak820_outline_audit.py \
  --build-dir .build/CANDIDATE \
  --output .build/CANDIDATE/repetition-audit.json
```

Seven synthetic gates check label boundaries, private symbol identity, excluded
hardware/non-CSEG code, forbidden operands, overlap, relocation markers and
repeated application. The linked verifier independently resolves each retained
immediate against final symbols, checks all helper bytes and every LCALL/count,
then compares an inline original body with the actual linked helper. Sixteen
states per helper cover register banks, carry/overflow and DPTR wrap. Each pair
compares all 64 KiB XRAM, 32 register-bank bytes and ACC/B/DPTR/PSW/SP. The only
permitted difference is the two temporary unused stack bytes written by LCALL;
the final SP is identical. Execution logs are compressed, with hashes retained.

The accepted bodies have no branches, calls, return, stack operations, arbitrary
direct memory/SFR/bit access, indirect IRAM, MOVC or PC-relative expression.
Architectural ACC/B/DPL/DPH and carry are explicitly whitelisted; SP/PSW are not. They
cannot nest. Relocation/register-normalized families are audit candidates only;
they are not silently substituted. The script is an instruction-semantics
check, not a model of physical IRQ timing.

## Selective callee-save ABI

```sh
python tests/ak820_optimization/callee.py \
  --build-dir .build/CANDIDATE \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --output-dir .build/CANDIDATE/callee-tests
```

This verifies all eleven audited C callees in the real IHX, using 2,674 calls
with changing R0–R7 sentinels. It checks stack restoration separately from return
values and memory effects: timers/IE restoration, all modifier and matrix-row
bytes, 1,024 pin fixtures, ROM/EEPROM cached and uncached reads, valid/invalid
updates, previous fault, rejected flush and several delay lengths. The ABI
contract is bank 0, matching application C and the OEM wrapper normalization;
arbitrary-bank entry is not claimed. No prebuilt runtime or naked assembly
function is declared callee-save.

For a negative control, run the same script against a build made with
`--no-callee-saves`. It is expected to exit nonzero. The measured isolated
baseline failed 2,159 cases across eight functions; three simple getters
already preserved the registers. This demonstrates sensitivity to register
corruption even when the ordinary functional return value remains correct.

The compiler list must be identical in every translation unit. The builder
records its selected default as `audited_callee_saves` and the complete passed
string as `compiler_extra_flags`; explicit custom `--extra-flags` are not
misrepresented as the audited list. Full feature and IRQ suites must also be
rerun because callee-save prologues change stack depth.

## Measured history

`measurements.json` records checksum-verified occupied IHX sizes, memory layout
and hashes of historical isolated checkpoints. `machine-repetitions.json`
records bodies/counts and actual same-profile before/after outlining pairs.
These checkpoints intentionally distinguish the RC4 feature set, corrected
RC5 behavior, flags and combined candidates. Intermediate failed experiments
are labelled; their size is not a release claim. The current release budget
comes from its own build report and final regression results.

`final-results.json` preserves the complete compact host/keycode/callee/MUL/
emitted/outlining results for the accepted release image, seven unit gates,
and the callee-save negative control. Each nested report has its original
SHA256; linked reports share the exact release image hash. Detailed simulator
logs remain in the recorded build paths and are not hardware evidence.
The final comment-only rebuild uses `*-v2` directories; all four corresponding
IHX/MEM pairs are byte-identical. The evidence retains original execution paths
and includes a read-only integrity rebind to the refreshed outline/source
manifest, without pretending the CPU suite was executed again.
