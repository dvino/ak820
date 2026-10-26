# Final beta.2 source and guide review — 2026-10-26

Result: bounded source PASS. No actionable new defect was established in the inspected frozen source and current English/Russian guide contracts. Final reports, catalogs, policies and completed qualification evidence remain pending review. This report is not release approval or a per-profile program approval.

The inspection was independent of the implementation. Only this review file was written. No build, regression suite, simulator, USB operation, packaging, commit or publication was performed. Repository AGENTS.md and RTK instructions were read. The writing-style skill was consulted; explicit repository wording rules were followed without claiming retrieved style evidence.

## Source contracts

The CI producer requires the boolean `whole_program_stack_qualified` from the final configuration report, alongside exact configuration, offline success and required qualification/profile reports. The old `whole_program_qualified` field cannot satisfy this condition. Its fixture explicitly rejects that obsolete field and a false combined result. The producer preserves fresh bootstrap/context generation and final configured qualification for every selected canonical profile. Default selection remains all ten; matrix selection is canonical, nonempty and distinct.

The workflow gives each of the ten profiles a separate checkout, retains final and bootstrap provenance, waits for every successful producer before assembly and restores the same relative build paths. Failed/cancelled output uses a distinct diagnostic artifact name which assembly cannot download as qualified input. Assembly rechecks committed policy/review/receipt inputs, exact configuration and image qualification before native packaging. Source inspection does not prove runner duration, cancellation behavior or successful CI execution.

Approval identities use exact IHX bytes and normalized linked symbols, with configuration/compiler/schema bound separately by the measured reproducible identity. Checkout-dependent MAP headers and report paths do not become the stable program identity. The raw MAP, build report, source manifest, qualification and attestation hashes remain independently measured and bound to the actual CI bundle. Tests cover changed paths with unchanged symbols and rejection of changed configuration, image/compiler identity and symbols. This avoids rejecting a legitimate reproduction solely for different absolute paths without admitting a different linked program.

The assembler exports capability records from its actual ten measured builds. Publication overlays that output and its measured matrix before the catalog packer compares exact approved bundle identities. Neither local catalog placeholders nor machine reproduction replace independent program approval.

## Installer and documentation agreement

The current EN/RU installation tables agree with the canonical ten profiles and `main` default. Main retains Leader, Dynamic Macros, Key Overrides and Direct; each variant's documented exchanges agree with `ak820_profiles`. The CLI exposes exact profile choice; the GUI locks its selector while an operation runs. A profile selection alone does not write hardware. The selected bundle and settings schema remain pinned through preparation and update checks. The installation instructions retain the three-second fresh physical confirmation and settings/OEM recovery boundaries.

Current EN/RU CI guides agree with the ten-job matrix, separate all-profile assembly, native package dependencies, retained failed evidence and fresh measured catalog export. INSTALL describes the intended beta.2 packages and links publication state to STATUS. STATUS explicitly says beta.2 is unpublished, full regression is running and hardware remains unvalidated; beta.1 evidence is scoped to its historical work image. No new claim of completed publication or physical acceptance was established.

An independent read-only extraction of the explicit package inventory found 70 public files: 66 Markdown files and four WebP assets. All current relative Markdown and HTML image/link file destinations resolve inside that inventory. The bilingual OS indicator protocol and README hardware images are included. Root INSTALL aliases use the existing rebase helper. Intentionally unbundled technical references are explicit repository URLs. This proves present source help closure only; final archive payloads and guide links still need artifact inspection.

## Disabled module fixtures

The fixture branches are selected from configuration bound to actual IHX and MAP hashes and cross-checked against linked Direct/NKRO allocation. Disabled cases assert behavior rather than skipping enabled expectations: Direct commands preserve state/output, stale NKRO settings preserve 6KRO output and independent owners, and omitted Grave Escape preserves settings without producing its removed usage. Enabled cases remain present.

The Mac/PC disabled-NKRO case follows firmware transform order: aggregate physical modifiers pass through Mac/PC before Ctrl/GUI. Its Ctrl-plus-Alt and separate release expectations exercise both transforms. Dynamic Macro trace dumps use the outgoing report address expected by the parser. These static findings agree with the scoped optional/remaining fixture reviews; current ten-profile execution is still required.

## Evidence still required

The lead reports 261 passing host-tools tests. That result was not rerun here and does not establish firmware or hardware acceptance. Earlier source reviews and their scoped finding closures were consulted; their older intermediate result counts and pending-state statements are historical snapshots.

Final stable configuration/runtime/qualification reports, measured web catalogs, settings records, per-profile policies, packing receipts and program review records require a separate exact-byte review after all ten workers finish. Their source hashes, guide inventory and image identities must agree with the resulting frozen tree. Pending merge/committed-tree identity, clean CI admission, native Windows/Linux smoke results, complete catalog/native payloads, download checks and publication identity remain separate gates. This report grants no device-write authorization.

