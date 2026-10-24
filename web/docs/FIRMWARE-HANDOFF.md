Русский перевод: [Передача для разработки приложения](ru/FIRMWARE-HANDOFF.md).

# Desktop development handoff

This note connects the current AK820 firmware contracts to the planned desktop configurator. It is an implementation handoff, not a desktop release claim. The published firmware release remains [v0.6.0-alpha.3](../../docs/STATUS.md). The [qualified development catalog](../../audits/rc6/module-completion-20261024/final/capability-catalog.json) contains the four fully checked images. Source profile definitions alone do not make an image a qualified catalog entry.

## Firmware and profile contract

The firmware defines 24 named profiles. Each profile is selected as a whole; there is no supported arbitrary feature combination or generic QMK/Vial editor. The profile names are:

`standard`, `nkro`, `one-shot`, `nkro-one-shot`, `space-cadet`, `nkro-space-cadet`, `one-shot-space-cadet`, `full`, `full-tap-dance`, `full-key-overrides`, `full-qmk-settings`, `full-mac-pc`, `full-mac-pc-os-indicators`, `full-os-indicators`, `full-leader`, `full-gui-lock`, `full-ctrl-gui`, `full-dynamic-macro-gui`, `full-mouse-auto-shift-gui`, `full-auto-shift-dynamic-macro`, `full-dynamic-macro`, `full-mouse`, `full-auto-shift`, and `full-mouse-auto-shift`.

The catalog must report the exact image and its enabled features. Schema 02 profiles use the existing settings layout. The three extension profiles—`full-tap-dance`, `full-key-overrides`, and `full-qmk-settings`—use schema 03. Schema 03 reserves storage for all three extension types, but each profile enables only its named module. A reserved table or stored value does not expose a control: use the catalog's enabled module entries and enabled QSIDs. The other 21 profiles use schema 02 and have no typed extension storage.

Profiles are individually configured and qualified. There is no all-module combined build. A catalog entry is valid only for its exact linked image and completed evidence; source metadata and host tests alone are insufficient. See [profile definitions](../../qmk-8051-ak820/util/ak820_profiles.py), [module storage](../../docs/MODULE-STORAGE.md), and the [development catalog contract](../../docs/DEVELOPMENT-CATALOG.md).

## Typed settings and validation

Keep the existing six-layer keymap, encoder mapping, macros, Combo, and RGB behavior. Add schema 03 editors only when the exact image enables the corresponding module:

- **Tap Dance:** eight entries, `TD(0)`–`TD(7)`. Actions accept `KC_NO` or basic/modified basic keycodes in the documented ranges; special actions, nested dances, layers, macros, consumer and mouse actions are rejected. A term of zero means 200 ms; explicit terms are 1–32767 ms. Each entry uses its own term, not QMK Settings QSID 7.
- **Key Overrides:** eight rows. Validate the trigger (`0x04–0xa4`), replacement (`KC_NO` or a supported modified basic keycode), six-layer mask (1–63), and option bits. Empty rows are all zero; invalid disabled rows are still invalid. Unsupported option bits and rows without an activation option must fail validation.
- **QMK Settings:** expose only IDs advertised by the image. The current typed set includes Grave Escape modifiers (0–15), Combo term (1–1000 ms), tapping term (1–1000 ms), tap-code delay (0–100 ms), Caps Lock delay (0–100 ms), and Auto Shift time (1–1000 ms only when Auto Shift is enabled). The modifier-mask default is 0; the timing defaults are 40, 200, 0, 80, and 175 ms respectively. QSID 4 remains stored in schema 03 but is unavailable unless both QMK Settings and Auto Shift are enabled. Tap-code delays apply to the documented `tap_code()` helpers, not compact tap/hold gestures, Tap Dance, or explicit macro timing.

