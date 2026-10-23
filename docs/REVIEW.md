Русский перевод: [Независимое ревью](ru/REVIEW.md).

# Independent reviews

Updated 2026-10-23. Review is specific to the source and artifact it names.
The development candidate and installer release are different images.
This page indexes evidence; it is not a machine-readable release approval.

| Work | Review and limits |
| --- | --- |
| Windows packaging | [Source review](../audits/rc6/windows-package-source-review-20261023.md): both application trees, exact file identities, synthetic packaging/smoke failures and manual-only workflow. Native Windows execution remains pending. |
| Compiler selection and regression reports | [Runner review](../audits/rc6/regression-runner-review-20261023.md): selected tools reach all suites, skips and launch failures stay visible, images are checked throughout the run. |
| Private XDATA journal pointer | [Bounded review](../audits/rc6/bounded-optimization-review-20261023.md): source/ABI, host and linked helper checks, controlled size delta and portable evidence. No release promotion or hardware approval. |
| Inventory, integration and current documents | [Completion review](../audits/rc6/roadmap-completion-review-20261023.md): independent code checks, exact inventory reproduction, finding closure and final documentation/evidence result. |
| Host settings protocol and workflow | [Protocol](../audits/rc6/host-settings-protocol-review-20261023.md), [backup/restore core](../audits/rc6/host-settings-core-review-20261023.md) and [installer workflow](../audits/rc6/host-settings-workflow-review-20261023.md): synthetic/offline checks, exact-image limits and failure stops. |
| Installer release binding | [Exact review record](../releases/rc6/reviews/independent-review.md): approved release IHX/MAP/build report and 19 current host files. This record does not approve the pointer candidate or a newly built EXE. |

The [current status](STATUS.md) names the exact firmware identities and evidence
levels. The [qualification manifest](../audits/rc6/roadmap-qualification-20261023/manifest.json)
retains initial failures and final results. Unit, host and CPU passes do not
prove physical USB/flash behavior, Windows input, power-loss durability or a
bound for every stack path. Prior release reviews remain in Git history and
artifact-specific reports; their image hashes must not be reused for a new build.

A future release needs a new independently reviewed record bound to its exact
IHX, MAP, build report and host inputs. Building or reviewing source does not
change the installer approval file. Publication and device writes remain
separate operations with their own authorization requirements.
