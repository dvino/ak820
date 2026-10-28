# Main and Tap Dance compression screen

Source baseline: `origin/dev` at `038981a63aa6358f6a41a8d5a5d29966214ebdac`.
These are development measurements, not a release or hardware qualification.
The release profiles have not been changed.

## Initial controls

The main control was built with the pinned SDCC 4.6.0 toolchain using the CI
profile producer in a glibc container. Its final build reported 40,495 occupied
CODE bytes: 1,886 low and 38,609 main. The profile regression run was stopped
at the owner's request; its output is not a complete qualification.

A temporary, development-only profile enabled every current main switch plus
Tap Dance. Its first bootstrap link stopped before short-call planning: ordinary
XRAM was 3,012 bytes against the physical 3,008-byte limit. A second diagnostic
allowed XRAM through `0x1100` and CODE through `0xe000`, solely to inspect its
linked layout. It is not an installable or hardware-valid image. It retained
3,012 ordinary XRAM bytes, 40,818 main-window and 1,886 low-window occupied CODE
bytes, for 42,704 total. Highest CODE address was `0xcf9d`; this is not the
precise physical-window deficit because placement and final spill trimming can
change it. The physical main window ends at `0xc700`.

The similarly configured main bootstrap (before the context-dependent parameter
spill pass) had 40,968 occupied CODE bytes. The diagnostic adds 1,736 occupied
bytes in these bootstrap configurations, not a prediction for a legal final
image. Default-keymap compression was already enabled in both.

- Main bootstrap IHX SHA256: `c19b05a45a1c0a583a915ca9bb61f8c890571e71b487ceef58a37b489a0f2f97`.
- Expanded diagnostic IHX SHA256: `a0f06db7c0b15f0587886addad08851d0f928c2af609af110b9280536357806f`.
- Build reports and listings remain in ignored `.build/goal-bootstrap2/main`,
  `.build/goal-control2/main`, `.build/goal-tap-diagnostic` and
  `.build/goal-tap-expanded-diagnostic` under `qmk-8051-ak820/`.
- A temporary diagnostic profile definition was removed after measurement;
  no release profile or published image was changed.

Linked instruction inventory for the expanded diagnostic identifies USB setup,
raw HID dispatch, Tap Dance event handling and dynamic keymap as candidates;
listing byte counts are not independently removable savings. Exact-image stack,
physical timing and hardware behavior remain unproved for this diagnostic.

## Isolated Tap Dance map screen

The private map setter receives only indices 0..7 or the sentinel 8. Removing
redundant value masks and sharing the final write preserves the neighboring
nibble for that domain. The host fixture now checks all 128 source positions,
all nine permitted values, and the neighbor after each update. Its UBSan host
cases and shared extension storage fixtures pass, and an isolated
production-source SDCC compile passes. A same-fixture SDCC object screen changed
CSEG from `0x869` to `0x85d` bytes and left XSEG unchanged. These 12 object
bytes are not a measured linked saving, and this screen is not a firmware-image
build or qualification. Independent source review found no behavioral defect;
full linked measurements and stack/IRQ checks are still needed.

## Alternate Repeat CODE-table lookup screen

The three callers of `find_alt_keycode` pass static `const` pair tables. The
AK820/SDCC path now uses a CODE-qualified pointer and direct CODE reads instead
of generic-pointer reads. Other targets retain their existing `pgm_read_byte`
path. A temporary same-flags compile of the actual Repeat translation unit,
using the diagnostic profile's recorded compile options but no link, changed
CSEG from `0x408` to `0x3e9` bytes and XSEG from `0x38` to `0x37`; CONST stayed
`0x28`. These object deltas are not linked-image savings.

`tests/ak820_repeat/table.py` checks first-match semantics over all byte targets,
even table lengths 0..254 and eight duplicate-rich patterns in both native
preprocessor paths, then compiles the target helper with SDCC. It is included in
`tools/test_keyboard.py --host`; the runner's unit tests pass. Neither native
checks nor the isolated compile prove target CPU execution or the full profile.
Independent source review found no behavioral defect in the supported domain;
final linked, stack/IRQ and regression evidence remain open. Two pair-at-a-time lookup variants were also screened: their isolated
CSEG sizes were `0x98` and `0xa2`, versus `0x87` for the selected helper
fixture, and both used one additional XRAM byte. They were not integrated.

## VIA record pointer screen

