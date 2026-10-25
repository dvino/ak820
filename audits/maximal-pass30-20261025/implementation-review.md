# Corrected default-keymap implementation review

Result: CLEAN for the corrected source and one-translation-unit eligibility only. Both initial P2 findings are closed. No new actionable finding was identified in the reviewed scope. This is independent review, not author approval, commit approval or linked-image acceptance.

Base HEAD: bb91d897748fac8ba3363887fa4af5c3a3a926c6, with the frozen dirty default compression implementation. Source was mounted read-only during compiler checks. No repository, Git, hardware or network mutation occurred. Review output is external to the repository.

## Finding closure

1. Private extraction controls: reject_phase_overrides rejects direct define/undefine controls, including split arguments and zero values. Crucially verify_final parses actual final CONST CODE arrays, demands exact bootstrap-derived classes/payload/offsets and rejects original keymaps or metadata allocations. An indirectly forced header definition therefore fails after compilation; object/rel/include are removed. The independent actual SDCC rerun exercised this indirect bypass and observed rejection and failed-artifact cleanup.

2. Final dependency closure: normal inputs and existing generated .build h/inc files are frozen before bootstrap. Bootstrap discovery and compile closures must match. Final discovery uses the final preprocessing phase, its dependencies must match the final compile closure, and every final path is checked against the preexisting snapshot plus the explicitly generated include digest. Bootstrap inputs and generator/compiler hashes are rechecked too. A newly discovered final-only generated header cannot inherit collect_inputs' outer build-directory exemption. The independent race rerun changed a real final-only header immediately after final dependency discovery and observed the intended Source changed during final compilation error plus object/include cleanup. To retain source read-only, this rerun used an external fixture header and supplied its initial digest through the input_snapshot test seam; the source .build header enumeration was inspected rather than written. The unchanged checked-in compile_tu race test additionally covers the actual .build fixture path; its writer result remains separately reported evidence.

## Independent executed evidence

- Seven generator/parser unit tests passed (0.057 s).
- Pinned cached container sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d, network none, userns host, uid/gid 1001, repository RO and external output RW.
- Real SDCC 4.6.0 compilation used the exact resume29-getter-bounds cflags.txt. Clean compressed compile, poisoned include replacement, option-off original 512-byte table equality, exact encoder-map and LED-point byte equality, indirect extraction rejection and final-only dependency race rejection passed. A successful clean generation restored current final object/include/report after negative tests.
- Script and full output: default30-independent-tu/rerun.py and rerun.log. Initial attempt used an incorrect toolchain path and failed before compilation; corrected actual compiler is repository-root toolchains/sdcc-4.6.0/bin/sdcc. The successful rerun is the qualifying evidence.

## Integration and limits

Make's explicit introspection prerequisites combine with its existing pattern recipe; the phony prerequisite forces regeneration on incremental builds. The include has a no-op bootstrap target for dependency-file remaking, while the introspection recipe regenerates it atomically before final compilation. CC_EXEC is reset from CC for each C object, so the Python wrapper does not leak into subsequent objects. Bootstrap assembly is outside the object ASM manifest and is never linked by this integration. No Make execution or full build was performed in this review; the root-owned full build must confirm those paths in practice.

The strict parser, dimensions/NO/TRNS/literal requirements, bounded decoder and original option-off path were inspected. Encoder/LED exact TU bytes were compared; dynamic layers, NVM/wire format and ordinary VIA read path are unchanged by these files. This does not newly qualify their runtime behavior. Compression is guarded by VIA/SDCC/model and the supported target in Make/builder. No claim of full-image 201-byte gain follows from the component prototype.

Linked image size, full feature preservation, exact-image stack/interrupt bounds, all regression gates, reset timing, hardware and installed state remain unqualified here. The decoder sanitizer exhaustive test was inspected but not rerun because its implementation did not change in these corrections. Final packet documentation and exact full-build evidence still require fresh independent review before commit. README in the test scope agrees with the corrected source; repository-wide final status documents were outside this bounded pre-build review.

## Reviewed source hashes

```text
18cdd970195f1c1cd98e7d5468f1efee95560fd12fc85d29336c1e6f6c6755b6  qmk-8051-ak820/builddefs/common_rules.mk
e13800a1b9d149730579a56bb097c544630db0258bf36314bc6ac32630e73dd5  qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/keymap.c
37951e53e75862158899501303c487a893c32f0747622633cb5837f0a05f4ddf  qmk-8051-ak820/quantum/keymap_introspection.c
c8e0217af804f9069f71ba87d2a03e657c0f88d532ab139e1c96ceb02c01872f  qmk-8051-ak820/util/build_ak820.py
3e62d72deef20e0d40f9124fe097b3c8e4ff173e549d2ec3c909333c9fadc114  qmk-8051-ak820/util/ak820_default_keymap.py
6eb0f821d489b1c09c4477beca950f6e06aea557c65dd7bac27cc11e192f3b1e  tests/ak820_default_keymap/test_generator.py
1e2d0904efd6b1fc209bd6f1b47f22b15f9a837022a1d5f8b87164db85928dde  tests/ak820_default_keymap/compile_tu.py
82993adac7a0d6b4bc08e3356cbabc8e51f58f623489fbee694be27decc85e81  tests/ak820_default_keymap/check_decoder.py
04e359f7b63adf1cc13f762d0e7c8dec083e14891527bfedcce35cf7375f2a21  tests/ak820_default_keymap/README.md
```
