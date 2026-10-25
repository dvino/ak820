#!/usr/bin/env python3
"""Build and run an offline differential test of AK820 dynamic_keymap_set_buffer."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

TEST_DIR = Path(__file__).resolve().parent
REPO = TEST_DIR.parents[1]
BASE_COMMIT = "eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e"
SOURCE_REL = Path("qmk-8051-ak820/quantum/dynamic_keymap.c")
CONFIG_REL = Path("qmk-8051-ak820/keyboards/ajazz/ak820/config.h")
KEYCODES_REL = Path("qmk-8051-ak820/quantum/keycodes.h")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"FAIL closed: {message}")


def one(pattern: str, data: str, label: str) -> re.Match[str]:
    matches = list(re.finditer(pattern, data, re.M))
    if len(matches) != 1:
        fail(f"expected one {label}, found {len(matches)}")
    return matches[0]


def extract_function(source: str) -> str:
    starts = list(re.finditer(r"^void dynamic_keymap_set_buffer\(uint16_t offset, uint16_t size, uint8_t \*data\) \{", source, re.M))
    ends = list(re.finditer(r"^uint16_t keycode_at_keymap_location\(", source, re.M))
    if len(starts) != 1 or len(ends) != 1 or starts[0].end() >= ends[0].start():
        fail(f"function extraction anchors invalid (start={len(starts)}, end={len(ends)})")
    function = source[starts[0].start():ends[0].start()]
    if function.count("ak820_eeprom_write_block_xdata(") != 1:
        fail("expected exactly one AK820 block-writer call in extracted function")
    if "DYNAMIC_KEYMAP_LAYER_COUNT" not in function or "QK_BOOT" not in function:
        fail("extracted function lacks expected bounds/firewall anchors")
    return function.rstrip() + "\n"


def mutants(function: str) -> dict[str, str]:
    prior = "uint8_t prior = eeprom_read_byte(target - 1);"
    if function.count(prior) != 1:
        fail("skipped-read mutant anchor missing or ambiguous")
    skipped = function.replace(prior, "uint8_t prior = 0xFF;", 1)
    first_start = function.find("        if (offset % 2 != 0) {")
    second_start = function.find("        if ((offset + size) % 2 != 0) {")
    loop_start = function.find("        while (remaining) {")
    if min(first_start, second_start, loop_start) < 0 or not first_start < second_start < loop_start:
        fail("boundary-read-order mutant anchors missing or ambiguous")
    reversed_reads = function[:first_start] + function[second_start:loop_start] + function[first_start:second_start] + function[loop_start:]
    boot = "        while (remaining) {"
    if function.count(boot) != 1:
        fail("boot-filter mutant anchor missing or ambiguous")
    bypass = function.replace(boot, "        while (0) {", 1)
    return {"skipped_read": skipped, "reversed_reads": reversed_reads, "boot_bypass": bypass}


def qk_boot_value(keycodes: str) -> int:
    boot = one(r"^\s*QK_BOOTLOADER\s*=\s*(0[xX][0-9a-fA-F]+)\s*,?\s*(?://.*)?$", keycodes, "QK_BOOTLOADER enum")
    one(r"^\s*QK_BOOT\s*=\s*QK_BOOTLOADER\s*,?\s*(?://.*)?$", keycodes, "QK_BOOT alias relation")
    return int(boot.group(1), 0)


def check_boot_alias_drift_rejected(keycodes: str) -> None:
    drifted, count = re.subn(r"^(\s*QK_BOOT\s*=\s*)QK_BOOTLOADER(\s*,?\s*(?://.*)?)$", r"\1QK_REBOOT\2", keycodes, count=1, flags=re.M)
    if count != 1:
        fail("cannot construct in-memory QK_BOOT alias drift check")
    try:
        qk_boot_value(drifted)
    except SystemExit as error:
        if "expected one QK_BOOT alias relation, found 0" in str(error):
            return
        fail(f"in-memory alias drift check failed for an unexpected reason: {error}")
    fail("in-memory QK_BOOT alias drift was not rejected")


def numeric_define(header: str, name: str) -> int:
    match = one(r"^\s*#\s*define\s+" + re.escape(name) + r"\s+(0[xX][0-9a-fA-F]+|[0-9]+)\s*(?:/\*.*?\*/)?\s*$", header, f"numeric define {name}")
    return int(match.group(1), 0)


def constants() -> tuple[dict[str, int], dict[str, bytes]]:
    paths = {"source": REPO / SOURCE_REL, "config": REPO / CONFIG_REL, "keycodes": REPO / KEYCODES_REL}
    blobs = {name: path.read_bytes() for name, path in paths.items()}
    config = blobs["config"].decode()
    keys = blobs["keycodes"].decode()
    vals = {name: numeric_define(config, name) for name in ("MATRIX_ROWS", "MATRIX_COLS", "DYNAMIC_KEYMAP_LAYER_COUNT", "DYNAMIC_KEYMAP_EEPROM_ADDR")}
    vals["QK_BOOT"] = qk_boot_value(keys)
    check_boot_alias_drift_rejected(keys)
    dynamic = blobs["source"].decode()
    if dynamic.count("typedef uint8_t dynamic_buffer_size_t;") != 1 or "#if defined(AK820_BOARD) && defined(__SDCC_mcs51)" not in dynamic:
        fail("dynamic_buffer_size_t uint8 target branch changed or is ambiguous")
    expected = {"MATRIX_ROWS": 16, "MATRIX_COLS": 8, "DYNAMIC_KEYMAP_LAYER_COUNT": 6, "DYNAMIC_KEYMAP_EEPROM_ADDR": 0x40, "QK_BOOT": 0x7C00}
    if vals != expected:
        fail(f"unexpected AK820 target constants: {vals}")
    return vals, blobs


def run(cmd: list[str], *, cwd: Path, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.STDOUT if capture else None, check=False)


def main() -> int:
    vals, blobs = constants()
    source = blobs["source"].decode()
    current = extract_function(source)
    oracle = (TEST_DIR / "oracle.inc").read_bytes()
    base = subprocess.run(["git", "show", f"{BASE_COMMIT}:{SOURCE_REL.as_posix()}"], cwd=REPO,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if base.returncode:
        fail("cannot read saved oracle source commit")
    if extract_function(base.stdout.decode()).encode() != oracle:
        fail("checked-in oracle does not match full original function from eb3c230")
    fixture = "\n".join(["#include <stdint.h>", "#include <stdbool.h>", "#include <stddef.h>",
                            *(f"#define {name} {value}" for name, value in vals.items()),
                            "#define AK820_BOARD 1", "#define VIAL_ENABLE 1",
                            "#define DYNAMIC_BUFFER_MEM", "typedef uint8_t dynamic_buffer_size_t;",
                            "uint8_t eeprom_read_byte(const uint8_t *p);",
                            "void eeprom_update_byte(uint8_t *p, uint8_t value);",
                            "void ak820_eeprom_write_block_xdata(const void *p, void *dest, size_t size);", ""])
    compiler = shutil.which(os.environ.get("CC", "gcc"))
    with tempfile.TemporaryDirectory(prefix="ak820-keymap-firewall-") as tmp:
        tmpdir = Path(tmp)
        (tmpdir / "fixture.h").write_text(fixture)
        (tmpdir / "current.inc").write_text(current)
        generated_mutants = mutants(current)
        for name, code in generated_mutants.items():
            (tmpdir / f"{name}.inc").write_text(code)
        if compiler:
            (tmpdir / "probe.c").write_text("int main(void) { return 0; }\n")
            probe = run([compiler, "-std=c11", "-fsanitize=address,undefined", str(tmpdir / "probe.c"), "-o", str(tmpdir / "probe")], cwd=tmpdir, capture=True)
            sanitizer = probe.returncode == 0
            flags = ["-std=c11", "-O1", "-g"] + (["-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if sanitizer else [])
            compiler_version = subprocess.run([compiler, "--version"], text=True, stdout=subprocess.PIPE, check=False).stdout.splitlines()[0]
            mutant_evidence = {}
            for name in ["current", *generated_mutants]:
                exe = tmpdir / f"run-{name}"
                test_source = TEST_DIR / "harness.c"
                include_option = [] if name == "current" else ['-DCURRENT_INCLUDE="' + name + '.inc"']
                compile_cmd = [compiler, *flags, *include_option, "-I", str(tmpdir), "-I", str(TEST_DIR), str(test_source), "-o", str(exe)]
                compiled = run(compile_cmd, cwd=tmpdir, capture=True)
                if compiled.returncode:
                    sys.stdout.write(compiled.stdout or "")
                    fail(f"host harness compilation failed for {name}")
                result = run([str(exe)], cwd=tmpdir, capture=True)
                if name == "current":
                    actual_result = result
                    if result.returncode:
                        sys.stdout.write(result.stdout or "")
                        fail("differential regression failed")
                elif result.returncode == 0:
                    fail(f"broken mutant escaped regression: {name}")
                else:
                    first_difference = next((line for line in (result.stdout or "").splitlines() if line.startswith("DIFF ")), None)
                    if first_difference is None:
                        sys.stdout.write(result.stdout or "")
                        fail(f"mutant {name} failed without a differential mismatch")
                    mutant_evidence[name] = {"status": "REJECTED", "first_difference": first_difference}
            result = actual_result
            compiler_evidence = {"compiler": compiler_version, "sanitizers": sanitizer, "container_image_sha256": None}
        else:
            docker = shutil.which("docker")
            if not docker:
                fail("neither GCC nor Docker is available")
            image = "ak820-nkro-study-env:local"
            inspect = run([docker, "image", "inspect", image, "--format", "{{.Id}}"], cwd=tmpdir, capture=True)
            if inspect.returncode or not (inspect.stdout or "").strip().startswith("sha256:"):
                fail("pinned offline fallback image ak820-nkro-study-env:local is unavailable")
            image_id = (inspect.stdout or "").strip()
            command_script = "set -eu; cd /out; printf 'int main(void){return 0;}\\n' | gcc -x c -std=c11 -fsanitize=address,undefined -o probe - >/dev/null 2>&1 && san=1 || san=0; if [ \"$san\" = 1 ]; then flags='-fsanitize=address,undefined -fno-omit-frame-pointer'; else flags=''; fi; gcc --version | head -n 1; gcc -std=c11 -O1 -g $flags -I/out -I/repo/tests/ak820_keymap_firewall /repo/tests/ak820_keymap_firewall/harness.c -o /out/run-current; /out/run-current; for name in skipped_read reversed_reads boot_bypass; do gcc -std=c11 -O1 -g $flags -DCURRENT_INCLUDE=\\\"$name.inc\\\" -I/out -I/repo/tests/ak820_keymap_firewall /repo/tests/ak820_keymap_firewall/harness.c -o /out/run-mutant; if /out/run-mutant >/out/mutant.out 2>&1; then echo MUTANT_SURVIVED:$name; exit 21; fi; if ! grep -q '^DIFF ' /out/mutant.out; then cat /out/mutant.out; exit 22; fi; sed -n '1p' /out/mutant.out | sed \"s/^/MUTANT_REJECTED:$name:/\"; done; echo RUNNER_SANITIZERS=$san"
            command = [docker, "run", "--rm", "--pull=never", "--network=none", "--userns=host", "--user", f"{os.getuid()}:{os.getgid()}", "-v", f"{REPO}:/repo:ro", "-v", f"{tmpdir}:/out:rw", image_id, "sh", "-c", command_script]
            result = run(command, cwd=tmpdir, capture=True)
            if result.returncode:
                sys.stdout.write(result.stdout or "")
                fail("offline Docker harness or mutant check failed")
            lines = (result.stdout or "").splitlines()
            compiler_line = next((line for line in lines if line.startswith("gcc ")), "unknown")
            sanitizer_line = next((line.split("=", 1)[1] for line in lines if line.startswith("RUNNER_SANITIZERS=")), "0")
            compiler_evidence = {"compiler": compiler_line, "sanitizers": sanitizer_line == "1", "container_image_sha256": image_id}
            mutant_evidence = {}
            for name in ("skipped_read", "reversed_reads", "boot_bypass"):
                line = next((entry for entry in lines if entry.startswith(f"MUTANT_REJECTED:{name}:")), None)
                if line is None:
                    fail(f"Docker run did not confirm mutant rejection: {name}")
                mutant_evidence[name] = {"status": "REJECTED", "first_difference": line.split(":", 2)[2]}
            result = subprocess.CompletedProcess([], 0, "\n".join(lines), None)
        evidence = {
            "status": "PASS", **compiler_evidence,
            "base_oracle_commit": BASE_COMMIT,
            "hashes": {"current_function_sha256": sha(current.encode()), "oracle_sha256": sha(oracle),
                       "harness_sha256": sha((TEST_DIR / "harness.c").read_bytes()),
                       "runner_sha256": sha((TEST_DIR / "run.py").read_bytes()),
                       **{f"{name}_file_sha256": sha(blob) for name, blob in blobs.items()}},
            "derived_constants": vals, "qk_boot_alias_drift_check": "REJECTED", "result": next((line for line in (result.stdout or "").splitlines() if line.startswith("PASS ")), ""),
            "mutant_checks": mutant_evidence,
            "fault_model_limits": "EEPROM read faults return 0xFF and set a sticky mock flag at the selected read occurrence; writer faults and durable backend behavior are not modeled.",
        }
        print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