The sole in-tree production caller forwards the board's retained key-record
pointer to `process_record_via`. A temporary screen changed its declaration and
definition to the existing `AK820_RECORD_MEM` address-space qualifier (empty on
other targets); this change was reverted to preserve the public generic-pointer
contract for external callers using other address spaces. A
same-flags isolated target-object compile, without linking, changed VIA CSEG
from `0x5c6` to `0x5bf` and XSEG from `0x14` to `0x13`; its quantum caller's
CSEG changed from `0x87e` to `0x87b`, with XSEG unchanged at `0x61`. These
object deltas do not establish a linked saving. The extracted production handler
host test checked all 65,536 keycodes in both press states; that temporary
fixture was removed with the reverted change. VIA bulk tests and runner unit
tests also passed. Target execution, full linked behavior, stack/IRQ
and final linked qualification remain open.

## RGB record pointer screen

The sole in-tree production `process_rgb` caller passes the same retained XDATA
record as VIA. A temporary screen changed its declaration and definition to
`AK820_RECORD_MEM`, empty on other targets; this change was reverted to preserve
the public generic-pointer contract. A same-flags isolated target-object compile, with no link,
changed RGB CSEG from `0x138` to `0x131` and XSEG from `0xf` to `0xe`.
Compared with the VIA-only caller screen, quantum CSEG changed from `0x87b`
to `0x878` and XSEG remained `0x61`. These object deltas are not linked-image
savings. The existing differential core fixture passed 33,554,432 cases per RGB
edge against its immutable reference; the target object compile checked the
screened declaration, definition and production caller, not target execution.
A separate Pi reviewer confirmed in-tree correctness but identified the narrowed
public API and missing repeatable target-ABI regression; the change was reverted.
Exact-image tests remain open.

Additional Repeat CPU check: `tests/ak820_repeat/cpu.py` extracts the current
production CODE lookup, compiles a standalone fixture with pinned SDCC 4.6.0,
and runs it on `s51`. It passed 1,792 cases (256 byte values × seven even table
sizes), including duplicate entries and zero-sized tables. This is not the linked
keyboard image, an interrupt/stack test, or hardware execution.

## Further candidate: Tap Dance extension buffers

A separate Pi scout identified generic Tap Dance extension getter/setter buffer
pointers which compact wrappers already cast to XDATA. Narrowing them might save
code, but would change a public address-space contract. The reset-local storage,
all compact and noncompact caller configurations, header dependencies and
external callers must first be proven safe; no change or saving is claimed.
Preserve bounds, invalid-storage zero fill, packet echo and NVM behavior.

## Independent source review

A fresh Pi reviewer checked the Tap Dance, Repeat and screened VIA changes and
their in-tree callers; no behavioral defect was found in their supported domains. The reviewer found
that the Repeat fixture printed an SDCC success even when no compiler was
provided; the message now distinguishes pass from skip. The VIA host test
cannot validate target address-space ABI. The isolated production VIA and quantum
object compilation above covered the screened declaration, definition and caller,
but that candidate was reverted; there is no dedicated automated target-ABI
regression fixture or target CPU execution. Exact-image resources, stack/IRQ and regression gates remain open.

Per the owner's subsequent instruction, do not build another changed firmware
image until profile composition is decided. Continue source-level and isolated
component compression work in the meantime.

### Further private-helper screens (no firmware link)

A read-only Pi scout proposed mouse direction normalization and settings-width
membership. Standalone SDCC 4.6.0 `-mmcs51 --model-large --opt-code-size -c`
screens plus an exhaustive native comparison found mouse direction CSEG
0x57 → 0x4c, all 256 inputs equivalent. It was **not applied**: compact Mouse
Keys is disabled in the actual expanded diagnostic profile, so this does not
help the main Tap Dance fit. For settings width, changing the existing bit-mask
membership to unsigned subtraction increased standalone CSEG 0x1c → 0x1f;
rejected. These are helper screens, not linked-image size claims.

Independent review of the Repeat simulator fixture confirmed its scope and case
count but noted that an unavailable compiler/simulator made the optional CPU
suite disappear silently from the host report. The report now explicitly records
`repeat_cpu_check` as passed, failed, or skipped; runner unit tests exercise both
the tool-present arguments and tool-absent skip. The reviewer did not execute
tests or firmware builds.

An active-profile Key Override `eligible` screen moved low/high modifier
splitting after the OR-mode early return. A synthetic SDCC 4.6.0 large-model
helper compile increased CSEG `0xbb` → `0xc0`, XSEG unchanged; rejected before
production-TU or behavioral testing. No code or interface was changed.

### Macro upload parser opcode screen

