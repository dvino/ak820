#!/usr/bin/env python3
"""Compile a harness containing exact VIA field-helper and bulk case source."""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "qmk-8051-ak820" / "quantum" / "via.c"
HARNESS = Path(__file__).with_name("harness.c")


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    i = opening
    state = "code"
    while i < len(text):
        c = text[i]
        n = text[i + 1] if i + 1 < len(text) else ""
        if state == "code":
            if c == "/" and n == "*":
                state = "comment"
                i += 2
                continue
            if c == "/" and n == "/":
                state = "line"
                i += 2
                continue
            if c == '"':
                state = "string"
            elif c == "'":
                state = "char"
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        elif state == "comment" and c == "*" and n == "/":
            state = "code"
            i += 2
            continue
        elif state == "line" and c == "\n":
            state = "code"
        elif state in ("string", "char"):
            if c == "\\":
                i += 2
                continue
            if (state == "string" and c == '"') or (state == "char" and c == "'"):
                state = "code"
        i += 1
    raise ValueError("unclosed C brace")


def extract_case(text: str, name: str) -> str:
    match = re.search(rf"\bcase\s+{re.escape(name)}\s*:\s*\{{", text)
    if not match:
        raise ValueError(f"missing case {name}")
    opening = text.index("{", match.start())
    end = matching_brace(text, opening)
    return text[match.start():end + 1]


def main() -> int:
    source = SOURCE.read_text()
    template = HARNESS.read_text()
    replacements = {}
    cases = (
        "id_dynamic_keymap_macro_get_buffer",
        "id_dynamic_keymap_macro_set_buffer",
        "id_dynamic_keymap_get_buffer",
        "id_dynamic_keymap_set_buffer",
    )
    for index, name in enumerate(cases):
        replacements[f"/*__CASE_{index}__*/"] = extract_case(source, name)
    for marker, value in replacements.items():
        if template.count(marker) != 1:
            raise ValueError(f"expected one marker: {marker}")
        template = template.replace(marker, value)
    with tempfile.TemporaryDirectory(prefix="ak820-via-decode-") as temp:
        c_file = Path(temp) / "harness.c"
        binary = Path(temp) / "harness"
        c_file.write_text(template)
        subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", str(c_file), "-o", str(binary)], check=True)
        subprocess.run([str(binary)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
