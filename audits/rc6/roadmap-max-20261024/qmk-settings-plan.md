# QMK Settings design note

**Status:** proposal only. QMK Settings remains disabled; no storage or protocol change is approved by this note. This is a source audit and design, not a build, device test, or image qualification.

## Upstream setting inventory

`quantum/qmk_settings.c` defines the Vial QSID table. `qmk_settings.h` defines the in-RAM widths, and the named default macros below supply reset values. Integer settings are transferred in the target's native little-endian representation; the `magic` setting is a 32-bit flag word. The table is conditional on `QMK_SETTINGS`; mouse IDs are additionally omitted unless `MOUSEKEY_ENABLE` and not `MK_3_SPEED`.

| QSID | Width | Upstream setting | Reset/default | Handler / current AK820 relevance |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | Grave Escape modifier overrides (ALT/CTRL/GUI/SHIFT bits) | 0 | `process_grave_esc.c` consumes these bits; Grave Escape is enabled on the board. |
| 2 | 2 | Combo term, ms | `COMBO_TERM` 50 ms upstream; board compact engine is explicitly fixed at 40 ms | `get_combo_term()` is the upstream hook. `ak820_combo.c` has a literal 40 ms threshold; QSID 2 would do nothing until that engine is wired to the setting. |
| 3 | 1 | Auto Shift flags | 0 | Auto Shift is disabled; flags are dormant. |
| 4 | 2 | Auto Shift timeout, ms | `AUTO_SHIFT_TIMEOUT` 175 ms | Auto Shift is disabled; timeout callback is dormant. |
| 5 | 1 | One Shot tap-toggle count | `ONESHOT_TAP_TOGGLE` 5 | Generic One Shot behavior is replaced by `NO_ACTION_ONESHOT` plus the bounded compact modifier implementation. Tap-toggle is not implemented there. |
| 6 | 2 | One Shot timeout, ms | `ONESHOT_TIMEOUT` 5000 ms | Compact One Shot has no timeout; do not expose this ID as effective. |
| 7 | 2 | Tapping term, ms | `TAPPING_TERM` 200 ms | `ak820_tapping.c` uses fixed 200 ms. It needs an explicit compact-engine read of the saved value before QSID 7 is effective. |
| 8 | 1 | Tapping policy bits: permissive hold, hold-on-other-key-press, force hold, retro tapping | 0 | The custom engine implements a fixed “other press resolves hold” rule and omits the other upstream policies; reject this ID rather than expose inert/unsupported combinations. |
| 9 | 2 | Mouse delay, ms | 5 kinetic / 150 inertia / 10 default | Mouse Keys disabled. |
| 10 | 2 | Mouse interval, ms | 10 kinetic / 16 inertia / 20 default | Mouse Keys disabled. |
| 11 | 2 | Mouse movement delta | 16 kinetic / 1 inertia / 8 default | Mouse Keys disabled. |
| 12 | 2 | Mouse maximum speed | 32 inertia / 10 otherwise | Mouse Keys disabled. |
| 13 | 2 | Mouse time to max | 32 inertia / 30 otherwise | Mouse Keys disabled. |
| 14 | 2 | Mouse wheel delay, ms | `MOUSEKEY_WHEEL_DELAY` (10) | Mouse Keys disabled. |
| 15 | 2 | Mouse wheel interval, ms | `MOUSEKEY_WHEEL_INTERVAL` (80) | Mouse Keys disabled. |
| 16 | 2 | Mouse wheel maximum speed | `MOUSEKEY_WHEEL_MAX_SPEED` (8) | Mouse Keys disabled. |
| 17 | 2 | Mouse wheel time to max | `MOUSEKEY_WHEEL_TIME_TO_MAX` (40) | Mouse Keys disabled. |
| 18 | 2 | Tap-code delay, ms | `TAP_CODE_DELAY` 0 in `action.h` when unset; `qmk_settings.h` fallback says 10, so the setting-enabled compile path must pin this explicitly | Used by `quantum.c`, `action.c`, Vial and related call sites; relevant even without another optional engine. |
| 19 | 2 | Caps Lock tap-hold delay, ms | `TAP_HOLD_CAPS_DELAY` 80 | Used by `quantum.c` and `action.c`; relevant. |
| 20 | 1 | Tapping toggle count | `TAPPING_TOGGLE` 5 | Generic action engine calls it; custom AK820 tap engine does not implement multi-tap locking. Exclude unless a caller is demonstrated. |
| 21 | 4 | Magic/keymap configuration flags | Live `keymap_config.raw`, not a constant default | Generic Magic getter/setter can mutate modifier swaps, GUI suppression, Grave/Escape, Backslash/Backspace and NKRO and calls `clear_keyboard()` plus `eeconfig_update_keymap()`. `MAGIC_ENABLE=no`; board instead offers a bounded volatile NKRO profile, so do not expose this broad setter. |

