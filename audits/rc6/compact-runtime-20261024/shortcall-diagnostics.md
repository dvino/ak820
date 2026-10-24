# Short-call linker diagnostics — 2026-10-24

The short-call pass now restores an authenticated linker-rejected candidate to
its original long transfer even when independent decoding finds valid bytes.
It then links a fresh tree from immutable input. Encoding-rejected sites and
linker-rejected sites are recorded separately in each iteration; their union
is removed. Baseline and final listing checks remain strict.

## Reproduced failure

The previous implementation was run against the saved
`qmk-8051-ak820/.build/runtime-macro-cursor` baseline and iteration 0 artifacts.
It raised `ValueError: Diagnostic page marker at independently valid site`.
The site was `quantum/keyboard.asm:776`, function `keyboard_setup`, originally
`lcall _print_set_sendchar`. The trial had address `0x97ff`, bytes `b1 26`, and
symbol address `0x9d26`. The architectural PC after the two-byte instruction
is `0x9801`, so the encoded target is correctly `0x9d26`.

A two-module fixture assembled and linked with pinned SDCC 4.6.0 reproduces
ASlink's warning at both `0x97fe` and `0x97ff` with target `0x9d26`. Both
encodings decode correctly using PC+2. This records observed linker behavior;
no claim about its internal relocation criterion is required by the fix.

## Authentication and checks

Only the exact recognized page marker immediately before a selected short
transfer can be admitted in a trial. The marker symbol, when present, must
match. The candidate must match the instruction kind, operand, function and
original source hash. Listing bytes must match IHX bytes. Unknown or malformed
markers, stale source, unexpected targets and changed image bytes fail.
Final authentication still rejects every page marker.

`python3 -m unittest discover -s tests/ak820_shortcalls -v` passed all 16 tests,
including the real linker fixture, independently valid candidate removal,
immutable long-transfer restoration and a second link, strict final marker
rejection, wrong symbols, malformed markers, stale source and corrupt bytes.
The real-linker fixture uses `AK820_SDCC_BIN` when supplied and otherwise uses
the checkout's default toolchain. Both tool hashes are checked against the
central `SDCC46_PINS` table. An explicitly configured missing or wrong tool
fails rather than skips. Profile suites receive the already validated
`toolchain/bin` through a scoped subprocess environment; the parent environment
is unchanged. All 16 tests also passed with zero skips using an external
temporary tool directory. The 24 configuration tests passed, including the
custom tool-directory propagation and parent-environment contract. The saved
final image was revalidated after this test-only correction; no firmware
rebuild was required.

## Full source build

The following command completed in `qmk-8051-ak820`:

```sh
python3 util/build_ak820.py --profile full-mouse-auto-shift --short-calls \
  --toolchain ../toolchains/sdcc-4.6.0 --qmk-bin .venv/bin/qmk \
  --build-dir .build/shortcall-diagnostic-fix
```

Iteration 0 selected 252 candidates. Independent decoding rejected 18 sites;
ASlink rejected 19, including the valid boundary site above. Their union was
19. Iteration 1 selected 233, had no encoding or linker rejections and returned
link exit code 0. The final strict build passed and saved 233 occupied bytes.
It contains 40,382 occupied CODE bytes and ends at `0xc699`.
The saved manifest independently revalidated all 233 sites, 4,448 control-flow
edges and 12 uniformly relocated hazard sections through `validate_saved()`.

Final image: `.build/shortcall-diagnostic-fix/ajazz_ak820_vial.ihx`.
SHA256: `c6f33d09845b4a4b1d2acde8c9b2a105f70618bbe81bd411fd7e6ee23a297150`.
The complete iteration records are in that build's `short-calls.json`.
Both the original failing tree and corrected reproduction are retained in
`shortcall-builds.tar.xz`; paths inside them record the original scratch build.

These are offline source, assembler, linker and byte-level checks. No device
commands were sent and no physical keyboard behavior was tested.
