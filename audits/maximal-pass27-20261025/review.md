# Pass 27 exact final diff review

Decision: CLEAN for this bounded research-source and evidence packet. No open finding remains. This is not completion of the full maximal objective, image installation approval, release approval or hardware qualification.

Repository: `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max`. Branch `optimize/resume-pass26b-20261025`; HEAD `cfd05a0f5d296cc692224038a747dabb6694041f` plus the reviewed working diff. Independent reviewer did not author packet source, tests, documents or evidence. Review output is external to the audit directory to avoid measurement self-hash cycles.

## Scope and findings

Reviewed every tracked diff and all owned untracked files in `tests/ak820_raw_classifier/` and `audits/maximal-pass27-20261025/`, excluding `__pycache__`. The only firmware source change is the USB raw request classifier. Both English/Russian STATUS and maximal reports, machine ledger, collector and retained evidence were checked.

One documentation finding was corrected by the author: the Russian maximal report linked to a nonexistent local plan. Its final target `../MAXIMUM-FUNCTIONALITY-PLAN.md` now resolves. The exact correction and all six changed Markdown documents' local links were independently rechecked. No other finding was identified.

The classifier preserves the original outer allowlist, contiguous read ranges, encoder setter exclusion and dynamic setter holes. All six compile-time guards cover the interior enum members and excluded tails needed by these ranges. Unknown command/subcommand handling remains false. Downstream authorization and NVM gates are unchanged. The saved switch function matches the original `cfd05a0f5d296cc692224038a747dabb6694041f` function byte for byte. The persistent test uses the current function, current assertions and complete enum blocks from actual current headers.

## Verification

- Collector independently rerun with `/tmp/pass27-final-review-measurements.json`; it returned success and the output matches retained `measurements.json` byte for byte. The collector authenticates retained build artifacts and source/tool inputs, checks differing baseline source against original Git blobs, and binds exact image/map/listing reports, startup/CPU support and host source hashes. It collects retained evidence, rather than rerunning or independently proving CPU assertions.
- `docs/maximal-current.json` current/baseline/control fields and evidence equal the regenerated measurements; the referenced measurements SHA256 is exact.
- Persistent host regression rerun: all 16,777,216 prefixes agree; all 32 candidate packet bytes remain unchanged; both actual setter-admitting C mutants are detected at their first mismatch. This is host prefix evidence, not SDCC or hardware proof.
- All 84 maximal and 79 WORK context provenance hashes independently checked; application-only and unqualified flags remain explicit. Fresh prior source/context reviews were read and retained; no old certificate was promoted to changed-source acceptance.
- Exact-image startup, reader and bounded CPU evidence identities/scopes were checked. Retained component results were used without redundant expensive CPU suites. Maximal records 629 RGB, 576 Combo GET, 48 cache-only updater cases, 15 IRQ orders, 256 selectors and 20 CODE integrity sessions. WORK records 15 IRQ orders, 256 selectors and 17 whole occupied CODE integrity sessions. Reader evidence records 45 reachable instructions and seven rejected mutations.
- `git diff --check` passed. No full build, commit, push, hardware/device command or release operation was performed in this review.

Measurements remain consistent: maximal CODE 44,699 (48 bytes saved), physical XRAM 3,007, stack capacity 167, conditional bound 165 and CODE overflow 4,346. WORK CODE is 37,470 (75 saved), physical XRAM 2,554, stack capacity 171 and conditional bound 160. Both retain their documented configuration; maximal has 14 optional modules plus the base. Complete OEM startup/IRQ routing/non-reentry, bank and opaque-writer contracts, legal maximal CODE placement, full configured regressions and physical validation remain open.

## Frozen review identities

Tracked binary diff SHA256: `dc81388286b5c7571cc509a81bcdf7739fdcfc4e6ff45e5077b77d767f1b1a44`.

```text
76cad8e05c8f3d8b91a6eb1849be8f98bab29ddd0c069beb8f73d7291866e5f5  audits/maximal-pass27-20261025/README.md
e53d4db9d33c5e1c7b6476254591766b5e10a956399d04b6412f066f317c6f1f  audits/maximal-pass27-20261025/baseline-context-review.md
916c6e2282ff3c979e6beb06ecb826016818d86828618f873030c461b4d0bfe7  audits/maximal-pass27-20261025/collect.py
a31ced23f5ae76e738d649f0fa28c504b226ba748cc48c6d8ae7c6f1ef8baff3  audits/maximal-pass27-20261025/host-regression.jsonl
02f6cf98000b003e0b7d5b6133d7d9988d0630b21ddeb5eebf904b01c7daf1bc  audits/maximal-pass27-20261025/linked-checks.json
94a6c30ba3a4b1d18e6f11c4dc2394100b76bded7ddcc19c5cefc98a660a96a4  audits/maximal-pass27-20261025/maximal-context.json
7bf8683b80e375ae2752867aab9c59eacbb5dd06c7e800d5264dbe333834788a  audits/maximal-pass27-20261025/measurements.json
ddd72f82bbc019110f07bb96c1117ebd0f863585383dc48f1dca8e2efaa0e029  audits/maximal-pass27-20261025/read-hook.json
ed86aeba450c92ee4c5554855f3a972158c1c1fb708a359cee38b5cbd5b41408  audits/maximal-pass27-20261025/source-context-review.md
ad99c86fd14883bfa0e9e2b6fb7452ac1ac75edf84f898d8db65dd46a7a51a17  audits/maximal-pass27-20261025/startup.json
7dab7c524d5caa5141f5d89ca10c2f91fc291b5f406b27f169e10cdd990c7a85  audits/maximal-pass27-20261025/work-context-review.md
f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5  audits/maximal-pass27-20261025/work-context.json
e1e65e46a0b7f3d392deb7bd22d8c0a7d16d328c1f73eea1a1aa31952055fa39  audits/maximal-pass27-20261025/work-irq.json
51a14d4b375005c38221c575bc3f90cfcbcb6b43fe32d82ac31bba89db4d8efc  audits/maximal-pass27-20261025/work-startup.json
3a14dec422daecfb2f8bc4f410ed7352a16431f681b83aadaac2457799ac4706  docs/MAXIMUM-FUNCTIONALITY-STATUS.md
1a3568c06ccbbc3bbcfa8a65e06882dc147ad982b8aeabaa595ffa8e4efd9b7f  docs/STATUS.md
4b60dfacc2b192c94329677fe3402befa4b2c92aa805b557f4d565035e788e77  docs/maximal-current.json
0b4c02b74471f8d2b015940cfc1e9e9240d65043e7a15a2d7c89f0ff48f54639  docs/ru/MAXIMUM-FUNCTIONALITY-STATUS.md
16e3720c593dfc1d4e66ac4c0c29a2591109514c1fbc375081c94ef56dd17a97  docs/ru/STATUS.md
e72369aab695c9e9480de3fa7ca887343a84dfc48e68b44eaee510bfeeb91bd1  qmk-8051-ak820/tmk_core/protocol/ch555/usb_ak820.c
eb27224d891d4eddb99dae86dff98c69631a535b82687e15793aaa195fb8b291  tests/ak820_raw_classifier/README.md
589c796d84e0f95cbf84a24350b220e903de5639de8de3396d556d0a180982b4  tests/ak820_raw_classifier/oracle_switch.inc
1d60ed63f08e487d88550e1e2cf1ecd59b34fe927a84d13adfb195f9e195bcbc  tests/ak820_raw_classifier/run.py
```