The private opcode-range condition now uses `(uint8_t)(value - 1) >= 7`
instead of `value < 1 || value > 7`; cast wrapping rejects 0 and 8–255,
and accepts exactly 1–7. With the expanded diagnostic's recorded make
options and pinned SDCC 4.6.0, separate production translation-unit compiles
(no link) changed `AK820LOW` 0x598 → 0x595 bytes; XSEG stayed 0x20. This is
three object bytes, not a linked-image saving. The first isolated compile
attempt used the wrong object target and the second lacked SDCC in PATH; both
were corrected without building a firmware image.

`tests/ak820_macro_guard/parse.py` compares return value and both state bytes
against the immutable old parser for all 16,777,216 byte-state/input cases.
`tests/ak820_macro_guard/cpu.py` separately runs all 256 opcode values through
the current parser on s51, including return and state. Both pass; the latter is
a standalone test image, not the keyboard image. Existing production VIA/NVM
host regression and 25,088 simulated upload power cuts across two erase orders
passed. The existing power-cut fixture is now repeatably invoked by
`tests/ak820_macro_guard/powercut.py` and the host runner. A Pi reviewer found no source-level defect and verified that validation,
retry and write-ordering APIs were not changed. Exact-image size, stack/IRQ,
timing and hardware power-fail behavior remain unverified.

Two further private Tap Dance variants were screened using separate production
translation-unit compiles under the expanded diagnostic's recorded options,
without linking. Inlining the packed-map getter increased CSEG 0x725 → 0x766
while reducing XSEG 0x8f → 0x8e; rejected because of the 65-byte CODE cost.
Sharing event-ID arithmetic through a function increased CSEG 0x725 → 0x74d and
XSEG 0x8f → 0x91; rejected. Both preserve the required event reread after
callbacks; neither was integrated or behavior-tested. The scout also ruled out
naively overlaying the two dynamic macro slots: both complete recordings must
coexist. A streamed settings transaction might save XRAM but is unproven and
must preserve journal operation order, failures, packet echo and startup migration.

Settings validator screen: replacing 16-bit comparisons with byte-wise range
checks for the default bound, small bound, or all bounds increased the actual
production object CSEG 0x538 → 0x560, 0x552, and 0x576 respectively; XSEG
remained 0x3d. All variants were rejected without behavior tests or linking.

An independent targeted XRAM lifetime investigation found no proved ≥4-byte
safe overlay: settings' candidate must coexist with committed current, the NVM
page cache, packet echo through USB send, Direct RGB's multi-packet stage, and
the fixed-address IAP stage; macro and Tap Dance state persist across tasks.
The fixed IAP reservation is outside ordinary linker XRAM. These are concrete
blockers, not an exhaustive impossibility proof; journal ordering and callback
lifetimes must be preserved by any redesigned transaction.

The repeatable host qualification was rerun in the pinned environment with
`--host --require-toolchain`: 25 suites, 356 unittest cases, zero skips, and both
standalone 8051 CPU checks passed; the report and per-suite logs are under
`work-logs/tap-dance-offline-tests.json` and its sibling logs directory. A Pi
review found two test-harness defects: recoverable UBSan could falsely pass and
`--require-toolchain` without `--host` could omit CPU checks. The macro power-cut
runner now uses `-fno-sanitize-recover=undefined` with an intentional UBSan
negative control; required-toolchain invocation rejects missing `--host` and
has a unit test. These are offline results, not linked-image qualification.

For this host run, SHA-256 of the touched production/test-runner files:

- `qmk-8051-ak820/keyboards/ajazz/ak820/ak820_macro.c`: `ca18dc353c34604e3e0fe3fd3214a3c38c99c522a04bfef79f57bfe6dce84c5b`
- `qmk-8051-ak820/keyboards/ajazz/ak820/ak820_tap_dance.c`: `01e6297d2ea7abccbb83bf35c4ea67350bbff841d4c2840b5b500ae9690fa647`
- `qmk-8051-ak820/quantum/repeat_key.c`: `50787ba80648242ac5c4faf4032547e380612f820f7771ed0c41e7c23b52174e`
- `tools/test_keyboard.py`: `90a67df79195abdd44627b03acfd752744a75d370409c32c7b2f97e9f4371637`
- `tools/test_keyboard_runner.py`: `54f23b4516df41d03a3a238e2364b2568147e6830da09163a2cf9b61f518f7a3`
- `work-logs/tap-dance-offline-tests.json`: `f2ef74461bbe0c48750e6f7425be06613a6e6480be05e2f94a0c1d86b968a725`

