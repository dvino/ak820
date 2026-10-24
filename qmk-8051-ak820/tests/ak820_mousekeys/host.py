#!/usr/bin/env python3
"""Compile and execute the production Mouse Keys C with a host USB/time seam."""
import os
from pathlib import Path
import subprocess
import tempfile
HERE = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="ak820-mousekeys-") as directory:
    binary = Path(directory) / "host"
    subprocess.run([os.environ.get("CC", "cc"), "-std=c99", "-Wall", "-Wextra", "-Werror",
                    "-I", str(HERE), str(HERE / "host.c"), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
