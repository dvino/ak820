# Nine-profile firmware catalog

Date: 2026-10-24. Input source: `570d58d`. The published alpha.3 image and its
release approval remain separate from these candidates.

## Scope and selection

The catalog offers nine whole profiles and covers all 14 existing optional
modules. It does not enumerate the 16,384 possible switch sets. Historical
profile names remain in the low-level CLI for reproduction; the desktop and
candidate builder use only `RELEASE_PROFILES`.

The default is `work`: NKRO control, One Shot, Space Cadet, Leader, Dynamic
Macros and the companion OS indicator, with the existing common functions.
It retains six layers, 16 Vial macros, an 8192-byte macro buffer and eight
Combos. Mouse Keys and Mac/PC are excluded. Auto Shift is separate because it
changes held-key typing. GUI lock and modifier swaps remain in specialist
packages. No new runtime module was added; new module development is paused.

The readable [module matrix](../../../docs/MODULE-MATRIX.md) and
[Russian matrix](../../../docs/ru/MODULE-MATRIX.md) describe profile membership.
The desktop-facing files are [firmware-matrix.json](../../../web/firmware-matrix.json)
and [module-descriptions.json](../../../web/module-descriptions.json).

## Final verification

All nine final exact images pass linked memory checks, complete runtime
proofs and full offline regression. Each passes 28 base suites, 286 unit tests
with zero skips and the profile suites below. Across the catalog there are
252 base-suite executions, 2,574 base unit-test executions and 255 supplemental
suite executions; shared tests repeat across images.

| Profile | CODE bytes | Stack bound / capacity | Stack margin | Supplemental suites |
| --- | ---: | ---: | ---: | ---: |
| `work` | 40386 | 162 / 165 | 3 | 30 |
| `essential` | 38660 | 162 / 167 | 5 | 26 |
| `typing` | 39281 | 162 / 166 | 4 | 28 |
| `mouse` | 39523 | 162 / 167 | 5 | 28 |
| `mouse-typing` | 40285 | 162 / 166 | 4 | 32 |
| `system` | 39082 | 162 / 166 | 4 | 33 |
| `tap-dance` | 40173 | 166 / 166 | 0 | 26 |
| `key-overrides` | 40464 | 162 / 162 | 0 | 26 |
| `settings` | 40075 | 162 / 166 | 4 | 26 |

`tap-dance` and `key-overrides` satisfy the current stack bound with **zero
margin**. They have no allowance for code growth without a new exact-image
analysis. The [machine summary](summary.json) binds full image and evidence
hashes and resources. [Independent artifact review](artifact-review.json)
reconstructed every row, checked all 252 base logs and every supplemental
result, and matched the exported matrix to those rows.

The candidate ZIP contains 75 unique members: 74 files plus the manifest.
Its CRC, directory equivalence and SHA256 check passed. It is 548,389 bytes;
SHA256 is `6f165df7685f72c30d80536868af5827719880b923d3cfc8e13a193f34cbbe7c`.
The generated [capability catalog](../../../web/capability-catalog.json)
also describes typed storage, active QSID values and limits for all nine
images. Match it to the selection matrix by exact IHX SHA256.


The qualification sequence is strict: inspect compiled inputs and memory;
prove the exact foreground, CRT startup and all enabled IRQ paths; then run
the base regressions and every suite required by that profile. Every explicit
unittest gate needs a positive test count and zero skips. Image and checker
identities are rechecked after tests and again before catalog export.

The stack contract sums the foreground bound, two bytes of main entry and the
conservative combined interrupt allowance. All 15 distinct-source interrupt
orders and all 256 LED selector values are checked in the CPU model. This
uses the documented SDCC/MCS-51 contract; it does not prove physical VS11K28A
USB, oscillator, flash, DMA timing or behavior during real power loss.

## Retained exact-build evidence

The reviewed source freeze is
`7125bee79af4717ac1fbafbce4652bfa102516e4`. All nine complete build trees,
listings, runtime witnesses and regression logs are retained in the
[final evidence index](final/retention.json). Each archive was reopened and
verified against its file manifest, exact image, source bytes at that commit
and runtime/profile checker snapshots. All nine checks pass.
[Independent retention review](retention-review.json) also matched all 29,145
retained files to the original build bytes and checked the final copied files.

