#!/usr/bin/env python3
"""Exercise busy-endpoint release/retry ownership in the linked SDCC image.

The C52 fixture supplies endpoint completion, reset and suspend state. It never
opens USB and does not model the real SIE, scheduling or electrical timing.
"""
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


def ready(endpoint):
    return [emitted.memory("xram", 0x2200 + endpoint, [0x12])]


def post(fw):
    return fw.call("_protocol_post_task")


def case(fw, name, setup, observations):
    commands = list(setup)
    for label, address, expected, steps in observations:
        commands += steps + fw.dump(label + "@", "xram", address, len(expected))
    log, stack = fw.execute(name, commands)
    results = []
    for label, address, expected, _ in observations:
        actual = fw.extract(log, label + "@", address, len(expected))
        results.append({"label": label, "address": address, "expected": expected,
                        "actual": actual, "pass": actual == expected})
    return {"name": name, "pass": all(item["pass"] for item in results),
            "observations": results, **stack}


def cases(fw):
    blank, a, b = [0] * 8, [0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0]
    fifo1, fifo2 = 0x1040, 0x1080
    init = fw.initialize()
    release = init + fw.call("_register_code", 4) + fw.call("_unregister_code", 4)
    yield case(fw, "keyboard-release-after-timeout", release, [
        ("busy_keeps_accepted_down", fifo1, a, post(fw)),
        ("current_is_released", fw.address("_actual_keyboard_report"), blank, []),
        ("late_in_publishes_release", fifo1, blank, ready(1) + post(fw)),
        ("release_queued", 0x2201, [0x10], []),
    ])
    yield case(fw, "keyboard-latest-pending-wins", init + fw.call("_register_code", 4), [
        ("intermediate_not_published", fifo1, a,
         fw.call("_register_code", 5) + fw.call("_unregister_code", 4) + post(fw)),
        ("latest_b_published", fifo1, b, ready(1) + post(fw)),
    ])
    for name, function, report_id, usage in [
        ("consumer", "_host_consumer_send", 4, 0xE9),
        ("system", "_host_system_send", 3, 0x81),
    ]:
        down = [report_id, usage, 0]
        yield case(fw, name + "-release-after-timeout", init + fw.call(function, usage), [
            ("busy_keeps_accepted_down", fifo2, down, fw.call(function, 0) + post(fw)),
            ("late_in_publishes_release", fifo2, [report_id, 0, 0], ready(2) + post(fw)),
        ])
    yield case(fw, "shared-independent-pending-releases", init + fw.call("_host_system_send", 0x81), [
        ("both_releases_wait", fifo2, [3, 0x81, 0], fw.call("_host_consumer_send", 0xE9) +
         fw.call("_host_system_send", 0) + fw.call("_host_consumer_send", 0) + post(fw)),
        ("system_release", fifo2, [3, 0, 0], ready(2) + post(fw)),
        ("consumer_release_next", fifo2, [4, 0, 0], ready(2) + post(fw)),
    ])
    yield case(fw, "consumer-latest-pending-wins", init + fw.call("_host_consumer_send", 0xE9), [
        ("only_latest_usage_retried", fifo2, [4, 0xEA, 0],
         fw.call("_host_consumer_send", 0) + fw.call("_host_consumer_send", 0xEA) + ready(2) + post(fw)),
    ])
    nkro_blank = [6, 0] + [0] * 30
    nkro_down = [6, 0, 16] + [0] * 29
    yield case(fw, "nkro-release-after-timeout", init + fw.write("_keymap_config", [0x80, 0]) +
               fw.call("_register_code", 4) + fw.call("_unregister_code", 4), [
        ("busy_keeps_nkro_down", fifo2, nkro_down, post(fw)),
        ("nkro_release_retried", fifo2, nkro_blank, ready(2) + post(fw)),
    ])
    reset_setup = init + fw.call("_register_code", 4) + fw.call("_register_code", 5)
    yield case(fw, "reset-discards-stale-pending", reset_setup, [
        ("reset_guard_preserves_old_fifo", fifo1, a, fw.write("_keyboard_reset", [1]) + ready(1) + post(fw)),
        ("no_stale_publication", 0x2201, [0x12], []),
        ("cleanup_publishes_release", fifo1, blank, fw.call("_protocol_pre_task") + post(fw)),
        ("latest_cache_reset", fw.address("_last_keyboard_report"), blank, []),
    ])
    yield case(fw, "suspend-resume-discards-stale-pending", reset_setup, [
        ("suspended_no_publication", 0x2201, [0x12], fw.write("_USB_SleepStatus", [2]) + ready(1) + post(fw)),
        ("resume_waits_for_cleanup", 0x2201, [0x12],
         fw.write("_USB_SleepStatus", [0]) + fw.write("_keyboard_reset", [1]) + post(fw)),
        ("resume_clears_latest", fifo1, blank, fw.call("_protocol_pre_task") + post(fw)),
    ])
    yield case(fw, "unconfigured-no-publication", release, [
        ("not_configured", 0x2201, [0x12], fw.write("_USB_EnumStatus", [0]) + ready(1) + post(fw)),
        ("configured_retries_latest", fifo1, blank, fw.write("_USB_EnumStatus", [1]) + post(fw)),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--s51", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    results = list(cases(fw))
    report = {"result": "PASS" if all(item["pass"] for item in results) else "FAIL",
              "hardware_validated": False, "level": "linked SDCC C52; simulated endpoint completion/reset/suspend",
              "ihx_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "map_sha256": hashlib.sha256((fw.build / "ajazz_ak820_vial.map").read_bytes()).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "emitted_helper_sha256": hashlib.sha256((ROOT / "tests/ak820_emitted/run.py").read_bytes()).hexdigest(),
              "within_release_code_windows": all(0x28A0 <= address < 0x3000 or 0x3027 <= address < 0xC700 for address in fw.code),
              "initial_sp": fw.initial_sp, "stack_capacity": fw.stack_capacity, "tests": results}
    (fw.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"result": report["result"], "tests": len(results),
                      "passed": sum(item["pass"] for item in results),
                      "max_tested_stack_bytes": max(item["tested_stack_bytes"] for item in results),
                      "report": str(fw.output / "results.json")}))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
