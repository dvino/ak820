# General update implementation plan

Source audit, 2026-10-23. No USB commands, builds or source changes were made
for this plan. The owner rejected the snapshot-only console update and requested
completion of the general updater first.

The update must preserve the settings captured at a firmware-defined freeze
point. A host cannot prove that settings stayed unchanged simply by reading
them twice. The installed source has no freeze operation. Adding one to the
target does not make it available before the first update.

## Installed source: what can be recovered

`quantum/vialrgb.c:vialrgb_save` exists and calls
`eeconfig_update_rgb_matrix`. VIA dispatches `id_lighting_save` to that handler
when VialRGB is enabled. This is a settings write, not a read-only operation.
Do not send it during diagnosis without write authorization. It can persist the
eight-byte RGB configuration, including fields that the ordinary RGB getter
does not expose. Check the exact installed build's linked handler and command
dispatch before relying on this capability; current source alone is not proof
of installed behavior.

`vialrgb_get_mode` returns effective mode, speed and HSV. When disabled, it
returns OFF rather than the hidden selected mode. It does not return flags.
`vialrgb_get_led_info` returns static LED geometry and flags, not current color.
`g_direct_mode_colors` has a setter but no getter. Saving the RGB configuration
does not persist this Direct color array. The source exposes CODE reads, not a
general RAM reader. Therefore existing Vial getters cannot export arbitrary
current RGB RAM losslessly.

`ak820_rgb.c` has a private dirty flag. Its delayed save runs after 1000 ms;
waiting does not prevent a later key, encoder or protocol command from making
another change. Closing other clients reduces competing host writes but cannot
freeze keyboard input. `bootloader_jump` performs a best-effort NVM flush and
then allows loader entry even on a storage failure. The host cannot query the
application status after that transition.

The first transition cannot promise preservation of arbitrary latest RAM with
the existing interface. Do not call an idle delay, repeated reads, process
closure, or a bridge image an atomic snapshot. A bridge image already requires
the same first transition. Do not erase until this limitation has an explicit
supported policy. An honest initial support matrix can reject this legacy
source for fully automatic preservation, or offer a separately explained
legacy procedure after the owner chooses its limits. That choice has not been
made here; snapshot-only updating was explicitly rejected.

## New source capability

Implement a versioned update protocol separate from the RC6 repair pins. Keep
FD01 version 1 decoding strict. Add a capability reply declaring protocol
version, build identity, settings schema, RAM export schema and maximum export
length. Unknown versions must stop preparation.

Use an explicit state machine: RUNNING, CONSENT, FREEZING, FROZEN, ENTERING and
FAULT. Fresh physical Esc + left Control confirmation belongs to the displayed
target update. Once confirmed, firmware rejects new settings mutations before
saving anything. It stops key/encoder actions that alter settings and rejects
VIA/Vial writers, macros, RGB setters and batch starts. Keep USB service and
read-only queries responsive. Define whether ordinary typing continues; this
must not reopen a settings mutation path.

At FREEZING, finish or reject any open batch, save private RGB configuration,
flush NVM, verify storage completion and require an empty journal header. A
failed save must enter FAULT and never enter the loader. Do not silently end
an incomplete macro upload or retain a partial transaction. Export the exact
RAM state that is part of the preservation contract, including all Direct HSV
colors and hidden RGB configuration fields. Animation phase, reactive ages,
currently held keys and executing macro position should have an explicit
preserve/reset policy; they must not be accidentally called user settings.

Freeze a generation number and a session token. Return both with every export
chunk, status and enter-loader request. The host reads NVM and RAM under that
token and verifies exact lengths and a content checksum. A stale token, wrong
generation, storage fault, malformed offset or unsupported schema fails closed.
Do not assume a checksum is authorization. Bind the fresh physical consent to
the target image digest and session token; specify how the full digest is
transferred within the 32-byte report limit.

