# Pass 28 final independent review

Decision: CLEAN for the reviewed offline pass28 packet. The earlier local-GCC P2 is independently closed. No unresolved actionable finding remains. This approval covers the frozen source, tests, audit package and five current documentation files recorded below; it is not whole-program completion, device acceptance, release approval or authorization to flash.

Reviewed HEAD eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e and complete current diff/untracked packet. AGENTS.md, Russian instructions and /home/danil/.codex/RTK.md were read. The reviewer did not author these changes. No firmware build, USB/device command, commit or push was performed. Test executables and collector output were temporary; this report is external to the repository.

## Source, ABI and bounded correctness

Only the locked AK820 QK_BOOT firewall changes. Non-AK820, unlocked, VIAL_ENABLE and VIAL_INSECURE paths remain intact. Zero/oversized and Vial-range checks precede pointer access/narrowing. For accepted lengths, leading/trailing partial pairs consume at most the available bytes and leave a nonnegative even interior count. Boundary reads remain unconditional in their original order, mutations agree with the original complete function, and the same original buffer, full size and destination reach the same writer. Public parameters and target memory qualifiers remain unchanged. Reviewed actual NVM cached-read and sticky-failure writer behavior agrees with the CPU fixture. No production-source finding.

The host oracle equals the full eb3c230 Git function. The harness compares packet including guards, reader count/order/addresses, fault flag and writer pointer/address/length/data. It explicitly excludes durable backend and writer faults. Direct subprocess GCC macro argv now contains literal quote characters rather than shell escapes; GCC receives one valid CURRENT_INCLUDE string definition.

Independently reran current run.py in the pinned offline Docker environment, with the repository mounted read-only and GCC selected by the local-compiler branch: PASS 6,849,504 cases, ASan/UBSan enabled, alias drift rejected, and skipped_read/reversed_reads/boot_bypass all rejected by actual DIFF lines. This closes original P2. An initial incorrect uid1000 invocation failed closed reading Git due to ownership; the uid1001 invocation passed. It was not admitted as evidence of a test failure. The earlier successful Docker-fallback result remains distinct historical evidence.

Reviewed linked.py and its support Console/Firmware code. Retained runner bytes match the original external proof. ABI slots use actual symbol widths/addresses; relevant source entries uniquely match build hashes. Semantic pair oracle does not duplicate cursor arithmetic. Empty 2600..26ff trampoline writes are guarded; no NVM ROM seeding or main/board initialization is used. Flash entry breakpoints and rejected-request reader/writer breakpoints must not fire. Full occupied-CODE snapshots, packet/cache/flags/SP/canaries are checked. The recorded 600 cases include 88 early rejections and retain all 44,638 occupied CODE bytes. This final review did not rerun the linked CPU suite; its retained proof and earlier independent raw-log verification were reviewed and identities were freshly validated by the collector.

## Audit and documentation

Independently replayed collect.py to /tmp/pass28-review-measurements.json: PASS and byte-identical to retained measurements.json. The collector checks current sources/tools/artifacts, permits only the named historical baseline source via the full Git commit, confirms retained pass27 context/review byte equality, validates actual current compiler context/provenance and reruns actual28 postlink binding checks. This establishes admissible retained context reuse rather than a new context certificate.

The five current documents, technical audit README and tests README agree with exact artifacts: maximal 44,638 CODE (-61), 3,007 physical XRAM, 4,285 main overflow; work 37,392 CODE (-78), 2,554 physical XRAM and 2,961 trailing bytes. Feature/storage configurations match retained pass27. Conditional stack is 165/167 and 160/171, with unchanged no-overlay policy. Context reuse, host fault limits, one-page CPU fixture, diagnostic-only status, open OEM/IRQ/bank/writer/full-regression/physical gates and no installer/release action are stated distinctly. The README compiler-fallback wording was corrected and freshly reviewed before freeze.

git diff --check passes. tools/check_docs.py emits four language-link failures in unchanged MAXIMUM-FUNCTIONALITY-PLAN.md, NVM-UPDATE-KERNEL.md, OPTIMIZATION-RESEARCH.md and ru/NVM-UPDATE-KERNEL.md; none concerns the reviewed changed files. Its process returns zero despite those diagnostics, so diagnostics, not exit status alone, were inspected.

Metadata-only integration may add this review/closure record and regenerate evidence ledgers without reopening source approval, provided new hashes are checked and no substantive source/test/evidence claims change. Any such change needs an exact final consistency recheck. No commit authorization is inferred beyond the root's/user's existing scope.

