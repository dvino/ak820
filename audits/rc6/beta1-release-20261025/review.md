# Independent work beta review

Date: 2026-10-25. Result: approved for commit and CI reproduction. Native package
acceptance and public publication remain pending. No device operation is approved.

The review covers the work installer safety/configuration gate, exact settings
identities and migration, host manifest closure, catalog promotion, publication
workflow, English/Russian instructions and retained verification evidence.
All 686 policy source records and 25 host records match their recorded bytes.
The canonical release gate, base logs and supplemental logs were checked against
the unchanged exact work image. This was not an independent build.

The current image passes 28 base suites, 291 unit tests without skips and 30
supplemental suites. An initial supplemental attempt stopped when two asset-tool
sources changed. Its complete logs and source snapshot were retained. The change
record confirms that firmware and base suite inputs did not change. All base
results were revalidated and the complete supplemental phase passed after the
source freeze. See [current qualification](current-work-qualification.json),
[the source-change record](supplemental-source-change.json) and
[the retained first attempt](initial-profile-attempt.tar.xz).

Independent reruns pass 52 settings tests, 24 safety-gate tests and eight asset
generator tests. The real retained-image safety validator passes with
99 foreground + two CRT entry + 61 interrupt bytes, 162 of 165 bytes available.
The reviewed policy is `af0a34e599519482749358533d01b4624ebd11724421df5dbd52f6691687f34e`.

The following findings were corrected and checked before approval:

- The acceptance record still described a data-only beta using alpha.3 installers.
  It now describes exact work installers and the eight candidate profiles.
- Installation guides used the original candidate ZIP name and included installed
  state. They now name `AK820-Beta1-Catalog.zip` and keep installed state in STATUS.
- Catalog promotion accepted local offline review without the full CI closure.
  It now requires CI reproduced authorization and checks current policy, source,
  safety witnesses and exact work identities. Promotion and hash closure tests pass.
- The publication asset glob included directories. An explicit list of ten catalog
  files replaces the glob. Both native installer jobs remain required.
- The bundle path check did not reject symlink ancestors. Component checks and
  resolved containment now protect every bundle, policy and witness file; two
  symlink regressions pass.
- A clean publication checkout lacks ignored LUFA source inputs. The workflow
  now installs the pinned, hash-checked dependency before policy closure checks.

No open code or documentation finding remains in this scope. Hardware behavior,
native package acceptance and public download checks remain separate. The
original nine-profile evidence is unchanged; the original candidate flags remain
historical measurements. Public release metadata promotes only exact work.

## Output closure

The source installer bundle was assembled with the authoritative offline builder
and validated private OEM references. Every copied manifest file under
`releases/rc6` matches the assembler output byte for byte. The installer's
`load_release(approved=True)` passes offline and binds the exact work IHX.
The source approval matches installer manifest SHA256
`f4e34ced4b5a0d748e5104fb1453d724c15ef32f03585c271d82d56c4182fdee`.
This checks source bundle consistency; native Windows/Linux acceptance remains
pending.

The successful current work evidence archive was independently read without
extraction. All 4,001 regular members match the per-file sizes and SHA256 hashes
in [the evidence index](current-evidence-index.json). Its size is 4,417,056 bytes
and SHA256 is
`37e029af016aded6ae1b2c85241ec968d0f490c83240dff699d5d88d6029f28f`.
It retains the exact image, compiler listings, base logs, final supplemental logs
and runtime proof. No device was opened or commanded during these checks.
