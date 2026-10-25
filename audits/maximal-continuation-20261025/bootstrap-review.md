# Bootstrap IRQ source-context review

Date: 2026-10-25. Scope: independent read-only review of the fresh bootstrap and its generated parameter-spills certificate. Repository HEAD: `09330ab708e1eb3671571f63894c583e01743eef`. No source changes or builds were performed during review.

## Decision

Approved for reuse solely as the source-context input to a bounded diagnostic parameter-spills build with the same protected IRQ compiler assembly, toolchain/runtime and reserved-memory map. No blocking integrity or provenance finding was found in this certificate. This decision does not qualify the bootstrap or a later transformed image for installation, full regression acceptance or hardware use. Any diagnostic output still needs its own exact-image startup, foreground, interrupt and stack checks before full regression work.

## Evidence checked

- `parameter-spills-context.json` SHA256: `5ef9515da0e78550a824626a42110b9579c1d6360b7a49c56fbb3e28ddb4e851`.
- All 83 certificate provenance entries exist and match their recorded SHA256, including the linked IHX, map, build report, stack report and all linked listings.
- The actual linked IHX SHA256 is `42578da9c4a99c8261f4800f6a8c2340f8288c3c7d25afb0c310db48f746b544`; the map SHA256 is `c92ddc571f06062c91f114d73b61b8f69a59ab5b35b87d2c357b246f24f67fc0`.
- The bootstrap report records maximal configuration, SDCC 4.6.0 #16555, 45,847 CODE bytes, code upper endpoint 65,536, keymap words and read-block assembly enabled, short calls, tail sharing, register-save trimming and outlining limit 400. Parameter-spills trimming and IRAM overlay are disabled. The report records 212 outline helpers.
- All 473 source manifest entries and 22 toolchain entries match current file bytes. The certificate's actual compiler, preprocessor, assembler, linker and six large-model runtime libraries match the toolchain at `ak820-max/toolchains/sdcc-4.6.0`.
- The current builder SHA256 matches the report exactly: `a514203ba0285d98b8f75b2984cef757acb9e44c0debe671be5ac0479679d938`.
- Stack and startup reports have identical exact-image identities. Current analyzer, decoder and startup checker bytes match their recorded hashes. Stack roots are foreground 103, USB 5, timer 2 and LED 2, with no unresolved paths in those reports. Startup records pre-main control bound 2, main-entry frame bound 2 and unchanged interrupt enables until main.
- Independently collected listing addresses cover all 1,875 reachable application IRQ instruction addresses. Their complete module set is exactly `ak820_board.asm`, `ak820_timer.asm` and `protocol/ch555/usb_ak820.asm`. All three original compiler-assembly canonical hashes equal the certificate. The reserved-map source hashes also match.
- The existing `validate_context` succeeds against the actual bootstrap object directory and DCE tree. Fresh generation through unchanged `make_context_certificate` produces an object identical to the supplied certificate. No certificate hashes were manually changed. A temporary negative fixture with a changed stack-report provenance digest is rejected.

## Limits and provenance interpretation

The certificate is a newly generated source lock derived from `.build/resume22-bootstrap-read-on-b`. It is not recovery of the missing external20 or external22 artifacts. None of its provenance entries identifies either missing packet; those packets remain unavailable. Earlier external evidence cannot be claimed from this review.

The certificate explicitly sets `application_irq_only=true`, `whole_image_qualified=false` and `hardware_qualified=false`. Whole-module assembly protection is stronger than locking individual IRQ instructions, but it remains a prelink source-context check. It does not transfer foreground stack acceptance to the parameter-spills output, prove interrupt wrapper behavior on hardware or establish a combined full-image stack bound. The stored bounds are reported as static analysis evidence only. No USB commands, hardware operations or full regression suites were run.