IDs 2 and 7 are useful only after adapting the compact engines: the existing upstream getters alone do not change their hard-coded timing. A first meaningful subset is therefore **QSID 1, 2, 7, 18 and 19**, with 2 and 7 enabled only in the same change that replaces the compact-engine literals. This is five settings and nine payload bytes, excluding metadata. If scope must stay to handlers already read by current board code, start with 1, 18 and 19 and leave Combo/tap-hold timing fixed. Do not include IDs 3–6 or 9–17 while their modules are disabled; do not include policy IDs 8 and 20 or broad Magic ID 21 while their semantics are absent or intentionally excluded.

The 36-byte `qmk_settings_t` is an upstream RAM struct, not a recommended AK820 persistent ABI. It includes settings for disabled Auto Shift, One Shot, Mouse Keys and unsupported tap policies, and its layout/order is expressly changeable (`qmk_settings.h`). A Vial-visible ID is not evidence that a current handler consumes it.

## NVM space and fixed data

The current dynamic layout is derived in `quantum/dynamic_keymap.c`:

| NVM offset | Size | Current use |
| ---: | ---: | --- |
| `0x0040` | `6 * 16 * 8 * 2 = 1536` (`0x600`) | Six 16×8 keymap layers |
| `0x0640` | 24 (`0x18`) | One encoder × six layers × two directions × two bytes |
| `0x0658` | 0 | QMK settings today (`VIAL_QMK_SETTINGS_SIZE=0` because the flag is disabled) |
| `0x0658` | 0 | Tap Dance today (`VIAL_TAP_DANCE_SIZE=0`) |
| `0x0658`–`0x06A7` | 80 (`8 * sizeof(vial_combo_entry_t)`, 10 each) | Eight Combo slots; compile-time assertion fixes base `0x658`, slot count 8 and slot size 10 |
| `0x06A8`–`0x07EF` | 328 (`0x148`) | No current dynamic feature allocation; upper boundary is `AK820_MACRO_BUSY_ADDR` |
| `0x07F0`–`0x07F2` | 3 | Macro busy marker and published length (`ak820_macro.h`) |
| `0x0800`–`0x27FF` | 8192 | Sixteen Vial macro slots/stream capacity |

This verifies a **logical gap** of 328 bytes after all current Combo slots and before macro metadata, with the exact pinned configuration. The `VIAL_KEY_OVERRIDE_EEPROM_ADDR + VIAL_KEY_OVERRIDE_SIZE <= AK820_MACRO_BUSY_ADDR` assertion reserves the intervening address domain for future dynamic features; current `KEY_OVERRIDE_ENABLE=no` makes its size zero. `DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR=0x800`, six layers and 16 macros are explicitly fixed in `keyboards/ajazz/ak820/config.h` and `ak820_macro.c`. The report does not label the gap universally free: code must keep Combo at `0x658`, avoid `0x7f0..0x7f2`, preserve macro data from `0x800`, and validate its new address and write path against the NVM journal/page rules. `DYNAMIC_KEYMAP_EEPROM_MAX_ADDR=10239` and the 8 KiB macro allocation consume the rest of the advertised dynamic area; they do not erase the lower logical gap.