## Inspected contract hashes

- `tools/build_ci_profiles.py`: `e35b43cdc29f8b0ae74b7a9810cc2ac032f7a3db85444e58b6bdc258a6bc4f10`
- `tools/build_ci_release.py`: `5d88cd4435ad7f6827649b7057a15dc79b393d93fd856c2b9436ee8f118f7acc`
- `qmk-8051-ak820/util/ak820_ci_authorization.py`: `da9f487b214e23c66cb88b436ea42b5025a61de03ea43153fa354172b89a6032`
- `tools/build_windows_installer.py`: `af5d0c0085e28aa2dc4c0dc8be9392ea3697fd08838b4f339306a82db4c326d6`
- `tools/build_beta_release_assets.py`: `755eef0906fa7bca8aab780296a3e0ba209e8d4f3cc596959f0b743fc2a666d9`
- `.github/workflows/windows-installer.yml`: `dc3d0d294329c7e7d1c4a149272524f846e068ae9dfffa517da4b0150d27ea9c`
- `docs/CI.md`: `6dc3c406f026c11f9a366892caeaa1a976506c0b81158d5c6a140dc71ad4a1f0`
- `docs/ru/CI.md`: `34b9f17653579945d3150e68ea59d51b400cad46e541e4e1ca8e22870cc2cdf5`
- `docs/INSTALL.md`: `6f1aa3a5718497524134d1b0efefd06d2201a3a6b59afb483ce7c7b93ac2ca4d`
- `docs/ru/INSTALL.md`: `7f36da8eed8e13ffed8bf1931dd6baa121aee8c925bbe91aee66fd3637586929`

## Scoped follow-up: external forensic qualification wrapper

Read-only inspection covered `/tmp/ak820-beta2-forensic-qualify.py` at SHA256 `3beb4a96dea01653843ec98894e478649477bf80f563e58d5196d0b9b8240625`, and the original spill capture/prepare and configure validator call sites. No qualification was launched and no source or wrapper file was edited.

The wrapper calls the original configure entrypoint once through `runpy` with the original command arguments, replacing only argv[0]. Each patched prepare/capture calls its saved original exactly once with unchanged positional/keyword arguments. Successful prepare returns the same replay object. The original configure code still compares all six proof fields, requires selected count and postlink qualification, compares assembly and verifies assembled proof. No validator predicate or artifact input is replaced. Expected proof is read from the original build; replay records and a divergent temporary-proof copy are written beneath a unique system-temporary archive. This is intended for invocation from the exact repository root; the wrapper derives its entrypoint/import paths from the working directory.

**Finding P2: diagnostic printing can replace original exceptions or returns.** `capture_trace` prints inside its exception handler before reraising. If that print fails, a logging exception can replace the original capture exception; in particular, an original ValueError would no longer necessarily reach prepare's existing metadata-rejection fallback. The recording failure handler in `prepare_trace` also prints without protection, so an observation error followed by a logging error can replace an otherwise successful original return. Guard diagnostic output itself as best effort before relying on strict exception transparency. Original capture/prepare errors must retain their original type and propagation, and observation failures must leave the successful replay object unchanged.

The wrapper does not relax acceptance predicates on inspection, but its exception transparency is not fully established until this narrow finding is closed. Runtime timing and I/O overhead can affect execution and remain diagnostic conditions. All nine other final qualifications and the final reports/catalog/policy/evidence gates remain outside this follow-up.

### Wrapper P2 closure

The P2 is closed at source by external wrapper SHA256 `0723d3e1e4f597e2b9fb810e6676d19a7afa4156cc55c25ca22f1dd9c4bc5f0d`. All diagnostic printing now uses `safe_log`, which catches ordinary logging exceptions. Original capture failures are then reraised with bare `raise`; original prepare failures remain outside the observation handler. Recording failures cannot replace a successful replay return. Archive initialization is also best effort: failure disables observation and leaves the original prepare result unchanged. Capture diagnostic lookup handles positional or keyword module arguments without assuming a third positional argument exists.

The original functions still run once with unchanged arguments; the same returned replay object reaches the original validator, whose predicates remain intact. The prior input/path and temporary-output conclusions still apply. No tests or qualification launch were performed for this closure. This approves only the bounded observation wrapper source; it does not close the multios proof discrepancy or qualify any image.

## New scoped source review: separate compiler AST and diagnostics

Result: bounded source PASS, with a minor stale comment noted below. This review covers only the fresh compiler-capture correction and its integration fixtures. It supersedes no pending image qualification. The reviewed hashes are:

- `qmk-8051-ak820/util/ak820_parameter_spills.py`: `ba093ea122e865d8c48f8638f2ab408d020849f0bc937cf23a2e6f6579f04afe`
- `qmk-8051-ak820/tests/ak820_parameter_spills/test_integration.py`: `a2e708af8b6f0f59897262ac66d4dff144aec41f1fd6f51fc6ab2f0c7027c8fe`

The implementation changes only compiler stream capture and retained diagnostic evidence. The compiler runs once with the same command, frozen preprocessed stdin, working directory and timeout. stdout remains the byte-exact AST log; stderr is captured separately to a diagnostic log. Neither stream is filtered, repaired or retried. Both logs enter the retained file set and its SHA256 map, which enters the typed metadata manifest. Diagnostic output is retained even before a nonzero compiler result is rejected.

Existing fail-closed checks remain unchanged: frozen source/include hashes and compiler flags; preprocessor include closure; compiler return code; required assembly/raw files; canonical assembly equality including literals and operands; input stability after capture; unique typed receive identity, required formal type, volatile-object and address-taken rejection; unique AST function identity; inline assembly exclusion; opcode and linked postcheck predicates. This separates compiler channels without relaxing a proof predicate or accepting a missing function identity.

The three added tests cover rejection of missing/duplicate AST identities, exact stdout/stderr retention with both hashes, and rejection of a nonzero mocked compiler result. Existing ambiguous-receive, preprocessed-source, type, escape and canonical-assembly tests remain. The stream fixture checks the resulting byte files and hashes; it does not assert the subprocess stderr argument directly, so actual compiler channel behavior remains execution evidence. The author reports 18 passing integration tests; no tests were rerun during this independent inspection.

The reported actual mixed-stream warning insertion and MMO selected-count discrepancy were supplied as the diagnostic rationale, not independently replayed here. Fresh builds, exact-image runtime bounds and full regressions are mandatory after this utility identity changes. Earlier image passes and partially completed qualification cannot qualify the changed source. Final regenerated reports, catalogs, policies and program evidence remain pending review.

Minor documentation issue: the capture docstring still says four retained semantic/provenance files, while the retained set now has six files (previously five). Update that description to name the retained outputs or omit the fixed count. This stale comment does not alter validation.

### Capture documentation closure and final utility pin

The stale retained-file-count comment is closed by utility SHA256 `30f9032ccf0fcb82ae785e0f7e15a1dcf69ef987686dbc50b7780621a22f52ad`. Its docstring now names compiler ASM, raw/AST dumps, preprocessed source, dependency file and compiler diagnostics, agreeing with the actual retained set. The scoped implementation conclusion above remains valid for this comment correction.

The new EN/RU optimization-research paragraphs agree with separate stdout AST and stderr diagnostic retention, hashes for both logs, unchanged source/type/ASM/postlink checks, and mandatory fresh builds with exact-image qualification after a capture-tool change. The fixture README also states that AST parsing remains strict and missing/duplicate function identity or compiler failure rejects capture. No warning filtering, retry or relaxed identity claim is introduced. The lead reports 77 document checks passing; no tests or builds were run for this review.

Reviewed document SHA256:

- `docs/OPTIMIZATION-RESEARCH.md`: `2643695327ce5790dfba2830cd760225d403baf36d57b55972c075d60f087790`
- `docs/ru/OPTIMIZATION-RESEARCH.md`: `2d36889670f7bccfe58d331ce7f5c70fd3f5864021e133bdb80262d1786a062a`
- `qmk-8051-ak820/tests/ak820_parameter_spills/README.md`: `8492da5663becd54f8b2bb0727a4b3f83af9618a97d54685aa50975093415b72`

No actionable issue remains in this scoped utility/documentation correction. Earlier stopped qualification and archived evidence do not qualify the corrected source. Fresh source-fixed builds, runtime proofs, full regressions and final reports/catalog/policy/evidence review remain required.

### Scoped CI wiring review: metadata capture unit contracts

Result: bounded source PASS for the added `Check compiler metadata capture contracts` step in `.github/workflows/windows-installer.yml`, SHA256 `d3c707fc132a02b780aba1e4c1c6233484ac51bb9c326b4a7e1f2e4d77f9f937`. It runs `python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_parameter_spills -p 'test_*.py' -v` from the checkout root, after compiler-selection tests and before the NVM host model. This discovers the reviewed spill unit fixtures in the shared Linux regression job. A nonzero result fails that job; every profile producer depends on its success, and assembly still requires shared checks plus all ten producers. No continue-on-error, condition bypass or new artifact admission path is introduced.

This wiring closes the CI discovery omission without changing compiler, firmware, utility or fixture inputs. The lead reports pinned actionlint success. No tests, builds or qualification launches were performed during this review. Successful CI execution and all current fresh exact-image qualification/evidence gates remain pending.