A read-only repeat-block audit of the already-outlined expanded diagnostic
reported 18 hypothetical groups with 88 nominal bytes at minimum saving 2.
Many occurrences are inside existing outline helpers; the implementation
explicitly forbids nested helpers, and call/stack, relocation, layout and actual
link effects are unproved. These are not available savings or an authorized
nested-outlining plan. No image or assembly tree was generated.

USB SETUP stall-epilogue screen: sharing all repeated `control_stall(); return;`
paths through a single label increased production-object CSEG 0x12ad → 0x130b
(+94 bytes), XSEG 0x7c and CONST 0x1a unchanged. Rejected; no behavior or IRQ
timing test was warranted and no image was linked. Large USB SETUP extent is
not itself evidence of removable bytes.

Parameter-spill investigation: the historical control pass saved 694 object
bytes, but its certificate and object figures do not apply to the current
Tap Dance combination. The historical Tap Dance listing has two apparent
immediate map-ID spill/reloads and several delayed-use parameters. The latter
cannot be deleted by relaxing a reference check: their stored values are read
later, sometimes across callback/reentrant paths. The current spill tool
correctly requires exact source/type/object identity, private storage, suffix,
IRQ/context and new-image postlink proofs. No certificate was broadened.

One control-image rejection was `as_emit`'s `_Bool` formal: its raw compiler
type is not recognized by the source-proof type filter, and its spill is also
read a second time before DPTR is discarded. Changing the private formal to
`uint8_t` in a production-object screen did not change CSEG (0x2c9) or XSEG
(0x13); rejected and restored. No behavior or image build was performed.
A separate `as_emit` branch rewrite reduced its isolated translation-unit
CSEG 0x2c9 → 0x2c7 (2 bytes), with XSEG unchanged. Not retained: tiny object
benefit is outweighed by new behavior/reentrancy testing and unknown post-pass
linked result. The original source was restored.

Default-keymap format opportunity (Pi scout): the diagnostic's generated
layout uses 64 class bytes + 114 payload bytes + 32 row offsets = 210 bytes.
In this particular source, both layers share the same KC_NO mask and layer 1
has 21 exceptional positions (12 one-byte values, nine with high byte 0x78).
A validated sorted-exception format could reduce these data to 174 bytes, at
most 36 bytes before decoder cost; a linear lookup would scan as many as 21
records instead of at most eight classes. It would require generator fallback
for arbitrary edited defaults, all-cell/bounds/reset tests and a target timing
bound. Not adopted: the maximum data-only gain is small, the required decoder
has unknown net size, and worst-case lookup timing would regress. This is not
an estimate of the image deficit or a general compression lower bound.

A 16-byte sentinel bitmap plus a first-match scan of eight existing slots
would nominally save 48 XRAM bytes, but is not equivalent. Starting from
cancel, two presses for the same source with TD(0) then TD(1), without an
intervening release, leave both slots live with the same source while the map
selects slot 1; the release clears slot 1, not slot 0. The current admission
API accepts that trace. A host regression executes this counterexample; a Pi
researcher independently reached the same conclusion. No claim is made that
normal debounced physical input generates duplicate presses. The proposed
bitmap-only substitution was rejected, preserving existing behavior; exact
base-9 packing would need target CODE/latency screens and proofs.

The Tap Dance host fixture (including the counterexample and generated-storage
cases) is now included in `--host` and uses the selected SDCC for a standalone
component compile when available. A full pinned `--host --require-toolchain`
run with this addition passed all 26 suites. The ordinary host environment has
no `cc`; the fixture was run in the pinned container instead.

A separate source-only base-9 map packing screen preserved nine representable
values per source in principle (five values per 16-bit word, 52-byte map).
The same diagnostic flags compiled production TU XSEG 0x8f → 0x83 (−12),
CSEG 0x725 → 0x81c (+247) and CONST 0 → 0x0a (+10), before runtime-library,
post-pass, final-link or timing effects. The map uses runtime 16-bit division
and multiplication on event paths. The candidate was restored and rejected:
its 257-byte object CODE/CONST growth undermines the already-overfull CODE
window, and no equivalence/CPU-time validation was performed. Thus this is a
screen, not a proposed deployed change.

A second map-format screen encoded each two nine-valued entries as a 7-bit
base-9 pair, packing 64 pairs into 56 bytes. Its 8051 same-flags object used
XSEG 0x8a instead of 0x8f (net −5 after extra temporaries), CSEG 0x837 instead
of 0x725 (+274), and CONST remained zero. The source was restored; the screen
was rejected without behavioral or timing validation because it worsens the
constrained CODE budget. These are pre-link object figures, not a firmware
measurement. The independently reviewed duplicate-source regression and its
`--host` runner integration had no source-review findings.

