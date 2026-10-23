# Preserve settings during an update

2026-10-23. Design from current source. No installer or firmware code changed.
No USB access, reset, bootloader command, settings write or flash was performed.
This document does not approve a device update.

## Decision

Add a general update path that builds its image from a fresh, validated readback
of the running firmware. Keep the existing RC6 repair path separate. That repair
accepts one exact snapshot, payload and original OEM backup; it deliberately
keeps the durable NVM and removes the failed probe's pending journal entry.
Removing its hash pins would change that repair into an unsafe general update.

Preserve two backups with different purposes: the complete fresh Vial ROM for
evidence and settings, and the original personal OEM backup for native recovery.
Do not pass a Vial ROM to `validate_native` or call it a native restore image.

## Existing contract

`qmk-8051-ak820/util/pack_ak820.py` defines these absolute half-open ranges:

| Data | Range / size |
| --- | --- |
| Application image | `0x2800..0xEFC0`, 51,136 bytes |
| NVM | `0xC700..0xEF00`, 10,240 bytes |
| Journal data page | `0xEF00..0xEF40`, 64 bytes |
| Journal header | `0xEF40..0xEF80`, 64 bytes |
| Package manifest | `0xEF80..0xEFC0`, 64 bytes |

The marker occupies `0x27C0..0x2800`. Protected loader and tail checks must remain
the same as in `ak820_tool.verify_live`; image construction must keep the OEM
loader contract and permanent boot marker behavior.

`nvm_layout`, `validate_nvm` and `migrate_vial_nvm` accept exactly two schemas:

| Schema | Layers | Encoder offset | Macro offset / capacity | Macro metadata offset |
| --- | --- | --- | --- | --- |
| `0x082001` | 2 | `0x0240` | `0x0300` / 9,472 bytes | `0x02F0` |
| `0x082002` | 6 | `0x0640` | `0x0800` / 8,192 bytes | `0x07F0` |

Offsets in this table are relative to `0xC700`. Both schemas start the keymap at
offset `0x0040`; each layer uses 256 bytes. Each encoder layer uses four bytes,
two keycodes for the two directions. The schema occupies NVM bytes 37..39 in
little endian. The NVM magic is `E6 FE`. Both formats publish 16 macros.

For `0x082002`, migration copies every NVM byte exactly, including inactive
bytes. For `0x082001`, it preserves the common header, both keymaps, both encoder
layers and valid macro stream. It makes four new layers and their encoders
transparent, changes the schema and moves macro metadata. It removes only zero
padding after the sixteenth macro. More than 8,192 meaningful macro bytes is a
failure, never truncation. An unknown schema, incomplete upload, invalid length,
unsupported opcode or malformed stream is a failure before image creation.

This is an NVM format allowlist, not permission to trust arbitrary firmware that
claims that schema. Source firmware must also match an exact supported source
image and known diagnostic protocol.

## Clean state before preparation

Use a fresh full ROM capture and a second read of NVM plus journal. Require exact
source code, manifest, protected regions and marker validation against the
supported source image. Require an empty journal header; a nonzero journal data
page alone is normal after a successful save. Never replay or discard a pending
journal as part of a general update.

Require known FD01 status with `storage_failed == false`, `page_dirty == false`
and `batch_depth == 0`. A cached clean page is allowed. Dirty RAM cannot be
reconstructed from FD00 flash reads and must not silently disappear on restart.
RGB also has a separate delayed-save flag in `ak820_rgb.c`; current FD01 does not
expose it. Before claiming all recent settings are preserved, expose all pending
save state in a supported diagnostic revision, or explicitly limit the contract
to already durable settings and reject unsupported source versions. Waiting an
arbitrary interval alone does not prove RAM is clean.

Current `diagnostic.capture(..., code=None)` does not request FD01. It can produce
a stable ROM capture while dirty RAM or a latched storage failure exists. Supply
the validated source build's code, not the target build's code, and require its
known status reply. Do not use a stable flash snapshot as a substitute for this
check. Reject unsupported status versions instead of guessing.

A timeout, changed readback, pending journal, storage failure or dirty state
stops the attempt. Do not flush, restore, retry, reset or recover automatically.
Save partial capture and report the reason.

## Minimal integration

1. Add a pure offline preparation function alongside `write_trial` in
   `util/prepare_ak820_trial.py`, or a dedicated updater preparation module.
   Inputs: original OEM recovery backup/reference, exact supported source image,
   fresh full source ROM, validated source status, target IHX/MAP. Validate all
   inputs before creating a new output directory. Reuse `verify_live`,
   `migrate_vial_nvm`, `pack(..., trial=False)` and `verify_payload`.
2. Give general update provenance a distinct format/mode. Record hashes of full
   source ROM, source image/build/schema, original recovery backup, target build,
   migrated NVM and final payload, plus migration report. Keep original inputs
   immutable. Keep existing RC6 repair pins and validator unchanged.
3. Add a corresponding validator in `util/ak820_tool.py`. `flash` must explicitly
   admit the new validated update mode; its existing prepared-repair hook must
   not become a generic bypass. Bind every validation to the exact image shown
   for physical consent. Repeat file/hash, release, provenance and device
   identity checks immediately before the first destructive command.
4. In `tools/installer/ak820.py`, add a general update orchestration function.
   Reuse the existing fresh Esc + left Control consent, cancellation guards,
   loader wait, one flash and postflash verification. After unlock and before
   loader entry, recheck clean status and NVM/journal against the accepted
   snapshot. If settings changed, stop; do not rebuild behind the displayed hash.
5. Route the GUI Update button in `tools/installer/gui.py` to this path when
   general updates are ready. Keep the repair session explicitly identified.
   No typed confirmation, external Vial step or manual Bootloader action.

After flashing, verify target code, protected regions, boot status/main-loop
progress, stable journal, clean status and exact migrated durable NVM. Any bad
readback or storage fault stops with logs, without a second flash. The installer
cannot prevent another configuration tool from editing settings between final
application checks and bootloader entry; a strict atomic snapshot needs firmware
support to freeze settings during the consent-to-loader transition. Do not claim
that current host checks provide that guarantee.

## Verification to add

Existing offline coverage includes `tests/ak820_package/test_entropy_schema.py`
(both encoder directions/layers, maps, lighting/header, macros, exact capacity,
malformed streams and current-schema byte copy), `test_legacy_trial_migration.py`
(verified old trial migration) and `tools/installer/test_prepared_update.py`
(repair pins, consent order, cancellation before erase, malformed replies,
missing loader, unstable capture, postflash storage fault and no second flash).
These files were inspected; no tests were executed for this design-only task.

Add offline tests for permanent-to-permanent preparation on both supported
schemas; exact NVM copy on current schema; old-schema migration with all layers,
both encoder directions, header/lighting, macros and inactive tail; immutable
input backups; wrong source build/protected bytes/marker; unknown schema/status;
dirty page, batch in progress, pending journal and latched storage fault;
overflow/incomplete macro; tampered provenance or files after consent; settings
changed after capture; cancellation at each pre-erase boundary; one flash only;
postflash NVM mismatch and every failure stopping without cleanup writes.
Use fake transports and synthetic images. Default commands stay offline or
read-only; explicit execution options and authorization gate mutation tests.

Offline migration tests prove byte transformations and failure ordering only.
Live protocol behavior, durable saves, cold boot, power loss, recovery, actual
key/encoder behavior and physical Alt Repeat remain deferred. Host/CPU journal
power-cut models do not establish the real device's storage behavior.

Writing follows the owner's supplied plain-language instructions. The writing
style skill was read; no style-retrieval tools were available or claimed.
