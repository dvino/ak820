Русский перевод: [Передача для разработки приложения](ru/FIRMWARE-HANDOFF.md).

# Desktop development handoff

The beta.3 source defines ten profiles and Python installation scripts for Windows and Linux x86_64. Standalone GUI installers are excluded; the companion application remains a separate development effort. [Firmware status](../../docs/STATUS.md) distinguishes qualification, release and physical validation.

Beta.3 adds two exact-image capabilities. `combo_actions: ["caps-word-toggle"]`
permits Caps Word (`0x7c73`) as a Combo output. `macro_layer_tap: true` permits
macro-on-tap, layer-on-hold codes `0x40F0`–`0x45FF` with low bytes `F0`–`FF`
on physical matrix keys. Missing fields mean no support. Earlier beta.2 rows
remain source-only entries in `historical_profiles`; their original keycodes
and settings must not be inferred from the new profile with the same name.

## Firmware and profile contract

The current catalog contains `main`, `game`, `mmo`, `typing`, `code`, `pointer`, `onehand`, `creative`, `shortcuts` and `multios`. The default is `main`. See the [individual profile guides](../../docs/profiles/README.md) for complete compositions. All functions cannot fit in controller memory at once; a Vial layer cannot enable an absent module. Historical CLI names are not additional choices in the new installer.

All ten profiles include QMK Settings and storage schema 03. Storage reserves all three extension types, but editors expose only modules and runtime QSIDs enabled by the exact image. Beta.3 `main` and `typing` enable Auto Shift and expose QSID 4. Earlier beta.2 `main` does not. `game`, `mmo`, `main` and `creative` retain Direct; the other profiles retain built-in effects and global RGB controls without per-LED host frames.

## Direct v1

Direct v1 exposes an 82-entry HSV8 palette (246 bytes), using Vial LED indices. Negotiate capabilities before use; do not infer support from the profile name. `direct_snapshot()` reads a coherent palette generation. `set_direct_frame()` sends all entries in sequential chunks of at most eight LEDs, then commits once against the snapshot generation. The host clamps V to 160. An unfinished upload expires after 1000 ms; incomplete, malformed or conflicting uploads do not replace the active palette. A committed frame advances generation. Conversion and scan-boundary publication can still be pending when the commit returns.

The palette is RAM-only. Snapshot and frame operations do not select Direct, enable RGB, or write EEPROM. Suspend or USB keyboard reset cancels pending work. Physical LED and DMA behavior still needs device validation. See the [Direct guide](../../docs/DIRECT.md) for packet fields and the complete API.

The [matrix](../firmware-matrix.json) records measured resources, settings and exact image identity. The [capability catalog](../capability-catalog.json) describes functions verified for each exact image and remains development-only; it does not approve a release or authorize a device write. Match catalog entries by IHX SHA256, and negotiate runtime support with Direct before using it. Check installer approval, per-profile approved bundles, settings identities and settings transitions separately for each image. Do not infer capabilities from a profile name.

The `guide.en` and `guide.ru` paths are relative to `web/`. During development, resolve them against the current checkout; a published companion package must include matching guides for offline help. Do not combine the old `beta.1` catalog with new profile images.

## Typed settings and validation

Keep the existing six-layer keymap, encoder mapping, macros, Combo, and RGB behavior. Add schema 03 editors only when the exact image enables the corresponding module:

- **Tap Dance:** eight entries, `TD(0)`–`TD(7)`. Actions accept `KC_NO` or basic/modified basic keycodes in the documented ranges; special actions, nested dances, layers, macros, consumer and mouse actions are rejected. A term of zero means 200 ms; explicit terms are 1–32767 ms. Each entry uses its own term, not QMK Settings QSID 7.
- **Key Overrides:** eight rows. Validate the trigger (`0x04–0xa4`), replacement (`KC_NO` or a supported modified basic keycode), six-layer mask (1–63), and option bits. Empty rows are all zero; invalid disabled rows are still invalid. Unsupported option bits and rows without an activation option must fail validation.
- **QMK Settings:** expose only IDs advertised by the image. The current typed set includes Grave Escape modifiers (0–15), Combo term (1–1000 ms), tapping term (1–1000 ms), tap-code delay (0–100 ms), Caps Lock delay (0–100 ms), and Auto Shift time (1–1000 ms only when Auto Shift is enabled). The modifier-mask default is 0; the timing defaults are 40, 200, 0, 80, and 175 ms respectively. QSID 4 remains stored in schema 03 but is unavailable unless both QMK Settings and Auto Shift are enabled. Tap-code delays apply to the documented `tap_code()` helpers, not compact tap/hold gestures, Tap Dance, or explicit macro timing.

Use the shared typed codec and firmware contract for range, reserved-byte, CRC and row validation. A setting write must check the response, getter and full NVM readback, including neighboring bytes. Stop at the first error or mismatch; do not retry or attempt blind recovery. An unchanged effective value must preserve blank/default storage without an unnecessary write. See [Tap Dance](../../docs/COMPACT-TAP-DANCE.md), [Key Overrides](../../docs/COMPACT-KEY-OVERRIDES.md), and [QMK Settings](../../docs/QMK-SETTINGS.md).

## Image matching, connection, and backups