The original qualification metadata records `570d58d` with a dirty working
tree; the compiler build report has no source metadata (`null`). These
descriptive fields are retained unchanged. Each retained record independently
binds the actual compiled and checker bytes to the reviewed source freeze.
The following evidence-only commit changes no firmware or checker input.

The [candidate ZIP](final/ak820-beta-catalog-20261024.zip) and its
[SHA256 file](final/ak820-beta-catalog-20261024.zip.sha256) are retained alongside
the full evidence. Reverification uses `retain_evidence.py verify` with the
recorded source commit and one profile directory; it does not need the
original scratch build tree.

## Small default-profile optimization

Only two production C functions changed. Dynamic Macro compaction copies its
two byte fields explicitly, avoiding SDCC's generic structure-copy helper.
The loop invariant `out <= i` makes the self-copy or earlier disjoint
replacement equivalent. Leader compares the full keycode before narrowing
its validated selector and writes the pending slot directly, eliminating
unnecessary spill storage. Prefix, timeout, release suppression, cancellation
and macro selection behavior are preserved.

| Work image | Main trailing bytes | Stack bound / capacity | Result |
| --- | ---: | ---: | --- |
| Initial ordinary calls | -214 | Not qualified | Rejected for CODE overflow |
| Initial checked short calls | 6 | 162 / 162 | Fits, no stack margin |
| Explicit Dynamic Macro field copy | 20 | 162 / 162 | 14 CODE bytes saved |
| Final Leader and Dynamic Macro changes | 22 | 162 / 165 | 16 CODE bytes and three stack-capacity bytes gained |

The final work image uses 40,386 CODE bytes and 2,676 XRAM bytes. Its low window
has 92 trailing bytes. The two CODE windows cannot exchange their spare space.
All nine curated builds use the existing independently checked short-call
transformation with pinned SDCC 4.6.0. Historical names keep their prior
short-call default. A compiler-control command must select its intended
historical profile explicitly.

Adding the OS indicator to the isolated Tap Dance, Key Overrides and QMK
Settings profiles was also measured: those probes exceeded the main window
by 198, 534 and 124 bytes. They were rejected and are not catalog images.
The OS indicator is mandatory in the chosen work profile and present in six
catalog profiles. Broader rewrites or reduced macro/layer capacities were not
needed for that default. Probe files and hashes are retained in
[optimization-probes.json](optimization-probes.json) and its accompanying
archive; these diagnostic files grant no qualification or installation status.

## Desktop and settings contracts

`ak820-firmware-matrix-1` binds profile IDs, exact Make options, linked artifact
hashes, measured CODE/XRAM/stack, dynamic entry counts and active QMK settings
IDs. Pair records describe membership in the finite catalog. An absent pair
means `no_catalog_profile`, not demonstrated source or hardware incompatibility.
The default is read from `default_profile`; the optional requirement resolver
only searches these existing packages.

`load_profile(..., trusted_catalog=...)` is additive. Its typed settings
identity binds exact IHX, permanent packed CODE, definition, schema, feature
set and supported keycodes. The permanent CODE hash covers the full
`0x2800..0xc6ff` interval, including entry, vectors and the copied OEM helper;
a hash of linked windows is insufficient. A complete validated OEM reference
was not available in this work environment. Consequently the supplied matrix
keeps `settings_identity=null`, `settings_status=not-packaged` and no cross-image
transitions. The builder can derive those identities with an explicit local
`--native-reference`; it never exports the OEM file.

Same-image restore is the catalog default. Other pairs need explicit exact
source/target IHX entries and still pass schema, enabled-module, typed-data and
source-specific keycode checks. Schema03 downgrade remains blocked; inactive
typed data cannot be silently lost. Dynamic Macro controls require physical
matrix positions. Key Override controls accept macro taps but reject macro
down/up commands that firmware ignores. Existing published image pins and
write/installation policies remain intact.

The candidate ZIP contains nine linked applications, configuration data,
qualification summaries and a SHA256 manifest. It is input for beta preparation;
it is not an installer bundle or the full evidence archive. Guide references
in the description JSON resolve from the source repository's `web` directory;
the source archive supplies those guides. The future application must bundle
and resolve its offline help when packaging the desktop client.

