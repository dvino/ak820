# Roadmap handoff acceptance, 2026-10-24

## Imported work

`ak820-roadmap-20261024-git.tar.gz` has SHA256
`59e6fbddfa01e51c1a411fc14b78ab3e531af5715edc77f11ad5441d7a2ead0c`.
The clean `dev` checkout advanced from `48ce5fa` to
`4f6fffb1779cae02bed0bd3e872e3cb26bbfc579` without conflicts. The archive's
Git checkout was clean. No firmware source was changed during acceptance.

An independent read-only check passed all 2,071 entries in
`roadmap-max-20261024/final/SHA256SUMS`. The archived
[final review](../roadmap-max-20261024/final-acceptance.md) approves eight
development profiles and their offline evidence, not release packaging.

## Documentation

The English and Russian README feature lists now link directly to their guides.
Configuration describes modifier One Shot, the three compact Space Cadet actions
and optional NKRO controls. The indexes expose these development functions.
The CI guide now names all eight profiles and links to the latest qualification.
The roadmap defines `full` and orders the remaining alpha.3 work.

All 41 public guides passed the offline path/translation-link checker.
Independent heading-fragment checks found no broken anchors. Syntax checks
passed for 231 tracked Python files and one shell file; existing upstream
Python escape warnings remain. The host tool suite passed 138 tests.

Independent documentation review found no actionable findings after checking
the feature descriptions against source, both languages, links and release
limits. Documentation approval does not approve an installer or firmware update.

The first local full-profile qualification records failure: 27 of 28 suites
pass, with 270 unit tests and zero skips, but the documentation checker ran
between adding the STATUS link and creating this report. Its log records the
temporarily missing `review.md`. The report now exists and the focused check
passes. The failed qualification and all 28 original suite logs are retained;
the failure is not counted as a complete qualification pass.

The complete base recheck on the same image passed all 28 suites and 270 unit
tests with zero skips. The nine supplemental full-profile suites also passed.
The production validators checked the complete base and supplemental contracts,
their source snapshots, logs and unchanged image identities. Runtime analysis
again leaves main and LED unresolved. Its nonzero result remains an unresolved
safety condition, not a passing runtime proof.

The original failed `configuration-report.json` remains unchanged. The separate
`acceptance-report.json` records the recheck through `validate_tests`,
`run_profile_tests` and `run_runtime_analysis` from the production configurator;
it does not grant release approval. [files.json](files.json) binds 308 retained
files by stored size and SHA256, with decompressed sizes and hashes for gzip
records. It includes both qualification results, original suite logs, recheck
reports and logs, exact application artifacts, tool tests and the expected
[package refusal](package-gate.json). Full intermediate object trees are omitted.

Final independent review verified all 308 stored and decompressed file records,
all 28 base and nine supplemental log bindings, report identities and the
English/Russian documentation. No actionable findings remain for this
acceptance commit. The original failure and unresolved runtime conditions
remain disclosed; this approval covers development acceptance only.

## Release decision

The local `full` build reproduces the archived application IHX hash
`45681603a105334214919be0b8c32fc4ea94e8fc9d5a2003e98d673809d15a78`:
40,018 CODE bytes, 2,630 XRAM bytes and 162 allocated stack bytes.
The checkout had documentation edits during this build; its report records
`dirty: true`. A byte-identical IHX is reproduction evidence, not new proof
of runtime stack use or device behavior.

The actual `configure_firmware.py package` command stops for all three required
conditions: no reviewed whole-program foreground stack bound, no combined
exact-image interrupt/nesting proof, and no approved installer/settings
transition for this feature identity. Main and LED remain unresolved; the
timer/USB callback bounds exclude OEM entry and nested interrupts. The VS11/OEM
priority and routing contract is not established by a generic CPU model.

No alpha.3 tag, public release or installer was produced. The published and
installed alpha.2 state is unchanged. No device was opened, reset or flashed.
The [next-release plan](../../../docs/ROADMAP.md#next-alpha-release) records
the work required before Windows/Linux packaging and publication.
