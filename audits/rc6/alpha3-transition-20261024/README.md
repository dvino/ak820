# Alpha3 settings transition

The installer settings profile binds FULL support to both the IHX SHA256 and reconstructed permanent CODE SHA256. Schema 0x082002 alone does not establish compatibility. Package approval remains a separate gate.

The reviewed image is IHX `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`, CODE `01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d`. The final `alpha3-release` build reproduces both identities. Changed firmware requires new pins and qualification.

FULL retains Combo version 1 and adds assignment support for NK_ON, NK_OFF, NK_TOGG, SC_LSPO, SC_RSPC and SC_SENT. OSM assignments remain supported. OSL, unsupported Space Cadet variants and unknown feature names remain blocked. The same rules apply to matrix, encoder and macro keycodes. Runtime NKRO mode and pending One Shot modifiers are volatile and are not restored.

Existing backup JSON remains valid: the recorded limitations are unchanged. A new volatile-state note appears in the restore plan. Forward image ordering, exact source ROM checks, fresh target backup, physical confirmations, cancellation before erase and stop-on-first-fault behavior remain unchanged.

The three new host model tests pass: optional keycode boundaries, matrix and both encoder directions roundtrip, and legacy-to-FULL planning with unknown-feature rejection. These checks use synthetic in-memory devices. No USB commands, firmware builds or device behavior tests were run for this change. The full settings backup suite passed 31 tests in 111.480 seconds; the workflow suite passed 16 tests in 73.092 seconds. Logs are stored beside this report. The revised alpha2 Combo migration assertion and the other two FULL tests passed again in 2.895 seconds. Independent transition review is complete with no blocking findings. The witness retains its original pre-review execution-stage label; final approval is recorded in the [release qualification](../alpha3-release-20261024/review.md).

The initial preflight used `.build/alpha3-full-guards`; the final `.build/alpha3-release` image has the same IHX and CODE identities. An offline preflight of the retained alpha2 backup passed for 498 matrix assignments, 12 encoder assignments and 8 Combos. The original backup stayed private and unchanged. `verify_transition.py` repeats this check from explicit local build, native ROM and backup paths. `alpha2-preflight.json` contains identities and counts, without raw ROM or settings. This checks backup validation and restore planning; it does not prove USB writes, physical key behavior or storage persistence.

The current candidate suite passed all 47 settings tests. `current-tests.log` records the result. `transition.json` binds that log, the source hashes and the real alpha2 preflight to the candidate image. Passing this witness does not approve a release or prove device behavior.