## Documentation audit

The feature catalog contains bilingual titles, summaries, limitations and guide
links for all 14 base and 14 optional features, plus titles, summaries and
purposes for all nine profiles. The brief summaries also introduce their
corresponding guide sections.

The audit corrected stale full-profile and profile-count claims; fixed local
links; aligned Tri Layer, Combo/tap-hold defaults, One Shot source support and
Grave Escape settings; restored interaction details lost during profile-page
simplification; and separated linked applications, candidate ZIPs, approved
installer bundles and installed alpha.3. Build examples select the correct
compiler/profile and treat the catalog output as a directory. Full qualification
examples run runtime checks before regressions.

The advanced audit checks 83 active Markdown files, local anchors, bilingual
feature/profile IDs and matrix agreement with the source registry. The existing
checker covers 69 public documents and language links, including root
CONTRIBUTING. Together they cover 84 distinct active files. Both final checks pass; their results
are recorded in the final verification summary. Syntax checks pass for 287
Python files and one shell file. Existing upstream invalid-escape warnings
remain; no executable source was changed for those warnings.

[External-link checks](external-link-audit.json) found 12 distinct external
Markdown destinations: ten resolved and none confirmed broken. Two remain
unverified: the GNU FAQ exact URL timed out; the GitHub issue-form route could
not be read through the available service. A fetch limitation is not recorded
as a 404. The exact Intel manual filename was confirmed in its directory
listing when direct retrieval exceeded the tool's file-size limit.

## Review and corrections

The [source review record](source-review.json) separates authors and reviewers.
The following findings were closed before final acceptance:

| Finding | Correction and verification |
| --- | --- |
| Dynamic Macro controls admitted from ignored sources | Matrix-only context validation; catalog settings tests |
| Key Override macro down/up incorrectly accepted | Opcode-aware macro contexts; tap remains supported |
| Requalification failed on existing test output | Replace generated results, reject symlink output, fail closed; repeated-run controls |
| Candidate export exposed incomplete output on failure | Sibling staging, all final paths preflighted, owned-output rollback and copied artifact hash checks |
| New unittest gates could succeed with no tests or skips | Enforce counts for every `-m unittest` invocation; negative logs for each gate |
| One Shot source behavior was described imprecisely | Matrix and both encoder directions can arm the queue; virtual/macro OSM retains the ordinary held-modifier fallback |
| English Grave Escape text implied fixed Alt/Ctrl behavior | Default distinguished from QMK Settings override flags; independent closure review |
| Catalog example named a ZIP as an output directory | Correct directory example and explicit ZIP/SHA sibling behavior |
| Desktop handoff still called firmware qualification future work | EN/RU text distinguishes completed offline images from future helper and physical integration |

The first work qualification stopped on the then-missing generated matrix docs
and a LeakSanitizer fatal error under the tracing sandbox. The docs and language
header were completed. The same RGB test passed outside that tracing wrapper
with AddressSanitizer, UndefinedBehaviorSanitizer and LeakSanitizer unchanged;
the complete final catalog qualification uses that environment. The first
failure and relevant logs remain in [initial-run](initial-run/).

A separate manual GitHub workflow builds the nine candidates with read-only
repository permissions and the existing pinned actions/dependencies. It uploads
one candidate ZIP/SHA and a separate compressed full-evidence CI artifact; it
has no publishing job. YAML/static checks and independent review passed.
Actionlint and a hosted execution of this new workflow were not performed.

The frozen test-source manifest also includes an unused compiler-cache experiment.
Independent review confirmed that no final build, compiler input closure, command
log or CI path uses it, and no cache sidecars exist in the nine builds. Its
unchanged bytes are retained because they were present in the tested source
snapshot. This does not enable or qualify a cache-assisted compiler pipeline.

## Release and hardware boundary

`release_approved`, `installable` and `hardware_validated` remain false for the
new candidates. Physical device command count is zero. The next installation
stage needs validated local OEM packing, the exact-image installer/release
review and physical acceptance. Desktop development can consume the catalogs,
descriptions and existing settings/protocol contracts while those separate
installation checks remain explicit.
