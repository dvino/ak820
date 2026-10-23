# Freeze settings for a general update

2026-10-23. Proposed contract from source inspection. None of this capability
is implemented or installed. This task changed this report only. No build,
USB command, reset, settings write or flash was performed. Every future live
command in this proposal still needs the owner's authorization. Flashing needs
confirmation for that individual operation.

The existing `durable-update-plan.json` remains offline evidence. It is never
a flash session. FD01 v1 cannot establish a clean RAM snapshot or prevent a
settings change between the last read and loader entry. Reject it for this
general update path. Do not weaken the existing pinned RC6 repair checks.

## Source facts

The following paths are relative to `qmk-8051-ak820/` unless stated otherwise.

- `tmk_core/protocol/ch555/usb_ak820.c:ak820_usb_raw_task` serves FD00 and FD01
  outside the ordinary NVM batch. FD01 v1 has NVM dirty/batch/fault state but
  does not expose delayed RGB saves. Ordinary raw commands run inside
  `ak820_nvm_begin/end`; ending a batch can flush.
- `keyboards/ajazz/ak820/ak820_rgb.c` has a separate `dirty` flag. Persistent
  wrappers change RAM immediately, then mark it dirty. `rgb_matrix_task` saves
  after one second. The `_noeeprom` functions also change RAM directly.
- `ak820_macro.c` keeps `uploading` separately from NVM page state. An
  interrupted upload can leave no dirty page but still have unpublished data.
  `quantum/dynamic_keymap.c:dynamic_keymap_macro_send` has a local `sending`
  guard. Extended macro actions can dispatch key actions, including actions
  that change settings or request bootloader entry.
- `quantum/via.c` has layout, keymap, bulk keymap, lighting, save, reset and
  macro mutations. `quantum/vial.c` adds encoder writes and unlock/lock.
  `keyboards/ajazz/ak820/rules.mk` disables Magic, dynamic macro recording,
  QMK settings, tap dance, combo, key override and auto shift in this build.
  Do not claim their generic upstream setters are currently supported.
- `ak820_boot.c:bootloader_jump` does a best-effort NVM flush before marker
  erase/reset. That is a recovery route, not a strict snapshot entry primitive.

These are source facts, not measurements of the installed firmware. Source
identity must be checked against an exact supported installed image before
using any diagnostic interpretation.

## Minimum state and status

Keep one RAM transaction, not a persistent lock or journal entry:
`IDLE -> FROZEN -> ARMED -> CONFIRMED -> ENTERING`. Any invalidation makes it
`REVOKED`; cancellation returns it to `IDLE`. All commands execute in the main
task, never in a USB ISR. A short interrupt guard may protect shared byte copies;
it must not disable interrupts during ROM capture, consent or host waits.

Reserve FD01 version 2, retaining bytes 4..21 of v1. Proposed remaining bytes:

| Byte | Meaning |
| --- | --- |
| 22 | capability bits: bit 0 pending-state visibility, bit 1 freeze v1, bit 2 guarded entry v1 |
| 23 | pending bits: RGB delayed save, macro upload, macro playback, journal header nonempty |
| 24 | transaction state: 0 IDLE, 1 FROZEN, 2 ARMED, 3 CONFIRMED, 4 REVOKED, 5 ENTERING |
| 25 | first rejection/revocation reason; zero means none |
| 26..29 | little-endian transaction generation, incremented at each new successful freeze |
| 30 | invariant fault: unexpected write or mutation while frozen |
| 31 | reserved, must be zero |

The journal bit reads the actual header; a completed save may leave journal
data behind, which is not pending work. Define exact accepted header bytes
from the NVM implementation. Status never flushes, clears faults, advances
consent or repairs a journal. Expose macro upload and playback with small
accessors instead of guessing from `macro_ready()` alone. Check all status
fields together at one main-task boundary, including raw work already admitted.
Unknown versions, bits, state values or nonzero reserved bytes fail closed.

Do not use a wrapping settings counter as proof that bytes are unchanged. A
counter can aid logging, but freeze plus exact repeated bytes is the proof.
Generation wrap ends the capability for this boot; do not reuse an old value.

## Wire commands and order

