# Compact input options — 2026-10-24

Both options are disabled in the standard build. The existing six layers,
16 Vial macros, eight Combos, NKRO reporting and Grave Escape remain enabled.

## NKRO control

`AK820_NKRO_CONTROL=yes` adds the three existing NKRO Magic keycodes without
including the Magic engine. The control clears the old report and cancels input
owners before changing the report mode. The mode is temporary. No saved-data
format changes or NVM writes are added. Restart uses the saved/default NKRO bit
in the existing `EECONFIG_KEYMAP` word at NVM offset 4. Typed settings backup
captures this word as raw evidence but does not restore it; temporary mode is
therefore explicitly outside backup scope.

The host check compiles the actual handler and checks inert releases, old-mode
cleanup ordering, unrelated configuration bits and absence of persistence calls.
The complete linked CPU checks cover both reports, the three controls, held
keys, modifiers and a resolved tap-hold owner. Both scenarios passed against
the measured final NKRO IHX listed in `measurements.json`.
This build includes the separately owned stable size-savings patch.

## One Shot modifiers

`AK820_COMPACT_ONESHOT=yes` adds OSM only. A released OSM arms a modifier set
for the next accepted non-control key. A held OSM works as an ordinary modifier;
using another key while held prevents arming on release. Matching physical
modifier owners survive One Shot consumption. Multiple queued modifier masks
combine. One consumed key can remain down; until its release, a new OSM acts as
a held modifier and does not arm another One Shot. This bounded fallback avoids
an extra per-key ownership table.

Physical matrix and encoder sources are supported. Repeat's synthetic recursion
uses its existing retained modifier state. Vial-injected or macro OSM actions
are outside this initial scope. OSL, timeout, locking, tap-toggle and upstream
One Shot settings are not implemented. Clear/unlock cancels queued and consumed
state along with existing input owners. There is no saved One Shot state.

The production host fixture checks all modifier encodings, held chords,
matching physical owners, rolled keys, busy fallback, cancellation, Repeat,
Caps Word and Combo output. The retained baseline and optional OSM runs each
also pass 156 differential tap-hold traces. The production-bounded OSM build passes both CODE windows: 40,479 total CODE
bytes, 38,607 main bytes and 1,872 low bytes, highest address `0xc6fa`. XRAM
uses 2,622 of 3,072 bytes. Allocated stack capacity remains 160 bytes; the
13 linked scenarios reach at most 44 bytes, which is not a whole-firmware runtime
allowance. The linked checks include actual Combo output and Caps Word owners.

## Rejected experiment

The earlier complete OSM+OSL engine passed host interaction checks but used
41,433 linked CODE bytes with highest address `0xcae7`. The probe intentionally
used `--code-end 0xd800` to obtain a measurement; it exceeds the production
window and is not an approved image. Its patch and reports remain here as
experimental evidence. It is absent from active source.

No device was opened, changed, reset or flashed. No physical behavior or
interrupt timing is established by these host and generic C52 checks.

## Combination limit

The complete NKRO plus OSM build exceeds the main window at
`0xc700..0xc792` and must be rejected. Costs are not additive. The separate
NKRO and OSM production builds are recorded in `measurements.json`; both also
include the stable size-savings patch and expanded foreground outlining. The
OSM post and cancel helpers occupy the low CODE area in a separate source file.
A mid-file codeseg pragma was ineffective and is not used.

## Review follow-up

Additional host assertions pass for overlapping queued masks, modifier and layer
controls, MT/LT taps and holds, and cancellation while OSM is held or consumed.
The tap checks verify that the shifted basic key was emitted. Two further linked
scenarios pass for actual Vial unlock while OSM is held and while its consuming
key is down. The NKRO handler is static again. A complete rebuild is byte-identical
to the prior final NKRO image and still has 159 allocated stack bytes; static
linkage did not recover a byte in this build context. The linked NKRO scenarios
pass again. OSM production code is unchanged by this follow-up.

## Integration identity

These are pre-integration measurements. The final integrated source restores the
private tapping source helper when One Shot is disabled. Final profile hashes,
resource totals and full suite outcomes will be recorded after the final runs in
[qualification.md](../qualification.md). The One Shot helper remains externally
visible only in the One Shot profile.
