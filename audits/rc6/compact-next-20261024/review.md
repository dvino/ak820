# Independent review and finding closure

The reviewed work starts at `38ad0133278463b4662dcb81eecaa17c9cd93b9b`.
Source and test files were frozen before the twelve passing runs in
[matrix.json](matrix.json). Each exact build records its compiler inputs and
test sources; [frozen-sources.json](frozen-sources.json) binds their current
repository bytes. Later edits were limited to documentation and evidence.

## Source and behavior

| Scope | Independent result | Evidence and limits |
| --- | --- | --- |
| Private XDATA views, scalar positions, byte RGB dispatch and Repeat ranges | Approved | Producer origins and emitted assembly checked; 234,881,024 extracted-function comparisons and 280 linked event cases pass. The pinned AK820 configuration limits remain explicit. |
| Event argument wrapper | Approved | Named six-byte snapshot avoids the rejected extra dereference; emitted tail jump preserves the public entry. The extra copy and XRAM cost are documented. |
| Compact Auto Shift | Approved | One-owner state, 175 ms boundary, modifier ownership, remapping, bypasses and clear paths agree with the guides. The exact combined image passes 27 enabled-default cases, including two Mouse interactions. |
| Compact Mouse Keys and transport | Approved | Accepted button state survives a failed clear/release; motion is consumed on failed sends; original configured/suspend/reset guards remain. The combined image passes 21 Mouse and 10 transport scenarios. |
| Direct RGB binding | Approved | Signed public bounds precede byte narrowing; board bounds and scan-IRQ DMA masking remain. Exact emitted tests cover invalid indices, Direct rendering and suspend/resume. |
| Optional short transfers | Approved | Immutable inputs, final-page decoding, NoICE symbol identity, unchanged instruction bytes, strict final bounds and default-off behavior checked. Fifteen unit controls, nine build-input controls and seven manifest-tamper checks passed in independent review. |
| Qualification integration | Approved | Original 28-suite base runner and CI/release policy remain unchanged. All eleven supplemental plans require short-call discovery; 23 configurator and 11 CI-authorization unit checks passed independently. |

These are independent nonauthor reviews of source, documentation and offline
evidence. They do not qualify hardware behavior, interrupt overlap, runtime
stack safety or a public release.

## Findings resolved before the final matrix

The short-transfer review identified missing imported-decoder provenance,
a source snapshot taken too late, an unbound final NoICE file and incomplete
unchanged-instruction checks. The builder now binds the decoder, snapshots
before rewriting, records final symbols and verifies opcode, width and fixed
operand bytes. Additional controls cover relative conditional operands and
diagnostic-only page warnings. The final parser remains strict.

The first unit-runner integration expected a nonexistent `run.py`. A discovery
entry then conflicted with the exact 28-suite base contract. The final change
restores `tools/test_keyboard.py` byte-for-byte to upstream and adds the new
suite to every profile's supplemental plan. Independent review then exposed
an empty-discovery acceptance gap. Zero-test and skipped-test results now fail,
including controls with a matching log hash. The final matrix follows these
corrections.

The Auto Shift fixture initially used an absent physical matrix position for
one Mouse interaction; the corrected populated position passes on the same
unchanged IHX. Ordinary test fixtures disable Auto Shift through the production
`AS_OFF` key path. Dedicated tests retain the enabled startup default and
require that observation. An absent observation marker is reported as
`not-observed` instead of claiming a checked mode.

Core audit source hashes were clarified as isolated measurements because the
integrated action source also contains Auto Shift hooks. Mouse guides now state
the immediate first attempt and group-timer restart. The Auto Shift test guide
now specifies its QMK working directory and correct relative build path; the
Russian user guide links to the technical report instead of repeating internal
verification material. Independent follow-up closed these documentation findings.

## Exact final combined image

The final IHX SHA256 is
`8873ebe29cea93673f44fa5c20adf8f5c372a73c70f1151da32b7c67671aad85`.
Independent final reviews matched the actual image, MAP, MEM, build report,
qualification and supplemental-report hashes. All recorded supplemental source
hashes and all 22 raw log hashes match. Base qualification is 28 suites and
273 unit tests, with no skips and no image changes during testing.

The final image has 40,403 occupied CODE bytes, 2,687 allocated XRAM bytes and
163 bytes of stack capacity. The main runtime root remains unresolved; the
timer, USB and LED callback bounds are 2, 6 and 2 bytes. These callback figures
exclude the OEM wrapper and nesting proof required for release. No old alpha.3
stack allowance is reused.

## Final retained-evidence closure

The complete twelve-variant matrix and retained evidence passed independent
review before commit. All table values and saved configuration identities agree.
The review checked 5,460 compiler-source references, 1,908 supplemental-source
references, all report-copy identities and the retained raw-file ledgers.
The independently executed verifier passed for 209 evidence files, 592 current
repository sources and all 22,405 raw members containing 906,138,677 bytes.
No findings remain in this evidence scope. This paragraph records that approval;
the checksums were refreshed after adding the record.

Independent short-transfer follow-up extracted proof inputs from both retained
short-call archives and reran `validate_saved()` successfully. It verified all
3,352 raw members of `full-short` and 3,108 of the combined image. The proofs
cover 238 sites and 4,334 edges for `full-short`, and 239 sites and 4,464 edges
for the combined image. All twelve base reports meet the unchanged contract;
both short variants meet the final supplemental contract. No findings remain.

The offline [package check](package-rejection.json) exits 1 as expected:
the new combined identity is not release-approved. CI authorization policy,
release-safety pins and device state remain unchanged. No USB, reset,
bootloader or flashing command was issued during this work.
