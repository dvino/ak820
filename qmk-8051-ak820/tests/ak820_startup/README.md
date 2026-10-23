# AK820 startup regression

The runner checks the **linked SDCC instructions** used by the AK820 startup and
the trial entry created by the production packer. It does not build firmware,
open HID, execute a flash operation or modify a reference image.

Run from `qmk-8051-ak820`, after building the candidate into a fresh directory:

```sh
python3 tests/ak820_startup/run.py \
  --build .build/r4unlock \
  --legacy-build ../releases/rc3/firmware \
  --stock-rom /path/to/private-oem-references/releases/rc5/reference/stock-full.bin \
  --simulator ../toolchains/sdcc-4.4.0/bin/s51 \
  --output .build/r4unlock/startup-checks
```

The legacy build directory is a preserved historical artifact. The stock ROM
argument must point into the owner's private archive; this checkout no longer
contains the release reference images.

Replace both `.build/r4unlock` paths with the current candidate directory.
`--simulator` is optional; omitting it skips full CRT/pre-erase CPU execution
and the report has no `ucsim` section. The full CPU check expects the original
build filenames (`ajazz_ak820_vial.ihx/.map/.mem`), as does the shared emitted-code
test harness. The legacy comparison also accepts archived `application.ihx/.map`.

## Checks and boundaries

| Check | Evidence |
| --- | --- |
| Real XINIT copy | Entire simulated XRAM equals an independent flat-copy oracle; writes have exactly the expected order and extent; no short `MOVX` or `P2` write executes. |
| Length boundaries | The same linked loop with patched relocation operands handles 0, 1, 255, 256, 257, 512, 538 and 2048 bytes, including destination page crossings. |
| Legacy contrast | The rc3 loop works under classic `P2` paging and writes different addresses under an alternative low-256 interpretation. These are explicit model assumptions, not measurements of VS11. |
| Packaging contract | The real packer accepts the board CRT, rejects the generic rc3 CRT and rejects a changed loop branch. |
| Native erase relocation | Every instruction in the exact 87-byte OEM leaf is decoded; all relative branch targets remain on instruction boundaries inside the copied span; it has no absolute call and ends with `RET`. This does not execute flash erase. |
| Trial marker guard | All 64 bytes zero reaches the CRT; each of 64 individual nonzero marker positions reaches the failure loop. |
| Optional generic C52 | Runs the entire linked CRT, checks XSEG clearing before ordinary C initializers, checks XINIT again at `main`, and checks XRAM guards before/after the application and at the USB FIFO. |
| Optional early entry | Starts the real packed entry with hostile inherited bank/SP/IRQ/XBUS state and stops **before** the native erase routine. Verifies bank 0, call frame at SP `0x22`, erase arguments `0x27C0`, disabled interrupts, selected DPTR0 and disabled automatic DPTR increment. |

`startup-report.json` binds results to the IHX, MAP, legacy inputs, stock ROM,
packer and runner hashes. With uCsim, `full-crt.sim/.log` and
`entry-before-erase.sim/.log` retain commands and raw observations.

Passing does not establish VS11 peripheral behavior, interrupt timing, flash
erase/program behavior, actual USB enumeration or physical keyboard scanning.
The generic CPU stack measurement covers only this CRT path, not worst-case
main/IRQ nesting. The rc3 hardware cause remains unproven until separately
authorized device observations resolve it.

See `docs/RC4-STARTUP-INVESTIGATION-RU.md` at the repository root for the
investigation and the separate read-only `AKBT` startup diagnostic contract.
