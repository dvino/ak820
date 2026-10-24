# Alpha.2 published artifact review

## Current decision

The published firmware, Windows and Linux assets pass independent review.
No blocking artifact or documentation finding remains. Tag workflow
`40060505913` completed all four jobs, including publication. Native package
reports record successful smoke checks on Windows and Ubuntu 22.04. This
review performed no USB access, device command or firmware installation.

## Firmware CI bundle

The reviewed immutable download is from tag workflow `40060505913`, source
commit `4772c433057bde5c9ccc4f2f3f904f1dcb326c17`. The canonical installer
`load_release(approved=True)` gate passed against this bundle and current
reviewed host code. This checks approval, manifest/file hashes, program review,
attestation, qualification contract, pinned tools and exact program identity.

| Item | SHA256 |
| --- | --- |
| Installer manifest | `ed4f347ce4af7b421c76a2f8c7e83c6d9e1e8f075dc10c4e8f81f51b2e7d908a` |
| Build attestation | `cf204c1f476bf069407825d5d6c323591a409a1b08e40dd7e3fc399d686bec71` |
| Application IHX | `a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f` |
| MAP | `01a2be4967a50b7a6ed8d8be9b5e153475a12d517de6b66a42963bad16eac805` |
| Canonical packing symbols | `7dcabc5f511cb17eae298bc53faf7da5cd8a34b627123e42089cda520cf93c74` |

All 615 tracked policy source records were independently compared with bytes
at the attested Git commit. The remaining twelve records are external LUFA
headers; their hashes match the pinned local reference. All 627 records agree.
CI reproduces the reviewed application IHX and canonical packing symbols.
The changed MAP hash is build-local metadata rather than a program change.

The bundled qualification reports all 28 required suites passing, 270 unit
tests, zero skips, unchanged IHX/MAP and zero physical device commands.
`hardware_validated` remains false. The bundle does not include the underlying
CI log files, so this check validates the bound report and contract, not those
absent logs. The earlier local logs were checked separately in the integration
review. CI evidence does not establish electrical flash, physical keyboard
behavior, power-loss recovery or settings retention after cold start.

## CI documentation

The English and Russian CI guides were reviewed against the workflow. Both
correctly describe the Ubuntu 24.04 firmware job, native Windows packaging,
native Ubuntu 22.04 x86_64 packaging, three-job publication gate, checksum
sidecars, fresh firmware verification inside both applications per package,
and user-facing notes from the checked-in release notes. No blocking finding
remains in those documentation changes.

## Published assets

The six downloaded release assets match the published alpha.2 asset list.
Each archive's SHA256 matches its downloaded sidecar. The public firmware ZIP
contains bytes equal to the independently reviewed CI bundle above.

| Archive | Bytes | SHA256 |
| --- | ---: | --- |
| `firmware-bundle.zip` | 136270 | `2d60d9c29aaabd17bc714c3dff1799f5e114f0d9d426c0608924fa1e4f6ec7a1` |
| `AK820-Windows.zip` | 20670624 | `a639e70ba5c17158f0602c6d0d51cac0f27477b9ac0fe9b3380e0cfbcf4b280c` |
| `AK820-Linux-x86_64.tar.gz` | 46506581 | `3172fe11523ce09fb9a6c0c8ee2064394b1dec7049dd6e68c6e137d411e9feed` |

All 36 approved files in each of the four application folders were independently
compared with the exact CI firmware/approval files and reviewed host hashes.
Every comparison passed. Both package provenance files declare the same
approved and collected inputs. Linux archive paths are relative and contain
no parent traversal or special files. No links are present in this actual
archive. Both Linux application executables retain mode `0755`.

The Windows provenance records Python 3.12.10 and PyInstaller 6.16.0. Its native
CLI help, offline verification and Tk widget smoke passed. Linux provenance
records x86_64, glibc baseline 2.35, Python 3.12.15 and PyInstaller 6.16.0.
Its frozen hidraw import, CLI help, offline verification and Tk startup under
Xvfb passed. These are native CI checks from the shipped package reports;
local GUI smoke was not performed. No package smoke enumerated or opened USB.
Manual dialogs, accessibility, scaling and actual device behavior remain
outside these results.

The release metadata records a prerelease published on 2026-10-24 at
04:06:44 UTC. Its bilingual notes match `ci/release-notes.md` and contain only
user-visible changes and limits. Archive paths agree with the English and
Russian installation instructions. Published alpha.2 and installed firmware
remain separate states; this review does not establish installation.

## Final status and read-only preparation review

The final STATUS, Combo and CI guides in English and Russian are approved
for the documentation/evidence commit. STATUS now describes the current source,
published artifact, verification and installed firmware without mixing obsolete
candidate history into current claims. The Combo guide describes supported
keys, the strict 40 ms boundary, suppression/release behavior and backup rules;
implementation and test details are linked from the retained technical report.
CI documentation agrees with the actual four successful jobs and both native
package outputs. No source runtime change followed the reviewed release commit.

The downloaded Linux CLI passed local help, offline verification and its frozen
hidraw import check. Both extracted executable hashes were independently
compared with the native package provenance and matched. Local GUI startup was
not run; the GUI smoke result is the native CI Xvfb check. The offline smoke
report's zero physical-device-command count applies to that smoke only.

The separate live read-only backup was independently checked without exposing
its private settings. All backup file hashes match its manifest. Saved NVM is
byte-equal to the full ROM's NVM range; the base schema validates and derived
settings equal the saved settings document. CODE SHA256 is
`cc5af6cc86724103fbc3e2c1815bf7a2235edc0ed85a932fd3e993cd6b4f7931`,
binding installed alpha.1 IHX `45f28e80…`. It records 498 key assignments,
12 encoder assignments, six layers and sixteen macros with 8192-byte capacity.
The legacy Combo section is absent as expected. All 5,636 recorded raw protocol
requests pass the adapter's read-only allowlist; two additional feature/status
rows belong to liveness checks. No settings setter or firmware transition is
present in that backup scope.

The preflight reports agree on target IHX `a64dc561…`, packed CODE
`d787703f62f96d7204bf25c566eac39f66b8c8c3f711ce152d7ff1eded9716da`
and complete target payload
`003d02080708238b9b862c84f724f8083896e71819f84df30d9cac02f1828362`.
The reported forward restore plan uses fresh packed defaults and preserves the
legacy section distinction. These are offline preparation checks, not a flash
or post-update verification. The read-only report correctly records zero
settings writes and zero flashes while distinguishing actual read commands
from offline checks.

No blocking documentation or evidence finding remains. This addendum approves
only the current documentation/evidence commit. It does not approve or execute
a live update. Installed firmware remains alpha.1; an update still needs its
own fresh backup and explicit operation confirmation, with alternate input and
stable power prepared. Physical alpha.2 behavior and durable changed settings
remain untested.
