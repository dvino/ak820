# Cleanup and dependency review

Date: 2026-10-23. Reviewer did not author the changes reviewed here.

## Decision

PASS for committing candidate tree
`b9149a71bd9812b51f7bb9342562fc224cce7f83`, subject to the separately reviewed
single-parent history procedure and verified backups. The three findings below
are closed. The exact production build has a separate passed record in
`source-trim-release-review-20261023.md`. This report's final addition is a
documentation-only change; the lead must check and stage that addition, then
record the resulting tree before committing. Other changes need renewed review.
This does not approve USB commands, flashing, publication or a Windows rebuild.
No USB commands, build, index change, commit, or deletion was performed by this
reviewer.

## Findings sent to the lead

1. The release assembler accepts only the old experimental builder hash for a
   selected SDCC 4.6 toolchain. The changed production builder therefore cannot
   assemble a fresh reviewed build through the normal path. Accept the reviewed
   production builder while retaining the immutable experimental path, and test
   rejection of changed builders and compiler binaries. Closed: the exact
   production path now passes report and input binding; alternative builders
   retain the experimental pin. All twelve assembler tests pass independently.
2. README and BUILD still describe included SDCC 4.4 and omit dependency
   restoration. The shown 4.4 build command now selects a builder that defaults
   to 4.6, so it fails its version check. Closed: README and English/Russian
   BUILD describe SDCC 4.6, LUFA restoration and the explicit 4.4 control flag.
   A doubled QMK path in the assembly example was also corrected.
3. The remaining-tree cleanup report mixes an initial proposal with completed
   removals. It says nothing was deleted, later records deletions, and disagrees
   about the erase-GUI candidate and RC4 compatibility shim. Record the final
   state or clearly date the separate phases. Closed: initial inventory and
   completed removals are identified, and the erase-GUI/shim entries agree.

## Checks completed

- Read AGENTS.md and the referenced RTK instructions.
- Reviewed the LUFA lock and installer, SDCC 4.6 installer and its tests,
  production builder changes, release assembler changes, ignore rules, current
  build/status/licensing guides, and cleanup/history review reports.
- LUFA installer: seven offline fixture tests pass. The archive hash is checked
  before extraction; links and special entries are rejected; a differing local
  directory is preserved. The lock includes the license and required headers.
- SDCC installer: eight offline fixture tests pass. Archive size/hash and six
  executable hashes are pinned. Member validation rejects traversal, duplicate
  paths, escaping links, link parents and special entries before extraction.
  Only HTTPS SourceForge redirects are accepted. A local archive does not fetch.
- Documentation checker: 29 public documents, zero broken-link/language-link
  failures. This checks links, not factual agreement.

The SDCC installer's existing-install check verifies the six executable pins,
not all library bytes. The build's exact dependency manifest must still be
validated. Its target is resolved before the symlink check: an in-repository
alias can pass, but the resolved target remains repository-confined and an
unreceipted directory is not overwritten. Neither observation is a blocking
finding for the documented pinned local setup.

## Checks still required

The exact production build independently passes all 465 source/tool input and
76 artifact checks. Its IHX is byte-identical to the reviewed SDCC 4.6 image.
The saved seven-suite offline report and its log hashes were checked; all seven
exit codes are zero. See the separate exact-build review for scope and binding.

## Final candidate tree

Independently inspected the staged tree above: 1,032 regular files, 10,337,241
bytes, no gitlinks, no untracked files and no unstaged changes. Required source,
tests, dependency installers, LUFA lock, current English/Russian guides and
root/QMK licenses are present. No toolchain, LUFA source tree, build directory,
OEM image, capture directory, executable, archive or personal backup is staged.
The retained release files are exactly the ten files under `releases/rc6`.
The source-manifest files omitted from Git are generated build files and the
twelve external LUFA headers covered by the tracked lock; no other required
source-manifest input is missing.

The active release manifest SHA256 is
`f181619c824bd93778bffe0e842d15bb0917ed5af15f65bd294ec4c461773402`.
Its sixteen host-file bindings match the current tree. Independent source
installer `verify` passed entirely offline, without loading hidapi or opening
USB. The documentation checker again passed all 29 public documents. BUILD
commands describe external dependency restoration and explicit compiler
selection. STATUS distinguishes source, fresh build, earlier Windows ZIP and
installed firmware; it correctly leaves the new full regression run pending.
The new run's intermediate failures are not counted as passes here. Existing
CPU evidence applies to the byte-identical IHX, within its recorded limits.

The history-procedure review remains a prerequisite: verify backups and ensure
the new commit has the intended sole parent. This review does not itself
change the index, references or commit history. Host and CPU results do not
establish device behavior.
