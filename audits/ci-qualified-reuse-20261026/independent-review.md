# Independent review of qualification reuse

Reviewed on 2026-10-26 against HEAD `31ab52c09138775a1ecd696465a70e50700bbb8a` and the dirty workflow/document changes. No implementation files were changed by this review.

Result: no blocking finding in the reviewed workflow and two STATUS changes. Workflow SHA256: `9538f2b70e5d3a5b6dcd27d612f00da81ab53791d7105bf5fadfa4bd26dd1c59`.

The default push, pull-request and empty-dispatch paths retain full profile qualification. Nonempty dispatch skips the matrix but assembly requires successful shared regressions, an uncancelled run and the explicit dispatch condition. Failed assembly or native packaging cannot reach publication. The existing publication check still requires the tagged source to be an ancestor of main. The current source SHA is checked against checkout and subsequently validated as forty hexadecimal characters by the unchanged assembler.

The prior-run gate requires the same repository, head repository, workflow ID/path, completed run, one successful latest qualification per profile and exactly ten unique nonexpired profile artifacts. Run-wide success is intentionally unnecessary: run 40258163824 completed all ten profile jobs successfully before assembly failed. Inputs enter Python through environment variables; numeric validation and subprocess argument lists prevent shell interpolation. Actions read permission is confined to assembly; contents write remains confined to publication. Metadata or source failures stop before artifact download.

The source ancestor/diff allowlist permits the intended release changes and rejects firmware, build tooling, catalogs and other workflows. Existing production assembly, runtime/compile evidence, profile policy and packing checks remain unchanged. The workflow itself is policy-bound: all ten current policies still need their workflow hashes refreshed for the final committed tree, followed by independent verification. This review does not approve that future policy update.

Verification: all nine author contract tests passed. An additional independent replay fetched current public jobs and artifact metadata for run 40258163824: 15 jobs, ten matching qualified artifacts, accepted by the validator. Twelve additional fixtures rejected missing/incomplete job status, absent/failed/cancelled/skipped/timed-out conclusions and non-boolean-false expiry values. A fresh git merge-base and actual source diff confirmed the recorded old commit is an ancestor and all committed changes are allowed. The embedded validator copy is byte-identical, as checked by the contract test.

Both STATUS edits use the exact absolute tagged GitHub correction-record URL and replace a transient cancelled-CI statement with a neutral release-page reference. No package-guide link rewrite was included.

This is static and metadata review, not evidence of a successful dispatched reuse workflow, native package publication or hardware behavior. No CI run, build, commit or USB operation was started by this review. The current CI failure stop instruction remains binding.


## Qualification reuse: frozen policy approval

Decision: PASS for the optional qualification reuse workflow, two STATUS corrections and all ten exact refreshed offline policies. This table supersedes earlier policy tables. Independent comparison against HEAD found only the workflow and English/Russian STATUS source hash/size records changed in each policy. Exact programs, compiler, runtime evidence, safety, packing and the 280-file test snapshot remain unchanged.

The substantive precommit receipt SHA256 is `df5c335b4bca467231f7479e6777a3f2bad9b1ab8507cef8621590213eb862fb`. All ten profiles and the global substantive gates pass; only committed-input admission and independent review records were deferred. All 25,026 retained input hashes were independently reread with zero mismatches. Test snapshot: `a469c44707139d70f4541d9018716e6eb6bc19628b4f99de8030a34d8e7283fe`. Independent checks passed for 77 public documents, all relative link targets within the 70-entry package guide closure, and actionlint.

| Profile | Exact policy SHA256 |
| --- | --- |
| code | `ac9b0e95d4e73a56b09a6a56ccb83598fb3803bc40a34adb7ca0b82f47442ee8` |
| creative | `29e267a1bfda3524c59f47f73075af82e01793885a23d6f9dc3903d4a9bde06c` |
| game | `82882d5cfda7cbc43d3525940916623cc208a6b8d534df8923fa4468135201b0` |
| main | `b43f7480a624c475b0ece8d3eb693a255c2e5c92db6af5720530ad2afcff6de5` |
| mmo | `753892f426b7ec242c98437b335d1ba15dbf5ab67c4949e9936ad38aef7316e2` |
| multios | `4703e55bd20032fbf881da31956ab6a2d2ec40f1d98c0a95026355d606ba8eed` |
| onehand | `fee8c21141beae8cf45480904cc9cbe9a1eea9c97fc758e9a642a138066ff8f4` |
| pointer | `41a3663a02cfec90c5a81eacd1d90e3a88ccff045c327a353019188bc8fcb89f` |
| shortcuts | `c1a355a6fb3ede58149040aa3a099d1bc57106a47da4a8301c50a532697f9e78` |
| typing | `25e2ad2273bad0d36f42ea1e834ba9251062ef2e251a616d24aa9cdccb33c4d1` |

Genuine program review records were authored after these substantive checks. Production authorization validation and committed-source admission must still confirm the frozen records; successful dispatched reuse, native packages and publication remain separate gates. No new CI run, build, commit or physical device command was started by this review. Hardware remains unvalidated.
