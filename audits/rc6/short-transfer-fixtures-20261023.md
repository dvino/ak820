# Short-call fixture run

Date: 2026-10-23. The pinned SDCC 4.4.0 assembler/linker fixture run stopped
after six of 42 planned cases. The sixth link crashed after reporting a page
error and left an empty IHX. No retry, firmware experiment or device command
followed. The remaining 36 cases were skipped. The boundary mismatch from
`short-transfer-relocation-source-20261023.md` remains unmeasured: the run
stopped before sites `0x07FE` and `0x07FF`.

## Commands and retained evidence

Native Python syntax compilation passed. The default runner printed a plan
with 42 cases and zero tool invocations. An initial attempt used the default
WSL distribution incorrectly; it failed before Python because that unrelated
distribution's disk path was missing. No tool ran in that attempt. The lead
then supplied the known working explicit Ubuntu launcher. No WSL repair or
reset was attempted.

The actual fixture command was:

```sh
rtk proxy wsl -d Ubuntu -- bash -lc 'cd /mnt/c/Users/vinok/git/AK820-git && python3 qmk-8051-ak820/.build/rc6-short-transfer-source-20261023/fixtures.py --execute --root-go ROOT_GO_J11_FIXTURES --repo /mnt/c/Users/vinok/git/AK820-git'
```

Its exit status was 1 because the runner stopped on invalid IHX readback.
The private runner and results are in
`qmk-8051-ak820/.build/rc6-short-transfer-source-20261023/`:

| Evidence | SHA256 |
| --- | --- |
| `fixtures.py` | `83450e90354be84bcca0545bf30d9f6a138f9804bcff3c3c4fe6381f8153119c` |
| `fixture-results/summary.json` | `08556f190e9591fd2d4f34cc30c29df58850f9ca02c82129dff872667c815670` |
| Pin file `docs/sdcc44-toolchain-checks.json` | `6c8a47f043004fb11234501affe1e7e85075c6ea68212ed67bb7dfde17f4059e` |
| Actual `sdas8051` | `f941912fe419442a29594f0ac2b4e0db15b538d520b451401ff30400b18b23c9` |
| Actual `sdld` | `67da2318c8523107b71df35861494134f4b5d73ef89024cf70db1dc93885f2f7` |

Both executable hashes matched the pin before invocation. Each attempted case
has separate command records with arguments, working directory, stdout,
stderr, exit status and timeout status. The summary records hashes and sizes
for its ASM, REL, listings, map, IHX and command logs. Output directories were
fresh; symbol-only destination areas emitted no overlapping bytes.

Assembler commands were `sdas8051 -plosgffw caller.rel caller.asm`, plus the
equivalent target-module command for external symbols. All eight assembler
invocations returned 0. Link arguments were
`sdld -n -i -m -w -u result caller.rel`, with `target.rel` added for external
symbols. All child processes finished; none timed out.

## Six measured cases

Every attempted instruction was ACALL at `0x07FD`. The decode uses page bits
from the actual site plus two, checks opcode bits and compares the decoded
address with the expected target. Complete IHX files passed record-length,
checksum, EOF, duplicate-address and exact-output-address checks.

| Case | Target form | Expected target | Link exit | Final bytes | Decoded target | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | Local symbol | `0x07FF` | 0 | `F1 FF` | `0x07FF` | Accepted, correct target |
| 01 | External symbol | `0x07FF` | 0 | `F1 FF` | `0x07FF` | Accepted, correct target |
| 02 | Absolute | `0x07FF` | 0 | `F1 FF` | `0x07FF` | Accepted, correct target |
| 03 | Local symbol | `0x0800` | 2 | `11 00` | `0x0000` | Expected page rejection; emitted IHX is unsafe |
| 04 | External symbol | `0x0800` | 2 | `11 00` | `0x0000` | Expected page rejection; emitted IHX is unsafe |
| 05 | Absolute | `0x0800` | -11 | Empty IHX | Unavailable | Linker terminated by SIGSEGV; stop |

Cases 03 and 04 emitted `2K Page relocation error` warnings and complete IHX
files despite exit status 2. Their bytes encode a different target. This
confirms that the presence of an IHX file cannot establish a valid link.

Case 05 first emitted the same warning, then terminated by signal 11
(`subprocess` return code -11). `result.ihx` exists but has zero bytes;
its SHA256 is
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The decoder reported `Missing IHX EOF`. The runner preserved the files and
stopped. This run does not establish the internal cause of the crash.

## Observed relocation records

These are actual records from accepted cases, consistent with the inspected
4.4.0 source. They demonstrate XH3, a three-byte address/opcode locus and
separate area, symbol and absolute reference forms.

```text
00 local:
T 00 07 FD 07 FF 11
R 00 00 00 04 08 03 00 02

01 external:
T 00 07 FD 00 00 11
R 00 00 00 02 0A 03 00 01

02 absolute:
T 00 07 FD 07 FF 11
R 00 00 00 02 08 03 FF FF
```

The byte index `03` points past the three-byte T address. Mode `08` is J11
area/absolute; mode `0A` is J11 symbol. Case 02 uses the `FFFF` absolute
reference. The linked accepted instruction occupies two bytes.

## Limits and next decision

This is an isolated assembler/linker result, not a CPU model or device test.
No AJMP case, `0x07FE`/`0x07FF` site, away-boundary control, branch-across-site
case or CODE-pointer case ran. There is no 42-case PASS, measured boundary
acceptance result, firmware shortening result or size saving.

Do not continue the interrupted matrix or change error handling to hide the
failure. A new bounded task must first examine the retained crash evidence
and decide whether to isolate the absolute-negative diagnostic path from
other fixtures. Any approved new run needs a fresh directory and the same
tool pin and independent next-PC target check. The current stop condition is
closed by preserving evidence and reporting the failure, not by retrying it.
