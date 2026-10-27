# Alpha2 admission correction review

Date: 2026-10-26. Independent bounded review; no implementation was authored in this review.

## Decision

The correction is accepted for source freeze and canonical requalification. No blocking defect was found in the reviewed checker, preparation change, focused tests or correction note. This is not final policy admission. Existing evidence predates the changed checker and tests and remains insufficient for final approval.

## Reviewed bytes

| File | SHA256 |
| --- | --- |
| `qmk-8051-ak820/util/ak820_release_safety.py` | `f941074b58f04454e3beb395b9db750dfd097cd375e9fbb479ddc7896493b4e9` |
| `tools/test_release_safety.py` | `db2a20023284e356da5c7a58bbf638a015e99598a15e1ee2b56610da49814531` |
| `audits/beta3-direct-20261026/prepare_release.py` | `601d858f2d7aae81cd09508955e808c6f063082b939fb23a7da28320f80becfe` |

The correction note is `alpha2-admission-fix.md` in this directory.

## Contract and evidence

The historical source is pinned to IHX `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`. The existing settings implementation assigns it no Combo version. An independent read-only validation of the actual archived alpha2 backup against the prepared main target returned 498 keys, 12 encoder assignments and `combo_entries=None`. This verifies the source condition directly; no synthetic eight-entry result was substituted.

The preparation change reads the source contract resolved by the validated profile and checks the exact source IHX, absent Combo version and actual `None` plan. Only then does it emit the typed preservation record. The recorded Combo write count remains zero. Other sources still follow their existing planning paths.

The restore implementation emits Combo writes only when the plan is not `None`. For a legacy backup without Combos, planning also retains its existing requirement that target Combo slots are default; nondefault slots cause rejection. The preservation record therefore does not authorize clearing or overwriting arbitrary existing target Combos, and it does not relax that planner restriction.

The release checker pins the exact historical source, selected target IHX and profile, source label and membership in the source-image list. Counts must be integers with exact values 498, 12 and zero; booleans are rejected. Offline success, integer zero device commands and the complete preservation object are mandatory. A Combo-capable or unrelated source cannot use this path.

The referenced preflight is loaded with the existing strict JSON parser after its SHA256 is checked. Its whole object must equal the embedded record after removing only the reference path and hash. The parser rejects duplicate fields, non-object JSON and invalid constants. The surrounding stack, startup, interrupt, source, artifact and transition-log gates remain active.

## Independent verification

`python3 -B tools/test_release_safety.py` passed all 31 tests with no skips. The focused controls cover the valid legacy plan; changed source, target, profile and label; missing source-list membership; eight writes, boolean and wrong counts; absent or contradictory preservation data; wrapper disagreement; and malformed or duplicate-field JSON with matching file hashes. Existing safety tests also passed.

The actual-backup planning check used the archived alpha2 fixture, the prepared main bundle and current trusted catalog. It opened no device and produced no restore writes. It is a bounded host check, not qualification of all ten images or a physical restore test.

## Required final closure

The changed checker and tests must be frozen and synchronized to the original build roots. Canonical qualification must run again for all ten unchanged linked images, with runtime checks before the complete base and profile suites and IHX/MAP/MEM identity checks. A fresh frozen installer suite and complete strict preparation must regenerate all ten measurement bindings, 330 ordinary plans, 100 Caps Word Combo plans, 100 macro Layer-Tap plans and policies. The canonical release-safety validator must then pass for every target before independent program approvals are written.

No production firmware, catalog, backup, policy or existing approval was edited during this review. No firmware build, device command, publication or installation was performed. Hardware validation remains false and physical device commands remain zero.
