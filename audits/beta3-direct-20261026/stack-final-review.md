# Final stack recognizer review

## Result

The narrow outlined-multiplication change is accepted for source freeze and fresh final builds. No blocking finding was identified. This review covers `tests/ak820_stack/analyze.py`, its focused tests and `mmo-stack-dispatch.md`; it does not qualify firmware runtime or hardware behavior.

## Exact-image evidence

The immutable MMO image at `/tmp/ak820-beta3-isolated/a/qmk-8051-ak820/.build/beta3-qualified/mmo/ajazz_ak820_vial.ihx` has SHA256 `963aff70931a3ac4530fa8a8fd9f2dd4ad43125c3dce963ce1c8a7cce3009821`. Loading its linked listings and IHX independently confirms bytes `75 F0 02 A4 22` at `0x5210`: `MOV B,#2; MUL AB; RET`.

The recognized dispatch starts at `0xA35A`; `0xA386` identifies its multiplication call site. The evidence note uses the latter address in its description of the dispatch call. The accepted proof includes helper instruction addresses `0x5210`, `0x5213` and `0x5214`, ten ROM callback targets, getter peak 1 and multiplication peak 2.

Running the current analyzer independently against that unchanged image produces foreground bound 102 and application IRQ bounds 2, 5 and 2, with no unresolved paths. Output: `/tmp/ak820-mmo-stack-independent-review.json`. `whole_program_qualified` remains false, correctly leaving startup, wrappers, nesting, storage contracts and final runtime qualification to their existing gates.

## Code and negative controls

Only logical rows 24 and 25 may be replaced by the outlined call. The recognizer checks the complete exact leaf, including RET, through instruction-boundary-aware reads. Normalization preserves subsequent physical addresses and branch destinations; the synthetic multiplication row introduces no accepted branch target. All existing register identities, nonzero/range guards, modifier getter restrictions, private spill provenance, ROM completeness and invocation-helper checks remain required.

The call adds a two-byte return frame before the callback pointer pushes. The leaf has no stack operation or child call, so peak 2 and zero residual height are sufficient. Its instructions are included in reachability for later interference checks. Callback frames, getter frames and continuation heights remain unchanged.

Independent command: `python3 -m unittest discover -s qmk-8051-ak820/tests/ak820_stack -p test_analyze.py`. All 33 tests pass. Added controls reject changed multiplier, changed multiply opcode, changed/missing RET, absent spill provenance, changed guard/XOR/invocation and missing ROM bytes. Existing inline success and structural rejection controls remain active. The helper mutation fixtures deliberately change instruction rows independently of code bytes; this still directly exercises exact-body rejection, while the production loader additionally enforces listing/IHX agreement.

## Build provenance

Fresh final builds are required for every profile. `util/build_ak820.py` records the analyzer among parameter-spill proof sources and rejects mutation during a build. `tools/configure_firmware.py::inspect` calls `validate_inputs`, so old final manifests cannot qualify the changed analyzer.

Unchanged bootstrap context certificates can be reused only after the existing `ak820_parameter_spills.validate_context` succeeds. That function validates certificate shape, tool and reserved-map hashes, immutable provenance files, protected compiler ASM and the absolute map contract. It does not compare the bootstrap source manifest with the current analyzer. No certificate, manifest or report should be rewritten manually to bypass these checks.

No implementation, firmware, certificate or failed build artifact was changed by this review. Only this report was written.
