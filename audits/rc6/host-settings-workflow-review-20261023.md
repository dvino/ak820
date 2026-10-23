# Installer settings workflow review — 2026-10-23

## Scope

Independent review covered `settings_workflow.py`, installer command routing,
the `host_update_snapshot` transport gate, workflow tests, Windows package
inputs and the combined offline test runner. GUI, localization and EN/RU
documentation were reviewed separately by an independent delegated reviewer.
No hardware was opened or written.

## Source checks

Backup, restore and update use the same validated settings backend. Offline
release approval, OEM recovery validation and exact target reconstruction
precede HID import and enumeration. Each command requires the OEM session.
The exact reviewed firmware profile remains the source and target boundary.

Update exports a fresh backup and plans every restoration field before
requesting physical confirmation. The installer forces a new lock/unlock
sequence, rechecks source ROM and settings, and validates backup and target
inputs before entering the loader. The displayed hash is the same payload
hash checked by the phase guard. Cancellation is checked before loader entry
and again immediately before erase. No retry or automatic recovery is added.

The transport's new gate requires a permanent image, an explicit selected
loader, a phase guard, exact payload/recovery checksums and native-backup
provenance. It cannot be combined with native installation, prepared repair
or a second loader transition. The lower-level command-line parser does not
expose this new bypass as a general flash flag.

After the single flash, application startup, full CODE/protected-region
identity, the complete flashed manifest and exact initial NVM are checked
before restoration. A second fresh physical unlock is required because the
application restart locks Vial again. Settings restore keeps a target-state
backup and checks bound inputs and cancellation before individual setters.
A failure leaves the backup available and stops the operation.

The Windows HOST_FILES allowlist binds all three new runtime modules. Both
PyInstaller commands include the tools import path and allowlisted module
files. The combined runner discovers the installer tests and now includes
the constrained protocol suite. These source/package-plan checks do not
prove a rebuilt Windows executable works; the previously built executables
remain separate artifacts.

## Verification and closure

`python -m unittest discover -s tools -p test_build_windows_installer.py`
passed all four offline tests. GUI/i18n tests passed 7 and 13 cases,
respectively, in the delegated review.
`python -m unittest discover -s tools/installer -p test_settings_workflow.py`
passed all 13 workflow tests in 22.205 seconds. These include actual backend
CLI/GUI backup and restore with a synthetic wire device, a single-flash
update model, a changed flashed-manifest failure, and guarded loader
rejections. Tk modal lifecycle and Windows executables are not exercised.

Two wording findings were sent for correction: the standalone Restore unlock
explanation incorrectly assumes a preceding restart, and the EN/RU roadmap
retains an unqualified SDCC 4.4 production instruction alongside the current
SDCC 4.6 baseline. Neither changes runtime authorization. Both are closed: EN/RU restore text now
requires a fresh unlock without assuming a restart; EN/RU ROADMAP marks the
4.4 comparison historical and names 4.6 as the current baseline. The historical
implementation plan now points to the current settings guidance.

No concrete source correctness or permission finding is open at this
checkpoint. The final release manifest and approval binding require separate
review after overall checks and regeneration. This report does not approve
hardware writes or establish physical behavior or power-loss persistence.

## Final offline binding and evidence check

The regenerated installer manifest SHA256 is
`ca4b4d3908d849318615d5a1ed8a333d53a188344e345410bb3a9dff884dd131`.
It independently matches `approved-release.json` and the durable validation
report. All nineteen current host-file records match the bound review,
installer manifest and validation report. All nine release-file records match
their actual bytes. The eight non-review release files are byte-identical to
Git baseline `c0c704e`, including firmware, build reports and reference data.
The bound release review was not changed during this final check.

All eight saved suite log SHA256 values in
`audits/rc6/host-settings-offline-20261023.json` were independently verified.
The saved logs show successful exit results and 222 reported unittest cases:
111 installer, 12 assembler, 4 Windows package-plan, 3 combined-runner,
19 device-runner, 9 constrained protocol and 64 package cases. The package
suite reports two skips; the compiler/boot dependencies were unavailable.
The eighth suite checks 31 public documents with zero failures. The original
host/runs report checksum matches the durable report's source checksum.

The saved offline verify event log checksum also matches. It records
`device_opened: false` and `physical_mutations: 0`. An independent rerun of
`python -B tools/installer/ak820.py verify` passed and explicitly reported
that hidapi was not loaded and USB was not opened. These results close the
combined offline source/package evidence gate only. They do not establish
new firmware compilation, CPU execution, Windows EXE behavior or live device
behavior. Final documentation agreement is recorded below after its update.

## Final documentation agreement and review closure

Final EN/RU STATUS, TESTING, ROADMAP, INSTALL and SETTINGS-BACKUP content was
checked against the source and durable evidence. Commands require the OEM
session; preservation is limited to the exact reviewed image. The documents
record 222 tests, two skipped dependency checks, 31 checked public documents,
the exact regenerated manifest checksum and nineteen bound host files. They
correctly distinguish this source/offline approval from older Windows
executables, earlier installed-firmware evidence and unperformed device work.
README introduces the source feature and points to the operating guidance.
The historical implementation plan is explicitly superseded by that guidance.

A fresh independent `python tools/check_docs.py` check passed: 31 public
documents, zero failures. A whitespace check with CRLF recognized as the
existing line-ending convention passed. No code or bound review changed in
this final evidence/documentation check.

Final independent review status: PASS for the reviewed host source,
documentation, tests and exact offline package binding. No findings remain
open. Remaining Windows build/native GUI checks, hardware writes, physical
behavior and power-loss persistence are separate unperformed validation;
publication and hardware operations are not authorized by this review.
