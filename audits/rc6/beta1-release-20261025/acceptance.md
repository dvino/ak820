# Work beta acceptance

Date: 2026-10-25. Release: `v0.6.0-beta.1`. The release is published. All three native CI jobs and
checks of all 16 downloaded public assets passed; see [publication](publication.json).

The beta integrates source `61a8c52d0c004ec2c67c0891945da98337db468e` from the
supplied archive and the later configurator migration from `d9954ac`.
Application source remains in the separate AK Configurator repository.
The [handoff check](handoff-check.json) compared all 7,980 tracked archive files
with that commit: no differences, missing files or uncommitted files were found.

Windows and Linux x86_64 installers target the exact `work` image:
`652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880`.
Its permanent packed CODE SHA256 is
`a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10`.
The source still uses the internal `rc6` bundle format; the public release is
beta.1. This internal folder name does not identify the installed image.

The other eight linked profiles, the selection matrix, exact-image capabilities,
and bilingual descriptions form the companion design catalog. They remain
candidates. The original catalog evidence and candidate ZIP are preserved;
release assets promote only the exact reviewed `work` row. Operation consent
and physical validation flags remain false. Original candidate flags describe
the earlier pre-release state; the work installer approval and release catalog
are separate, exact-image records.

All nine retained evidence sets passed the [source/evidence recheck](evidence-recheck.json).
This rechecked 29,145 retained files and original qualification records; it was
not a fresh build or regression run. Original firmware images and compiled
inputs are unchanged. The subsequent host approval/settings changes are tested
separately and included in fresh work qualification.

Offline packing used validated private OEM references. Both permanent and
trial payload checks passed; native recovery remained byte-equal. No private
ROM, settings, device capture or generated flash image enters public assets.
The [packing receipt](../../../ci/packing-receipt.json) contains only sanitized
hashes and results. A real retained alpha.2 settings backup passed migration
preflight for 498 keys, 12 encoder assignments and eight Combo slots. The
[transition record](transition.json) binds the 52 settings tests and exact
preflight output; host models include alpha.3-to-work and downgrade rejection.

The work foreground bound is 99 bytes; main entry adds two and interrupts add
61: 162 of 165 stack bytes, leaving three. The catalog's Tap Dance and Key
Overrides candidates have zero modeled margin. These models do not establish
physical USB timing, LED DMA, real flash faults, power-loss behavior or manual
GUI behavior. No device command was sent. Installed firmware remains alpha.3.

Final checks and findings are recorded in [verification.json](verification.json)
and [independent review](review.md). Public download checks passed and are recorded in
[published-assets-check.json](published-assets-check.json).

The immutable program and offline-review records describe approval before CI.
Their pending-package wording is scoped to that earlier review point; current
publication and native acceptance are recorded above and in publication.json.
