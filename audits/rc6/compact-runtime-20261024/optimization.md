# Smaller encoder and mouse event setup

These changes preserve the existing firmware features and NVM schema. The
combined `full-mouse-auto-shift` image uses 40,231 occupied CODE bytes with
verified short transfers, 172 fewer than the reproduced baseline. Allocated
XRAM falls from 2,687 to 2,655 bytes. Stack allocation remains 163 bytes. The same source also fits without short
transfers: 40,449 occupied CODE bytes, with 35 main trailing bytes and 16 low
trailing bytes. The previous combined source required short transfers to fit.
This is an offline development image. No device command was issued, and the
published and installed alpha.3 firmware is unchanged.

## Changes

The AK820 encoder path constructs one six-byte event instead of four separate
CW/CCW press/release objects. Row and event type are selected once. The existing
shared action wrapper snapshots the event, so processing the press cannot
change the source object. Release reads the timer again and clears `pressed`.
Both existing delays remain. Other boards keep the original path.

Mouse Keys cancel each opposing pair once before constructing the report.
The shared axis helper then needs only the selected pair, rather than three
large-model arguments at every call. Wheel Y keeps its existing negative-bit
priority even for arbitrary held/selected combinations. Cadence, movement
size, endpoint backpressure, button retry and report layout are unchanged.

The numeric-string helpers retain their public API, separate buffers, cache
and initial cache sentinels. Removing explicit zero initializers from the two
buffers and padding bytes preserves C's implicit static zero initialization.
The existing CRT clears XSEG. SDCC no longer emits redundant explicit GSINIT
stores, and dead-code elimination can remove these twelve unused XRAM bytes
in this profile. The nonzero cache sentinel initialization remains.

## Measurements

Every row uses SDCC 4.6.0, the existing outlining and baseline callee-save
list, and the `full-mouse-auto-shift` profile. The preimage column is the exact
occupied CODE in the immutable post-outline image before short transfers.
Changes in outlining and page placement mean isolated savings are not additive.

| Source | Preimage CODE | Final CODE | Allocated XRAM | Result |
| --- | ---: | ---: | ---: | --- |
| Baseline `06b8f0f` | 40,642 | 40,403 | 2,687 | Control reproduced |
| One encoder event | 40,532 | 40,306 | 2,669 | Retained |
| Encoder and first mouse form | 40,492 | 40,274 | 2,667 | Wheel priority corrected below |
| Encoder and corrected mouse | 40,498 | — | — | Short-transfer diagnostic rejected |
| Encoder, corrected mouse and implicit zeros | 40,449 | 40,231 | 2,655 | Accepted candidate |
| Candidate without short transfers | 40,449 | 40,449 | 2,655 | Strict build passed |
| Candidate plus broad callee-save trial | 41,311 | — | — | Final memory bounds rejected |
| Candidate plus small callee-save trial | 40,507 | 40,281 | — | Larger than candidate; rejected |

The accepted candidate shortens 218 transfers. Its main window has 253
trailing bytes and its low window has 16. The windows remain separate. Its
IHX SHA256 is
`1e278dcf536ee96195b765ea2f2ff8808108ecfd15d6fb9e8d82cc2e51f81d75`.
The reproduced control hash is
`8873ebe29cea93673f44fa5c20adf8f5c372a73c70f1151da32b7c67671aad85`.

## Verification

The accepted exact short-transfer image passed these targeted checks:

| Check | Coverage |
| --- | --- |
| `ak820_compiler/linked.py` | Eight matrix/action/encoder observations; both encoder directions; press and release identity/Boolean bytes; later release timer value |
| `ak820_core_compact/linked.py` | 280 event-copy ABI cases |
| `ak820_emitted/run.py` | Three existing emitted scenarios |
| `ak820_mousekeys/run.py` | 21 existing linked Mouse Keys scenarios |
| `ak820_mousekeys/host.py` | Existing host scenarios plus all 65,536 held/selected pairs against the former axis rules; ASan/UBSan with leak detection disabled |

The exact image without short transfers also passed the eight compiler
observations, 280 event-copy cases and 21 linked Mouse Keys scenarios. Its IHX
SHA256 is `59355f36c7da013d363a9ea0f5226e2e622274fd9c26673004e276acc19712f1`.

The encoder compiler test now stops at the actual shared action wrapper on
both calls. Reading only the final shared buffer would miss a wrong press
byte. Changing the simulated peripheral timer after the press breakpoint also
checks that release gets a fresh time. Both production action calls execute.

The first mouse simplification used `-axis(selected >> 4)` for wheel Y.
Exhaustive comparison found a different priority when both selected wheel bits
were set without both held bits. Production state normally excludes that
combination, but the final expression preserves the former result for every
combination. The first form is not retained.

C52 tests supply matrix, NVM and endpoint state. They do not prove physical
encoder wiring, USB/peripheral timing, interrupt overlap, persistent writes or
a runtime stack bound. Stack capacity is an allocation. No complete profile
matrix or release qualification is claimed for this work package.

## Rejected approaches

The corrected mouse-only placement caused the unchanged short-transfer checker
to reject a diagnostic page marker at a site its independent decoder considered
valid. The checker was not weakened. The failed log is retained in `optimization-rejected/`.
Adding the implicit-zero source change moved the image and passed the existing
checker. The diagnostic disagreement was subsequently fixed by restoring rejected
long transfers; see [short-call diagnostics](shortcall-diagnostics.md).

A broad callee-save experiment added 21 C functions to the existing eleven.
It exceeded the permitted final CODE interval through `0xc98b`. Before
short-transfer effects, `ak820_nvm_flush` grew by 279 bytes, `register_code`
and `unregister_code` by 107 each, and `ak820_usb_send` by 97. Preserving their
registers across child calls outweighed reductions at callers. A second trial
kept only eight smaller functions: `get_repeat_key_count`, `ak820_nvm_begin`,
`ak820_nvm_end`, `ak820_macro_ready`, `ak820_tapping_source`, `register_mods`,
`unregister_mods` and `clear_weak_mods`. It still grew the final image by 50
bytes. Neither compiler-flag change is retained.

## Evidence and reproduction

`optimization-candidate/` contains the accepted image, exact linker/build/short-transfer
reports, targeted CPU logs and results, and a complete compressed raw build.
`optimization-no-short/` contains the strict image without short transfers and its targeted
CPU results. `optimization-control/` contains the reproduced baseline identity and linker/build reports.
`optimization-files.json` records retained evidence bytes and SHA256 values. Scratch paths
inside reports are provenance. The final build source snapshot is recorded in
`optimization-candidate/build-report.json`; it precedes documentation and test-description
updates, which do not change compiled firmware.

From `qmk-8051-ak820`, use a fresh output directory:

```sh
python util/build_ak820.py --profile full-mouse-auto-shift --short-calls \
  --build-dir .build/runtime-new \
  --toolchain /path/to/sdcc-4.6.0 --qmk-bin /path/to/qmk
```

Independent source/test/evidence review is closed in [review.md](review.md).
These figures remain isolated measurements; final integration qualification is
recorded in the work-package report.
