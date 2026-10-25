# Pass29 independent review — not approved

Read-only independent review on 2026-10-25. Repository HEAD is 6c2cdc0452b664e37cd32a30b31e3e5f800c49cc. This is an intermediate review of the current package, not final integration approval. The author and root were notified of findings immediately. No repository edits, builds, device access, network or Git writes were performed.

## Open finding

P2 — `tests/ak820_getter_bounds/run.py:150`: the local compiler branch in `execute()` always invokes `[cc[0], *args]`. Execution passes `[binary]`, so this invokes `gcc binary` instead of running the executable. The documented preferred host-compiler path fails its first variant. Reproduced in the pinned offline Docker image with GCC exposed as the local compiler, repository mounted read-only, userns=host and user 1001:1001; the failure is `ld: cannot open output file a.out: Read-only file system`. A writable working directory would still cause GCC to relink an executable rather than execute it. Keep OPEN until a different writer corrects dispatch and a fresh independent reviewer reruns the unchanged corrected runner.

## Bounded observations

The eight-line production patch forwards the two AK820 location wrappers directly to existing guarded getters and retains original guards for other boards. Generic C getters reject invalid coordinates before native EEPROM access. The current assembly geometry helper rejects invalid coordinates, uses every nonzero direction byte as clockwise, and the reader emits B=0 generic-pointer addresses. No production behavior defect was found in this bounded change.

The host harness extracts current wrappers/generic functions/assembly bodies and the full committed oracle blob. It checks returns, exact read count and ordered addresses against independently computed expectations across all byte inputs. Four configurations include AK820 generic, assembly translation, other-board generic and alternate generic geometry. Three mutations exercise direction, generic layer bounds and assembly layer bounds. Its bool model uses uint8_t, which intentionally preserves raw ABI direction bytes. The assembly translation is a host model, not target instruction execution or memory-qualifier proof.

A supplementary independent offline GCC run with an in-memory dispatch correction passed 134217728 comparisons, all three mutants and 33554432 generic ASan/UBSan comparisons. Evidence: external `getter29-independent-host-model-only.jsonl`. This does not approve the checked-in broken runner or constitute a reviewed source fix. The original author evidence was not overwritten.

The linked runner was inspected for actual linked parameter widths/slots and tailcalls, CRT-to-main-only execution, disabled IE/IE_EX, actual cache priming, read-entry breaks, stopguards on flash/native writes, exact returns/SP/canaries/cache flags and occupied CODE snapshots. The console restricts simulated ROM writes to verified empty trampoline space; the imported initializer that seeds ROM is not called. Aggregate parsing checks actual raw B/DPTR reader traces. The collector independently enforces the exact 2431-case set and source/build/tool/trace bindings.

At review, all eight final shard reports completed functional cases but were PASS=false because their final CODE dumps were incomplete (shard0 `after15919`). Therefore there was no accepted complete linked getter aggregate. These attempts cannot qualify the image. A forthcoming runner dump correction and complete rerun require fresh review; this review does not approve that correction.

The current collector was inspected: retained28 source fallback is limited to the full exact6c2 dynamic_keymap.c blob; unchanged/current sources, generated artifacts, tools, certificate provenance and fresh postlink checks are verified. It preserves conditional stack/IRQ, whole-image, full configured regression and hardware limits. It was not executed because the linked aggregate was absent and package authoring remained active. Documentation and the final generated manifest/ledger were not frozen, so full-package agreement and final approval remain pending.

## Review snapshot

Hashes below bind the files as present at report writing; linked runner may already be under an explicitly unreviewed follow-up correction. The substantive versions inspected are described above. No future edits are implicitly approved.

- `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max/qmk-8051-ak820/quantum/dynamic_keymap.c` SHA256 `c97c3ea6511d51f246a9044679e418a3adcbc456022fa712f35c26c9e76a4a0b`
- `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max/tests/ak820_getter_bounds/run.py` SHA256 `3b19caceb2609c677259b6175b3066990cdcd5ec44dd371b6c66830e61a24495`
- `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max/tests/ak820_getter_bounds/README.md` SHA256 `04ff123c04d3b46fe7ec1582b936128f22ba64403a8426d90937c16c7d7f7451`
- `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max/audits/maximal-pass29-20261025/collect.py` SHA256 `14746af9263ac08c09e9630e6ef9c84412cecf43e37fe37e6c8b03845f1df590`
- `/home/danil/ChatGPT/ak820-pass29-research-20261025/linked-getters/run.py` SHA256 `691646ee5cb11b23cb6cd17f38e63c834bb2742ed295238c480cd9de9d484da4`
- `/home/danil/ChatGPT/ak820-pass29-research-20261025/linked-getters/aggregate.py` SHA256 `afb74216a71c1dae14c432c97660e5655da6a17bde303b6e4d6df3c8989c59fd`
- `/home/danil/ChatGPT/ak820-pass29-research-20261025/linked-getters/README.md` SHA256 `63a5bd3e038974d7bfff493a61e4e041e3f70636603acc74edec2bdf816d2bb1`

A later final review may allow metadata-only copying of its review file and ledger regeneration, followed by a quick identity recheck, to avoid a self-hash cycle. Any source/test/runner substantive correction requires a fresh independent reviewer.
