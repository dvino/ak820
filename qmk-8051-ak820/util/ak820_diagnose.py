#!/usr/bin/env python3
"""Read-only AK820 CODE capture and offline NVM/journal analysis.

`analyze` never opens HID. `capture` sends only FD00 CODE reads, plus FD01
when an explicitly supplied, diagnostic-capable IHX/MAP pair is bound by its
build report and exactly matches CODE.
It never sends a VIA getter/setter, erase, reset or loader command. Partial
captures and the request/response trace are retained on failure.
"""
from __future__ import annotations

import argparse
import binascii
import json
from pathlib import Path
import sys
import time

from pack_ak820 import (APP_END, APP_START, BUILD_ID, CODE_END, CODE_START,
                       EXTENSION_BUILD_ID, LOW_END, LOW_START, MANIFEST_START, NVM_END, NVM_START,
                       digest, read_ihex, read_symbols, verify_payload, nvm_layout)

NVM_FAULT_NAMES = (
    'none', 'recovery_page', 'recovery_crc', 'recovery_write', 'recovery_cleanup',
    'header_erase', 'header_zero', 'journal_write', 'metadata_program',
    'metadata_readback', 'commit_program', 'commit_readback', 'target_write',
    'cleanup', 'write_range', 'batch_overflow', 'schema_mismatch',
)


def key_address(layer: int, row: int, column: int, *, build_id=BUILD_ID) -> int:
    layers = nvm_layout(build_id)['layers']
    if not (0 <= layer < layers and 0 <= row < 16 and 0 <= column < 8):
        raise ValueError(f"Key coordinates require layer 0..{layers-1}, row 0..15, column 0..7")
    return NVM_START + 0x40 + layer * 0x100 + row * 0x10 + column * 2


def journal_report(rom: bytes) -> dict:
    data = rom[NVM_END:NVM_END + 64]
    header = rom[NVM_END + 64:MANIFEST_START]
    result = {"header_hex": header.hex(), "data_hex": data.hex(),
              "data_crc16": binascii.crc_hqx(data, 0xFFFF),
              "data_nonzero": any(data), "header_empty": not any(header)}
    if not any(header):
        result["state"] = "empty_header"
        result["meaning"] = "No committed redo record; retained journal data is permitted."
        return result
    committed = header[0] == 0xA5 and all(header[i] ^ header[i + 4] == 0xFF for i in range(1, 5))
    result["commit_and_inverse_valid"] = committed
    if not committed:
        result["state"] = "uncommitted_or_torn_header"
        result["meaning"] = "Not a valid committed record; preserve it for diagnosis."
        return result
    page = int.from_bytes(header[1:3], "little")
    expected_crc = int.from_bytes(header[3:5], "little")
    result.update(page=page, expected_crc16=expected_crc,
                  data_crc_valid=expected_crc == result["data_crc16"])
    if page >= (NVM_END - NVM_START) // 64:
        result["state"] = "committed_invalid_page"
    elif not result["data_crc_valid"]:
        result["state"] = "committed_invalid_data_crc"
    else:
        address = NVM_START + page * 64
        matches = rom[address:address + 64] == data
        result.update(target_address=address, target_matches_journal=matches,
                      state="committed_target_matches" if matches else "committed_target_differs")
    result["meaning"] = "Journal is not clean; this report neither replays nor erases it."
    return result


def analyze(rom: bytes, expected: bytes | None = None, key=None, *,
            target_build_id=BUILD_ID, allow_legacy=True) -> dict:
    if len(rom) != 65536:
        raise ValueError("A full 65536-byte CODE dump is required; partial captures are not full ROMs")
    schema = int.from_bytes(rom[NVM_START + 37:NVM_START + 40], "little")
    result = {"format": "ak820-code-diagnostic-1", "rom_bytes": len(rom),
              "rom_sha256": digest(rom), "eeprom_schema": schema,
              "expected_schema": target_build_id, "schema_matches": schema == target_build_id,
              "trial_marker_all_zero": not any(rom[0x27C0:APP_START]),
              "journal": journal_report(rom), "physical_mutations_sent": 0,
              "persistence_after_restart": "not established by this capture",
              "ram_cache": "not read; key values below come directly from CODE"}
    if key is not None:
        address = key_address(*key, build_id=schema)
        result["key"] = {"layer": key[0], "row": key[1], "column": key[2],
                         "code_address": address, "bytes_hex": rom[address:address + 2].hex(),
                         "keycode": int.from_bytes(rom[address:address + 2], "big")}
    if expected is not None:
        metadata = verify_payload(expected, target_build_id=target_build_id,
                                  allow_legacy=allow_legacy)
        # NVM and journal are intentionally allowed to change after installation.
        regions = ((APP_START, CODE_END), (MANIFEST_START, APP_END))
        mismatches = [a for lo, hi in regions for a in range(lo, hi)
                      if rom[a] != expected[a - APP_START]]
        result["expected_image"] = {"sha256": digest(expected), "trial": metadata["trial"],
                                    "code_entry_manifest_match": not mismatches,
                                    "mismatch_count": len(mismatches),
                                    "first_mismatches": mismatches[:16]}
    return result


