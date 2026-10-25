#!/usr/bin/env python3
"""Run NVM diagnostic regression with memory-only Flash. No USB/device access."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix="ak820-diagnostic-") as temporary:
    binary = Path(temporary) / "nvm-diagnostic"
    subprocess.run([
        os.environ.get("CC", "cc"), "-std=c11", "-Wall", "-Wextra", "-Werror", "-g", "-O1",
        "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
        "-I" + str(ROOT / "keyboards/ajazz/ak820"),
        str(ROOT / "tests/ak820_diagnostic/nvm_harness.c"),
        str(ROOT / "keyboards/ajazz/ak820/ak820_nvm.c"), str(ROOT / "keyboards/ajazz/ak820/ak820_crc.c"), "-o", str(binary),
    ], check=True)
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = "detect_leaks=0"
    subprocess.run([str(binary)], check=True, env=env)
