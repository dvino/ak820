# Short-call relocation source review

Independent review, 2026-10-23. No findings block the source-derived claims
in `short-transfer-relocation-source-20261023.md`. The binary fixtures remain
pending. This review does not approve instruction shortening in firmware.

I read the cited local SDCC 4.4.0 assembler and linker source paths and checked
the eight extracted-file hashes against the report. All match. This review
does not independently certify the publisher, downloaded archive or installed
binary provenance. No assembler, compiler, linker, simulator or USB operation
was run. No production files were changed.

The source supports the reported J11 encoding. `i51pst.c:179-180` supplies
the AJMP/ACALL base opcodes; `i51mch.c:98-105` routes both through `outrwm`.
`asxxxx.h` and `aslink.h` agree on the J11 mode and recognition mask.
The SDAS branch of `asout.c:1670-1709` emits two destination bytes followed
by the opcode, points the relocation at the first destination byte and
advances the assembly location by two. Symbol references add the symbol
flag; absolute targets use reference `0xFFFF`. The reported high-first
ordering and escaped-mode cautions agree with `out_rw`, `out_txb` and
`write_rmode`.

The boundary mismatch follows from the inspected linker source.
`lkrloc3.c:314-320` establishes relocated record PC and the removed-byte
offset. The J11 branch compares the full relocated destination page against
`pc + rtp - rtofst`, before hiding the extra opcode byte and updating the
offset. There is no added instruction length in that comparison. Thus the
report's six predictions at sites `0x07FD`, `0x07FE` and `0x07FF` follow
from the source. The last two sites differ from the next-PC page rule. The
predictions remain hypotheses about the installed executable until fixtures
check actual diagnostics and bytes.

The opcode merge at `lkrloc3.c:568-570` produces the stated target bits and
low byte. It still runs after a page error is recorded. The later error path
reports the warning, increments the error counter and continues toward
output, as the report states. The report correctly leaves actual process
exit behavior unclaimed. The full-sum versus sixteen-bit writeback distinction
also agrees with `adb_2b`; the report appropriately limits this observation
to the inspected J11 branch and supported address range.

Retain the planned isolated local, external-symbol and absolute-target
fixtures for both instructions. Check tool hashes, exit status, relocation
records, warnings, final bytes and the independent next-PC rule. An IHX file
or quiet link alone is insufficient. The full address-consumer audit,
control reproduction and any firmware experiment remain separate gates.
