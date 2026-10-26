Русский перевод: [Хранение настроек модулей](ru/MODULE-STORAGE.md).

# Module settings storage

All ten current beta.2 profiles use NVM schema `0x082003`. The low-level packer API defaults to legacy schema `0x082002` unless a target
schema is selected explicitly. The beta.2 profile build selects schema `0x082003`;
the low-level API default does not change its format.
The schema adds typed storage for eight Tap Dance entries, eight Key Override
entries and QMK Settings.

The six keymap layers, encoder table at `0x640`, eight ten-byte Combos at
`0x658`, macro metadata at `0x7f0` and macro buffer at `0x800..0x27ff`
keep their prior layout. The extension addresses below are relative to NVM.
Header addresses and encoding are unchanged.

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

## Profiles, migration and backup

Every profile stores all eight Tap Dance rows, all eight Key Override rows and
the QMK Settings record. QMK Settings are available in all ten profiles. Tap
Dance is active only in `mmo`, `onehand`, `creative` and `shortcuts`. Key
Overrides are active in `main`, `game`, `typing`, `code`, `pointer`, `shortcuts`
and `multios`; they are inactive in `mmo`, `onehand` and `creative`. Storage in an
inactive table is retained, but the installer does not read or restore its
values as active settings. It will stop before writing if a backup contains
inactive values that cannot be reproduced by the target.

`pack.migrate_vial_nvm(..., target_build_id=pack.EXTENSION_BUILD_ID)` explicitly
initializes schema `0x082003` from schema `0x082001` or `0x082002`. Schema02
fields, including nonempty Combos, are copied. Existing schema01 macro capacity
checks still apply. Copies already using schema03 remain byte exact; downgrade
to schema02 is rejected. Low-level `pack` and `verify_payload` also require an
explicit target to produce schema03. The ordinary low-level packaging default
remains schema02.

The installer uses typed backup format `ak820-settings-backup-2` for these
profiles. It includes all extension tables and settings, and checks exact image
hashes and profile metadata. Declared features must match the selected profile.
Legacy `ak820-settings-backup-1` backups can initialize extension storage only
when target tables are empty and QMK Settings are at defaults. A schema03
backup cannot be restored to schema02. The approved profile image identities
and offline transition limits are in [Status](STATUS.md).

Direct RGB palette values and volatile module state are not part of the backup.
A value that the target cannot reproduce stops restore before its first write.
These format checks do not establish physical key behavior or persistence after
power loss.
