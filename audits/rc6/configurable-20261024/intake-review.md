# Archive acceptance, 2026-10-24

Accepted for offline development: `129c1c8..bcc337d` (four commits).
The `dev` branch was advanced through Git; the archive’s lost executable bits
were not imported.

Archive: `ak820-configurable-profiles-20261024-git.zip`.
SHA256: `bcfa631caca1db1ee6adcce2ed2608239bc02de7b15ff0f6445bc477be620ba3`.

## Independent review

A separate GPT-6.1 Sol reviewer inspected NVM page types and private state,
OSM ownership and cancellation, NKRO controls, profile selection, release
guards, documentation and verification evidence. No blocking finding remained.
All 178 indexed evidence files matched their sizes and SHA256 hashes.
Whitespace in generated evidence and CRLF-style test edits was nonblocking.
No source correction was required. Final review also matched the retained
local reports to the results below and approved this acceptance record with
no findings.

## Local checks

- Syntax: 226 Python files and one shell file passed.
- Documentation: 41 public documents, zero failures.
- Host tools: 133 tests passed.
- Installer: 132 tests passed.
- Fresh standard qualification: all 28 suites and 270 unit tests passed,
  zero skips; image identity remained unchanged. Its 13 profile gate tests passed.
- NKRO production handler host checks passed.
- One Shot host interactions, negative controls and 156 differential traces passed.
- A fresh standard build with the pinned SDCC 4.6.0 reproduced application
  SHA256 `004bf2cbda40f9c90ab92e0ee6b6a29bc2098e39d5ee8bc6d0da5df638f2565a`
  and 39,814 CODE bytes. The first attempt lacked LUFA; the next used the
  existing local dependency.

Retained local results: [configuration](intake/configuration-report.json),
[full qualification](intake/qualification.json),
[profile gates](intake/profile-tests.json),
[One Shot host](intake/one-shot-host.json) and
[installer tests](intake/installer-tests.txt). Original temporary paths in the
machine reports identify the execution location.

The 11 tap-hold negative controls intentionally ran faulty temporary binaries.
All were rejected. Their assertion failures produced Linux core-dump notices;
these were expected test failures, not failures of the unchanged source.

## Limits

Acceptance covers source and offline development. Optional profile binaries
were checked against retained evidence, not rebuilt during this acceptance.
No USB device was opened and no firmware was installed. Published and installed
alpha.2 evidence is unchanged. Runtime stack bounds, physical USB, interrupt
nesting, flash durability and installer transitions remain unqualified;
configured development profiles remain blocked from release packaging.
