# RC6 erase candidate review

Date: 2026-10-23. Independent review by an agent that did not author the candidate. No build, CPU test, USB access, reset or flash was performed by this reviewer.

## Current decision

Independent offline review passed with no open blocking finding. The firmware build and prepared personal payload pass this bounded review. Release assembly remains pending independent review of the newly requested GUI update workflow. This is not hardware validation or permission to flash.

## Reviewed scope

The bounded comparison is audits/rc6/candidate-erase-source.diff, from final3 flash source SHA256 cb063c26d81c784a106aa7078db195f1ac3ade7a54b381b3f02fc787609b30f5 to candidate b5ef5524ff1206a7d49fc5e3aa3436b9feed9bba33c2a1062429f42c21c1b34b. The reviewer independently checked the current candidate hash. The change adds the register-only erase leaf and verifies all 64 CODE bytes after erase. The earlier block-program change is outside this bounded delta.

## Source findings

The erase leaf reads ROM_CTRL into A, preserves the before-status in B, checks bit 6, issues A6 and reads status before any XRAM access. DPH:DPL returns before:after. It does not touch register-bank registers or interrupt state. Emitted caller scratch-register use remains to be checked.

The caller still sets mode 80, value zero, aligned target address and CODE_WE. It saves IE, disables EA, clears CODE_WE and SAFE_MOD, then restores IE. The status predicate is unchanged. ROM_STATUS and ROM_CTRL are the same SFR in ch555.h.

The public erase function rejects misaligned addresses. flash_operation rejects addresses outside C700..EF7F before issuing an opcode. With 64-byte alignment, EF40 is the last allowed page; its full readback ends at EF7F. Readback happens after the IAP cleanup and stops at the first nonzero byte. A failed erase therefore returns before write_page can program the target. The diagnostic retains A6. No wire format, NVM schema or range change is present.

Matching the OEM register ordering removes an observed difference. It does not establish that the ordering caused the device fault or that the candidate fixes it. The saved device fault and valid retained journal are described in target-write-fault-analysis.md. A boot can replay that journal, so any later flash/restart decision must account for the existing committed temporary value.

## Pending evidence

Bind the final decision to the actual Git build IHX/MAP/report hashes and source snapshot; inspect emitted erase/caller instructions and scratch-register ABI; review stack/resource and safety/model tests; verify the 15 host tests and matching documentation. The ineffective-erase model must expect A6 for this candidate, while preserving the old 9A baseline reproduction. Device behavior remains unproved until a separately authorized operation.

## Integration checks reviewed

The runner forwards the selected IAP fault profile only to ak820_iap and records it in the report. The guarded-erase model requires A6 as the last target operation and rejects any target 9A during the setter and boot replay; legacy-iap keeps the baseline expectation. The added orchestration test checks the guarded profile reaches exactly the IAP command and report. Both testing documents explain that selecting a profile does not identify the linked image. No blocking issue was found.

The reviewer read host/runs/rc6-candidate-base-tests.json: seven suites passed and physical_device_commands is zero. These are base host and documentation checks, not linked-candidate CPU or device validation.

## Frozen build and emitted code

The reviewer independently hashed the completed actual-Git build in qmk-8051-ak820/.build/rc6-candidate-erase-20261023. IHX SHA256 is d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce; MAP is 9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000; build-report.json is 976a98b72c3db45cb8950df4a3b544e40334bb04cf785aea30c876a4f34aafcd. The report records the reviewed flash source hash, all 130 commands succeeded, and hardware_validated and packed_device_update are false.

The emitted dce/ak820_flash.asm lines 647..658 preserve the naked leaf exactly. At 814..824 the caller immediately copies DPL/DPH into r6/r7 before reusing DPTR; no live B or DPTR state is relied on. The program leaf and its caller preserve their earlier path. At 936..941 erase preserves target r6/r7 around flash_operation, then iterates r5 over exactly 64 bytes. The CODE read helper preserves r6/r7 and leaves r5 intact.

MEM and MAP agree: stack starts at 68, initial SP is 67, OSEG starts at 63 with length 5, and SSEG provides 152 bytes. There is no static overlap. The leaf has no pushes; its call uses two return-address bytes. During readback the read helper uses two register-save bytes in addition to the call return address. The smaller free stack compared with final3 still requires the fresh CPU stack evidence before final approval. CODE is 39347 bytes, main CODE 37488 and low CODE 1859, with highest occupied address C296 below NVM C700.

## Personal session checked offline

Reviewed host/runs/prepare_rc6_erase_candidate.py and host/runs/20261023-rc6-erase-candidate-ready. The script checks frozen IHX/MAP, verifies the previous permanent image and the saved pre-fault snapshot 20608dac9d21320ca113b97a6a398c473f3d188a14a6ea0fd8ff86240fc883b1, and preserves only its durable NVM. It makes no live-state freshness claim and opens no HID. The reviewer independently repacked the permanent payload from the frozen build, private stock ROM and saved NVM: the result is byte-equal. Permanent payload SHA256 is 54290ce406fda133bd90703664f60559e23620f184f89033c98dddb56e2299ed, size 51136.

Direct byte checks confirmed durable NVM equality and CD40=00A900AA. The candidate payload journal area is all zero, so it does not replay the failed temporary KC_NO journal. restore-native.bin equals the original recovery backup application slice and retains SHA256 d7152819712470cf37a0c29d69b756edc4a51aca1d20c13e1fcf4b96f9638535. This establishes prepared bytes, not installed state or erase success on silicon.

## Final test evidence and finding closure

The reviewer independently read host/runs/rc6-candidate-cpu-summary.json and verified all six result-file SHA256 values. Features 33, unlock 10, tri-layer 16, emitted ABI 3, reactive RGB 12 and IRQ 5 cases passed against the frozen IHX; before/after IHX, MAP and report hashes agree. Highest tested main stack use in the summary is 66 bytes. The IRQ model uses 80 reserved main bytes plus a conditional 42-byte nested IRQ bound, leaving 30 of 152 bytes. These are exercised paths and a conditional model, not a whole-program stack proof. RGB summary zero is an absent-measurement default; its underlying result records peak SP124 and 21 tested bytes, not zero usage.

The complete guarded-erase IAP run passed all 12 cases in qmk-8051-ak820/.build/rc6-iap-candidate-erase-retry1-20261023/results.json, SHA256 6fde8d82a35fc50e8e8625b2a57bba83ca05064fdb875026c6e96f9834724239. Every case binds the frozen IHX. Maximum IAP peak SP is 146. The ineffective-erase case retains the committed journal, withholds setter ACK, stops at stage12 after A6/C0/C0 at CD40 without a target 9A, and reports replay stage3. This verifies the guard under the explicit failure model, not a silicon fix. The earlier attempt in .build/rc6-iap-candidate-erase-20261023 remains incomplete: normal/dense cases passed, then the next simulator initialization timed out. The lead reports that only the uCsim banner was received and both processes were terminal before the separate complete rerun. The timeout is retained as a failed test attempt; it is not counted as a passing full run.

Reviewed the IAP README and profile code: the preselected legacy/guarded expectations reject the wrong image behavior, explain model limits, and keep cached getters separate from durable evidence. The runner forwarding regression gap was closed with an explicit guarded-profile assertion. The ROADMAP finding was closed in English and Russian by labeling final3 as the prior baseline and naming candidate tests/review as the next step. Current STATUS/README wording distinguishes source, candidate build and the installed first image. All 15 HOST_FILES are byte-identical to the previously independently reviewed machine record; this review rebinds them to the candidate build. No correctness finding is waived.
