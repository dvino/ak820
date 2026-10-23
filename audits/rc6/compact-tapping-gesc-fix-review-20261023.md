# Grave Escape and fixture correction review

The source and fixture corrections are approved within the scope below. No
source blocker remains. This does not approve an image, policy, package,
installation or hardware operation. The previous full qualification failed;
a fresh complete result is still required for the corrected artifact.

The compact Grave Escape handler now distinguishes Repeat's retained synthetic
record using `get_repeat_key_count()`. Ordinary physical and encoder presses
update their source cache even though compact records already carry a keycode.
The corresponding release resolves to the originally selected basic action.
Repeat changes only its retained record and preserves the Repeat-position cache.
The synchronous Vial virtual position retains the static fallback because it
has no source cache slot. Generic handling remains unchanged.

Compact press/release uses `register_code` and `unregister_code`. These retain
owned basic-key counts, including overlaps and rollover. Raw `add_key` on press
could not be paired with the owned basic release path and caused a stuck Grave.
The compact handler omits the final duplicate report because these calls send
the report themselves. The compact-only Layer-Tap limit checks the already
computed high byte. This is equivalent under the existing pinned keycode ranges:
Mod-Tap is 0x20–0x3f and Layer-Tap is 0x40–0x4f; layers remain limited to 0–5.

The host fixture now includes the actual Grave Escape handler. Its cases cover
Shift release before physical, both encoder and virtual releases, distinct
physical/Repeat resolutions and same-resolved basic/GESC overlaps in both
release orders. Separate mutations reproduce the lost-cache and raw-owner
faults. An independent run completed successfully:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/run.py --negative-controls --output /tmp/ak820-gesc-independent-review-20261023.json
```

All eleven mutations were rejected; all 156 eligible retained-QMK traces
matched. All 43 source/header hashes in the report still matched the tree.
The retained report is `compact-tapping-gesc-fix-review-host-20261023.json`,
SHA256 `174b5a7d1a266ab7b4f97ec3b31aaf25f7b7a89b0c4d66eb8e30a29ba1c5e4ac`.
This is Host C/UBSan evidence with substituted callbacks, not linked 8051,
physical timing, USB or durable-storage evidence.

The older fixture changes also agree with the approved ownership contract.
Caps Word supplies raw `del_weak_mods` without a report side effect. Repeat
expectations keep owned modifiers until release and check the effective report
instead of the private raw weak-mod byte. Unlock and Tri Layer setup now calls
`layer_state_set` rather than writing effective output behind the ownership
model. Duplicate Lower holds retain separate owners, and the configured Lower
and Upper pair derives Adjust for ordinary MO holds too. These changes preserve
the stated checks while removing assumptions about private implementation
state. The tapping README describes the added handler, overlap cases and eleven
negative controls accurately. The older linked suites still need execution
against the new artifact.

No production source was edited by this review. No build or device operation
was performed. Prior image policy/packing records cannot qualify this changed
source and must be replaced only after the new checks complete.
