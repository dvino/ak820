# Short-call build experiment

The optional `--short-calls` build step saves **239 CODE bytes** in the isolated
`full-mouse-auto-shift` image dated 2026-10-24. The final strict link uses
40,403 bytes and leaves 81 trailing main-window bytes and 16 low-window bytes.
This is development evidence. It does not approve a release or describe installed
firmware. No device commands were issued.

The [evidence summary](short-calls-20261024.json) records hashes and original
scratch paths. Its report copies and failed traces are retained in the
[isolated evidence index](compact-next-20261024/isolated-shortcalls/files.json).
The [final matrix](compact-next-20261024/matrix.json) is separate passing evidence;
its combined raw build archive contains the final ASM, REL, RST, linker trials,
NoICE symbols and complete per-site proof.

## Size and scope

| Item | Result |
| --- | ---: |
| Post-outline diagnostic preimage | 40,642 bytes |
| Final strict image | 40,403 bytes |
| Saved bytes | 239 |
| Initial candidates | 251 |
| Invalid sites restored after the first trial | 12 |
| Final ACALL instructions | 108 |
| Final AJMP instructions | 131 |
| Verified direct and relative control-flow edges | 4,464 |
| Computed-jump or PC-relative sections with uniform movement | 12 |
| XRAM allocation | 2,687 bytes |
| Allocated stack | 163 bytes |

The image includes the compact Mouse Keys and Auto Shift implementations, the
core changes, the event-entry wrapper and the Repeat range simplification. The
239-byte saving compares this exact post-outline preimage with its shortened
image. It is not an additive estimate from other profiles.

The implementation admits a fixed foreground module set and Quantum modules
other than `quantum/color.asm`, which contains inline assembly. It excludes
boot, flash, NVM, IRQ and USB control modules; outline calls and helper bodies;
whole functions containing computed jumps or PC-relative instructions; and
complex or literal transfer targets. Only baseline same-page sites are tried.
No switch recognizer broadens the scope.

## Build and verification

The flag is off by default. Both `util/build_ak820.py` and
`tools/configure_firmware.py build` accept `--short-calls`. The configurator
continues to require its ordinary profile checks. This example requests the
combined development profile:

```sh
python tools/configure_firmware.py build \
  --profile full-mouse-auto-shift --short-calls \
  --build-dir qmk-8051-ak820/.build/combined-shortcalls \
  --toolchain /path/to/sdcc-4.6.0 \
  --qmk-bin /path/to/qmk --python /path/to/build/python
```

The builder preserves the post-outline ASM and JSON in `shortcalls-input`.
Every trial starts from those same inputs and reassembles them. Diagnostic
layouts may use the 64 KiB address-space ceiling; they are never accepted as
firmware. Each independently invalid short transfer is permanently restored to
its original long form. The accepted image is linked again with the original
CODE and XRAM limits and checked against the original two CODE windows.

The final tree remains at `dce`, so existing validators use the final image and
listings. The original `dce-input` and outline manifest remain available. The
new `short-calls.json` binds the initial source snapshot, tool, baseline image
and symbols, selected source lines, iteration history,
final bytes, resolved targets and actual saving. The build report binds the imported validator sources and
final ASM, REL, RST, NoICE symbols and proof. Configurator inspection rechecks
the saved proof against those inputs and final image.

The independent checks cover exact source edits, listed instruction bytes
against IHX, unchanged instruction opcode and width, fixed nonrelocation bytes,
relative-branch condition bytes, decoded transfer destinations and uniform
movement of computed-jump or PC-relative sections. Symbolic immediate fields
remain assembler relocation fields; this is not a separate proof of every
unlisted data byte or peripheral effect. ACALL/AJMP target bits may move while
their opcode family and intended destination remain correct.

ASlink truncates map symbol names at 32 characters, including with its wide-map
option. The optional build therefore emits NoICE `.noi` symbols with complete
names and matches their addresses to CODE map entries. Missing or ambiguous
symbol evidence is a failure. Final NoICE output is hashed in the saved proof.
The page calculation uses the address after the two-byte instruction, including
at a 2 KiB boundary.

Failed diagnostic links are tolerated only for complete pinned ASlink 2 KiB
page-error blocks. A matching marker in a trial listing is filtered into a
temporary file only when it identifies a selected, independently invalid site.
The raw listing is retained. Baseline and final listing parsing remains strict.

## Results and review closure

The same final IHX, SHA256
`8873ebe29cea93673f44fa5c20adf8f5c372a73c70f1151da32b7c67671aad85`,
passes the following checks:

- Strict final link, original CODE/XRAM windows and configurator inspection.
- Fifteen short-call positive and negative unit controls.
- Nine build-input tests with the pinned compiler available.
- Exact outline integrity: 192 helpers and 1,403 replacement calls.
- Three emitted baseline CPU cases and 21 Mouse Keys cases.
- Twenty-seven Auto Shift cases, including two simultaneous Mouse Keys cases.
- Startup control-stack bound of two bytes.
- Existing linked feature, unlock, Tri Layer, guarded-erase IAP, RGB, bounded
  function, tapping and Combo suites in the retained aggregate run.

Independent review closed the imported decoder provenance gap, the late input
snapshot, the unbound final NoICE output and the unchanged-instruction opcode
check. Additional controls cover conditional-branch operands, existing short
opcode target bits and diagnostic-only warning filtering. Independent saved
proof validation and seven manifest-tamper controls pass. The
[review record](compact-next-20261024/review.md) links the final integrated evidence.

The first simultaneous movement fixture used matrix position `(1,4)`, which is
absent from the physical matrix mask. Its failed trace is retained. The corrected
fixture uses `(6,4)` and passes all 27 cases on the unchanged image.

The first aggregate runner entry incorrectly expected a `run.py` file in the new
unit-test directory. An intermediate correction used base-runner discovery.
Final integration instead restores the unchanged 28-suite base runner and
requires the new discovery suite in every profile's supplemental plan, with
empty and skipped run rejection. The isolated handoff JSON retains the
intermediate runner hash, not the final integration source identity.
The retained aggregate report remains failed: it also includes
three stale documentation language links in the isolated snapshot and the RGB
host LeakSanitizer environment failure. It is not qualification evidence for an
all-tests-passed claim.

LeakSanitizer cannot inspect `/proc/<pid>/task` in this environment. Final root
workers use `ASAN_OPTIONS=detect_leaks=0` while retaining AddressSanitizer and
UndefinedBehaviorSanitizer. Leak checking is therefore outside that result.
The isolated default-environment RGB attempt and its single confirming failure
remain recorded.

The runtime analyzer bounds the timer, USB and LED callbacks at two, six and two
bytes respectively. Main remains unresolved at an indirect dispatch and has no
proved whole-program bound. The allocated stack number is not a stack safety
proof. Physical USB, IAP, DMA, interrupt timing and keyboard behavior remain
untested by this experiment.

## Primary references

- [SDCC Compiler User Guide](https://sdcc.sourceforge.net/doc/sdccman.pdf):
  `--acall-ajmp` is limited to code within the same 2 KiB block.
- [Keil linker optimization](https://www.keil.com/support/docs/2297.htm):
  code arrangement can increase the use of ACALL and AJMP.
- [Keil page-boundary warning](https://www.keil.com/support/docs/178.htm):
  moving modules can make a short transfer reach the wrong page.
- [ACALL instruction definition](https://www.keil.com/support/man/docs/a51/a51_acall.htm):
  the page comes from the incremented program counter.
