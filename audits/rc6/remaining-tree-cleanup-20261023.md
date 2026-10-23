# Remaining-tree cleanup audit

Date: 2026-10-23. This report records the pre-cleanup inventory and the bounded
cleanup later authorized by the coordinating agent. Removed files were copied
to the verified external backup recorded below before removal. Inventory counts
describe the pre-cleanup snapshot. No build, test, USB operation, index
generation or commit was run for this cleanup.

## Snapshot and boundaries

Current file count and bytes were measured from the working tree, including
ignored files where present, before the bounded removals recorded below. The
main data-bearing areas are:

| Area | Files | Bytes | MiB | Treatment in this audit |
| --- | ---: | ---: | ---: | --- |
| `.build` | 9,602 | 319,205,436 | 304.37 | Build output; leave untouched |
| `dist` | 6,711 | 340,100,328 | 324.25 | Protected; leave untouched |
| `qmk-8051-ak820` | 36,056 | 1,262,978,833 | 1,204.59 | Firmware and upstream tree; leave untouched |
| `toolchains` | 4,416 | 278,361,583 | 265.42 | Installed toolchains; leave untouched |
| `host/runs` and `host/windows` | 469 | 36,693,377 | 34.99 | `host/runs` retained; obsolete `host/windows` archived and removed |
| `releases` | 722 | 30,237,066 | 28.84 | Audit below; no changes |
| `docs` | 110 | 5,797,734 | 5.53 | Audit below; no changes |
| `audits` | 85 | 2,395,541 | 2.28 | Audit below; no changes |
| `evidence` | 20 | 541,620 | 0.52 | Preserve private and failure evidence |
| `tools` | 100 | 951,556 | 0.91 | Classify below; no changes |

The pre-existing `git status --porcelain --untracked-files=all` snapshot had
44,229 path entries: 39,966 worktree deletions, 4,061 index deletions, 158
untracked files and 44 modifications. Most entries are under the QMK tree,
toolchains and history. This audit did not stage or change those entries. The
local compiler addition remains outside this audit's ownership.

`host/runs`, `dist`, `.build`, `qmk-8051-ak820`, both current release candidates
(`releases/rc6` and `releases/rc6-sdcc46-breathing-20261023`), and active
installer, build, device-regression and firmware sources were left in place.
The distinct `releases/rc6-erase-gui-20261023` candidate and its reports were
archived and removed as specifically authorized.

## Current entry points and live dependencies

- `AK820.cmd` and `AK820.sh` dispatch to `tools/installer/ak820.py`. Keep both
  wrappers and the source GUI/CLI implementation in `tools/installer/`.
- `tools/build_release_bundle.py` produces the reviewed source bundle;
  `tools/build_windows_installer.py` packages the approved release. Their
  fixture suites are `tools/test_build_release_bundle.py` and
  `tools/test_build_windows_installer.py`.
- `tools/test_keyboard.py` is the combined offline regression entry point. It
  calls installer tests, both packaging suites, its own runner test,
  `tools/test_ak820_device_tests.py`, the QMK package tests and `tools/check_docs.py`.
  With explicit options it also dispatches host and linked-CPU suites under
  `qmk-8051-ak820/tests/`; those are in the protected firmware tree.
- `tools/ak820_device_protocol.py` and `tools/ak820_device_tests.py` are the
  live read/test protocol path; `tools/test_ak820_device_tests.py` tests it.
  Keep these files. Default execution is designed to plan/read only; setting
  writes have separate explicit gates.
- `tools/check_docs.py` backs the documentation checker called by the combined
  runner. `docs/INDEX.md` links the current user guides, `docs/STATUS.md` and
  `docs/ROADMAP.md`; the Russian guide set mirrors the English set.
- The root `LICENSE`, `qmk-8051-ak820/LICENSE` and component-specific notices
  have distinct scopes. Keep the QMK and third-party license files with their
  upstream source. The root `COPYING` and `COPYING-GPLv3` have already been
  removed in the existing worktree; `docs/LICENSING.md` identifies root
  `LICENSE` as the project license. Do not remove `qmk-8051-ak820/LICENSE`,
  `license_GPLv2.md`, `license_GPLv3.md`, `license_Modified_BSD.md`, or nested
  LUFA license copies as “duplicates.”

