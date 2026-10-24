#!/usr/bin/env python3
"""Differential host regressions using production bodies and immutable RC4 fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def function(path, name):
    text = path.read_text()
    match = re.search(r"^(?:static )?[\w *]+\b" + name + r"\([^\n]*\) \{", text, re.M)
    if not match:
        raise ValueError(f"Cannot extract {name} from {path}")
    return text[match.start():text.index("\n}", match.end()) + 2]


def without_includes(path):
    return re.sub(r"^#\s*include[^\n]*\n", "", path.read_text(), flags=re.M)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT, help="Firmware source tree to test (default: this checkout)")
    parser.add_argument("--test", choices=("cache", "color", "macro", "buffers"), action="append", help="Run selected checks; default all")
    parser.add_argument("--output", type=Path, help="Optional JSON report with tested source/fixture hashes")
    args = parser.parse_args()
    root = args.source_root.resolve()
    selected = args.test or ["cache", "color", "macro", "buffers"]
    tests = []
    paths = set()
    if "cache" in selected:
        files = [root / "quantum/action_layer.c", root / "quantum/keymap_common.c", root / "tmk_core/protocol/report.c", root / "quantum/quantum.c", HERE / "fixtures/keycode_decoder_rc4.c", root / "quantum/action_util.c"]
        paths.update(files)
        parts = [without_includes(files[0]), function(files[1], "action_for_keycode"), function(files[2], "KEYCODE2CONSUMER"), function(files[3], "get_event_keycode"), files[4].read_text()]
        # Compact tapping's layer owner calls this shared production bitset
        # transition. Include its real storage and implementation so this
        # cache fixture still compiles against the current layer API.
        parts += [function(files[5], "ak820_macro_change")]
        adapter = ("#define AK820_STATE_MEM\n"
                   "bool ak820_macro_change(uint8_t *bits, uint8_t index, bool pressed);\n"
                   "bool ak820_macro_primitive, ak820_macro_cancelled;\n")
        body = (HERE / "harness.c").read_text().replace("/* PRODUCTION */", adapter + "\n".join(parts))
        definitions = ["ENCODER_MAP_ENABLE", "VIAL_ENABLE", "DYNAMIC_KEYMAP_ENABLE", "EXTRAKEY_ENABLE"]
        tests += [("cache-profile", body, definitions), ("cache-with-optional-layer-array", body, definitions + ["KEY_OVERRIDE_ENABLE"])]
    if "color" in selected:
        files = [root / "quantum/color.c", root / "quantum/led_tables.c", HERE / "fixtures/color_rc4.c"]
        paths.update(files)
        body = (HERE / "color_harness.c").read_text().replace("/* ACTUAL */", without_includes(files[0])).replace("/* TABLE */", without_includes(files[1])).replace("/* REFERENCE */", files[2].read_text())
        # Exact historical differential is the full-precision control. The
        # compact production curve has separate bounded-error tests.
        tests += [("color", body, ["USE_CIE1931_CURVE", "AK820_FULL_CIE"])]
    if "macro" in selected:
        files = [root / "quantum/dynamic_keymap.c", root / "quantum/send_string/send_string.c", HERE / "fixtures/macro_playback_rc4.c"]
        paths.update(files)
        parts = [function(files[0], n) for n in ("decode_keycode", "dynamic_keymap_macro_send")]
        parts += [files[2].read_text(), *[function(files[1], n) for n in ("send_string", "send_string_with_delay")]]
        body = (HERE / "macro_harness.c").read_text().replace("/* SOURCES */", "\n".join(parts))
        tests += [("macro", body, ["EEPROM_CUSTOM"])]
    if "buffers" in selected:
        files = [root / "quantum/action_util.c", root / "quantum/debounce/sym_defer_g.c", HERE / "fixtures/report_rc4.c", HERE / "fixtures/debounce_rc4.c"]
        paths.update(files)
        parts = [function(files[0], "send_keyboard_report"), function(files[1], "debounce"), files[2].read_text(), files[3].read_text()]
        body = (HERE / "buffers_harness.c").read_text().replace("/* SOURCES */", "\n".join(parts))
        tests += [("buffers", body, [])]
    results = []
    with tempfile.TemporaryDirectory(prefix="ak820-optimization-") as temp:
        work = Path(temp)
        (work / "_timer.h").write_text("#define FAST_TIMER_T_SIZE 16\n")
        for name, body, definitions in tests:
            source, binary = work / f"{name}.c", work / name
            source.write_text(body)
            argv = [os.environ.get("CC", "cc"), "-std=gnu11", "-O2", "-g", "-Wall", "-Wextra", "-Werror",
                    "-Wno-unused-parameter", "-Wno-old-style-declaration", "-Wno-unknown-pragmas", "-Wno-int-to-pointer-cast",
                    "-fsanitize=address,undefined", "-fno-omit-frame-pointer", *["-D" + d for d in definitions],
                    "-include", str(root / "keyboards/ajazz/ak820/config.h"),
                    *["-I" + str(p) for p in (work, root / "quantum", root / "quantum/keymap_extras", root / "quantum/sequencer", root / "quantum/send_string",
                                              root / "platforms", root / "tmk_core/protocol", root)], str(source), "-o", str(binary)]
            subprocess.run(argv, check=True)
            env = os.environ.copy(); env["ASAN_OPTIONS"] = "detect_leaks=0"
            result = subprocess.run([str(binary)], env=env, text=True, capture_output=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            print(f"{name}: {result.stdout.strip()}", flush=True)
            results.append({"name": name, "pass": True, "summary": result.stdout.strip()})
    paths.add(root / "keyboards/ajazz/ak820/config.h")
    paths.add(root / "quantum/keymap_common.h")
    paths.update(p for p in HERE.rglob("*") if p.is_file() and p.suffix in (".py", ".c"))
    report = {"pass": True, "limits": "Host C semantics with sanitizers; actual SDCC/8051 ABI requires emitted.py and ak820_emitted tests.", "tests": results,
              "source_sha256": {str(p.relative_to(root) if p.is_relative_to(root) else p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
