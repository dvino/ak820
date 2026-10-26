# Independent CI CRC link review

Result: PASS, 2026-10-26. The reviewed base is `64ac8b210453d261b78f00938666e6ab05644342`. The implementation, policies and host-model evidence were authored separately from this review. Only this report, the ten program review records and the appended final-review decision were written for this review. Repository and RTK instructions were read; supplied documentation wording rules were followed.

The workflow diff adds `ak820_crc.c` to the two shared NVM and macro host-model link commands. `ak820_nvm.c:48` calls `ak820_crc16`; the added file provides its host implementation. Compiler options, sanitizers, working directories, execution and failure behavior are unchanged. Workflow SHA256 is `303487a6fd0441643cfefd67aef07592f5ee476fcffb68106500b3bf0acde57a` (21,719 bytes).

The actual retained model output and commands were inspected in `ci-host-crc-link-fix.log` and the original external audit output. Both compilation and execution statuses are zero with ASan and UBSan retained. NVM passed 10,944 cut cases and its additional checks; macro passed 25,088 cut cases across two erase orders and grammar/storage checks. All five CRC/NVM/macro/model source hashes match actual current bytes. This is host CPU evidence. No compiler, regression producer or USB operation was run by this reviewer.

Each policy differs from the base only in the workflow source record SHA256 and size (21,623 to 21,719). All 825–827 source records in each policy match current bytes. Program identities, packing receipts, settings/transition evidence, runtime proofs and host manifests are unchanged. All ten runtime proof source snapshots remain current and exclude the workflow. The 280-file test-source snapshot is unchanged at `a469c44707139d70f4541d9018716e6eb6bc19628b4f99de8030a34d8e7283fe`. No firmware qualification input changed, so the existing complete ten-image qualification remains applicable.

The refreshed actionlint receipt changes only its workflow SHA256. The lead reported the actual new-workflow actionlint command returned zero; no independent actionlint execution is claimed here.

The reviewed external validator retains SHA256 `7998ed63e697ab58134f3ba85d074265bd2d977e0f7bc2ff04f4a6c35f88571f`. Its completed new `/tmp/ak820-beta2-crc-precommit.json` result has no substantive errors: all ten profiles and global `all_other_evidence_passed` are true, with 25,026 checked inputs and the unchanged test-source snapshot. Overall false is required in precommit mode; committed-input admission and independent review are explicitly deferred. The new receipt SHA256 is `0bdbcf435ee2ae36e7536797732b504a90ac3b447b85e2c6fbeea9e6ed6a97f9`. Every receipt policy hash matches the actual newly reviewed policy bytes. This receipt consumes existing evidence and does not rerun qualification.

The ten actual program review records were refreshed only after that inspection. Production `ak820_ci_authorization.validate_policy` and a separate exact-policy-byte-hash check passed for each actual record against current host manifests and packing receipts. The current approval hashes are:

| Profile | Current exact policy SHA256 |
| --- | --- |
| main | `7ce2ca07729635a7689f7b8ac9e7518c2e861f26a828d337cd337b4ec06c46e7` |
| game | `11b0bee1efeaf3b66d12d1eb58894ead85151f9bf33dae5bde3dc2f35bba9253` |
| mmo | `f76ed3cff0463e313ac802d3fdfee7e24ec53fdf57fbb3aa0de2af50505352a6` |
| typing | `353ffa8dd525e267658288c338f8f98c8bc33fae7941bc3c02041c5521d96ec7` |
| code | `67abebf54abd93079126481e602400071d3f307cb5dd3cc4a83a84b8d8766ae7` |
| pointer | `0fd324593024b372129981ef442e521cdc5cf79fa44eddb2b931b746b41912ff` |
| onehand | `b6505a5a28d4e4eb61ffd6da56d7da9000d554c2a818bf966bfdd86b62ab5488` |
| creative | `534cca4bc73b17e4047008fedc999ce8adec3fda10aa389cba04cb6e22e5ba3d` |
| shortcuts | `aad7c463ae69c5334a004540bf6e10d5db962c4206e4553b54b6549a5efd72bd` |
| multios | `fa9871ede762213117329393ebc853fd44faa12ae94b3ece79ce9a471dd99885` |


No actionable finding remains for this bounded correction and policy reapproval. Exact committed admission must pass after commit. Successful CI reproduction, native package checks, downloaded assets and publication remain separate pending gates. The failed CI run is not a successful release; this review does not claim a release or asset exists. Hardware remains unvalidated; physical device commands performed by this reviewer: zero.
