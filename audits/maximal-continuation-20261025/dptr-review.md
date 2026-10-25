# Independent review: immediate DPTR restore elision

Date: 2026-10-25. Baseline: `09330ab708e1eb3671571f63894c583e01743eef`.
Decision: **approve the bounded component patch after the correction below**. No open findings. This is not approval of a linked firmware image or deployment.

## Finding and closure

**P1, closed: reject location-dependent immediate expressions.** The initially supplied implementation accepted any nonspace/noncomma operand after `dptr,#`. In SDAS, `.` denotes the first byte of the current instruction (pinned toolchain `share/sdcc/doc/sdas/asmlnk.txt`, section 1.3.4, lines 1308 onward). Deleting the preceding restore moves that instruction by three bytes. A followup such as `mov dptr,#.` therefore cannot support the claimed identical overwrite proof. The correction restricts operands to bare C symbols and fixed decimal/hexadecimal literals within 16 bits. Expressions, local numeric labels, signed literals and character constants fail closed. The new adversarial test covers `.`, `(.+1)`, `(.-1)`, symbol arithmetic, local labels and overflowing constants. All 40 replay admissions use bare C symbols, so this restriction preserves the measured admission count. Correction independently reviewed and accepted.

## Safety assessment

The enhancement runs only after the existing private-formal, typed valid-C, opcode/storage and suffix/context checks qualify a candidate. It removes exactly the final generated `MOV DPTR,#formal_endpoint`, retaining the original boundary-state replacement for audit. The generated assignment sequence and parity-producing ACC move remain intact. Only DPL/DPH can differ at the shortened prefix endpoint. The immediately following full `0x90` instruction reads neither incoming byte and replaces both; equivalence is correctly claimed after that instruction.

Admission rejects nonempty semantic source lines between the spill endpoint and following instruction. Labels, directives, areas and hidden unlisted instructions therefore block it; comments and blank lines do not. Function inventory boundaries and the required byte-address contiguity prevent crossing functions or discontinuities. Branches, calls, MOVX, partial DPL writes, wrong opcode and wrong length are rejected. Following text is outside the replacement window and remains unchanged. The operand restriction closes the instruction-location dependency found during review. This argument assumes the existing captured compiler-generated assembly context; it does not extend permission to arbitrary handwritten assembler symbol aliases.

## Tests and evidence

Independent focused execution: `python3 -m unittest discover -s qmk-8051-ak820/tests/ak820_parameter_spills -p 'test*.py'`: **15 tests PASS**. Existing tests remain present. Admission tests cover barriers, wrong bytes/length/address, non-overwrites and report accounting. The host state model is representative and hand written; it is corroboration, not a proof of generator implementation.

The retained CPU fixture is also representative machine code, not generated-instance replay. It compares the existing replacement plus overwrite with the shortened replacement plus the same overwrite, for widths 1–4 and all 256 initial PSW values (including all register banks), observing 256 IRAM bytes, 128 SFR bytes and 256 XRAM canaries at common continuation PC 0x0200. The ACC capture order for width four and final parity-producing ACC move agree with the generator. Independent reparsing of the retained simulator log confirmed all 1,024 old/new pairs agree in these observations, and retained evidence hashes match. The 2,048 executions reported by the runner are consistent. No additional simulator process, build or device operation was performed by this review.

The replay records 40 admissions among 82 previously selected sites, nominal object savings 607 to 727 bytes: 120 additional nominal bytes. This is not a linked-image measurement. The README accurately describes the grammar, equivalence point, representative CPU scope, 15 tests and remaining gates.

## Exact-image guards and limits

Preparation binds original ASM/LST hashes, including the following instruction, and whole rewritten module hashes. Object verification rechecks those identities, checks the exact CSEG delta, rejects changes in other areas, and re-inventories fresh ASM/listing alignment. The postlink audit binds new IHX/MAP and final linked listing hashes to the fresh stack report, rejects rewritten functions reachable from enabled application IRQ roots, and verifies private XRAM placement. These are retained safeguards; the enhancement does not bypass them.

The existing postlink audit does not separately decode this followup at its final position or itself establish startup, IRQ wrapper preservation, nesting and stack-capacity acceptance. With fixed immediate grammar, frozen compiler assembly and the pinned trusted assembler/linker, a new opcode decoder is not required for this bounded component change. A final image still requires the mandated exact-image full stack/IRQ check before regression qualification. No such image is qualified by the supplied component evidence.

The argument requires ordinary foreground execution and IRQ behavior preserving DPTR and the existing context contract. Disabled-interrupt/timer CPU runs do not prove asynchronous interrupt behavior or timing equivalence. The fixture does not prove the original spill rewrite, every compiler instance, final linking, physical behavior or device installation. Cycle counts intentionally differ. No builds, commits, USB commands, resets or device writes were performed in this review.

## Frozen identities (SHA256)

| File | SHA256 |
| --- | --- |
| util/ak820_parameter_spills.py | cfb43d3ccaf73ec27183c65eb142a6fc8263a1bf2df8694e0650fa822dd0c9f0 |
| tests/ak820_parameter_spills/README.md | 768e2c8d554b5352506b490838cc17af0cc9bea923e83a8cec862d5bcae01a19 |
| tests/ak820_parameter_spills/test_dptr_restore.py | f5b75328e31f822660ba57fb2b0ba3e69e7c84be9ed6c3070eb99d421cc08c49 |
| tests/ak820_parameter_spills/cpu_dptr_restore.py | 49ebf6deeba848d43105ac81b9cfcad13ad9cedec61ade81746f111a8fe3f22b |
| dptr-component-final/results.json | 15011487aaaeed3dc2b32d909b714c189e00a44fb9a90737b4da1b9fb4d88dc2 |
| dptr-component-final/admission-replay.json | 9c86ecd2f8ec94cbd77d212304a34d767312e71615d0cea16df7cf0067765a89 |
| dptr-component-final/dptr.sim | cc702a377aa11f41b0b4a3589c9df5ea8216db0c3a5d1ed44a81b7ac752d3758 |
| dptr-component-final/dptr.log | b60b9280d388138c1284969d210fdee2c586753d2c8be686ccd20ee824874f12 |
| Pinned s51 | 61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd |

Source paths are relative to `ak820-dptr-work/qmk-8051-ak820`. Evidence paths are relative to `continuation-artifacts`.
