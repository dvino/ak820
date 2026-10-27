# Historical settings contract review

2026-10-26. Independent read-only review of the historical profile configuration changes in `ak820_profiles.py`, their settings-reader integration in `settings_backup.py`, and `test_catalog_settings.py`. No actionable findings remain within this scope.

The beta.2 profile compositions are finite and separate from `PROFILES`. Source validation accepts only an exact current configuration or an exact reconstructed beta.2 configuration. Arbitrary feature additions, unknown fields and altered keycode lists fail validation. Current catalog rows still use strict current validation. Historical rows cannot become transition targets.

Catalog parsing retains each typed image's validated configuration internally. `_profile_images`, `_check_getters` and restore QMK-setting selection use that configuration. The public settings identity retains its existing fields; the internal `_configuration` does not enter its canonical comparison. Source and target capability domains remain separate: source getters follow the source image, while restore checks and writable setting IDs follow the target image.

Old identities default to no Caps Word Combo action and no macro layer tap capability. Old MAIN excludes Auto Shift and GUI-lock keycodes and QSID 4 even when current MAIN gains both features. Three legacy pinned source identities retain their separate reader path.

Verification:

- `python -m unittest discover -s tools/installer -p test_catalog_settings.py -v`: 21 tests passed in 65.943 seconds.
- `python -m unittest discover -s tools/installer -p test_extension_backup.py -v`: 3 tests passed.
- The saved `historical-catalog.json` was parsed with its ten profiles moved to `historical_profiles`, no current rows or transition edges, and current MAIN temporarily extended in memory with `auto-shift` and `gui-lock`. All 13 images parsed, including three pinned legacy sources. Old MAIN retained QSID list `[1, 2, 7, 18, 19]`; keycodes `0x7009` and `0x7C13` were rejected; Combo actions remained empty and macro layer tap remained false.
- Attempting to parse the same old catalog as current rows under the changed MAIN composition failed strict configuration validation, as required.

The historical MAIN test also exercises source backup validation, forward restore planning and mocked source getters with the original QSID list. Poisoned historical configuration and an old configuration presented as a current row are rejected.

These results cover static inspection and host models. No firmware build, USB command, flash, device setting change or physical behavior check was performed. The helper reconstructs historical configuration metadata using the shared configuration formatter; later changes to that formatter or shared constants require another historical-reader review. This review grants no release or device-write approval.
