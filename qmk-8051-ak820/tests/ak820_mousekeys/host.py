#!/usr/bin/env python3
"""Compile and execute the production Mouse Keys C with a host USB/time seam."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
for key, default in (("cursor-step", 8), ("cursor-period", 20), ("wheel-step", 1), ("wheel-period", 80)):
    parser.add_argument("--mouse-" + key, type=int, default=default)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="ak820-mousekeys-") as directory:
    binary = Path(directory) / "host"
    subprocess.run([os.environ.get("CC", "cc"), "-std=c99", "-Wall", "-Wextra", "-Werror",
                    "-I", str(HERE), str(HERE / "host.c"), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
    defines = ["-DAK820_MOUSE_" + key.upper() + "=" + str(getattr(args, 'mouse_' + key))
               for key in ('cursor_step', 'cursor_period', 'wheel_step', 'wheel_period')]
    subprocess.run([os.environ.get("CC", "cc"), "-std=c99", "-Wall", "-Wextra", "-Werror",
                    *defines, "-I", str(HERE), str(HERE / "override.c"), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
