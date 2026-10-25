# Pass 30 final packet independent review

Result: CLEAN for the frozen implementation, tests, documentation and recorded evidence. No actionable finding remains. This review is independent of the implementation and documentation authors. Base HEAD is bb91d897748fac8ba3363887fa4af5c3a3a926c6; the manifest below identifies the reviewed pre-integration dirty tree. This is approval of this bounded diagnostic packet, not installability, release, physical acceptance or completion of the full-feature objective.

## Source and integration

Reviewed the complete generator, Make integration, builder changes, both C changes, unit/TU/sanitizer/linked test sources and README. The bootstrap compiles current C literals under the actual configured SDCC flags; strict CONST CODE parsing rejects unsupported metadata, lengths and directives. The fixed 16x8x2 class/payload/offset representation round-trips every word. Bounds precede decoder index arithmetic; uint8 offsets are checked by generation. Encoder/LED allocations and ordinary VIA dynamic NVM/wire paths retain their contracts. The option remains off by default; original and non-VIA branches remain under their original behavior, while unsupported compressed configurations fail closed.

Make forces introspection regeneration, provides the generated include bootstrap target and resets CC_EXEC per object. The bootstrap assembly is outside the linked object manifest. Compiler/generator identities, bootstrap and final preprocessing/compile dependency closures, generated header hashes, final assembly arrays and absence of original bootstrap allocations are checked. Private phase arguments are rejected; indirect phase injection is caught by final assembly verification. Failed final compiles remove the object and include. The earlier P2 phase-override and final dependency-closure findings are closed by the corrected source and separately retained independent actual compiler rerun. The builder binds the generator, dependency evidence and generation files in its artifact/source manifests.

## Independent verification executed in this review

- Seven generator/parser tests passed. Host execution of the sanitizer checker initially could not find cc; the qualifying rerun used the pinned cached container and passed all 16,777,216 uint8 coordinate triples with the exact integrated C getter and current bootstrap defaults.
- The pinned offline container was sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d, network none, userns host, uid/gid 1001. Source/build/evidence mounts were read-only. No full QMK build was started by this reviewer.
- Independently aggregated the four accepted linked-decoder shards: 275 unique calls per image, 550 total, all 256 valid defaults and 19 invalid cases. Current immutable-input hashes matched; full occupied CODE before/after matched; the valid generic C52 tick delta totals 706,464. The installed tests/ak820_default_keymap/linked.py is byte-identical to the executed external runner (f00607127e111b42efbdf30d690cf8950f01d10dc344a0ad5ac454dc49a5183e). Its actual emitted ABI, empty trampoline-only simulator ROM writes, backend stopguards, SP and canary assertions were inspected. No nonexistent raw-count entry was executed: its DCE removal is explicitly static-only evidence.
- Executed the final collector 7ab096f432aa02437988d797a91fe568ca90cf95875c76d37158805753290f06 in the same offline container with all required external sibling evidence mounted read-only. It authenticated all four fresh source/toolchain/artifact manifests, current generated dependency/ASM/linked bytes, retained context certificates and fresh actual postlink checks. Independently regenerated measurements.json and docs/maximal-current.json and compared both parsed JSON structures exactly; requested final output writes were intercepted, leaving the reviewed source read-only. Disposable postlink reports used /tmp.
- git diff --check passed. The historical pass29 audit is untouched. No repository/source/build/Git, device or network write occurred in this review; only this external review report was written.

## Image and evidence agreement

Fresh same-source maximal OFF/ON images are 44,601/44,400 occupied CODE bytes, a 201-byte saving; work OFF/ON are 37,361/37,170, a 191-byte saving. Physical XRAM grows by three bytes in each pair. Maximal ON IHX is e4f1d3f64583da25a189c048a9905213a926ca43ae005652ab98964ccc1d954f. The OFF images exactly match the respective old29 images. All14 module settings and fixed six-layer/16-macro/8192-byte/eight Combo-TD-KO/both-encoder configuration limits remain preserved in the paired reports.

Maximal has main high address 0xd6ce, 4,047 overflow bytes, 3,010 physical XRAM bytes and conditional stack 165/167. Work has high 0xba90, 3,183 trailing main bytes, physical XRAM 2,557 and conditional stack 160/171. Those stack totals include the actual CRT two-byte frame and three distinct 17-byte wrappers plus callback bounds. OEM bank/routing/non-reentry assumptions remain explicit.

The broad maximal check preserves the occupied 4,047 bytes at/above 0xc700 in 20 sessions; it does not claim a full 44,400-byte comparison in those 20 sessions. The work IRQ check preserves its full 37,170 bytes in 17 sessions. Separately, the new decoder proof preserves every occupied CODE byte in each exact enabled/control image in every accepted shard. The final audit/status text maintains this distinction. Reader 45-instruction/seven-mutant proof, CRT-to-main-only scope, 629 RGB/576 Combo/48 cache updater/15 IRQ order/256 selector cases and retained certificate provenance agree with the recorded evidence.

