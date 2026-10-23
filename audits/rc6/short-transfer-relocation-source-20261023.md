# SDCC 4.4.0 short-call relocation source

Date: 2026-10-23. This is source inspection only. No assembler, compiler,
linker, packer or device command was run. It closes the missing release-source
prerequisite in `short-transfer-design-20261023.md`; it does not close the
fixture, complete address-consumer audit or firmware experiment prerequisites.
The supplied plain-language instructions and write-like-me skill were applied.
Its retrieval tools were unavailable; no retrieved writing sample is claimed.

## Source and identity

The [official release announcement](https://sourceforge.net/p/sdcc/mailman/message/58730353/)
links the source tag `tags/sdcc-4.4.0-/sdcc`, including the trailing hyphen.
The [official 4.4.0 directory](https://sourceforge.net/projects/sdcc/files/sdcc/4.4.0/)
lists `sdcc-src-4.4.0.tar.bz2`. The download succeeded from
`https://downloads.sourceforge.net/project/sdcc/sdcc/4.4.0/sdcc-src-4.4.0.tar.bz2`
using `curl.exe -L --fail --max-time 90 -o <archive> <URL>`.
The archive contains `sdcc-4.4.0/`; `.version` says `4.4.0`.
This is the official release archive, not a trunk or newer manual substitute.
No independent publisher signature or published SHA256 was checked. The local
hash identifies the downloaded bytes; it does not prove that installed binaries
were built from them. A separate SVN tag export was not obtained or compared.

Archive: 20,036,262 bytes; SHA256
`ae8c12165eb17680dff44b328d8879996306b7241efa3a83b2e3b2d2f7906a75`.
Private retained archive and extraction:
`qmk-8051-ak820/.build/rc6-short-transfer-source-20261023/`.
All source paths and line numbers below refer to that archive's
`sdcc-4.4.0/` directory. Hashes are over extracted file bytes.

| File | SHA256 |
| --- | --- |
| `.version` | `45293c3defe2e38d375d335358fc87b58cd19936ed6588da68f1fef632d3c8d1` |
| `sdas/as8051/i51mch.c` | `6aebcf28ee2c6af24ee480647eadb3b1a4704a20fb1d2c9fcbdad0d6ded9fa3b` |
| `sdas/as8051/i51pst.c` | `f43a1bb1674d20647955d9d1e664b968807cd2ac7115b412d1e07788ba5c8d3f` |
| `sdas/asxxsrc/asxxxx.h` | `fc95da3551e0eedf59fb7d23efe340a240ae742a601aebf50ab309ab4ddf990f` |
| `sdas/asxxsrc/asout.c` | `d3202fd620a19fc05d50b4623b6ad0420d733d84d696ccab53fd0452a91fdb42` |
| `sdas/linksrc/aslink.h` | `d37f9fee3518c69a8860446175a1461729734f49aac20e2356fae43cca18bcde` |
| `sdas/linksrc/lkrloc.c` | `b0f09e8a4189c2334117c64f256cdb00e96ba2e06805b2ccb0002c119966c3f2` |
| `sdas/linksrc/lkrloc3.c` | `cdf5aed5fca03d208fc1469ab64e7e743139bb5a378b2dc3e16b55deb87d919c` |

## Assembler record

`i51pst.c:179-180` assigns `ajmp` opcode `0x01` and `acall` opcode
`0x11`, both `S_JMP11`. `i51mch.c:98-105` parses the destination expression
and calls `outrwm(&e, R_J11, op)`.

`asxxxx.h:372-376,393-394,414-420` defines `R_WORD=0`, `R_BYTX=0x08`,
`R_SYM=0x02`, and `R_J11=(R_WORD|R_BYTX)`; the J11 recognition mask is
`R_BYTE|R_BYTX|R_MSB` (`0x89`). `aslink.h:355-361` supplies the matching
linker `R3_J11` definition. Ordinary area J11 mode is `0x08`; symbol J11 is
`0x0A` before any expression flags. These values are special word modes,
not ordinary byte-selection relocations.

For the SDAS 8051-like path, `asout.c:1670-1709` emits a three-byte T locus:
two destination/addend bytes, followed by the raw opcode. It emits a relocation
whose byte index is `txtp - txt - 3`. For symbolic expressions the reference
is the symbol number with `R_SYM`, or the area number otherwise. Absolute
destinations use area-mode reference `0xFFFF` (`1671-1682`). Assembly location
advances by two bytes (`1709`), although this T locus contains three.

`out_txb` (`1521-1533`) and `out_rw` (`1485-1493`) honor `hilo`; for XH3,
the destination/addend and two-byte reference index are high-byte first.
The three address bytes at the start of an XH3 T record are separate from
the two-byte J11 destination locus. `write_rmode` (`332-357`) writes mode
and byte index, escaping the mode when needed. Thus a plain J11 R entry is
mode, T byte index, reference high byte, reference low byte. A general parser
must still handle escaped modes and retain T/R association.

## Linker behavior and a boundary mismatch

`lkrloc.c:77-92` dispatches object format version 3 to `reloc3`.
`lkrloc3.c:334-370` reads mode (including its escape), byte index and reference;
it adds the resolved symbol value or area base. For absolute J11 reference
`0xFFFF`, it adds zero. `adb_2b` (`lkrloc.c:189-204`) adds the base to the
two-byte addend, writes its low sixteen bits back, and returns the full sum.

The exact J11 check in `lkrloc3.c:556-560` is:

```c
relv = adb_2b(reli, rtp);
if ((relv & ~((a_uint) 0x000007FF)) !=
    ((pc + rtp - rtofst) & ~((a_uint) 0x000007FF))) {
    error = 6;
}
```

`pc` is the relocated T address (`314-320`); `rtofst` starts as `a_bytes`
(`315`) and accounts for prior removed object bytes. The record index points
to the first address byte of the instruction locus. Therefore the source
compares the destination page with the instruction site's page. It does not
add the two-byte instruction length. This differs at the last two bytes of
a 2-KiB page from the hardware next-PC rule described in the design report.
This conclusion follows from the source path; it has not been tested against
the installed pinned executable.

For a site `0x07FE` or `0x07FF`, a target `0x07FF` passes this source check
but fails the hardware `s+2` page rule; target `0x0800` does the reverse.
Site `0x07FD` does not have this mismatch. Fixtures must exercise these cases
and record the actual executable's diagnostics and bytes. A quiet link cannot
replace the independent final check
`((s+2)&0xF800)==(target&0xF800)` in the supported 16-bit CODE range.

Run the following isolated matrix for both ACALL and AJMP, using local and
external symbolic destinations. These predictions are source-derived
hypotheses, not observed results from the pinned binary. Also cover absolute
destinations to exercise the `0xFFFF` reference path.

| Site | Target | Predicted source check | Hardware next-PC check |
| --- | --- | --- | --- |
| `0x07FD` | `0x07FF` | Accept | Accept |
| `0x07FD` | `0x0800` | Page error | Reject |
| `0x07FE` | `0x07FF` | Accept | Reject |
| `0x07FE` | `0x0800` | Page error | Accept |
| `0x07FF` | `0x07FF` | Accept | Reject |
| `0x07FF` | `0x0800` | Page error | Accept |

Use separate source and target areas so the fixed-address fixtures do not
accidentally overlap instruction bytes. Inspect each final site independently;
never execute a fixture merely because the linker accepts it.

`lkrloc3.c:568-570` merges address bits 10:8 into opcode bits 7:5,
hides the third object byte and increments `rtofst` by one. Final output is
`opcode | ((target >> 3) & 0xE0)`, then `target & 0xFF`. The opcode's base
comes from the assembler's third locus byte. The source performs the merge
even after setting the page error.

Error 6 is `2K Page relocation error` (`685`). The error path calls `relerr3`
(`654-660`), which reports to stderr and an open map (`887-892`);
`errdmp3` prints an ASlink warning and increments `lkerr` (`945-946`).
The source continues toward output (`669-675`): an emitted IHX is not proof
of success. This inspection did not establish the installed process exit
status or whether a wrapper rejects every such warning.

The full-sum page comparison also rejects a destination above 16 bits when
the source page remains in the 16-bit range. There is no separate J11 unsigned
16-bit overflow check in this branch. Do not generalize this to all object
modes, wrapped expressions, different link windows or other architectures.

## What is still required

No REL file was rewritten and no firmware shortening was attempted. The
archive closes source availability, but does not certify a general REL parser,
all expressions, all address consumers, final layout, timing or hardware.
Keep the copied-ASM approach and fresh full links from the design report.
Run isolated boundary fixtures only after the lead releases the shared build
constraint. Check actual tool hashes, diagnostics, exit status, R entries,
final bytes and the independent next-PC page rule. Then reproduce the control
before considering one firmware edge. Stop on a mismatch or unexplained mode.
