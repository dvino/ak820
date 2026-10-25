# Classifier27 WORK context and persistent regression review

Result: PASS for consuming the fresh WORK bootstrap context in a transformed legal-window WORK diagnostic build. PASS for the persistent host regression. No blocking finding was identified. These decisions do not qualify the future transformed image, stack capacity, IRQ wrappers/nesting, installation, or hardware behavior.

Reviewed tree: cfd05a0f5d296cc692224038a747dabb6694041f plus the current USB classifier diff and tests/ak820_raw_classifier. No full build, firmware source edit, index edit, commit or device command was performed. The concurrent maximal transformed build and its outputs were excluded.

## WORK context

All 496 build-report source/toolchain entries and all 993 artifact entries match the current files. The report identifies profile work, CODE 37989, and parameter_spills=null. The pinned SDCC tools/runtime, fixed-map source hashes, all 79 certificate provenance paths and hashes, and all three protected whole compiler ASM modules were checked. The protected modules are board, timer and the entire USB module.

make_context_certificate was independently rerun into /tmp/classifier27-work-review-context.json; its parsed result exactly equals classifier27-work-bootstrap-context.json. validate_context passed against the original WORK compiler object tree, WORK DCE tree, current fixed-map sources and toolchains/sdcc-4.6.0. No maximal-profile or old baseline certificate was substituted.

The stack analyzer and startup checker were independently rerun with only external /tmp output files; each parsed result exactly equals its supplied WORK JSON. Root bounds are main 98, USB 5, timer 2, LED 2; every unresolved list is empty. Pre-main and main-entry bounds are 2; initial SP is 84; interrupt enables remain unchanged until main. The certificate retains application_irq_only=true, whole_image_qualified=false, hardware_qualified=false; whole_program_qualified remains false.

## Persistent host regression

The saved oracle function equals the original cfd05a0 USB function byte-for-byte. The runner extracts the live current function, all six current classifier assertions and complete enum blocks from the actual VIA/Vial/VialRGB headers. Missing function, unterminated function, missing assertions and missing required enum symbol were independently exercised and raised failures. Compilation failures and missing mutation anchors also terminate nonzero by inspection.

The test was executed with the isolated local Docker compiler image and networking disabled. PASS covers every 16,777,216 three-byte prefix. Each case compares against the original switch and checks all 32 candidate packet bytes for mutation. The source reads only the first three bytes; remaining bytes use a fixed sentinel pattern. This is exhaustive prefix behavior, not enumeration of all possible 32-byte packets.

Both tests compile and execute actual changed C candidates: removing the encoder-setter exclusion is detected at [254,4,0]; removing dynamic setter exclusions is detected at [254,13,2]. The mutants terminate at their first mismatch as intended. Successful runner JSON-lines are retained in classifier27-host-regression.jsonl. README accurately describes its command, offline dependencies and limits. This host result does not prove SDCC output or device behavior.

## Identities

- runner: `1d60ed63f08e487d88550e1e2cf1ecd59b34fe927a84d13adfb195f9e195bcbc`
- oracle: `589c796d84e0f95cbf84a24350b220e903de5639de8de3396d556d0a180982b4`
- USB source: `e72369aab695c9e9480de3fa7ca887343a84dfc48e68b44eaee510bfeeb91bd1`
- WORK context: `f351d4a52acea5c542ab8d76a2303842baccd88eca580755fc779c10bfdb91d5`
- WORK image: `343f3b336e0b130417b35c1c5330360549a91edad27797eec7b6b72c040b3c61`
- WORK map: `a24dece0841281d6d14647ec413e0695d90ab721f67cb2923fdb8bfd762df10b`

The prior frozen component/source review remains separate evidence. The next transformed legal-window WORK image requires fresh exact-image postlink, stack/startup and applicable IRQ/wrapper/storage checks. No final-image acceptance is granted here.
