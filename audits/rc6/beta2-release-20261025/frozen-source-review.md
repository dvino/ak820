# Frozen beta.2 source review — 2026-10-26

Independent read-only inspection against HEAD `feeff6f`; origin/main `dc0e7c` integration remains pending. This reviewer authored no implementation in this worktree. Only this review file was written. No USB access, builds, regression reruns, packaging, commits or publication were performed.

## Decision

F1 and F2 are closed by the scoped follow-ups below. F3 is also closed by the final scoped help review below; no actionable finding remains open in this bounded source review. No further actionable defect was established in the inspected selected-image, settings, CI assembly and RGB paths. This is a bounded source review, not approval of the complete release program, final policy witnesses, native packages or pending merge result. The previous `fresh-source-review.md` describes earlier intermediate gaps and must not be used as current final acceptance.

## Finding F1 — P2: beta.2 packages ship beta.1 download and image instructions

`docs/INSTALL.md:19-35` and its Russian counterpart direct readers to beta.1, describe work as the sole installable image and give its old exact hash. Native package guide lists include these files verbatim. `tools/build_beta_release_assets.py:357-361` copies them to INSTALL-en/ru and only replaces the obsolete `ak820-beta-catalog-20261024.zip` string, which the current guides no longer contain. Thus a beta.2 package includes instructions that send a reader back to beta.1 and contradict the ten-profile selection feature. Replace the release-facing instructions in both languages with the actual beta.2 asset names and behavior before packaging; inspect both native packages and the catalog guide payload. The lead independently confirmed the issue and assigned its correction; corrected bytes have not yet been reviewed here.

## Inspected contracts

- Selected profile resolves one approved bundle and exact configured NVM schema. Frozen `ReleaseContext` stores manifest JSON privately and returns a copy; `load_release` reconstructs and compares manifest, paths and schema. GUI disables the selector for the active worker; CLI passes a per-operation context. `settings_workflow` pins the exact host and release bytes, rechecks them before loader entry and erase, and binds the prepared session to the selected release.
- `prepare_trial`, installer readback, settings preparation, device protocol and transport session/flash calls pass `target_build_id` through schema-sensitive packing and verification. Current installer readback disables historical acceptance. Recovery remains separately checked against the original complete OEM backup.
- Settings catalogs require exact configuration-derived image contracts, reject duplicate identities and validate explicitly pinned historical sources. Transition targets must be current catalog images. Restore preflight checks keycodes and extension support before mutation. RGB translation decodes the source saved enum to the stable wire effect, then encodes the target enum; unsupported Direct palettes stop before erase/write. Verify compares the translated saved configuration.
- CI producer builds all ten exact names with fresh diagnostic seeds and source/IRQ certificates, then runs configured qualification. Assembly remeasures each image, checks stable configuration/IHX/compiler/schema/symbol identities, requires committed settings/policy/review/packing inputs, and constructs output atomically. Raw build artifacts retain their own separate hashes; stable identity does not erase exact-build evidence requirements.
- The beta catalog packer checks ten unique capability rows by profile rather than producer order, computes linked CODE identity using the capability producer algorithm, checks each approved bundle, and includes the recursive guide list. This closes the earlier two catalog comparison defects on source inspection. Final byte-level guide closure remains an artifact gate.
- Optional Direct removes its animation enum and allocation. RGB host restore and linked fixtures account for the shifted Reactive enum. Linked RGB fixtures bind configuration to image hash and Direct symbols. Layer wrapper fixture fallbacks invoke the retained state API when optimization removes wrappers; this is appropriate for those indicator cases, but does not independently prove key event or physical timing behavior.
- `configure_firmware.check_pass30` replays recorded transform stages, verifies their adjacency and assembled proofs, validates parameter metadata/context and exact-image postlink proof, and checks explicit assembly kernel presence. This inspection follows those admission paths; it is not a new exhaustive audit of every pre-existing transform implementation.

## Evidence inspected and remaining gates

