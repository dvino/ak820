#!/usr/bin/env python3
"""Verify the optional compact XZ generator without changing JSON or codecs."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import random
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def header(path):
    return bytes(int(value, 16) for value in re.findall(r"0x([0-9a-fA-F]{2})", path.read_text()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root, out = args.source_root.resolve(), args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    generator = root / "util/vial_generate_definition.py"
    definition = root / "keyboards/ajazz/ak820/keymaps/vial/vial.json"
    spec = importlib.util.spec_from_file_location("ak820_compact_definition", generator)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    baseline = out / "rc4-generator.py"
    baseline.write_bytes(subprocess.check_output(["git", "show", "cb9ff6ea:qmk-8051-ak820/util/vial_generate_definition.py"], cwd=ROOT.parent))
    old, default, compact = (out / name for name in ("rc4.h", "default.h", "compact.h"))
    for script, output, extra in ((baseline, old, []), (generator, default, []), (generator, compact, ["--compact-xz"])):
        subprocess.run([sys.executable, str(script), str(definition), str(output), *extra], check=True)
    assert default.read_bytes() == old.read_bytes(), "Default generator output changed"
    raw = json.dumps(json.loads(definition.read_text()), separators=(",", ":")).strip().encode("utf-8")
    rng = random.Random(820)
    long_pattern = "".join(chr(33 + rng.randrange(90)) for _ in range(8192))
    corpus = [raw, b"{}", b"", b"[]", b'{"name":"\\u0410"}',
              json.dumps({"pattern": long_pattern * 3}, separators=(",", ":")).encode()]
    tests = []
    for index, data in enumerate(corpus):
        original, encoded = module.compress_definition(data), module.compress_definition(data, True)
        assert original == lzma.compress(data) and len(encoded) <= len(original)
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
        assert decoder.decompress(encoded) == data and decoder.eof and not decoder.unused_data
        assert decoder.check == lzma.CHECK_CRC64
        external = subprocess.run(["xz", "--format=xz", "--decompress", "--stdout"], input=encoded, capture_output=True, check=True)
        assert external.stdout == data
        tests.append({"case": index, "pass": True, "raw_bytes": len(data), "default_bytes": len(original),
                      "compact_bytes": len(encoded), "kept_original": encoded == original,
                      "sha256": hashlib.sha256(encoded).hexdigest()})
    assert tests[-1]["kept_original"], "The larger-definition fallback was not exercised"
    assert header(compact) == module.compress_definition(raw, True)
    report = {"result": "PASS", "hardware_validated": False,
              "level": "actual generator CLI + Python/XZ CLI decoding; linked GUI round-trip in run.py",
              "baseline_commit": "cb9ff6ea", "default_header_unchanged": True,
              "codec": "XZ / LZMA2 / CRC64", "json_bytes": len(raw),
              "default_blob_bytes": len(header(default)), "compact_blob_bytes": len(header(compact)),
              "source_sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in (generator, definition, root / "builddefs/build_vial.mk", Path(__file__))},
              "tests": tests}
    (out / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("result", "default_header_unchanged", "codec", "json_bytes", "default_blob_bytes", "compact_blob_bytes")}))


if __name__ == "__main__":
    main()