## Frozen reviewed file hashes

This is the preintegration reviewed snapshot. measurements.json and docs/maximal-current.json hashes below identify that snapshot, not a self-referential postintegration ledger. The future integrated final-review.md is excluded.

```text
f6ec095e55bb20cf613da85220eb27144043f7b0623463bab610bdde787d059c  qmk-8051-ak820/quantum/dynamic_keymap.c
cba9d046c100a13e3fdd157af0fe0c1dc39b1900fd8b3eeb0a623417c19f1df4  docs/STATUS.md
81f48af165c5d69b76b39515b37073667e4f35629b831c725fcdcdd91a5d489c  docs/ru/STATUS.md
58e6096f9a73d72a1dc35d7d87a4f968e26d19fea9bf2ca901d938b61be868f0  docs/MAXIMUM-FUNCTIONALITY-STATUS.md
9dffda05812f15e7d6f7ae875021fbd6f6f550f025080e1880c5eada2b8d1787  docs/ru/MAXIMUM-FUNCTIONALITY-STATUS.md
cbbed6ea72863fbc8e1279bcced1ba415faa9010fc652091ae94938adc1a6c84  docs/maximal-current.json
c7c984fced5cb0dc341996dd70026815fd429c9a66ec5dcf13f3cff14108f062  tests/ak820_keymap_firewall/README.md
2262dad9ab79ac0bb8375dcd378ccd37a2350bd5324772b8f7864d2eac3673ed  tests/ak820_keymap_firewall/harness.c
1c96072592f2f583292d14fa6e96da7c17194a262dbeaf917589f5a6123a74b1  tests/ak820_keymap_firewall/linked.py
9bb774aeb767b016f6ccd620c8039d5a744f0e4b7f252a7fe601a3b5ab3f4868  tests/ak820_keymap_firewall/oracle.inc
23bf85f141f4c90c18a0d6a2c1460b64230c32f4b6457084becce1fe4f86b4e7  tests/ak820_keymap_firewall/run.py
3d7cef843ccb297b558ce9f8af7688a6365371be8879d0a30c0330be0b32b736  audits/maximal-pass28-20261025/README.md
cc06fc6bfa7dd778e10d2ad1e2877576d6d8fb429cfd4d55481408635266215b  audits/maximal-pass28-20261025/collect.py
97245b773245b530316b7a3390951b279abb23c1abde636601cf3bf669ee43e9  audits/maximal-pass28-20261025/host-regression.jsonl
6e3282608a04e63c3f8f85a923a49aa9b42b1e204280510855c680f14bffd2a0  audits/maximal-pass28-20261025/keymap-linked.json
4016d539bddda3499d16f435970771dc5f80b14c749a5cedeb16df813e2db28a  audits/maximal-pass28-20261025/linked-checks.json
94a6c30ba3a4b1d18e6f11c4dc2394100b76bded7ddcc19c5cefc98a660a96a4  audits/maximal-pass28-20261025/maximal-context.json
9b4027a9b130c8595837378181b297b0bd71855743d1a1ef80a2f9dcf1521c6b  audits/maximal-pass28-20261025/measurements.json
7b9e05d58885b74bdd6d9345b80a1284d64e6c4a25bbdbf3bd9cd7fdbca95efb  audits/maximal-pass28-20261025/prototype-review.md
2539525cfcdcb93ba5ab81cd0b7c5d64a1688366261476a27022e9f40317fb29  audits/maximal-pass28-20261025/read-hook.json
ed86aeba450c92ee4c5554855f3a972158c1c1fb708a359cee38b5cbd5b41408  audits/maximal-pass28-20261025/source-context-review.md
7893cca11497723b04afb7d05401167ec57d99c9c7c1b88f43065ed685a35b26  audits/maximal-pass28-20261025/source-cpu-review.md
eefd022ab100a8d4e664b32fd9fa70badeb972254cf54dbcea3bdd32dbf5c363  audits/maximal-pass28-20261025/startup.json
7dab7c524d5caa5141f5d89ca10c2f91fc291b5f406b27f169e10cdd990c7a85  audits/maximal-pass28-20261025/work-context-review.md
f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5  audits/maximal-pass28-20261025/work-context.json
533e44a62b1e6e2ae8112461276406f8aa0a8e4f7d698d73154e345e3206d076  audits/maximal-pass28-20261025/work-irq.json
9389e5689217532e1d71e7301cc5a061ac4fd985e088a01396e7bc1fc09a6119  audits/maximal-pass28-20261025/work-startup.json
```