## Fresh diagnostic with user permission

The user explicitly permitted a local main + Tap Dance diagnostic with all
main features intact, without publishing or flashing the image. The temporary
`main-tap-dance-diagnostic` profile adds only `tap-dance` to main; it was
inserted into `util/ak820_profiles.py` for each build and restored in a
`finally` block. No release profile was changed. The initial invocation used
the wrong virtual environment and failed with `ModuleNotFoundError: No module
named 'qmk_cli'`; the retry used the existing pinned `.venv-goal-glibc`.

With pinned SDCC 4.6.0, `--compress-default-keymap`, both NVM assembly kernels,
`--keymap-words-asm`, `--trim-register-saves`, `--tail-share`,
`--outline-max-helpers 400` and `--short-calls`, the normal physical-XRAM
bootstrap failed before short-call planning with `?ASlink-Error-Insufficient
EXTERNAL RAM memory.` The linker map reports ordinary XRAM 3,011 / 3,008 bytes
at 0x0440–0x1002: three bytes over. This is a bootstrap build without the
context-dependent parameter-spill pass, and not a completed final-image fit
measurement. Its baseline CODE is not a final physical-placement result.

For diagnosis only, a second otherwise identical build widened XRAM to
0x1100 and CODE end to 0xe000. It linked with 42,667 occupied CODE bytes
(40,784 main, 1,883 low), maximum address 0xcf7b, 3,011 ordinary XRAM bytes,
498 short-call substitutions, and no parameter-spill pass. Its local IHX
SHA256 is `353825c8831eaa8a71ff0b1e25110b4116c9045d9e9c02b2e7d8db9d8d188aa8`.
Those widened bounds do not describe hardware: **the image is invalid and must
not be flashed**. The physical main CODE window ends at 0xc700, but the
address difference is not a precise final CODE deficit because placement and
qualified parameter-spill trimming can change. Neither build demonstrates a
legal image, an exact final deficit, stack/IRQ qualification or hardware
behavior. Build logs, the failed physical memory map and the expanded report
are stored in `work-logs/tap-dance-current-diagnostic/`; the image itself is
ignored locally and is not published. The control comparison, before matching
final passes, is 42,704 → 42,667 occupied CODE bytes and 3,012 → 3,011 XRAM.

Correction to the earlier 7-bit pair screen: its initial byte-offset formula
was wrong and UBSan caught `runtime error: index 56 out of bounds for type
'uint8_t [56]'`; its size figures describe a defective experiment and cannot
be used as a valid optimization result. A corrected offset passed the host
fixture, all neighbor/value checks and isolated SDCC compilation, but has not
been validated on target CPU or for timing. It remains diagnostic-only and was
restored after testing. Independent review found no issue in the fresh build
record and explicitly did not approve release or flashing.

### Temporary pair7 experiment with the context-dependent pass

To get past bootstrap XRAM without disabling a feature, a **temporary**
corrected 7-bit pair map (56 bytes rather than 64) was used only for another
diagnostic, and then source and the temporary profile were restored. The host
fixture passed all allowed-value/neighbor checks, the duplicate-source trace,
and an isolated SDCC compile. It did not prove target CPU equivalence,
timing, or hardware safety, so this representation is not adopted.

Its expanded-CODE bootstrap used the physical XRAM window and linked at 3,006
of 3,008 bytes XRAM, 42,989 occupied CODE bytes and highest 0xd0bd. Bootstrap
stack analysis produced foreground 103 bytes and IRQ roots 2/5/2 bytes, but
explicitly did not qualify the whole program; the context certificate was
then generated for this exact bootstrap. The next build used the physical CODE
and XRAM windows and the context-dependent parameter-spill pass. It selected
78 transformations, 711 object bytes, **not postlink-qualified**; its physical
XRAM remained 3,006 / 3,008 bytes. The builder rejected the linked result:
`ValueError: Linked code outside permitted interval: 0xc700..0xcebb`. This
address range is the particular rejected experimental layout, not a universal
or precise minimum savings requirement; the candidate also adds CODE and has
unmeasured event latency. Since the address check failed, later postlink
qualification did not run. No firmware image was published or flashed.
Logs, memory map, spill report and bootstrap stack report are saved alongside
the previous diagnostic evidence.
The diagnostic-only source change is retained as `pair7-diagnostic.patch`
(SHA256 `b686e9c5ccc8eab917dfe0c6b673e623bea78c4c330f6bfd9d6ce0a81edd86f1`)
for reproducibility; it is not applied to the working source. The fixture's
size assertion was temporarily adjusted for this representation during its
host screen, then restored.
A follow-up temporary UBSan fixture also checked every one of the 128 source
values after each neighbor/value update, including adjacent packed-pair
boundaries; it passed. This remains a host check, not target CPU or timing
qualification.

