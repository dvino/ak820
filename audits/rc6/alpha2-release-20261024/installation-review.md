# Alpha.2 installation review

2026-10-24. Result: approved for the installation evidence and documentation
commit. No findings remain. The review was independent of the installation
report and status edits. No device commands, firmware changes or builds were
performed during this review.

The recorded operation followed explicit approval to flash. The update log
contains one bootloader transition, one erase/flash, one restart and successful
completion. The flash receipt agrees. Separate fresh physical confirmations
are recorded for update and settings restoration. Restoration reports two
typed writes and successful readback; no retry is recorded.

The private before and final backup manifests, every listed file size and
SHA256, and both event/receipt hashes match `device-result.json`. The downloaded
release IHX matches the installed IHX hash. Final CODE bytes and the complete
64-byte application manifest match the planned permanent payload. The CODE
SHA256 is `d787703f62f96d7204bf25c566eac39f66b8c8c3f711ce152d7ff1eded9716da`.
The final full-ROM and NVM hashes also match the report.

Before and final saved NVM are byte-identical. The supported settings agree:
498 key assignments, 12 encoder assignments, 16 macro slots and eight saved RGB
bytes. The final backup includes eight empty Combo entries. Its 5,647 trace
rows contain no recorded error; every raw request passes the protocol
validator with writes disabled, including the Combo getters.

The English and Russian STATUS sections agree with this evidence. General
operation was reported as apparently working. This does not establish individual
physical key or encoder behavior, Combo timing, nonempty Combo writes,
power-cycle retention, power-loss behavior, or manual Windows/Linux GUI
acceptance. The report and both translations retain these limits. Readback and
successful restoration do not prove a write test of every setting slot.

Settings, raw device data and recovery files remain private. The public report
contains hashes and counts without personal paths or raw settings/OEM bytes.