Default lookup costs add 42,260 instructions across 256 valid calls in generic C52. They are component-only measurements, not complete reset, CH555 milliseconds, an 11 ms comparison or ordinary keypress latency. Main, complete NVM/settings startup, durable storage, full configured regression and hardware behavior remain unproved. The oversized maximal image is diagnostic and cannot be installed.

## Exactly two further bounded passes and pause

Reviewed both external READMEs/results, event component shape/listing evidence and protocol extractor, and authenticated their relevant hashes. Pass1 tried one event-chain candidate: 12,288 matching bounded leaf traces and three killed mutants, but component CSEG 565 -> 627 (+62); even ideal full 58-byte wrapper removal leaves +4. It was rejected with no integration/full build. These leaf traces do not qualify the full feature/event/IRQ system. Pass2 produced no eligible substantial candidate, patch or compile. The 42-byte/ideal 28-byte ceiling applies only to its three identified zero-fill loops; it is not a global protocol bound. Current source and historical authenticated listing identities are kept distinct.

Both requested additional passes are complete. The only integrated gain is 201 bytes, below the approximate 0.5 KiB checkpoint. The recorded instruction to pause after closing this packet and preparing handoff agrees with the evidence. No global compression minimum or achieved full-feature goal is claimed. Root commit/push/handoff and the user's requested pause remain integration steps, not physical qualification.

## Post-review integration allowance

The following metadata-only actions do not invalidate this review: copy this report byte-for-byte into the audit as the final review record, rerun the already-reviewed collector to update its evidence-file list/measurements/current ledger with that exact copy, and perform a quick exact-copy/hash/JSON regeneration/diff check. This excludes any implementation, test, runner, substantive documentation, build or evidence alteration. Such an alteration needs fresh independent review. This allowance avoids a report/manifest self-hash cycle; the manifest below binds the reviewed tree before this review is copied into it.

## Reviewed pre-integration file SHA256 manifest

