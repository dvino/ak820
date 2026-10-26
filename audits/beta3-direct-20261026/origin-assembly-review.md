# Original-root assembly review — 2026-10-26

Result: the reviewed helper is suitable for the planned offline assembly after
the helper, catalog and per-profile authorization inputs are reviewed, committed
and synchronized into every original root. No unresolved blocking finding was
identified in the final bytes below. This review does not approve any firmware
image, policy, physical operation or publication.

## Reviewed source

SHA256 values:

| File | SHA256 |
| --- | --- |
| `assemble_origins.py` | `c1171ab75e5787c1d0f896fbdfd770807048f6e149e136488f4f51f841b586da` |
| `test_assemble_origins.py` | `ced2063964eeac011b159b38e40f42fcf8683fb87e288c10787abb0249b22181` |
| `tools/build_ci_release.py` | `89b72e2860e4ada4a2c1f00984beeb623bfa9d0c63278954769ab51d3d67bfe3` |
| `tools/build_capability_catalog.py` | `6e28dbb11bacfdaa491a23cef60c03341261508fe8549569dbd6c2b37e6a3e3b` |
| `tools/installer/ak820.py` | `6ce93cce23a6b8fc5be0032ad46eb7c7034cc23131de8a1c5985354ada474c22` |
| `tools/build_beta_release_assets.py` | `93f4315c47c7563b6486cc2b6520fdfaa3dc460fd7ca6d80fd278366089ab663` |
| `measure_origin.py` | `e8e366c04d7bd27dde984489aafa2bd31cd6091c9110d3d627571abb40c71bca` |

The first, second and last paths are relative to this report's directory.

## Gate comparison

The helper preserves the `settings_matrix_from_builds` checks for the exact ten
ordered profiles, configuration, complete exact-image qualification, static and
reproducible identities, schema, current and historical image set, and false
candidate approval flags. Each worker reconstructs its row through canonical
`firmware_matrix.measured_row` in the original build root. It reconstructs the
capability row through canonical `inspect_entry`, whose inspection validates the
pinned tools. The merge checks complete unique profiles, exact build identities,
unique IHX and CODE hashes, and development-only capability flags.

Every worker calls canonical `ci.assemble(expected_profile=...)`. Committed
policies, program reviews, packing receipts, source commit, current host code,
qualification and approval generation remain subject to that gate. The helper
does not generate authorization inputs or bypass their validators.

All roots must have the same committed tree and exact working-file bytes.
Protected repository paths reject symlinks. Central and original build trees
must match before assembly and remain unchanged afterwards; workers also check
their own source and build trees around assembly. Copied bundles must equal the
worker's measured bundle tree byte for byte before aggregate output is accepted.

The copied bundle loader is adequate for this stage. `_load_release` with
`approved=True` validates manifest file sizes and hashes, linked IHX/MAP/report,
current host manifest, independent review binding, CI policy and program review,
attestation and qualification contracts, and approval of the exact manifest.
`beta.validate_profile_links` additionally binds the matrix and capabilities to
the copied approved images, configuration, features and CODE identities. Calling
`beta.validate_bundle` here would incorrectly require its pinned beta.1 work
image and central beta.1 policy; the replacement retains the relevant checks
through the per-profile canonical assembly and loader paths.

Aggregate output uses a private temporary directory and a final rename after
source/build stability checks. Archives preserve bytes with sorted entries and
fixed metadata. No device operation is part of this path.

## Finding and closure

The initial version checked worker sibling freshness with `exists()` alone.
A dangling `.worker.json` or checksum symlink could pass preflight and later be
followed by a write. Direct worker mode also lacked the same preflight.

The final version uses `require_fresh_worker_output` for both orchestrator and
worker entry. It rejects existing paths and dangling symlinks for the output,
archive, checksum and worker metadata before measurement or assembly. The
aggregate output also checks both conditions before final rename. The new
negative control rejects all three dangling sibling paths without changing the
link or creating its absent sentinel target. This finding is closed for the
reviewed bytes.

## Verification and limits

`python audits/beta3-direct-20261026/test_assemble_origins.py` passed all nine
tests independently after the correction. The suite covers invalid origins,
path traversal and symlinks, incomplete or reordered catalogs, unqualified
rows, stale identities/configurations, false approval flags, incomplete worker
sets, changed source or missing committed helper, dangling output siblings, and
deterministic byte-preserving archives.

This was static code review and focused host testing. It did not execute a
complete ten-profile assembly, rerun firmware qualification, approve pending
policies, publish a release or access a device. A later successful assembly must
retain its actual worker reports and logs. The helper remains audit-only; this
review does not propose replacing the canonical release tooling.
