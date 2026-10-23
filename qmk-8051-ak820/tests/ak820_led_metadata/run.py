#!/usr/bin/env python3
"""Check every VialRGB LED metadata response against the immutable RC4 layout."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    fixture_path = Path(__file__).with_name("rc4-metadata.json")
    fixture = json.loads(fixture_path.read_text())
    assert len(fixture["entries"]) == 82
    commands, expected = fw.initialize(), []
    for led, length in [*[(i, 32) for i in range(82)],
                        *[(i, 32) for i in (82, 255, 256, 65535)],
                        *[(i, size) for i in (0, 81) for size in (0, 31, 33, 255)]]:
        packet = [7, 0x44, led & 255, led >> 8] + [0xA5] * 28
        reply = packet.copy()
        if length == 32 and led < 82:
            reply[2:7] = fixture["entries"][led]
        label = f"led_{led}_length_{length}@"
        commands += fw.write("_raw_buffer", packet) + fw.write("_vialrgb_get_value_PARM_2", [length])
        commands += fw.call("_vialrgb_get_value", fw.address("_raw_buffer"))
        commands += fw.dump_symbol(label, "_raw_buffer", 32)
        expected.append((label, reply))
    log, stack = fw.execute("all-led-metadata", commands)
    results = []
    for label, reply in expected:
        actual = fw.extract(log, label, fw.address("_raw_buffer"), 32)
        results.append({"label": label, "pass": actual == reply, "expected": reply, "actual": actual})
    report = {"result": "PASS" if all(item["pass"] for item in results) else "FAIL", "hardware_validated": False,
              "level": "linked SDCC C52; real VialRGB handler and CODE tables; no physical USB/DMA",
              "ihx_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
              "reference": {key: value for key, value in fixture.items() if key != "entries"},
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "initial_sp": fw.initial_sp, **stack, "tests": results}
    (fw.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"result": report["result"], "tests": len(results), "tested_stack_bytes": stack["tested_stack_bytes"],
                      "report": str(fw.output / "results.json")}))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
