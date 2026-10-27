# Host and release source acceptance review

Date: 2026-10-27.

Reviewed base: `fac89a85610845612ff7db34d111dae7a33a670b`, plus the six-file
working-tree correction and new `test_handoff_edges.py` inspected before commit.
The firmware acceptance report was read separately. This review owns only this report.

## Result

No remaining blocking finding was found in this host, documentation and handoff
checker scope. The reviewed correction is ready to commit with its regression
test and review records. Final merged-main and version-tag CI, exact package
identity and actual publication remain separate required checks. This report
does not approve a future CI run or a release that has not been produced.

The Counter-based checker requires all 100 expected beta.2 catalog transitions
to occur exactly once while retaining the 330-row inventory requirement. A
repeated required edge now fails even if another row is replaced to keep the
total unchanged. This corrects the earlier set-membership check. The new tests
cover complete, duplicate, missing and truncated inputs.

English and Russian handoff notes accurately distinguish the retained archive
verification from this correction. The earlier independent review is explicitly
historical; its original checker hash and results are not presented as a fresh
execution. The current source catalogs were checked, but the original delivery
ZIP and the complete revised archive checker were not replayed in this review.
The CI guides now describe manual publication on a version tag with an explicit
`qualified_run_id`, matching the workflow publication condition and reuse gates.

## Checks and evidence

Fresh independent checks:

- `python3 -m unittest discover -s audits/beta3-beta2-handoff-20261027 -p test_handoff_edges.py -v`: four tests passed.
- Source catalog comparison: installer and web catalogs are equal; 330 rows
  contain every one of the 100 expected beta.2 edges exactly once. Expected
  sources were derived from `beta2-input-fixtures.json` and targets from the
  current catalog.
- `python3 tools/check_docs.py`: 79 public documents, zero failures.
- `git diff --check`: passed.
- Current Direct host protocol and settings-capability changes were reread
  against `b35b77cddbefdb509058f1fbaaeafaa3982ce172`, alongside the retained
  host-final, release-handoff and final-generated-admission reviews. No new
  inconsistency was identified. Their build, image and archive checks remain
  retained evidence rather than fresh executions in this pass.

The fresh root-run logs were inspected at
`/home/danil/ChatGPT/ak820-release-acceptance-artifacts-20261027/`:

- `direct-host-tests.log`: 303 tests passed.
- `direct-settings-tests.log`: 186 tests passed in the completed rerun.

The initial 186-test execution failed with two errors caused by exhausted
filesystem space while writing/closing a protocol trace. That run was not
accepted as a pass. The complete rerun finished with `OK`; the affected
failure-stop test also passed. No source change was required for this closure.

Reviewed checker SHA256:
`b4d23c7bdeaaa3e64f67febc1ddcf0e37bd33ad5e32b15f528eefcc116964af8`.

Reviewed new test SHA256:
`142bcddbc550cb18cdb9f734183ddb69e243c4a96ea77d96320ce17cbf482ed8`.

## Limits

The current correction changes an offline audit helper, its tests and documents;
it does not change production firmware or host runtime. The retained firmware
review covers its own source and exact-image evidence scope. No firmware build,
heavy archive extraction, hardware execution, USB command, settings write,
reset, bootloader transition or flashing was performed in this review.

Host tests and retained CPU/static evidence do not prove physical USB timing,
LED/DMA publication, W behavior, typing, encoders, durable storage, power-loss
recovery or arbitrary-backup compatibility. Final CI must bind the actual
merged source to all ten image/package identities before publication.

## Final status wording

The subsequent changes to `docs/STATUS.md` and `docs/ru/STATUS.md` were
independently reread before commit. Both accurately record the 303 host,
186 installer/settings and four catalog-edge test passes, the 79-document
check and the retained independent reviews. Both require final merged-main
and release-tag CI before publication and preserve the physical-validation
limits. These status paragraphs are accepted within this source review;
they do not claim that publication or hardware validation has occurred.