The thin `tools/build_rc4_bundle.py` and `tools/test_build_rc4_bundle.py` were
compatibility shims into the current release builder/tests. Static searches
found no current callers, so they were archived and removed with the standalone
`tools/verify_repository.py` verifier. Invoking those old names is no longer
supported.

## Reports, old material and stale links

The three old protocol/configurator/recovery notes formerly under
`docs/history/` were already absent from the working tree during this sweep
(their directory was empty). They are not linked from the current
`docs/INDEX.md`. Do not restore them as part of this cleanup; confirm the
earlier source-trim backup contains any unique uncommitted material before the
parent commits those existing deletions.

Before cleanup, `docs/` contained 110 files (about 5.53 MiB), including many
generated research JSON reports that are not in the current guide index.
Several were large embedded-source snapshots: `qmk8051-iram-libraries-audit.json`
(788,764 bytes), `qmk8051-opt-code-size-checks.json` (800,345), and three IRAM
audit snapshots at 773,410 bytes each. These were historical experiment
evidence, not routine user documentation. The 81-file JSON set was archived
with its matching old research scripts after checking guide links and retained
test/build entrypoints.

Before removal, some machine reports demonstrably described files no longer
present:

- `docs/firmware-inventory.json` records inputs under the removed `firmware/`
  tree and old root scripts such as `tools/build_fn_layer_candidate.py`,
  `tools/flash_candidate.py`, and `requirements-ak820.txt`.
- `docs/movx-addressing-evidence.json` records old script paths including
  `tools/check_startup_decoder.py` and
  `tools/build_vial_readonly_dispatcher.py`.
- `docs/qmk8051-source-provenance.json` referred to root `COPYING`; that file
  was already absent, and the same report recorded upstream paths that were
  404 at collection time.

`docs/firmware-inventory.json` and `docs/movx-addressing-evidence.json` were
historical snapshots, not current build inputs, and had no inbound references
from current guides or runtime tools. Both were copied and verified in the
external backup listed below, then removed. Static search found that the old
`tools/probe_qmk8051_toolchain.py` reads `docs/qmk8051-source-provenance.json`;
that tool and report were archived and removed together. The retained
installer, package builder and device regression entry points do not import
this research toolkit or JSON set. Current Markdown guides were searched for
links to those JSON reports before removal; their contents were not edited or
represented as regenerated.

At first inventory, `audits/rc6/` had 72 pre-existing files / 2,365,295 bytes
with current release, installer, device and optimization reviews linked from
the status/roadmap. Current RC6 audit material was retained. The separate
`audits/rc1-independent/` directory had 13 files / 30,246 bytes with the older
external review and fixtures; it was archived and removed. `evidence/` contains 20 files /
541,620 bytes, including OEM and failed-run material; preserve it and keep it
out of public bundles.

## Releases and package copies

| Directory | Files | Bytes | Finding |
| --- | ---: | ---: | --- |
| `releases/rc1` | 31 | 698,081 | Historical package and independent evidence; archived and removed below |
| `releases/rc2` | 229 | 8,713,564 | Historical package plus substantial audit evidence; archived and removed below |
| `releases/rc3` | 272 | 11,458,545 | Historical package, source and audit evidence; archived and removed below |
| `releases/rc4` | 86 | 1,122,133 | Immutable prior release; archived and removed below |
| `releases/rc5` | 74 | 6,983,190 | Historical release/review; archived and removed below |
| `releases/rc6` | 10 | 428,914 | Required by current defaults/tests and live test examples |
| `releases/rc6-erase-gui-20261023` | 9 | 402,626 | Distinct candidate; archived and removed |
| `releases/rc6-sdcc46-breathing-20261023` | 10 | 428,914 | Exact duplicate of `releases/rc6` at audit time |

The two 428,914-byte directories have the same SHA256 for all ten files: the
IHX, MAP, MEM, release manifest, both reference JSON files, both reports, the
reproduction builder and independent review. The IHX hash in both is
`f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`. This is
strong evidence for a de-duplication candidate, but their directory names carry
different release meaning. `releases/rc6` is consumed by the device-test
default, its tests, release-builder default and installer tests. The
versioned directory is named in current status/release evidence. Keep both
until the owner chooses the canonical path and the tests/defaults/docs are
updated together; do not remove either as part of this audit.

