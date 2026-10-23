# Archive import review

Reviewed snapshot: `0573016`, compared with `c0c704e`.
Archive SHA256: `c8b138fb4db7caac64ceaa2108e08ddcd1a4024d19b07c8c22318396d4e463ec`.

Independent static review covered settings, protocol gates, GUI, packaging,
runner, private journal pointer and related documentation. No production
defect was confirmed in the reviewed paths. ZIP extraction lost 36 executable
modes; import from the embedded Git snapshot restored them. Imported content
matches the snapshot. All 68 qualification-manifest entries match size/SHA256.

Local offline run: 15 of 17 suites passed; 244 unit tests ran with two skips.
Installer verify passed without HID. SDCC/s51 are absent; linked CPU tests
were not repeated. USB harness compilation failed because external LUFA is
absent. Archived qualification remains evidence from its original environment.

Open P2: `tools/installer/test_settings_workflow.py:223–224` waits only 20
seconds for the GUI worker. The local run exceeded that limit. Failure tears
down temporary files and mocks while the worker remains active, which can
affect subsequent tests. Independent follow-up review confirmed this finding.
A fix must keep a bounded deadline and terminate the worker before teardown.
This failure does not establish a production deadlock.

Local report and logs are retained beside this review. No build or device
operation was performed. Imported files are staged; no commit was created.
The test finding remains open.

Dated closure, 2026-10-23: the P2 timeout finding above is resolved. The GUI
model now runs in a child process with a bounded parent deadline and verified
termination before teardown. Current full qualification passes 23 suites,
257 unit tests and zero skips. See ../ci-integration-20261023/qualification.json
and ../ci-integration-20261023/review.md for current evidence and review.
The earlier environment and failed run above describe the initial import only.
