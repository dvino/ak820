# Review of the offline durable update plan

2026-10-23. Independent review of `util/prepare_ak820_update.py`, its eight
focused tests and `general-update-preparation-20261023.md`. The reviewer did
not author the implementation. No blocking findings were found within the
offline preparation scope. This review does not approve a live update.

The helper checks the permanent source payload and its caller-supplied exact
hash/build policy, the original OEM recovery and references, protected ROM
regions, application code and manifest, NVM format, empty journal header,
repeated NVM/journal bytes and raw FD01 status. Current NVM is copied in full.
Legacy migration uses the existing explicit schema conversion and rejects
macro overflow. The original recovery is validated separately from the Vial
ROM and remains the caller's responsibility to retain.

All validation and payload generation precede output directory creation.
Inputs are immutable bytes or files read without writes. Existing output
directories are rejected. IHX/MAP files are read again after packing to detect
ordinary concurrent changes. No transport is constructed by this function.
The single JSON plan contains neither `images.json` nor the binary files
required by `ak820_tool.session_image`; that reader rejects the plan directory.

The policy is a caller-controlled choice, not independent authentication of a
device capture or source release. FD01 v1 cannot show the separate pending RGB
save or freeze settings. Matching supplied bytes therefore prove only the
recorded durable snapshot. The plan accurately records this limit, sets
freshness and flash authorization false and leaves the future capability
unimplemented. Its documentation makes the same distinction.

## Verification

The reviewer ran this from the repository root:

```powershell
rtk proxy python -m unittest discover -s qmk-8051-ak820/tests/ak820_package -p test_general_update_preparation.py
```

Result: eight synthetic offline tests passed after the author's coverage
changes. The new English and Russian STATUS paragraphs accurately describe
the offline component and its live-update limits. No build, USB operation, device
write, reset, bootloader command or flash was performed.

## Coverage follow-up

The author addressed the three initial coverage recommendations:

- Damaged original recovery, native reference and stock now fail before output.
- Deterministic changes after parsing exercise both IHX and MAP change guards.
- Distinct values now cover every slot on all six layers, twelve encoder
  assignments, sixteen nonempty macros, RGB and inactive NVM capacity. The
  complete NVM output is compared with the supplied snapshot.

A direct trial-source rejection case is still an optional small coverage gap;
the helper explicitly rejects trial sources before output. No implementation
defect was found. The reviewer reran the strengthened suite independently.

Physical input behavior, live status provenance, delayed RAM saves, cold boot,
power loss and successful flashing remain untested. Future live integration
needs a separate review and the owner's operation-specific authorization.
