# Hosted tap-hold CI review, 2026-10-24

Result: PASS. No blocking findings remain in the reviewed CI evidence and documentation changes. This review covers the retained reports in this directory and the current English/Russian STATUS, TESTING and ROADMAP changes. It does not approve the separate indicator implementation or a hardware update.

## Evidence checked

The live GitHub result for [run 40026118029](https://github.com/dvino/ak820/actions/runs/40026118029) reports commit `586ac209817436ac937426045920a466a6432488`, completed Linux and Windows jobs with success, and skipped publication. It agrees with `github-run.json`.

The downloaded Linux ZIP has SHA256 `c5534fd9ca98e69185207490b209384790e2f94e9238189e8f8a6c4579c98aed`. Every file in the ZIP matches the extracted fresh bundle. The qualification report matches the retained copy: all 26 suites returned zero, 258 unit tests ran, and none were skipped. The IHX hash is `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`. The real installer `load_release(approved=True)` accepted this fresh bundle with its exact approval file. Only the bundle and approval paths were selected; no HID guard or validation replacement was used.

The downloaded Windows ZIP has SHA256 `6c14e70408bf29c75c68733aa2784472fcee6b2fad76e66afdf01f32502e2dcf`. Both EXE hashes match `windows-check.json`. All 36 approved input hashes were recomputed from the ZIP for each application. Every fresh Linux bundle file, including the approval file at its packaged path, is identical in both application directories. The packaged provenance and smoke reports match the retained copies. The Windows report records passed CLI help, offline verification and native Tk startup. The live job result confirms that its native package-build-and-smoke step passed. No Windows EXE was executed on Linux during this review.

The evidence-manifest hashes passed before this review file was added. Regenerate the manifest to include this file before committing the evidence package.

## Documentation and limits

The English and Russian changes agree on the run, commit, suite counts and startup checks. STATUS states that the candidate is uninstalled and that indicator implementation is a separate current work item absent from this CI image. TESTING and ROADMAP keep visible Windows dialog acceptance and physical behavior open. The archive check and source-derived indicator analysis are linked without claiming verified physical C/W connections.

These results prove hosted builds, offline qualification, package contents and recorded native startup checks. They do not prove USB behavior, visible dialog interaction, keyboard behavior, durable settings storage or a successful physical update. No source build, USB operation, reset, bootloader transition or flash was performed in this review.