The current packing preflight contains ten trial/permanent pairs with recovery byte equality. Ten retained runtime summaries report passed whole-program stack qualification, no unresolved roots, bounds 160 or 164 bytes, and capacities 167–172 bytes. These are static/CPU evidence, with physical commands zero and hardware validation false. The transition preflight contains 120 passed offline cases: ten self edges, ninety cross-profile edges and twenty historical-source cases. Its own provenance states packed defaults plus an archived physical ROM, not fresh device capture. No live restore acceptance follows from it.

Full exact-image regression is still running in isolated trees per the lead. This review did not substitute earlier historical review claims for those final results. `profile-policy-preparation.json` explicitly lists remaining freeze/hash refresh, full regression, settings test record, independent policy review and committed-input gates. The actively prepared `ci/profiles` witnesses and program reviews are not approved by this document.

Before final commit/release acceptance: close F1 with a fresh byte review; integrate origin/main and check the actual resulting tree; refresh all affected report/source hashes; finish ten-image regressions and independently review their bound results; independently review final per-profile policies/program reviews/packing receipts; exercise clean committed-input CI assembly; inspect native Windows/Linux package smoke and exact bundle identity; inspect public catalog and standalone guide links. No physical operation is authorized by these gates or this report.

## Inspected source hashes

SHA256 values identify this inspection snapshot; edits require scoped re-review.

- `.github/workflows/windows-installer.yml`: `5a2762d30c3a0471b33417b6bd06e7e9dac60bc72894151eaa457424d9ddd597`
- `tools/build_ci_profiles.py`: `7e408a2124efa85510de0109ec35af0821d9ca8eecd3035bfad93c31be1e6376`
- `tools/build_ci_release.py`: `196d7bf6d73a8309eca4386f44f4765253b99903a21f46c3f7f13c21842dd94a`
- `tools/build_beta_release_assets.py`: `6491d67554af5cf385b0e953a543d021ac563712a5e28a5ed51a9b51fd12909f`
- `tools/build_windows_installer.py`: `db24fa76eaad46826b84c0f88ca69d7f0c142d71d1d2fa9c83d5cb36c433d02f`
- `tools/build_linux_installer.py`: `d4cbab8efec02ab47d70b229f34ec695f2b1b85c06d6a0c74742e9af603545d2`
- `tools/configure_firmware.py`: `406b8135bb3f85c12ca6163eed15eb8376129cdfb3795d2af6c1f8f2a6682340`
- `tools/ak820_device_protocol.py`: `1e4018b75793ecd27876e4b72ad733511f01356a59d7a800868f5dd2ea25137b`
- `tools/installer/ak820.py`: `45461adb311e634f44d94af7295e7cbda08a79470b3b9c34a145ec130297b17c`
- `tools/installer/gui.py`: `87192b4982e876fad76f38c7eb8b500521e7dd942c4e11fea5a8d9c4546cf38b`
- `tools/installer/settings_backup.py`: `1353bc56e16db36d48545b2712c6971910201da8797dd140df1a153a3a2472b2`
- `tools/installer/settings_workflow.py`: `739b941cb1724fdf08b9fb5d798adec507260c22a2d97cdcd02ce7f1247bb26f`
- `tools/installer/test_profile_selection.py`: `505b0f0c589cf5559693f564d4a31936cc99c36a563c4e28395a55bfffabb731`
- `tools/installer/test_transport_schema.py`: `61b65fe7f0b6102abd1784da1e20fd9d02e6c7f4f7be8e92aa39a1959bd7178a`
- `tools/installer/test_catalog_settings.py`: `c2bee692cb94f25cc619fe810e63ce75c6c6dd68072861a1f460aac8ae11c74f`
- `qmk-8051-ak820/util/pack_ak820.py`: `d392ed795cf34f3c0e1a2e58e07b5a35f1e14500c5bd91c6bcaccfd4f9a7cc7c`
- `qmk-8051-ak820/util/ak820_tool.py`: `87229c0fb92dcbbcc0d60f3d75ed43f459647c5a0fccf7cc57e0dd36bb884f0b`
- `qmk-8051-ak820/util/ak820_diagnose.py`: `4833247da16ab7557eca9ae67d0fda9f5952d406f68aead4407baf40bac771b8`
- `qmk-8051-ak820/keyboards/ajazz/ak820/ak820_rgb.c`: `dd07f58a1c7194ba2122bb7c57cba8951e0cdd59cd79d32a534263a505e9376f`
- `qmk-8051-ak820/quantum/rgb_matrix/animations/rgb_matrix_effects.inc`: `a803d72f383db337a443a9b9f9388a3c8d8f3dd92f5a1dc057aa6ab5045552ac`
- `qmk-8051-ak820/tests/ak820_rgb/emitted.py`: `8df6849ebe4ec4b0d667ac6088e061c7f77c7e9164b6dee088731d08b1d34143`
- `qmk-8051-ak820/tests/ak820_vialrgb/linked.py`: `a019dbc682d933066648b22dee69319be686d353e8bb2101df638a8074aab865`
- `docs/INSTALL.md`: `e73d8ea7fa0b83c018856c9b23b5e24302d26195c7d1724c05f2396ff4d23352`
- `docs/ru/INSTALL.md`: `b56efb8d43a87e292a71fab0aef387eb4a873de4929f3a2be43e359bd0d5a596`

