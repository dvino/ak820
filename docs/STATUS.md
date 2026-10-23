Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-24. Development source implements compact Mod-Tap/Layer-Tap.
Its latest build uses pinned SDCC 4.6.0 and has 24 trailing CODE bytes. Complete
qualification is being rerun after a Grave Escape ownership correction. The
checked-in installer bundle still contains the earlier firmware. CI builds its
own firmware and passes that fresh bundle to Windows packaging.
No firmware or settings writes were performed in this work.

## Retained release and pointer-only comparison

| Measurement | Retained release control | Reproduced candidate |
| --- | ---: | ---: |
| Occupied CODE bytes | 38,100 | 38,069 |
| Main / low CODE bytes | 36,292 / 1,808 | 36,261 / 1,808 |
| XRAM bytes | 2,067 | 2,066 |
| Initial SP / allocated stack capacity | 0x62 / 157 bytes | 0x62 / 157 bytes |

In this retained earlier comparison, the source change affected only the
private journal-header validator's XDATA pointer. Journal format, CRC, replay order, six layers and sixteen macros with
8192 shared bytes are unchanged. The candidate saves 31 CODE bytes and one
XRAM byte. The tested helper uses four stack bytes instead of six; this is not
a bound for every runtime path or interrupt overlap. The delay-expression
probe added three CODE bytes and was rejected. See the
[bounded probe report](../audits/rc6/bounded-optimization-20261023.md) and
[memory guide](RESOURCE-BUDGET.md).

Exact application IHX hashes:

