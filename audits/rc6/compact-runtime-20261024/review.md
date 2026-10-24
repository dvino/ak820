# Review record

## Scope and separation

Code is reviewed by a reviewer other than its author before commit. The
published alpha.3 image and installed device were not changed. This record
covers offline source and test work; final integrated qualification is recorded
separately and does not inherit alpha.3 release approval.

## Independent reviews

| Work | Independent review | Result |
| --- | --- | --- |
| Encoder event reuse, Mouse Keys pair normalization, implicit static zeros | Root review of the optimizer's source, emitted-event contract and retained differential/linked evidence | Approved; both waits and fresh release time remain; all 65,536 held/selected combinations preserve axis priority; nonzero cache sentinels remain |
| Short-transfer diagnostic rejection and custom tool path | Root review of the separate author's tool/test changes and successful full-image reproduction | Approved; immutable long transfer is restored for the union of byte-invalid and authenticated linker-rejected sites; final gate stays strict |
| GUI controls | Independent `review_gui` source/docs review and rerun of host plus 11 linked cases | Approved after One Shot finding was fixed and retested |
| Dynamic Macros | Independent `review_dynamic` source/docs review and rerun of host plus 26 linked cases | Approved after nested Vial ownership finding was fixed; final isolated evidence refreshed and checked |
| EEPROM cursor and profile/configurator wiring | Independent `review_integration` static ABI/bounds review, ASan/UBSan rerun and 25 configurator tests | Approved, including full 8192-byte upper boundary; final profile-list cleanup checked before commit |
| User guides and README/roadmap integration | Root review of the separate documentation author's EN/RU changes; independent integration review of English scope/behavior | Source, published image and installed state remain distinct; exact combined evidence still pending |

## Findings and closure

The first Mouse Keys reduction reversed priority for arbitrary opposing wheel
bits. Exhaustive comparison exposed it; the final expression preserves the old
negative-bit priority in every held/selected pair. Both short and long-transfer
isolated images passed the linked event and mouse suites.

GUI controls initially consumed pending One Shot modifiers. Exactly `GU_ON`,
`GU_OFF` and `GU_TOGG` are now excluded on both edges before the consumer.
Queued and held OSM cases cover all three controls followed by ordinary use.

Dynamic Macro playback initially could execute inside an extended Vial
DOWN/UP primitive, using the wrong owner context. The task now pauses while
`ak820_macro_primitive` is set. Due-press and due-release regressions execute
actual extended operations 6/7 and check owned key/modifier release.

The cursor first exposed two host-fixture issues: a direct 16-bit to 64-bit
pointer cast and use of a native host address as a logical EEPROM base.
Production casts now pass through `uintptr_t`; the host stub uses logical
`0x0800` and checks offsets before indexing its array. ASan/UBSan tests include
slot 15 ending at `0x27ff` with extended/basic/delay operands and a missing
separator scan stopping at exclusive `0x2800`.

The short-call real-linker test initially assumed a default local toolchain.
It now honors the validated explicit path, verifies pinned assembler/linker
hashes and fails on a configured missing/wrong tool. Tests passed for the
local and external paths without skips. The caller's environment is preserved.

The exploratory all-input profile exceeded the main window by 804 bytes and
was removed from the accepted selector. The final selector and guides list 16
profiles. It is retained only as a rejected experiment.

## Combined-feature review and checkpoint closure

The separately authored GUI/Dynamic Macro and GUI/Auto Shift scenarios were
reviewed and independently rerun by root: both exact probe images passed all
12 cases. The former stores raw GUI+Ctrl while masking publication, excludes
GUI controls from recording, reveals the same playing tap with GU_ON, then
releases macro ownership while preserving physical Ctrl. The latter keeps
Auto Shift enabled, checks masked-GUI bypass and the 174/175 ms boundary, and
preserves the Shift owner across GUI toggles and release. Production handlers
run without injecting private feature state. The first macro fixture used an
early tick; the corrected normal idle task observes the documented 10 ms
phase. Firmware was unchanged. Results, simulator scripts and logs are retained
in `integration-probes/gui-dm-combined/` and `gui-as-combined/`.

Independent integration review approved the implementation checkpoint after
verifying the 16-profile roster, rejected selection, documentation links,
accepted artifact hashes, both CODE windows and the 804-byte rejected overflow.
The frozen eighteen-variant matrix and final evidence review remain required
before this work is reported as fully checked. No
physical behavior, runtime stack bound or release eligibility is inferred.