Validate the selected firmware source and its exact image identity against a catalog entry before asking for operation permission or enabling any write path. Match the connected model/revision and installed CODE to that entry; unknown or ambiguous identity blocks mutation. Start with an explicit, read-only connection and read the complete supported settings before enabling edits. Require a user action for each change, verify it by readback, and stop on disconnect, timeout, storage error, or mismatch. Never retry writes or continue automatically. These defaults follow [the requirements](REQUIREMENTS.md), and do not grant permission to operate a physical keyboard during development.

Use `ak820-settings-backup-1` for schema 02 and `ak820-settings-backup-2` for schema 03, including all typed extension data when present. Backups are tied to reviewed image hashes and schema/profile metadata. Validate shape, fields, ranges, and compatibility before applying; preserve all typed stored data in export. A schema 03 backup cannot be restored to schema 02. Differences in inactive tables or settings without an enabled setter block restoration before any write. Schema 01/02 migration to schema 03 requires an explicit target, preserves schema 02 fields including Combos, and retains macro-capacity checks. See [module storage](../../docs/MODULE-STORAGE.md) and [settings backup requirements](REQUIREMENTS.md#5-settings-backups-and-oem-firmware).

The additive host API is `load_profile(bundle, native_backup, trusted_catalog=matrix)`. The matrix must come from a separately trusted source. Its per-image `settings_identity` contains exact IHX and permanent packed CODE SHA256, definition SHA256, NVM schema, profile features, explicit supported keycodes, and Combo/extension versions. The CODE hash covers the complete `0x2800..0xc6ff` range, including the entry, vectors and copied OEM erase helper; the linked-window hash is a different identity. The loader reconstructs that packed CODE from the selected bundle and validated OEM reference, then checks the recorded hash. Missing metadata, unknown contract fields, changed features, unsupported commands or a hash mismatch block settings use. A matrix without packed identity can describe a build candidate but cannot supply this settings contract. The default API retains the published image pins and release policy.

A catalog allows same-image restore by default. Other image pairs require an explicit `settings_transitions` record with exact source and target IHX hashes; list order, profile names and shared schema grant no transition. A reviewed pair still has to pass schema, enabled-module and stored-value checks. Validate every matrix and encoder mapping and every key-bearing macro command. `image_keycode_supported` also checks the source: Tap Dance, Leader, dynamic macro controls and Auto Shift controls need physical matrix positions; macro actions cannot invoke Space Cadet. Key Override mode controls accept a macro tap, but explicit macro down/up commands are rejected. Mouse Keys support four cursor directions, five buttons and four wheel directions; extra buttons and acceleration commands remain unavailable. Temporary dynamic recordings, held/queued One Shot state and session mode switches are not durable settings and are not restored.

The current Python scripts use `tools/installer/settings_backup.py` and `settings_workflow.py` for durable settings backup and restore. Direct palette export adds an optional, separately hashed `direct-ram.json` sidecar only for an exact Direct v1 image with runtime support. The explicit `restore_direct_palette` API restores it as a complete RAM frame; it does not select Direct mode or write EEPROM. A future companion should implement these contracts without depending on Python at runtime. Firmware preparation and OEM recovery must use existing image ownership, protected-region and exact-source checks. A filename or USB VID/PID alone does not prove that a factory image belongs to the connected keyboard.

## Desktop implementation sequence

Follow [the agreed plan](PLAN.md) without selecting a new UI foundation in this handoff:

1. Test the Entropy native Rust/egui editor and browser/Wasm path with recorded AK820 replies and a fake transport. Compare the bounded Pipette baseline against the same required features and fixture failures. Separately prove browser permission and a read-only request; assess the native loader separately. Do not reset, enter a loader, or write during this stage. Record the working end-to-end result, maintenance, license, coverage and adaptation cost before choosing a base.
2. Define shared model, protocol, firmware, backup and release/catalog data contracts. Reuse the current catalog/configuration generators and the Python packer/workflows as behavioral references. Add fixtures for exact-image acceptance, rejection, migration, limits, and backup compatibility. Keep catalog generation and image qualification explicit; do not infer capabilities from a release label or a profile name.
3. Adapt the selected native client and shared editor for Windows, Linux x86_64, macOS arm64 and x86_64. Implement exact-image capability display, complete reads, supported editors, help in Russian and English, local backup history, offline firmware/catalog/help, and fail-stop USB behavior. Verify each OS build, USB path, startup, and memory use separately.
4. Add firmware update, restore and OEM rollback only after source ownership, device matching, and the operation sequence are proven. Keep fresh backup, exact image checks, explicit confirmation, cancellation before erase, post-write verification, and stop conditions. Beta.3 provides Python installation scripts for Windows and Linux x86_64; it does not include standalone GUI installers. Keep confirmation, backup, exact-image, cancellation and stop requirements for any future update flow.
5. Treat the OS-layout helper as a separate optional stage. Profiles that provide the OS indicator or Mac/PC support require exact-image offline qualification before release. The desktop helper, platform layout detection and end-to-end integration with a physical keyboard remain to be implemented and tested. Pause helper device access during firmware operations.

Requirements and acceptance gates remain in [REQUIREMENTS.md](REQUIREMENTS.md); stage dependencies and stop conditions remain in [PLAN.md](PLAN.md). Current published firmware and verification state are recorded in [firmware status](../../docs/STATUS.md).
