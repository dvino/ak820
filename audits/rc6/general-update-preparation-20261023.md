# Offline durable-settings update plan

2026-10-23. `util/prepare_ak820_update.py` adds a pure preparation function.
It does not open USB, build firmware, reset the keyboard or flash it.
This is one preparation component. GUI integration is not complete.

`prepare_durable_update` accepts the original OEM recovery backup, OEM
references, exact supported permanent source payload, full source ROM,
second NVM plus journal read, raw FD01 reply, explicit source policy and target
IHX/MAP files. It validates every input before creating a new output directory.
The policy pins the complete source payload hash and schema and accepts only
FD01 v1. It is a caller-controlled allowlist decision; it does not authenticate
where the supplied evidence came from. Status dictionaries and freshness flags
are not accepted as evidence. Unknown policy fields or versions fail.

The function reuses native validation, `verify_live`, `migrate_vial_nvm`,
permanent `pack` and `verify_payload`. Current-schema NVM is copied byte for
byte, including inactive bytes, six keymap layers, twelve encoder keycodes,
sixteen macros and RGB settings. Legacy settings use the existing strict
migration. Macro overflow is an error. A dirty page, active batch, storage
fault, pending journal, changed second read or wrong identity stops preparation.
The original backup and source inputs remain unchanged. The original backup
is retained by the caller; the plan records its hash and never treats a Vial
ROM as native recovery.

The only output is `durable-update-plan.json`. It embeds the proposed payload
as hexadecimal text and records hashes for both OEM references, original
recovery, source payload/full ROM/status/repeat read, target IHX/MAP, migrated
NVM and target payload. It records source/target schemas and the migration
report. Existing output directories are rejected.

This format deliberately has no `images.json`, recovery session or generic
flash image filename. The current generic transport cannot consume this plan.
The existing pinned repair validator and its files remain unchanged.

FD01 v1 cannot report the separate delayed RGB save flag. Supplied clean status
and matching flash reads cannot prove that every recent RAM setting is durable
or that settings stayed fixed between checks. The plan therefore always says
`durable-snapshot-only`, sets live freshness and flash authorization false, and
marks the required pending-save visibility and snapshot-freeze capability as
unimplemented with no supported version. No live-ready option exists.

## Verification

Run from the repository root:

```powershell
rtk proxy python -m unittest discover -s qmk-8051-ak820/tests/ak820_package -p test_general_update_preparation.py
```

Result: eight synthetic offline tests passed. They cover current-schema exact
copy and completed-save journal data, legacy migration, malformed and oversized
macros, status versions and storage state, untrusted status assertions, changed
snapshots, protected bytes, code, marker, manifest, unknown schema, input
immutability, no overwrite and rejection by the generic flash-session reader.
The exact-copy fixture assigns distinct nondefault keycodes to every slot on
all six layers and all twelve encoder keycodes. It contains sixteen nonempty
macros, saved RGB header bytes and nonzero unpublished macro capacity. The
assertion compares all 10,240 NVM bytes. Additional failures cover corrupt
original recovery and OEM references and deterministic IHX/MAP edits after
parsing; neither race creates output or changes source/recovery inputs.
Synthetic OEM hash pins and fake transport fixtures are used. No device test
was run. These tests do not prove live protocol freshness, physical key/encoder
behavior, RAM persistence, cold boot, power-loss behavior or successful flashing.

Independent review is still required before commit. Writing follows the
owner's supplied plain-language rules; the writing-style skill was read and no
retrieved style match is claimed.
