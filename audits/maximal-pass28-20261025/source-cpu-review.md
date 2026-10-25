# Pass28 source and CPU evidence review

2026-10-25. Independent read-only review against HEAD eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e, branch optimize/resume-pass26b-20261025. Repository instructions and RTK instructions were read. No firmware build, device access, tracked edit, commit or push occurred.

Decision: production source and the bounded exact-linked CPU proof are admissible within the limits below. The host regression runner has one P2 defect requiring correction and fresh independent review before whole-packet approval. This is not final documentation or commit approval; future root documentation was not available for review.

## Finding P2: direct GCC mutant macro quoting

In tests/ak820_keymap_firewall/run.py, the local compiler branch constructs include_option with shell-escaped backslash-quote characters and passes it as a subprocess argument without a shell. GCC receives those backslashes literally. Mutant harness compilation fails at #include CURRENT_INCLUDE instead of exercising the mutant. This branch is selected whenever GCC is available.

Confirmed using the actual include_option AST expression evaluated with a test name and passed directly to GCC in offline Docker via subprocess argv. GCC exited 1 with `missing terminating " character` and `#include expects "FILENAME" or <FILENAME>`. The probe used stdin and generated no repository artifact. Fix direct argv to contain literal surrounding quote characters without shell backslashes. Validate the local-compiler branch with GCC available, then obtain fresh independent review. The author must not approve the correction.

The recorded Docker fallback result remains valid: its shell quoting is a different path and its three mutants reached real DIFF failures. The frozen runner reviewed here has SHA256 b7c4be4b038242e54ea342f32ae37f821b6b61ad2e49d25f4a1defaef7f6e943. Any later correction is outside this review.

## Production source

Reviewed the actual complete function, diff, original oracle and NVM backend. dynamic_keymap.c SHA256 is f6ec095e55bb20cf613da85220eb27144043f7b0623463bab610bdde787d059c. The change is confined to the locked AK820 QK_BOOT filter; other-board code retains its existing branch.

The size and range gates precede byte narrowing and partner reads. Nonzero accepted sizes are at most 28; valid offsets are bounded by the 1536-byte extent. The leading partial pair advances cursor and decreases remaining once; the trailing partial pair decreases remaining once. These operations cannot underflow: a one-byte request cannot have both partial edges, and a two-edge request has at least two bytes. The resulting remaining count is even. Partial reads retain their prior order and unconditional occurrence, including fault behavior in the host mock. Whole boot pairs become ffff; a partial boot pair modifies only its input byte. The backend call, address, length and sticky-failure contract are unchanged. No production-source finding was identified.

## Host evidence

The oracle is the complete original function tied to eb3c230, not an invented model. The harness compares the full packet, read addresses/order/count, fault flag, writer pointer/address/length/data and canaries. The saved host result records 6,849,504 cases with ASan/UBSan and actual skipped-read, reversed-read and boot-bypass mutants rejected by DIFF. Config and QK_BOOT constants are source-derived with drift rejection. The EEPROM read-fault mock is explicitly limited; it does not qualify writer failures or durable storage. Existing Docker host evidence is admitted; portable runner completion is blocked by P2 above.

## Exact-linked CPU evidence

Reviewed linked-firewall/runner.py SHA256 1c96072592f2f583292d14fa6e96da7c17194a262dbeaf917589f5a6123a74b1, README, latest results, support classes and actual backend. Independently recomputed every recorded immutable-input hash: all match. Independently parsed raw before/after CODE dumps from cpu.log against the IHX: all 44,638 occupied bytes match in both snapshots, including oversized-image regions. The latest results contain 600 passing calls, including 88 rejected requests. Earlier failed parser attempts remain failed; only the latest successful run is admitted here.

The target oracle operates on aligned input/partner byte semantics rather than copying cursor arithmetic. Partial-edge boot pairs, whole boot pairs, equal-cache writes, keymap endpoints, both lock states and initial dirty/sticky-failure combinations are covered. In the real backend cached scalar reads remain readable after sticky failure; writes stop through load_page returning false. The fixture models that behavior correctly and does not claim new read-fault injection.

Actual map/listing metadata supplies symbol addresses, spaces and allocation widths. ASM and relocated-listing widths agree for the two-byte size and three-byte generic data pointer; offset is loaded in DPTR and XRAM generic pointer tag is zero. Current config, keycodes, dynamic_keymap and NVM source hashes each require a unique matching build-manifest source entry. QK_BOOT alias identity is checked and missing/changed/duplicate in-memory cases are rejected.

Only verified-empty 2600..26ff trampoline ROM writes are generated. CRT executes to main entry, main and board/NVM initialization do not execute, and IE/IE_EX are then disabled. No ROM NVM seed is installed. Every target call must reach 2700; flash erase/program/program_page/write_page entry breakpoints remain installed. Reject cases additionally stop at EEPROM reader and block-writer entry, so unexpected storage access cannot silently pass. Full packet guards, cache page, flags, SP return and IRAM canary are checked per call. Raw dump /h fixes the earlier disassembly parsing failure; CODE snapshots agree byte-for-byte with the original image.

No CPU-script correctness finding was identified for this bounded fixture. Single primed cache page with batch depth 1, cached reads and stopped flash paths do not qualify cross-page transitions, flash effects, durable storage, IRQ behavior, peripheral timing or physical keyboard behavior. Observed peak SP 105 is only a bounded-run observation, not the whole-image stack bound. The root image is oversized and is not a flashable/device-qualified artifact.

## Context provenance spot check

Read current validate_context: it checks tools/fixed maps, every provenance hash, protected-module canonical contents and absolute map. Independently verified all recorded provenance file hashes in both exact build context certificates: root 84 entries and work 79 entries match. Certificate hashes are 94a6c30ba3a4b1d18e6f11c4dc2394100b76bded7ddcc19c5cefc98a660a96a4 and f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5. This check does not substitute for running complete build validation or re-reviewing all older transform certificates. Root linked-check/startup/read-hook evidence was inspected for identity and scope; no old RGB regression suite was rerun.

Required closure: fix local GCC quoting; run that branch with real mutant DIFF rejection; obtain a fresh independent review of the correction and completed exact packet including new documentation. No author-fix approval is implied by this report.