## Scoped follow-up: INSTALL correction and policy helper

F1 is **closed at source**. Both guides now describe beta.2 asset names and download URLs, ten profiles with main default, checksum/extraction/launch steps, exact settings compatibility and fresh physical update consent. They identify publication state through Status without asserting publication. Reviewed SHA256: `docs/INSTALL.md` `c7bbdea4074f75eca317ddc5be6ade4f53358a1394fe524562dc2f6555b86d4d`; `docs/ru/INSTALL.md` `54ecdc7961af23fe1a535ba3e6b128ad687a848d84e5b7b8e1ea35d8a97593c9`.

### Finding F2 — P2: root catalog INSTALL aliases have broken relative help links

`tools/build_beta_release_assets.py:357-361` places the full English and Russian guide text at archive root as `INSTALL-en.md` and `INSTALL-ru.md`. Their relative links retain their original `docs/` base. For example the English root copy links to `ru/INSTALL.md`, `STATUS.md`, `profiles/README.md` and `SETTINGS-BACKUP.md`, while the archive includes those documents under `docs/`. The Russian root alias similarly links to `../INSTALL.md`, `STATUS.md` and `profiles/README.md`. These local help links therefore fail after extraction. Rebase local links when creating root aliases, or make root aliases point to the corresponding packaged `docs/INSTALL.md` and `docs/ru/INSTALL.md`. Inspect both aliases and their targets in the final archive. The original `docs/...` copies retain their valid bases.

### Policy helper inspection

Reviewed `prepare_profile_policy.py` SHA256 `4820b45d08bc8f1df9f7e4230c8bd3c0f4170ab06234e0d4e72a21d2f6ae0288`. It does not produce an independent program review and marks generated records as drafts. It includes the complete fixed bilingual `guide_files()` allowlist in each policy, plus host files, actual build source paths, safety sources and witness files. It copies actual stack/startup/IRQ evidence from each qualified tree, binds IHX and symbol identities, and populates packing receipt values from the ten-image packing preflight. The reference-hash field convention matches the existing work receipt; the recovery hash is the APP recovery slice, not a newly claimed full-ROM identity.

No additional actionable defect was established in this helper's current draft role. Its own input checks are narrower than final admission: it checks runtime pass/IHX but leaves detailed analyzer/source/stack placement/IRQ consistency to `release_safety.validate`, and requires only a successful supplied settings record before setting transition passed. Final validation must still reject stale or incomplete test/source closure. The copied runtime summaries' recorded source hashes were compared to the current tree in this follow-up; no drift was found. That read-only hash comparison does not replace a fresh regression or independent evidence review.

The helper's final generated policies, settings test record, all-image qualification, program reviews and packing evidence are still unapproved by this scoped source inspection. F2 and all remaining artifact gates above remain outstanding.

## Scoped follow-up: root aliases rebased

F2 is **closed at source** by `standalone_guide()`. Both source guides are rebased from their original docs directory when copied to root INSTALL aliases. External URLs and same-document anchors remain unchanged; parent traversal is normalized and archive escape is rejected. Read-only evaluation of the actual English and Russian source copies found every resulting local INSTALL alias target in `PUBLIC_GUIDES`. The focused fixture covers both language bases, fragments and external URLs. The lead owns its pending test result; this reviewer did not rerun that suite.

