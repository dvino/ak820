Русский перевод: [CI и выпуски](ru/CI.md).

# CI and releases

The [release workflow](../.github/workflows/windows-installer.yml) runs on branch
pushes, pull requests, version tags and manual launches. Its current source path
builds the ten [profiles](profiles/README.md), with `main` as default. All ten
use schema03. Published artifacts and hardware results are recorded separately
in [Status](STATUS.md).

## Firmware and installer jobs

The Ubuntu 24.04 job checks Python and shell syntax, workflow syntax with pinned
actionlint, undefined Python names with pinned Ruff, and offline tests. SDCC
4.6.0, LUFA and the QMK environment use pinned dependencies. Actions are pinned
by full commit. No keyboard, private OEM ROM or device session is supplied to CI.

After shared checks, ten matrix jobs each run the producer with `--profile <name>`. Every job keeps its complete final and bootstrap trees. A separate assembly job requires all ten successes, restores those trees at the same checkout paths and repeats the exact-image admission checks before packaging. Omitting `--profile` builds all ten locally.

`tools/build_ci_profiles.py` is the all-profile producer. Each profile gets a
fresh bootstrap and source/IRQ context, then the audited pass30 build. The final
image's foreground, startup and IRQ bounds are checked before full base and
profile regressions. Bootstrap evidence must remain unchanged. Unknown paths,
missing context, overflow, failed tests or skipped required checks stop the run.
Host storage power-loss models remain separate from physical durability.

To build all ten locally (the workflow adds one `--profile` per matrix job):

```sh
python tools/build_ci_profiles.py \
  --builds-root qmk-8051-ak820/.build/ci-profiles \
  --bootstrap-root qmk-8051-ak820/.build/ci-profile-bootstrap \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python \
  --report qmk-8051-ak820/.build/ci-profile-builds.json
```

These output roots must be fresh. Run from the repository root after installing
the pinned dependencies and QMK environment described in [Build](BUILD.md).
Do not run builds concurrently in one source tree.

After qualification, `tools/build_ci_release.py --all-profiles` checks the
per-profile policies under `ci/profiles`, independent reviews, packing receipts
and `tools/installer/settings-catalog.json`. It writes complete bundles to
`dist/ci-firmware/profiles/<profile>`. Missing or stale approval inputs fail
closed; creating a linked image alone does not satisfy this gate.

Assembly also exports the capability catalog from those exact CI builds. Publication uses this catalog and the measured firmware matrix, so path-dependent MAP and report hashes refer to the approved CI files. It does not replace them with hashes from local builds.

The assembly job produces approved firmware bundles. The tagged release job
checks their source commit, copies all ten profiles to `releases/beta4`, builds
the Python Windows and Linux x86_64 packages and companion catalog, and checks
the published package checksums. It does not build standalone GUI installers.

## Validation time

The expensive pass30 transform replay runs once per unchanged build in a
validation session. Release assembly uses `tools/ci_parallel_assembly.py` with
`--validation-workers 4` for the first inspections. Workers return successful
results through memory to the parent, which runs the original assembler and
rehashes every input before reuse. `--validation-workers 1` uses the same
checks serially. The original `tools/build_ci_release.py` remains usable. Later inspections hash the complete replay inputs again before
reusing that result. The snapshot covers source and checker files, intermediate
file contents and directory membership, compiler tools, headers and libraries,
default-keymap dependencies, bootstrap provenance, and the process environment.
It uses file contents, not modification times. Changed or unsupported inputs
run the full validator again; a failed replay cannot create a cache entry.

This cache stays in the current job's processes. It is not uploaded, restored
from disk, or shared between CI runs. Each new job still performs its own first
replay. A worker failure stops assembly. All other
image, source, memory, runtime, test-log and release-policy checks still run.
Regression logs are outside the replay inputs; creating them does not require
recompiling the same proof. Profile logs record total and test-only time per
suite. ZIP and gzip artifacts upload without a second compression pass.

## Catalogs and evidence

The source firmware matrix can contain ten unmeasured rows. The capability
catalog remains empty until exact qualified records are imported. Do not copy
previous identities into current rows. A catalog does not grant writes or
physical validation; see [Development catalog](DEVELOPMENT-CATALOG.md).

The separate [candidate workflow](../.github/workflows/firmware-catalog.yml) and
`tools/build_profile_catalog.py` export development candidates. They do not
supply release approval. Any fresh current-profile path must supply the required
source/IRQ context; a historical nine-profile workflow is not evidence for the
new compositions. Retain complete logs and intermediate evidence, including
partial results from failures.

Per-profile release policy binds exact IHX, MAP symbols, build inputs and host
files. A matching packing receipt records previously reviewed local checks
using private references; CI does not repeat OEM-dependent packing in the cloud.
Machine reproduction and bundle approval do not replace independent review or
authorize a device write. Changed source or host bytes require renewed evidence.

## Publication and local checks

Only a qualifying SemVer tag on a checked commit in `main` can publish after
required jobs pass. Branch pushes and pull requests produce artifacts without
publishing. A manual run on a version tag can publish after fresh full profile
qualification, or after an explicit `qualified_run_id` passes all
artifact-reuse checks. Other manual runs only produce artifacts. Only the
publication job receives write access.
Local tests do not create tags or releases. Release assets use Python scripts
for Windows and Linux x86_64, matching SHA256 files and English and Russian
instructions. Exact publication results are recorded separately in Status.

Required workflow job names are:

- `Linux syntax and shared host checks`.
- `Qualify firmware (<profile>)` — all ten profiles.
- `Revalidate and assemble all ten profiles`.

For local syntax and document checks, run `python tools/ci_checks.py` and
`python tools/check_docs.py`. To qualify an existing completed current image:

```sh
python tools/configure_firmware.py qualify \
  --build-dir qmk-8051-ak820/.build/local-1 \
  --toolchain toolchains/sdcc-4.6.0
```

Qualification rechecks the saved context and complete transform chain before
runtime proofs and regressions. A local pass does not establish a successful
GitHub run, publication or hardware behavior.
