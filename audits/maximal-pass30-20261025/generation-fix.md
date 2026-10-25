# Default-keymap generation corrections

Bounded source correction only. No full firmware build, Git mutation, network or hardware operation.

The private extraction macro is rejected in incoming define/undefine arguments, including zero-valued and split definitions. Final assembly is independently parsed: original keymaps and bootstrap metadata must be absent, and class/payload/offset byte arrays must exactly match the bootstrap encoding. An indirect forced-include definition therefore fails closed.

Both compiler dependency closures are discovered separately. Normal source and existing generated .build headers are frozen before bootstrap; the newly generated include is explicitly frozen after creation. Final dependency discovery and actual final compile must have identical closures. Every final dependency hash and every bootstrap dependency hash is checked after compilation. Final-only generated headers cannot inherit the outer build directory exemption. The report preserves existing bootstrap fields and adds final closure hashes, command, dependency digest, phase-only paths and the generated-include difference.

Validation: seven generator tests PASS. Offline exact-flag one-TU suite PASS at `.build/default30-tu-fix-final`: clean compile, stale include replacement, option-off original defaults, identical encoder/LED bytes, indirect extraction-phase rejection with failed artifact removal, and final-only generated .build header mutation immediately after discovery rejected. The final successful rerun restores current include/object/report after negative tests. The earlier `.build/default30-tu-fix-generated` run was invalidated by an intentional writer edit while it was running; the generator hash guard rejected it. It is not qualifying evidence.

Environment: cached image ak820-nkro-study-env:local, sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d; Docker --network=none --userns=host --user 1001:1001; parent directory bind at same absolute path. Interpreter /tmp/buildenv/bin/python. Compiler toolchains/sdcc-4.6.0/bin/sdcc. Flags qmk-8051-ak820/.build/resume29-getter-bounds/obj_ajazz_ak820_vial/cflags.txt. Test command: tests/ak820_default_keymap/compile_tu.py --flags FLAGS --compiler COMPILER --output qmk-8051-ak820/.build/default30-tu-fix-final.

No decoder or runtime source changed in this correction. The earlier integrated decoder 16,777,216-case ASan/UBSan result remains applicable to that unchanged decoder; it was not repeated for wrapper-only provenance checks. Full image, linked stack/interrupt and runtime/hardware qualification remain root-owned. Fresh independent review required; no self-approval.

Frozen files:

- `qmk-8051-ak820/util/ak820_default_keymap.py`: `3e62d72deef20e0d40f9124fe097b3c8e4ff173e549d2ec3c909333c9fadc114`
- `tests/ak820_default_keymap/test_generator.py`: `6eb0f821d489b1c09c4477beca950f6e06aea557c65dd7bac27cc11e192f3b1e`
- `tests/ak820_default_keymap/compile_tu.py`: `1e2d0904efd6b1fc209bd6f1b47f22b15f9a837022a1d5f8b87164db85928dde`
- `tests/ak820_default_keymap/README.md`: `04e359f7b63adf1cc13f762d0e7c8dec083e14891527bfedcce35cf7375f2a21`

Successful generation report SHA256: `507035ffdd59103c849b74817f1932733c4b99485c1175b048f38128b85b966f`. Final table verification: True.