- Checked-in release and installed-image profile: `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
- Reproduced candidate and CI target: `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`.

The candidate has not been installed. Its IHX is an application, not a full
flashable ROM. Local OEM recovery inputs are still needed to construct the
complete update. The reviewed settings models now support same-image restore
and the explicit legacy-to-candidate transition. Downgrades and unknown images
are rejected. That transition has not been tested on a keyboard.

## Current verification

The compact Mod-Tap/Layer-Tap implementation remains a development candidate.
After the Grave Escape correction, its build fits with 24 trailing bytes before
`0xc700`: 40,399 populated CODE bytes, XRAM 2,512, stack allocation capacity 157.
Its IHX is `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`. No candidate update
has been installed. The latest corrected image passed all 65 tap-hold cases and the separate
33 feature, 10 unlock and 16 Tri Layer cases. The first run
failed because its cancellation fixture assumed the wrong reset branch; that
fixture-only error was independently reviewed and corrected. Cancellation is
tested through a scoped simulator hook, not EEPROM/reset execution. The first complete 26-suite run also found a real Grave Escape raw-owner/cache
fault and outdated layer/weak-mod fixture assumptions. The source and fixtures
were corrected and independently reviewed. The [fresh 26-suite qualification](../audits/rc6/compact-tapping-qualification-20261024/qualification.json)
passed with 258 unit tests, no skips and unchanged IHX/MAP hashes. The earlier
failed report is retained. [Independent offline review](../audits/rc6/compact-tapping-final-integration-review-20261024.md)
passed. Fresh bundle assembly and dev CI remain pending. The 23-suite evidence below applies to the
retained earlier image, not this candidate.

The [clean local run](../audits/rc6/ci-integration-20261023/qualification.json)
passed all **23 suites**, including **257 unit tests with zero skips**, eight
host C suites and six linked CPU suites. IHX and MAP hashes stayed unchanged.
A separate discovery run passed all 109 host-tool unit tests; compiler version
selection passed three tests. These counts overlap with the combined runner
and are not added into a distinct-test total.

Syntax checks passed for 208 tracked Python files and one shell file.
Actionlint passed. Ruff found no errors under the selected correctness rules
for duplicate dictionary keys, tuple assertions and undefined names. Existing
escape-sequence warnings in upstream QMK Python files are recorded separately.
The local sanitizer run uses `ASAN_OPTIONS=detect_leaks=0`: address and undefined
behavior checks ran where enabled, but memory leaks were not checked locally.

The initial import run failed a 20-second GUI test deadline and lacked LUFA.
The GUI model now runs inside a child process with bounded termination and
joined cleanup. A later run during edits is retained as a failure; the clean
run above supersedes it. The exact required suite identities and CPU/IAP
options are checked before CI can authorize a bundle.

A separate [read-only device run](../audits/rc6/ci-integration-20261023/readonly-summary.json)
passed for the legacy firmware: 498 key assignments, 12 encoder assignments,
16 macros through the 8192-byte view and 82 RGB descriptors were checked.
Settings writes, durable RGB save and physical behavior were skipped.
The Linux hidraw backend and udev access worked. The source setup now builds
that backend explicitly without reusing a wheel built for another backend.

The [evidence manifest](../audits/rc6/ci-integration-20261023/evidence-manifest.json)
binds the retained local report and console logs. Full simulator transcripts
for this run and private device captures remain outside Git. Earlier qualification with
247 unit tests is retained in the
[previous run](../audits/rc6/roadmap-qualification-20261023/final/report.json);
it describes the pre-CI source snapshot, not the current host implementation.

## CI, packaging and issue forms

Every branch push and pull request runs checks and builds. `dev` and untagged
`main` produce artifacts. A new SemVer tag on a commit in `main` publishes only
after Linux and Windows pass; prerelease tags are marked accordingly. Windows
packaging consumes the firmware built by that Linux job. The publish gate
checks that both packaged applications contain that same fresh bundle.
See [CI and releases](CI.md) for the exact flow and review policy.

Local policy and packing checks use the exact candidate and verified private
OEM references. Only hashes and sanitized packing results enter Git; CI reuses
that checked result for the reproduced program. A machine build attestation
is distinct from independent review and never authorizes device access.

The current source approval binds 21 host files. The checked-in legacy release
manifest SHA256 is `de139a02195c777bda20994e85ebae207f98015723e80a415cdfcca7d36cb2ac`.
Its [review record](../releases/rc6/reviews/independent-review.md) keeps the old
firmware and the updated host code separate. Source `verify` passed without
HID load or USB access. [GitHub run 40007909621](https://github.com/dvino/ak820/actions/runs/40007909621)
passed on commit `4f55c59a7307c80f22888dd043b508cd7bef0416`: Linux built
the firmware and passed all checks; Windows built both applications with that
fresh bundle and passed packaging, CLI and Tk startup checks. Three artifacts
were uploaded. Publication was skipped as expected for an untagged `dev` push.
Visible dialogs and device behavior were not tested. The saved job logs and
artifact metadata are in [the evidence directory](../audits/rc6/ci-integration-20261023/github-run.json).

Three GitHub Issue Forms are defined for bugs, features and flashing/recovery.
YAML and documentation checks passed, and independent review closed the issue
chooser link correction. The forms exclude V2, Pro and Max and request sanitized
logs rather than OEM ROM or private backups. The forms are committed separately
on `main`; remote commit `15ca3bce33866d5d8d7828f4f23338180ac94dad` was verified.

## Retained device evidence and remaining work

Earlier installation evidence records payload SHA256
`a1b8beec9a2a675c955bac946339e31f1823e17cdfb60f4755796e550530c711` and full ROM
SHA256 `56b2de776924c48bda6d08a2604edc8ab94f24e5ec7365f7b584c0fe7dd70fc5`.
It verifies CODE, manifest, protected regions, initial NVM and a clean store
after restart. Physical typing was confirmed separately. It does not prove
this new host transition or cold power-loss persistence.

Live settings writes, macro upload, saved RGB, physical encoder/lighting and
power-loss acceptance remain open. C/W electrical mapping still needs evidence
from OEM firmware before implementation. Persistent Direct palette work is
cancelled; the Windows language helper remains unfinished. Caps remapping and language-key
implementation are deferred by the current request. [Roadmap](ROADMAP.md)
keeps those tasks and the remaining bounded optimization research separate.

Update, 2026-10-23: [Node.js 24 run 40009482255](https://github.com/dvino/ak820/actions/runs/40009482255) passed Linux and Windows; publication was skipped. Neither job log contains the Node.js 20 deprecation warning. Persistent Direct palette development was cancelled and removed from this branch. The stable schema remains `0x082002`; installer offline verification passes. The cancelled prototype is preserved separately as an unapproved experiment. Mod-Tap / Layer-Tap is the next selected input feature; Caps remains unchanged.