ENTER_LOADER must require that token and the frozen clean state. It must not
perform an unobserved best-effort settings flush. Marker erase/readback failure
must return an error while retaining the frozen session and evidence. A
successful transition must use the snapshot already acknowledged by the host.
No automatic retry or reset follows an error.

Cancellation before erase must remain available. Specify a deliberate abort
operation that invalidates the token and returns to normal operation without
restoring old settings. A host timeout/disconnect must stop host actions; do
not automatically reset or enter the loader. Decide and test whether firmware
stays frozen until explicit abort or safely releases the freeze. The UI must
explain the chosen behavior.

## Target restoration and session format

Create a separate general-update manifest with exact source/target build IDs,
IHX/MAP and payload hashes, full source ROM, frozen NVM/RAM export, protocol
version, token/generation, native recovery backup and protected-region hashes.
Validate every input before creating a flashable session. Reject unknown NVM
or RAM schemas and any migration that would truncate macros or layers.

Copy NVM bytes exactly when schemas match. For known migrations, emit the
mapping and verify every preserved field. An empty journal header means the
retained journal data page must not be replayed. Pack the target with a clear
journal. A nonempty header is a stop condition, not permission to guess which
copy is newer.

Direct colors need either a reviewed target startup import format or a guarded
post-start RAM import while the target remains frozen. Do not add them to
durable storage without checking capacity and defining the new layout. Keep
the session and original recovery backup even if later verification fails.
The target must report import completion, exported state equality and clean
storage before normal input resumes. A failed import leaves an explicit stopped
state; do not silently reset RGB or resume with partial settings.

## Host and UI work packages

1. Firmware protocol owner: inventory every settings writer; implement freeze,
   status, token-bound export, abort and strict loader entry. Own firmware tests
   and the protocol document. Report linked CODE/RAM/stack growth against the
   actual SDCC 4.6 release before accepting the design.
2. Settings owner: define NVM/RAM schemas, lossless migration and Direct RGB
   export/import. Own schema fixtures, migration tests and target startup gates.
   Do not change source support claims until installed-source capabilities are
   independently verified.
3. Host owner: add a separate general session builder and validator, immutable
   artifact checks and a single update orchestrator. Reuse the reviewed loader
   transport, not trial-provenance flags or modified repair pins. Console and
   GUI must call this same state machine.
4. UI owner: Update shows the exact image, requests fresh physical confirmation,
   freezes/saves/captures, enters loader, flashes once and verifies. No typed
   yes/ready, separate Vial app or manual Bootloader step. Show unsupported
   legacy source before starting confirmation. Keep cancellation before erase.
5. Independent reviewer: check code, protocol, source/target artifacts,
   documentation and negative-test evidence together. Resolve findings before
   any live operation. Root owns integration and any separately authorized
   device action; implementers send no USB writes.

## Required gates

Offline tests must cover every writer while frozen; concurrent getter/setter
ordering; pending RGB save; Direct HSV export boundaries; disabled RGB with a
hidden mode; open batches/macros; dirty page, failed flush and nonempty journal;
stale token/generation; malformed reports; input mutation during freeze;
abort, timeout and disconnect at each phase; changed files after preparation;
wrong source/target; and target import/readback failure. Assert that failures
emit no loader/erase/retry/reset command.

Use CPU/host tests for firmware ordering and storage-fault paths. Build and
inspect exact linked artifacts. Mock transport tests prove host sequencing,
not USB or durable behavior. Read-only live capability/export checks require
an installed supporting source. Settings-write tests, loader entry and flashing
need explicit authorization for each operation. Hardware tests must cover
power-loss persistence and real input separately; ordinary CODE readback cannot
prove either. Automated regression must cover supported remapping and both
encoder directions in host/CPU models and explicitly report physical checks
that remain untested.

The release may advertise general preservation only after a supported source
can freeze and export the complete declared settings state, the target can
restore it, independent review passes, and separately authorized live evidence
supports the protocol and storage claims. The currently installed legacy source
remains a specific unresolved first-transition gate.
