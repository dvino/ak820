# Release acceptance policy review

Date: 2026-10-27.

Reviewed base: `fac89a85610845612ff7db34d111dae7a33a670b`, with the final
acceptance corrections present before commit. Result: approved for this
source and policy refresh. Final merged-main and release-tag CI and publication
remain pending. No hardware result is approved.

## Checked changes

Each of the ten release policies differs from its base only in the SHA256 and
size records for `docs/STATUS.md` and `docs/ru/STATUS.md`. Every other policy
field is identical, including image and symbol identities, host inputs and
packing receipt. The two documents accurately report the fresh acceptance
checks and require final main/tag CI before publication. The corrected CI guides
in both languages describe manual tagged publication with qualified-artifact
reuse, matching the actual workflow.

All 8,686 current source/host policy bindings passed byte and size comparison.
Present files were read directly; 31 unique sparse paths were read from base
Git blobs. The 120 external bindings are the same 12 LUFA files repeated across
ten profiles. Their actual bytes and policy hashes match the required-file
hashes in the committed LUFA lock, revision
`549b97320d515bfca2f95c145a67bd13be968faa`.

All 290 test-source and ten runtime-source hashes in
`final-source-freeze.json` match the current source. All ten unchanged IHX and
symbol identities match their existing independent program-review records.
Their test-source snapshot identities are preserved without alteration.
This review does not rebuild the images or rerun linked qualification.

The fresh firmware and host acceptance reports were read. The host report
covers the four audit-edge regression tests and 79-document check. The actual
external logs `direct-host-tests.log` and `direct-settings-tests.log` end with
303 and 186 tests respectively and `OK`. Their execution remains attributed to
the recorded root-run checks rather than a new execution in this policy pass.

The ten program-review records now bind the refreshed exact policy bytes and
this report. No policy, firmware, host implementation, test source or packing
input was authored by this reviewer.

## Approved policy hashes

| Profile | Policy SHA256 |
| --- | --- |
| main | `b98e35151dcb46f529a935cc1c2dbd2f2eed30d9bd74f726fca79771c434f776` |
| game | `3269448c5d4bce37cc0694239026d0e23495558d502c75ce82e76ae2f5d599d0` |
| mmo | `3236df2b4cceca5b4f18c9da831ee402950d6b313535ec3191c20a56040ad570` |
| typing | `0b89ca702777ef979eeb9fd4386a98229b56f70cff40b09bb534523d3df8c1e7` |
| code | `90d4c35f866b690e2fb2491033688921e2e53cf838731a5b55589c4a1e6d7c47` |
| pointer | `a3ff2b1356748046a907424501009eaca04455dfe556b07ca829cb4f251d2ba9` |
| onehand | `99db3b5af4a9543cddf826eca5fc2b7c8fec9bcbe0dbfe9fc21d346ad8540341` |
| creative | `2302c459037075db7b660736a129166e93034e0e6426f6f8496c09a7af913531` |
| shortcuts | `9c0658ad1f7e899eebcd9c5098de45e2cb366095e703317fa3720c67afc6eed7` |
| multios | `3920a0e072065214e894a3a789b224301399457f3a24c8fe6e06f37737a0c99b` |

## Limits

Historical package verification binds its recorded source and metadata; it does
not qualify a future final commit. Release publication must bind the final
merged source to all ten exact firmware and package identities. Python package
source review and host tests do not establish Windows execution, physical USB,
LED/DMA publication, W behavior, typing, encoders or durable storage.

No USB action, device command, settings write, reset, bootloader transition,
flashing, commit, push or publication was performed. Writes in this review are
limited to this report and the ten independent program-review records.
