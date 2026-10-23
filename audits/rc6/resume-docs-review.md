# RC6 resumed documentation review

Date: 2026-10-23. Independent bounded follow-up; no source changes or USB operations.

Result: PASS after correction of one documentation finding.

Reviewed README and AGENTS in English/Russian, plus current STATUS, BUILD and TESTING claims and translations against the Windows artifact report and current files. The AGENTS plain-language rule is equivalent in both languages. README distinguishes the project, uninstalled RC6 candidate, and currently installed RC5. STATUS/BUILD consistently identify the fresh Windows output, offline checks, private-image exclusion limits, and pending hardware verification. Superseded staging is described as external archived history rather than a current local input.

Finding D1 (closed): TESTING EN/RU still described artifact review as in progress and said no portable ZIP existed. Root corrected both paragraphs. Re-read confirms completed review links and the portable ZIP path. No other factual defect found in this scope.

Release manifest SHA256: 2b99a807b6aa3cfc8fda224c9116de246430f7a42ff5a6a37195730a914c1ae6. All 15 HOST_FILES still match manifest sizes/SHA256; mismatches: 0. GUI/CLI executable hashes remain those recorded in windows-resume-review.md. No command or release-hash changes were introduced by these documentation updates.

Final local portable ZIP independently checked: dist/AK820-RC6-Windows-20261023.zip, 21,062,938 bytes, SHA256 d1496ff2e080a945be3c0e86eb0ec6bdfa34c63e79daaa9c064a425189960149. All 1,225 entries passed ZIP CRC validation. All ten reviewed documentation files in the ZIP match current checkout bytes, including corrected TESTING EN/RU. This follow-up report remains outside the ZIP to avoid circular identity changes.

Reviewed document snapshot SHA256:

| File | SHA256 |
| --- | --- |
| README.md | f42b28bd3bc665a0a3672f2042c1152409040e8534cd6e4835f6871591619a99 |
| docs/ru/README.md | 81488f888db8888bb17c23071a0e9049668830f195be51ce961b5f5f781ddb9f |
| AGENTS.md | 779ba5a668460b7df47a9c11a6e406cd3867b49831a8db887fa7e0592904902e |
| docs/ru/AGENTS.md | 45b5e1d658a86124f1de19fa87f0d6a9aac386995e988e214ab6a5de0b8380cd |
| docs/STATUS.md | 80fa971e14d2dc3ff7db8c8fa122cc198a59e74cc1cec254d54635571de631b9 |
| docs/ru/STATUS.md | 06e8068e45075c94dd71541bdb31e5fa94ba0686b5e0d9292253579bda80bf05 |
| docs/BUILD.md | f4b1001fd9b557fbe9678510487c2a3ee56f4735ae573b96018c88e778517e23 |
| docs/ru/BUILD.md | 52b8d6a16c763be2b914a490306922d5925bf6800d1f8e5bf00a91a95be275c4 |
| docs/TESTING.md | 7cd69aa1dd568169f58b6079d3105b9c7f9700741c2af10be363ca996affeb97 |
| docs/ru/TESTING.md | 41192ed35f8f52b55b8f538f57b9fccdb5c3991b8b712a741d28af777715c783 |

No hardware behavior, flash consent, publication approval, commit approval beyond this bounded documentation agreement check, or whole-program safety claim is implied. Frozen docs/REVIEW.md and runtime _internal files were not modified.
