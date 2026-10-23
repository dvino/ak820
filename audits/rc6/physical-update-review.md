# Physical update review

Date: 2026-10-23. Independent source and offline host review. The reviewer did
not author the update backend or the RU/EN interface. No USB access, device
command, firmware build, reset or flash ran during this review.

The reviewed update starts with a fresh full ROM read and admits only the
pinned RC6 repair image, recovery backup and recorded fault snapshot. The
copied session is checked again before the loader transition and before erase.
It keeps the saved durable settings and clears the failed encoder probe's
pending journal. It does not replay the temporary encoder assignment.

After Update, FE08 locks Vial, FE05 confirms the lock, and FE06 starts a new
physical hold. FE07 must report unlocked, inactive and counter zero, followed
by a final FE05 check. Only then may one 0B request enter the loader. Neither a
typed word nor a separate Vial application participates in update consent.
The wire checks match the firmware's fixed Esc and left Control matrix cells.
An echoed 0B response is not treated as proof that the loader started.

The installer requires a unique supported loader interface and its identity
reply before erase. Cancellation is checked before each application mutation,
during the loader wait and immediately before erase. After erase begins, it
finishes checksum and restart rather than interrupting the write. Any timeout,
malformed reply, changed identity, storage failure or bad readback stops the
run without automatic retry, restore or recovery. The attempted mutations are
logged, including failures where the device may have accepted a command.

Success requires application startup progress, full code and protected-region
readback, stable settings and journal reads, no storage failure, and the exact
prepared durable settings. These host checks do not prove physical typing,
either encoder direction, durable writes after this update, power-loss
persistence or the physical controller's erase behavior.

The RU/EN interface selects Russian for Russian Windows UI language and English
otherwise. Language switching changes current instructions without sending a
USB command or restarting the operation. The image hash and restoration warning
remain visible during physical confirmation.

Review corrections: the initial remaining-hold display counted elapsed ticks
while saying they were remaining seconds. The author changed it to round up
the remaining firmware ticks and added 30/20/1/0 boundary checks. Review also
requested English translation of the backend's visible physical-consent block
and language switching for the logs-folder label.

All three findings are closed. Source inspection confirms the corrected
countdown, translated consent block with its unchanged SHA256, and translated
logs-folder label. The independent final installer run passed all 72 tests.
The build and packaging host run passed 17 tests. The firmware package suite
passed 64 tests with two skips. The reviewer also ran the GUI's offline
`--self-test` successfully; this constructs and destroys the window without USB.

Result: PASS for this bounded source and offline host review, with no open
blockers. The release review binds all 16 current runtime host files, including
the new i18n module. The real `tools/build_release_bundle.validate_review`
accepted the required `passed` status, all three frozen build hashes and all
16 host file hashes together. This permits assembly and offline checking of
the standalone release. It does not authorize a live update.

INSTALL and STATUS describe the integrated physical hold and RU/EN behavior,
keep standalone assembly pending, and distinguish readback from physical
typing and power-cycle checks. The earlier typed-confirmation GUI reviews are
superseded. Root's automatic runner check still sees the old published local
host manifest until the new 16-file release is assembled; it must be rerun
after promotion. That stale-manifest result is not a completed PASS.