Use the shared typed codec and firmware contract for range, reserved-byte, CRC and row validation. A setting write must check the response, getter and full NVM readback, including neighboring bytes. Stop at the first error or mismatch; do not retry or attempt blind recovery. An unchanged effective value must preserve blank/default storage without an unnecessary write. See [Tap Dance](../../docs/COMPACT-TAP-DANCE.md), [Key Overrides](../../docs/COMPACT-KEY-OVERRIDES.md), and [QMK Settings](../../docs/QMK-SETTINGS.md).

## Image matching, connection, and backups

Validate the selected firmware source and its exact image identity against a qualified catalog entry before asking for operation permission or enabling any write path. Match the connected model/revision and installed CODE to that entry; unknown or ambiguous identity blocks mutation. Start with an explicit, read-only connection and read the complete supported settings before enabling edits. Require a user action for each change, verify it by readback, and stop on disconnect, timeout, storage error, or mismatch. Never retry writes or continue automatically. These defaults follow [the requirements](REQUIREMENTS.md), and do not grant permission to operate a physical keyboard during development.

Use the existing `ak820-settings-backup-2` contract for complete supported settings, including typed extension data when present. Backups are tied to reviewed image hashes and schema/profile metadata. Validate shape, fields, ranges, and compatibility before applying; preserve all typed stored data in export. A schema 03 backup cannot be restored to schema 02. Differences in inactive tables or settings without an enabled setter block restoration before any write. Schema 01/02 migration to schema 03 requires an explicit target, preserves schema 02 fields including Combos, and retains macro-capacity checks. See [module storage](../../docs/MODULE-STORAGE.md) and [settings backup requirements](REQUIREMENTS.md#5-settings-backups-and-oem-firmware).

Reuse `tools/installer/settings_backup.py` and `settings_workflow.py` as behavioral references and port their contracts into the shared desktop model; do not depend on Python at runtime. Firmware preparation and OEM recovery must use the existing image ownership, protected-region, and exact-source checks. A filename or USB VID/PID alone does not prove that a factory image belongs to the connected keyboard.

## Desktop implementation sequence

Follow [the agreed plan](PLAN.md) without selecting a new UI foundation in this handoff:

1. Test the Entropy native Rust/egui editor and browser/Wasm path with recorded AK820 replies and a fake transport. Compare the bounded Pipette baseline against the same required features and fixture failures. Separately prove browser permission and a read-only request; assess the native loader separately. Do not reset, enter a loader, or write during this stage. Record the working end-to-end result, maintenance, license, coverage and adaptation cost before choosing a base.
2. Define shared model, protocol, firmware, backup and release/catalog data contracts. Reuse the current catalog/configuration generators and the Python packer/workflows as behavioral references. Add fixtures for exact-image acceptance, rejection, migration, limits, and backup compatibility. Keep catalog generation and image qualification explicit; do not infer capabilities from a release label or a profile name.
3. Adapt the selected native client and shared editor for Windows, Linux x86_64, macOS arm64 and x86_64. Implement exact-image capability display, complete reads, supported editors, help in Russian and English, local backup history, offline firmware/catalog/help, and fail-stop USB behavior. Verify each OS build, USB path, startup, and memory use separately.
4. Add firmware update, restore and OEM rollback only after source ownership, device matching, and the operation sequence are proven. Keep fresh backup, exact image checks, explicit confirmation, cancellation before erase, post-write verification, and stop conditions. Browser flashing remains a separate required product path; a desktop installer does not replace it.
5. Treat the OS-layout helper as a separate optional stage. Firmware support for the OS indicator and Mac/PC baseline exists in profile source, but the helper, platform layout detection, integration, and exact-image qualification remain work. Pause helper device access during firmware operations.

Requirements and acceptance gates remain in [REQUIREMENTS.md](REQUIREMENTS.md); stage dependencies and stop conditions remain in [PLAN.md](PLAN.md). Current published firmware and verification state are recorded in [firmware status](../../docs/STATUS.md).
