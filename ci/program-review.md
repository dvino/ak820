# Independent alpha.3 program review, 2026-10-24

The exact full-profile program and release preparation are approved for commit
and CI reproduction. Native Windows and Linux package acceptance and publication
remain pending. This review grants no permission to flash and makes no claim
about physical device behavior. Installed firmware remains alpha.2.

The reviewed application IHX is
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`;
canonical symbols are
`8c54e3a043fd636b4073aa16f328abcc53ca0f9c8430c80b5b2d664190805ce0`.
All 608 policy source records and 21 host records match current file sizes and
SHA256 hashes. All 384 retained evidence records match their hashes and sizes,
including decompressed bytes where recorded. Policy SHA256 is
`32092b9468e7474d77720e5989bbe8cf5b087f6a817cdc19719c5d278c7655ef`.

The code changes preserve the fixed transport's null-driver checks and report
handling while replacing mutable callback dispatch with direct calls. The
private Repeat guard prevents recursive delivery without changing the repeat
count exposed to the event pipeline. The LED selector masks its index to four
bits. The independently reviewed stack, startup and IRQ checks bind the emitted
program and their source contracts. Main contributes 93 control-stack bytes,
CRT entry two, and all three wrappers and callbacks 61: 156 of the allocated
162 bytes. All 15 distinct-source IRQ orders and all 256 selector values pass
in the CPU model. This proof assumes valid memory access, bank-0 SDCC calls,
private guard objects and MCS-51 in-service/RETI behavior. It does not establish
physical VS11 routing or timing.

The complete retained qualification passes 28 base suites, 273 unit tests and
zero skips, followed by 13 supplemental full-profile suites on the unchanged
image. Its SHA256 is
`cdc45835029716b8046fb0810ad9eff685401f27e2542434689fc9a38927ca8b`.
The initial fixture failure remains recorded separately. Independent reruns
passed 20 release-safety tests and 31 settings-backup tests. The package command
also passed independently against current sources, exact images, pinned tools,
base and supplemental contracts and their retained logs. This was verification
of an existing build, not a fresh independent build.

Settings support is bound to both IHX and permanent CODE, rather than schema
alone. FULL-only keycodes are accepted only for that target feature profile.
The transition witness records 47 tests and a real retained alpha.2 backup
preflight covering 498 keys, 12 encoder assignments and eight Combo slots.
Fresh backups, fresh physical confirmation, cancellation before erase and
stop-on-first-failure behavior remain. Volatile NKRO and pending One Shot state
are not restored. Offline packing records both modes and byte-equal native
recovery; private images are absent from the public receipt.

English and Russian user documentation agrees with the candidate behavior and
limits. Release notes describe user-visible additions only. The workflow builds
and qualifies FULL, and still requires both native installer jobs and checksum
checks before publication. Current bytes were compared directly because the
candidate is uncommitted; final CI must reproduce these committed inputs and
pass its committed-HEAD checks.

Physical keys, encoder rotation, USB timing, LED DMA, cold-start retention,
electrical flash faults, power-loss recovery and interactive GUI acceptance
remain untested for this image. Detailed review findings and closure are in
[audit review](../audits/rc6/alpha3-release-20261024/program-review.md).

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "32092b9468e7474d77720e5989bbe8cf5b087f6a817cdc19719c5d278c7655ef",
  "program": {
    "ihx_sha256": "d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18",
    "symbols_sha256": "8c54e3a043fd636b4073aa16f328abcc53ca0f9c8430c80b5b2d664190805ce0"
  },
  "qualification_sha256": "cdc45835029716b8046fb0810ad9eff685401f27e2542434689fc9a38927ca8b"
}
```
