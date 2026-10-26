# Profile composition test correction

The test-only change in `tools/test_configure_firmware.py` was reviewed independently of its author. The current ten-profile assertion adds only Auto Shift to main; its expected sets for the other nine profiles are unchanged. Exact set comparison also rejects an unintended GUI-lock addition to main.

A separate historical-main assertion checks that beta.2 lacks Auto Shift and GUI lock, remains accepted by the source reader, and is rejected as the current main configuration. This keeps the former source contract distinct from the new installation target.

No production code or gate was removed. The previous failure was a stale expected profile composition. An independent WSL Ubuntu run of `python3 tools/test_configure_firmware.py` passed all 40 tests; its log is `profile-test-correction-unit.log`. Native Windows execution cannot complete the symlink test without the required local privilege. Fresh all-profile qualification remains required. The failed run is retained, and its result is not relabelled as a pass. This review does not approve the pending regression results, release packages or device behavior.
