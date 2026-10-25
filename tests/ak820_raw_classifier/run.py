#!/usr/bin/env python3
"""Exhaustively compare the current USB classifier with its saved switch oracle."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QMK = ROOT / "qmk-8051-ak820"
USB = QMK / "tmk_core/protocol/ch555/usb_ak820.c"
HEADERS = [QMK / "quantum/via.h", QMK / "quantum/vial.h", QMK / "quantum/vialrgb.h"]
ORACLE = HERE / "oracle_switch.inc"
SIZE = 32
EXPECTED_ASSERTS = 6


def fail(message: str) -> None:
    raise RuntimeError(message)


def function(text: str) -> str:
    match = re.search(r"static\s+bool\s+raw_request_is_nonpersistent\s*\(\s*void\s*\)\s*\{", text)
    if not match:
        fail("current classifier function signature not found")
    start = match.start()
    brace = text.find("{", match.start())
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[start : pos + 1]
    fail("unterminated classifier function")


def enum_blocks(path: Path, required: set[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    result = []
    pos = 0
    while True:
        match = re.search(r"\benum(?:\s+[A-Za-z_]\w*)?\s*\{", text[pos:])
        if not match:
            break
        start = pos + match.start()
        brace = text.find("{", start)
        depth = 0
        end = None
        for i in range(brace, len(text)):
            if text[i] == "{": depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    semicolon = text.find(";", i)
                    if semicolon < 0: fail(f"enum terminator missing in {path}")
                    end = semicolon + 1
                    break
        if end is None: fail(f"unterminated enum in {path}")
        block = text[start:end]
        present = {name for name in required if re.search(rf"\b{re.escape(name)}\b", block)}
        if present:
            result.append(block)
            required -= present
        pos = end
    if required:
        fail(f"enum symbols missing from {path}: {', '.join(sorted(required))}")
    return result


ENUM_SYMBOLS = {
    HEADERS[0]: {"id_get_protocol_version", "id_get_keyboard_value", "id_dynamic_keymap_get_keycode",
                 "id_dynamic_keymap_macro_get_count", "id_dynamic_keymap_macro_get_buffer_size",
                 "id_dynamic_keymap_macro_get_buffer", "id_dynamic_keymap_get_layer_count",
                 "id_dynamic_keymap_get_buffer", "id_bootloader_jump", "id_vial_prefix", "id_uptime",
                 "id_layout_options", "id_switch_matrix_state", "id_firmware_version"},
    HEADERS[1]: {"vial_get_keyboard_id", "vial_get_size", "vial_get_def", "vial_get_encoder",
                 "vial_set_encoder", "vial_get_unlock_status", "vial_unlock_start", "vial_unlock_poll",
                 "vial_lock", "vial_qmk_settings_query", "vial_qmk_settings_get", "vial_dynamic_entry_op",
                 "dynamic_vial_get_number_of_entries", "dynamic_vial_tap_dance_get", "dynamic_vial_tap_dance_set",
                 "dynamic_vial_combo_get", "dynamic_vial_combo_set", "dynamic_vial_key_override_get",
                 "dynamic_vial_key_override_set"},
    HEADERS[2]: {"vialrgb_get_info", "vialrgb_get_mode", "vialrgb_get_supported",
                 "vialrgb_get_number_leds", "vialrgb_get_led_info"},
}


def assertions(text: str) -> str:
    fn = re.search(r"static\s+bool\s+raw_request_is_nonpersistent", text)
    if not fn: fail("classifier location lost while extracting adjacent assertions")
    before = text[:fn.start()]
    lines = [line.strip() for line in before.splitlines() if line.strip().startswith("_Static_assert(")]
    chosen = lines[-EXPECTED_ASSERTS:]
    if len(chosen) != EXPECTED_ASSERTS:
        fail(f"expected {EXPECTED_ASSERTS} adjacent classifier assertions, found {len(chosen)}")
    return "\n".join(chosen)


def c_source(candidate: str, reference: str, enums: str, asserts: str) -> str:
    def rename(code: str, name: str, buffer: str) -> str:
        code = re.sub(r"\braw_request_is_nonpersistent\b", name, code)
        return re.sub(r"\braw_buffer\b", buffer, code)

    candidate = rename(candidate, "candidate", "candidate_buffer")
    reference = rename(reference, "reference", "reference_buffer")
    return f'''#include <stdbool.h>\n#include <stdint.h>\n#include <stdio.h>\n#include <string.h>\n#define RAW_EPSIZE {SIZE}\nstatic uint8_t candidate_buffer[RAW_EPSIZE], reference_buffer[RAW_EPSIZE];\n{enums}\n{asserts}\n{reference}\n{candidate}\nstatic int run_case(unsigned int n, const char *label) {{\n  uint8_t before[RAW_EPSIZE]; unsigned int i;\n  for (i=0;i<RAW_EPSIZE;i++) candidate_buffer[i]=reference_buffer[i]=(uint8_t)(i*37u+11u);\n  candidate_buffer[0]=reference_buffer[0]=(uint8_t)(n>>16);\n  candidate_buffer[1]=reference_buffer[1]=(uint8_t)(n>>8);\n  candidate_buffer[2]=reference_buffer[2]=(uint8_t)n;\n  memcpy(before,candidate_buffer,RAW_EPSIZE);\n  bool expected=reference(), got=candidate();\n  if (expected != got) {{ printf("{{\\\"kind\\\":\\\"mismatch\\\",\\\"variant\\\":\\\"%s\\\",\\\"bytes\\\":[%u,%u,%u],\\\"expected\\\":%s,\\\"actual\\\":%s}}\\n",label,n>>16,(n>>8)&255,n&255,expected?"true":"false",got?"true":"false"); return 1; }}\n  if (memcmp(before,candidate_buffer,RAW_EPSIZE)) {{ printf("{{\\\"kind\\\":\\\"mutation\\\",\\\"variant\\\":\\\"%s\\\",\\\"bytes\\\":[%u,%u,%u],\\\"error\\\":\\\"candidate modified packet\\\"}}\\n",label,n>>16,(n>>8)&255,n&255); return 2; }}\n  return 0;\n}}\nint main(int argc,char **argv) {{ unsigned int n; int rc; const char *label=argc>1?argv[1]:"current"; for(n=0;n<16777216u;n++) {{ rc=run_case(n,label); if(rc) return rc; }} printf("{{\\\"kind\\\":\\\"pass\\\",\\\"variant\\\":\\\"%s\\\",\\\"prefixes\\\":16777216,\\\"packet_bytes\\\":32,\\\"immutable\\\":true}}\\n",label); return 0; }}\n'''


def run_variant(cc: tuple[str, ...], source: str, label: str, directory: Path) -> tuple[int, str]:
    cfile = directory / f"{label}.c"
    binary = directory / label
    cfile.write_text(source, encoding="utf-8")
    if cc[0] == "docker":
        compiler = ["docker", "run", "--rm", "--network", "none", "-v", f"{directory}:/work", "-w", "/work", cc[1]]
        c_arg, bin_arg = f"/work/{cfile.name}", f"/work/{binary.name}"
    else:
        compiler = [cc[0]]
        c_arg, bin_arg = str(cfile), str(binary)
    build_args = ["-O2", "-std=c11", "-Wall", "-Wextra", c_arg, "-o", bin_arg]
    build = subprocess.run([*compiler, "gcc", *build_args] if cc[0] == "docker" else [*compiler, *build_args], text=True, capture_output=True)
    if build.returncode: fail(f"{label} compile failed:\n{build.stderr}")
    result = subprocess.run([*compiler, bin_arg, label], text=True, capture_output=True) if cc[0] == "docker" else subprocess.run([bin_arg, label], text=True, capture_output=True)
    if result.returncode == 0:
        return 0, result.stdout.strip()
    if result.returncode == 1:
        return 1, result.stdout.strip()
    fail(f"{label} failed ({result.returncode}): {result.stdout}{result.stderr}")


def main() -> int:
    local_cc = shutil.which("gcc") or shutil.which("cc")
    if local_cc:
        cc = (local_cc,)
    elif shutil.which("docker"):
        image = "ak820-nkro-study-env:local"
        check = subprocess.run(["docker", "run", "--rm", "--network", "none", image, "gcc", "--version"], capture_output=True, text=True)
        if check.returncode: fail(f"host compiler unavailable and Docker image {image} has no gcc")
        cc = ("docker", image)
    else:
        fail("host C compiler gcc or cc, or Docker with the ak820-nkro-study-env:local image, is required")
    usb_text = USB.read_text(encoding="utf-8")
    candidate = function(usb_text)
    reference = function(ORACLE.read_text(encoding="utf-8"))
    all_enums = []
    for header in HEADERS: all_enums.extend(enum_blocks(header, set(ENUM_SYMBOLS[header])))
    enum_text = "\n".join(all_enums)
    assert_text = assertions(usb_text)
    base = c_source(candidate, reference, enum_text, assert_text)
    mutants = {
        "mutant_admit_encoder_setter": ("raw_buffer[1] != vial_set_encoder", "1"),
        "mutant_admit_dynamic_setters": ("raw_buffer[2] != dynamic_vial_tap_dance_set && raw_buffer[2] != dynamic_vial_combo_set", "1"),
    }
    hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [USB, *HEADERS, ORACLE]}
    print(json.dumps({"kind": "sources", "sha256": hashes, "compiler": list(cc)}, sort_keys=True))
    with tempfile.TemporaryDirectory(prefix="ak820-raw-classifier-") as temp:
        directory = Path(temp)
        os.chmod(directory, 0o777)  # The isolated, temporary bind mount must be writable by Docker's user.
        status, output = run_variant(cc, base, "current", directory)
        print(output)
        if status: fail("current classifier differs from original switch oracle")
        for label, (needle, replacement) in mutants.items():
            if needle not in candidate: fail(f"mutation anchor absent from current function: {needle}")
            mutant = candidate.replace(needle, replacement, 1)
            status, output = run_variant(cc, c_source(mutant, reference, enum_text, assert_text), label, directory)
            print(output)
            if status != 1: fail(f"{label} was not detected")
    print(json.dumps({"kind": "result", "status": "PASS", "mutants_detected": len(mutants)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
