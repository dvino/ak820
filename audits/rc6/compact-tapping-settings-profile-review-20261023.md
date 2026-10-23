# Compact tap-hold settings profile review

## Result

The profile code has no identified runtime defect in this scope. Approval is limited to the settings profile and host transition preparation;
the persistent regression-test finding below is closed.
This review does not approve the firmware image, a release, CI selection, an
installer package or a device operation.

## Finding and closure

P2 — retain the complete ordered transition matrix in the reusable test.
`test_three_profile_order_allows_forward_path_and_rejects_each_downgrade`
checks first-to-third restore and third-to-earlier rejection. After the helper
changed from two profiles to three, the older candidate-to-legacy test also
became third-to-first. The suite therefore lost the explicit pointer-to-legacy
case and does not explicitly exercise pointer-to-compact. Add persistent
checks for all nine source/target pairs: six same-image or forward pairs must
pass, and all three backward pairs must fail with the downgrade reason.
Closure: the author replaced the partial case with
`test_three_profile_transition_matrix_all_nine_pairs`. Independent inspection
confirmed all nine pairs and the downgrade reason assertions. Independent
rerun with `python3 -m unittest tools.installer.test_settings_backup.SettingsTests.test_three_profile_transition_matrix_all_nine_pairs`
passed: one test in 0.800 s. The author also reported the complete 23-test
settings suite passing in 96.5 s. The finding is closed.

## Evidence

The production diff adds only the exact third IHX/CODE tuple. Its values agree
with `compact-tapping-offline-packing-20261023.json`: IHX
`24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655`
and permanent CODE prefix
`cdd600ad232f4f7f0f744db082de16769dc915b18baf85fdc8e57f22dd39fe2b`.
The schema remains `0x082002`. Ordered dictionary construction preserves the
legacy → pointer → compact ranking. Exact CODE and embedded manifest checks,
protected loader/tail checks, backup provenance, target identity checks and
pre-write failure gates are unchanged.

An independent in-memory check exported each of the three synthetic profiles
and ran `plan_restore` for all nine source/target pairs. It passed in 0.83 s:
all same-image/forward pairs passed and all backward pairs raised the downgrade
error. The exports sent no setters. This check supports the implementation but
was followed by the persistent regression correction described above. The author's
reported 23-test suite pass was reviewed as supplied evidence; it was not
repeated in full.

English and Russian settings documentation agree on exact identity, ordering,
unchanged settings capacity and the uninstalled candidate boundary. Their
Caps Word and macro descriptions refer to `TAP-HOLD.md` and do not contradict
its current semantics. The completed linked CPU result remains a failed
64-of-65 run. The fixture diagnosis does not establish a production defect or
a completed replacement qualification. CPU/artifact qualification and release
approval remain pending.

No build, physical USB access, device write, reset, bootloader transition,
flash or commit was performed during this review. Synthetic host results do
not prove physical timing, USB behavior, durable storage or installed behavior.

## Reviewed file identities

| File | SHA256 |
| --- | --- |
| `tools/installer/settings_backup.py` | `32207d2494398f2b5b28a111d9c4c99c6e05455d27e57d9825bf8ff78c37c8ee` |
| `tools/installer/test_settings_backup.py` | `405aa5684965092c00d307ffebf5aa22b5b950e2d3c397e6910f948819c562c8` |
| `docs/SETTINGS-BACKUP.md` | `8e83621c6933b60bb660ba1750b0b4fa2633f61b84b65c327cd6a20358ee3e3d` |
| `docs/ru/SETTINGS-BACKUP.md` | `16ed4896d15ebc53fe1f8f2b30f48196c3a16af2eed6a2fd27b0a7c25ae385c2` |
| `audits/rc6/compact-tapping-settings-profile-review-input-20261023.md` | `a7d217e7fd4f6ce7f29d047e35ea490250c49ada21dda605cd9c3de674cfe03d` |
