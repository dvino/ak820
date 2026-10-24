# Independent work beta review, 2026-10-25

The exact `work` program and installer preparation are approved for commit and
CI reproduction. Native Windows and Linux package acceptance and publication
remain pending. This approval permits no device operation and makes no claim
about physical behavior. Installed firmware remains alpha.3.

The reviewed IHX is `652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880`. Canonical linked symbols are `934f49ebf4d4c01a64c775e2f7b6e9cd2d7f8ad8d3fad50167d1483dec3112d1`.
All 686 policy source records and 25 host records match current sizes and
SHA256 hashes. Policy SHA256 is `af0a34e599519482749358533d01b4624ebd11724421df5dbd52f6691687f34e`.

The safety gate now accepts only the canonical configuration recorded with the
reviewed exact image. It does not approve another profile by name or schema.
The `work` application adds Leader, Dynamic Macros and OS indication to the
previous full profile. Its stack allowance is 99 foreground bytes, two CRT entry
bytes and 61 bytes for all enabled interrupt wrappers and callbacks: 162 of 165
bytes. Startup, all 15 distinct-source IRQ orders and all 256 LED selector values
are covered. These static and CPU results assume valid memory access, bank-0
SDCC calls, private guard objects and MCS-51 in-service/RETI behavior. They do not
establish physical VS11 timing.

The current exact image passes 28 base suites with 291 unit tests and zero skips,
and all 30 supplemental work suites. The first supplemental attempt stopped
because the asset generator and its tests changed during qualification. Its
logs and source snapshot are retained. Those two files do not affect the base
suite inputs or firmware image. The base logs and image were revalidated, then
the entire supplemental phase passed on the final source snapshot. The canonical
package approval was independently rechecked. This used the retained exact
build, not a fresh independent build. Base qualification SHA256 is `ae9ea35779bb1a850c243a37acac938282909eafcacd05b07a3935bd770c029d`;
the final combined record is [current work qualification](../audits/rc6/beta1-release-20261025/current-work-qualification.json).

The installer binds settings semantics to exact IHX and permanent CODE, including
the work feature set. Independent reruns pass 52 settings tests, 24 safety-gate
tests and eight catalog asset tests. The retained alpha.2 backup passes offline
preflight for 498 keys, 12 encoder assignments and eight Combo slots. Forward
alpha.3-to-work restore preserves both encoder directions; reverse downgrade
is rejected before writes. Fresh backups, physical confirmation, cancellation
before erase and stop-on-first-failure behavior remain required. Offline packing
covers permanent and trial modes and byte-equal native recovery.

Both contract modules and the Linux builder and dependency pins are included in
the host manifest. Public catalog promotion requires CI reproduced authorization,
current policy and source closure, exact work identities and safe regular-file
paths. Only work is promoted; eight profiles remain candidates. The publication
workflow requires both native package jobs, verifies packaged CI inputs and uses
an explicit asset file list. Pinned external LUFA inputs are fetched before the
catalog policy check in a clean publication checkout.

English and Russian installation instructions agree with the exact work image,
archive names and catalog limits. Review findings and closure are recorded in
[the audit review](../audits/rc6/beta1-release-20261025/review.md).

Physical keys, encoder rotation, USB timing, LED DMA, cold-start retention,
electrical flash faults, power-loss recovery and interactive GUI acceptance
remain untested for beta.1. Native package acceptance must pass before publication.

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "af0a34e599519482749358533d01b4624ebd11724421df5dbd52f6691687f34e",
  "program": {
    "ihx_sha256": "652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880",
    "symbols_sha256": "934f49ebf4d4c01a64c775e2f7b6e9cd2d7f8ad8d3fad50167d1483dec3112d1"
  },
  "qualification_sha256": "ae9ea35779bb1a850c243a37acac938282909eafcacd05b07a3935bd770c029d"
}
```
