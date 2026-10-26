Русский перевод: [CI и выпуски](ru/CI.md).

# CI and releases

The [release workflow](../.github/workflows/windows-installer.yml) runs on branch
pushes, pull requests, version tags and manual launches. Its current source path
builds the ten [profiles](profiles/README.md), with `main` as default. All ten
use schema03. This describes configured checks, not a completed beta.2 release.
Published beta.1 on 2026-10-25 had nine catalog profiles and standalone installers
for exact `work`. Artifact and hardware results belong in [Status](STATUS.md).

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

The Windows and Linux jobs download that same run's bundles, check their source
commit and stage them in `releases/beta2/<profile>`. Every selectable profile
needs its own matching manifest and approval. Packaging verifies collected
inputs inside both GUI and CLI applications. Windows performs native startup
smokes; Linux uses Ubuntu 22.04 x86_64/glibc 2.35 and Xvfb. CLI help, offline
verification and Tk startup do not open USB or prove interactive device behavior.

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
required jobs pass. Branch pushes, pull requests and manual checks produce
artifacts without publishing. Only the publication job receives write access.
Local tests do not create tags or releases. Standalone Windows/Linux packages,
SHA256 files and EN/RU instructions remain required release assets. Exact
publication results are recorded separately in Status.

Required workflow job names are:

- `Linux syntax and shared host checks`.
- `Qualify firmware (<profile>)` — all ten profiles.
- `Revalidate and assemble all ten profiles`.
- `Native Windows package build and smoke`.
- `Native Linux x86_64 package build and smoke`.

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
