#!/usr/bin/env python3
"""Host sanitizer test of production USB + verbatim backend/host retry paths."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_recovery", ROOT / "tests/ak820_recovery/run.py")
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.source_root.resolve(), args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    backend = root / "tmk_core/protocol/ch555/ch555_ak820.c"
    (output / "backend.inc").write_text(re.sub(r"^\s*#\s*include[^\n]*", "", backend.read_text(), flags=re.M))
    host = root / "tmk_core/protocol/host.c"
    (output / "host-extra.inc").write_text("\n".join(recovery.function(host.read_text(), signature) for signature in (
        "void host_system_send", "void host_consumer_send", "uint16_t host_last_system_usage", "uint16_t host_last_consumer_usage")))
    info = json.loads((root / "keyboards/ajazz/ak820/info.json").read_text())
    includes = [output, ROOT / "tests/ak820_usb", *[root / item for item in (
        ".", "tmk_core", "tmk_core/protocol", "tmk_core/protocol/ch555", "tmk_core/protocol/ch555/lufa_utils",
        "quantum", "platforms", "platforms/mcs51", "lib/ch555")]]
    defines = ["AK820_BOARD", "AK820_USB_HOST_TEST", "QMK_MCU_CH555", "PROTOCOL_CH555", "RAW_ENABLE",
               "SHARED_EP_ENABLE", "EXTRAKEY_ENABLE", "NKRO_ENABLE", "MATRIX_ROWS=16", "MATRIX_COLS=8",
               "EEPROM_CUSTOM", "EEPROM_SIZE=0x2800", "FIXED_CONTROL_ENDPOINT_SIZE=64", "FIXED_NUM_CONFIGURATIONS=1",
               "USB_POLLING_INTERVAL_MS=1", "USB_MAX_POWER_CONSUMPTION=500", "ARCH=ARCH_MCS51",
               "VENDOR_ID=" + info["usb"]["vid"], "PRODUCT_ID=" + info["usb"]["pid"], "DEVICE_VER=0x0100",
               "MANUFACTURER=" + json.dumps(info["manufacturer"]), "PRODUCT=" + json.dumps(info["keyboard_name"]),
               'SERIAL_NUMBER="vial:f64c2b3c"']
    binary = output / "transport-host"
    command = ["cc", "-std=gnu11", "-Wall", "-Wextra", "-Werror=implicit-function-declaration",
               "-Wno-unknown-pragmas", "-Wno-unused-parameter", "-Wno-old-style-declaration",
               "-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-g", "-O1",
               *["-I" + str(item) for item in includes], *["-D" + item for item in defines],
               str(Path(__file__).with_name("harness.c")), str(root / "tmk_core/protocol/usb_descriptor.c"), "-o", str(binary)]
    subprocess.run(command, check=True)
    environment = os.environ.copy()
    environment["ASAN_OPTIONS"] = "detect_leaks=0"
    run = subprocess.run([str(binary)], env=environment, capture_output=True, text=True)
    (output / "host.log").write_text(run.stdout + run.stderr)
    paths = [backend, host, root / "tmk_core/protocol/ch555/usb_ak820.c", root / "tmk_core/protocol/ch555/usb_ak820.h",
             root / "tmk_core/protocol/usb_descriptor.c", Path(__file__), Path(__file__).with_name("harness.c"),
             ROOT / "tests/ak820_usb/ak820_usb_test_shim.h", ROOT / "tests/ak820_recovery/run.py"]
    report = {"result": "PASS" if run.returncode == 0 else "FAIL", "hardware_validated": False,
              "level": "host ASan/UBSan; production USB + verbatim backend/host bodies; MMIO/timer/hooks fixtures",
              "command": command, "source_sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
              "stdout": run.stdout, "stderr": run.stderr}
    (output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(run.stdout + run.stderr, end="")
    return run.returncode


if __name__ == "__main__":
    raise SystemExit(main())
