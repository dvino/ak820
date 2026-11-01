# Beta.5 offline settings review, 2026-11-01

The release evidence producer needs to model settings transitions before a
release policy exists. The public settings v3 profile-loading and restore-planning
gates and the device write gate remain closed. Shared offline computations do
not approve an image or authorize a device operation.

Independent code review found no defects in the separation or its production
call boundaries. A separate test review found missing v3-specific rejection
cases for keycodes, macros, Combos, RGB and core NVM, and no real planner
rejection in frozen-policy preflight. Those cases were added; follow-up review
confirmed the intended semantic errors and the unchanged-output boundary. The
preflight test substitutes synthetic profile reconstruction, so it is not
exact-image evidence. The reviewer also notes that planner errors may aggregate
multiple blockers.

Documentation review found an incorrect description of byte 17 and an ambiguous
historical beta.5 publication claim. Byte 17 was corrected to QSID 22; the
original 2026-10-29 release is distinguished from the current candidate. A
further review found that the release notes and guides implied v3 backup/export
was available. They now state that v3 export and migration remain blocked.
Independent follow-up reviews found no remaining issues in these corrections.

Verification on the changed source, using offline tests only:

- Installer suite: 249 tests passed.
- Evidence-output suite: 16 tests passed.
- Release-safety suite: 39 tests passed.

The installer tests include simulated device and loader interactions; their
output is not evidence of physical device operations. No hardware test, write,
reset or flash was performed. The earlier ten-image qualification used the
previous source snapshot and must be repeated against the final host sources.
Draft results, synthetic tests and this review do not approve a release.

For requalification with a read-only source checkout, two Mouse Keys tests now
place temporary build directories under `.build`. Independent review found that
the assertions and builder path checks remain intact. The focused suite passed
13 tests. For this run, `.build` must already exist, resolve beneath the
builder's source root and allow the qualification user to create and remove
entries; the source is mounted read-only. The review did not verify the mounts or the complete qualification
suite.
