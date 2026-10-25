# Bootstrap 27 context review

Decision: PASS for research reuse of the relocated private-formal context certificate only. No blocking finding was found within this scope.

Reviewed source: `ak820-max`, HEAD `cfd05a0f5d296cc692224038a747dabb6694041f`, branch `optimize/resume-pass26b-20261025`. The working tree was clean during review. The review did not change source, certificates or build outputs. No device commands or full builds were run.

## Identity and provenance

- `RESTORE-VERIFICATION.json` records 65,584 verified files / 3,285,243,699 bytes, matching archive and staged index entries, zero content mismatches and no errors. It records 82 safe-tar Git-object permission normalizations; these are not content mismatches. This review inspected that receipt rather than repeating the complete archive verification.
- All 496 build inputs (474 source inputs and 22 toolchain inputs) and all 1,058 build artifacts matched their current SHA256 values. The build reports SDCC 4.6.0 #16555, maximal configuration, CODE 45,303 and `parameter_spills: null`; no parameter trimming was used for this baseline.
- All 84 certificate provenance entries matched current files. All 10 selected compiler/linker/runtime hashes and all three reserved-map source hashes matched. Ordinary XRAM is [0x0440,0x1000); reservations are [0x0200,0x0400), [0x0400,0x0440), [0x1000,0x1400). The assembly absolute-allocation check accepted exactly the LED DMA and flash-stage aliases.
- All three complete protected compiler-assembly modules matched their canonical hashes: `ak820_board.asm`, `ak820_timer.asm`, `protocol/ch555/usb_ak820.asm`. `validate_context` passed against the current original object tree and DCE assembly.
- Regenerating the certificate into a temporary external directory produced an exactly equal JSON object, including protected-module selection and all provenance entries.
- Stack and startup reports matched the current IHX, MAP and every one of 80 linked listings. Analyzer, decoder and startup-checker source hashes matched current source. Independently rerunning both analyzers into temporary external files returned exit 0 and exactly reproduced both JSON objects.

## Contract and limits

Application roots have no unresolved paths: `_main` 103 bytes, USB IRQ 5, timer IRQ 2, LED IRQ 2. Root entry return addresses are excluded by the analyzer contract. Startup independently reports a 2-byte pre-main/main-entry frame bound, initial SP 88 (0x58), and unchanged interrupt enables until main.

The certificate gates the target, format, valid-C private-formal contract, all three application IRQ roots, map, tools, provenance and complete protected modules. Preparation rejects changed protected modules and excludes them from transformations. The certificate remains application-IRQ-only with `whole_image_qualified: false` and `hardware_qualified: false`. Its reuse does not qualify a new linked image: that image still requires its own postlink audit and exact-image stack/startup/IRQ-wrapper/nesting/capacity checks. Valid C accesses, normal large-model ABI and private unescaped nonvolatile objects remain prerequisites. OEM interrupt wrappers, physical behavior and installation are not accepted by this review.

Certificate SHA256: `7c104353864c2613bb31adcbf6c860ba1728cb41ade82c8bc297ef9324c8b9b0`.
