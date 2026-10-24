# Independent alpha.3 release review, 2026-10-24

The exact candidate is approved for offline release preparation, commit and CI
reproduction. No blocking code or release-preparation finding remains. Native
installer acceptance and publication remain pending; hardware is not validated.
The machine approval and exact identities are in
[program review](../../../ci/program-review.md).

The review covered firmware changes, settings compatibility, the safety gate,
qualification contracts, source policy, packing receipt, release workflow and
English/Russian documentation. The author of this review did not implement the
candidate changes. No build or USB command was issued during this review.

## Verification

- All 608 policy source records and 21 host records match current bytes and sizes.
- All 384 retained evidence records match stored sizes and hashes, including
  decompressed bytes where recorded. The 450 available build source paths match
  their recorded hashes; the package verifier separately checks the complete
  build input and toolchain contract.
- The retained base report has 28 distinct required suites, 273 tests and no
  skips. Its exact-image and pinned-toolchain checks pass independently.
- The independent package eligibility command passes for the existing
  `qmk-8051-ak820/.build/alpha3-release` build. It validates the 13 supplemental
  suites, source snapshots and log contracts alongside the base qualification.
- Independent reruns pass 20 release-safety tests and 31 settings-backup tests.
  The retained transition records the complete 47-test settings pass.
- The linked proof closes main and all three callbacks. Adding the CRT entry
  allowance and all wrappers gives 93 + 2 + 61 = 156 bytes against 162 allocated.
  The final IRQ report covers all 15 distinct-source orders and 256 selectors.

The retained initial fixture failure is correctly separated from the complete
passing recheck. Earlier component proofs and review closure were checked
against final identities; exploratory images do not substitute for this image.
The application-only analyzer retains `whole_program_qualified: false`; the
separate reviewed startup and IRQ composition supplies the overall allowance.

## Findings and closure

Two preliminary reports still described independent review as pending. The
transition README now records the completed component review, distinguishes the
original execution-stage status from later approval, and identifies the final
release build. The stack report now records final artifact reproduction and
component-review closure. These were documentation corrections; machine inputs
and the policy hash did not change. Both findings are closed.

No additional defect was found in the direct transport dispatch, private Repeat
guard, bounded LED selector, exact FULL settings profile or package checks.
Typed failure stops and physical confirmation requirements remain unchanged.
Public release notes contain only user-visible changes and relevant limits.

## Remaining conditions

The policy SHA256 is
`32092b9468e7474d77720e5989bbe8cf5b087f6a817cdc19719c5d278c7655ef`.
The review compares uncommitted current bytes directly. Committed-HEAD checks
cannot approve those bytes until commit; final CI must reproduce the same
inputs and exact image, then pass native Windows/Linux packaging and checksum
gates. This review is not publication or package-runtime evidence.

Physical keys, encoder motion, USB timing, LED DMA, cold-start retention,
electrical flash behavior, power-loss recovery and interactive GUI acceptance
remain untested for alpha.3. Installed firmware remains alpha.2. No flash,
reset or bootloader transition is authorized by this review.
