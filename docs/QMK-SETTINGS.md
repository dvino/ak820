Русский перевод: [Настройки QMK](ru/QMK-SETTINGS.md).

# QMK Settings

Change a small set of timing and behavior settings through Vial.

Profiles with `AK820_QMK_SETTINGS` provide the settings below through Vial.
A change is saved and remains after restart. Reset restores the defaults in this
table. Reset does not change the keymap, macros, Combos or NKRO profile.

| QSID | Setting | Width | Accepted values | Default |
| ---: | --- | ---: | --- | ---: |
| 1 | Grave Escape modifier overrides | 1 byte | ALT=1, CTRL=2, GUI=4, SHIFT=8; combine bits, 0–15 | 0 |
| 2 | Combo matching time | 2 bytes | 1–1000 ms | 40 ms |
| 3 | Auto Shift state | 1 byte | mask `0x1d`: bit 0 enabled, bit 2 excludes punctuation, bit 3 excludes digits, bit 4 excludes letters | 1 |
| 4 | Auto Shift hold time, only in compact Auto Shift profiles | 2 bytes | 1–1000 ms | 175 ms |
| 6 | One Shot timeout | 2 bytes | 0–30000 ms; 0 means no timeout | 0 |
| 22 | Caps Word ruleset | 1 byte | 0 = English, 1 = Russian | 0 |
| 7 | Tap/hold decision time | 2 bytes | 1–1000 ms | 200 ms |
| 18 | Tap-code delay | 2 bytes | 0–100 ms | 0 ms |
| 19 | Caps Lock tap delay | 2 bytes | 0–100 ms | 80 ms |

The tap-code and Caps Lock delays apply to the `tap_code()` and
`tap_code16()` helpers. These include send-string characters and legacy
`SS_TAP_CODE` macro actions. Compact Mod-Tap, Layer-Tap, Space Cadet and Tap
Dance gestures dispatch records directly and do not use these delays. Extended
Vial macro down/up actions also use their own explicit timing.

QSID 3 uses the default value `1`; its mask sets enabled, excludes punctuation,
excludes digits and excludes letters with bits 0, 2, 3 and 4 respectively.
Changing QSID 3, 6 or 22 takes effect immediately after a successful setting
operation, including an explicit write of the unchanged value. Only unchanged
requests avoid a flash write and input cancellation. Their saved values persist across restart. Other
settings are applied after a successful save. Changing an actual setting first
releases active outputs and cancels pending input. Held physical keys stay
blocked until released. A storage error stops writes; the new runtime value is
not applied. No automatic retry or rollback follows a failure.

## Record and protocol

The board uses its own typed record, without enabling upstream `QMK_SETTINGS`.
Combo storage remains at `0x658`. The 24-byte record at `0x6a8..0x6bf` fits
within one 64-byte journal page and uses the checked NVM transaction path.

| Bytes | Meaning |
| --- | --- |
| 0–1 | ASCII `QS` |
| 2 | Record version, 2 |
| 3 | Payload length, 15 |
| 4 | Capabilities, `0x7f` |
| 5 | Grave Escape flags |
| 6–7 | Combo time |
| 8–9 | Tap/hold time |
| 10–11 | Tap-code delay |
| 12–13 | Caps Lock delay |
| 14–15 | Auto Shift time; stored even in profiles that do not expose QSID 4 |
| 16 | Auto Shift flags (same bit mask as QSID 3) |
| 17 | Caps Word ruleset (`0` English, `1` Russian) |
| 18–19 | One Shot timeout |
| 20–21 | Reserved, zero |
| 22–23 | CRC16-CCITT, polynomial `0x1021`, initial value `0xffff`, over bytes 0–21 |

All words, including CRC, use little-endian byte order. Record validation checks
the entire header, ranges, reserved bytes and CRC before loading any value.
An all-zero or erased record selects defaults without writing. Other invalid
records select defaults and latch a schema fault, which blocks further writes.
Valid version-1 records are read and upgraded in RAM without a startup write. The first changed setting commits version 2. Version 1 stores the original fields and has zero in bytes 16–21.

Query returns supported 16-bit QSIDs greater than the requested ID, followed by
`0xffff` padding. Get and Set return zero for success and `-1` for unsupported
IDs, insufficient buffer capacity or rejected values. Set also rejects storage
faults. Vial packets contain trailing padding, so capacity may exceed the typed
value width. QSID 3 and QSID 4 are exposed only with `AK820_COMPACT_AUTOSHIFT`; QSID 6 requires One Shot.
QSID 22 is present in every profile that enables QMK Settings. Caps Word
activation gestures are available in all ten profiles. The `0x7e00`, `0x7e01`
and `0x7e02` selectors choose English, choose Russian or toggle the session
ruleset; they do not change the computer's keyboard layout.

The host test `qmk-8051-ak820/util/test_ak820_settings.c` checks defaults,
validation, persistence, cancellation, unchanged-value writes and storage failure.
It models the storage API; it does not prove flash power-loss recovery or physical
keyboard timing. Exact-image stack, interrupt and device qualification are
separate requirements.
