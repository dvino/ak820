# CI integration review — 2026-10-23

Independent review by review_fresh_ci passed for code, policy and verification
evidence. The approved policy is recorded in ../../../ci/program-review.md.
The source and document changes preserve the distinction between the installed
legacy firmware, the locally built candidate and future CI artifacts.

Closed findings: the GUI test worker now has a process deadline and is stopped
before teardown; Linux setup rebuilds hidapi with the hidraw backend and bypasses
cached wheels; syntax checks compile without executing modules; qualification
requires all 23 suite identities; packaging binds the current Git commit and
tracked source bytes; ignored LUFA headers require the pinned dependency lock;
SemVer validation checks identifiers; report paths work across operating systems.
The earlier 222-test settings paragraph is marked historical in both languages.

qualification.json records the complete successful offline run: 23 suites,
257 unit tests, zero skips, unchanged program. readonly-summary.json records
read-only diagnosis of the installed legacy image. No setting write, reset,
loader transition or firmware update was performed. Physical behavior and
power loss on the device remain untested. Native Windows and GitHub runs are
pending. Local sanitizer checks disabled leak detection; CI does not suppress it.

The initial import failure remains in ../archive-import-review-20261023; its
GUI timeout finding is closed by the process deadline and passing current run.
Generated evidence is preserved verbatim; evidence-manifest.json binds the
machine evidence files. This review text is not a machine test result.

Follow-up review, 2026-10-23: independent reviewer review_fresh_ci approved
the Node.js 24 logs and summary for run 40009482255, bilingual status/roadmap
and cancellation record. Saved log sizes and hashes match the summary; Linux
and Windows passed, publication was skipped, and the Node.js 20 warning is
absent. The final API recheck was rate-limited; retained connector logs support
this review. Palette code was removed from dev and retained only in the
independently reviewed experimental archive a68818e. Stable schema082002 and
approved host bytes were restored; offline installer verification passed.
Mod-Tap / Layer-Tap is selected next; Caps stays unchanged. This review does
not approve experimental palette installation or physical device behavior.
