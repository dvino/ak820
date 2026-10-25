# Default keymap integration review

Result: findings; no approval for full measurement. Review was read-only and performed before a source freeze. No firmware build, Make dry run, linked-image qualification, hardware access or source edits were performed.

Reviewed base: `bb91d897748fac8ba3363887fa4af5c3a3a926c6`. Only the default compression integration and its tests were examined.

## Findings

1. **Private extraction mode can override the final compilation.** `compile_current()` copies the original compiler arguments to both phases and appends `AK820_DEFAULT_KEYMAP_EXTRACT` only for the bootstrap. If the caller already supplies `-DAK820_DEFAULT_KEYMAP_EXTRACT` through extra flags (or an included configuration header defines it), the final compilation also takes the extraction branch. The original 512-byte keymap and metadata then remain, while the generated compressed include is unused. No check rejects that command or checks the final ASM representation. This violates the two-phase contract and the requirement that unsupported configurations fail closed. Reject reserved extraction controls and verify the final representation before accepting the output; flag screening alone cannot catch an indirect header definition.

2. **Final dependency closure is not checked by the wrapper.** The wrapper discovers and rechecks the bootstrap dependency set, then verifies only those paths after final compilation. The final dependency file is produced but is neither compared nor independently snapshotted/verified. `AK820_DEFAULT_KEYMAP_EXTRACT` changes preprocessing, so final-only headers can exist. The generated include is an intentional difference, but any other final-only input requires explicit verification. The full builder checks ordinary final source dependencies against its build-start snapshot; however generated files beneath the build directory are exempt in `collect_inputs()`. Thus final-only generated headers are a concrete gap in the requested source-change-during-compilation gate. Establish the final closure before compiling and verify it, allowing only the explicitly generated include with its known digest.

## Static observations

The Make recipe resets `CC_EXEC` from `CC` for each object; wrapping introspection does not persist into later C objects. The wrapper receives the full compiler argument list. The forced introspection prerequisite causes regeneration for incremental compiles, and the generated include is replaced atomically. The bootstrap assembly is outside the object manifest and is never linked by this integration.

The strict CONST parser rejects expressions, symbols, wrong sections, duplicate symbols and wrong dimensions. The codec uses 64 class bytes and 32 row offsets; it rejects payloads above 255 bytes and validates a round trip. For the supported 16 by 8 by 2 layout, decoder indexing and byte offsets remain bounded. Invalid uint8 coordinates return KC_TRNS, and the raw count remains two. The implementation changes only the VIA raw default lookup path; non-VIA lookup retains its original path. Encoder, LED, NVM, wire and protected-module behavior were not newly qualified by this review.

## Executed check

`python3 -m unittest discover -s tests/ak820_default_keymap -p 'test_*.py' -v`: five tests passed (0.052 seconds). These are generator/parser tests, not a linked-image, stack, interrupt, timing, CPU-emulator or physical acceptance result. The one-TU and decoder harnesses were inspected but not executed.

## Reviewed file hashes

```text
18cdd970195f1c1cd98e7d5468f1efee95560fd12fc85d29336c1e6f6c6755b6  qmk-8051-ak820/builddefs/common_rules.mk
e13800a1b9d149730579a56bb097c544630db0258bf36314bc6ac32630e73dd5  qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/keymap.c
37951e53e75862158899501303c487a893c32f0747622633cb5837f0a05f4ddf  qmk-8051-ak820/quantum/keymap_introspection.c
c8e0217af804f9069f71ba87d2a03e657c0f88d532ab139e1c96ceb02c01872f  qmk-8051-ak820/util/build_ak820.py
67e6b68be83cda48be83a03dd9883453c6fe1ee4d38605bca87ac68c65162ac3  qmk-8051-ak820/util/ak820_default_keymap.py
82993adac7a0d6b4bc08e3356cbabc8e51f58f623489fbee694be27decc85e81  tests/ak820_default_keymap/check_decoder.py
604a9aca027646c09647c5797450e23b785320ce4df4d81e0fe5d0cdedaedb6f  tests/ak820_default_keymap/compile_tu.py
d9b8da6ba767415c87c58e96902091fa8a67a4ffb30393c99c0c5d247e6d1132  tests/ak820_default_keymap/test_generator.py
c070f767a39a92a216686818df625aa6bddc96e9c35911c51d76eafd48abbf8f  tests/ak820_default_keymap/README.md
```

Substantive corrections require a fresh writer and fresh independent review. After implementation closure, the exact full image still requires current stack/interrupt and post-link checks, protected-context equivalence where reused, and regression evidence. Component savings and native decoder equality do not establish full-image savings or latency acceptance.
