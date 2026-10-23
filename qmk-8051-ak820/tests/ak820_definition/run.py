#!/usr/bin/env python3
"""Exercise the linked Vial definition reader and the repository GUI decoder.

The CPU receives fixed packets in simulated XDATA. The unmodified GUI method
then reads the captured responses through a fake transport. No USB is opened.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import re
import struct
import types

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
spec = importlib.util.spec_from_file_location("ak820_emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def gui_decode(responses):
    """Run the real reload_layout body and real KLE parser, mocking only HID."""
    base = REPO / "src/main/python"
    source = base / "protocol/keyboard_comm.py"
    tree = ast.parse(source.read_text())
    method = next(node for cls in tree.body if isinstance(cls, ast.ClassDef)
                  for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "reload_layout")
    kle_path = base / "kle_serial.py"
    kle_spec = importlib.util.spec_from_file_location("ak820_gui_kle", kle_path)
    kle = importlib.util.module_from_spec(kle_spec)
    kle_spec.loader.exec_module(kle)
    constants = base / "protocol/constants.py"
    namespace = {"struct": struct, "json": json, "lzma": lzma, "KleSerial": kle.Serial}
    exec(compile(constants.read_text(), str(constants), "exec"), namespace)
    namespace["MSG_LEN"] = 32
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[])), str(source), "exec"), namespace)
    requests = []

    def send(device, command, retries):
        requests.append(command.hex())
        assert command[0] == 0xFE and retries == 20
        key = (command[1], int.from_bytes(command[2:6], "little") if command[1] == 2 else 0)
        return responses[key]

    client = types.SimpleNamespace(dev=None, usb_send=send, reload_via_protocol=lambda: None,
                                   check_protocol_version=lambda: None, encoderpos={}, encoder_count=0, rowcol={})
    namespace["reload_layout"](client)
    return client, {"method_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "kle_source_sha256": hashlib.sha256(kle_path.read_bytes()).hexdigest(),
                    "constants_sha256": hashlib.sha256(constants.read_bytes()).hexdigest(),
                    "requests": requests}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--s51", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    generated = list(fw.build.glob("obj_*/src/vial_generated_keyboard_definition.h"))
    if len(generated) != 1:
        raise ValueError("Expected exactly one compiler input definition header")
    blob = bytes(int(value, 16) for value in re.findall(r"0x([0-9A-Fa-f]{2})", generated[0].read_text()))
    linked_blob = bytes(fw.code[fw.address("_keyboard_definition") + i] for i in range(len(blob)))
    assert linked_blob == blob, "Linked definition differs from generated input"
    pages = (len(blob) + 31) // 32
    invalid = {pages, pages + 1, 31, 2047, 2048, 65535, 0xFFFF0000, 0xFFFFFFFF}
    invalid.update((1 << bit) | low for bit in range(16, 32) for low in (0, 1, pages - 1, 65535))
    invalid = sorted(page for page in invalid if page >= pages)
    requests = [(0, 0, 32), (1, 0, 32)]
    requests += [(2, page, 32) for page in [*range(pages), *invalid]]
    requests += [(cmd, 0, size) for cmd in (0, 1, 2) for size in (0, 1, 31, 33, 255)]
    commands = [f"run {fw.address('__sdcc_gsinit_startup'):#x} {fw.address('_main'):#x}"]
    fixtures = []
    for cmd, page, size in requests:
        packet = [0xFE, cmd, *page.to_bytes(4, "little"), *([0xA5] * 26)]
        reply = packet.copy()
        if size == 32 and cmd == 1:
            reply[:4] = len(blob).to_bytes(4, "little")
        elif size == 32 and cmd == 2 and page < pages:
            chunk = blob[page * 32:(page + 1) * 32]
            reply[:len(chunk)] = chunk
        label = f"command_{cmd}_page_{page:08x}_length_{size}@"
        commands += fw.write("_raw_buffer", packet) + fw.write("_vial_handle_cmd_PARM_2", [size])
        commands += fw.call("_vial_handle_cmd", fw.address("_raw_buffer"))
        commands += fw.dump_symbol(label, "_raw_buffer", 32)
        fixtures.append((cmd, page, size, label, reply))
    log, stack = fw.execute("definition-pages", commands)
    tests, responses = [], {}
    for cmd, page, size, label, reply in fixtures:
        actual = fw.extract(log, label, fw.address("_raw_buffer"), 32)
        passed = actual[:4] == [6, 0, 0, 0] if cmd == 0 and size == 32 else actual == reply
        tests.append({"label": label, "pass": passed, "actual": actual,
                      "expected": reply if cmd != 0 or size != 32 else "protocol 6; remaining ID bytes replayed into GUI"})
        if size == 32 and (cmd != 2 or page < pages):
            responses[(cmd, page)] = bytes(actual)
    client, gui = gui_decode(responses)
    definition_path = ROOT / "keyboards/ajazz/ak820/keymaps/vial/vial.json"
    source_json = json.loads(definition_path.read_text())
    assert client.definition == source_json
    assert len(client.keys) == 83 and len(client.encoders) == 2
    by_matrix = {(key.row, key.col): key for key in client.keys}
    f12, delete, backspace = by_matrix[(12, 0)], by_matrix[(14, 2)], by_matrix[(13, 1)]
    assert (f12.x, f12.width) == (12.75, 1)
    assert (delete.x, delete.width) == (14.0, 1)
    assert delete.x + delete.width == backspace.x + backspace.width == 15.0
    assert delete.x - (f12.x + f12.width) == 0.25
    nav_column = [(13, 0), (15, 1), (15, 2), (14, 3), (15, 3)]
    assert [by_matrix[matrix].x for matrix in nav_column] == [15.5] * 5
    assert [by_matrix[matrix].width for matrix in nav_column] == [1] * 5
    assert by_matrix[(15, 5)].x == 15.25  # Keep Right arrow in place.
    rotations = sorted(client.encoders, key=lambda key: key.encoder_dir)
    assert [(key.encoder_idx, key.encoder_dir, key.x, key.y) for key in rotations] == [
        (0, 0, 16.75, 0), (0, 1, 18.0, 0)
    ]
    assert rotations[0].x - (by_matrix[(13, 0)].x + by_matrix[(13, 0)].width) == 0.25
    assert rotations[1].x - (rotations[0].x + rotations[0].width) == 0.25
    report = {"result": "PASS" if all(item["pass"] for item in tests) else "FAIL",
              "hardware_validated": False, "level": "linked C52 Vial reader + actual GUI reload_layout/KLE, mocked HID",
              "ihx_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "within_release_code_windows": all(0x28A0 <= address < 0x3000 or 0x3027 <= address < 0xC700 for address in fw.code),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_json_sha256": hashlib.sha256(definition_path.read_bytes()).hexdigest(),
              "definition_bytes": len(blob), "definition_sha256": hashlib.sha256(blob).hexdigest(),
              "valid_pages": pages, "gui": gui, "gui_keys": len(client.keys), "gui_encoder_directions": len(client.encoders),
              "initial_sp": fw.initial_sp, **stack, "tests": tests}
    (fw.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("result", "definition_bytes", "valid_pages", "gui_keys", "gui_encoder_directions", "tested_stack_bytes")}))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
