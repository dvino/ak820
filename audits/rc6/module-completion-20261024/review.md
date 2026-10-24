# Independent source review

Reviews were completed independently of the author for each implementation
area. No review grants a release, settings write or device update permission.
Final aggregate evidence review follows the full regression matrix.

| Area | Reviewed decision and closure |
| --- | --- |
| Tap Dance | Eight padded rows; bounded physical-source admission, remap between taps, overlap ownership and cancellation. Recursive dispatch uses a private four-use guard with one common reset. Removing the guard fails the negative control. |
| Key Overrides | Projection preserves shared key ownership in 6KRO/NKRO. Required/forbidden modifier transitions, same-usage owners and rollover are explicit. Late key loading is safe because sync has no callback. Duplicate overlay usage skips only empty-slot search. |
| QMK Settings | Typed XDATA API, byte capacities, exact widths/ranges, defaults, CRC `c97b`, reserved bytes and conditional Auto Shift ID. Blank default records remain unchanged; failed storage never publishes success. |
| NVM and backup | Fixed Combo address, page-contained TD/KO records, schema selection, explicit migration and downgrade rejection. Restore preflight rejects inactive differences; unchanged blank defaults preserve durable bytes. |
| Core ABI | All affected record callers use model-large XDATA. Repeat pointer declarations agree across translation units. The callee-saved repeat getter uses DPTR/A only. |
| Empty callbacks | Current AK820 SDCC callbacks are strong empty/default implementations with no overrides or escaping addresses. Elision is target-specific; future custom callbacks require restoring the path and requalification. |
| Combo helpers | Fully parenthesized predicates have side-effect-free arguments and preserve input/output validation. Host traces and storage checks pass. |
| Stack checker | The additional private Tap Dance guard is enumerated under the existing strict source/linked idiom proof. Opcode assumptions and whole-program gates are unchanged. |
| Catalog | Exact image, compiler, source, runtime, base and supplemental evidence remain required. Module limits use the shared codec; stored and enabled capabilities differ. No write or release authority is inferred. |
| Test binding | Root tests and QMK utilities are included in qualification source hashes. The negative control mutates all four source locations. Settings ordinary and Auto Shift host variants retain UBSan. |
| Storage fixture | Production types, addresses, validators and getters/setters are extracted. All eight padded slots, neighbors, invalid rows/indices, write order, failure ACKs and latched failure are covered. |
| Public documentation | New guides and profile descriptions match source. Historical evidence now names the old Mac/PC and OS profiles explicitly; current profile count is 24. Published alpha.3 limits are scoped to that release. |

Focused reviews passed 32 analyzer cases, 29 configuration-gate cases,
12 catalog-gate cases and the typed storage fixtures. Earlier linked probes
passed 21 Tap Dance cases, 13 Key Overrides cases (59 checks and 80 outgoing
report sends), and 12 Settings cases (52 checks). These focused results do
not replace the final current-image regression evidence.

The full regression exposed stale host/CPU fixture assumptions. Independent
inspection accepted the host address qualifier, image-bound optional counts,
production settings initialization and the outgoing HID pointer observer after
NKRO report-ID assignment. All three Combo suites pass 26 cases. Specialized
Key Overrides retains 13 cases, 59 checks and 80 sends; Settings retains 12
cases and 52 checks. Legacy schema02 metadata is accepted only with extensions
off; malformed schema03 and inconsistent image/configuration hashes fail.
Wrong outgoing pointers, report IDs and bitmaps are rejected by negative controls.
The shared checker input changed, so all four exact runtime proofs were repeated
before full regression. Source and fixture corrections are approved for freeze;
final aggregate evidence review remains pending.

The retention tool was independently inspected for source/commit binding,
complete artifact manifests, unchanged report bytes, combined runtime checks,
base/profile log verification and honest preservation of source metadata.
Portable verification checks retained evidence and does not rerun CPU tests.

A follow-up full-regression finding was confined to the core Repeat host
fixture: its hand-written record preamble also needed the empty host pointer
qualifier. Independent inspection accepted the two-line boundary change.
All five ordinary UBSan groups pass (234,881,024 bounded input combinations).
No firmware input or runtime-proof source changed; runtime-only images remain
bound to `ac48c65`, while full qualification uses the fixture follow-up commit.
The initially failed supplemental logs remain in the complete Tap Dance build.

A second follow-up corrected user-facing NKRO/One Shot observations: the shared
feature fixture now selects the actual projected report and verifies each
outgoing callback pointer. Original state assertions and report-ID expectations
are unchanged. Direct unlock fixtures retain their original default behavior.
Independent inspection and negative controls accepted the change. NKRO passes
7 cases and 44 checks on all four images; KO One Shot passes 15 cases and 61
checks; the specialized KO suite retains all 13 cases, 59 checks and 80 sends.
Only test fixtures changed. No firmware or runtime-proof input changed.

## Final acceptance

Independent final review approved the evidence and documentation with no
blocking findings. All 26 row/archive bindings and four complete-regression
archives were checked. Matrix and catalog hashes, profile coverage, compiler
input freezes, source scopes, resource tables and permission flags agree.
The complete acceptance record is [final-review.md](final-review.md).
No physical or release approval is inferred from that review.
