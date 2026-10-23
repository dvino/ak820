# Breathing arithmetic review — 2026-10-23

Independent reviewer: a fresh review agent that did not author the candidate. Scope: the private arithmetic probe and its saved evidence. No compiler, build, simulator, USB operation or production edit was run during review. Only this review file was written.

## Decision

GO for integrating the exact reviewed arithmetic expression into source, followed by the normal production build and regression checks. There is no arithmetic or ABI blocker in the saved candidate. This is not approval to flash or a claim about installed firmware. The evidence and reproduction notes below were closed in a follow-up review.

The private candidate source has SHA256 `810ac091fb9f0206ab6e6db86e6ab2f51a8003f647c64f35ebb8602db6d23415`. Its only source change replaces the existing return expression with:

```c
uint8_t delta = pgm_read_byte(&CIE1931_CURVE[index + 1]) - low;
uint8_t fraction = value & 7;
uint8_t product = (uint8_t)(delta * fraction);
return low + (product >> 3);
```

## Arithmetic and emitted code

The current compact table has 32 entries, starts at 0 and ends at 255. All 31 adjacent deltas are positive, from 1 through 36. The fraction is from 0 through 7, so every product is at most 252. Integer promotion of the two unsigned-byte operands to SDCC's signed 16-bit `int` is safe: neither subtraction nor multiplication exceeds its range. Converting the product to `uint8_t` loses no bits. The shift happens after the product, and the final sum stays within the next table value. There is no signed overflow or changed precedence.

I independently enumerated all 256 inputs using the actual saved table and both expressions. There were zero differences. Inputs 248 through 255 still take the existing index-31 early return, so no access to entry 32 occurs. This proves identity to the old compact function above 160; it does not prove new accuracy against the full curve in that region. The last interval represents samples at 240 and 255 and already has different spacing from earlier intervals.

`AK820_BOARD` is defined by the board configuration. With `USE_CIE1931_CURVE` enabled and `AK820_FULL_CIE` absent, the compact table and changed branch are selected together. The full-table branch and disabled-CIE branch are unchanged; they were not compiled by this probe.

The candidate assembly uses `mul ab`, retains the low byte, shifts it by three and returns in DPL. Its input remains in DPL. The control uses `__mulint`. No function signature or caller contract changes. This review does not establish interrupt-overlap safety beyond the existing implementation.

## Evidence checked

The private folder is `qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023/`. I read both retained scripts, reports, source and assembly, plus the CPU runner and saved logs. The scripts are confined to private output directories and contain no hardware access.

The current production source hash matches the compile report (`2d9a4e6541c9b49a76c3f2f1785401c06126c69d47c045421a58abb904fe3aee`). The candidate source hash also matches. The control assembly is byte-identical to the canonical RGB assembly. The reconstructed control IHX is byte-identical to canonical IHX `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`. The saved baseline build-report hash matches too. This establishes the control through the saved dead-code and outlining pipeline; the candidate replaces only the RGB assembly input in that pipeline.

I independently parsed both IHX files, checked record checksums and counted their address windows. Control contains 39,432 CODE bytes: 37,573 main and 1,859 low. Candidate contains 39,390: 37,531 main and 1,859 low. Both stay inside the declared windows. The saving is 42 linked bytes. Saved linker reports give unchanged XRAM of 2,071 bytes and stack capacity of 152 bytes. Stack capacity is not measured stack margin.

Candidate CPU results bind to IHX `6b94dcab471db542d236747babfe553ec984299294ff8428b594cfd1ab9444b5`. Every listed linked metadata hash and current runner/source hash matches its file. The compiler and simulator hashes also match the installed files. The runner directly calls the linked helper for 161 inputs and passes 50 rendered-frame fixtures. Control and candidate outputs match; the direct-helper exercised stack falls from five bytes to two. The renderer observations are identical. The suite does not directly compare helper outputs to sparse interpolation, but its recorded outputs and the static identity proof support the same behavior.

Baseline and candidate use identical simulator and test-source hashes. Their saved logs confirm helper counters of 63,181 and 42,895 vclks, and renderer counters of 10,013,062 and 10,006,762 vclks. These are comparable model operation counters for the same fixtures and call machinery. They are not wall time or physical chip timing.

## Findings and closure

1. Minor: the two reproduction commands currently rerun scripts whose output directories already exist. `probe.py` creates `control` and `candidate` without `exist_ok`; `link_probe.py` likewise refuses existing linked directories. A rerun therefore stops with `FileExistsError`. Document that these are retained one-shot scripts and provide a fresh-output procedure before calling the displayed commands reproducible. Do not delete the retained evidence to work around this.
2. Minor: `compile-report.json` names a field `full_curve_error_oracle_max`, but its generator compares `table[v >> 3]` with the full curve, without interpolation. Its value 17 is not an interpolation-error bound. Rename or explain this field in the probe evidence. The prose audit does not repeat this number and correctly confines the supported-domain error claim to one.
3. Clarification: CPU `source_sha256` records the unchanged production RGB source, not the private candidate source. Candidate provenance is supplied by the separate compile report, candidate assembly and linked-image/metadata hashes. Keep these reports together; do not cite the CPU source field alone as the candidate source identity.

Follow-up closure, 2026-10-23: I reread the amended audit, scripts and metadata. Finding 1 is closed: both scripts now accept `--out`, the compile script requires a fresh directory, and the audit supplies matching fresh-output commands. The link script accepts explicit control assembly and candidate assembly paths. Finding 2 is closed: the generator and saved metadata use `quantized_curve_error_max`, and the audit explains exactly what 17 measures. Clarification 3 is closed: `production_source_sha256` is explicit, and the link report also records each RGB source and assembly hash. The recorded candidate source and assembly hashes remain the reviewed values. These changes describe retained evidence; they do not claim a new compiler, linker or CPU run. Reproduction still requires the original pre-integration source expected by the probe's exact replacement assertion.

The candidate's exact source integration is acceptable. No combined production build or packed image was reviewed here. Physical timing, LEDs, DMA, USB, storage and installed behavior remain untested.
