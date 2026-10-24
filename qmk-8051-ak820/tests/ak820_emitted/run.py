#!/usr/bin/env python3
"""Run offline regressions against an already linked AK820 SDCC image.

The generic uCsim C52 models CPU instructions, not VS11K28A peripherals. This
runner modifies only simulated memory, supplies matrix/NVM/USB status fixtures,
and never opens a physical device. It does not build or change firmware inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def memory(space: str, address: int, data) -> str:
    return f"set memory {space} {address:#x} " + " ".join(f"{value:#x}" for value in data)


class Firmware:
    def __init__(self, build: Path, simulator: Path, output: Path, *, auto_shift: bool = False):
        self.build, self.simulator, self.output = build, simulator, output
        self.image = build / "ajazz_ak820_vial.ihx"
        self.symbols = {
            name: int(address, 16)
            for address, name in re.findall(
                r"^(?:[CD]:)?\s+([0-9A-F]{8})\s+(_\S+)",
                (build / "ajazz_ak820_vial.map").read_text(), re.M
            )
        }
        # Linker maps omit static symbols. Relocated listings retain their
        # current names and addresses; no generated temporary suffix is pinned.
        self.symbol_spaces, self.symbol_sizes = {}, {}
        for listing in sorted((build / "dce").rglob("*.rst")):
            area, pending = "", None
            for line in listing.read_text().splitlines():
                section = re.search(r"\.area\s+(\w+)", line)
                if section:
                    area, pending = section[1], None
                label = re.match(r"^\s*([0-9A-F]{6})\s+\d+\s+(_[\w$]+):", line)
                if label:
                    address, pending = int(label[1], 16), label[2]
                    self.symbols.setdefault(pending, address)
                    self.symbol_spaces[pending] = "bits" if area == "BSEG" else "xram"
                allocation = re.search(r"\s\.ds\s+(\d+)\s*$", line)
                if allocation and pending:
                    self.symbol_sizes[pending] = int(allocation[1])
                    pending = None
        self.code = {}
        for line in self.image.read_text().splitlines():
            record = bytes.fromhex(line[1:])
            if sum(record) & 255:
                raise ValueError("Invalid IHX checksum")
            if record[3] == 0:
                address = int.from_bytes(record[1:3], "big")
                self.code.update((address + index, value) for index, value in enumerate(record[4:-1]))
            elif record[3] not in (1,):
                raise ValueError("Expected a 16-bit AK820 IHX")
        ram_report = (build / "ajazz_ak820_vial.mem").read_text()
        stack = re.search(r"sp set to 0x([0-9a-fA-F]+)\) with (\d+) bytes available", ram_report)
        if not stack:
            raise ValueError("Missing linked stack layout")
        self.initial_sp, self.stack_capacity = int(stack[1], 16), int(stack[2])
        self.has_auto_shift = "_ak820_autoshift_process" in self.symbols
        if auto_shift and not self.has_auto_shift:
            raise ValueError("Auto Shift fixture requires an Auto Shift image")
        self.auto_shift = auto_shift
        self.output.mkdir(parents=True, exist_ok=True)

    def address(self, name: str) -> int:
        if name not in self.symbols:
            raise ValueError(f"Required retained symbol is absent: {name}")
        return self.symbols[name]

    def write(self, name: str, data) -> list[str]:
        return [memory(self.symbol_space(name), self.address(name), data)]

    def symbol_space(self, name: str) -> str:
        return self.symbol_spaces.get(name, "xram")

    def write_scalar(self, name: str, value: int) -> list[str]:
        """Write one complete scalar using its actual linked allocation width."""
        width = self.symbol_sizes[name]
        if width not in (1, 2, 4):
            raise ValueError(f"Not a supported scalar allocation: {name}: {width}")
        return self.write(name, value.to_bytes(width, "little"))

    def call(self, name: str, argument: int | None = None) -> list[str]:
        address = self.address(name)
        commands = []
        if argument is not None:
            commands += [memory("sfr", 0x82, [argument & 255, (argument >> 8) & 255]),
                         memory("sfr", 0xF0, [(argument >> 16) & 255])]
        # Only simulator ROM is changed. The real image has no code here; the
        # offline trampoline calls the target and stops before OEM code runs.
        commands += [memory("rom", 0x2600, [0x12, address >> 8, address & 255, 0x02, 0x27, 0]),
                     "run 0x2600 0x2700"]
        return commands

    def clock(self, value: int) -> list[str]:
        return self.write("_timer_count", value.to_bytes(4, "little"))

    def initialize(self) -> list[str]:
        commands = [f"run {self.address('__sdcc_gsinit_startup'):#x} {self.address('_main'):#x}",
                    "fill rom 0xc700 0xef7f 0",
                    f"fill xram {self.address('_ak820_led_dma'):#x} {self.address('_ak820_led_dma') + 511:#x} 0"]
        # CRT runs, but main/board init does not: fake peripherals never claim
        # to implement the actual oscillator, flash, IRQ or USB controller.
        keymap = bytes(self.code[self.address("_keymaps") + index] for index in range(512))
        nvm = bytearray(512)
        for index in range(0, 512, 2):
            nvm[index:index + 2] = keymap[index:index + 2][::-1]
        commands += [memory("rom", 0xC740 + index, nvm[index:index + 32]) for index in range(0, 512, 32)]
        # Board init normally loads runtime timing settings. Zeroed simulated
        # ROM selects production defaults without requesting a flash write.
        if "_ak820_settings_init" in self.symbols:
            commands += self.call("_ak820_settings_init")
        commands += self.call("_host_set_driver", self.address("_ch555_usb_stack_driver"))
        commands += self.write("_USB_EnumStatus", [1]) + self.write("_D0UsbConfig", [1])
        commands += ["fill xram 0x2201 0x2203 0x12"]
        if self.has_auto_shift:
            # Ordinary regressions exercise immediate typing with Auto Shift
            # explicitly switched off. Its dedicated suite keeps the actual
            # power-on default and covers deferred events and interactions.
            # Use the production AS_OFF key path, not a private-state write.
            if not self.auto_shift:
                address = 0xC740 + 2 * (15 * 8 + 7)
                commands += [memory("rom", address, [0x7c, 0x14])]
                for pressed in (1, 0):
                    commands += self.write("_action_exec_PARM_1", [7, 15, 0, 0, 1, pressed])
                    commands += self.call("_action_exec")
                commands += [memory("rom", address, nvm[254:256])]
            commands += self.dump_symbol("fixture_auto_shift_enabled", "_as_enabled", 1)
        return commands

    @staticmethod
    def dump(label: str, space: str, address: int, count: int) -> list[str]:
        return [f"echo @@{label}", f"dump {space} {address:#x} {address + count - 1:#x} 16"]

    def dump_symbol(self, label: str, name: str, count: int) -> list[str]:
        return self.dump(label, self.symbol_space(name), self.address(name), count)

    @staticmethod
    def extract(log: str, label: str, address: int, count: int) -> list[int]:
        if "@@" + label not in log:
            raise ValueError(f"Simulator observation missing: {label}")
        tail = log.rsplit("@@" + label, 1)[1]
        values = {}
        for row, data in re.findall(r"^0x([0-9a-f]+)\s+((?:[0-9a-f]{1,2}\s+)+)", tail, re.M):
            for offset, value in enumerate(data.split()):
                values[int(row, 16) + offset] = int(value, 16)
            if all(address + index in values for index in range(count)):
                return [values[address + index] for index in range(count)]
        raise ValueError(f"Incomplete simulator observation: {label}")

    def execute(self, name: str, commands: list[str]) -> tuple[str, dict]:
        script = "\n".join(commands + ["state", "quit"]) + "\n"
        command_file = self.output / (name + ".sim")
        command_file.write_text(script)
        # A file console keeps input echo and dump output ordered. Streaming a
        # long script through stdin can interleave echo into memory-dump rows.
        run = subprocess.run([str(self.simulator), "-t", "C52", "-b", "-c", "-", str(self.image)],
                             input="exec " + json.dumps(str(command_file)) + "\n", capture_output=True, text=True, timeout=45)
        (self.output / (name + ".log")).write_text(run.stdout + "\n" + run.stderr)
        if run.returncode:
            raise RuntimeError(f"Simulator failed for {name}: {run.returncode}")
        if "Stack overflow" in run.stdout:
            raise RuntimeError(f"Simulator stack overflow in {name}")
        mode = "not-compiled"
        if self.has_auto_shift:
            mode = "not-observed"
            if "@@fixture_auto_shift_enabled" in run.stdout:
                enabled = self.extract(run.stdout, "fixture_auto_shift_enabled", self.address("_as_enabled"), 1)
                if enabled != [int(self.auto_shift)]:
                    raise RuntimeError(f"Auto Shift fixture mode was not established in {name}")
                mode = "enabled-default" if self.auto_shift else "disabled-with-AS_OFF"
        peaks = re.findall(r"Most value of stack pointer=\s+0x([0-9a-f]+)", run.stdout)
        if not peaks:
            raise RuntimeError(f"Simulator did not complete {name}")
        peak = int(peaks[-1], 16)
        return run.stdout, {"peak_sp": peak, "tested_stack_bytes": peak - self.initial_sp,
                            "fixture_auto_shift": mode}

    def transition(self, rows: list[int], clock: int) -> list[str]:
        return (self.write("_ak820_scan_rows", rows) + self.write("_ak820_scan_ready", [1]) +
                self.clock(clock) + self.call("_protocol_task") + ["fill xram 0x2201 0x2203 0x12"] +
                self.clock(clock + 6) + self.call("_protocol_task"))

    def frame(self, clock: int) -> list[str]:
        commands = self.clock(clock)
        for _ in range(11):  # 82 LEDs, at most eight per task call
            commands += self.call("_rgb_matrix_task")
        return commands

    def led_address(self, index: int) -> int:
        slot = self.code[self.address("_ak820_rgb_slots") + index]
        return self.address("_ak820_led_dma") + slot * 4


def matrix_fn(fw: Firmware) -> dict:
    commands, rows = fw.initialize(), [0] * 16
    observations = [("fn_down", "_layer_state", 1, [2]),
                    ("fn_f1_down", "_last_consumer_usage", 2, [0x94, 0x01]),
                    ("fn_up", "_layer_state", 1, [0]),
                    ("f1_release", "_last_consumer_usage", 2, [0, 0]),
                    ("a_down", "_actual_keyboard_report", 8, [0, 0, 4, 0, 0, 0, 0, 0]),
                    ("a_up", "_actual_keyboard_report", 8, [0] * 8)]
    for (row, value, clock), (label, name, count, _) in zip(
            [(10, 32, 100), (1, 1, 120), (10, 0, 140), (1, 0, 160), (1, 8, 180), (1, 0, 200)],
            observations):
        rows[row] = value
        commands += fw.transition(rows, clock) + fw.dump_symbol(label, name, count)
    log, stack = fw.execute("matrix-fn", commands)
    actual = {label: fw.extract(log, label, fw.address(name), count) for label, name, count, _ in observations}
    return {"name": "matrix_debounce_fn_release_and_key", "pass": all(actual[label] == expected for label, _, _, expected in observations),
            "observations": actual, **stack}


def macro_action(fw: Firmware) -> dict:
    macro = bytes([1, 6, 0x21, 0x52, ord("a"), 1, 7, 0x21, 0x52, 1, 5, 0x77, 0xFF, ord("b")]) + bytes(16)
    commands = fw.initialize() + [memory("rom", 0xC740, [0x77, 0]),
                                  memory("rom", 0xCEF0, [0, len(macro), 0]), memory("rom", 0xCF00, macro)]
    commands += fw.call("_ak820_macro_init") + fw.transition([1] + [0] * 15, 100)
    commands += fw.dump_symbol("layer", "_layer_state", 1) + fw.dump_symbol("report", "_actual_keyboard_report", 8)
    log, stack = fw.execute("macro-action", commands)
    layer = fw.extract(log, "layer", fw.address("_layer_state"), 1)
    report = fw.extract(log, "report", fw.address("_actual_keyboard_report"), 8)
    return {"name": "macro_extended_layer_and_recursion_guard", "pass": layer == [0] and report == [0] * 8,
            "macro_bytes": macro.hex(), "final_layer": layer, "final_report": report, **stack}


def rgb(fw: Firmware) -> dict:
    # Stable AK820 compact RGB config: enabled, solid=1, Direct=5. At V=80
    # the enabled CIE1931 curve produces 18. Pure red tests a nonzero result;
    # Direct adds grayscale, pure blue and a final-index green LED.
    commands = fw.initialize() + fw.write("_rgb_matrix_config", [5, 0, 255, 80, 96, 255, 0, 0])
    commands += fw.frame(100) + fw.dump("solid", "xram", fw.led_address(0), 4)
    direct = bytearray(82 * 3)
    direct[:6] = bytes([0, 0, 80, 170, 255, 80])
    direct[-3:] = bytes([85, 255, 80])
    commands += fw.write("_g_direct_mode_colors", direct) + fw.call("_rgb_matrix_mode_noeeprom", 5) + fw.frame(200)
    for index in (0, 1, 2, 81):
        commands += fw.dump(f"direct_{index}", "xram", fw.led_address(index), 4)
    # Seed a known live color through the public API, so the sleep
    # regression is independent of whether HSV rendering itself is working.
    commands += fw.write("_rgb_matrix_set_color_PARM_2", [60]) + fw.write("_rgb_matrix_set_color_PARM_3", [30])
    commands += fw.write("_rgb_matrix_set_color_PARM_4", [10]) + fw.call("_rgb_matrix_set_color", 0)
    commands += fw.dump("before_sleep", "xram", fw.led_address(0), 4)
    commands += fw.dump("bounds_before", "xram", fw.address("_ak820_led_dma"), 512)
    for invalid in (0xffff, 0x8000, 82, 255, 256, 32767):
        commands += fw.call("_rgb_matrix_set_color", invalid)
    for invalid in (82, 255):
        commands += fw.call("_ak820_rgb_set_color", invalid)
    commands += fw.dump("bounds_after", "xram", fw.address("_ak820_led_dma"), 512)
    commands += fw.write("_USB_SleepStatus", [2]) + fw.call("_protocol_pre_task")
    commands += fw.dump("sleep_immediate", "xram", fw.address("_ak820_led_dma"), 512)
    commands += fw.frame(300) + fw.dump("sleep_rendered", "xram", fw.address("_ak820_led_dma"), 512)
    commands += fw.dump_symbol("sleep_usb_state", "_usb_device_state", 1)
    commands += fw.write("_USB_SleepStatus", [0]) + fw.call("_protocol_pre_task") + fw.frame(400)
    for index in (0, 1, 81):
        commands += fw.dump(f"resume_{index}", "xram", fw.led_address(index), 4)
    commands += fw.dump_symbol("resume_usb_state", "_usb_device_state", 1)
    log, stack = fw.execute("rgb-solid-direct-suspend-resume", commands)
    actual = {"solid": fw.extract(log, "solid", fw.led_address(0), 4),
              "before_sleep": fw.extract(log, "before_sleep", fw.led_address(0), 4)}
    expected = {"solid": [255, 18, 0, 0], "before_sleep": [255, 60, 30, 10]}
    actual['invalid_indices_preserve_dma'] = (fw.extract(log, 'bounds_before', fw.address('_ak820_led_dma'), 512) ==
                                             fw.extract(log, 'bounds_after', fw.address('_ak820_led_dma'), 512))
    expected['invalid_indices_preserve_dma'] = True
    for prefix, indices in (("direct", (0, 1, 2, 81)), ("resume", (0, 1, 81))):
        colors = {0: [255, 18, 18, 18], 1: [255, 0, 0, 18], 2: [0, 0, 0, 0], 81: [255, 0, 18, 0]}
        for index in indices:
            label = f"{prefix}_{index}"
            actual[label] = fw.extract(log, label, fw.led_address(index), 4)
            expected[label] = colors[index]
    for label in ("sleep_immediate", "sleep_rendered"):
        actual[label + "_nonzero_bytes"] = sum(value != 0 for value in fw.extract(log, label, fw.address("_ak820_led_dma"), 512))
        expected[label + "_nonzero_bytes"] = 0
    for label, value in (("sleep_usb_state", 3), ("resume_usb_state", 2)):
        actual[label] = fw.extract(log, label, fw.address("_usb_device_state"), 1)
        expected[label] = [value]
    return {"name": "rgb_solid_direct_suspend_resume", "pass": actual == expected, "observations": actual,
            "expected": expected, **stack}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path, help="Existing build with IHX/map/mem and relocated dce/*.rst")
    parser.add_argument("--s51", required=True, type=Path, help="Path to the supplied uCsim s51 executable")
    parser.add_argument("--output-dir", type=Path, help="Simulator commands, logs and results; defaults to BUILD/emitted-tests")
    args = parser.parse_args()
    fw = Firmware(args.build_dir.resolve(), args.s51.resolve(), (args.output_dir or args.build_dir / "emitted-tests").resolve())
    result = {"linked_image_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(), "cpu": "uCsim C52",
              "initial_sp": fw.initial_sp, "stack_capacity_bytes": fw.stack_capacity,
              "limits": "CPU/ABI checks with supplied peripheral state; no physical USB/IAP/DMA/timing validation; stack peaks cover only exercised paths without IRQ overlap",
              "tests": []}
    for test in (matrix_fn, macro_action, rgb):
        try:
            result["tests"].append(test(fw))
        except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            result["tests"].append({"name": test.__name__, "pass": False, "error": str(error)})
    result["pass"] = all(test["pass"] for test in result["tests"])
    (fw.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
