# Archive and HID trace review

## Archive preservation

Independent read-only checks agree with
[`private-archive-preservation-check-20261024.json`](private-archive-preservation-check-20261024.json).
The private ZIP SHA256 is
`5216301983821dd40d6a0bab21ca85f73b032e94e48c574fed5637752fba5b63`.
It matches the supplied sidecar. All 130 file entries pass ZIP CRC checks,
and all 130 corresponding files under the private `captures/` directory
match the ZIP bytes exactly. The backup is outside the repository; no
archive, ROM or raw disassembly was added to Git by this review.

## HID trace checks

The 65,536-byte ROM SHA256 is
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`.
An independent parse checked the Intel HEX record checksums and confirmed
that all 65,536 decoded bytes match that ROM. The pinned s51 executable
SHA256 is
`61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd`.

The first review correctly checked the archive and byte identities but
incorrectly approved request 9 routing to `0x5306`. It also closed a wording
finding without catching that arithmetic error. The deeper independent review
in [`oem-indicator-dataflow-review-20261024.md`](oem-indicator-dataflow-review-20261024.md)
identified the error. That earlier approval of the request path is withdrawn.

## Corrected routing and closure

A fresh static decode checked the instructions and each zero-result branch.
For request 9, the accumulator is 7 after `ADD #0xFE`, then 6 after `DEC`,
then 0 after `ADD #0xFA`. The `JNZ` at `0x5105` therefore does not jump;
`0x5107` jumps to `0x52CE`. For request 10, the corresponding values are
8, 7 and 1. The `JNZ` at `0x5105` jumps to `0x510A`; its `DEC` produces
zero, so `0x510B` does not jump and `0x510D` reaches `0x5306`. These branches
check the accumulator directly, not the carry flag. The instruction at
`0x5103` subtracts 6; the cumulative subtraction at that point is 9.

At `0x52CE`, the literal checks for `04 02 01 00` at `0x1002..0x1005`
set `0x086F`. The other successful branch requires `00 02 00 00` and sets
`0x05CA` to one. At `0x53A1`, the saved request byte must equal 9;
with `0x05CA` nonzero, the code clears the flag and copies `0x1000` to
`0x09AD`. The corrected HID report agrees with these instructions. This
recheck closes the arithmetic finding for the bounded static path. The
request-type mask still does not enforce an exact class request type.

The fresh decode also independently confirms the central staging claim in
`oem-indicator-dataflow-review-20261024.md`: at `0xEA30`, bit 1 of `0x09AD`
selects `R3=0xFF` or zero. The call uses `R7=0x47` and `R5=1`.
The helper at `0xEC9C..0xECC9` calculates `0x066D + 4*R7`, writes
`0xFF` at that address, then writes `R3` at offset `R5`. Thus slot 71's
first byte is at `0x0789` and the selected value is at `0x078A`.
The same decode confirms the adjacent conditional stores from `0x0A79`
to slot 79 offset 1 and from `0x0A84` to slot 79 offset 3.

This additional review does not independently approve the other report's
switch-helper interpretation, copy loop, caller conditions or action-4 state
origin; those claims remain within that report's separate review scope.
No conclusion about a physical C/W connection follows from this recheck.

The fresh private decode is `independent-review-corrected-decode.txt` beside
the author's decode, with mode `0600` in a `0700` directory. The earlier
private decode remains as the evidence of the first review. Archive
verification is unchanged.

These checks do not validate installed firmware, transfer timing, scheduling,
electrical polarity or device behavior. Only static decoding and literal
arithmetic checks were used; no CPU execution, build, USB command, reset,
bootloader transition or flash was performed.
