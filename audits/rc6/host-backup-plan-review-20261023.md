# Review of the local backup plan

Independent documentation and source review, 2026-10-23. The reviewed plan is audits/rc6/general-update-implementation-plan-20261023.md. No runner, prepared session or firmware file was changed during this review. No USB operation was performed. Live installation evidence was recorded separately.

The plan follows the latest decision: defer implementation, keep backup/restore in a shared installer module, use existing commands and add no firmware preservation protocol. It distinguishes a local settings copy from OEM recovery and states that the current one-off update resets settings without automatic restoration.

## Protocol agreement

Source inspection confirms the listed operations: key getters/setters VIA 04/05; encoder getters/setters Vial FE/03 and FE/04; macro count, capacity, read and write VIA 0C/0D/0E/0F; RGB query VIA 08/41, setter 07/41 and durable Save 09. Layout options use VIA keyboard-value get/set 02/03 with layout-options subcommand 02 and a big-endian 32-bit value. Encoder wire directions and persistent order differ; reuse the existing adapter's mapping.

The current macro allocation is 8192 bytes for 16 macros. Published logical length controls getters and execution; stale physical tail is hidden. Upload must start at zero, remain contiguous and terminate all sixteen macros. Binary operands cannot be treated as text or null-terminated strings. The plan's bounded chunks, logical-length rule, interrupted-upload tests and no blind retry policy agree with the implementation.

After restart Vial is locked again. Macro upload and protected QK_BOOT assignments require another physical unlock. The plan states this and keeps the unlock in the installer. It does not promise a one-hold restore that the existing firmware cannot provide.

RGB OFF retains the selected mode. Restoring the saved selected mode and then OFF is supported by the existing setter. Flags have no corresponding setter. Current Direct HSV colors have no getter. Hidden current RAM mode and flags also cannot be proved equal to NVM by comparing available getters. Saving RGB during read-only export would be a write and is correctly excluded.

## Clarifications before implementation

1. The current tools/ak820_device_protocol.py adapter intentionally rejects macro write 0F, RGB Save 09 and layout-value 02/03. Reuse its tested response decoding, but extend the explicit restore allowlist and authorization deliberately. Do not assume the existing restricted adapter already implements every planned operation.
2. Define success for exported, supported values. Available getter equality cannot establish preservation of arbitrary hidden RAM fields. Surface missing getters/setters before erase; never infer complete current-RAM preservation from matching visible values. No freeze exists, and repeated reads do not make a snapshot atomic.
3. Reconcile the older current-priority and no-install statements in both ROADMAP translations and STATUS after the lead records the live result. Their new top-level host-only decision is clear, but older sections still describe the previous release-preparation stage.

No blocking protocol error was found in the deferred host-only plan. These clarifications were sent to the lead. Implementation, packages, host tests, settings-write tests and physical persistence validation remain future work; this review is not approval of an implemented restore function.

## Precommit follow-up

The plan now explicitly requires authorized allowlist extensions and states that matching visible getters cannot establish hidden RAM preservation. Findings 1 and 2 are closed.

The exact reviewed one-off runner remained unchanged at SHA256 da0a01da7c3c944b37c2038004bdeffd189c0ef30ec167f9f671413ebabaf131. Its eight tests independently passed again in 0.060 seconds. The recorded live result reports payload a1b8beec9a2a675c955bac946339e31f1823e17cdfb60f4755796e550530c711, full ROM 56b2de776924c48bda6d08a2604edc8ab94f24e5ec7365f7b584c0fe7dd70fc5 and no settings restoration. The loader event record contains exactly commands 1,2,3,4,5. Physical typing was confirmed separately; the result file itself correctly retains its narrower automatic-test claim.

The separate read-only installed report passes 498 key assignments, 12 encoder slots, 16 macros with an 8192-byte view and 82 LED descriptors. It explicitly skips settings writes and durable RGB saving. README and STATUS in both languages agree with those facts and keep physical encoder/lighting and power-cycle checks untested. Private sessions and raw settings remain under ignored host/runs; the reviewed Git additions contain no raw ROM or settings bytes. No firmware C or active approved host-file input changes are present in this work package.

The older ROADMAP stage paragraphs were replaced in both languages. The retired prototype reference in optimized-breathing-canonical-review-20261023.md is now explicitly historical and points to the deferred host-only replacement. Retired prototype files have no remaining executable references.

## Final closure

PASS for the reviewed work package, 2026-10-23. AGENTS and its Russian translation agree on impersonal documentation, a project-focused README, package instructions in INSTALL and validation evidence in STATUS. README, INSTALL, ROADMAP and STATUS in both languages agree on installed SDCC 4.6, completed as-is flashing with package defaults, separately confirmed typing and deferred host-only backup/restore. INSTALL explicitly identifies the older exact-candidate repair path and states that it cannot update the current SDCC 4.6 image; the completed installation used the separate reviewed one-off runner.

Reviewed scope includes the host-only plan, the two review reports, the unchanged one-off runner and its tests, retired prototype documents/module/test removals, the historical review clarification and the documentation files listed above. Firmware source and approved installer runtime inputs remain unchanged. Current private ROM/settings evidence is excluded from Git. The eight one-off tests passed independently; the existing source-installer offline verification also passed. The direct test invocation is python tools/test_flash_reviewed_release_once.py; module-style invocation without tools on sys.path is not a runner defect.

All findings recorded in this review are closed. No blocking code, documentation, test-scope or privacy finding remains for commit. This approval does not claim physical encoder or LED behavior, macro upload, durable RGB saving or power-loss persistence. No additional live operation, commit, merge or push was performed during review.
