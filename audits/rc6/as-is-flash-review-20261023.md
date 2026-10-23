# One-off update review

Independent offline review, 2026-10-23: PASS for the exact runner and prepared session below. This review covers the one-off settings-reset update requested by the owner after cancellation of firmware preservation work. It does not claim settings restoration, physical keyboard validation or power-loss validation. No USB command, unlock, reset, loader entry or flash was performed by the reviewer.

## Exact reviewed inputs

| File | SHA256 |
| --- | --- |
| tools/flash_reviewed_release_once.py | da0a01da7c3c944b37c2038004bdeffd189c0ef30ec167f9f671413ebabaf131 |
| tools/test_flash_reviewed_release_once.py | 613ed2d09de25c87b883ad8199436d5290fc4275be438a1a6293a5620ccfe137 |
| host/runs/20261023-as-is-flash/oneoff.json | 9e1f735a478f3c37c9edc3f8e942e5610de81e1ddcb986fb8bfa377a43742267 |
| host/runs/20261023-as-is-flash/payload.bin | a1b8beec9a2a675c955bac946339e31f1823e17cdfb60f4755796e550530c711 |
| host/runs/20261023-as-is-flash/source-rom.bin | ece49000b6d6b08d3ff08cb7ecfbf1bd374b302ac0ae354e150c6317de96b177 |

The runner pins target IHX f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e and source IHX d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce. It also checks source MAP and the approved release, including its existing host-file manifest. This separate runner does not change that manifest, spoof trial or repair provenance, or replace transport functions globally.

## Checks performed

Reviewed preparation, validation, execution and loader sequencing. Offline preparation validates the exact known source code and build manifest, protected regions, validity marker, current NVM schema and empty journal header. It saves current settings as evidence and builds the target using the original OEM migration. That resets settings; it does not restore the current-settings backup. Both source and target images must reproduce exactly from their saved IHX/MAP and the validated personal native backup.

Before live mutation, execution checks clean storage, saves a fresh complete ROM and settings copy, compares the full ROM to the reviewed snapshot, repeats settings/status checks and validates the session and runner identity. It locks Vial, starts a new physical unlock and requires the physical three-second hold. Existing installed Vial code advances this hold from physical matrix scans rather than polling. The runner checks exact ROM, status, unlock and selected application path again before requesting loader entry.

The loader path sends one sequence of commands 1, 2, 3, payload, 4, 5. It validates the immutable session and selected loader before erase and before restart. A failed command, timeout, short report, changed input or failed readback raises and stops. No retry, automatic reset, recovery or settings restoration follows a failure. The execution-started file prevents reusing a previously attempted session. Interrupting the process before erase remains possible; after erase, interruption can leave the loader stopped.

After restart, execution saves full ROM and status, checks target CODE, manifest, protected regions, marker and clean journal, compares initial NVM exactly with the target payload, and repeats the NVM/journal read and status. Physical typing, encoder behavior and persistence after power loss remain untested by these checks.

Independent test command:

```
python -m unittest discover -s tools -p test_flash_reviewed_release_once.py
```

All eight tests passed in 0.056 seconds. These are host tests with USB boundaries mocked. They check offline default behavior, execute argument separation, exact single command order, no erase after changed session, no retry/restart after erase failure, backup/consent/flash/verification order, and source/storage/consent failure stops.

Independent PREPARE ONLY command succeeded:

```
python tools/flash_reviewed_release_once.py --session host/runs/20261023-as-is-flash --source-rom host/runs/20261023-as-is-preflash/rom.bin --reference-dir C:/Users/vinok/Documents/Codex/AK820-private-transfer-20261023/oem-reference
```

No blocking code finding remains in this reviewed one-off workflow. This result applies only to the exact hashes above. Any runner or prepared-session change requires a new review. The lead remains responsible for checking those hashes and the owner's operation-specific authorization immediately before execution.