RC1–RC5 were historical release snapshots, not current installer defaults.
Current source/package code did not read them as runtime files. The RC4
compatibility builder was removed; some RC5 example paths remain in docs for
an OEM-reference folder convention, which the parent is aligning. The
referenced `stock-full.bin` is expected in the owner’s private OEM archive,
not in the checkout. These historical releases included evidence beyond the
firmware binaries; the complete remaining directories were archived together
before removal.

`dist` contains 6,711 files / 340,100,328 bytes and is explicitly outside this
pass. The English/Russian BUILD, INSTALL and TESTING guides still describe the
superseded `dist/rc6-physical-gui-20261023/`; status documents retain it as
history while naming the newer SDCC 4.6 package. The parent owns aligning the
current user instructions. No file under `dist` was changed.

## Licensing and upstream copies

The root now has one license file, `LICENSE` (35,823 bytes). The deleted root
`COPYING` (GPL-2 text) and `COPYING-GPLv3` (GPL-3 text) were separate license
texts; both were preserved in the earlier verified license backup. Their
removal followed the prior licensing review, while `docs/LICENSING.md` points
to the root project license and QMK/component licenses remain.
`README-vial-upstream.md` was also removed in the existing worktree; it had no
current guide link in the searched entry points.
Do not remove the maintained QMK fork’s own license files or LUFA’s nested
license texts. They accompany third-party code and are not redundant project
copies. The large generated JSON audit reports embed upstream snippets and
license notices; that is another reason to archive or remove the whole obsolete
report set coherently, not strip notice text from individual snapshots.

## Safe next cleanup groups

1. **Already completed in this bounded cleanup:** after external backup and
   per-file SHA256/size verification, removed `releases/rc1` through `rc5`,
   `releases/rc6-erase-gui-20261023`, `host/windows`, the three compatibility /
   verifier scripts, the historical docs JSON set and `audits/rc1-independent`.
2. **Already executed in the pre-existing worktree:** root license texts,
   upstream README and a broad old-doc/history set are local deletions. This
   audit did not expand or reverse those deletions. Reconcile remaining report
   references before committing.
3. **Release de-duplication:** after choosing one canonical RC6 path, update
   builder/test defaults, device-test defaults, test fixtures and both language
   versions of affected docs, then re-verify the manifest and package against
   the canonical directory before removing its exact duplicate.
4. **Residual release index:** `releases/HASHES.json` remains and is referenced
   by `audits/rc6/public-artifact-scope-review.md`. Its RC1–RC3 entries point to
   archived releases; its OEM/failure-evidence entries still describe retained
   evidence. Keep it until the audit owner decides whether to preserve it as
   historical evidence or revise that review/index pair.
5. **SDCC 4.4 helper:** retained for control builds and the s51 simulator. Its local report now goes to ignored host/runs/sdcc44-toolchain-checks.json instead of the retired docs JSON.

## Completed archive and verification

The following removed material was copied to
`C:\Users\vinok\Documents\Codex\AK820-private-backups\20261023-remaining-tree-cleanup\`:

| Archived group | Files | Bytes |
| --- | ---: | ---: |
| `releases/rc1`–`releases/rc5` and erase-GUI candidate | 701 | 29,378,139 |
| `host/windows` | 12 | 54,541 |
| Compatibility/verifier scripts and old research toolkit | 45 | 271,255 |
| Historical docs JSON reports | 83 | 5,576,958 |
| RC1 independent review and fixtures | 13 | 30,246 |
| **Total archived source files** | **854** | **35,311,139** |

`backup-manifest.tsv` lists each archived relative path, byte count and SHA256.
All 854 entries were re-read from the backup and matched the manifest; the
archive contains 855 files including the manifest. The manifest SHA256 is
`39355c3dbb91deb33a75b674d64cdc91ae293f23c98bbeb005ccc09af5b46c43`.
The removed release data is therefore preserved outside the checkout, not
discarded. The distinct erase-GUI candidate and its recovery/review data are
in that same verified backup.

After removal, each authorized target path was checked absent. Protected
`releases/rc6`, `releases/rc6-sdcc46-breathing-20261023`, `dist`, `host/runs`
and `qmk-8051-ak820` remained present. No build, test, USB operation, indexing
or commit was run for this cleanup.

The bounded source removals above were authorized by the coordinating agent
after backup verification. Protected build, output and live device-session
paths remain outside the cleanup.
