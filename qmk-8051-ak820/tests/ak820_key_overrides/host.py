#!/usr/bin/env python3
"""Run the existing production Key Overrides host fixture; no device access."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[3] / 'tests/test_compact_key_overrides.py'), run_name='__main__')

# Shared production storage regression; no device access.
import subprocess
import sys
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parents[2] / "tests/ak820_extensions/storage.py")])
