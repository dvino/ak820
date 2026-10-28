# Main profile, local offline qualification (2026-10-28)

Build: `qmk-8051-ak820/.build/headroom-retry-main`. Source identity records
commit `a53ca97b8e748c4b88b89582f26e38032714d1b9`, dirty `true`, and source
manifest SHA-256 `3524de3b932bb137ddf2899dcd8923b5ad672c0d7db994175e4bee90d40720c2`.
It is therefore not a clean build of that commit.
The physical-window build contains 40,330 occupied CODE bytes: 38,447 in
0x3027–0xc6ff (38,617-byte window; 170 bytes unoccupied) and 1,883 in
0x28a0–0x2fff (1,888-byte window; 5 bytes unoccupied). These are occupancy
counts, not a guarantee that additional code can be placed or linked.
Ordinary external RAM is 2,854 of 3,008 bytes (154 free). The linker `.mem`
ROM count includes other linker bookkeeping; CODE counts above come from the
build report.

`configuration-report.json` records `offline_tests_passed: true` and
`whole_program_stack_qualified: true`. `qualification.json` contains 36
suites and 356 unit tests, none skipped. `profile-tests/results.json` records
36 profile-specific suites. The build container exited 0. The 161/182-byte
stack bound leaves 21 bytes under the report's assumptions: CRT entry with
interrupts disabled, valid memory accesses, and the SDCC bank-0 ABI. OEM
wrappers are a pinned reference, not a check of a connected device. See
`configuration-report.json` runtime analysis for all limits. Results are for
this linked image and offline CPU/host checks; no physical-device validation or
flashing was performed. Bootstrap and other profiles do not qualify this image.
