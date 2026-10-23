Русский перевод: [CI и выпуски](ru/CI.md).

# CI and releases

The [workflow](../.github/workflows/windows-installer.yml) runs on every branch
push, pull request and `v*` tag. It can also be started from the Actions page.
No keyboard, OEM backup or repository secret is needed for checks and builds.

The workflow pins Node.js 24 actions by full commit hash: checkout 7.0.1, setup-python 7.1.0, upload-artifact 7.0.2 and download-artifact 8.0.2.

## Checks and build outputs

The Linux job checks the syntax of tracked Python and shell files, validates
GitHub Actions workflows with a hash-pinned actionlint, checks project Python
for undefined names with pinned Ruff, and runs all host tool unit tests.
It downloads the pinned SDCC 4.6.0 and LUFA archives, checks their hashes,
builds the application, then runs host C and linked CPU regressions. Storage
harnesses model interrupted journal and macro writes. These checks cannot
prove physical USB, lighting or flash durability.

After the tests pass, Linux assembles a fresh public firmware bundle from that
run's IHX, MAP, MEM and build report. Windows downloads that bundle, checks its
commit identity and replaces the checkout's old release inputs before building
both installer applications. It checks packaged input hashes, runs CLI help and
offline verification, and creates and closes the Tk interface. This is an
automatic startup check, not a check of visible dialogs or interactive behavior.

Every branch push, including `dev` and untagged `main`, produces build artifacts
without publishing a release. The outputs include:

- The standalone public firmware bundle, with SHA256 and build evidence.
- The complete Windows portable ZIP, with SHA256 and startup-check reports.
- Linux application files and the host/CPU test logs.

The application IHX is not a complete flashable ROM. The installer constructs
the full update using a fresh backup and local OEM recovery data. Raw OEM ROM,
private sessions and device captures never enter the workflow or its artifacts.
The Windows installer contains the fresh firmware, not the old checked-in
`releases/rc6/firmware` files. The publishing job verifies both application
folders inside the Windows ZIP against the same run's firmware bundle.

## Review and reproducible builds

`ci/release-policy.json` records the independently reviewed IHX hash, the hash
of every parsed MAP symbol, the host code and the source inputs used by the
build and tests. `ci/program-review.md` binds the actual independent review to
that policy. `ci/packing-receipt.json` records prior local packing checks for
that exact program, performed using private OEM references.

CI must reproduce the reviewed program and symbol addresses, use the pinned
toolchain, and pass every required suite with zero skips. It checks the reviewed
inputs against the current Git commit. It then writes a machine build
attestation and an exact bundle approval. The machine record is reproduction
evidence, not a new independent review or permission to write a keyboard.

When firmware or reviewed host inputs change, update the policy and review
after independent review. Repeat affected local packing checks when their
inputs change. Track the evidence and hashes; new generated firmware binaries
do not have to be placed in the release directory or committed for CI. A stale
policy fails closed. CI reuses the verified packing receipt for the exact
program; it does not claim to repeat OEM-dependent packing in the cloud.

## Publish a release

Use a new SemVer tag on a checked commit in `main`, for example `v0.6.0`.
Only that tag starts publication, after Linux and Windows jobs pass. A tag on
a commit outside `main` cannot publish. `v0.6.0-rc.1` creates a prerelease;
build metadata such as `+build.1` is accepted. A manual run only checks and
builds. Ordinary branch pushes and pull requests do not publish.

The release contains both public firmware and Windows ZIP files with their
SHA256 files. Only the publishing job receives `contents: write`; checks and
builds use read access. No tag or release is created by local tests. See
[Build](BUILD.md) for the local build and packing commands.

Repository protection rules are separate GitHub settings. Select both job
names as required checks if branch protection is enabled:

- `Linux syntax, host, CPU, and pinned firmware build`.
- `Native Windows package build and smoke`.

## Run checks locally

From the repository root:

```sh
python3 tools/ci_checks.py
python3 tools/check_docs.py
python3 -B tools/test_keyboard.py --host \
  --build-dir qmk-8051-ak820/.build/local-1 --require-toolchain \
  --toolchain toolchains/sdcc-4.6.0 --iap-fault-profile guarded-erase
```

The last command requires a completed pinned build. It does not open USB.
The workflow also runs tool-specific tests and the separate storage harnesses.
Check the workflow for their exact commands. A local pass does not prove that
the GitHub-hosted jobs ran; execution results belong in [Status](STATUS.md).
