# Compact tap-hold settings profile: review input

## Scope

This preparation adds the compact tap-hold image to the installer's exact
settings-profile allowlist and extends the in-memory transition model to three
ordered images. It does not select or package a release, build firmware, or
change an installed keyboard.

The added profile is:

- IHX SHA256: `24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655`
- Permanent CODE SHA256: `cdd600ad232f4f7f0f744db082de16769dc915b18baf85fdc8e57f22dd39fe2b`
- NVM schema: `0x082002`
- UID, keycode set, and NVM capacities: unchanged from the two earlier profiles

The allowlist order is legacy `f1c4…` → pointer candidate `feac…` → compact
tap-hold candidate `24e9…`. The existing rank check permits same-image and
forward restores in that order and rejects downgrades. Unknown IHX/CODE pairs,
incorrect embedded manifest identity, and mismatching target snapshots remain
rejected by the existing checks. No provenance check or pre-write gate was
relaxed.

## Verification evidence

`python3 -m unittest tools.installer.test_settings_backup` passed: 23 tests,
including a three-profile transition matrix. The matrix covers all nine
source/target pairs: six same-image or forward pairs are accepted and all three
downgrades are rejected. The suite uses synthetic in-memory images; it is a
host model and does not prove CPU behavior, artifact contents, USB behavior,
durable storage, physical key timing, or installed firmware behavior.

The first and latest completed CPU final run passed 64 of 65 cases; the
`macro-cancel-stops-stream` result came from a `NO_RESET` fixture mismatch that
has since been diagnosed and corrected. Verification of the corrected fixture
is still pending, so CPU qualification is not claimed. Artifact qualification,
independent review, release approval, and device validation also remain
pending. No device writes or firmware operations were part of this preparation.

## Files for independent review

- `tools/installer/settings_backup.py`: exact image tuple added.
- `tools/installer/test_settings_backup.py`: ordered three-profile transition
  model and downgrade coverage.
- `docs/SETTINGS-BACKUP.md` and `docs/ru/SETTINGS-BACKUP.md`: profile hashes,
  transition order, behavior boundary, and qualification state.

The compact tap-hold behavior and Caps Word semantics are documented in
`docs/TAP-HOLD.md`; that file is outside this preparation's ownership and must
be checked for agreement during integration review.

## Replacement after the broader regression run

The earlier third-image pair above was preparation only and was never released.
The broader run found a Grave Escape raw-owner/cache interaction. After its
reviewed correction, the third profile was replaced, not extended, with:

- IHX: `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`.
- Permanent CODE prefix: `7e6b90f51a99ac335c0cb910fffc85f1d1705e7159a12de46f8e492807c36d40`.

The actual offline packing identities are in
`compact-tapping-grave-fixed-packing-20261023.json`. The superseded image is
not accepted by the current profile. Schema, capacities and forward-order
rules are unchanged. Fresh host/CPU and complete qualification remain separate
gates; no image is installed by this change.
