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
