# Independent program review — 2026-10-24

The exact compact tap-hold program policy, packing receipt, legacy installer
host bindings and complete offline qualification evidence are approved for
CI reproduction. This review did not author the production implementation,
policy, packing receipt or qualification run. Scoped independent source,
fixture and settings-profile reviews are retained in `audits/rc6/`.

All 614 policy source records, 21 shared host records and nine retained legacy
bundle records matched their current sizes and SHA256 hashes. The policy binds
IHX `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`
and symbols `9854215cfd08ae2e70fb5f30ba65be76af8880e893a0a8f85658a63ea870ac6c`.
All 467 build input records and 77 build artifact records matched actual bytes.
The legacy bundle keeps its earlier firmware; its review, manifest and installer
approval hashes bind the updated host source without selecting the new image.

The complete qualification passed all 26 required suites, 258 unit tests and
zero skips with unchanged IHX/MAP. The exact suite contract, pinned tools and
all 26 saved log hashes were checked independently. The corrected linked
65-case report matches all expected snapshots and supplied report traces.
The retained qualification is
`audits/rc6/compact-tapping-qualification-20261024/qualification.json`.
Findings and closure are recorded in
`audits/rc6/compact-tapping-final-integration-review-20261024.md`.

This approval covers offline reproduction of this exact program and reviewed
host source. It does not establish a successful dev CI run, native interactive
Windows acceptance, physical key or encoder timing, USB behavior, interrupt
overlap, durable storage, reset execution, a new installed image or permission
to flash. The macro cancellation case uses a disclosed simulator hook. Private
OEM inputs and packed images remain outside Git and CI.

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "01ce9857aad8c36a32a93a25650e56d198e82d8454e60ae279dd5885b1f90781"
}
```