After restoring the temporary pair7 source, the pinned
`tools/test_keyboard.py --host --require-toolchain` run passed all 26 suites,
including both target-CPU Repeat and Macro checks. The report and individual
logs are `work-logs/tap-dance-host-current.json` and its associated logs
directory. These offline checks are not qualification of an installable image.
An independent Pi review checked the pair7 bootstrap, context provenance,
physical failure, non-qualified spill report, and restored source/profile;
it found no issues in the recorded conclusions and did not approve flashing.

### Comparable current main CODE measurement

The owner permits periodic diagnostic builds without asking, while the final
build is deferred; diagnostic images are not published or flashed. A fresh
local `main` build (no Tap Dance), pinned SDCC 4.6.0 and the same profile and
optimization settings as the `origin/dev` control, used a newly generated
bootstrap context certificate for the parameter-spill pass. Its bootstrap is
40,939 occupied CODE bytes versus 40,968 at baseline (29 bytes less). The
physical-window diagnostic after all passes is **40,464 occupied CODE bytes
versus 40,495 at baseline: 31 bytes saved (0.0766%)**. This comprises 38,581
versus 38,609 in main (28 bytes less) and 1,883 versus 1,886 in the low window
(3 bytes less). The highest occupied address is 0xc6e0 versus 0xc6fc; this is
not the same as the occupied-byte delta. Physical ordinary XRAM is 2,852 / 3,008.
The spill pass selected 74 changes and is postlink-qualified by its own audit;
this does not establish whole-program safety or hardware qualification. Both
build reports and logs are recorded in `tap-dance-current-diagnostic/`. These
are measurements of the current main without Tap Dance; its 31-byte saving must
not be confused with the cost or fit of main plus Tap Dance.

### Validator range screens after the comparable main measurement

The Key Override validator's two byte-only basic-key checks were changed to
wrapping unsigned byte ranges, keeping the original full-width predicate for
the 16-bit event key. The target production object changed CSEG 0x589 → 0x587
(2 bytes), XSEG 0x65 unchanged. The actual host validator is checked for all
256 basic-key bytes and the existing engine fixture exhausts 16-bit trigger,
replacement and layers; an added engine case checks wide keycode 0x0104
passes through despite matching the trigger's low byte. Pi review caught an
earlier incorrect attempt that used the byte predicate at the 16-bit event
call site; that attempt was fixed before acceptance, not treated as a saving.

Tap Dance's two basic/modifier ranges now use the same byte-safe arithmetic.
Its production object changed CSEG 0x725 → 0x716 (15 bytes) and XSEG
0x8f → 0x8e (1 byte). The production validator is checked against the old
predicate over all 65,536 possible 16-bit output values, and the host/storage
and isolated SDCC compile suites passed. These are object sizes only, not
linked main-plus-Tap-Dance savings, and do not establish physical fit, target
timing or hardware behavior. The already reported 31-byte main saving and
41-byte total split-window space precede these latest changes.

The corresponding Combo validator byte ranges were screened while keeping the
full-width event path unchanged. Its actual production object CSEG changed
0x431 → 0x429 (8 bytes), XSEG 0x3e unchanged. New host/UBSan checks cover
all 256 input bytes for each input, all 65,536 output keycodes, and event
0x0104 passing through. Independent Pi reviewers approved the corrected Key
Override, both Tap Dance range checks, and Combo source/test changes; these
reviews are not hardware qualification. All 26 host/toolchain suites passed,
including target-CPU Repeat and Macro checks.

A subsequent comparable physical-window `main`-without-Tap-Dance diagnostic
measured 40,453 occupied CODE bytes: **42 bytes below the initial 40,495**, and
11 below the previous 40,464. Main window usage is 38,570 of 38,617 (47 bytes
unoccupied), low window 1,883 of 1,888 (5 unoccupied); the windows are separate,
so 52 aggregate bytes are not necessarily usable as one contiguous block. The
highest CODE address is 0xc6d5, leaving 42 consecutive bytes to 0xc6ff. XRAM
is 2,852 / 3,008. The build used the pinned toolchain and the same optimization
settings with a freshly generated bootstrap context; its spill-specific audit
passed, but this is not a whole-image or hardware qualification. Its report
and logs are preserved under `tap-dance-current-diagnostic/`; no image was
published or flashed. The updated Tap Dance validator is not enabled in this
`main` measurement, so its object gains are not included in these 42 bytes.

