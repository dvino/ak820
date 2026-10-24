Русский перевод: [Хранение настроек модулей](ru/MODULE-STORAGE.md).

# Module settings storage

Schema `0x082003` adds typed settings for the `full-tap-dance`, `full-key-overrides`
and `full-qmk-settings` source profiles. Schema `0x082002` remains the host default.
No schema03 image is added to the installer approval list by this change.

The six keymap layers, encoder table at `0x640`, eight ten-byte Combos at
`0x658`, macro metadata at `0x7f0` and macro buffer at `0x800..0x27ff`
keep their schema02 layout. All addresses are relative to NVM.

| Field | Address | Encoding |
| --- | --- | --- |
| QMK Settings | `0x6a8..0x6bf` | 24-byte versioned record |
| Tap Dance | `0x6c0` | Eight ten-byte `<5H` records |
| Key Overrides | `0x740` | Eight ten-byte `<HHHBBBB` records |

Each entry table places rows 0–5 at `base + index*10` and rows 6–7 at
`base + 64 + (index-6)*10`. A row never crosses a 64-byte journal page.
Padding is reserved.

The settings record starts with `QS`, version 1, payload length 11 and
capabilities `0x3f`. Grave Escape flags occupy byte 5. Little-endian words
at 6, 8, 10, 12 and 14 store Combo term, tapping term, tap delay, Caps Lock
delay and Auto Shift timeout. Defaults are 0, 40, 200, 0, 80 and 175.
Terms and Auto Shift timeout accept 1–1000 ms; delays accept 0–100 ms;
Grave Escape flags accept 0–15. Bytes 16–21 are zero. Bytes 22–23 hold
CRC16-CCITT, initial value `0xffff`, over bytes 0–21, little endian.
An entirely zero or erased record means defaults. Other invalid records fail.

Tap Dance outputs accept KC_NO or basic and modified basic keycodes below
`0x2000`, with low byte `0x04..0xa4` or `0xe0..0xe7`. Term zero means
200 ms; explicit terms accept 1–32767 ms. Empty Key Override rows are zero.
Other rows require trigger `0x04..0xa4`, replacement KC_NO or a modified
basic keycode with low byte `0x04..0xa4`, a layer mask of 1–63 and options
with at least one of bits 0–2. Option bit 6 is forbidden.

## Host migration and backup

`pack.migrate_vial_nvm(..., target_build_id=pack.EXTENSION_BUILD_ID)` explicitly
initializes schema03 from schema01 or schema02. Schema02 fields, including
nonempty Combos, are copied. Existing schema01 macro capacity checks still
apply. Schema03 copies remain byte exact; downgrade to schema02 fails.
`pack` and `verify_payload` also require an explicit target for schema03.
The normal release packaging command retains schema02 defaults.

Backup format `ak820-settings-backup-2` includes a complete typed `extensions`
object. It requires exact reviewed image hashes and schema03 profile metadata
(`extensions_version: 1`, `combos_version: 1`, and a supported profile name).
The declared features must match `ak820_profiles.configuration(profile)` exactly.
Each current profile enables only its named module. Export checks getters only
for enabled modules and checks the exact advertised table counts and settings IDs.
Restore rejects differences in inactive tables or inaccessible settings before
writing any field. All typed storage remains part of the backup.
The existing release pins are unchanged. Duplicate, missing and unknown typed
JSON fields fail validation. Legacy backups may initialize only empty/default
extension targets. Schema03 backups cannot restore to schema02.

DeviceAPI uses existing Vial dynamic entry commands for table rows and QMK
Settings query/get/set/reset commands for settings. Writes still require the
explicit write-enabled adapter and the restore workflow's physical unlock.
Every new setter checks its ACK, getter and full NVM readback, including
neighboring bytes. Failure stops the operation without retry or recovery.
Settings operations that already match the effective defaults preserve a blank
zero or erased record and verify the original bytes without writing.
These host checks do not prove physical key behavior or power-loss persistence.