```text
b81ecb3171cd832f8bee7c6c16f89f85d220cf9947253d69e883b7c56c7cde44  audits/maximal-pass30-20261025/README.md
7ab096f432aa02437988d797a91fe568ca90cf95875c76d37158805753290f06  audits/maximal-pass30-20261025/collect.py
286eb3ab00f3ce59fc6a6ed2bd6964643bfe4511330afcfd16c998c838642c0e  audits/maximal-pass30-20261025/decoder-linked-README.md
3daff05a4284a03d32ed0a64c4c8e350a29ff354aa13ff65b9ca02d78170167c  audits/maximal-pass30-20261025/decoder-linked-SHA256SUMS
c331c5ed42e91f97e2c46ae4b809fab820e469a8273a62809cb1b88e7435d77f  audits/maximal-pass30-20261025/decoder-linked.json
115c2f5a1665613c7ff492c4ea72811ff1772ed38684964033975c474e795406  audits/maximal-pass30-20261025/external-evidence.json
b634f5cddd76cd9cc7b1be19e1cdd90d0ce0a2d987c771a5ecbd7b79b99586f9  audits/maximal-pass30-20261025/extra-pass1-event-SHA256SUMS
6dec65edb92248a9c0bc0713944b8e2f1690d65239cde10714b327901c918a0c  audits/maximal-pass30-20261025/extra-pass1-event.json
c64ebe11d002392aa2d6f7615481d34b15232d67fce177c1712be217c5260fe8  audits/maximal-pass30-20261025/extra-pass1-event.md
22f18a01cc9f56f07a12e1d1bceda9cffb7e473ba8ab95683d4ae6b6df8d5843  audits/maximal-pass30-20261025/extra-pass2-protocol.json
0e27a9b57b9edcd86f2bdd5c418dced7bcbb110a32927c4acfe3be72239eb1b8  audits/maximal-pass30-20261025/extra-pass2-protocol.md
59fe79a1ce8b870433251accb82bc69f38e5d3bb85a18beae4e006907a8de5de  audits/maximal-pass30-20261025/generation-fix.md
df3fed384cac67d52cee63c88989bfbd434c1c8298f05e0cbf12e192bb4074a1  audits/maximal-pass30-20261025/host-check-0.log
1d215a419f9c4bb7bdb060ea6abf359620babc2bb46411fe1e9d0cb8725e2f70  audits/maximal-pass30-20261025/host-check-1.log
b9b6eda927d94808c29c2a71f3b69decc097d8c19a928c75410380cf84d0aa4f  audits/maximal-pass30-20261025/host-check-2.log
1d819070d210d38ef860443bd5e32eb4cf5647fe5ed07f02cc4c10d1e4cbb7c1  audits/maximal-pass30-20261025/host-checks.json
945c961043a400058f62e1f3342161028490263eb9e650cf205bfa4e14145f1f  audits/maximal-pass30-20261025/implementation-review.md
a11ad89252456766c5876efecf41e0601fe25faf5a13e2cf5f5103432a7836d6  audits/maximal-pass30-20261025/initial-review.md
2488a123d616aaff74d977c5a533910fdd279c26967f5c06430b64dad5f6a022  audits/maximal-pass30-20261025/linked-checks.json
94a6c30ba3a4b1d18e6f11c4dc2394100b76bded7ddcc19c5cefc98a660a96a4  audits/maximal-pass30-20261025/maximal-context.json
388c545ec2f4eddff532a58517fc2d68c3b10e25dd77414e0b267776ceff92a7  audits/maximal-pass30-20261025/measurements.json
e670f521f3a0399342fc78fd0945f74ac76f207325bae612bb88f96a0775f4b9  audits/maximal-pass30-20261025/prototype-review.md
af92b32ade2a36e2629faa2341b25822026dd9ba6013d544b27cf12262bfabfe  audits/maximal-pass30-20261025/read-hook.json
ed86aeba450c92ee4c5554855f3a972158c1c1fb708a359cee38b5cbd5b41408  audits/maximal-pass30-20261025/source-context-review.md
c2ac955a1bdf0ef0422ea5fa112ff9f7e16bc493f6a7f091df7da396b64bd8be  audits/maximal-pass30-20261025/startup.json
c91d60ec3128c3e3ba8c97735dea0f01b43839b7302760ea38c6eac716725c7c  audits/maximal-pass30-20261025/translation-unit-checks.json
7dab7c524d5caa5141f5d89ca10c2f91fc291b5f406b27f169e10cdd990c7a85  audits/maximal-pass30-20261025/work-context-review.md
f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5  audits/maximal-pass30-20261025/work-context.json
f31c0458e2d5c356ac271ffc80b57a5e986b211f356f2491f6b983f1ce556590  audits/maximal-pass30-20261025/work-irq.json
b4e334105266dbc6a74d12b5477ee3710d2c9e920201a6a0f207fbec2761b557  audits/maximal-pass30-20261025/work-startup.json
1fe6ecd344672df7416754be29294530ffcca26a70d7af8320c68257762d7e5c  docs/MAXIMUM-FUNCTIONALITY-STATUS.md
33531bb04b6f24230079d2c77b916fe70969c64e76faae3ef76e4ed34bde8d2c  docs/STATUS.md
e821c5ba75ebf9fae356c218bda0b24d272b2e131a6981a516526c345c2a58cd  docs/maximal-current.json
f82a29d41cd5c14f0184b03a4100918db3f1454bc8eb66130d833017da5d1b21  docs/ru/MAXIMUM-FUNCTIONALITY-STATUS.md
d7d12cf9837ad597974baf963e532a5e725624db33b8c9766e0ef3515beebd45  docs/ru/STATUS.md
18cdd970195f1c1cd98e7d5468f1efee95560fd12fc85d29336c1e6f6c6755b6  qmk-8051-ak820/builddefs/common_rules.mk
e13800a1b9d149730579a56bb097c544630db0258bf36314bc6ac32630e73dd5  qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/keymap.c
37951e53e75862158899501303c487a893c32f0747622633cb5837f0a05f4ddf  qmk-8051-ak820/quantum/keymap_introspection.c
3e62d72deef20e0d40f9124fe097b3c8e4ff173e549d2ec3c909333c9fadc114  qmk-8051-ak820/util/ak820_default_keymap.py
c8e0217af804f9069f71ba87d2a03e657c0f88d532ab139e1c96ceb02c01872f  qmk-8051-ak820/util/build_ak820.py
8c69e07b8fea54103891cc1332ba0b5f79a3d5f10bc0bc62b7c7c6e1cf448b9a  tests/ak820_default_keymap/README.md
82993adac7a0d6b4bc08e3356cbabc8e51f58f623489fbee694be27decc85e81  tests/ak820_default_keymap/check_decoder.py
1e2d0904efd6b1fc209bd6f1b47f22b15f9a837022a1d5f8b87164db85928dde  tests/ak820_default_keymap/compile_tu.py
f00607127e111b42efbdf30d690cf8950f01d10dc344a0ad5ac454dc49a5183e  tests/ak820_default_keymap/linked.py
6eb0f821d489b1c09c4477beca950f6e06aea557c65dd7bac27cc11e192f3b1e  tests/ak820_default_keymap/test_generator.py
```