Reserve FD02 for freeze v1 after checking that it is unused. Every request and
reply is exactly 32 bytes: `[FD,02,01,op]`, then a 16-byte host-generated random
transaction token at bytes 4..19, result at 20 (request must be zero), state at
21 (request zero), generation at 22..25 (zero only for BEGIN), reason at 26,
and zero at 27..31. Define op values 1 BEGIN, 2 ARM, 3 ENTER, 4 CANCEL, 5 QUERY.
Malformed/unknown operations receive an explicit failure without state change.
All replies echo token and generation. A new BEGIN while active returns BUSY;
it must not replace the token or restart consent. No automatic command retries.
FD01 remains the token-free read-only status; QUERY requires the active token.

The token prevents stale transaction reuse; it is not authentication against a
malicious process on the same PC. Host provenance pins the token/generation to
the complete hashes of source ROM, repeated NVM/journal, source policy, target,
OEM recovery and displayed final payload. The firmware does not need a SHA256
implementation or target-image copy. It binds physical consent to the immutable
host transaction; exact image integrity remains an installer responsibility.

1. The installer validates the source policy and all local inputs. It requires
   FD01 v2 and all three capabilities. It sends BEGIN only through a separately
   authorized future live path. BEGIN checks clean NVM, zero batch, no fault,
   empty journal, RGB not dirty, upload/playback idle, no pending reset and no
   already admitted settings action. It atomically enables mutation gates and
   rechecks these conditions before acknowledging FROZEN. A failure does not
   flush, wait for a save, clear pending state or silently rebuild.
2. While frozen, capture the fresh full ROM, then NVM/journal again. Validate
   exact source code, manifest, protected regions, marker and both byte reads.
   Produce the proposed payload and save the complete fresh backup. Validate
   original OEM recovery separately. Keep the transaction token/generation in
   the accepted host record. Any changed file or device bytes revokes this
   attempt. Never replace the displayed image after consent.
3. Display the final payload identity and backup in the installer. Clicking
   Update sends ARM for that token/generation. ARM starts a new physical consent
   attempt, clears previous consent and does not reuse `vial_unlocked`. Require
   the physical Esc and left Control matrix positions both released after ARM,
   then both held continuously for three seconds. Polling cannot fabricate the
   transition. The normal matrix scanner continues; remapped or macro-generated
   keycodes do not count. No typed confirmation, external Vial application or
   manual Bootloader action is introduced.
4. The physical hold changes only this transaction to CONFIRMED. It must not
   unlock general setters while frozen. The installer queries this status and
   repeats token/generation, clean-state, exact device identity, payload/file
   hashes and NVM/journal checks. ENTER succeeds only for that same confirmed
   transaction. It makes one last clean-state check and consumes consent before
   any marker erase. Any attempted mutation since BEGIN invalidates consent.
5. ENTER calls a new guarded loader primitive that never invokes
   `ak820_nvm_flush`. It permits only the intentional marker operation, verifies
   its readback and resets once. Reuse the audited marker implementation behind
   this guard; do not route through the current best-effort `bootloader_jump`.
   A failed marker operation stops and reports a fault; no repeated erase/reset.
   Once marker erase starts, this is the first destructive command and ordinary
   cancellation is no longer promised. Loader appearance is not permission to
   erase the application: host revalidates exact accepted payload/provenance,
   loader identity and protected bytes before application erase, then flashes
   once and verifies target and migrated NVM. No second flash on failure.

The marker erase itself is destructive even though it precedes application
erase. Check cancellation immediately before it. A timeout after ENTER is an
ambiguous transition, not permission to retry ENTER or flash a different device.

## Mutation gates

Gate entry before changing RAM, not only at EEPROM writes. A lower-level NVM
gate is a final invariant check, not a substitute: otherwise a setter can change
RAM while its save is blocked and lie about the snapshot.

