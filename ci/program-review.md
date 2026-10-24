# Independent Combo program review — 2026-10-24

The exact Combo program, settings backup/restore changes, release workflow,
packing receipt and final policy are approved for CI reproduction and the next
alpha release. This approval covers offline release preparation. Public CI and
its generated packages must still pass their normal validation gates. It grants
no permission to flash and does not establish a new installed image.

The implementation, policy, packing receipt and qualification were authored
separately from this review. All 627 policy source records and 21 host records
were checked against current sizes and SHA256 hashes. Policy SHA256 is
`e4ae796fe635b87c4a2375eeab73c5b6ebff88c98eef8b8a3d9fc3e9099faba1`.
The fresh build reproduces IHX
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`
and canonical packing symbols
`7dcabc5f511cb17eae298bc53faf7da5cd8a34b627123e42089cda520cf93c74`.
All 470 build source/toolchain records and 79 artifact records were checked.
The nine retained legacy bundle records and installer approval also match;
that bundle retains its earlier firmware.

Firmware qualification before the later Linux host integration passed all 28 required suites, 265 unit tests and zero
skips with unchanged IHX/MAP and zero physical device commands. Its full suite
contract and all 28 saved log hashes were independently checked. Qualification
SHA256 is `c5f7b57572aab136a81c172d7357d8aa0bf6b936f44687b8e6cb6e960fc50027`.
An independent targeted rerun passed five Combo settings tests, eleven protocol
tests and eleven CI authorization tests. Extra retained logs were hash-checked:
111 tool tests, eleven authorization tests, three compiler tests, 10,944 NVM
power-cut model cases and 25,088 macro upload power-cut model cases passed.
ASan and UBSan were enabled for the power-cut models; LeakSanitizer was disabled.
These models do not establish electrical flash behavior.

The fifth exact settings profile binds the candidate's packed CODE. Candidate
backups carry all eight Combo entries. Legacy backups omit that section and
cannot clear a nonempty target. Explicit empty candidate entries clear slots.
Unknown markers, unsupported records and bad readbacks stop the operation.
Typed setters verify ACK, status, logical readback and complete durable NVM.
Failure tests cover timeout, bad ACK, storage fault, getter mismatch and
neighbor corruption, with no later command. Saved production preflights accept
retained legacy and alpha.1 backups into fresh target defaults; they are not
fresh current-device backups. Offline packing records permanent/trial images
and byte-equal native recovery without opening USB.

The installer retains a fresh physical hold for the displayed update and a
second guarded hold for settings restoration. Exact images, fresh backups,
cancellation before erase, one flash and failure stops remain. Documentation
and translations agree with this behavior. Public release notes contain only
user-visible changes and limits, and the release workflow reads that file.
All findings and closure are recorded in
`audits/rc6/combos-alpha-release-review-20261024.md`.

Physical Combo behavior, interactive GUI acceptance, physical unlock, USB
latency, arbitrary IRQ overlap, electrical IAP, power-loss recovery and
cold-start retention remain untested for this image. Published release CI and
fresh package acceptance remain pending. Installed firmware remains alpha.1.
Private OEM inputs and images remain outside Git.

## Linux installer addition

The native Linux x86_64 builder, pinned requirements, runtime paths, workflow
and bilingual release installation instructions are approved for commit and
CI. The final policy includes the new builder and tests. Firmware is unchanged;
the earlier 28-suite qualification remains firmware evidence, not a full test
of the later host changes. CI will rerun the complete qualification.

Nine packaging tests and four runtime path tests passed independently. The
frozen preparation regression also passed independently. The retained six
Linux integration logs were checked against recorded sizes and hashes. They
record 130 full installer tests before the final path fixes, 120 tool tests,
nine packaging tests, four runtime-path tests, one frozen preparation test and
syntax checks. A separate final complete workflow run reports sixteen tests
passing; its output is retained in the work session rather than a hashed file.

Review found and closed two frozen resource path errors: the udev rule lookup
and settings source pins now use explicit collected paths under the frozen
application root. Regression fixtures use nonexistent virtual module paths and
mock permission commands; they never install rules or access hardware. Frozen
Linux logs use XDG state storage; the Windows log path is unchanged.

The builder requires native x86_64 glibc 2.35 and does not bypass that guard on
the local glibc 2.39 host. It validates executable modes, internal tar links,
collected approved files, the frozen hidraw import and CLI/Tk smoke results.
The publication gate requires both native package jobs, checks sidecar hashes,
and checks each Linux/Windows application's exact fresh firmware and approval.
Native Ubuntu 22.04 collection and runtime smoke remain pending. Release is
approved only after those CI gates pass; local fixtures do not establish a
working native package. Installation guides match both archive layouts and
cover checksums, extraction, launch and Linux permissions. No hardware operation
is authorized by this addition.

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "e4ae796fe635b87c4a2375eeab73c5b6ebff88c98eef8b8a3d9fc3e9099faba1"
}
```
