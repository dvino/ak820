# Outer delivery preflight review

Date: 2026-10-26. Result: PASS for static preflight only; both findings below are closed.

Scope: static, read-only review of the prepared outer delivery helper and its
package verification dependency. The packager was not run. Final archives,
receipts, Git bundle import and hardware behavior are not approved by this review.
Repository AGENTS.md was read. Only this review record was written.

## Exact reviewed inputs

| Input | SHA256 |
| --- | --- |
| `/tmp/package-ak820-beta3-delivery.py` | `1598482db51068d747d9f462fafc330b2f865385bba0f23072fb5ea1902c9593` |
| `/tmp/verify-ak820-beta3-packages.py` | `fd57fcd9d068ff9d6303b529cf07ce92d57c6ebe55f35ec1a81d032edfc60eab` |
| `/tmp/ak820-beta3-bundle-import-baseline.json` | `967d8feb998317c0e5fd151907dc7430aecb439ca54c3e5b1f2cd103bba03e7d` |

## Findings and closure

1. The firmware checksum sidecar is copied without checking its content. The
   assembly receipt binds `firmware-bundle.zip`, but the helper does not require
   `firmware-bundle.zip.sha256` to name that archive and contain its actual hash.
   A stale sidecar can therefore enter a delivery whose generated manifest and
   result say PASS. Validate its exact digest and filename before copying it.
2. The output ZIP must be fresh, but the adjacent `.delivery-record.json` is
   written with `write_bytes`. An existing record is overwritten, and a symlink
   is followed. Require a fresh record path and use exclusive creation. This
   preserves the same no-overwrite contract as the ZIP output.

## Checks that passed in static review

The helper binds the supplied bundle bytes to a PASS receipt with the expected
base and final HEAD, requires a clean committed repository, and requires the
source commit to be an ancestor of HEAD. Platform archive and detached-checksum
bytes are bound to the package verification report. The release directory must
match catalog payload plus platform archives, sidecars and SHA256SUMS exactly;
loose catalog files must match the archive and the checksum inventory is exact.
The package verifier checks canonical archive paths, duplicates, regular-file
members, platform payload parity and prohibited runtime/private payload names.
The outer helper rejects symlinks while copying release files and selects a
small explicit set of verification files. The delivery manifest hashes every
other ZIP member; a manifest cannot include its own hash. ZIP bytes are reread
and compared after writing.

The generated README identifies an incremental bundle and requires an existing
repository with the stated base. Its fetch and switch commands are appropriate
if the final bundle exports `codex/beta3-direct-w`; that ref must be confirmed in
the actual final bundle review. The baseline JSON records an isolated import
setup without future commits or alternates; it is setup evidence, not proof of
a successful final import. The referenced standalone installation guides are
produced at release root by `tools/build_beta_release_assets.py`. Claims of
Python packages, ten profiles and offline-only verification agree with the
intended inputs. Actual final package contents and report truth remain for the
independent final output check. No USB, network, build or publication operation
was performed.

## Corrected helper review

The corrected `/tmp/package-ak820-beta3-delivery.py` SHA256 is
`d866289410557a445cdbde5ee45655d9b8b2e5df7718f54a033729bdbd3ec4f0`.
Static inspection confirms that the firmware sidecar must now equal the exact
verified archive digest, two spaces, canonical filename and newline. Both
output paths must be fresh, including symlink checks, and the receipt is opened
with `xb`. Findings 1 and 2 are closed for these bytes. The original helper hash
above identifies the initial reviewed revision. The other input hashes remain
unchanged. No packager run or final artifact approval is implied.
