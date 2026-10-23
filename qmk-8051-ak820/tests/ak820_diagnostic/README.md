# Read-only diagnostics regression

`python3 -B tests/ak820_diagnostic/run.py` executes the production NVM backend
against memory-only Flash. It checks all first-failure stage codes 1–15,
preservation of that first failure across retries, cached getter versus CODE
contents, and that reading the status performs no storage access at all.
`tests/ak820_usb/run.py` verifies the actual FD01 handler and endpoint routing,
including dirty/faulted storage, unlock-in-progress, repeated snapshots, zero
padding, and an unknown subcommand. The same new FD01 test fails on rc2 because
rc2 routes FD01 through ordinary NVM begin/flush/end.

For an already linked firmware, run:

```sh
python3 -B tests/ak820_diagnostic/emitted.py \
  --build .build/your-candidate \
  --simulator /absolute/path/to/sdcc-4.4.0/bin/s51 \
  --output /absolute/path/to/diagnostic-evidence
```

This executes the actual SDCC FD01 instructions with explicit RAM/MMIO
fixtures. Breakpoints on begin/flush/end/erase/program detect accidental entry
to persistence code. CPU PASS does not implement CH555 electrical Flash or USB
timing and does not prove behavior on the physical keyboard.

## FD01 v1 wire format

Request: `FD 01` followed by 30 zero bytes. Response: exactly 32 bytes.
The command bypasses NVM batching/flush/end and does not clear any state.
Use it only after identifying firmware that implements this version: rc2 does
not have this read-only command. FD00 remains the direct CODE-readback path.

| Byte(s) | Meaning |
|---|---|
| 0–3 | `FD 01 01 A8`: command, subcommand, version, signature |
| 4 | `storage_failed` (0 or 1) |
| 5 | `page_valid` (0 or 1) |
| 6 | `page_dirty` (0 or 1) |
| 7 | batch depth |
| 8–9 | cached logical page, little endian; ignore if `page_valid=0` |
| 10 | first NVM failure stage, below |
| 11 | last IAP attempt valid (0 or 1) |
| 12 | last hardware IAP command (`A6` erase, `9A` program) |
| 13 | actual ROM_STATUS before issuing the command |
| 14 | actual ROM_STATUS after the command; equals before if precondition prevented issuing it |
| 15–16 | last attempted in-range Flash address, little endian |
| 17 | Vial unlocked |
| 18 | Vial unlock in progress |
| 19 | USB enumeration state |
| 20 | USB sleep flags |
| 21 | Raw HID state during snapshot; normally `RAW_WORK=3` |
| 22–31 | reserved, zero |

If byte 11 is zero, bytes 12–16 are zero and no attempt has been recorded since
startup. The IAP record describes the **last attempt**, not necessarily the
first failing address. In particular, an NVM readback mismatch follows the
last program operation, and the mismatch can be at another byte. Diagnostics
do not freeze or alter the operating algorithm; the normal storage-failure
latch blocks later writes. `eeprom_driver_init` initializes the NVM failure
state normally. An FD01 request never initializes or resets it.

| Stage | Meaning |
|---|---|
| 0 | No NVM failure latched |
| 1 | Recovery journal page out of range |
| 2 | Recovery journal CRC mismatch |
| 3 | Recovery target write/readback failed |
| 4 | Recovery journal-header cleanup failed |
| 5 | Journal-header erase failed |
| 6 | Erased journal header was not all zero |
| 7 | Journal data write/readback failed |
| 8 | Header metadata program failed |
| 9 | Header metadata readback failed |
| 10 | Commit-byte program failed |
| 11 | Commit-byte readback failed |
| 12 | Target page write/readback failed |
| 13 | Final journal-header cleanup failed |
| 14 | EEPROM write request out of range |
| 15 | NVM batch depth overflow |
| 16 | Incompatible VIA NVM schema; automatic defaults reset and subsequent writes blocked |

Stage 16 is latched by `via_init()` after EEPROM journal recovery. It prevents
the VIA defaults reset; it does not claim that an earlier valid committed
journal was never replayed. Read-only FD00/FD01 and the physical recovery path
remain available. Use explicit offline schema migration before installation.

FD01 is evidence about RAM and the last IAP attempt. Durable settings must
still be confirmed by direct FD00 CODE reads and journal state. A RAM cache
can contain a new keycode after a failed write.