Reviewed source SHA256: `tools/build_beta_release_assets.py` `755eef0906fa7bca8aab780296a3e0ba209e8d4f3cc596959f0b743fc2a666d9`; fixture `tools/test_build_beta_release_assets.py` `0927e3b69a5feeee1e57610ab981d0e47d75cc74589effa339c95bc50200587c`.

### Finding F3 — P2: the packaged guide allowlist still omits linked user help

The root alias fix preserves the original docs copies, but does not close their onward help links. `docs/INDICATORS.md` links to `../web/docs/OS-INDICATOR-PROTOCOL.md`; the Russian counterpart links to `../../web/docs/ru/OS-INDICATOR-PROTOCOL.md`. Neither protocol guide is in `PUBLIC_GUIDES`, `HOST_FILES` or the beta catalog guide payload. Thus readers following the packaged indicator instructions encounter missing local documentation. The packaged README also references absent `docs/images/banner.webp`, `pcb.webp` and `controller.webp`. These diagrams identify supported hardware and should remain available with the corresponding document.

Extend the explicit public allowlist with needed public user-help dependencies, including their recursive public dependencies, or rewrite intentionally online links to repository URLs during package assembly. Do not recursively copy audits or private directories: the packaged Status files also have repository-relative audit links, and README has developer-document links; those should point explicitly online when the targets are intentionally outside the package. A closure check should distinguish bundled local targets from explicit online destinations. Final native and catalog payload inspection remains required.

## Scoped follow-up: packaged help closure and parallel CI producer

F3 is **closed at source**. `guide_files()` now returns 70 explicit public files, including the bilingual OS indicator protocol and four README WebP assets. Markdown receives UTF-8 validation; binary assets retain the safe path, existing-file and symlink checks. Intentionally unbundled technical references in README, Build Profiles, Auto Shift, protocol guides and Status now point explicitly to repository URLs. A read-only extraction of Markdown/image relative destinations from every current `PUBLIC_GUIDES` document found no destination outside the actual `guide_files()` payload. No private audit directory is included. This establishes current source help closure, not existence or integrity of final native/catalog artifacts.

The selected-profile CI producer accepts only nonempty distinct canonical subsets and processes them in catalog order. Selection preserves the full diagnostic bootstrap, fresh context certificate and configured final qualification steps. Its default still covers all ten profiles. The revised workflow uses ten separate matrix checkouts with fail-fast disabled; each archives final build, complete bootstrap and producer record beneath the same checkout-relative `.build` paths. The single assembly job waits for all ten successes, restores all ten archives, recreates pinned toolchain/LUFA/QMK dependencies and invokes the existing all-profile admission path. Native package jobs depend on assembly. No actionable defect was established in these paths on inspection.

The focused producer fixtures cover selected and multiple profiles, catalog order, invalid and duplicate selection, and required bootstrap/final calls. Reported five producer and sixteen package fixture passes belong to the lead's execution record, not reruns by this reviewer. The 120-minute per-profile and assembly timeouts are operational limits that require actual CI evidence. Source inspection does not prove they suffice or qualify download/extraction behavior on a real runner.

At this snapshot, CI guide prose and the example workflow command are still being updated by the lead to describe matrix selection and assembly. Final documentation agreement must be read after those edits. Previous partial regressions were stopped before the final freeze per the lead; they are not final ten-image regression evidence.

Scoped source SHA256:
- `tools/build_ci_profiles.py`: `9fb8e4317f7437f8009cf4a2318d1670f6940ede1ea147010721b3f970ced210`
- `tools/test_build_ci_profiles.py`: `d9063e7aaeb09602220845b99d96c0ac8ebc0f44f06e93ba373498d09995f795`
- `.github/workflows/windows-installer.yml`: `1024c6f27287005a9a4feea1854bda1db419f47f421bcea9f9f2cf98bae3b88b`
- `tools/build_windows_installer.py`: `af5d0c0085e28aa2dc4c0dc8be9392ea3697fd08838b4f339306a82db4c326d6`
- `tools/test_build_windows_installer.py`: `3707bfd5c81c90c6a2a32e30e13c271ad4e808bcb34c548485056bdaec2a30cc`

