# Macro cancellation CPU diagnosis — 2026-10-23

The original complete linked CPU run remains **FAIL**: 64 cases completed and
`macro-cancel-stops-stream` timed out after 45 seconds. The fixture assumed
that EE_CLR called `clear_keyboard` followed by `eeconfig_init`. The linked
image takes the other compile-time branch. This is a fixture error; no
production defect was established by the timeout.

The image is `.build/compact-modtap-send-mask-20261023/ajazz_ak820_vial.ihx`
under `qmk-8051-ak820`, SHA-256
`24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655`.
All addresses below come from that image's relocated listings and map.

## Evidence

The actual EE_CLR dispatch at 0xA55A calls `eeconfig_disable` at 0x9057,
then `soft_reset_keyboard` at 0xA281. The old fixture changed only the unused
`eeconfig_init` entry at 0x9054 to RET. It therefore left the storage and
reset path active. `eeconfig_disable` first calls `eeprom_driver_erase`.
`soft_reset_keyboard` calls `shutdown_quantum`, which clears the keyboard,
waits 250 ms through `mDelaymS`, and then enters `mcu_reset`. The latter writes
board reset registers and loops at 0x3492. Generic C52 does not model these
peripherals. The original timeout log did not complete, so its exact final PC
cannot be recovered or attributed to one of those peripheral operations.

A diagnostic derived from the saved failed script stopped at 0x9057 before
executing `eeconfig_disable`. It completed in about 0.3 seconds. The report
was still `02 00 04 00 00 00 00 00` and `ak820_macro_cancelled` was zero.
This confirms dispatch to the unpatched path; it does not execute EEPROM erase
or reset. The script and log are saved beside the original failed script as
`macro-cancel-diagnose-eeconfig-disable.sim` and `.log`.

```sh
# Run from qmk-8051-ak820; the script stops before storage/reset.
printf 'exec "%s"\n' "$PWD/.build/compact-modtap-send-mask-cpu-20261023/macro-cancel-diagnose-eeconfig-disable.sim" | \
  ../toolchains/sdcc-4.6.0/bin/s51 -t C52 -b -c - \
  .build/compact-modtap-send-mask-20261023/ajazz_ak820_vial.ihx
```

A further diagnostic attempted 100,000 instructions after that stop. Its
existing report breakpoint automatically issued `run`, which escaped the
intended step bound. It hit a separate 10-second wall timeout with no completed
log. That diagnostic is **FAIL**, provides no final-PC evidence, and was not
retried. Its script remains `macro-cancel-diagnose-step-limit.sim`.

## Corrected fixture scope

The replacement case tests a public `clear_keyboard` call while the actual
macro interpreter is active. It makes no EE_CLR claim. It replaces only the
interpreter's DOWN `LCALL register_code` at 0x8D6F, originally `12 74 F6`, with
`12 26 40`. A unique match of the emitted surrounding saves and restores of
r7/r6/r5 is required. The original image guard remains in place.

The test hook at unused simulated ROM 0x2640..0x267A first calls the original
`register_code` at 0x74F6. It saves direct bank-0 registers 0..7, ACC, B, DPL,
DPH and PSW, calls the linked `clear_keyboard` at 0x7682, restores the saved
state and returns. The SDCC listings assign ar0..ar7 to direct addresses 0..7;
the exercised caller uses those same direct push/pop addresses. The CRT starts
with bank zero, and the diagnostic CPU states show PSW bank bits zero. This
fixture does not model an interrupt or a different register bank. Its 59-byte
hook is checked against linked image bytes and stays clear of `Firmware.call`
at 0x2600..0x2605 and its stop at 0x2700.

The stream is DOWN A, DOWN B. Physical-source model fixtures already hold
left Shift and consumer Volume Up. After the first actual DOWN returns, the
hook invokes the real clear. Actual owner cleanup and the interpreter's next
cancellation check run. The interpreter must return before DOWN B. Fresh
press/release events then verify that release admits a new B press.

A single corrected case completed and passed in
`.build/compact-modtap-cancel-hook-diagnostic-20261023/`: all eight snapshots,
the five keyboard reports and the two consumer reports matched. The macro
sample was 263,328 emulator clocks; peak SP was 136 from initial 101 (35 bytes).
The recorded peak includes the injected hook and is not a production-only
stack measurement. The `results.json` records every patch byte and boundary.

This is CPU evidence for public clear, owner cleanup and stream cancellation.
It does not establish EE_CLR, NVM or reset behavior, interrupt overlap, USB,
physical input or timing. No production file was changed, no build was run,
and no device was opened. The initial 65-case failure remains separate from
this passing single case. A corrected complete suite and independent review
are still required before claiming a complete pass.