| Path | Required gate while FROZEN/ARMED/CONFIRMED |
| --- | --- |
| VIA layout, single/bulk keymap, reset, lighting set/save, EEPROM reset, macro write/reset; Vial encoder and any enabled future setting command | reject before the ordinary raw NVM batch and before setter dispatch; reply explicit rejected status, never echoed success |
| RGB key bindings, encoder-dispatched RGB actions, direct Vial RGB setters, persistent wrappers and `_noeeprom` config setters | reject before changing `rgb_matrix_config`, dirty flag or change timestamp; animation phase/render caches and USB suspend display state may continue |
| Persistent default-layer/header writes, EEPROM clear/reset, future EEPROM-backed feature bindings | reject action before RAM changes; keep a final guard in EEPROM/NVM update, reset and flush entry points |
| Ordinary transient MO/TO/TG/default-layer selection | either suppress new actions during the transaction or allow only proven RAM-only actions; minimum implementation suppresses new key/encoder actions while retaining matrix scan and release cleanup |
| Macro upload and publication/reset | BEGIN refuses existing upload; reject new upload/reset before metadata or RAM parser changes |
| Macro playback, Repeat/Alt Repeat and queued/tapped actions | BEGIN refuses active playback or pending injected actions; suppress new playback/actions; cancel only transient held HID state, never save settings as cleanup |
| Delayed RGB task or any deferred save | BEGIN refuses pending work; frozen task cannot flush it. Unexpected pending state revokes and latches invariant failure, it is never made clean by saving |
| Ordinary boot/reset command or QK_BOOT from physical, encoder or macro path | reject during transaction; only guarded ENTER can consume consent and erase marker |
| Unknown raw/vendor command | frozen command allowlist rejects it before callbacks or NVM batching; add reads deliberately rather than assuming unknown commands are safe |

All rejected mutation attempts set REVOKED and preserve the first reason. They
must not mutate the setting. This lets another configuration program cause a
visible stopped attempt, but never an unreported settings loss. A no-op setter
is still a rejected attempt; do not try to infer that it is harmless.

USB enumeration/control traffic, FD00, FD01, token QUERY/CANCEL, approved Vial
identity/definition/read commands, matrix scanning, timer ticks, RGB rendering
and consent scanning continue. Do not freeze the CPU, USB task or status path.
Use the existing held-state release approach when entering the transaction;
preserve its release of momentary layers and HID state without persisting it.
Reject BEGIN until any cleanup that could dispatch a setting action is finished.
If any mutation can run reentrantly from USB servicing during macro delays,
check playback busy before acquiring freeze. Do not assume one main loop alone
rules out that reentrancy; cover it with the CPU harness.

## Cancellation and failure

CANCEL for the matching token/generation revokes consent first, locks Vial,
clears unlock progress and the transaction, then releases mutation gates without
writing settings. A duplicate CANCEL is an explicit stale result, never a new
transaction. Previously held keys must be released before accepting fresh action
presses so thawing does not turn a suppressed hold into an RGB/default-layer
mutation. The scanner and normal release cleanup continue during this interval.

Use a fixed bounded lease (proposal: 120 seconds, renewed only by matching
QUERY; renew cannot clear REVOKED). Expiry, USB deconfiguration/reset, explicit
Vial lock or a storage fault revoke consent and cancel the RAM transaction
without resetting the MCU or writing settings. Suspend revokes; do not continue
an old consent after resume. Host timeout/disconnection ends the attempt and
never triggers recovery. Locally the firmware may release a healthy freeze on
lease expiry; this is RAM cleanup, not clearing a storage fault. A storage fault
stays latched and continues blocking writes after cancellation.

While REVOKED, keep gates until explicit matching CANCEL or lease expiry. A
wrong-token CANCEL does not release another transaction. After any cancellation
or reconnect, a new attempt needs new freeze/capture/display/physical hold.
Cancellation races with ENTER are serialized in main context: if CANCEL wins,
ENTER fails; if ENTER has consumed consent and begun marker erase, host reports
that cancellation was too late and does not issue a reset or blind restore.

## Implementation ownership for a future work package

These are proposed future edits, not changes made here:

- Firmware transaction module `keyboards/ajazz/ak820/ak820_update.c/.h` and
  `rules.mk`: state, token, lease, mutation gate and clean predicates.
- `ak820_nvm.c/.h`, `ak820_macro.c/.h`, `ak820_rgb.c`: read-only busy accessors,
  earliest mutation gates and final storage invariant guards.