The NVM begins at absolute `0xC700` (`ak820_nvm.h`; `pack_ak820.py` uses relative offsets in the NVM slice). Thus the proposed gap is absolute `0xCDA8`–`0xCEEF`; Combo begins at absolute `0xCD58`, macro metadata at `0xCEF0`, and macro data at `0xCF00`. The device NVM/journal extends beyond these dynamic regions. Existing Combo writes are ten-byte records and the backup path compares durable NVM bytes after each write (`tools/ak820_device_protocol.py`, `settings_backup.py`). Do not treat gap bytes as safe without page-boundary, journal, power-cut and write-range tests for the selected record transaction.

## Proposed record and API contract

Keep the upstream Vial QSID protocol (`vial_qmk_settings_query/get/set/reset`, `quantum/vial.c`) for client compatibility, but replace direct persistence of the raw 36-byte struct with an AK820-owned, typed encoding. Propose a compact fixed record at NVM-relative `0x06A8`, maximum 32 bytes for v1, wholly inside the measured gap. Suggested fields: 2-byte magic, 1-byte record version, 1-byte payload length, 1-byte supported-setting bitmap, the five supported typed values, and a checksum over header plus payload; pad remaining record bytes with a specified erased/default value. Exact magic, checksum algorithm and transaction are schema decisions to approve and test, not settled here. A record must reject unknown versions, lengths, reserved bits, invalid values and checksum failures as a unit; never partially apply bytes or interpret a different version as the current struct.

Define reset values in the board profile rather than relying on inconsistent upstream fallbacks. The current board behavior is Grave Escape overrides off, Combo term 40 ms, compact tapping term 200 ms, tap-code delay 0 ms, Caps Lock delay 80 ms. Reset must restore those exact behaviors, clear active/pending owners where a timing/policy change could affect them, update runtime handlers, and persist via the same checked transaction. Startup must initialize the runtime values from a validated record or these defaults. Until the record is validated, Vial must not report partially loaded state.

For each exposed QSID, enforce its exact width, range and effective hook before ACK. In particular, changing a timing value during an active Combo or pending tap decision must have a defined boundary (recommended: clear/cancel with the existing ownership safeguards, then apply); setting the same value should avoid flash writes. QSID 21 remains unavailable until a deliberate per-flag Magic policy, persistent behavior, and interaction with the separate NKRO control are designed.

## Backup, restore and migration proposal

The current local backup format is `ak820-settings-backup-1`; it contains typed keys, encoders, layout options, macros, RGB and optional Combos, but no QMK Settings field. Restore writes those typed operations through the Vial protocol and checks durable NVM. `settings_backup.py` pins exact firmware identities and NVM schema; `pack_ak820.py` migrates known legacy layouts by constructing a new NVM image and copying defined fields. A new firmware feature must not be restored into an old exact image simply because the user values resemble the old profile.

Proposed transition:

1. Add a new NVM schema/build identity for the record layout and a new typed backup format (for example, format 2) with `qmk_settings: {version: 1, values: ...}`. Keep integer types explicit and reject unknown keys, duplicate JSON fields, out-of-range values, missing required values and unsupported source/target image identities. Include exact source build/image identity as today.
2. Export by decoding the validated NVM record and cross-checking every value against Vial QSID getters. Preserve the complete raw NVM and full-ROM evidence as current workflow does. Never expose unknown record bytes as editable typed values.
3. Restore only from format 2 to an exact compatible format-2 target. Apply typed QSID setters only after fresh unlock, before/after durable reads, and stop on any mismatch or fault. Setters and record commits must leave Combo slots, macro metadata, macro stream and surrounding bytes unchanged. Do not rollback/reset/retry after a failure, following the existing workflow contract.
4. Forward-migrate a known old NVM schema by constructing the destination using the existing explicit migration, copying all currently defined legacy fields, initializing the new settings record to board defaults, and keeping the existing six layers, all 16 macros and their complete published stream. Existing format-1 backups mean defaults for new settings; they must never silently clear/change nonempty Combo slots or macro data. Require an explicit compatibility rule for each exact old-to-new image pair.
5. Reject unknown/newer record versions and backups from newer schema to older firmware. Older firmware must retain NVM and enter the existing schema-fault/no-write path rather than rewrite or reinterpret the new record. Existing restore source-rank protection already rejects downgrade; extend it to the new schema/record capability.

