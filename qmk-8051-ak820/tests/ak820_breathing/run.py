#!/usr/bin/env python3
"""Offline C52 checks of breathing in an existing linked SDCC image; never builds or opens USB."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)
Firmware, memory = emitted.Firmware, emitted.memory


def curve():
    # Independent existing 256-entry reference, not interpolation's own oracle.
    text = (ROOT / "quantum/led_tables.c").read_text()
    return [int(v) for v in re.search(r"CIE1931_CURVE\[256\].*?\{(.*?)\};", text, re.S)[1].split(",") if v.strip()]


def sine(theta):
    theta &= 255
    offset = ((255 - theta) if theta & 64 else theta) & 63
    section, fraction = offset // 16, (offset % 16) + bool(theta & 64)
    base, slope = ((0, 49), (49, 41), (90, 27), (117, 10))[section]
    value = base + slope * fraction // 16
    return 128 - value if theta & 128 else 128 + value


def hsv(h, s, v):
    if not s:
        return [v] * 3
    region = h * 6 // 255
    rem = ((h * 2 - region * 85) * 3) & 255
    p = v * (255 - s) // 256
    q = v * (255 - s * rem // 256) // 256
    t = v * (255 - s * (255 - rem) // 256) // 256
    return ([v, t, p], [q, v, p], [p, v, t], [p, q, v], [t, p, v], [v, p, q], [v, t, p])[region]


def helper(fw):
    commands = fw.initialize()
    for value in range(161):
        commands += fw.call("_breathing_cie", value) + fw.dump(f"v{value:03}", "sfr", 0x82, 1)
    log, stack = fw.execute("breathing-helper", commands)
    actual = [fw.extract(log, f"v{i:03}", 0x82, 1)[0] for i in range(161)]
    expected = curve()[:161]
    error = max(abs(a - b) for a, b in zip(actual, expected))
    ok = error <= 1 and actual[0] == 0 and actual[160] == expected[160] and actual == sorted(actual)
    return {"name": "linked_helper_all_supported_values", "pass": ok, "value_range": [0, 160],
            "max_full_curve_error": error, "values": actual, **stack}, actual


def frames(fw, corrected):
    commands = fw.initialize()
    # Each requested phase is injected before the production speed increment.
    # Timer values cross 16-bit wrap; source timer_read ABI is also called below.
    cases = [(p, h, s) for p in (0, 1, 63, 64, 95, 127, 128, 129, 191, 255)
             for h, s in ((0, 255), (85, 255), (170, 255), (43, 128), (0, 0))]
    for number, (phase, hue, sat) in enumerate(cases):
        commands += fw.write("_rgb_matrix_config", [9, hue, sat, 160, 96, 255, 0, 0])
        commands += fw.write("_phase", ((phase * 256 - 128) & 65535).to_bytes(2, "little"))
        commands += fw.write("_rendering", [0]) + fw.write("_frame_at", [0xe0, 0xff])
        commands += fw.clock(0x10020) + fw.call("_timer_read") + fw.dump(f"timer{number:03}", "sfr", 0x82, 2)
        # Sentinel records make exactly which LEDs changed observable.
        commands += [f"fill xram {fw.address('_ak820_led_dma'):#x} {fw.address('_ak820_led_dma')+511:#x} 0x55"]
        commands += fw.call("_rgb_matrix_task")
        commands += fw.dump_symbol(f"index{number:03}", "_led_index", 1)
        commands += fw.dump_symbol(f"phase{number:03}", "_frame_phase", 1)
        commands += fw.dump(f"partial{number:03}", "xram", fw.address("_ak820_led_dma"), 512)
        for _ in range(10):
            commands += fw.call("_rgb_matrix_task")
        commands += fw.dump_symbol(f"done{number:03}", "_rendering", 1)
        commands += fw.dump(f"full{number:03}", "xram", fw.address("_ak820_led_dma"), 512)
    log, stack = fw.execute("breathing-frames", commands)
    observations, ok, max_error = [], True, 0
    base = fw.address("_ak820_led_dma")
    for number, (phase, hue, sat) in enumerate(cases):
        raw = 160 * sine(phase - 64) // 256
        channels = hsv(hue, sat, corrected[raw])
        expected = [255 if any(channels) else 0] + channels
        reference = hsv(hue, sat, curve()[raw])
        partial = fw.extract(log, f"partial{number:03}", base, 512)
        full = fw.extract(log, f"full{number:03}", base, 512)
        indices = fw.extract(log, f"index{number:03}", fw.address("_led_index"), 1)
        phase_out = fw.extract(log, f"phase{number:03}", fw.address("_frame_phase"), 1)
        timer = fw.extract(log, f"timer{number:03}", 0x82, 2)
        done = fw.extract(log, f"done{number:03}", fw.address("_rendering"), 1)
        channels_ok = True
        for led in range(82):
            offset = fw.led_address(led) - base
            channels_ok &= full[offset:offset + 4] == expected
            channels_ok &= partial[offset:offset + 4] == (expected if led < 8 else [0x55] * 4)
        error = max(abs(a-b) for a, b in zip(expected[1:], reference))
        max_error = max(max_error, error)
        passed = channels_ok and indices == [8] and phase_out == [phase] and timer == [0x20, 0] and done == [0] and error <= 1
        ok &= passed
        observations.append({"phase": phase, "hue": hue, "saturation": sat, "raw_v": raw,
                             "dma_record": expected, "pass": bool(passed)})
    return {"name": "linked_renderer_82_led_frames_and_eight_led_tasks", "pass": bool(ok),
            "frames": observations, "max_full_curve_channel_error": max_error, **stack}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    fw = Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if any(address in fw.code for address in range(0x2600, 0x2606)):
        raise ValueError("Simulator trampoline would overwrite linked code")
    provenance = [Path(__file__), ROOT / "tests/ak820_emitted/run.py", ROOT / "keyboards/ajazz/ak820/ak820_rgb.c",
                  ROOT / "quantum/color.c", ROOT / "quantum/led_tables.c"]
    result = {"cpu": "uCsim C52", "linked_image_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "simulator_sha256": hashlib.sha256(args.s51.read_bytes()).hexdigest(),
              "linked_metadata_sha256": {str(p.relative_to(fw.build)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [fw.build / "ajazz_ak820_vial.map", fw.build / "ajazz_ak820_vial.mem",
                            *sorted((fw.build / "dce").rglob("*.rst"))]},
              "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in provenance},
              "initial_sp": fw.initial_sp, "stack_capacity_bytes": fw.stack_capacity,
              "limits": "Offline CPU/ABI and simulated DMA memory only; no physical timing, smoothness, DMA transfer, USB or storage validation. Stack peaks cover exercised paths without IRQ overlap. Full-CIE/no-CIE variants are not compiled or tested by this runner.", "tests": []}
    try:
        first, values = helper(fw)
        result["tests"].append(first)
        if not first["pass"]:
            raise RuntimeError("Helper check failed; stopping before renderer tests")
        result["tests"].append(frames(fw, values))
    except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        result["tests"].append({"name": "execution", "pass": False, "error": str(error)})
    result["pass"] = all(t["pass"] for t in result["tests"])
    (fw.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
