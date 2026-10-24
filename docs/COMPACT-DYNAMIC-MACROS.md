Русский перевод: [Динамические макросы](ru/COMPACT-DYNAMIC-MACROS.md).

# Compact Dynamic Macros

Record and replay two temporary keyboard sequences.

The curated `work` package includes two temporary recording slots. The older
`full-dynamic-macro` CLI profile remains available for reproducing previous builds.
Each slot stores up to 16 completed keyboard taps in RAM. Map `DM_REC1` or
`DM_REC2` to start recording; starting again replaces that slot. Press
`DM_RSTP` to stop, or `DM_PLY1` / `DM_PLY2` to stop and play a slot.

Recording captures ordinary keyboard usages from `0x04` through `0x7f` and the
effective modifiers for each key. A key is saved after its final release.
Unfinished keys are dropped when recording stops. Entries keep press order, but
playback sends consecutive taps with at least 10 ms between press/release
phases; original timing and held duration are not saved. At capacity, new key
presses are ignored until recording stops.

The slots are cleared when the keyboard restarts or loses power. They are not
stored in Vial macros or settings. Playback controls pressed while playback is
active are ignored.

Mouse, media and system keys, standalone modifiers, encoder output, Vial macro
output, generated Repeat/Alt Repeat, and synthetic Grave Escape or Space Cadet
outputs are not recorded. Layer and configuration actions are excluded. Nested
Vial macro key primitives pause playback. Physical modifiers combine with
recorded modifiers; a key already held by another input is skipped. Modifiers
are captured before the GUI output filter: a recorded Win/GUI modifier is
sent only while GUI output is enabled. Playback does not run Caps Word or
Auto Shift again.

This is a bounded development feature, not the full QMK Dynamic Macro engine.
It is not included in the published alpha.3 firmware. See [Build profiles](BUILD-PROFILES.md)
for profile limits and [Status](STATUS.md) for verification and release state.
