# Delivery helper preflight review

Scope: bounded static review of two temporary helpers on 2026-10-26. Neither helper was executed. No source synchronization, bundle import, build, commit, network or device operation was performed. Execution receipts require a later review.

Reviewed SHA256 identities:

| Helper | SHA256 |
| --- | --- |
| `/tmp/ak820-beta3-sync-committed-origins.py` | `2fa6f83e12583365b8a4d687e11c75935fd496b252d67819aaa1170e6b8b444e` |
| `/tmp/verify-ak820-beta3-git-bundle.py` | `ee221be1004c7108ffc3c8124a2edc026e129463d63da4deaad18861a63f766d` |

## Findings

Status: closed for static preflight. No remaining blocker was found in the corrected helpers for the owned, non-concurrent task workflow. Actual synchronization and import receipts remain outside this review.

Sync closure: corrected helper SHA256 `f4c27f7ea0700eab66bdd869ac8dfa4c26025970e42019b0db5c1ffc99f06296` was read without execution. Findings 3 and 4 are closed for the owned, non-concurrent task workflow. Both removal and copy paths now use `owned_path`, which rejects symlink components and checks the real origin path. A fresh receipt guard runs before mutations, and exclusive creation prevents overwriting an existing receipt. The sync helper has no remaining blocker in this bounded static review.

Verifier closure: corrected helper SHA256 `90aa91b3a4ef60be2a1b9e2edf13faeb1c8ef003be41b7703083a430e466fa6c` was read without execution. Findings 1, 2 and 5 are closed. The helper compares exact whitespace-separated identity/ref pairs, no longer requires a symbolic branch in the bare baseline, and checks a version 2 header with exactly BASE as prerequisite and the expected final branch/head as its sole exported ref. The destination ref must be absent before fetch. Final-HEAD absence requires successful `cat-file --batch-check` and exactly `HEAD missing` followed by a newline; the command, stdin, return code and outputs are recorded. This avoids treating an arbitrary Git error as proof of absence. Exclusive receipt/log creation and post-import commit/tree/fsck checks remain present. No actual baseline import was performed during this review.

1. The verifier compares `git bundle list-heads` output to a tab-delimited string. Git emits a space between the identity and ref. Parse exactly two whitespace-separated fields and compare the resulting pair. Otherwise the valid bundle fails.
2. The verifier requires the bare baseline's symbolic HEAD to name `codex/beta3-direct-w`. Read-only inspection found `refs/heads/master`, with no resolved HEAD. The prepared bare object baseline therefore fails before import. Validate the intended baseline object state independently of the exported source branch, or explicitly prepare the expected baseline ref before use.
3. The sync helper's deletion loop checks the leaf for symlinks but not its ancestors. A symlinked ancestor could direct an unlink outside the owned origin. The origin itself is also not checked for symlinks. Check containment and all path components before every mutation, including removal. The three inspected origin directories and their shared parent were ordinary directories at review time.
4. The sync receipt uses `write_text` at a fixed path. It can replace prior evidence or follow a symlink. Require a fresh receipt and exclusive creation.
5. The verifier checks BASE presence and ancestry but does not inspect the bundle prerequisite header. Make the intended export contract explicit and validate it: the exact BASE prerequisite for an incremental bundle, or no prerequisites for a full bundle. A successful `bundle verify` alone does not establish that export boundary.

## Checks already present

The sync helper validates tracked working bytes against committed blob identities before copying, restricts tracked modes to regular files, copies ordinary source files, shares only final-evidence tar archives, and resets each owned index and HEAD after synchronization. It does not clean ignored build outputs.

The verifier records commands, return codes, stdout and stderr; checks final HEAD absence before verification and fetch; imports an explicit branch ref into an owned namespace; compares imported commit and tree identities; runs full fsck; and writes receipt and log files with exclusive creation. Its receipt includes the required status, base, head, bundle SHA256 and source commit fields. These are static observations, not executed PASS evidence.

The baseline metadata identifies BASE `b35b77cddbefdb509058f1fbaaeafaa3982ce172`, declares no alternates and no future commit objects. The separate base-pack inventory and base-object list were inspected. The actual final-HEAD absence gate remains to be executed after final commits exist.