- `tmk_core/protocol/ch555/usb_ak820.c`: FD01 v2/FD02 dispatch before batching,
  explicit rejection, lifecycle revocation and frozen read allowlist.
- `quantum/via.c`, `quantum/vial.c`, `quantum/dynamic_keymap.c` and the enabled
  action/encoder dispatch points: raw setter, unlock, macro and injected-action
  gates. Determine the exact common action dispatch location in implementation;
  do not scatter incomplete RGB-only checks through physical key handlers.
- `keyboards/ajazz/ak820/ak820_boot.c`: separate guarded update entry and
  refusal of ordinary boot requests during a transaction. Preserve separately
  reviewed recovery behavior outside it.
- `util/ak820_diagnose.py`, `util/prepare_ak820_update.py`, `util/ak820_tool.py`,
  `tools/installer/ak820.py`, `tools/installer/gui.py`: versioned parser/policy,
  immutable provenance, token flow, fresh in-installer consent, cancel guards,
  one flash and postflash exact checks. The current offline plan format stays
  nonflashable; define a separately reviewed live-session format.
- Focused CPU/fake-host tests, README, English/Russian STATUS and protocol
  documentation: describe source, built artifact and installed state separately.

Code-size hypotheses only: a few RAM flags plus 16 token bytes and timers may
fit existing XDATA; checks at common dispatch points may cost less CODE than
guards at every caller. The token copy, reply encoder, clean predicates and
boot separation still cost CODE. No byte count or fit claim was measured here.
After the canonical build is idle, measure map/code/XDATA deltas and placement,
including fixed-address overlap; do not assume a design fits the current image.

## Required offline evidence

| Level | Cases |
| --- | --- |
| CPU/source harness | each BEGIN precondition including RGB dirty with clean NVM, upload active with clean page, playback/reentrant USB, pending journal, batch/fault; no flash primitive called on rejection |
| CPU/source harness | every enabled raw setter, physical/encoder RGB action, default-layer/reset, macro and injected action while frozen; RAM and NVM unchanged, explicit rejection and REVOKED; final low-level guard catches a deliberately missed caller |
| CPU/source harness | timer/USB/render/status continue; delayed save never runs while frozen; actual matrix release then fresh 3-second hold; old unlock, held-before-ARM, macro keys and replayed polls never confirm |
| CPU/source harness | CANCEL, wrong token, stale generation, duplicate BEGIN/ENTER, lease wrap/expiry, suspend/reset/deconfigure, held-key release, storage-fault latch, cancel/ENTER ordering; guarded entry calls no flush and performs at most one marker operation |
| Fake host | unsupported v1/missing capabilities/malformed v2, wrong source image, all immutable hashes/backup/source checks, changed ROM/NVM/journal or local files at every boundary; no ENTER or erase on failure |
| Fake host | display/ARM order, consent token binding, timeout at each step, mutation revocation, cancel before marker/application erase, different loader/device, malformed or missing reply, postflash code/NVM/storage mismatch; no automatic retry/restore/second flash |
| Package/model | current schema copies all 10,240 NVM bytes; legacy migration retains six target layers, both encoder directions, RGB/header, sixteen macros and allowed inactive data; overflow and incomplete streams fail |

These tests model protocol ordering, byte preservation and CPU control flow.
They do not prove live USB timing, real key/encoder behavior, physical consent,
durable saves, cold boot, power loss, recovery or installed code. Those remain
deferred and need explicit authorization; do not add a live command to default
test runs.

## Bootstrap limit

The current source protocol and installed source described by the existing
update work lack this capability. A general updater must say unsupported, not
fall back to delays or v1 clean reads. Installing capability-bearing firmware
first is itself a separate update: it cannot retroactively supply atomic
freeze to its old source. Keep the existing exact pinned repair route separate;
if the owner later chooses a bootstrap operation, review its exact source,
backup and payload, explicitly state its durable-only limits and require that
operation's flash confirmation. This report authorizes neither bootstrap nor
hardware access. Do not present the proposed freeze as already working.

Writing follows the owner's plain-language instructions and supplied wording.
The writing-style skill was read; no retrieved style match is claimed.
