# Linked inventory, 2026-10-23

The reusable inventory reads a build report, validates every listed artifact's size and SHA256, rejects escaped paths and normalized aliases, and compares relocated instruction bytes with the linked Intel HEX image. Main and low occupied totals are independently recomputed from the declared nonoverlapping windows; inconsistent totals and bytes outside those windows cause refusal. It reads CODE areas and global target labels from the linked MAP. It also reads the retained-function summary from the reachability report. It changes no firmware and performs no hardware operation.

## Baseline result

The SDCC 4.6 roadmap baseline contains **38,100 occupied bytes**: 36,292 in the main window and 1,808 in the low window. Its IHX SHA256 is `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.

The MEM total of **38,105** is the sum of the MAP's CODE area sizes. Exactly five addresses inside those areas have no IHX data: **0x302a through 0x302e**, in HOME. The relocated `dce/quantum/main.rst` has `.ds 5` at 0x302a, immediately after the interrupt-vector jump at 0x3027. This is reserved space counted in an area's allocation, not five occupied bytes and not an absolute-section overlap.

The 64 relocated listings provide **35,313 validated instruction bytes**. The remaining **2,787 occupied bytes** are uncovered by this instruction inventory. That remainder includes data and library code; it is not classified as waste or available space. Per-module rankings and qualified function-label buckets appear in the JSON report. Their sizes count covered instruction rows, not complete function extents. For example, the largest covered modules are USB protocol code (4,837 bytes), dynamic keymap code (2,696 bytes), and RGB code (2,379 bytes).

The covered rows contain **1,214 direct transfers**. Of those, **522 long transfers** have targets in the page selected by `(site + 2) & 0xf800`, the 8051 two-byte ACALL/AJMP rule. This is a current-placement observation. It does not establish a safe rewrite, net savings after relocation, timing, stack behavior or a complete call graph. No short-call conversion is implemented.

There are **44 direct calls to named generic-pointer helpers** in covered rows, including MAP-resolved library targets. Computed transfers, external loader entries, interrupt edges and address-table dispatch require separate analysis. The reachability report's retained edges remain source/assembly evidence; this inventory does not relabel them as a complete linked call graph.

## Artifact and naming limits

The build report authenticates the IHX, MAP, MEM and reachability artifacts against its recorded hashes. It does not record relocated listing hashes. The inventory therefore records each listing's current SHA256 and validates its instruction bytes against the IHX, while treating listing function labels as descriptive. Matching instruction bytes cannot authenticate a changed function label or prove that all linked instructions have listings. MAP target names have the build report's artifact binding. Same-named local labels remain separate through module-qualified names.

Instruction coverage is intentionally restricted to relocated CODE rows with assembler cycle annotations, matching IHX bytes and complete classic-8051 instruction lengths. A 256-entry opcode-length table checks all instructions; the reserved A5 opcode is refused. Instruction boundaries still come from listings rather than a control-flow disassembly. No timing sum is derived from those annotations. Unknown listing syntax, mismatched instruction bytes, overlapping instruction rows, malformed HEX, conflicting MAP areas and replaced report artifacts cause refusal. Missing listings reduce reported coverage; the report makes no complete-function ranking claim. The input build report itself is a supplied trust anchor, not a cryptographic signature from an independent builder.

## Reproduction

Run from the repository root:

```sh
python qmk-8051-ak820/util/ak820_linked_inventory.py \
  --root audits/rc6/bounded-evidence-20261023/control \
  --report audits/rc6/bounded-evidence-20261023/control/.build/bounded-control/build-report.json \
  --output /tmp/ak820-control-inventory.json
python qmk-8051-ak820/util/ak820_linked_inventory.py \
  --root audits/rc6/bounded-evidence-20261023/pointer \
  --report audits/rc6/bounded-evidence-20261023/pointer/.build/bounded-probe/build-report.json \
  --output /tmp/ak820-pointer-inventory.json
python -m unittest discover -s qmk-8051-ak820/tests/ak820_inventory -v
```

Seven offline tests pass. They check malformed HEX, artifact replacement, escaped paths, normalized aliases, incorrect main/low totals, out-of-window bytes, overlapping windows, truncated non-transfer instructions, listing/IHX byte mismatch, missing instruction coverage, module-qualified local names, invalid listing rows, and the 2 KiB page boundary including 16-bit wraparound. They do not exercise hardware or prove parser support for every possible ASxxxx output format.

The comparison is preserved in `linked-inventory-pointer-20261023.json`. Both saved reports now regenerate exactly from the retained roots above; the original transient probe folders are not required. That image has SHA256 `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`: 38,069 occupied bytes, 35,282 covered instruction bytes, the same 2,787 uncovered bytes, and 41 generic-helper calls. This comparison observes a 31-byte occupied-code reduction and three fewer covered generic-helper calls. It does not verify behavior or deployment.

Independent code review passed. Seven inventory tests and ten runner tests passed in an independent rerun. Both inventories were independently regenerated in memory from the retained roots and exactly matched the saved JSON files. A documentation finding about transient reproduction paths was corrected above. Final documentation and evidence review is recorded in [completion review](roadmap-completion-review-20261023.md). No hardware test was performed.
