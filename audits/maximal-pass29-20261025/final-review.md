# Pass 29 corrected final independent review — CLEAN

Fresh read-only independent review after the local compiler dispatch correction, 2026-10-25. Reviewed repository HEAD `6c2cdc0452b664e37cd32a30b31e3e5f800c49cc` and the frozen pass 29 packet. No actionable findings remain. This approves this bounded source/test/documentation/evidence packet for integration, not firmware installation or whole-program/hardware acceptance. Repository source, build outputs, Git and devices were not modified; no firmware build, hardware access or network was performed. Temporary verification output and this external review were written.

## Finding closure and source

The initial P2 is CLOSED. Actual `run.py` SHA256 `3b19caceb2609c677259b6175b3066990cdcd5ec44dd371b6c66830e61a24495` now prefixes GCC only for compiler arguments and executes the generated binary directly otherwise. A fresh independent run imported the actual unchanged module, redirected only `EVIDENCE`, and completed the local GCC branch: 134,217,728 comparisons across four variants, all three real mutants rejected, plus 33,554,432 AK820 generic comparisons under ASan/UBSan. This used `/usr/bin/gcc` 12.2 inside pinned image `sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d`, network disabled and repository parent read-only. Evidence: `/tmp/getter29-independent-local-gcc.jsonl`. The initial review is preserved as historical open-finding evidence; its model-only run is not substituted for this actual corrected-runner result.

Reproduction command:

```sh
docker run --rm --network=none --userns=host --user 1001:1001 -v /home/danil/ChatGPT/ak820-pass26b-restored-20261025:/review:ro -v /tmp:/review-output -w /review/ak820-max sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d python3 -c 'import importlib.util; from pathlib import Path; p=Path("tests/ak820_getter_bounds/run.py"); s=importlib.util.spec_from_file_location("getter_review", p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.EVIDENCE=Path("/review-output/getter29-independent-local-gcc.jsonl"); raise SystemExit(m.main())'
```

The eight-line production patch is AK820-only forwarding to existing guarded readers. Generic C and assembly bounds precede EEPROM access; non-AK820 checks remain. Every nonzero raw encoder direction byte selects clockwise consistently. Host extraction/oracle, independent address/return expectations, mutations and assembly translation were inspected; translated assembly is correctly distinguished from CPU execution.

## Linked proof and collector

Installed `linked.py` exactly matches the final external runner (`691646ee5cb11b23cb6cd17f38e63c834bb2742ed295238c480cd9de9d484da4`). Runner, external aggregate, final shard reports and actual raw CPU logs were independently inspected. Eight shards contain exactly 2,431 distinct cases: 768 valid matrix, 15 invalid matrix, 1,536 valid encoder including all direction bytes, 112 invalid encoder. Independent raw-log parsing found 576 actual reader entries per shard, 4,608 total, all with B=0 and ordered DPTR matching reported reads. Each shard preserves all 44,601 occupied CODE bytes before/after, address-order digest `b0b7cf133e144661cf06ea643f43d0d314f589575b17ff07b69503023b6e94dc`.

The linked runner checks emitted ABI widths/slots and tailcalls, actual reader returns, cache bytes/flags, SP and canaries. Flash/native write stopguards are active; simulated ROM writes are restricted to verified-empty trampoline space. No ROM/NVM initializer seed is called. CRT executes only to main entry, IE/IE_EX disabled. Earlier incomplete/snapshot-parser attempts are retained and not promoted to PASS. The final `dump /h rom` snapshots and raw logs support complete CODE preservation. This review did not repeat the CPU runs or claim independent reproduction of their hardware behavior.

The final collector SHA256 `4565f5ea8a4851f721da3303a1b03e032e8fb7c241107760691f5e3785d8c858` was independently executed after freeze:

```sh
python3 audits/maximal-pass29-20261025/collect.py --output /tmp/getter29-independent-final-measurements.json
```

PASS. Its result exactly equals frozen `measurements.json`; current ledger measurements hash and principal values match. It binds all 102 retained external CPU files, installed runner, aggregate, per-shard source/tool manifests and raw traces. Retained pass28 fallback is restricted to the full exact6c2 `dynamic_keymap.c` Git blob; unchanged dependencies/current inputs match in place. Retained pass27 context certificates/reviews are byte-identical and honestly labelled reused; protected actual ASM/tools/provenance and current postlink audit are revalidated. Current-image startup, finite reader and other bounded CPU identities are verified. `git diff --check` passes.

## Documentation and remaining limits

All five current documents, audit README, tests README and machine ledger agree with retained artifacts: maximal 44,601 CODE (-37), highest `0xd797`, overflow 4,248, physical XRAM 3,007/3,072, conditional stack 165/167; work 37,361 CODE (-31), highest `0xbb4f`, trailing free 2,992, physical XRAM 2,554, conditional stack 160/171. All 14 optional modules and fixed storage limits remain. Historical setter evidence is not represented as a new pass29 test. Outer local-GCC container provenance is separate from the runner's correctly null own container field.

This packet does not close full configured regressions, complete OEM startup/IRQ/routing/non-reentry and bank contracts, opaque writer qualification, new read faults, dirty cross-page transitions, durable storage, peripherals or hardware validation. Maximal remains overflowing, diagnostic and not installable. Work control does not replace the release. No release/installer/device change is approved or performed.

## Preintegration manifest and allowed follow-up