The migration code currently zero-initializes a new NVM image and copies keys, encoders, macros and defined header/RGB fields; this means default initialization can be explicit and reproducible rather than copying arbitrary gap bytes. Preserve this property and report each field copied/defaulted. The raw NVM file is evidence, not a license to import arbitrary bytes. No storage migration, API changes, or client compatibility has been implemented or approved by this report.

## Disabled behaviors and interactions to retain in the roadmap

- `AUTO_SHIFT_ENABLE=no`, `MOUSEKEY_ENABLE=no`, `MAGIC_ENABLE=no`, `SPACE_CADET_ENABLE=no`, `TAP_DANCE_ENABLE=no`, `KEY_OVERRIDE_ENABLE=no`, `LEADER_ENABLE=no`, `DYNAMIC_MACRO_ENABLE=no`, and ordinary `COMBO_ENABLE=no`; Combos use the separate `AK820_COMPACT_COMBO` engine.
- `NO_ACTION_ONESHOT` and compact One Shot intentionally omit layer One Shot, tap-toggle and timeout. QSID 5/6 must not suggest otherwise.
- Compact tapping has one pending decision and fixed hold-on-other-key behavior; upstream `QS.tapping` getter callbacks do not make the custom engine support all four policies.
- The board's Combo engine accepts only two ordinary key inputs, has an 8-slot limit, excludes encoder pulses as candidates, and uses fixed 40 ms matching today. Setting timing is not permission to enable upstream generic Combo semantics.
- Vial QMK settings Reset also resets generic keymap config flags in upstream source and calls `clear_keyboard()`; an AK820 implementation must preserve established key ownership/cancellation safety and must not inadvertently enable broad Magic/NKRO state changes.
- `TAP_CODE_DELAY` may affect macro/string/Vial timing as well as tap behavior. Bounds and blocking/latency effects require review; do not silently inherit different upstream fallback values.
- Settings values are feature-set-sensitive. Installer backup/restore and package identity must bind them to the exact approved image/profile, as already required for Combos and other saved values.

## Evidence paths

- `docs/ROADMAP.md`, `docs/BUILD-PROFILES.md`: QMK Settings disabled, 36-byte struct, fixed current Combo/tap timing, migration and qualification requirements.
- `qmk-8051-ak820/quantum/qmk_settings.h`, `qmk_settings.c`: struct members, widths, QSID table, conditionals, reset logic, getters, setter callbacks and Magic side effects.
- `qmk-8051-ak820/quantum/dynamic_keymap.c`: `VIAL_ENCODERS_EEPROM_ADDR`, `VIAL_QMK_SETTINGS_EEPROM_ADDR`, tap-dance/Combo/override address arithmetic and static assertions.
- `qmk-8051-ak820/keyboards/ajazz/ak820/config.h`, `rules.mk`, `ak820_combo.c`, `ak820_tapping.c`: exact board limits and compact-engine behavior.
- `qmk-8051-ak820/keyboards/ajazz/ak820/ak820_nvm.h`, `ak820_macro.h`, `ak820_macro.c`: NVM bounds, macro metadata and capacity invariants.
- `qmk-8051-ak820/util/pack_ak820.py`: explicit known-schema validation, empty-NVM construction and forward migration.
- `quantum/vial.c`, `quantum/vial.h`: QMK Settings command IDs and Vial command dispatch.
- `tools/ak820_device_protocol.py`, `tools/installer/settings_backup.py`: Combo wire/storage representation, exact image pins, typed backup and durable restore behavior.

## Independent review

An independent review checked the QSID widths, defaults and conditional handlers,
Magic/reset side effects, struct size, address arithmetic and storage assertions
against the vendored source. The 328-byte logical gap, absolute addresses,
migration initialization and restore downgrade guard agree with that source.
The proposal-only package was approved with no blocking findings; persistence,
API, migration and runtime behavior remain unimplemented and unapproved.
