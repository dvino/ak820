Русский перевод: [Независимое ревью](ru/REVIEW.md).

# Independent reviews

The current published release is `v0.6.0-beta.5`. The last recorded physical installation
was `v0.6.0-alpha.3`; it does not verify beta hardware behavior.
Exact images, checks and limits are recorded in [Status](STATUS.md).

| Scope | Evidence |
| --- | --- |
| Beta.3 release | [Release acceptance](../audits/beta3-direct-20261026/release-acceptance-firmware-20261027.md) and [independent firmware review](../audits/beta3-direct-20261026/firmware-final-review.md). |
| Nine-profile beta preparation | [Catalog, optimization, documentation and contract review](../audits/rc6/beta-catalog-20261024/README.md). |
| Alpha.3 release | [Release qualification](../audits/rc6/alpha3-release-20261024/review.md) and [independent program review](../audits/rc6/alpha3-release-20261024/program-review.md). |
| Alpha.3 installation | [Device result](../audits/rc6/alpha3-release-20261024/device-result.json). |
| Earlier stack, IRQ and Ctrl/GUI work | [Technical report and review records](../audits/rc6/runtime-stack-20261024/README.md). |
| Previous compact-feature source | [Review](../audits/rc6/compact-runtime-20261024/review.md) and [acceptance](../audits/rc6/compact-runtime-20261024/acceptance.md). |
| Runtime stack and IRQ proof | [Exact-image technical report](../audits/rc6/runtime-stack-20261024/README.md). |
| Repository cleanup | [Retained evidence and checks](../audits/rc6/cleanup-20261024.md). |

Host and CPU results apply to the checked source and images. They do not prove
physical behavior. Exact-image runtime proof covers its measured startup,
foreground and IRQ paths; release qualification remains a separate review.
Neither source review nor runtime proof authorizes installation or device writes.