Additional component screen: changing the compact action dispatcher's three
byte-only basic/modifier/system ranges to unsigned subtraction increased the
production object CSEG 0xc10 → 0xc17 (+7 bytes), XSEG 0x39 unchanged. It was
rejected and restored; byte-range shortening is not assumed profitable in other
compiler contexts.

Two temporary SDCC-only `__bit` recursion guards made the expanded-CODE
main+Tap Dance bootstrap fit exactly 3,008 / 3,008 XRAM and occupy 42,612 CODE
bytes. The earlier expanded diagnostic occupied 42,667 bytes but allowed XRAM
through 0x1100, so the 55-byte comparison is approximate, not a same-layout
final-image delta. The listing placed the guards in independent bits 0x17 and
0x38 with JNB/SETB/CLR. However, exact bootstrap stack analysis stopped with
`ValueError: Private guard object declaration/address contract changed: quantum/dynamic_keymap.c`:
the analyzer's proven recursion-guard contract recognizes private XRAM bools,
not bit-addressed guards. Both bit-guard source edits were reverted; bypassing
the analyzer or assuming it understands bit instructions is not acceptable.
No context certificate or physical-CODE link was produced for that variant.

A separate candidate changes only Tap Dance's local `extra` to an SDCC bit;
the recursion guards remain original byte bools. In same-flags production
objects it changes XSEG 0x8e → 0x8d, BSEG 4 → 5 bits, CSEG 0x716 → 0x709.
Its host TD/storage and isolated SDCC compile pass, but target execution,
reentry/IRQ review, whole-image accounting and stack proof remain outstanding.

`leader_waiting` changed to an independent target bit (ordinary bool retained
for host); `leader_running` and all three recursion guards remain unchanged.
Its production object XSEG 0x1b → 0x1a, BSEG 1 → 2 bits, CSEG 0x269 →
0x249. Combined with TD `extra`, a physical-XRAM/excess-CODE bootstrap reached
3,008 / 3,008 XRAM, and runtime analyzer generated a context certificate. The
subsequent normal-CODE-window diagnostic rejected addresses 0xc700–0xccfc;
its invalid temporary IHX has 42,028 occupied bytes, 1,533 outside approved
CODE windows. No invalid image was published or flashed. An earlier physical
attempt with only byte-range changes had failed at 3,010 / 3,008 XRAM.

Independent review found the linked Leader test used a synthetic alias without
copying symbol address space, reading XRAM for a bit symbol. Fixed
`qmk-8051-ak820/tests/ak820_tapping/emitted.py` to copy the source symbol's
space and received independent re-review. The physical-window main-without-TD
image's 26 linked Leader cases passed; listing showed `_leader_waiting` at
bit 0x0d and the preheld-release fixture read `bits 0xd` = 1. Isolated
production TD fixture on 8051 now checks both `extra` branches and nested
reentry (3 CPU cases); it is registered in the standard runner with explicit
pass/skip reporting and reviewed independently. Host and isolated CPU tests do
not establish TD's behavior in a linked main+TD image or IRQ/hardware safety.

Comparable physical main diagnostic without TD uses 40,415 occupied CODE
bytes (80 fewer than original 40,495; 38 fewer than the prior 40,453).
38,532 / 38,617 main-window bytes and 1,883 / 1,888 low-window bytes occupied:
85 + 5 free bytes in separate windows. Highest address 0xc6af; XRAM 2,851 /
3,008. The actual image was not flashed or released.

The first 35-suite `--host --require-toolchain --build-dir` run failed IAP,
RGB and Combo because the invocation used the default `legacy-iap` expectation
for the guarded-erase image and the manually constructed build lacked the
identity-bound `configuration-report.json`; Combo expected zero Key Overrides
instead of the image's eight and RGB refused to proceed. The first failure
report and original logs are retained separately, not rewritten as a pass.
Generated the report using the standard `configure_firmware.inspect`, then
reran with `--iap-fault-profile guarded-erase`: all 35 suites passed, 356 unit
tests, zero skipped, tested IHX/map hashes unchanged. The linked image SHA256
is `747817d1256ddc0393954f1b4ab68332c170b6a9ba8b023383c947d9c43a1628`.
Independent full-image qualification, representative hardware and main+TD CODE
fit are still open. Source and per-suite logs are retained, while simulator
traces not needed for the findings remain in the ignored build/work directory.