def decode_status(reply: bytes) -> dict:
    if len(reply) != 32 or reply[:4] != bytes((0xFD, 1, 1, 0xA8)):
        raise ValueError("Unexpected FD01 diagnostic reply/version")
    if any(reply[22:]):
        raise ValueError("Nonzero reserved FD01 fields")
    if any(reply[i] not in (0, 1) for i in (4, 5, 6, 11, 17, 18)):
        raise ValueError("Invalid FD01 boolean field")
    return {"version": reply[2], "storage_failed": bool(reply[4]),
            "page_valid": bool(reply[5]), "page_dirty": bool(reply[6]),
            "batch_depth": reply[7],
            "cached_page": int.from_bytes(reply[8:10], "little") if reply[5] else None,
            "first_failure_stage": reply[10],
            "first_failure_stage_name": NVM_FAULT_NAMES[reply[10]] if reply[10] < len(NVM_FAULT_NAMES) else 'unknown',
            "last_iap": {"valid": bool(reply[11]), "operation": reply[12],
                         "status_before": reply[13], "status_after": reply[14],
                         "address": int.from_bytes(reply[15:17], "little")},
            "vial_unlocked": bool(reply[17]), "vial_unlock_in_progress": bool(reply[18]),
            "usb_enum_status": reply[19], "usb_sleep_status": reply[20],
            "raw_state_during_diagnostic": reply[21]}


def diagnostic_build(ihx: Path | None, mapfile: Path | None, build_report: Path | None):
    if ihx is None and mapfile is None and build_report is None:
        return None
    if ihx is None or mapfile is None or build_report is None:
        raise ValueError("FD01 requires --ihx, --map and --build-report; FD00 needs none of them")
    # The symbol alone is insufficient: a new MAP mixed with an old IHX can
    # point into otherwise valid old CODE. Bind both files to one build first.
    report = json.loads(build_report.read_text(encoding="utf-8"))
    if report.get("code_window") != [CODE_START, CODE_END]:
        raise ValueError("Unexpected diagnostic build CODE window")
    for path, suffix in ((ihx, ".ihx"), (mapfile, ".map")):
        artifacts = [item for item in report.get("artifacts", [])
                     if isinstance(item, dict) and str(item.get("path", "")).endswith(suffix)]
        if len(artifacts) != 1 or artifacts[0].get("sha256") != digest(path.read_bytes()):
            raise ValueError("IHX/MAP pair does not match the build report")
    symbols = read_symbols(mapfile)
    code = read_ihex(ihx)
    address = symbols.get("_ak820_nvm_diagnostic")
    if address is None or address not in code:
        raise ValueError("This build does not declare the FD01 diagnostic implementation")
    if not code or any(not (LOW_START <= a < LOW_END or CODE_START <= a < CODE_END) for a in code):
        raise ValueError("Diagnostic IHX has bytes outside the permitted CODE windows")
    return code


