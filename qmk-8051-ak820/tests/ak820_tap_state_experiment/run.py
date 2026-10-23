#!/usr/bin/env python3
"""Compare real process_action bodies for the RC5 common-tail experiment.

The baseline comes from immutable RC4 Git history. The candidate is extracted
from the selected source file. Trace/state stubs cover output behavior, not
SDCC ABI, complete action_tapping timing, callbacks, or peripheral behavior.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPO = ROOT.parent
BASELINE_COMMIT = "cb9ff6ea"
BASELINE_BODY_SHA256 = "eb41bd65c82c2331c5430cbbdc9742cb55afdb1f3b4fcf5627ed3e1465b71b05"
PROFILES = {
    "active-disabled": ["NO_ACTION_TAPPING", "NO_ACTION_ONESHOT"],
    "tapping-oneshot": [],
    "hold-interrupt": ["HOLD_ON_OTHER_KEY_PRESS_PER_KEY"],
    "retro-interrupt": ["HOLD_ON_OTHER_KEY_PRESS_PER_KEY", "RETRO_TAPPING", "RETRO_TAPPING_PER_KEY", "DUMMY_MOD_NEUTRALIZER_KEYCODE=0"],
}


def body(text):
    start = text.index("void process_action(")
    # The original source contains unindented braces inside its One Shot
    # branch. A first closing-brace search would silently truncate it.
    end = text.index("\n/** \\brief Utilities for actions.", start)
    return text[start:end]


def sha(value):
    return hashlib.sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--candidate", type=Path, help="Candidate action.c (default: source-root/quantum/action.c)")
    parser.add_argument("--profile", choices=tuple(PROFILES), action="append")
    parser.add_argument("--output", type=Path, help="JSON report to write")
    args = parser.parse_args()
    root = args.source_root.resolve()
    candidate_path = (args.candidate or root / "quantum/action.c").resolve()
    baseline_source = subprocess.check_output(["git", "show", BASELINE_COMMIT + ":qmk-8051-ak820/quantum/action.c"], cwd=REPO, text=True)
    baseline = body(baseline_source)
    predicate_start = baseline_source.index("bool is_tap_action(")
    predicate_end = baseline_source.index("\n}", predicate_start) + 2
    predicate = baseline_source[predicate_start:predicate_end]
    candidate = body(candidate_path.read_text())
    if sha(baseline.encode()) != BASELINE_BODY_SHA256:
        raise ValueError("Unexpected immutable baseline body")
    if candidate == baseline:
        raise ValueError("Candidate equals the baseline; select the actual common-tail action.c")
    harness = (HERE / "harness.c").read_text().replace("/* IS_TAP_ACTION */", predicate)
    source = harness.replace("/* FUNCTIONS */", baseline.replace("void process_action(", "void baseline_action(", 1) + "\n" + candidate.replace("void process_action(", "void factored_action(", 1))
    results = []
    with tempfile.TemporaryDirectory(prefix="ak820-common-action-") as tmp:
        work = Path(tmp)
        generated = work / "compare.c"
        generated.write_text(source)
        for name in args.profile or PROFILES:
            binary = work / name
            argv = [os.environ.get("CC", "cc"), "-std=gnu11", "-O2", "-Wall", "-Wextra", "-Wno-unused-function", "-Wno-unused-variable", "-Wno-unused-label",
                    "-fsanitize=undefined", "-fno-sanitize-recover=undefined", "-I" + str(root / "quantum"), *["-D" + value for value in PROFILES[name]], str(generated), "-o", str(binary)]
            subprocess.run(argv, check=True)
            result = subprocess.run([str(binary)], text=True, capture_output=True)
            print(name + ": " + result.stdout.strip() + result.stderr.strip(), flush=True)
            result.check_returncode()
            results.append({"profile": name, "pass": True, "summary": result.stdout.strip()})
    report = {
        "pass": True,
        "level": "Host C/UBSan: real process_action bodies, differential call traces/final state/record; no SDCC ABI or timing proof",
        "coverage": "Every 16-bit action payload in LMODS/RMODS/LMODS_TAP/RMODS_TAP/LAYER_MODS/LAYER_TAP/LAYER_TAP_EXT; both directions, all 16 tap counts, 16 state seeds per profile",
        "baseline_commit": BASELINE_COMMIT,
        "baseline_body_sha256": sha(baseline.encode()),
        "tap_predicate_sha256": sha(predicate.encode()),
        "candidate_body_sha256": sha(candidate.encode()),
        "candidate_file_sha256": sha(candidate_path.read_bytes()),
        "harness_sha256": sha((HERE / "harness.c").read_bytes()),
        "runner_sha256": sha(Path(__file__).read_bytes()),
        "tests": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
