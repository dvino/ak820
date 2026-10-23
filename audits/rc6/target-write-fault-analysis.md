# RC6 encoder write fault

Date: 2026-10-23. This is an offline analysis of saved captures and emitted code. No USB command, build, reset, restore or flash was performed for this report. The report follows the owner's supplied plain-language guidance; no style retrieval tool was available.

## What failed

The saved FD01 result reports stage 12 (`target_write`), page 25, and the last IAP operation `9A` at `CD40`, with status `40` before and after. The installed program and manifest still match RC6 SHA256 `f90a40dcad7364f2278fa5daf2bfa444060140a71401b2c4595bb035aff6aebe` according to the post-fault capture.

This identifies a readback failure, rather than a false return from erase or block programming. In `ak820_nvm.c`, `write_page()` calls erase, then block program, then compares CODE bytes. Reaching the recorded `9A` means erase returned true. The recorded `40`/`40` makes block programming return true under the emitted predicate `(before & 0x40) && !(status & 0x02)`. The remaining failure branch is the byte comparison. The final3 `dce/ak820_nvm.asm` and `dce/ak820_flash.asm` preserve this control flow and predicate.

Status success therefore did not establish that the target page was erased or replaced.

## Exact saved-ROM difference

Inputs:

- `host/runs/rc6-encoder-probe-1792746171779534100/before-rom.bin`
- `host/runs/20261023-rc6-post-encoder-fault-readonly/rom.bin`
- The adjacent `report.json` files and the probe's `transport.jsonl`.

Only 19 bytes differ across the full 65536-byte captures. All changed bytes were zero before:

| Address | After |
| --- | --- |
| EF03, EF05, EF07 | AA, BB, BC |
| EF09, EF0B, EF0D, EF0F, EF11, EF13, EF15, EF17 | 01 each |
| EF40, EF41, EF43, EF44, EF45, EF46, EF47, EF48 | A5, 19, 2C, ED, E6, FF, D3, 12 |

`CD40..CD7F` is exactly unchanged. Its first bytes are `00 A9 00 AA 00 BB 00 BC`. The journal page at `EF00` starts `00 00 00 AA 00 BB 00 BC`. Only the desired target byte at `CD41` differs from the old page (`A9` to `00`). The captured journal header is committed and valid, with page 25 and CRC16 `ED2C`; journal data has the matching CRC. The post-fault second read found NVM and journal stable.

These observations fit an ineffective erase followed by a bit-setting program: programming the desired zero cannot clear the old `A9`. They also fit a protected target range where both operations have no effect. They do not prove either mechanism. Successful journal preparation began from all-zero pages, so it does not demonstrate that any nonzero page was erased.

## Compare with OEM sequences

`releases/rc3/reports/oem-page-program-disassembly.txt` supplies the OEM block program at `1230..123D` and erase at `1694..16F2`. The erase helper uses `ROM_BUF_MOD=80`, `ROM_DAT_BUF=00`, opcode `A6`, address low masked to a 64-byte boundary, and CODE_WE `08` outside `F000..F3FF`. Thus `80` is backed by an OEM erase sequence; the unsupported old single-byte *program* mode must not be confused with erase mode.

RC6 uses the same mode, value, opcode, aligned address and CODE_WE selection for `CD40`. The emitted RC6 erase still differs in instruction ordering: it saves/loads status through XDATA using DPTR between reading ROM_CTRL, testing bit 6 and writing the opcode. The OEM helper keeps those values in registers and reads/tests/writes/reads ROM_CTRL consecutively. RC6's naked block program intentionally removed the corresponding DPTR hazard for opcode `9A`; erase remains ordinary C. This is a concrete comparison target, not proof that `A6` depends on DPTR or timing.

The retained ROM bytes at OEM address `E650` cannot be inspected in this RC6 application capture: that range is zero. Use the existing OEM disassembly or the separately held original ROM when comparing the copied helper and its relocated address. Do not mistake this RC6 zero region for the OEM routine.

## Next offline work

1. Extend the host flash model with an erase that reports `40` but leaves the old page unchanged. Confirm the current result: stage 12, unchanged target, valid retained journal. This catches the exact observed limitation without claiming silicon emulation.
2. Add separate erase readback before target programming in a proposed code change. Record erase status, first nonzero address/value and first program mismatch separately. That would distinguish an ineffective erase from a later program failure on a future explicitly authorized test.
3. Compare a register-only erase leaf with the OEM erase sequence and inspect emitted instructions. Preserve the address, mode, CODE_WE and interrupt behavior; do not infer that matching assembly is a device PASS.
4. Review exact silicon protection and erase-execution rules against the private original ROM and register definitions. In particular, check whether application-origin erase has range, instruction-location, DPTR, unlock-window or command-order constraints. Current captures cannot choose among these explanations.

No code change or model run is claimed here. No automatic restore is proposed.

## Restart risk

The record authorizes startup replay in the current implementation: `eeprom_driver_init()` clears the RAM fault latch, then `recover_journal()` accepts this header and CRC and calls `write_page(CD40)`. A reset or cold boot therefore initiates another erase/program attempt without another host setter. If it succeeds, the temporary clockwise `KC_NO` becomes persistent and the header is cleaned. If it fails, recovery records stage 3 (`recovery_write`) and retains the journal. An unexpected partial erase/program could also change the target page before a later failure.

The temporary value may already be visible in the dirty RAM page cache while the direct CODE capture still shows `A9`. Neither capture establishes current physical encoder behavior. Preserve power/state and avoid encoder rotation, reset and recovery attempts until the owner and lead choose the next separately authorized operation.
