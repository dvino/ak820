# CRC checks

Run `./tests/ak820_crc/run.sh` from the repository. Docker uses the cached
`ak820-nkro-study-env:local` image and SDCC 4.6.0 in the sibling beta1 toolchain.
`AK820_TOOLCHAINS` and `AK820_TEST_IMAGE` override those locations.
No firmware image is built and no device is accessed.

The native C reference checks all 16,777,216 CRC state/byte transitions, all
buffer lengths and the standard CCITT-FALSE vector. The linked 8051 executable
runs the actual emitted assembly in s51 against an independent C reference for
lengths 0 through 255 and four input patterns. Buffer boundary canaries and an
assembly caller check zero-length return and preservation of R0/R1.
The ordinary compiled C caller also keeps its loop state live across calls.

The SDCC branch uses the default non-reentrant large-model bank-0 ABI: XDATA pointer and
return value in DPTR, length in the XDATA `_ak820_crc16_PARM_2` slot. R2-R7, ACC and carry are
scratch; the previous compiler-generated C function also overwrites those
registers. No extra stack storage or nested calls are used. Do not apply
`--callee-saves` to this function or call it from an ISR, recursively, or via a
callback. The CPU model does not establish device behavior or qualify the full
firmware's stack and interrupt paths.

The simulator executes 50,000,000 instructions with a 120-second wall limit.
Success requires the terminal success marker, a count of 1024 completed cases
and the ABI success witness (`a5 00 04 a5` at XDATA 0x2000). Failure paths stop
in an explicit assembly loop before those success markers can be written.
`latest-result.json` records the compiler, flags, source and CPU image hashes.
`AK820_CRC_RESULT` overrides the result file path. The measured CRC code area is
52 bytes; the full firmware must be measured and checked separately.
