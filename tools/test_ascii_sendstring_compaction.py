"""Equivalence checks for AK820's packed ASCII keycode/Shift table."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "qmk-8051-ak820/quantum/send_string/send_string.c"


def initializer(source: str, name: str, occurrence: int = 0) -> list[str]:
    matches = list(re.finditer(rf"\b{re.escape(name)}\s*\[\s*\d+\s*\][^=]*=\s*\{{", source))
    match = matches[occurrence]
    start = match.end()
    end = source.index("};", start)
    body = re.sub(r"//[^\n]*", "", source[start:end])
    entries = []
    depth = 0
    entry_start = 0
    for position, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            entry = body[entry_start:position].strip()
            if entry:
                entries.append(entry)
            entry_start = position + 1
    tail = body[entry_start:].strip()
    if tail:
        entries.append(tail)
    return entries


def function(source: str, declaration: str) -> str:
    start = source.index(declaration)
    opening = source.index("{", start)
    depth = 0
    for position in range(opening, len(source)):
        if source[position] == "{":
            depth += 1
        elif source[position] == "}":
            depth -= 1
            if depth == 0:
                return source[start : position + 1]
    raise AssertionError(f"unterminated function: {declaration}")


def shift_bits(source: str) -> list[int]:
    marker = "ascii_to_shift_lut[16]"
    start = source.index(marker)
    end = source.index("};", start)
    block = source[start:end]
    bits = [int(bit) for row in re.findall(r"KCLUT_ENTRY\(([^)]*)\)", block) for bit in row.split(",")]
    if len(bits) != 128:
        raise AssertionError(f"expected 128 Shift bits, found {len(bits)}")
    return bits


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value)


def lut_values(source: str, name: str) -> list[str]:
    entries = initializer(source, name)
    values = []
    for entry in entries:
        match = re.fullmatch(r"KCLUT_ENTRY\(([^)]*)\)", entry)
        if match:
            bits = [int(bit.strip()) for bit in match.group(1).split(",")]
            values.append(str(sum(bit << index for index, bit in enumerate(bits))))
        else:
            values.append(entry)
    return values


def c_harness(
    send_char: str,
    keycodes: list[str],
    shift: list[str],
    altgr: list[str],
    dead: list[str],
    *,
    target_sdcc: bool,
) -> str:
    names = {"XXXXXXX"}
    for entry in keycodes + shift + altgr + dead:
        names.update(re.findall(r"\b(?:KC_[A-Z0-9_]+|XXXXXXX)\b", entry))
    names.update({"KC_LEFT_SHIFT", "KC_RIGHT_ALT", "KC_SPACE"})
    names.discard("XXXXXXX")
    definitions = ["#define XXXXXXX 0"]
    definitions.extend(f"#define {name} {index}" for index, name in enumerate(sorted(names), 1))
    return f'''#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#define AK820_BOARD 1
{'#define __SDCC_mcs51 1' if target_sdcc else ''}
#define PROGMEM
#define pgm_read_byte(p) (*(p))
{chr(10).join(definitions)}
const uint8_t ascii_to_keycode_lut[128] = {{{", ".join(keycodes)}}};
const uint8_t ascii_to_shift_lut[16] = {{{", ".join(shift)}}};
const uint8_t ascii_to_altgr_lut[16] = {{{", ".join(altgr)}}};
const uint8_t ascii_to_dead_lut[16] = {{{", ".join(dead)}}};
const uint8_t ascii_bit_mask_lut[8] = {{1, 2, 4, 8, 16, 32, 64, 128}};
static unsigned count;
static unsigned char event_type[8];
static uint8_t event_code[8];
static void emit(unsigned char type, uint8_t code) {{ event_type[count] = type; event_code[count++] = code; }}
void register_code(uint8_t code) {{ emit('R', code); }}
void unregister_code(uint8_t code) {{ emit('U', code); }}
void tap_code(uint8_t code) {{ emit('T', code); }}
{send_char}
int main(void) {{
    for (unsigned i = 0; i < 128; ++i) {{
        count = 0;
        send_char((char)i);
        printf("%u", i);
        for (unsigned j = 0; j < count; ++j) printf(" %c:%u", event_type[j], event_code[j]);
        putchar('\\n');
    }}
    return 0;
}}
'''


def run_harness(source: str) -> list[str]:
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if not compiler:
        raise unittest.SkipTest("a native C compiler is required for send_char execution equivalence")
    with tempfile.TemporaryDirectory(prefix="ascii-sendstring-") as temporary:
        c_file = Path(temporary) / "harness.c"
        executable = Path(temporary) / "harness"
        c_file.write_text(source)
        subprocess.run([compiler, "-std=c99", "-Wall", "-Werror", str(c_file), "-o", str(executable)], check=True)
        result = subprocess.run([str(executable)], check=True, capture_output=True, text=True)
        return result.stdout.splitlines()


class ASCIICompactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = SOURCE.read_text()

    def test_all_ascii_inputs_execute_same_key_and_modifier_events(self) -> None:
        # The generic declaration remains intact under the target table's #else
        # branch, so this oracle is independent of the repository's Git history.
        original_keycodes = initializer(self.current, "ascii_to_keycode_lut", occurrence=1)
        current_keycodes = initializer(self.current, "ascii_to_keycode_lut", occurrence=0)
        original_shift = lut_values(self.current, "ascii_to_shift_lut")
        original_altgr = lut_values(self.current, "ascii_to_altgr_lut")
        original_dead = lut_values(self.current, "ascii_to_dead_lut")

        self.assertEqual(len(original_keycodes), 128)
        self.assertEqual(len(current_keycodes), 128)
        old_function = function(self.current, "void send_char(char ascii_code)")
        new_function = function(self.current, "void send_char(char ascii_code)")
        expected = run_harness(
            c_harness(old_function, original_keycodes, original_shift, original_altgr, original_dead, target_sdcc=False)
        )
        actual = run_harness(
            c_harness(new_function, current_keycodes, original_shift, original_altgr, original_dead, target_sdcc=True)
        )
        self.assertEqual(actual, expected)

    def test_negative_control_detects_lost_shift_bit(self) -> None:
        current_keycodes = initializer(self.current, "ascii_to_keycode_lut", occurrence=0)
        self.assertIn("0x80", current_keycodes[ord("!")])
        current_keycodes[ord("!")] = re.sub(r"\|\s*0x80", "", current_keycodes[ord("!")])
        target_function = function(self.current, "void send_char(char ascii_code)")
        old_shift = lut_values(self.current, "ascii_to_shift_lut")
        old_altgr = lut_values(self.current, "ascii_to_altgr_lut")
        old_dead = lut_values(self.current, "ascii_to_dead_lut")
        mutated = run_harness(
            c_harness(target_function, current_keycodes, old_shift, old_altgr, old_dead, target_sdcc=True)
        )

        original_keycodes = initializer(self.current, "ascii_to_keycode_lut", occurrence=1)
        baseline = run_harness(
            c_harness(
                function(self.current, "void send_char(char ascii_code)"),
                original_keycodes,
                old_shift,
                old_altgr,
                old_dead,
                target_sdcc=False,
            )
        )
        self.assertNotEqual(mutated, baseline)

    def test_string_delay_parser_and_wait_order_are_unchanged(self) -> None:
        body = function(self.current, "void send_string_with_delay(")
        required_order = (
            "if (!ascii_code) break;",
            "if (ascii_code == SS_QMK_PREFIX)",
            "ascii_code = *(++string);",
            "if (ascii_code == SS_TAP_CODE)",
            "} else if (ascii_code == SS_DELAY_CODE)",
            "while (isdigit(keycode))",
            "while (ms--)\n                    wait_ms(1);",
            "send_char(ascii_code);",
            "// interval",
            "while (ms--)\n                wait_ms(1);",
        )
        positions = [body.index(fragment) for fragment in required_order]
        self.assertEqual(positions, sorted(positions))

    def test_lookup_entries_preserve_original_keycode_and_shift_ownership(self) -> None:
        old_keys = initializer(self.current, "ascii_to_keycode_lut", occurrence=1)
        new_keys = initializer(self.current, "ascii_to_keycode_lut", occurrence=0)
        bits = shift_bits(self.current)
        self.assertEqual((len(old_keys), len(new_keys), len(bits)), (128, 128, 128))
        for index, (old, new, shifted) in enumerate(zip(old_keys, new_keys, bits)):
            expected = f"({old} | 0x80)" if shifted else old
            self.assertEqual(normalized(new), normalized(expected), f"ASCII index {index}")


if __name__ == "__main__":
    unittest.main()
