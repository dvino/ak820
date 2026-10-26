# Beta.2 exact program evidence review

Review snapshot: 2026-10-26, HEAD `feeff6fe6dfc98fa2f3857849adb0a446bb93dc3` with current working files. Result: no actionable defect established in the inspected evidence; final program approval is pending. No per-profile program approval is created by this report.

This independent review authored none of the implementation, policies or input proofs. Only this report was written. Inspection was read-only apart from this report; no builds, regression reruns, USB access, device commands, packaging, commits or publication were performed. Plain, impersonal wording follows repository instructions and the writing-style skill; retrieval tools were unavailable, so no retrieved style match is claimed.

## Exact identities and safety witnesses

All ten current `ci/profiles/<id>/release-policy.json` source records match actual file sizes and SHA256 values. IHX hashes and normalized linked-symbol hashes match the original qualified builds in groups a, b and c. Copied foreground, startup and IRQ report bytes match the corresponding originals. Every foreground listing hash and map hash was also checked against those builds.

`ak820_release_safety.validate` passed for each profile with current repository source/witness records. Artifact reads alone were routed to the original qualified build trees, checking each recorded size and SHA256 before use; no file was copied or altered for this check. The normal final committed-tree admission remains required.

| Profile | Whole-program bound | Linked capacity |
| --- | ---: | ---: |
| main | 160 | 168 |
| game | 160 | 167 |
| mmo | 164 | 167 |
| creative | 164 | 168 |
| typing | 160 | 172 |
| code | 160 | 172 |
| multios | 160 | 171 |
| pointer | 160 | 172 |
| onehand | 164 | 172 |
| shortcuts | 164 | 172 |

Each report covers foreground, pre-main entry and all enabled IRQ callbacks without unresolved roots. All 15 distinct-source IRQ orders and 256 selector inputs are recorded. Analyzer, decoder and checker identities agree with current source. Capacity agrees with actual linked stack placement. These are static and CPU-model results under the recorded ABI/peripheral assumptions; physical timing, power loss, durable storage and hardware behavior are not established.

## Packing, transitions and source closure

Each policy binds its actual packing receipt. All ten permanent images, ten trial images and ten recovery images match the actual private preflight file sizes and SHA256 values. Each recovery image is byte equal to the original OEM full-ROM application slice `[0x2800:0xEFC0]`. The private pinned archive manifest verifies 128 of 128 entries. No private bytes or backup payloads were copied into this report or the public tree.

The transition matrix contains 120 passed offline cases: ten self transitions, ninety cross-profile transitions, ten archived alpha.2 ROM cases and ten beta.1 packed-work cases. Each target IHX and schema agrees with its profile evidence; packed defaults and archived ROM derivation remain explicit. This does not establish a new device capture or live restore result.

The supplied settings run records 69 successful host tests; the host-tools run records 260 with no skips. Both logs match their pinned hashes, and all recorded source hashes match this snapshot. The transition implementation/test closure is accepted by the current safety validator. The policy includes all 70 explicit public guide files. Program policy, packing receipt and safety dependencies do not include final program-review output or their own policy bytes; no approval/hash cycle is introduced by this layout. Existing independent source reviews cover the policy helper and CI catalog changes; their scope does not substitute for final program evidence.

## Remaining gates

Full regression is still running in the original qualified build trees. Partial results are not a completed ten-profile qualification. Before final per-profile records can be written, all ten final qualification reports must pass and bind their actual image, source manifest, runner and retained evidence. The current docs/status and measured web catalogs must finish their final update and receive agreement review. Any resulting source/witness drift requires regeneration and scoped independent review.

The final policies and packing receipts must then be checked again against the frozen tree, including guide closure and final settings/host records. Final per-profile program reviews require this completed evidence. Integration with the intended main branch, clean committed-input CI assembly, native package smoke checks, final package/catalog guide closure and publication identity remain separate release gates. This report authorizes none of those external actions and no device operation.

## Follow-up: broader policy source closure

The helper delta at SHA256 `d060f04542188eecf1ffc63d3fa80001d635ab488f93cc23b9c88ef507745c86` adds runtime-summary source names to safety records and `configured.test_source_snapshot()` to program policy records. The current snapshot contains 280 source/fixture paths, including `configure_firmware.py`, `firmware_matrix.py` and `build_capability_catalog.py`. It excludes generated policies and review outputs, so this expansion does not create a policy/review hash cycle. This closes the identified coverage omission in the proposed generated policy inputs after regeneration.

**Finding P2 — reject stale runtime source hashes before regenerating safety records.** The helper currently takes only the keys of `summary['source_files']` and records fresh current hashes. It does not compare those hashes to the source hashes retained by the runtime summary. A stale summary can therefore supply path names while the regenerated safety record claims current sources. At this follow-up, retained main runtime evidence differs from current `ak820_emitted/run.py`; the expected fresh preflight is still pending. Require every recorded runtime source hash to equal the actual safe repository path hash before copying witnesses and creating safety records. A final manual check remains necessary even after this fail-closed helper condition is added.

The earlier no-defect conclusion applies only to its prior inspected snapshot. This finding and all final regression, refresh and approval gates remain open. No final per-profile approval is granted.

## Scoped closure: stale runtime source rejection

The stale-source P2 is closed at source by helper SHA256 `a3eca67e2cdfdee2512efa45b77128244e298032a49a073fc149dc299edb5106`. Immediately after checking runtime pass and IHX identity, the helper now compares every retained runtime source hash with `digest(safety.safe_path(ROOT, name))`. A mismatch raises an error before copying witnesses or generating that profile's records. Safe-path validation also rejects missing files, escaping paths and symlink components. The previous fresh-hash relabeling path is therefore blocked for a stale recorded runtime source.

This closure is based on independent source inspection. The helper was not run while fresh preflights were writing their outputs. Final copied runtime evidence, regenerated policies and all ten completed qualifications remain unapproved until the stable final snapshot is available for review.
