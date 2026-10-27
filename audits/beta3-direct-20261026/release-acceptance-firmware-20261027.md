# Firmware release acceptance review

Date: 2026-10-27.

Reviewed immutable range: `b35b77cddbefdb509058f1fbaaeafaa3982ce172..fac89a85610845612ff7db34d111dae7a33a670b`.

## Result

No blocking finding was identified in the reviewed firmware/runtime scope.
This independent review covers Direct frame transactions and generation-qualified
readback, native row publication, the GUI-lock W pulse, the narrow stack-checker
change, retained exact-image reports and corresponding English/Russian claims.
It supports offline acceptance of these inputs; it does not approve hardware
behavior or establish final published package identity.

Direct range and ID checks precede staging writes. Sequential uploads and exact
normalized duplicates preserve the active palette until complete commit. The
foreground owns the logical HSV palette; the IRQ consumes frozen staging.
QUEUED/PUBLISH prevent staging reuse and normal renderer writes. Publication
starts at row zero, preserves R6 and releases staging after row 15 transfer.
Generation-qualified reads and logical-versus-physical completion agree with
the Direct guides in both languages.

W pulse arithmetic keeps phase bounded and preserves the required registers.
Upper layers retain priority, suspend/unconfigured USB resets pulse startup,
and C/OS component channels remain independent. The indicator guides agree.
The stack recognizer checks the complete outlined multiplication leaf and
accounts for its two-byte return frame.

## Checks performed

- `python3 -m unittest discover -s qmk-8051-ak820/tests/ak820_stack -p test_analyze.py`: 33 tests passed.
- All 290 test-source and ten runtime-source SHA256 pins in `final-source-freeze.json` matched current reviewed bytes. Sparse files were read with `git show HEAD:path`; no heavy artifacts were extracted.
- All 30 retained foreground, IRQ and startup report SHA256 values matched their ten `profiles/*/runtime-summary.json` references.
- All ten runtime summaries report `passed: true`, `whole_program_stack_qualified: true`, no unresolved roots, `hardware_validated: false` and zero physical device commands.

| Profile | Stack bound | Capacity | Margin |
| --- | ---: | ---: | ---: |
| main | 160 | 182 | 22 |
| game | 160 | 177 | 17 |
| mmo | 164 | 180 | 16 |
| typing | 160 | 184 | 24 |
| code | 160 | 184 | 24 |
| pointer | 160 | 184 | 24 |
| onehand | 164 | 185 | 21 |
| creative | 164 | 183 | 19 |
| shortcuts | 164 | 185 | 21 |
| multios | 160 | 184 | 24 |

Retained reviews read: `firmware-final-review.md`, `stack-final-review.md` and
`final-generated-admission-review.md`. Their earlier pending-admission statements
were assessed against the later final freeze and per-profile reports. This pass
checked source pins and retained report correspondence; it did not independently
rebuild images, rerun full linked qualification or authenticate archive contents.

## Remaining limits

Final publication requires exact package/image correspondence and the final
merged-main identity checks. Physical USB timing, added LED interrupt timing,
DMA publication, W behavior, typing, encoders, durable storage and power-loss
recovery remain unvalidated by this review. Static bounds and CPU/host models
do not establish those behaviors.

No firmware implementation, test source or evidence record was modified. No
build, heavy archive extraction, USB action, reset, bootloader transition,
flashing, settings write, commit or publication was performed. This report is
the sole authorized write from this review.
