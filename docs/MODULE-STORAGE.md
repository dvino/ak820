Русский перевод: [Хранение настроек модулей](ru/MODULE-STORAGE.md).

# Module settings storage

The current candidate uses NVM schema `0x082003` in all ten profiles. The
low-level packer API defaults to legacy schema `0x082002` unless a target schema
is selected explicitly; profile builds select their schema independently. Schema
`0x082003` adds typed storage for eight Tap Dance entries, eight Key Override
entries and QMK Settings. This describes source state, not a published or
qualified release.

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

The 24-byte `QS` record has three versions: v1 length 11/capabilities `0x3f`,
v2 length 15/`0x7f`, and v3 length 17/`0xff`. All use CRC16-CCITT (initial
`0xffff`) over bytes 0–21, stored little endian at 22–23. Common values are
Grave Escape flags (byte 5, 0–15), Combo term (6), tapping term (8), tap delay
(10), Caps Lock delay (12) and Auto Shift timeout (14). Defaults are 0, 40,
200, 0, 80 and 175; terms/timeouts accept 1–1000 ms and delays 0–100 ms.
Version 2 adds QSID 3 at byte 16 (one byte, 0–29; valid bits 0, 2–4), QSID
6 at byte 18 (two bytes, 0–30000), and QSID 22 at byte 17 (one-bit boolean).
Version 3 retains QSID 22 at byte 17 and adds QSID 23, a little-endian Leader
timeout of 1–1000 ms at bytes 20–21; its default comes from the exact target
image. Firmware treats all-zero
or all-`ff` records as defaults; malformed nonblank records fail. Offline backup
must not infer unknown source values from that behavior: blank v2/v3 records are
rejected when source QSID 22 cannot be authenticated.

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
migrates NVM schemas `0x082001` or `0x082002` to `0x082003`. Schema02 fields,
including nonempty Combos, are copied; schema01 macro capacity checks remain.
Settings records migrate monotonically v1→v2/v3 and v2→v3; downgrade is
rejected. Adding QSID 23 requires the exact target-image Leader default.
Low-level `pack` and `verify_payload` require an explicit target for schema03;
the ordinary low-level packaging default remains schema02.

The installer uses typed backup format `ak820-settings-backup-2` for these
profiles. It includes all extension tables and settings, and checks exact image
hashes and profile metadata. Declared features must match the selected profile.
Legacy `ak820-settings-backup-1` backups can initialize extension storage only
when target tables are empty and QMK Settings are at defaults. A schema03
backup cannot be restored to schema02. The approved profile image identities
and offline transition limits are in [Status](STATUS.md).

Format and schema support do not admit an image as a settings source or restore
target. The separate exact-image policy in [Settings backup and
restore](SETTINGS-BACKUP.md) must also pass. Current candidate v3 loading,
restore planning and protocol writes remain blocked; offline codec support does
not qualify images or authorize settings writes.

Direct RGB palette values and volatile module state are not part of the backup.
A value that the target cannot reproduce stops restore before its first write.
These format checks do not establish physical key behavior or persistence after
power loss.