The manifest below binds the complete 29-file reviewed packet before this report is copied in. It excludes untracked Python bytecode caches. Its JSON file `/tmp/getter29-review-preintegration-manifest.json` SHA256 is `0b3ec7b84118f58e69db3efd577edd7778be53f2fda3f56831354e74f4637a6a`.

Metadata-only copying of this report into the audit and collector regeneration of evidence/measurements/current ledger are permitted without a new full review, followed by a quick check that every other manifest file is unchanged, the copied review is exact and the collector still passes. This avoids a review self-hash cycle. Any substantive source/test/runner/collector/documentation correction requires a fresh writer and independent review.

```json
{
  "audits/maximal-pass29-20261025/README.md": "50672afee56450f7de4cfb684d48cff1c44b6138b1b14ca5b3bd81417aa99a89",
  "audits/maximal-pass29-20261025/collect.py": "4565f5ea8a4851f721da3303a1b03e032e8fb7c241107760691f5e3785d8c858",
  "audits/maximal-pass29-20261025/getter-linked-SHA256SUMS": "1630bb04a9c49e8eaabf7440d6f6424723f380918a86dca981290458c547c816",
  "audits/maximal-pass29-20261025/getter-linked.json": "96410e0956aabb5a6cd15c364f8960f2d86a75b092c37c2dec8d74fe888666c0",
  "audits/maximal-pass29-20261025/host-execution-context.json": "95b843a8bf5b902d3c6642d30385e55f4a33c952641ab7e1723637af57d40d5f",
  "audits/maximal-pass29-20261025/host-regression.jsonl": "13b9431f45eeb9e069566d244126833ce5fca9462df3806a45b6af7a992bdb87",
  "audits/maximal-pass29-20261025/initial-review.md": "ea9e0712f86e632d28e1bd0f83c3539db1cfebf0fe81d35d1a1f048df8a0aaca",
  "audits/maximal-pass29-20261025/linked-checks.json": "7e96832230661c2e28909e43e6da4013b3ed69f2d8224d7119b5a3caee980e3c",
  "audits/maximal-pass29-20261025/maximal-context.json": "94a6c30ba3a4b1d18e6f11c4dc2394100b76bded7ddcc19c5cefc98a660a96a4",
  "audits/maximal-pass29-20261025/measurements.json": "f40ecacc22c697fe3e0130da06dac4efb3194fa7cdecf4022de1b11fc03295f5",
  "audits/maximal-pass29-20261025/prototype-report.md": "d625792ce170a536503a4487c7f08d44a12ffbd012bd98e972e265c7019dae9d",
  "audits/maximal-pass29-20261025/prototype-review.md": "d89770e28be64f504b0c8d10c6b913a375cde7dcb7d8281c33741541467c47df",
  "audits/maximal-pass29-20261025/read-hook.json": "f9d9549ba519c010121ae04a91088fca51cce86c5d327d5c32a798b72d8676cb",
  "audits/maximal-pass29-20261025/source-context-review.md": "ed86aeba450c92ee4c5554855f3a972158c1c1fb708a359cee38b5cbd5b41408",
  "audits/maximal-pass29-20261025/startup.json": "07de2bcae0c41edb2576556edaf2216250c17de110a643cec445ff9ad017b687",
  "audits/maximal-pass29-20261025/verification-tools.json": "59fa34e344370a1ad30c3ee96812c769ebe2ce7b75300efbb9cf962d9f871813",
  "audits/maximal-pass29-20261025/work-context-review.md": "7dab7c524d5caa5141f5d89ca10c2f91fc291b5f406b27f169e10cdd990c7a85",
  "audits/maximal-pass29-20261025/work-context.json": "f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5",
  "audits/maximal-pass29-20261025/work-irq.json": "4fe7bea3893e598661ee983e5c4fed3b8da5a5ffeaf3ff41cd9f1cccec516e3c",
  "audits/maximal-pass29-20261025/work-startup.json": "530c8ec01d4a6d9e562f6ed3e57303fd20f5a4df9aed3fddf96ac4c6d29d5342",
  "docs/MAXIMUM-FUNCTIONALITY-STATUS.md": "b117fff5a059ee79f1463effa4dd73f71e5d112f26b6f8e26ed1902b8bbc3f57",
  "docs/STATUS.md": "51f9e135a92d273315b9ef2f5a9312d7a8aa612170017a1812f43d904e480172",
  "docs/maximal-current.json": "e79813667937889b1ddb81aac08bdb6838cf1fa0d165ce03fc67e4c0785ad514",
  "docs/ru/MAXIMUM-FUNCTIONALITY-STATUS.md": "60577a72094dba6663fc365f4d5cbfb5ef972c0012f4f5cb35e14e28600db691",
  "docs/ru/STATUS.md": "5a161486cc321491a0f0c45749c1eeb4642e3939704721302df253f35bf0eefc",
  "qmk-8051-ak820/quantum/dynamic_keymap.c": "c97c3ea6511d51f246a9044679e418a3adcbc456022fa712f35c26c9e76a4a0b",
  "tests/ak820_getter_bounds/README.md": "bf46454bfd9b3ae89ac833632b7236e9df3cfc16c19884f33a928975f605c01c",
  "tests/ak820_getter_bounds/linked.py": "691646ee5cb11b23cb6cd17f38e63c834bb2742ed295238c480cd9de9d484da4",
  "tests/ak820_getter_bounds/run.py": "3b19caceb2609c677259b6175b3066990cdcd5ec44dd371b6c66830e61a24495"
}
```
