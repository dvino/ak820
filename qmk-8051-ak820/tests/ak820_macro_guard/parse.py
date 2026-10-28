#!/usr/bin/env python3
"""Exhaustively compare the production upload parser to its pre-change logic."""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
source = (root / 'keyboards/ajazz/ak820/ak820_macro.c').read_text()
start = source.index('static bool parse_byte(')
end = source.index('\n}\n', start) + 2
production = source[start:end]
fixture = '''#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#define AK820_XDATA
#define DYNAMIC_KEYMAP_MACRO_COUNT 16
typedef struct { uint8_t terminated, arguments; } macro_parse_t;
'''+production+'''
/* Independent immutable pre-change reference; preserve failure side effects. */
static bool reference(macro_parse_t *state, uint8_t value) {
    if (state->terminated == DYNAMIC_KEYMAP_MACRO_COUNT) return value == 0;
    if (state->arguments == 3) {
        if (value < 1 || value > 7) return false;
        state->arguments = value <= 3 ? 1 : 2;
    } else if (state->arguments) {
        if (!value) return false;
        --state->arguments;
    } else if (!value) {
        ++state->terminated;
    } else if (value == 1) {
        state->arguments = 3;
    } else if (value >= 128) {
        return false;
    }
    return true;
}
int main(void) {
    for (unsigned term = 0; term < 256; ++term)
        for (unsigned arg = 0; arg < 256; ++arg)
            for (unsigned value = 0; value < 256; ++value) {
                macro_parse_t actual = {term, arg}, expected = actual;
                bool a = parse_byte(&actual, value);
                bool b = reference(&expected, value);
                if (a != b || actual.terminated != expected.terminated ||
                    actual.arguments != expected.arguments) {
                    fprintf(stderr, "mismatch: term=%u arg=%u value=%u\\n", term, arg, value);
                    return 1;
                }
            }
    puts("macro parse differential: 16777216 cases passed");
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-macro-parse-') as folder:
    path = Path(folder)
    (path / 'test.c').write_text(fixture)
    subprocess.run([os.environ.get('CC', 'cc'), '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                    str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True)
