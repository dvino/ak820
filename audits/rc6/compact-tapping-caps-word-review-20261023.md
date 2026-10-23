# Caps Word interaction review

Date: 2026-10-23. Scope: compact tap-hold interaction with Caps Word,
raw and owned weak modifier cleanup, actual event-pipeline host tests,
and the English and Russian TAP-HOLD documents and tap-hold contract.

Independent source review found that Caps Word previously removed its raw weak
Shift through an owned-modifier wrapper. That could consume another action's
Shift owner and leave raw Shift behind. The compact profile now removes the
raw Shift with `del_weak_mods` and sends the updated keyboard report; the generic
profile retains its previous path. The new negative control reproduces the
original fault and is rejected.

Pure Mod-Tap and Layer-Tap holds do not enter Caps Word's ordinary key pipeline.
This intentional behavior is now documented: Shift-MT preserves the mode,
Ctrl-MT ends it on the next ordinary press with Ctrl held, and LT alone does
not end it. Resolved taps enter the ordinary pipeline. Default Caps Lock
assignment remains unchanged.

The independent reviewer inspected timeout and interruption traces for Shift-MT,
Ctrl-MT and LT, short taps, report modifier bytes, layer lookup, mode state and
release cleanup. The independent Host C/UBSan run completed with exit zero,
`pass=true`, 156 eligible QMK traces passed, and all nine negative controls
rejected. Retained report: [host verification](compact-tapping-caps-word-host-20261023.json).

The safety finding is closed at source and host-test levels. The stale seven-item negative-control description was corrected to nine;
the list now includes the Caps Word cleanup and derived-mask controls.
This review does not approve final firmware size, linked CPU execution, USB
behavior or physical keyboard behavior.
