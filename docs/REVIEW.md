Русский перевод: [Независимое ревью](ru/REVIEW.md).

# Independent reviews

Updated 2026-10-24. This page indexes review evidence. It is not a release
approval record. The published and installed image is `v0.6.0-alpha.2`; exact
identity and verification state are in [Status](STATUS.md).

| Scope | Review evidence |
| --- | --- |
| Published alpha.2 artifacts | [Published artifact review](../audits/rc6/alpha2-release-20261024/published-artifact-review.md) checks downloaded packages, source and packaged inputs. [Asset check](../audits/rc6/alpha2-release-20261024/asset-check.json) records archive verification. |
| Installed alpha.2 | [Installation review](../audits/rc6/alpha2-release-20261024/installation-review.md) and [device result](../audits/rc6/alpha2-release-20261024/device-result.json) bind the installed image and read-only final settings check. |
| Build and qualification | Tag CI run [40060505913](https://github.com/dvino/ak820/actions/runs/40060505913) passed four jobs. Firmware qualification passed 28 suites and 270 unit tests with zero skips. |
| Earlier development work | Reviews and qualifications for earlier images remain in their dated reports and Git history. Their approvals and hashes do not apply to alpha.2. |

The current evidence does not establish physical Combo timing, nonempty Combo
write/restore, power-cycle retention, power-loss behavior, manual GUI acceptance
or a worst-case stack bound. Host and linked CPU results do not prove device
behavior. Any future release review must bind its exact IHX, MAP, build report,
host inputs and packages. A source review does not approve a new package or
device operation.
