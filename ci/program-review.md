# Independent program review — 2026-10-24

The exact tap-hold and C/W program policy, packing receipt, legacy installer
host bindings and complete offline qualification evidence are approved for
CI reproduction. This review did not author the production implementation,
policy, packing receipt or qualification run. Source/ABI and settings reviews
are retained in `audits/rc6/`.

All 615 policy source records, 21 shared host records and nine retained legacy
bundle records matched their current sizes and SHA256 hashes. The policy binds
IHX `45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`
and symbols `11e50e3e0d6e1e9831d4ca85822a65306907753bed5000f7d4301f69af8ade06`.
All 468 build input records and 78 build artifact records matched actual bytes.
The legacy bundle keeps its earlier firmware; its review, manifest and installer
approval bind updated host source without selecting the new image.

The complete qualification passed all 26 required suites, 258 unit tests and
zero skips with unchanged IHX/MAP. The suite contract, pinned tools, all 26
saved log hashes and retained evidence manifest were checked independently.
The 12 RGB and 11 indicator observations match expected values. All 65 linked
tap-hold cases match expected snapshots and supplied report traces. An
independent 23-test settings run and production profile loading of the actual
packed program also passed. Final documentation agrees with these scopes.
Evidence is retained in
`audits/rc6/oem-indicators-qualification-20261024/qualification.json` and
`audits/rc6/oem-indicators-final-integration-review-20261024.md`.

This approval covers offline reproduction of this exact program and reviewed
host source. It does not establish successful public CI, fresh bundle
acceptance, native interactive Windows acceptance, physical C/W connections,
key/encoder timing, USB behavior, IRQ overlap, durable storage, reset execution
or a new installed image. It grants no permission to flash. LeakSanitizer was
excluded; ASan/UBSan remained active. The macro cancellation case uses a
disclosed simulator hook. Private OEM inputs and images remain outside Git.

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "93f60dcf6ac827c2315e88fff8fd266168585aaf330429128900954a3f2184b7"
}
```