def capture(output: Path, expected: bytes | None = None, code=None, key=None, app_factory=None, *,
            target_build_id=BUILD_ID, allow_legacy=True) -> dict:
    # Validate all local inputs before opening the keyboard or creating output.
    if expected is not None:
        verify_payload(expected, target_build_id=target_build_id,
                       allow_legacy=allow_legacy)
    if key is not None:
        key_address(*key, build_id=target_build_id)
    if code is not None and not code:
        raise ValueError("Empty expected diagnostic CODE")
    output.mkdir(parents=True, exist_ok=False)
    report = {"format": "ak820-code-capture-1", "completed": False,
              "physical_mutations_sent": 0, "bytes_captured": 0,
              "fd01_requested": False}
    partial = output / "rom-prefix.bin"
    trace_path = output / "transport.jsonl"
    app = None
    rom = bytearray()
    try:
        if app_factory is None:
            from ak820_tool import Application
            app_factory = Application
        app = app_factory()
        if app.native:
            raise ValueError("Expected the running AK820 Raw HID application, not native firmware")
        with partial.open("xb") as raw_file, trace_path.open("x", encoding="utf-8") as trace:
            def exchange(packet):
                started = time.monotonic()
                row = {"request_hex": packet.hex()}
                try:
                    reply = bytes(app.raw(packet))
                    row["reply_hex"] = reply.hex()
                    return reply
                except Exception as error:
                    row["error"] = f"{type(error).__name__}: {error}"
                    raise
                finally:
                    row["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
                    trace.write(json.dumps(row) + "\n")
                    trace.flush()

            def read_code(address, size):
                result = bytearray()
                for delta in range(0, size, 27):
                    count = min(27, size - delta)
                    at = address + delta
                    request = bytes((0xFD, 0, at >> 8, at & 255, count)) + bytes(27)
                    reply = exchange(request)
                    if len(reply) != 32 or reply[:5] != request[:5]:
                        raise ValueError("Mismatched FD00 reply; capture stopped without retry")
                    result.extend(reply[5:5 + count])
                return bytes(result)

            for address in range(0, 65536, 27):
                block = read_code(address, min(27, 65536 - address))
                raw_file.write(block)
                raw_file.flush()
                rom.extend(block)
                report["bytes_captured"] = len(rom)
            raw_file.close()
            partial.rename(output / "rom.bin")
            report["analysis"] = analyze(bytes(rom), expected, key,
                                         target_build_id=target_build_id,
                                         allow_legacy=allow_legacy)
            # Detect edits or a still-running transaction during the long dump.
            stable = read_code(NVM_START, MANIFEST_START - NVM_START) == rom[NVM_START:MANIFEST_START]
            report["nvm_and_journal_stable_on_second_read"] = stable
            if code is not None:
                matches = all(rom[address] == value for address, value in code.items())
                report["diagnostic_ihx_matches"] = matches
                if not matches:
                    raise ValueError("CODE differs from diagnostic build; FD01 was not sent")
                if not stable:
                    raise ValueError("NVM/journal changed during capture; FD01 was not sent")
                report["fd01_requested"] = True
                report["status"] = decode_status(exchange(bytes((0xFD, 1)) + bytes(30)))
            report["completed"] = True
            if not stable:
                report["warning"] = "Settings changed during capture; do not treat this as one coherent snapshot"
    except Exception as error:
        report["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        if app is not None:
            try:
                app.close()
            except Exception as error:
                report["close_error"] = f"{type(error).__name__}: {error}"
        (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    offline = sub.add_parser("analyze", help="Analyze a saved full ROM; never opens HID")
    offline.add_argument("rom", type=Path)
    live = sub.add_parser("capture", help="FD00 reads only; matching IHX/MAP/build report enables FD01")
    live.add_argument("--output", type=Path, required=True)
    live.add_argument("--ihx", type=Path)
    live.add_argument("--map", dest="mapfile", type=Path)
    live.add_argument("--build-report", type=Path)
    for item in (offline, live):
        item.add_argument("--expected-trial", type=Path)
        item.add_argument("--key", nargs=3, type=int, metavar=("LAYER", "ROW", "COLUMN"))
        item.add_argument("--target-build-id", type=lambda value: int(value, 0),
                          choices=(BUILD_ID, EXTENSION_BUILD_ID), default=BUILD_ID)
    args = parser.parse_args()
    expected = args.expected_trial.read_bytes() if args.expected_trial else None
    if expected is not None and not verify_payload(expected, target_build_id=args.target_build_id,
                                                    allow_legacy=True)["trial"]:
        raise ValueError("--expected-trial must identify a trial payload")
    if args.command == "analyze":
        result = analyze(args.rom.read_bytes(), expected, args.key,
                         target_build_id=args.target_build_id)
    else:
        code = diagnostic_build(args.ihx, args.mapfile, args.build_report)
        result = capture(args.output, expected, code, args.key,
                         target_build_id=args.target_build_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