## Final CI documentation read and finding F4

The updated English and Russian CI guides now correctly distinguish shared checks, ten independently checked-out matrix producer jobs, single assembly, and native package jobs. The local example intentionally omits `--profile` and explains the workflow's one-profile override. Required job names agree with the workflow.

### Finding F4 — P2: failed matrix jobs discard qualification evidence

The `linux-profile` archive step runs only with `if: success()`; its artifact upload also has the default success condition. A failed full qualification therefore uploads neither linked image nor partial runtime/test logs, and the runner discards them at teardown. The previous workflow retained linked evidence with `if: always()`. Current CI documentation explicitly requires retaining partial results from failures. Keep successful qualified artifacts exclusive to successful jobs, but add an always-run bounded diagnostic archive/upload for existing final/bootstrap/report outputs, including failed runs. Missing outputs must not hide the original failure. Assembly must continue depending on all ten successful qualified jobs.

Documentation SHA256:
- `docs/CI.md`: `9323c69321b3266ca215df5967ce5364ad435d5a62f8d661e10d85561b3f48b0`
- `docs/ru/CI.md`: `1074a96b8c4cc5861f2a2470cac87933d26e78821bb68ccf1859d9fd23f092b6`

## Final scoped closure before freeze

F4 is **closed at source**. Failed or cancelled matrix jobs now archive the existing complete `.build` tree, or an explicit missing-output marker if no build directory was created, and upload it for 30 days under `ak820-failed-profile-evidence-<profile>`. That name cannot match assembly's `ak820-qualified-profile-*` download pattern. Successful producer archives and the all-ten success dependency remain unchanged. This preserves diagnostic evidence without admitting failed images. Actual cancellation/upload behavior remains a CI execution condition.

The beta catalog fixture now uses `mkdir(exist_ok=True)` for `web`, because the expanded public guide fixture already creates it for the OS protocol guides. This is consistent with fixture preparation and does not relax production validation.

No actionable finding remains open in this bounded source/docs review. All F1–F4 corrections were read independently of their authors. The reviewed source may proceed to final freeze and the remaining qualification/evidence review; this statement does not approve unfinished ten-image regression, draft per-image program policies, pending merge identity, native artifacts, publication or device writes. The lead's current 259-test run is pending and is not claimed as passed here.

Final scoped snapshot SHA256:
- `.github/workflows/windows-installer.yml`: `8434908462bc22f273fbf8aa612d9d299541112d15aefaf18fbd52c2d3ebcaea`
- `tools/build_ci_profiles.py`: `9fb8e4317f7437f8009cf4a2318d1670f6940ede1ea147010721b3f970ced210`
- `tools/test_build_ci_profiles.py`: `d9063e7aaeb09602220845b99d96c0ac8ebc0f44f06e93ba373498d09995f795`
- `tools/build_windows_installer.py`: `af5d0c0085e28aa2dc4c0dc8be9392ea3697fd08838b4f339306a82db4c326d6`
- `tools/test_build_windows_installer.py`: `3707bfd5c81c90c6a2a32e30e13c271ad4e808bcb34c548485056bdaec2a30cc`
- `tools/build_beta_release_assets.py`: `755eef0906fa7bca8aab780296a3e0ba209e8d4f3cc596959f0b743fc2a666d9`
- `tools/test_build_beta_release_assets.py`: `34b9839cd803a1637177d6a4f7f60b4d24dfbead45e9b66b280faf149be16072`
- `docs/INSTALL.md`: `c7bbdea4074f75eca317ddc5be6ade4f53358a1394fe524562dc2f6555b86d4d`
- `docs/ru/INSTALL.md`: `54ecdc7961af23fe1a535ba3e6b128ad687a848d84e5b7b8e1ea35d8a97593c9`
- `docs/CI.md`: `9323c69321b3266ca215df5967ce5364ad435d5a62f8d661e10d85561b3f48b0`
- `docs/ru/CI.md`: `1074a96b8c4cc5861f2a2470cac87933d26e78821bb68ccf1859d9fd23f092b6`
