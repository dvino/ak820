Русский перевод: [Обновление NVM](ru/NVM-UPDATE-KERNEL.md).

# Optional XDATA NVM update kernel

`--nvm-update-block-asm` selects a separate SDCC translation unit for
`ak820_eeprom_update_block_xdata`. The option is off by default. The existing C
body remains the fallback. No writer, journal, flash format or flush rule changes.

The kernel compares each existing byte before reading the corresponding XDATA
source byte. It stops at the first mismatch and tail-calls the existing writer
with the original source pointer, all three generic address bytes and original
16-bit length. Equal and empty requests return without calling the writer.
The comparison address wraps at 16 bits, as in the C expression `offset + i`.
Out-of-range values still pass through the existing scalar EEPROM hook, which
returns zero. A mismatch retains the writer's complete-request range rejection
and failure timing; the kernel never retries a failed write.

## ABI and stack contract

The supported compiler is pinned SDCC 4.6.0, MCS51 large model, calling convention
zero, register bank zero and fixed XDATA parameter slots. The two-byte XDATA
source arrives in DPTR; the generic address and length occupy the ordinary
five parameter bytes. The updater must remain caller-clobbered.
R2–R7, A, B, DPTR and arithmetic flags are scratch. The comparison kernel
preserves R0/R1; a mismatch tail-calls the existing C writer, whose normal
caller-scratch contract may change them. Bank selection remains unchanged.
The scalar `eeprom_read_byte` hook must preserve R0–R7. Its
builder-owned assertion does not replace validation of the actual linked hook.

Two private stack bytes retain the original source. During a scalar read, the
additional return address costs two bytes and the current scalar cache path
can use two more. This gives six bytes above the updater's incoming stack
pointer before outlining or IRQ effects. The equal/empty exit removes both
private bytes. The mismatch exit removes them before jumping to the writer;
the writer therefore returns directly to the original caller. The writer's
own stack remains a separate bound. These functions and static parameter slots
must not be entered recursively or from an interrupt while active. Exact image
startup, call graph, outliner, bank and IRQ checks remain mandatory.

The builder rejects unsupported stack, parameter, model and calling-convention
flags, a caller-preservation declaration for the updater, a missing audited
scalar hook and attempts to supply its own assertion or feature define through
extra flags. The source also rejects incompatible compiler predefined macros.

## Component verification

Run from the repository root:

```sh
python tests/ak820_nvm_updateasm/policy.py
python tests/ak820_nvm_updateasm/run.py \
  --toolchain /path/to/sdcc-4.6.0 \
  --output outputs/nvm-update-kernel
```

The command writes `outputs/nvm-update-kernel/` with the generated harness,
frozen C reference, compiler assembly/listings/objects, linked fixture, logs
and checksummed JSON result. The CPU fixture compiles the production kernel in
a separate translation unit and compares it with the C loop. Its scalar and
writer are mocks; it does not exercise flash hardware or journal persistence.
It checks ordered read addresses, first-mismatch dispatch, original writer
arguments, all four generic pointer tags, empty/equal requests, page and NVM
boundaries, 16-bit address wrap, source canaries, R0/R1, bank zero and balanced
SP. A scalar mock changes the current source byte before returning, checking
read-before-source ordering. A failing writer mock checks dispatch without
retry. Lengths include 0, 1, 2, 16, 64 and 257; a separate first-mismatch request
checks forwarding of length 65535. The full 65535-byte equal traversal is not
covered by this fixture.

All 3169 paired CPU cases passed, including the maximum-length first-mismatch
case. Final source hashes are recorded in the adjacent JSON result. The standalone object
comparison is 156 to 118 CSEG bytes, 7 to 0 DSEG bytes and 7 to 5 XSEG bytes.
The reference uses the equivalent scalar EEPROM adapter in place of the private
`read_offset` symbol, so this is a component measurement only. No linked image
saving, full firmware stack bound or hardware result follows from these totals.
The [independent component review](../audits/maximal-continuation-20261025/nvm-kernel-review.md)
approved the kernel within this scope. Image 26b includes it and passed 48
bounded calls through the actual linked updater and unchanged C writer with
primed cache and deferred writes. Stop breakpoints prevented entry into the
physical erase/program/page-writer paths. All relevant source, cache, original
writer arguments, return SP and canaries were checked. Empty/equal paths
preserved R0/R1; preservation is not asserted across the C tailwriter.

The exact linked scalar-reader check covers 45 reachable instructions, two
extra stack bytes and seven rejected effect mutations. It establishes
conditional R0–R7 preservation, not read-value or writer correctness. The
current image's conditional total stack is 165 of 167 bytes. CODE still exceeds
the legal window, and the OEM startup/IRQ contract remains incomplete.
[Current verification](../audits/maximal-continuation-20261025/README.md) records
these separate results. No hardware or full configured regression result is
claimed.