A source-only VIA layout-option assembly screen wrote the four packet bytes to
an SDCC little-endian `uint32_t` union, preserving all four callback bytes in
principle. Same-flags TD-enabled production `via.c` object CSEG changed 0x5c6 →
0x598 (−46 bytes), but XSEG increased 0x14 → 0x18 (+4), BSEG stayed 2 and
CONST 0. The latest TD bootstrap already fills ordinary XRAM (3,008 / 3,008),
so this variant was restored and rejected rather than trading a physical XRAM
overflow for an object-only CODE reduction. No equivalence test or firmware
image was built; object savings are not linked savings.
Passing the union member directly to the setter rather than copying it through
an additional local produced the same 0x598 CSEG / 0x18 XSEG and was also
restored; the extra four XRAM bytes did not come from the explicit copy alone.

An independent one-byte XRAM candidate changes private USB
`raw_reply_without_nvm` to `__bit`, without touching IRQ handshakes or recursion
guards. Same-flags TD-enabled isolated production object changed XSEG 0x7c →
0x7b, CSEG 0x12ad → 0x12a7 and BSEG 13 → 14 bits; CONST stayed 0x1a. The
production USB host harness passed, including original-request recovery
whitelist, persistence gate and reset scenarios. This remains an object screen,
not linked or physical validation. An attempt to invoke the separate recovery
fixture without its mandatory `--build-dir` only printed its usage and did not
run it. Awaiting independent USB-context review and an exact linked build.
Independent USB source review found no defect in the bit candidate; main-only
request lifetime and reset ownership remain unchanged. Host shim maps `__bit`
to `bool`, so target execution and exact-image stack/IRQ proofs remain open.
A VIA layout sequential-shift alternative retained XSEG 0x14 and changed CSEG
0x5c6 → 0x5c3 (−3 object bytes); it was restored because the tiny unlinked
saving does not justify changing a public-protocol path without linked and
callback equivalence tests.

A fresh USB-bit main diagnostic was built with a fresh bootstrap-derived spill
context, same pinned toolchain, profile and optimization chain as the earlier
main controls. Occupied CODE 40,408 (38,525 main, 1,883 low): 87 bytes less
than original 40,495, and 7 less than previous 40,415. Free space is 92 main
and 5 low bytes, separate windows; highest CODE 0xc6a8. XRAM 2,850 / 3,008,
one byte less than preceding 2,851. This is main WITHOUT Tap Dance. The image
IHX SHA256 is ace7932c5dd6c7f60b904cadf613bc71764b29d1099b102d10395660cb4298b0.
The full host+target offline suite passes all 35 suites with required toolchain
and guarded-erase profile, unchanged image/map, zero skipped; exact-image
runtime check passes with 161 / 179 stack bytes, 18 bytes margin and qualified
foreground/startup/IRQ bound. First suite invocation failed RGB and Combo
because the manually built image lacked configuration-report.json; `inspect`
prints the report instead of creating it, so it was extracted as JSON and bound
to this image, then the full suite reran successfully. The first failure and
its logs are kept separately, not rewritten. No device was opened, flashed,
or validated; no release or installer/settings transition is approved. The
main+TD invalid 1,533-outside-window diagnostic predates this USB change and
must not be conflated with this valid-window main-only image.

One Shot/tapping source-decoder ABI screen retained the by-value public wrapper
and introduced a target XDATA pointer helper for its three existing callers.
Against identical TD-enabled compile flags, tapping object CSEG 0x632 → 0x62c
and XSEG 0x9f → 0xa1; action object CSEG 0xc2d → 0xc15, XSEG 0x39 unchanged.
The combined 30-object-byte reduction is not a linked saving. The two-byte
XRAM increase already exceeds the one byte recently freed from the previous
fully occupied TD bootstrap; public-wrapper DCE and whole-image allocation are
not established. All changes were restored, with no behavior, target CPU,
stack/reentry or linked test; the candidate is not accepted or qualified.

Final independent Pi source/evidence review found no issues in reporting the
bounded outcome: main-only has 40,408 occupied CODE and exact-image runtime
bound 161/179; separate offline record passes 356 unit tests and 35 suites with
no skips. The runtime report itself retains `offline_tests_passed: false`; the
separate suite pass does not set that approval flag. The last physical-XRAM
main+TD diagnostic predates the USB-bit change and its 1,533 out-of-window
bytes are neither an exact latest-source deficit nor proof all layouts cannot
fit. Reviewer did not independently rebuild, recompute hashes or inspect a
device; it reviewed a provided committed source diff, whose completeness it did
not independently verify. Merge verdict OK with notes for bounded reporting,
not release or hardware validation.
