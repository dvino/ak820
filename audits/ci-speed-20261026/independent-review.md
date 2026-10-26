# Independent review of CI validation time

Reviewed on 2026-10-26 against base `4a1fcff046da09071700b730b1db5982ce427deb` and the frozen worktree changes. The reviewer did not author the implementation, tests, policies or verification evidence. Only this report and the ten program-review records were written during review.

## Decision and scope

PASS for the reviewed source changes and exact refreshed offline policy bindings listed below. No blocking finding remains. This approval covers the validator optimization, worker wrapper, workflow compression settings and English/Russian documentation. It retains prior exact-image safety evidence; it does not claim fresh qualification of all ten profiles.

The original deterministic replay remains intact as `_replay_pass30`. Cache reuse requires a new content snapshot including reported artifacts, intermediate membership, generated dependencies, external bootstrap certificate provenance, source/checker trees, compiler tools, include/runtime trees, cwd and environment. A changed input invokes full replay; failed replay and changed-during-replay inputs cannot populate a success entry. Unsupported snapshots fall back to the original validator without caching. No disk receipt or prior CI result grants a cache hit.

Workers use spawn, clear the requested entry, and run full inspection. The parent accepts only the expected build/toolchain key and exact replay-result shape, copies the result, then runs the unchanged assembler. Its inspections recompute current snapshots before reuse. Worker failure stops assembly. Linked-image, compiler/source, allocation, memory, runtime, test-log and release-policy checks remain outside the memoized replay. The XDATA change hoists the same artifact path conversion without removing path, duplicate, content, size or allocation checks. `build_ci_release.py`, host code and packing receipts are unchanged.

## Findings and closure

- Root directory symlinks originally differed from the stated no-directory-link policy. Root and nested links now prevent cache admission; full-validator fallback preserves original acceptance behavior. The added directory-link test confirms repeated uncached replay.
- Process context was initially absent from the snapshot. Cwd and environment are now bound; an environment-change test confirms invalidation.
- Snapshot failure behavior needed direct coverage. Missing-input and directory-link tests now confirm that successful fallback does not populate the cache.
- New worker orchestration and tests needed explicit policy coverage. All ten policies now bind the wrapper, two new test modules and both CI documents.
- A relative README link to CI documentation would not resolve in the packaged guide set. Both README links now use absolute current-main URLs.

## Verification evidence

The reviewer independently reran 13 cache tests and seven wrapper tests: all passed. Earlier review also exercised the actual wrapper help route. The retained host-discovery log reports 281 tests passed. These executions overlap with other suites and are not additive distinct-test counts.

The frozen fresh `multios` build and full qualification passed in 424.183 seconds, with 28 base suites, 331 unit tests and zero skips, plus 37 successful supplemental suites. The configuration report and runtime summary agree on a 160-byte whole-program stack bound within 171-byte capacity. Its exact IHX is `d8467f3cdd50bf6a4bca14ab1c4c05804f7bdd9a1d55a4ef589e4fdc51fa62c0`, matching the retained multios program identity. All file hashes and sizes in `local-verification.json` were independently reread with no mismatch; base/supplemental pass flags, counts and exit codes were inspected.

The real spawn benchmark records identical cold/warm inspection results: 22.974 seconds cold and 2.454 seconds warm. Two cold worker inspections took 24.273 seconds; two parent inspections took 4.347 seconds with zero additional replay calls. This verifies actual worker-result reuse. Local timings and the earlier 84-minute GitHub run use different hosts and do not establish an end-to-end release speedup.

All 9,176 policy/source/host/safety bindings and 40 retained witness records were independently reread with zero byte-hash or size mismatches. Comparison with the base confirmed identical program, host manifest, packing-receipt digest, safety program and witness records in every profile. Each safety manifest changes only the configure_firmware source record. Each policy changes seven existing source records and adds exactly five records. No source records were removed. Policy/source admission against committed HEAD is intentionally pending until commit.

The final `static-checks.json` was inspected: workflow validation, pinned Ruff correctness checks, syntax checks for 354 Python and three shell files, and 77-document validation all report exit code zero. The recorded syntax warnings concern pre-existing unrelated QMK escape sequences. These static results complement the fresh qualification; they do not establish committed-source admission.

The current test-source snapshot was independently recomputed as `bd8ce77746a7dee28e55792a20a7a35459a755075c09df9890a8b39e88ee30c2` and matches the verification record. Program-review records bind the exact policy bytes below.

| Profile | Exact policy SHA256 |
| --- | --- |
| code | `63b8746fbc47df325fb9e36bd19f4b498aa8e3079bbf5a025308951135580457` |
| creative | `01cd6b39954e97fa32e61a4250d10f983be406a2ad7d4ef0c2bba90d4d9c456c` |
| game | `722a5cd44a27e5c9226018614b119ae22852ed697dd8d328f32e2618882ca885` |
| main | `5f6b9c61a17777f85f2e88218faf36b3da93bf301ed2d8e851485be7933917b9` |
| mmo | `dccab084241d3c8c43c36f9ba260dc9aa92db4dd2943a935e684a4519a123cd6` |
| multios | `b5c3bc28f8f9ea211237c36352eb4d776003c1925049a271762021a5e631968d` |
| onehand | `1b5ce1af8f79b5836335087814fb8731a4d823956dfa8042de2f9d9388657cac` |
| pointer | `385d58fc8eee13fef49ff30f958dc499fa3b35366651e2ae120d5a41fee0b77d` |
| shortcuts | `c5cc202a5c4d346c6c6562e565e5556bab2c3f2d586f7f0eeddf86e351e2f01f` |
| typing | `b4cc20d382a9a91d76f5b83cfa5aa593f6d99c468d0f3a78e675030508fffa2e` |

## Limits and remaining gates

Fresh local firmware qualification covers multios only. The other profiles retain their previously reviewed exact programs and safety witnesses. Full ten-profile GitHub qualification, native Windows/Linux package builds, publication and committed-source admission have not been established by this review. Production committed-source checks must run after commit. Existing qualification reuse rejects the changed Python sources. No new physical device behavior is proved; hardware remains unvalidated and no device commands were sent.
