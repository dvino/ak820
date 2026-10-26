# Beta.1 release asset review

2026-10-25. Result: accepted for publication with the limits below. This review covers the actual downloaded native archives, firmware bundle and regenerated catalog. It does not authorize device writes.

The firmware source is `bef20f89d3da01d770767919bc7c8fc3c3a1a808`. The installer manifest SHA256 is `b2239648809b6b8907089b4ce36e43ed25a0a677605b8cb41c272ab545e8a076`. Its approval binding, all 13 payload sizes and hashes, and the installer’s offline approved-release validator pass. The 25 packaged host inputs match the reviewed source. Documentation corrections do not change those inputs or the reviewed release policy.

| Asset | SHA256 |
| --- | --- |
| firmware-bundle.zip | `d5429dbf7ad84e6c6c6b21da555cc360f2444a682aa2730d5df5efc68fb396be` |
| AK820-Windows.zip | `6370ed8a0eb7750debe65925d57c63dd1da99a3cd98b8be97b6fb54feb5c8976` |
| AK820-Linux-x86_64.tar.gz | `f8163fb1e3c014341c549ceeafd1a5f388131d8f7b26609a1486a2e93e0d8508` |
| AK820-Beta1-Catalog.zip | `ccf180581fd092a8180940b3af4445c548c6f4f1a195277f32e20c3fcefdea06` |

Independent direct reads of both native archives confirm each GUI and CLI collected input against the approved firmware bundle or reviewed host source. Both executable hashes match their native build provenance. Windows provenance records CLI help, offline verification and native Tk startup smoke as passed. Linux provenance records CLI help, offline verification, Tk startup under Xvfb and frozen hidraw import as passed. The full [asset check](ci-assets-check.json) also passes archive safety, PE AMD64 / ELF64 x86_64 architecture, exact collected inputs and Linux offline CLI smoke.

The catalog’s 78 declared payload files match their sizes and SHA256 values. The ZIP payload matches the separate public files. All nine expected profiles are present. Only `work` is approved and installable; the other eight remain candidates. The work IHX SHA256 is `652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880`; its permanent CODE identity is `a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10`. Release approval remains separate from hardware validation and operation consent. Flashing, settings writes and hardware validation flags remain false.

The bilingual module descriptions include 28 features and nine profiles. English and Russian installation guides explain package selection, checksums, extraction and launch. The initial downloaded guides had relative links to files absent from the archive. This finding is closed: support links are absolute, their targets exist at the pinned source commit, and both shipped guides directly explain the module guide path base. The four-document correction and [link evidence](standalone-guide-links.json) pass independent review for a documentation-only follow-up commit.

No device commands were executed in this review. Native startup smoke does not prove interactive manual GUI workflows. Physical keys, both encoder directions, USB behavior, flash/update/recovery, settings persistence, power-loss behavior and installed firmware remain untested by this asset review. Publication acceptance applies to the exact assets above and does not imply hardware acceptance.

## Published files and final record

Post-publication review on 2026-10-25 passes. All 16 files in the public download directory match the expected sizes and SHA256 values in [assets.json](assets.json) and [publication.json](publication.json). Live GitHub release metadata independently confirms every asset size and SHA256 digest, the public non-draft prerelease state and the lightweight tag at compiled source `bef20f89d3da01d770767919bc7c8fc3c3a1a808`. The published archives retain the accepted hashes above. The [public asset check](published-assets-check.json) passes, including Linux offline CLI smoke.

English and Russian STATUS agree on the source, built packages and last recorded alpha.3 installation. They distinguish successful host/CPU/native smoke results from untested physical behavior. The ROADMAP edit removes installation state from future plans. Acceptance, publication, verification, CI and [completion](completion-audit.json) records agree with the checked assets and retained evidence. All 686 source files and 25 host inputs still match their release-policy sizes and SHA256 values.

The final documentation and evidence changes are approved for commit. No open findings remain. This approval does not claim a beta device installation or manual GUI acceptance.
