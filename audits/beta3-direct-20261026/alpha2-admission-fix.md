# Alpha2 transition admission correction

The retained alpha2 image has IHX SHA256
`f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
`tools/installer/settings_backup.py::_legacy_images` gives this image no
Combo version. `plan_restore` returns `combo_entries=None` for its backup.
The restore loop emits no Combo writes and preserves the target's Combo slots.
The former release checker required eight writes for this source and therefore
rejected the generated zero-write preflight.

The corrected checker admits only this exact historical source, the reviewed
target IHX and the selected target profile. The source must also occur in the
transition's source-image list. It requires 498 keys, 12 encoder entries and
zero emitted Combo writes as integer counts, plus a passed offline preflight
with zero device commands. The required `combo_restore` object records
`source_combos_version=null`, `plan_combo_entries=null` and
`target_policy="preserve-existing"`. This is evidence of preservation; it does
not grant an exception to a Combo-capable source.

The checker reads the referenced JSON after checking its SHA256. Its complete
content must match the embedded transition preflight after excluding only
`result_path` and `result_sha256`. Matching file bytes alone no longer admit
malformed or unrelated content. Duplicate JSON fields remain rejected.

Bounded verification: `python tools/test_release_safety.py` passed 31 tests.
The cases include positive legacy preservation; wrong source, target, profile
and source case; a missing source-list entry; eight writes; boolean and wrong
counts; missing or contradictory preservation evidence; wrapper disagreement;
and malformed JSON with a matching digest. Existing stack, IRQ, source,
artifact, transition-log and policy contract tests also passed.

Changed checker SHA256:
`f941074b58f04454e3beb395b9db750dfd097cd375e9fbb479ddc7896493b4e9`
(224 lines). Changed test SHA256:
`db2a20023284e356da5c7a58bbf638a015e99598a15e1ee2b56610da49814531`
(308 lines). These are source identities, not firmware qualification.

The checker is part of the frozen test source snapshot. Earlier qualification
does not cover this changed source. Regenerated transition evidence, a fresh
frozen-test record and independent review are required before committing.
No firmware, settings restore implementation, catalog or build artifact was
changed by this correction. No full build, full regression or device operation
was performed for this bounded check. Physical behavior remains untested.
