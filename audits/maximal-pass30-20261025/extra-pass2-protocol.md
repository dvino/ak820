# Common protocol path: bounded rejection

Result: no eligible weighty variant in this pass. No patch or protocol engine was created. The existing typed bulk-read path, grouped VIA buffer-command decoding, single reply path, classifier27, firewall28 and getter29 were retained. No repository file, build output, device, network or Git state was changed.

Reproduce the evidence extraction:

```sh
python /home/danil/ChatGPT/ak820-bounded-final-passes-20261025/pass2-protocol/run.py
```

`results.json` records source hashes, listing hashes, exact image29 instruction counts and static incoming direct-call counts. All six inspected current protocol/backend files match the frozen `19a9d53` source byte for byte. The image29 IHX identity is `693fdcd928f2d84b32e19b858cdd6cce29b46d01ea5694403788da08bf3969f9`. Costs below describe that authenticated image, not a newly built maximal/work image. Static call counts exclude tail jumps and indirect calls and do not describe execution frequency.

| Surface | Listed instruction bytes | Incoming direct calls | Decision |
|---|---:|---:|---|
| VIA receive | 1271 | 1 | Four bulk commands already share offset/size decoding. Macro write has unlock, backend result and silent-return rules; keymap write has a separate keycode firewall. |
| Vial handler | 1222 | 1 | Largest parser body, but command payloads, response mutation and reload rules differ. Its 371 affected pattern bytes are overlapping instruction categories, not removable bytes. |
| Common dynamic read | 180 | 0 | Already shared through wrapper tail transfers. Keep backend chunk, zero-fill and API width. |
| Keymap/macro read wrappers | 55 / 76 | 1 / 1 | Different base/limit and macro used-length lookup remain necessary. |
| Raw NVM reply gate | 63 | 0 | Already one shared flush and fault gate. |
| Request fault classifier | 161 | 1 | Already optimized in classifier27. It classifies the original request before response mutation, unlike dispatch. |
| NVM begin/end | 21 / 24 | 5 / 6 | Already shared; call multiplicity is not duplicated function bodies. |

The remaining concrete repeated parser operation is the three dynamic-entry getter zero-fill loops in Vial. Each is 14 instruction bytes at `0xc6d6..0xc6e3`, `0xc71c..0xc729` and `0xc7a0..0xc7ad`. All already call the same outlined byte-store helper. Their total inline cost is 42 bytes. Even free reuse of one loop could remove at most 28 of those inline bytes before new calls, register/ABI preservation, routing, decoder or table costs. This is a bound for these loops only, not for every conceivable parser rewrite. It is too small to qualify as a weighty variant; no table/decoder prototype was pursued. The surrounding getters still need distinct backend calls and must save the index before clearing its packet byte. Getter29 already removed the larger temporary-entry copies.

USB control setup validates USB transaction stages and buffer ownership. VIA/Vial handlers validate public command boundaries, unlock admission and command fields. These are different predicates with different rejection/reply behavior. Combining their names or their total function sizes does not identify removable repeated work. Removing Vial's public length check would change its direct-call contract. NVM fault classification cannot replace admission because classification runs before packet mutation and only decides whether a reply may survive a fault. Diagnostic requests deliberately bypass flush/batching; they cannot use the normal reply gate without a behavior change. Macro upload is transactional, while keymap writes validate partial keycode pairs. A common setter selected from a metadata table would still need these paths and has no demonstrated large duplicated body to remove.

No candidate was compiled: component baseline/candidate costs, finite-domain differential tests, storage/order mocks and mutants are not applicable to a rejection without a patch. No saving, speed improvement or new acceptance is claimed. All optional features, six layers, 16 macros/8192 bytes, eight entries per Combo/Tap Dance/Key Override, both encoder directions and unsupported-command behavior remain untouched. Full functional regression, exact-image stack/IRQ, USB, durable storage and physical acceptance gates remain open. This pass is complete and stops here.
