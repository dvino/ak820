# NVM updater independent component review

Date: 2026-10-25. Scope: the `ak820-nvm-work` worktree, its updater kernel, builder and make integration, component tests, retained component evidence and `docs/NVM-UPDATE-KERNEL.md`. `AGENTS.md` was read. No full firmware build, device action or commit was performed.

## Decision

The bounded component is approved. No blocking correctness finding was identified in the reviewed implementation. This decision does not approve a final firmware image, its stack bound, its effective linked memory savings, or hardware behavior. The exact configured linked image must pass the startup, foreground, outliner and interrupt stack checks required by AGENTS.md before its full regression suites and completion.

Reviewed kernel SHA256: `8710fc9922f4cf9688808faf43fc57a42a29fcb0dd3261ed3e4e25a7bcd69d66`.

## ABI and behavior

The incoming source DPTR is pushed low byte then high byte. Both exits pop high byte then low byte, restoring the original source. The mismatch path removes those two private bytes before its long jump, so the writer receives the original caller's return frame. Its three generic address parameter bytes and both original length bytes are copied individually to the writer's separate parameter slots. No pointer tag is reconstructed or discarded on dispatch.

R2/R3 hold the current offset, R4/R5 the current source and R6/R7 the remaining 16-bit count. The decrement correctly borrows when the low count byte is zero. Offset and source increments wrap at 16 bits. Empty requests skip both reads and writer dispatch. Equal requests only read. The first mismatch forwards the complete original request; range rejection, page writes, failure and flushing remain the existing writer's responsibility.

The scalar call precedes the source MOVX on every iteration. The scalar result is saved in B only after the hook returns, so its permitted B clobber is harmless. The production scalar adapter tail-jumps to `read_offset`; that implementation preserves R0-R7 and its cache path balances its two DPTR saves. The updater does not touch R0/R1 or PSW bank selection. The documented six bytes above updater entry on the scalar cache path are correct before outlining and interrupt effects: two retained source bytes, two call-frame bytes and two scalar private bytes. The writer path has no retained updater private bytes.

The flag is default-off and passed explicitly through the builder into make. The C implementation is excluded when the opted-in separate translation unit supplies the symbol. The builder rejects the reviewed incompatible model, stack, calling-convention and updater callee-save settings, requires its audited scalar hook contract, and owns the assertion/feature define. Source guards and size/layout assertions agree with the documented pinned ABI.

## Independent verification

`python tests/ak820_nvm_updateasm/policy.py` passed all four tests. The complete focused CPU fixture was independently rebuilt and executed with `/workspace/scratch/b8435c5556a8/ak820-max/toolchains/sdcc-4.6.0`; all 3169 paired cases passed. Independent outputs are under `/tmp/nvm-kernel-independent-review/`. The fixture IHX SHA256 reproduced exactly: `f8cfd5e0713b173476bf4406f2958e3f59cf9c7d9ab0bd555a3f3f3945981a99`.

The object areas also reproduced: reference/kernel CSEG 156/118, DSEG 7/0 and XSEG 7/5 bytes. These are component figures, not a claim that final linked DSEG falls by seven bytes or final stack capacity improves.

The fixture checks ordered scalar offsets, equal/empty requests, first and final mismatches, high-byte count borrow through length 257, NVM/page boundaries, offset wrap, four generic tag values, writer argument preservation, writer call count, scalar mutation before source reads, source canaries, R0/R1, bank selection and balanced SP. The maximum-length first-mismatch case checks unchanged 65535 forwarding.

## Evidence limits and nonblocking observations

The scalar and writer are mocks. The failure switch demonstrates one dispatch and no retry after return; it does not simulate flash failure or prove production failure handling. The frozen reference substitutes the equivalent scalar EEPROM adapter for the private `read_offset` entry. Static inspection confirms that equivalence for the reviewed production source, but the parent must check the linked adapter and its preserving hook contract.

Full 65535-byte equality and source-pointer wrap are not dynamically exercised. The count and pointer arithmetic were reviewed instruction by instruction; the document explicitly discloses the full-length equal-traversal limit. IRQ reentry and parameter-slot aliasing are outside this fixture and remain excluded by the runtime contract.

`result.json` hashes the kernel, runner, generated reference, IHX and compiler/simulator binaries. It does not independently hash the generated harness, included header, builder, policy test or document. This is an evidence completeness improvement opportunity, not a discovered execution defect: the harness is retained and the runner that generates it is hashed.

Documentation agrees with observed source and component results and clearly separates CPU/component evidence from linked-image and device qualification. Its final pending-review sentence should be updated during parent integration to point to this review and the eventual linked-image evidence. README/STATUS must also reflect the final integrated state if the parent retains this option.
