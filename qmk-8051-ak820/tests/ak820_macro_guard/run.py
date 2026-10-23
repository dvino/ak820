#!/usr/bin/env python3
"""Compile and exercise the current AK820 macro interpreter with host stubs.

Run from the source root: python3 tests/ak820_macro_guard/run.py
No USB access. The production function bodies are extracted at run time;
the harness does not contain a second implementation of the interpreter.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def definition(source: str, name: str) -> str:
    match = re.search(r"^(?:static )?(?:void|uint16_t) " + name + r"\([^\n]*\) \{", source, re.M)
    if not match:
        raise ValueError("Missing production function: " + name)
    end = source.index("\n}", match.end()) + 2
    return source[match.start():end]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cc", default=os.environ.get("CC", "cc"))
    parser.add_argument("--no-sanitize", action="store_true")
    args = parser.parse_args()
    source = (ROOT / "quantum/dynamic_keymap.c").read_text()
    vial = (ROOT / "quantum/vial.h").read_text()
    constants = []
    for name in ("VIAL_MACRO_EXT_TAP", "VIAL_MACRO_EXT_DOWN", "VIAL_MACRO_EXT_UP"):
        constants.append(re.search(r"^#define " + name + r" \d+$", vial, re.M).group(0))
    sender = (ROOT / "quantum/send_string/send_string.c").read_text()
    actual = "\n".join(constants + [definition(sender, "send_string"), definition(sender, "send_string_with_delay"),
                                  definition(source, "decode_keycode"), definition(source, "dynamic_keymap_macro_send")])
    harness = (HERE / "harness.c").read_text().replace("/* AK820_ACTUAL_SOURCE */", actual)
    with tempfile.TemporaryDirectory(prefix="ak820-macro-guard-") as work:
        work = Path(work)
        (work / "host.c").write_text(harness)
        flags = ["-O1", "-g", "-Wall", "-Wextra", "-Werror"]
        if not args.no_sanitize:
            flags += ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
        subprocess.run([args.cc, *flags, "-I" + str(ROOT / "quantum/send_string"), str(work / "host.c"), "-o", str(work / "host")], check=True)
        env = os.environ.copy()
        # The harness has no allocations. Leak scanning needs /proc access
        # unavailable in some sandboxes; address/undefined checks stay enabled.
        env["ASAN_OPTIONS"] = "detect_leaks=0"
        subprocess.run([str(work / "host")], check=True, env=env)


if __name__ == "__main__":
    main()
