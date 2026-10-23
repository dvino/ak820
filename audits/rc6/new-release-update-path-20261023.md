# Console update path, 2026-10-23

The existing console cannot safely update the installed permanent RC6 build to
the new SDCC 4.6 release while promising to keep all current settings. Keep the
RC6 repair guard unchanged. A separate general update path is required.

This is a source audit only. No USB command, device write, build or hardware
test was performed. The requested target IHX SHA256 supplied for this audit is
`f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`;
this audit did not independently hash the release artifact.

## Existing guards

`tools/installer/ak820.py:update_prepared` validates the prepared session before
reading the keyboard. It also requires the session IHX and MAP hashes to match
the loaded approved release. It captures a fresh full ROM, checks the repeated
NVM and journal read, and validates that snapshot again before loader entry and
before erase. Fresh physical Esc + left Control confirmation is required.
Cancellation remains possible before erase. The function flashes once and
checks the running application, protected bytes, durable settings and storage
status. It does not establish physical typing or persistence after power loss.

`qmk-8051-ak820/util/ak820_tool.py:validate_prepared_update` admits exactly:

| Input | Required SHA256 |
| --- | --- |
| IHX | `d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce` |
| MAP | `9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000` |
| Payload | `54290ce406fda133bd90703664f60559e23620f184f89033c98dddb56e2299ed` |
| Fault snapshot | `bf7bc0f89b7f17223384864a21699cb510fd573f2587277a9fb7d846ddd01333` |
| Personal recovery backup | `1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1` |

The repair keeps the durable NVM from that fault snapshot and clears its pending
journal. It does not replay the failed encoder probe. Changing the pins to the
new release would turn a reviewed repair into an unreviewed general updater.

`prepare_permanent` serves a verified trial-to-permanent installation. It reads
the running trial and repacks settings with the original trial build inputs.
It is not an installed permanent-to-new-permanent update route. Setting its
manifest fields by hand or passing a hardware-check flag would bypass the
intended evidence and is not an acceptable update plan.

## Work still needed

`qmk-8051-ak820/util/prepare_ak820_update.py` is an offline prototype. It checks
the exact source identity, protected bytes, repeated NVM/journal bytes and
FD01 status; migrates durable NVM; then packs a target payload. Its output is
`durable-update-plan.json`, not a flash session. It explicitly records
`flash_authorized: false` and `live_freshness_verified: false`.

FD01 version 1 cannot establish that a pending RGB save has finished or freeze
the live settings while reading them. Two equal storage reads alone cannot
prove that no pending RAM setting will be lost. The prototype therefore cannot
be promoted to a live updater by adding a CLI switch.

1. Define which settings must survive, including pending RGB changes. Specify
   an exact supported source build and a migration contract. If the installed
   source cannot expose pending saves or freeze a snapshot, stop and resolve
   that limitation before promising full preservation.
2. Implement and review a source capability that reports pending saves and
   holds a coherent snapshot, or design a separately reviewed, explicitly
   limited durable-storage update. Do not describe the latter as preserving
   every current setting.
3. Add separate generic session preparation and validation. Bind the fresh
   source snapshot, exact target IHX/MAP, migrated settings, original personal
   recovery backup and protected bytes. Keep repair admission separate.
4. Connect this session to one console/installer orchestration path with fresh
   physical confirmation, cancellation before erase, one flash, exact readback
   and storage checks. A timeout, storage fault or bad readback must stop the
   operation without retry, reset or blind restore.
5. Add offline rejection tests for wrong source/target, changed inputs, dirty or
   failed storage, snapshot changes, migration failure, cancellation and bad
   readback. Review code, documentation and evidence independently before use.

Console authorization permits the requested operation; it does not supply the
missing snapshot capability or make an old repair session fit a new release.
No safe existing console command for this general update was established by
this audit.

## Bounded snapshot option

The lead reported a new read-only capture in
`host/runs/20261023-sdcc46-before-console-update/`: ROM SHA256
`ece49000b6d6b08d3ff08cb7ecfbf1bd374b302ac0ae354e150c6317de96b177`,
matching installed CODE, repeated stable NVM/journal, clean FD01 status and an
empty journal header. These are lead-supplied results, not checks rerun here.

A separate one-off tool could preserve exactly that accepted durable snapshot.
It would pin the source ROM and source build, target IHX/MAP and recovery
references; validate the source; migrate NVM; bind an immutable session; require
fresh physical consent; then perform one guarded flash and exact readback.
It must state that unsaved RAM settings can be lost.

This still cannot guarantee detection of every change until loader entry.
The final read/status command and loader command are separate. Firmware can
change settings between them. `ak820_boot.c:bootloader_jump` calls a best-effort
NVM flush and deliberately allows loader entry even if that flush fails.
FD01 cannot report a failure after the application has entered the loader.
A console implementation must not claim that this gap has been closed.

For a source with an empty journal header, do not replay retained journal data.
`verify_live` accepts retained data at `EF00:EF40` only when `EF40:EF80` is empty.
`migrate_vial_nvm` copies only durable NVM; when the source schema equals the
target schema it copies those bytes exactly. Packing a target with a cleared
journal is consistent with that completed-transaction state. Nonempty headers
must stop preparation.

`ak820_rgb.c` has a private dirty flag and normally saves after 1000 ms.
Waiting that long cannot prove that no new change arrived. Loader entry flushes
NVM, not the private RGB RAM state. No reviewed external command that proves
all RGB RAM has been saved was established here.

No one-off console implementation was authored: the requested guarantee of
detecting changes until loader entry cannot be established with the available
firmware capability. A snapshot-only operation needs an explicit scope choice
and independent review; it does not complete the general updater.
