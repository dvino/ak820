# Combo alpha release review

## Decision

The final Combo source, host integration, documentation, packing receipt and
policy are approved for commit, CI reproduction and the next alpha release.
No blocking finding remains. Public CI and generated packages must still pass
the normal release validation gates. This approval does not authorize a live
update or claim physical acceptance. Installed firmware remains alpha.1.

The comparison starts at `4b83bb9` and includes imported `d361501` plus the
reviewed release integration. The initial findings below describe the imported
state; the closure section records the final result.
No build, USB access, reset, bootloader command, flash, commit or push was
performed during this review. Only this report and `ci/program-review.md` were
written.

## Evidence checked

The review covered the previous independent Combo review, the Combo contract,
STATUS, the stored final qualification, release policy and program review,
packing authorization, NVM migration, installer preparation/update, and settings
backup/restore code. The previous review approves development commits and a Git
archive; it explicitly excludes release and installer promotion.

The retained candidate IHX hashes to
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`.
The MAP hashes to
`a26c441c873cba85ca4c7c8a2ea659798b6d6d4eb87daa8840dc843e813307a9`.
The build report hashes to
`b69cc6fe6813264f61b193d9fe4ebe41e9e34277007bfd5a2384c5f296c4a583`.
The stored final qualification reports 28 passing suites, 258 unit tests and no
skips, with unchanged IHX/MAP. All 28 saved log hashes were independently
checked. The initial failed qualification remains separate from the final pass.
These are retained build and offline results, not device acceptance.

## Initial release findings

1. `ci/release-policy.json`, `ci/packing-receipt.json` and
   `ci/program-review.md` still authorize the earlier `45f28e80…` program.
   The policy source records also predate Combo and compiler changes. A fresh
   exact build and qualification must bind the final IHX, packing symbols,
   source files and host files. Offline packing must validate permanent/trial
   images and byte-equal native recovery with the private OEM inputs. Regenerate
   the receipt and policy, then obtain independent approval of the completed
   release work. Do not replace the earlier program hash without reviewing its
   replacement evidence. The generated public bundle must pass its ordinary
   manifest, approval, host and authorization gates.

2. `tools/installer/settings_backup.py` accepts four exact legacy images and
   does not accept the Combo candidate. It exports/restores no Combo section.
   Merely adding the candidate image would permit an apparently successful
   backup/restore which loses configured Combos. Add an exact reviewed profile
   and explicit per-image Combo capability. Export eight validated entries,
   validate them against saved NVM, and restore through bounded typed Vial
   commands with ACK, logical readback and complete NVM comparison. Stop on the
   first fault, timeout or mismatch; do not retry or recover automatically.

3. Define legacy migration before promoting the new profile. A backup without
   a Combo section must remain distinct from eight explicitly empty entries.
   The latter must intentionally clear all entries. State whether a missing
   legacy section leaves target entries unchanged or initializes only a fresh
   target; test that policy. The base schema `0x082002` alone cannot identify
   Combo capability. `migrate_vial_nvm()` currently copies same-schema bytes
   exactly, including the old gap, and is not an explicit Combo migration.
   Unsupported marker versions and malformed records need a documented,
   conservative preflight policy. No unrelated reserved NVM may be imported.

The confirmation-flow question is closed. The GUI rule requires the fresh
update hold and keeps the operation inside the installer; it does not prohibit
a separate guarded settings restoration hold. The existing two-hold flow is
retained. INSTALL now states both holds, exact-image display, one flash,
verification and cancellation before erase. No consent redesign is required.

## Required verification and documentation

Add model tests for legacy forward update, candidate export/restore with
nonempty entries, intentional clearing, missing legacy section, malformed or
unsupported records, exact-program rejection and failures during Combo writes.
Assert that no later command runs after a timeout, fault or bad readback. Check
both encoder directions remain covered by the complete regression suite.
Rerun affected installer/protocol tests and the complete offline qualification
against the final build. Review tests, reports, policy and host changes together.

README, INSTALL, STATUS, Combo documentation and their translations must agree
on the actual published artifact, backup compatibility, confirmation flow and
remaining limits. Keep the previous published alpha, the new built candidate
and installed firmware separate. An offline alpha package may retain
`hardware_validated: false`; it must not imply physical acceptance.

Fresh backup, exact image and recovery input checks, source rechecks before
loader entry, cancellation before erase and failure stops are already present
in the imported settings workflow. Preserve them through integration. Local
preparation must use saved private inputs without opening USB. Live read-only
diagnosis and firmware flashing remain separate scopes. No flash is authorized
by this review.

Physical Combo behavior, GUI interaction, physical unlock, USB timing,
interrupt overlap, changed-setting durability, cold-start retention and
power-loss recovery remain untested. Stored host/CPU passes do not close those
conditions.

## Host integration review

The added Combo protocol helpers match production Vial command layouts and
firmware validation. Writes require explicit write mode. Setters check ACK,
status, getter readback and the complete expected NVM including neighboring
bytes. The settings format derives the explicit eight-entry section from saved
NVM only for the exact Combo image. Legacy backups still omit it. A legacy
restore rejects a nonempty Combo target; an explicit empty candidate section
clears entries. Marker/version errors stop validation. Final restore compares
all expected NVM and logical settings. No runtime blocker was found in these
paths during this pass.

The CI qualification contract now requires both Combo host and linked CPU
suites, increasing its required suite count from 26 to 28. A missing suite
cannot be hidden by a report which otherwise says PASS. Final targeted failure
tests, complete qualification and release bindings remain required before
approval.

The requested restore-level failure test now supplies two differing entries
and injects a timeout, bad ACK, storage fault, getter mismatch or neighboring
byte corruption. Each case stops after the first Combo setter and records no
request after the terminal failure. An independent rerun passed all five Combo
settings tests, eleven protocol tests and eleven authorization tests. A
redundant full settings rerun was deliberately interrupted to avoid contention;
it is not counted as a pass or a failure.

All 622 final policy source records and 21 host records matched their current
file sizes and SHA256 hashes. The receipt hash matches the policy. Policy SHA256
is `223953489da71bcbe0690e91ca9f8577bcb465e1f0978c48c42e5a8d93f9eb3f`.
All nine retained legacy bundle records and its installer approval also match.
The saved production profile check accepts candidate IHX `a64dc561…` and packed
CODE `d787703f62f96d7204bf25c566eac39f66b8c8c3f711ce152d7ff1eded9716da`.
The packing report records permanent/trial images of 51,136 bytes and byte-equal
native recovery, with no USB opened. The fresh application IHX reproduces the
retained candidate; its MAP is allowed to differ in build-local paths while
canonical packing symbols remain unchanged.

The fresh build's 470 source/toolchain records and 79 artifact records were
independently checked without mismatch. Fresh MAP SHA256 is
`bae10d8b083cd98713af28203f422528b3a691751f64308eabab031918093862`;
canonical packing symbols hash to
`7dcabc5f511cb17eae298bc53faf7da5cd8a34b627123e42089cda520cf93c74`.
The English and Russian settings guides now list the fifth exact profile,
eight-entry section and legacy migration policy. This closes the missing
settings-guide finding.

Two retained-backup preflights are recorded separately. The first validates a
legacy `f1c4347e…` snapshot. The second validates a retained alpha.1
`45f28e80…` snapshot from before settings restoration. Both produce an allowed
forward plan into fresh candidate defaults without a Combo section. Neither is
a fresh current-device backup or proof that live settings are unchanged.

## Final finding closure and approval

All initial findings are closed. The final policy binds 623 source records,
21 host records and the regenerated packing receipt. Every record was rechecked
against current bytes. Final policy SHA256 is
`d02e7114fdd9f4b3ecf4bc24923936d121575c9832ec2e570f8b38b4fd7d2e05`;
it replaces the earlier integration policy hash recorded above. The independent
machine-readable approval is in `ci/program-review.md`.

Final qualification passed all 28 required suites, 265 unit tests and zero
skips with unchanged fresh IHX/MAP and zero physical device commands. The
complete qualification contract and all 28 saved log hashes were independently
verified. Report SHA256 is
`c5f7b57572aab136a81c172d7357d8aa0bf6b936f44687b8e6cb6e960fc50027`.
The five extra-verification logs were also checked against their recorded
sizes and hashes. They record 111 tool tests, eleven authorization tests,
three compiler tests, 10,944 NVM power-cut model cases and 25,088 macro upload
power-cut model cases. Those power-cut checks use ASan/UBSan with LeakSanitizer
disabled and remain host models.

The final workflow publishes `ci/release-notes.md` through `--notes-file`.
The bilingual notes contain only the new Combo feature and backup behavior.
The new English/Russian AGENTS rule matches the requested audience-focused
documentation policy. User guides cover behavior and actions; STATUS retains
validation and installed-state evidence. The settings guides list the fifth
profile and explicit migration contract. The two physical confirmations remain
inside the installer as reviewed above.

The application build, offline packing and settings profile agree. The final
review therefore approves the completed offline release work for commit and
release CI. Public CI/package acceptance and all stated physical conditions
remain separate. No hardware flashing permission follows from this result.

## Linux release scope review

The added standalone Linux x86_64 installer, native CI job, publication checks,
state directory handling and English/Russian installation guides are approved
for commit and CI. Native Ubuntu 22.04 packaging and smoke must pass before
publication. The final policy SHA256 is
`e4ae796fe635b87c4a2375eeab73c5b6ebff88c98eef8b8a3d9fc3e9099faba1`;
it replaces earlier policy hashes in this report. All 627 source records,
21 host records, packing receipt and retained legacy bundle/approval were
independently rechecked against final bytes.

Two blocking findings were closed before approval. The permission rule lookup
used the frozen module's virtual `__file__` rather than the collected rule;
it now uses `ROOT/tools/installer/70-ak820.rules`. Settings preparation similarly
tried to hash virtual module paths; it now pins the explicit collected source
copies. Focused fixtures supply nonexistent virtual paths and mock all
permission subprocesses. Four runtime path tests and one frozen preparation
test passed independently. Nine Linux packaging tests also passed independently.

All six saved Linux integration log hashes and sizes were independently checked.
The full installer run passed 130 tests before the two path fixes; the final
focused tests cover those fixes. The saved tool run passed 120 tests. The full
final workflow run reports sixteen passing tests in retained session output.
Syntax checks cover 220 Python files and one shell file; actionlint passed.
No firmware changed, so the earlier 28-suite/265-test result remains firmware
qualification with its original host scope. CI reruns the full final suite.

The Linux builder retains the native glibc 2.35 guard; the local glibc 2.39 host
was not used to claim native package success. Archive fixtures verify executable
permissions, safe internal library links, approved inputs and failure stops.
The builder's real CI smoke requires frozen hidraw import, CLI help/verification
and Tk under Xvfb. Publication requires both native Windows and Linux jobs,
sidecar hashes and fresh firmware/approval agreement in both applications per
package. Native package success remains a publication prerequisite.

Installation guides match the exact archive and executable paths, checksum
commands and Linux permission command. The permanent release rule is recorded
in both AGENTS versions. Notes remain limited to user-visible changes. No
hardware access or installation followed from this review.
